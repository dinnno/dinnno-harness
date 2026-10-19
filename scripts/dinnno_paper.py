#!/usr/bin/env python3
"""dinnno paper — deterministic parts of the `paper` skill. Called as `dinnno paper <cmd>`.

  export                 zip writing/ for Overleaf, snapshot it as the sync base, list files changed since the last sync
  import ZIP             3-way merge an Overleaf source zip (base / Overleaf / local); conflicts are left untouched (exit 3)
  numbers                writing/numbers.yaml -> writing/numbers.tex, every value re-read from its source file
  check [--bib]          bare numbers, missing cites, stale numbers.tex, TODO/GAP, unsynced files, D-day; --bib also
                         looks every cited bib title up on Semantic Scholar / arXiv (cached in writing/.sync/bibcheck.json)

The numbers key grammar is the one hoi-sam's runs/paper_main/*/check_numbers.py introduced.
"""
from __future__ import annotations

import csv
import datetime as dt
import difflib
import hashlib
import json
import re
import shutil
import sys
import time
import urllib.parse
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

import yaml

# Files that live in writing/ but are not part of the LaTeX project sent to Overleaf.
LOCAL_DIRS = {".sync", "_export", "notes", "reviews", "reference"}
LOCAL_FILES = {"README.md", "VENUE.md", "STYLE.md", "numbers.yaml", ".gitignore"}


def find_root() -> Path:
    d = Path.cwd().resolve()
    for p in [d, *d.parents]:
        if (p / "docs/RESEARCH_SPEC.md").is_file():
            return p
    sys.exit("dinnno paper: docs/RESEARCH_SPEC.md가 있는 프로젝트 안에서 실행한다")


ROOT = W = SYNC = BASE = Path()  # set in main once the command is known


def set_root():
    global ROOT, W, SYNC, BASE
    ROOT = find_root()
    W = ROOT / "writing"
    SYNC = W / ".sync"
    BASE = SYNC / "base"


def need_writing():
    if not W.is_dir():
        sys.exit("writing/이 없다. paper 스킬의 init을 먼저 한다")


def project_files(top: Path) -> dict[str, bytes]:
    out = {}
    for p in sorted(top.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(top)
        if rel.parts[0] in LOCAL_DIRS or (len(rel.parts) == 1 and rel.name in LOCAL_FILES):
            continue
        if rel.name.startswith(".") or rel.suffix == ".zip":
            continue
        out[rel.as_posix()] = p.read_bytes()
    return out


def base_files() -> dict[str, bytes]:
    if not BASE.is_dir():
        return {}
    return {p.relative_to(BASE).as_posix(): p.read_bytes() for p in sorted(BASE.rglob("*")) if p.is_file()}


def write_file(top: Path, rel: str, data: bytes | None):
    p = top / rel
    if data is None:
        if p.exists():
            p.unlink()
        return
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)


def changed_since_base() -> list[tuple[str, str]]:
    local, base = project_files(W), base_files()
    rows = []
    for rel in sorted(set(local) | set(base)):
        if rel not in base:
            rows.append(("new", rel))
        elif rel not in local:
            rows.append(("deleted", rel))
        elif local[rel] != base[rel]:
            rows.append(("modified", rel))
    return rows


def text_diff(a: bytes | None, b: bytes | None, rel: str, la: str, lb: str) -> list[str]:
    try:
        ta = (a or b"").decode().splitlines(keepends=True)
        tb = (b or b"").decode().splitlines(keepends=True)
    except UnicodeDecodeError:
        return [f"(binary) {rel}\n"]
    return list(difflib.unified_diff(ta, tb, f"{la}/{rel}", f"{lb}/{rel}", n=1))


# ---------------------------------------------------------------- export
def cmd_export(_args):
    need_writing()
    rows = changed_since_base()
    first = not BASE.is_dir()
    files = project_files(W)
    out = W / "_export" / f"{ROOT.name}_overleaf.zip"
    out.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for rel, data in files.items():
            z.writestr(rel, data)
    if BASE.exists():
        shutil.rmtree(BASE)
    for rel, data in files.items():
        write_file(BASE, rel, data)
    print(f"zip: {out.relative_to(ROOT)} ({len(files)} files)")
    if first:
        print("첫 업로드: Overleaf → New Project → Upload Project → 이 zip. Compiler pdfLaTeX, main document main.tex")
    elif not rows:
        print("지난 동기화 이후 바뀐 파일 없음")
    else:
        print("Overleaf에 반영할 파일 (같은 경로로 업로드해 덮어쓰기, deleted는 Overleaf에서 삭제):")
        for kind, rel in rows:
            print(f"  {kind:8s} writing/{rel}")


# ---------------------------------------------------------------- import
def read_zip(zpath: Path) -> dict[str, bytes]:
    out = {}
    with zipfile.ZipFile(zpath) as z:
        for info in z.infolist():
            if info.is_dir():
                continue
            rel = Path(info.filename)
            if rel.is_absolute() or ".." in rel.parts:
                sys.exit(f"zip에 안전하지 않은 경로가 있다: {info.filename}")
            out[rel.as_posix()] = z.read(info)
    # Overleaf zips are flat; a zip re-made by hand may wrap everything in one top folder.
    tops = {k.split("/", 1)[0] for k in out}
    if "main.tex" not in out and len(tops) == 1 and f"{next(iter(tops))}/main.tex" in out:
        out = {k.split("/", 1)[1]: v for k, v in out.items()}
    return {k: v for k, v in out.items() if k.split("/", 1)[0] not in LOCAL_DIRS and k not in LOCAL_FILES}


def cmd_import(args):
    need_writing()
    if not args:
        sys.exit("usage: dinnno paper import <overleaf-source.zip>")
    zpath = Path(args[0]).expanduser().resolve()
    ov = read_zip(zpath)
    local, base = project_files(W), base_files()
    # 다른 프로젝트의 zip이면 base 파일 대부분이 "Overleaf에서 삭제됨"으로 보여 로컬이 지워진다
    if base and len(set(ov) & set(base)) < len(base) / 2 and "--force" not in args:
        sys.exit(f"import 중단: {zpath.name}에 지난 export 파일이 {len(set(ov) & set(base))}/{len(base)}개뿐이다. "
                 "이 원고를 export한 Overleaf 프로젝트의 zip이 맞는지 확인한다(맞으면 --force).")
    taken, kept, conflicts, same = [], [], [], 0
    diff_lines: list[str] = []
    conf_dir = SYNC / "conflicts"
    if conf_dir.exists():
        shutil.rmtree(conf_dir)
    for rel in sorted(set(ov) | set(local) | set(base)):
        o, l, b = ov.get(rel), local.get(rel), base.get(rel)
        if o == l:
            same += 1
            write_file(BASE, rel, o)
        elif l == b:
            write_file(W, rel, o)
            write_file(BASE, rel, o)
            taken.append(rel)
            diff_lines += text_diff(b, o, rel, "before", "overleaf")
        elif o == b:
            kept.append(rel)
        else:
            conflicts.append(rel)
            if o is not None:
                write_file(conf_dir, rel, o)
            diff_lines += text_diff(l, o, rel, "local", "overleaf")
    (SYNC).mkdir(exist_ok=True)
    (SYNC / "last_import.diff").write_text("".join(diff_lines))
    print(f"import: {zpath.name} — 같음 {same}, Overleaf 반영 {len(taken)}, 로컬만 수정(유지) {len(kept)}, 충돌 {len(conflicts)}")
    for rel in taken:
        print(f"  overleaf → writing/{rel}" + (" (Overleaf에서 삭제됨, 로컬도 삭제)" if rel not in ov else ""))
    for rel in kept:
        print(f"  local    writing/{rel} (다음 export 때 올린다)")
    for rel in conflicts:
        print(f"  CONFLICT writing/{rel} — Overleaf 판은 writing/.sync/conflicts/{rel}, 로컬은 그대로 둠")
    if diff_lines:
        print(f"\n사용자 수정 diff: writing/.sync/last_import.diff ({len(diff_lines)}줄). 앞부분:")
        sys.stdout.write("".join(diff_lines[:80]))
    if conflicts:
        print("\n충돌 파일은 덮어쓰지 않았다. 파일마다 어느 쪽을 살릴지 정한 뒤 로컬을 고치고 export한다.")
        sys.exit(3)


# ---------------------------------------------------------------- numbers
def md_tables(path: Path):
    tables, cur = [], None
    for line in path.read_text().splitlines():
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if cur is None:
                cur = {"header": cells, "rows": []}
            elif not all(re.fullmatch(r":?-+:?", c) for c in cells):
                cur["rows"].append(cells)
        elif cur is not None:
            tables.append(cur)
            cur = None
    if cur is not None:
        tables.append(cur)
    return tables


def resolve(source: str, key: str) -> str:
    path = ROOT / source
    kind, *parts = key.split("|")
    if kind == "csv":
        filt = dict(kv.split("=", 1) for kv in parts[0].split(";"))
        with open(path) as f:
            hits = [r for r in csv.DictReader(f) if all(r.get(k) == v for k, v in filt.items())]
        if len(hits) != 1:
            raise KeyError(f"csv 행 {len(hits)}개가 {filt}에 맞음 (정확히 1개여야 함)")
        return hits[0][parts[1]]
    if kind == "md":
        label, col, sel = parts
        for t in md_tables(path):
            if col not in t["header"]:
                continue
            j = t["header"].index(col)
            for r in t["rows"]:
                if r[0] == label:
                    cell = r[j]
                    if sel == "raw":
                        return cell
                    if sel == "v":
                        return cell.split(" [")[0].split(" (")[0]
                    if sel == "ci":
                        return "[" + cell.split(" [", 1)[1]
                    raise KeyError(f"md sel {sel!r}")
        raise KeyError(f"md 행 {label!r} 열 {col!r} 없음")
    if kind == "json":
        data = json.loads(path.read_text())
        vals = []
        for p in parts[0].split(","):
            x = data
            for k in p.split("."):
                x = x[int(k)] if isinstance(x, list) else x[k]
            vals.append(x)
        return parts[1].format(*vals)
    if kind == "line":
        n, sub = int(parts[0]), parts[1]
        line = path.read_text().splitlines()[n - 1]
        if sub not in line:
            raise KeyError(f"{sub!r}가 {n}번째 줄에 없음")
        return sub
    raise KeyError(f"모르는 key 종류 {kind!r}")


def tex_escape(v: str) -> str:
    return v.replace("\\", r"\textbackslash{}").replace("%", r"\%").replace("&", r"\&").replace("#", r"\#").replace("_", r"\_")


def build_numbers() -> tuple[str, list[str]]:
    spec = yaml.safe_load((W / "numbers.yaml").read_text()) or {}
    entries = spec.get("numbers") or []
    errs, lines, seen = [], [], set()
    lines.append("% generated by `dinnno paper numbers` from writing/numbers.yaml — 손으로 고치지 않는다\n")
    for e in entries:
        m = e.get("macro", "")
        if not re.fullmatch(r"[A-Za-z]+", m):
            errs.append(f"macro {m!r}: 영문자만 쓴다")
            continue
        if m in seen:
            errs.append(f"macro {m}: 중복")
            continue
        seen.add(m)
        try:
            v = resolve(e["source"], e["key"])
            if e.get("fmt"):
                v = e["fmt"].format(float(v))
        except Exception as ex:  # report every broken entry, not just the first
            errs.append(f"{m}: {type(ex).__name__}: {ex} ({e.get('source')})")
            continue
        lines.append(f"\\newcommand{{\\{m}}}{{{tex_escape(str(v))}}}  % {e.get('fact', '-')} | {e['source']}\n")
    return "".join(lines), errs


def cmd_numbers(_args):
    need_writing()
    text, errs = build_numbers()
    for x in errs:
        print(f"ERROR {x}")
    if errs:
        sys.exit("numbers.tex를 쓰지 않았다. 위 항목의 원천을 고친다")
    (W / "numbers.tex").write_text(text)
    print(f"writing/numbers.tex: {text.count(chr(10)) - 1} macros")


# ---------------------------------------------------------------- check
STRIP_ARG_CMDS = r"includegraphics|vspace\*?|hspace\*?|label|ref|eqref|autoref|cref|Cref|cite\w*|resizebox|scalebox|setlength|addtolength|input|include|url|href|definecolor|color|textcolor|cellcolor|rowcolor|arraystretch|renewcommand|newcommand|begin|end|multicolumn|multirow|cmidrule"


def bare_numbers(path: Path) -> list[tuple[int, str]]:
    out = []
    for i, raw in enumerate(path.read_text().splitlines(), 1):
        if "num-ok" in raw:
            continue
        line = re.sub(r"(?<!\\)%.*", "", raw)
        line = re.sub(r"\\(?:" + STRIP_ARG_CMDS + r")(\[[^\]]*\])?(\{[^{}]*\})*", " ", line)
        line = re.sub(r"[\d.]+\\(?:linewidth|textwidth|columnwidth|hsize|baselineskip)", " ", line)
        line = re.sub(r"-?\d+(?:\.\d+)?\s*(?:pt|em|ex)\b", " ", line)  # LaTeX lengths only; cm/mm can be results
        for m in re.finditer(r"(?<![\w\\.])\d+\.\d+(?![\w.])|(?<![\w\\.])\d+(?:\.\d+)?\s*\\%", line):
            out.append((i, m.group(0)))
    return out


def tex_files() -> list[Path]:
    return [p for p in sorted(W.rglob("*.tex")) if p.relative_to(W).parts[0] not in LOCAL_DIRS and p.name != "numbers.tex"]


def parse_bib(text: str) -> dict[str, dict]:
    out = {}
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", text):
        typ, key = m.group(1).lower(), m.group(2)
        if typ in {"comment", "string", "preamble"}:
            continue
        i, depth = m.end(), 1
        while i < len(text) and depth:
            depth += {"{": 1, "}": -1}.get(text[i], 0)
            i += 1
        body = text[m.end():i - 1]
        t = re.search(r"\btitle\s*=\s*(\{(?:[^{}]|\{[^{}]*\})*\}|\"[^\"]*\")", body, re.I)
        title = re.sub(r"[{}\"]", "", t.group(1)).strip() if t else ""
        out[key] = {"type": typ, "title": re.sub(r"\s+", " ", title)}
    return out


def norm_title(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def ssl_context():
    # conda pythons ship their own CA file; the system bundle also carries site/proxy CAs
    import os, ssl
    sys_bundle = "/etc/ssl/certs/ca-certificates.crt"
    if not os.environ.get("SSL_CERT_FILE") and Path(sys_bundle).is_file():
        return ssl.create_default_context(cafile=sys_bundle)
    return ssl.create_default_context()


def fetch(url: str) -> bytes:
    """GET with retry on 429/5xx. 404 returns b'' (Semantic Scholar's 'no match')."""
    for wait in (0, 3, 8, 20):
        time.sleep(wait)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "dinnno-paper"})
            with urllib.request.urlopen(req, timeout=20, context=ssl_context()) as r:
                body = r.read()
                if r.status == 200 and body:
                    return body
                err = f"HTTP {r.status} empty"
        except urllib.error.HTTPError as ex:
            if ex.code == 404:
                return b""
            err = f"HTTP {ex.code}"
            if ex.code not in (429, 500, 502, 503, 504):
                break
        except Exception as ex:
            err = str(ex)
    raise RuntimeError(err)


def cands_s2(title: str):
    body = fetch("https://api.semanticscholar.org/graph/v1/paper/search/match?fields=title,year,venue&query="
                 + urllib.parse.quote(title))
    return [(x.get("title", ""), x.get("year"), x.get("venue")) for x in (json.loads(body).get("data", []) if body else [])]


def cands_arxiv(title: str):
    import xml.etree.ElementTree as ET
    q = urllib.parse.quote(f'ti:"{re.sub(r"[^A-Za-z0-9 ]+", " ", title)}"')
    root = ET.fromstring(fetch(f"https://export.arxiv.org/api/query?max_results=5&search_query={q}"))
    ns = {"a": "http://www.w3.org/2005/Atom"}
    return [(re.sub(r"\s+", " ", e.findtext("a:title", "", ns)), e.findtext("a:published", "", ns)[:4], "arXiv")
            for e in root.findall("a:entry", ns)]


def lookup_title(title: str) -> dict:
    """FOUND = a source returned a title with similarity >= 0.9. NOT FOUND = at least one source answered and none
    matched. UNCHECKED = every source failed (network / rate limit) — never cached as a verdict."""
    best = {"score": 0.0}
    errors, answered = [], 0
    # DBLP answers 202 with an empty body from this network, so it is not a source.
    for name, fn in (("semanticscholar", cands_s2), ("arxiv", cands_arxiv)):
        try:
            cands = fn(title)
            answered += 1
        except Exception as ex:
            errors.append(f"{name}: {ex}")
            continue
        for ct, year, venue in cands:
            sc = difflib.SequenceMatcher(None, norm_title(title), norm_title(ct)).ratio()
            if sc > best["score"]:
                best = {"score": round(sc, 3), "source": name, "matched": ct, "year": year, "venue": venue}
        if best["score"] >= 0.9:
            break
        time.sleep(1.1)  # unauthenticated rate limits
    best["status"] = "FOUND" if best["score"] >= 0.9 else ("NOT FOUND" if answered else "UNCHECKED")
    if errors:
        best["errors"] = errors
    return best


def check_bib(bib: dict[str, dict], used: set[str]) -> int:
    cache_p = SYNC / "bibcheck.json"
    cache = json.loads(cache_p.read_text()) if cache_p.exists() else {}
    bad = 0
    for key in sorted(used & set(bib)):
        title = bib[key]["title"]
        if not title:
            print(f"  WARN bib {key}: title 없음")
            bad += 1
            continue
        h = hashlib.sha1(title.encode()).hexdigest()[:12]
        hit = cache.get(key)
        if not hit or hit.get("title_hash") != h or hit.get("status") != "FOUND":
            hit = lookup_title(title) | {"title_hash": h, "checked": dt.date.today().isoformat()}
            cache[key] = hit
        if hit["status"] == "UNCHECKED":
            del cache[key]
            print(f"  WARN bib {key}: 확인 못 함(네트워크) {hit.get('errors')}")
            bad += 1
            continue
        if hit["status"] != "FOUND":
            bad += 1
            near = f" — 가장 가까운 것: {hit.get('matched')!r} ({hit.get('score')})" if hit.get("matched") else ""
            print(f"  WARN bib {key}: 실재 확인 실패 {title!r}{near}{' ' + str(hit.get('errors')) if hit.get('errors') else ''}")
    SYNC.mkdir(exist_ok=True)
    cache_p.write_text(json.dumps(cache, indent=1, ensure_ascii=False) + "\n")
    print(f"bib 실재 확인: 인용된 {len(used & set(bib))}개 중 확인 실패 {bad}개 (캐시 writing/.sync/bibcheck.json)")
    return bad


def cmd_check(args):
    need_writing()
    errors = warns = 0
    texs = tex_files()
    # 1. bare numbers
    bare = [(p, i, s) for p in texs if p.parent.name == "sec" for i, s in bare_numbers(p)]
    for p, i, s in bare:
        print(f"WARN 매크로 밖 수치 {p.relative_to(ROOT)}:{i}: {s}  (원천 있는 수치는 numbers.yaml로, 의도한 상수면 줄 끝에 % num-ok)")
    warns += len(bare)
    # 2. cites
    alltex = {p: p.read_text() for p in texs}
    used = {k.strip() for t in alltex.values() for g in re.findall(r"\\cite\w*\*?(?:\[[^\]]*\])*\{([^}]*)\}", t) for k in g.split(",") if k.strip()}
    bib = {}
    for b in W.rglob("*.bib"):
        if b.relative_to(W).parts[0] not in LOCAL_DIRS:
            bib |= parse_bib(b.read_text())
    missing = sorted(used - set(bib))
    for k in missing:
        print(f"ERROR bib에 없는 cite 키: {k}")
    errors += len(missing)
    # 3. numbers.tex freshness
    if (W / "numbers.yaml").exists():
        text, errs = build_numbers()
        cur = (W / "numbers.tex").read_text() if (W / "numbers.tex").exists() else ""
        for x in errs:
            print(f"ERROR numbers: {x}")
        errors += len(errs)
        if not errs and text != cur:
            print("ERROR numbers.tex가 원천과 다르다(STALE). dinnno paper numbers를 다시 돌린다")
            errors += 1
    # 4. TODO / GAP
    marks = [(p, i, m) for p, t in alltex.items() if p.parent.name == "sec" for i, l in enumerate(t.splitlines(), 1)
             for m in re.findall(r"\\(TODO|GAP)\{", re.sub(r"(?<!\\)%.*", "", l))]
    n_todo, n_gap = sum(m == "TODO" for *_, m in marks), sum(m == "GAP" for *_, m in marks)
    for p, i, m in marks:
        print(f"  {m:4s} {p.relative_to(ROOT)}:{i}")
    # 5. sync state
    rows = changed_since_base()
    if not BASE.is_dir():
        print("Overleaf: 아직 export한 적 없음")
    elif rows:
        print("Overleaf 미반영 (마지막 동기화 이후 로컬 변경): " + ", ".join(f"{k} {r}" for k, r in rows))
    # 6. D-day
    venue = (W / "VENUE.md").read_text() if (W / "VENUE.md").exists() else ""
    m = re.search(r"deadline:\*\*\s*(\d{4}-\d{2}-\d{2})", venue)
    dday = f"D-{(dt.date.fromisoformat(m.group(1)) - dt.date.today()).days}" if m else "deadline 미기재"
    # 7. optional bib existence
    if "--bib" in args:
        warns += check_bib(bib, used)
    print(f"\n[paper] {ROOT.name}: {dday} · ERROR {errors} · WARN {warns} · TODO {n_todo} · GAP {n_gap} · cite {len(used)}/{len(bib)} bib · 미반영 {len(rows)}")
    sys.exit(1 if errors else 0)


CMDS = {"export": cmd_export, "import": cmd_import, "numbers": cmd_numbers, "check": cmd_check}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in CMDS:
        print(__doc__.split("\n\n")[1])
        sys.exit(2)
    set_root()
    CMDS[sys.argv[1]](sys.argv[2:])
