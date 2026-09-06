#!/usr/bin/env bash
# dinnno-harness installer — one source, three runtimes (Claude Code, Codex, Grok).
#   ./apply.sh --global [--with-ponytail]   # link rules, skills, CLI, and the SessionStart hook
#   ./apply.sh /path/to/project             # copy the docs scaffold into a project (existing files kept)
set -euo pipefail

HARNESS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WITH_PONYTAIL=0

backup_if_exists() { # regular file/dir → timestamped backup; symlink → removed
  local p="$1"
  if [[ -e "$p" && ! -L "$p" ]]; then mv "$p" "$p.bak.$(date +%Y%m%d-%H%M%S)"; echo "backup: $p"
  elif [[ -L "$p" ]]; then rm "$p"; fi
}

link() { backup_if_exists "$2"; mkdir -p "$(dirname "$2")"; ln -s "$1" "$2"; echo "linked: $2 -> $1"; }

prune_old_links() { # remove symlinks in $1 that point into any dinnno-harness checkout (old layout / old ports)
  local dir="$1"; [[ -d "$dir" ]] || return 0
  for p in "$dir"/*; do
    [[ -L "$p" ]] || continue
    case "$(readlink -f "$p" 2>/dev/null || readlink "$p")" in *dinnno-harness*) rm "$p"; echo "pruned: $p";; esac
  done
}

link_skills_into() {
  local target="$1"; mkdir -p "$target"; prune_old_links "$target"
  for d in "$HARNESS_DIR"/skills/*/; do
    [[ -f "$d/SKILL.md" ]] || continue
    local n; n="$(basename "$d")"
    [[ "$n" == ponytail && $WITH_PONYTAIL -eq 0 ]] && continue
    link "${d%/}" "$target/$n"
  done
}

merge_hooks_json() { # merge hooks/hooks.json into a Claude/Codex-style settings file (idempotent)
  local file="$1"
  python3 - "$file" "$HARNESS_DIR/hooks/hooks.json" "$HARNESS_DIR" <<'PY'
import json, sys, os
path, src, hd = sys.argv[1:4]
new = json.load(open(src))["hooks"]
for ev in new:
    for g in new[ev]:
        for h in g["hooks"]:
            h["command"] = h["command"].replace("__HARNESS_DIR__", hd)
cfg = json.load(open(path)) if os.path.exists(path) else {}
hooks = cfg.setdefault("hooks", {})
for ev, groups in new.items():
    existing = hooks.setdefault(ev, [])
    have = {h.get("command") for g in existing for h in g.get("hooks", [])}
    for g in groups:
        if all(h["command"] in have for h in g["hooks"]):
            continue
        existing.append(g)
json.dump(cfg, open(path, "w"), indent=2, ensure_ascii=False); open(path, "a").write("\n")
print(f"hooks merged: {path}")
PY
}

merge_hooks_toml() { # Grok: append a [[hooks.SessionStart]] block to config.toml once
  local file="$1"; mkdir -p "$(dirname "$file")"; touch "$file"
  grep -q 'dinnno check' "$file" && { echo "hooks present: $file"; return; }
  cat >> "$file" <<EOF

# dinnno-harness SessionStart hook (added by apply.sh)
[[hooks.SessionStart]]
  [[hooks.SessionStart.hooks]]
  type = "command"
  command = "$HARNESS_DIR/scripts/dinnno check --hook"
  timeout = 15
EOF
  echo "hooks appended: $file"
}

install_global() {
  # rules: one file, three readers
  link "$HARNESS_DIR/AGENTS.md" "$HOME/.claude/CLAUDE.md"
  link "$HARNESS_DIR/AGENTS.md" "$HOME/.codex/AGENTS.md"
  link "$HARNESS_DIR/AGENTS.md" "$HOME/.grok/AGENTS.md"
  # skills: same set everywhere
  link_skills_into "$HOME/.claude/skills"
  link_skills_into "$HOME/.agents/skills"
  link_skills_into "$HOME/.grok/skills"
  # old layout leftovers (commands/, agents/) — remove only links that point at a harness checkout
  prune_old_links "$HOME/.claude/commands"; prune_old_links "$HOME/.claude/agents"
  prune_old_links "$HOME/.grok/agents"; prune_old_links "$HOME/.codex/agents"
  # CLI + hooks
  chmod +x "$HARNESS_DIR/scripts/dinnno"
  link "$HARNESS_DIR/scripts/dinnno" "$HOME/.local/bin/dinnno"
  mkdir -p "$HOME/.claude" "$HOME/.codex"
  merge_hooks_json "$HOME/.claude/settings.json"
  merge_hooks_json "$HOME/.codex/hooks.json"
  merge_hooks_toml "$HOME/.grok/config.toml"
  echo
  echo "done. open a new Claude Code / Codex / Grok session."
  echo "  - Codex needs [features] hooks = true in ~/.codex/config.toml"
  echo "  - ~/.local/bin should be on PATH for 'dinnno' (hooks use the absolute path anyway)"
  echo "  - ponytail is opt-in: ./apply.sh --global --with-ponytail"
}

install_project() {
  local target="$1"; mkdir -p "$target"; target="$(cd "$target" && pwd)"
  cp -r --update=none "$HARNESS_DIR/templates/." "$target/" 2>/dev/null || cp -rn "$HARNESS_DIR/templates/." "$target/"
  [[ -e "$target/gitignore" && ! -e "$target/.gitignore" ]] && mv "$target/gitignore" "$target/.gitignore"
  rm -f "$target/gitignore"
  # stamp last-sync with the newest CHANGELOG entry so a fresh project starts in sync
  local last; last="$(grep -E '^- [0-9]{4}-[0-9]{2}-[0-9]{2} — ' "$HARNESS_DIR/CHANGELOG.md" | tail -1 | cut -c3-70)"
  grep -q '{설치일}' "$target/AGENTS.md" 2>/dev/null && sed -i "s|{설치일}|$last|" "$target/AGENTS.md"
  echo "installed into: $target"
  echo "next: fill docs/RESEARCH_SPEC.md and AGENTS.md, then start a session with the harness skill"
}

case "${1:-}" in
  --global) [[ "${2:-}" == "--with-ponytail" ]] && WITH_PONYTAIL=1; install_global;;
  -h|--help|"") sed -n '2,4p' "$0"; exit 1;;
  *) install_project "$1";;
esac
