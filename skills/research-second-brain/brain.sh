#!/usr/bin/env bash
# Read-only launcher for the research second brain (oh-dinnno-opsidian).
# Resolves vault root and a pyyaml-capable interpreter, then forwards all args
# to interface/brain_query.py.
set -euo pipefail

find_root() {
  if [[ -n "${SECOND_BRAIN_ROOT:-}" && -f "$SECOND_BRAIN_ROOT/interface/brain_query.py" ]]; then
    printf '%s' "$SECOND_BRAIN_ROOT"; return 0
  fi
  # walk up from CWD: works from any project inside the wrapper
  local dir="$PWD"
  while [[ "$dir" != "/" ]]; do
    if [[ -f "$dir/tools/oh-dinnno-opsidian/interface/brain_query.py" ]]; then
      printf '%s' "$dir/tools/oh-dinnno-opsidian"; return 0
    fi
    if [[ -f "$dir/interface/brain_query.py" ]]; then
      printf '%s' "$dir"; return 0
    fi
    dir="$(dirname "$dir")"
  done
  local candidate
  for candidate in "$HOME/Workspace/dinnno-research-wrapper/tools/oh-dinnno-opsidian" \
                   "$HOME/dinnno-research-wrapper/tools/oh-dinnno-opsidian" \
                   /root/oh-dinnno-opsidian; do
    [[ -f "$candidate/interface/brain_query.py" ]] && { printf '%s' "$candidate"; return 0; }
  done
  return 1
}

find_python() {
  local py
  for py in python3 /usr/bin/python3 python; do
    command -v "$py" >/dev/null 2>&1 || continue
    "$py" -c 'import yaml' >/dev/null 2>&1 && { printf '%s' "$py"; return 0; }
  done
  return 1
}

ROOT="$(find_root)" || {
  echo "second brain vault not found — set SECOND_BRAIN_ROOT to the oh-dinnno-opsidian clone" >&2
  exit 1
}
# Phone captures and radar runs land on the remote, so fast-forward the local clone at most hourly.
# Never merges or touches local edits: if ff-only fails, say how far behind and query what is here.
gd="$(git -C "$ROOT" rev-parse --absolute-git-dir 2>/dev/null || true)"   # vault may be a submodule
stamp="$gd/dinnno-brain-pull"   # last attempt, success or not, so offline runs do not retry every query
if [[ -n "$gd" ]] && { [[ ! -f "$stamp" ]] || (( $(date +%s) - $(stat -c %Y "$stamp") > 3600 )); }; then
  touch "$stamp"
  if ! GIT_TERMINAL_PROMPT=0 timeout 20 git -C "$ROOT" pull --ff-only -q >/dev/null 2>&1; then
    behind="$(git -C "$ROOT" rev-list --count 'HEAD..@{u}' 2>/dev/null || echo '?')"
    echo "second brain: pull 실패 — 원격보다 ${behind}커밋 뒤처진 로컬 사본으로 조회한다" >&2
  fi
fi

PY="$(find_python)" || {
  echo "no python with pyyaml found — install pyyaml (pip install pyyaml)" >&2
  exit 1
}

exec "$PY" "$ROOT/interface/brain_query.py" --root "$ROOT" "$@"
