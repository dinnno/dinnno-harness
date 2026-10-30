#!/usr/bin/env python3
"""dinnno gpu — GPU ledger and queue shared by every session on every machine. Called as `dinnno gpu <cmd>`.

  ls [HOST...]                              GPUs, running / waiting runs, holds, GPU processes outside the ledger
  where --mem G --hours H                   which host takes a run of that size now, or how far back in line it stands
  run --host H --mem G --hours H [--gpu I] [--ram G] [--cwd PATH] [--prio N] [--project P] -- CMD...
                                            queue CMD on H; a waiter on H starts it when its turn comes and it fits
  hold --host H --mem G --from "YYYY-MM-DD HH:MM" --hours H [--gpu I] [--note TEXT] [--project P]
                                            reserve GPU memory for a time window (manual hosts: record a web reservation)
  cancel --host H ID                        drop a waiting run or a hold
  wait --host H ID [--until start|end] [--timeout S]

--mem is the probe peak of the run; it starts only when the GPU has 1.5x that free (capped at the card size minus 1G),
after reserving room for the runs ahead of it in line and for other projects' holds that overlap its --hours.
The ledger lives on each GPU host (~/.dinnno/gpu/ledger.json) so runs launched from any machine share one queue.
This file is piped to the host over ssh and run there as `_host <op>`; nothing is installed on the hosts.
Hosts come from config/gpu_hosts.json ($DINNNO_GPU_HOSTS overrides).
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import datetime as dt
import fcntl
import json
import os
import pwd
import secrets
import shlex
import signal
import socket
import subprocess
import sys
import time
from contextlib import contextmanager
from pathlib import Path

SELF = Path(__file__).resolve()
STATE = Path.home() / ".dinnno/gpu"
LEDGER, LOCK, HIST, LOGS = STATE / "ledger.json", STATE / "lock", STATE / "history.jsonl", STATE / "logs"
POLL = 30


# ---------------------------------------------------------------- host side (runs on the GPU machine)

@contextmanager
def ledger():
    STATE.mkdir(parents=True, exist_ok=True)
    with open(LOCK, "w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        box = {"entries": json.loads(LEDGER.read_text())["entries"] if LEDGER.exists() else []}
        yield box
        tmp = LEDGER.with_suffix(".tmp")
        tmp.write_text(json.dumps(box, indent=1, ensure_ascii=False))
        tmp.replace(LEDGER)


def history(e, **kw):
    with open(HIST, "a") as f:
        f.write(json.dumps({**e, **kw}, ensure_ascii=False) + "\n")


def smi(query):
    out = subprocess.run(["nvidia-smi", query, "--format=csv,noheader,nounits"],
                         capture_output=True, text=True, timeout=15).stdout
    return [[x.strip() for x in l.split(",")] for l in out.strip().splitlines() if l.strip()]


def gib(x):
    try: return float(x) / 1024
    except ValueError: return 0.0  # [N/A]


def proc_info(pid):
    def rd(name):
        try: return Path(f"/proc/{pid}/{name}").read_bytes()
        except OSError: return b""
    try: user = pwd.getpwuid(os.stat(f"/proc/{pid}").st_uid).pw_name
    except (OSError, KeyError): user = "?"
    try: cwd = os.readlink(f"/proc/{pid}/cwd")
    except OSError: cwd = ""
    try: pgid = os.getpgid(pid)
    except OSError: pgid = -1
    start = 0.0
    stat = rd("stat").decode(errors="replace")
    if stat:
        ticks = int(stat.rsplit(")", 1)[1].split()[19])
        btime = next(int(l.split()[1]) for l in open("/proc/stat") if l.startswith("btime"))
        start = btime + ticks / os.sysconf("SC_CLK_TCK")
    return {"pid": pid, "pgid": pgid, "user": user, "cwd": cwd, "project": project_of(cwd),
            "cmd": rd("cmdline").replace(b"\0", b" ").decode(errors="replace").strip()[:90], "start": start}


def project_of(d):
    x = d
    while x and x != "/":
        if os.path.exists(x + "/docs/RESEARCH_SPEC.md") or os.path.exists(x + "/.git"): return os.path.basename(x)
        x = os.path.dirname(x)
    return d.replace(str(Path.home()), "~") or "?"


def snapshot():
    gs = [{"i": int(i), "uuid": u, "name": n, "used": gib(a), "total": gib(b)}
          for i, u, n, a, b in smi("--query-gpu=index,uuid,name,memory.used,memory.total")]
    by_uuid = {g["uuid"]: g["i"] for g in gs}
    aps = [{**proc_info(int(pid)), "gpu": by_uuid.get(u), "used": gib(m)}
           for u, pid, m in smi("--query-compute-apps=gpu_uuid,pid,used_memory")]
    return gs, aps


def alive(pid, group=False):
    try: (os.killpg if group else os.kill)(pid, 0)
    except ProcessLookupError: return False
    except PermissionError: pass
    return True


def sweep(box):
    keep, now = [], time.time()
    for e in box["entries"]:
        if e["kind"] == "hold" and e["until"] <= now: continue
        if e["kind"] == "run" and not alive(e["waiter"]):
            if e["state"] == "wait": history(e, ended=now, outcome="waiter lost before start"); continue
            if not alive(e["pgid"], group=True): history(e, ended=now, outcome="exited, rc unknown"); continue
        keep.append(e)
    box["entries"] = keep


def need(mem, total):
    return min(mem * 1.5, total - 1)


def plan(entries, gs, aps, now, kind):
    """Walk the waiting line in order. Returns {run id: gpu index it starts on now, or None}.

    A run that does not fit blocks the GPUs it could use for everyone behind it (strict FIFO per GPU),
    so a large run is not starved by small ones slipping past."""
    avail = {g["i"]: g["total"] - g["used"] for g in gs}
    total = {g["i"]: g["total"] for g in gs}
    for e in entries:  # a started run whose memory has not ramped up yet still owns its --mem
        if e["kind"] == "run" and e["state"] == "run" and e["gpu"] in avail:
            seen = sum(a["used"] for a in aps if a["pgid"] == e["pgid"])
            avail[e["gpu"]] -= max(0.0, e["mem"] - seen)
    holds = [e for e in entries if e["kind"] == "hold"]

    def room(e, g):
        end = now + e["hours"] * 3600
        if kind == "manual":  # only inside our own web reservation
            mine = any(h["gpu"] == g and h["project"] == e["project"] and h["from"] <= now < h["until"] for h in holds)
            return avail[g] if mine else float("-inf")
        return avail[g] - sum(h["mem"] for h in holds
                              if h["gpu"] == g and h["project"] != e["project"] and h["from"] < end and h["until"] > now)

    def in_own_hold(e):  # a run inside its project's active hold goes first: the hold is its slot
        return any(h["project"] == e["project"] and h["from"] <= now < h["until"] for h in holds)

    blocked, out = set(), {}
    for e in sorted((e for e in entries if e["kind"] == "run" and e["state"] == "wait"),
                    key=lambda e: (not in_own_hold(e), -e["prio"], e["created"])):
        cands = [g for g in ([e["gpu"]] if e["gpu"] is not None else avail) if g in avail and g not in blocked]
        fit = [g for g in cands if room(e, g) >= need(e["mem"], total[g])]
        if fit:
            g = max(fit, key=lambda g: room(e, g))
            out[e["id"]] = g
            avail[g] -= e["mem"]
        else:
            out[e["id"]] = None
            blocked.update(cands)
    return out


def launch(e, g):
    LOGS.mkdir(parents=True, exist_ok=True)
    pre = ["systemd-run", "--user", "--scope", "-q", "-p", f"MemoryMax={e['ram']}G", "--"] if e["ram"] else []
    env = dict(os.environ, CUDA_DEVICE_ORDER="PCI_BUS_ID", CUDA_VISIBLE_DEVICES=str(g))
    with open(e["log"], "ab") as log:
        return subprocess.Popen(pre + ["bash", "-c", e["cmd"]], cwd=e["cwd"], env=env, stdin=subprocess.DEVNULL,
                                stdout=log, stderr=subprocess.STDOUT, start_new_session=True)


def op_waiter(p):
    eid = p["id"]
    while True:
        with ledger() as box:
            sweep(box)
            e = next((x for x in box["entries"] if x["id"] == eid), None)
            if e is None: return {}
            gs, aps = snapshot()
            g = plan(box["entries"], gs, aps, time.time(), e["hostkind"]).get(eid)
            if g is not None:
                proc = launch(e, g)
                e.update(state="run", gpu=g, pgid=proc.pid, started=time.time())
                break
        time.sleep(POLL)
    rc = proc.wait()
    with ledger() as box:
        box["entries"] = [x for x in box["entries"] if x["id"] != eid]
    history(e, ended=time.time(), outcome=f"rc={rc}")
    return {}


def op_status(p):
    with ledger() as box:
        sweep(box)
        entries = box["entries"]
    gs, aps = snapshot()
    order = plan(entries, gs, aps, time.time(), p["kind"])
    tracked = {e["pgid"] for e in entries if e["kind"] == "run" and e["state"] == "run"}
    mem = {l.split(":")[0]: int(l.split()[1]) / 2**20 for l in open("/proc/meminfo")}
    hist = [json.loads(l) for l in HIST.read_text().splitlines()[-30:]] if HIST.exists() else []
    return {"gpus": gs, "apps": aps, "entries": entries, "order": order, "hist": hist,
            "untracked": [a for a in aps if a["pgid"] not in tracked],
            "ram": [mem["MemAvailable"], mem["MemTotal"]], "now": time.time()}


def linger():
    out = subprocess.run(["loginctl", "show-user", pwd.getpwuid(os.getuid()).pw_name, "-p", "Linger"],
                         capture_output=True, text=True).stdout
    return out.strip() == "Linger=yes"


def op_submit(p):
    e, warn = dict(p["entry"]), []
    gs, _ = snapshot()
    gidx = [g["i"] for g in gs]
    if e["gpu"] is not None and e["gpu"] not in gidx: raise SystemExit(f"GPU{e['gpu']} 없음 (있는 것: {gidx})")
    e["id"] = secrets.token_hex(3)
    e["created"] = time.time()
    if e["kind"] == "run":
        if not os.path.isdir(e["cwd"]): raise SystemExit(f"cwd 없음: {e['cwd']}")
        if max(g["total"] for g in gs) < e["mem"]: raise SystemExit(f"--mem {e['mem']}G는 이 머신의 어느 GPU에도 안 들어간다")
        if e["ram"] and not (p["local"] or linger()):
            warn.append("이 머신은 linger가 꺼져 있어 systemd --user scope가 ssh 종료와 함께 죽는다 — RAM 상한 없이 띄운다")
            e["ram"] = None
        e.update(state="wait", pgid=None, log=e["log"] or str(LOGS / f"{e['id']}.log"))
        with ledger() as box:
            sweep(box)
            w = subprocess.Popen([sys.executable, str(SELF), "_host", "waiter", json.dumps({"id": e["id"]})],
                                 stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                 start_new_session=True)
            e["waiter"] = w.pid
            box["entries"].append(e)
            ahead = sum(1 for x in box["entries"] if x["kind"] == "run" and x["state"] == "wait") - 1
    else:
        if e["gpu"] is None:
            if len(gidx) > 1: raise SystemExit(f"GPU가 {len(gidx)}장이다 — --gpu로 고른다")
            e["gpu"] = gidx[0]
        total = next(g["total"] for g in gs if g["i"] == e["gpu"])
        with ledger() as box:
            sweep(box)
            clash = [h for h in box["entries"] if h["kind"] == "hold" and h["gpu"] == e["gpu"]
                     and h["from"] < e["until"] and h["until"] > e["from"]]
            if p["kind"] == "queue" and sum(h["mem"] for h in clash) + e["mem"] > total:
                raise SystemExit("겹치는 예약과 합치면 GPU 용량을 넘는다: "
                                 + ", ".join(f"{h['project']} {h['mem']:.0f}G {fmt(h['from'])}~{fmt(h['until'])}" for h in clash))
            box["entries"].append(e)
            ahead = 0
    return {"id": e["id"], "log": e.get("log"), "ahead": ahead, "warn": warn}


def op_cancel(p):
    with ledger() as box:
        e = next((x for x in box["entries"] if x["id"] == p["id"]), None)
        if e is None: raise SystemExit(f"장부에 없음: {p['id']}")
        if e["kind"] == "run" and e["state"] == "run":
            raise SystemExit(f"이미 실행 중이다. 끄려면 사용자 확인 후 그 머신에서 kill -- -{e['pgid']}")
        box["entries"].remove(e)
        if e["kind"] == "run":
            try: os.kill(e["waiter"], signal.SIGTERM)
            except ProcessLookupError: pass
            history(e, ended=time.time(), outcome="cancelled")
    return {"id": p["id"]}


HOST_OPS = {"status": op_status, "submit": op_submit, "cancel": op_cancel, "waiter": op_waiter}


# ---------------------------------------------------------------- client side

def fmt(t):
    return dt.datetime.fromtimestamp(t).strftime("%m-%d %H:%M")


def hosts():
    path = os.environ.get("DINNNO_GPU_HOSTS") or SELF.parent.parent / "config/gpu_hosts.json"
    return {h["name"]: h for h in json.loads(Path(path).read_text())["hosts"]}


def is_local(h):
    return socket.gethostname() == h["hostname"]


def call(h, op, payload, timeout=40):
    payload = {"kind": h["kind"], "local": is_local(h), **payload}
    if is_local(h):
        cmd, inp = [sys.executable, str(SELF), "_host", op, json.dumps(payload)], None
    else:
        d = "~/.dinnno/gpu"
        remote = (f"mkdir -p {d} && cat > {d}/.new.$$ && mv {d}/.new.$$ {d}/dinnno_gpu.py && "
                  f"exec python3 {d}/dinnno_gpu.py _host {op} {shlex.quote(json.dumps(payload))}")
        cmd, inp = ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=8", h["ssh"], remote], SELF.read_bytes()
    try:
        r = subprocess.run(cmd, input=inp, capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"{h['name']}: {timeout}s 안에 응답 없음")
    if r.returncode:
        raise RuntimeError(f"{h['name']}: {(r.stderr.decode(errors='replace').strip().splitlines() or ['exit ' + str(r.returncode)])[-1]}")
    return json.loads(r.stdout)


def slurm_status(h):
    r = subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=8", h["ssh"],
                        'squeue -u "$USER" -h -o "%i|%j|%T|%M|%l|%b"'], capture_output=True, text=True, timeout=20)
    if r.returncode: raise RuntimeError(f"{h['name']}: {(r.stderr.strip().splitlines() or ['exit ' + str(r.returncode)])[-1]}")
    return [l.split("|") for l in r.stdout.strip().splitlines()]


def dday(h):
    if not h.get("until"): return ""
    return f"사용 종료 {h['until']} (D-{(dt.date.fromisoformat(h['until']) - dt.date.today()).days})"


def local_project():
    return project_of(os.getcwd())


def gather(names):
    hs = hosts()
    def one(n):
        h = hs[n]
        try: return n, (slurm_status(h) if h["kind"] == "slurm" else call(h, "status", {})), None
        except (RuntimeError, subprocess.TimeoutExpired) as ex: return n, None, str(ex)
    with cf.ThreadPoolExecutor(len(names)) as ex:
        return [(hs[n], *rest) for n, *rest in ex.map(one, names)]


def show(h, st, err):
    head = {"queue": "장부·대기열", "manual": "웹 예약(사람)", "slurm": "Slurm"}[h["kind"]]
    extra = " — ".join(x for x in (h.get("note", ""), dday(h)) if x)
    print(f"\n■ {h['name']} [{head}]" + (f" — {extra}" if extra else ""))
    if err: print(f"  접속 실패: {err}"); return
    if h["kind"] == "slurm":
        for jid, name, state, used, limit, gres in st: print(f"  job {jid} {name} {state} {used}/{limit} {gres}")
        if not st: print("  내 job 없음")
        return
    for g in st["gpus"]:
        print(f"  GPU{g['i']} {g['name'].replace('NVIDIA ', '')}: {g['used']:.1f}/{g['total']:.0f}G 사용, 여유 {g['total'] - g['used']:.1f}G")
    runs = [e for e in st["entries"] if e["kind"] == "run"]
    for e in sorted(runs, key=lambda e: e.get("started") or 0):
        if e["state"] == "run":
            print(f"  실행  {e['id']} {e['project']:<14} GPU{e['gpu']} {e['mem']:.0f}G  시작 {fmt(e['started'])}  예상 종료 {fmt(e['started'] + e['hours'] * 3600)}")
    waiting = sorted((e for e in runs if e["state"] == "wait"), key=lambda e: (-e["prio"], e["created"]))
    for k, e in enumerate(waiting, 1):  # display order; a run inside its own hold actually goes first (see plan)
        g = "?" if e["gpu"] is None else e["gpu"]
        print(f"  대기#{k} {e['id']} {e['project']:<14} GPU{g} {e['mem']:.0f}G {e['hours']:g}h  등록 {fmt(e['created'])}"
              + ("  → 다음 확인 때 시작" if st["order"].get(e["id"]) is not None else ""))
    for e in sorted((e for e in st["entries"] if e["kind"] == "hold"), key=lambda e: e["from"]):
        print(f"  예약  {e['id']} {e['project']:<14} GPU{e['gpu']} {e['mem']:.0f}G  {fmt(e['from'])} ~ {fmt(e['until'])}"
              + (f"  ({e['note']})" if e.get("note") else ""))
    groups = {}
    for a in st["untracked"]:
        k = (a["gpu"], a["user"], a["project"])
        groups.setdefault(k, []).append(a)
    for (g, user, proj), ps in sorted(groups.items(), key=lambda kv: -sum(a["used"] for a in kv[1])):
        oldest = min(a["start"] for a in ps) or st["now"]
        print(f"  장부밖 GPU{g} {proj}({user}) {sum(a['used'] for a in ps):.1f}G {len(ps)}개, {(st['now'] - oldest) / 3600:.1f}h째 — {ps[0]['cmd'][:60]}")
    print(f"  RAM 가용 {st['ram'][0]:.0f}/{st['ram'][1]:.0f}G")


def cmd_ls(a):
    hs = hosts()
    for h, st, err in gather(a.hosts or list(hs)):
        show(h, st, err)


def cmd_where(a):
    proj, now = a.project or local_project(), time.time()
    hyp = {"id": "?", "kind": "run", "state": "wait", "project": proj, "mem": a.mem, "hours": a.hours,
           "gpu": None, "prio": 0, "created": now + 1}
    for h, st, err in gather(list(hosts())):
        tag = f"{h['name']:<8}"
        if err: print(f"{tag} 접속 실패 — {err}"); continue
        if h["kind"] == "slurm": print(f"{tag} Slurm(sbatch)로 낸다 — 내 job {len(st)}개, {dday(h)}"); continue
        fits = [g for g in st["gpus"] if g["total"] >= a.mem]
        if not fits: print(f"{tag} 안 들어감 (가장 큰 GPU {max(g['total'] for g in st['gpus']):.0f}G)"); continue
        if h["kind"] == "manual":
            free = [f"GPU{g['i']}({g['total'] - g['used']:.0f}G)" for g in st["gpus"] if g["total"] - g["used"] >= need(a.mem, g["total"])]
            print(f"{tag} 웹 예약이 필요하다 — 지금 비어 보이는 GPU: {', '.join(free) or '없음'}"); continue
        g = plan(st["entries"] + [hyp], st["gpus"], st["apps"], now, "queue").get("?")
        if g is not None:
            free = next(x for x in st["gpus"] if x["i"] == g)
            print(f"{tag} 지금 들어간다 — GPU{g}, 여유 {free['total'] - free['used']:.1f}G (필요 {need(a.mem, free['total']):.0f}G)")
            continue
        ahead = sum(1 for e in st["entries"] if e["kind"] == "run" and e["state"] == "wait")
        ends = [e["started"] + e["hours"] * 3600 for e in st["entries"] if e["kind"] == "run" and e["state"] == "run"]
        print(f"{tag} 줄 선다 — 앞 대기 {ahead}개, 장부 run 종료 예상 {', '.join(fmt(t) for t in sorted(ends)) or '없음(장부 밖 점유가 비켜야 함)'}")


def parse_when(s):
    return time.time() if s == "now" else dt.datetime.strptime(s, "%Y-%m-%d %H:%M").timestamp()


def cmd_run(a):
    h = hosts()[a.host]
    if h["kind"] == "slurm": raise SystemExit(f"{a.host}는 Slurm이다 — sbatch로 낸다")
    if not a.cmd: raise SystemExit("실행할 명령이 없다: dinnno gpu run ... -- CMD")
    cwd = a.cwd or (os.getcwd() if is_local(h) else None)
    if not cwd: raise SystemExit(f"{a.host}는 원격이다 — --cwd에 그 머신의 경로를 준다")
    e = {"kind": "run", "hostkind": h["kind"], "project": a.project or local_project(), "mem": a.mem, "hours": a.hours,
         "gpu": a.gpu, "ram": a.ram, "cwd": cwd, "cmd": shlex.join(a.cmd) if len(a.cmd) > 1 else a.cmd[0],
         "prio": a.prio, "log": a.log}
    r = call(h, "submit", {"entry": e})
    for w in r["warn"]: print(f"주의: {w}")
    print(f"{a.host} 대기열에 올림: id {r['id']}, 앞에 {r['ahead']}개, 로그 {a.host}:{r['log']}")
    print(f"확인: dinnno gpu ls {a.host} / 기다리기: dinnno gpu wait --host {a.host} {r['id']}")


def cmd_hold(a):
    h = hosts()[a.host]
    if h["kind"] == "slurm": raise SystemExit(f"{a.host}는 Slurm이다 — 예약은 스케줄러가 한다")
    start = parse_when(a.start)
    e = {"kind": "hold", "project": a.project or local_project(), "mem": a.mem, "gpu": a.gpu,
         "from": start, "until": start + a.hours * 3600, "note": a.note or ""}
    r = call(h, "submit", {"entry": e})
    print(f"{a.host} 예약: id {r['id']}, {e['project']} {a.mem:g}G {fmt(e['from'])} ~ {fmt(e['until'])}")


def cmd_cancel(a):
    call(hosts()[a.host], "cancel", {"id": a.id})
    print(f"{a.host}: {a.id} 취소")


def cmd_wait(a):
    h, end = hosts()[a.host], time.time() + a.timeout
    while time.time() < end:
        st = call(h, "status", {})
        e = next((x for x in st["entries"] if x["id"] == a.id), None)
        if e and e["kind"] == "run" and e["state"] == "run" and a.until == "start":
            print(f"시작: {a.id} GPU{e['gpu']} {fmt(e['started'])}"); return
        if e is None:
            done = [x for x in st["hist"] if x["id"] == a.id]
            print(f"끝: {a.id} " + (done[-1]["outcome"] if done else "(장부·이력에 없음)")); return
        time.sleep(POLL)
    raise SystemExit(f"timeout: {a.id} 아직 {'대기' if e and e['state'] == 'wait' else '실행'} 중")


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "_host":
        print(json.dumps(HOST_OPS[sys.argv[2]](json.loads(sys.argv[3])), ensure_ascii=False))
        return
    ap = argparse.ArgumentParser(prog="dinnno gpu", description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="op", required=True)
    s = sub.add_parser("ls"); s.add_argument("hosts", nargs="*"); s.set_defaults(fn=cmd_ls)
    s = sub.add_parser("where"); s.add_argument("--mem", type=float, required=True); s.add_argument("--hours", type=float, required=True)
    s.add_argument("--project"); s.set_defaults(fn=cmd_where)
    s = sub.add_parser("run")
    for k, kw in [("--host", {"required": True}), ("--mem", {"type": float, "required": True}),
                  ("--hours", {"type": float, "required": True}), ("--gpu", {"type": int}), ("--ram", {"type": float}),
                  ("--cwd", {}), ("--prio", {"type": int, "default": 0}), ("--project", {}), ("--log", {})]:
        s.add_argument(k, **kw)
    s.add_argument("cmd", nargs=argparse.REMAINDER); s.set_defaults(fn=cmd_run)
    s = sub.add_parser("hold")
    for k, kw in [("--host", {"required": True}), ("--mem", {"type": float, "required": True}),
                  ("--from", {"dest": "start", "required": True}), ("--hours", {"type": float, "required": True}),
                  ("--gpu", {"type": int}), ("--note", {}), ("--project", {})]:
        s.add_argument(k, **kw)
    s.set_defaults(fn=cmd_hold)
    s = sub.add_parser("cancel"); s.add_argument("--host", required=True); s.add_argument("id"); s.set_defaults(fn=cmd_cancel)
    s = sub.add_parser("wait"); s.add_argument("--host", required=True); s.add_argument("id")
    s.add_argument("--until", choices=["start", "end"], default="end"); s.add_argument("--timeout", type=float, default=86400)
    s.set_defaults(fn=cmd_wait)
    a = ap.parse_args()
    if getattr(a, "cmd", None) and a.cmd[0] == "--": a.cmd = a.cmd[1:]
    try: a.fn(a)
    except RuntimeError as ex: raise SystemExit(str(ex))


if __name__ == "__main__":
    main()
