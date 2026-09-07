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
PY="$(find_python)" || {
  echo "no python with pyyaml found — install pyyaml (pip install pyyaml)" >&2
  exit 1
}

exec "$PY" "$ROOT/interface/brain_query.py" --root "$ROOT" "$@"
