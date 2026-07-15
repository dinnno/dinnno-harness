#!/usr/bin/env bash

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

bash -n "$ROOT/apply.sh"

required=(
  "$ROOT/AGENTS.md"
  "$ROOT/templates/AGENTS.md"
  "$ROOT/templates/docs/RESEARCH_SPEC.md"
  "$ROOT/templates/docs/ARCHITECTURE.md"
  "$ROOT/templates/docs/LEARNINGS.md"
  "$ROOT/templates/docs/LOOP.md"
  "$ROOT/templates/docs/progress.md"
  "$ROOT/templates/docs/plans/_plan_template.md"
  "$ROOT/templates/docs/done/_done_template.md"
  "$ROOT/templates/docs/references/_INDEX.md"
  "$ROOT/agents/implementer.toml"
  "$ROOT/agents/research-reviewer.toml"
)

for path in "${required[@]}"; do
  [[ -f "$path" ]] || { echo "missing: $path" >&2; exit 1; }
done

for skill in harness audit add-ref blueprint-ref tidy; do
  file="$ROOT/skills/$skill/SKILL.md"
  metadata="$ROOT/skills/$skill/agents/openai.yaml"
  [[ -f "$file" ]] || { echo "missing: $file" >&2; exit 1; }
  [[ -f "$metadata" ]] || { echo "missing: $metadata" >&2; exit 1; }
  grep -qx "name: $skill" "$file" || { echo "bad skill name: $file" >&2; exit 1; }
  grep -q '^description: .' "$file" || { echo "missing description: $file" >&2; exit 1; }
  if grep -q 'TODO' "$file"; then
    echo "unfinished skill: $file" >&2
    exit 1
  fi
done

python3 - "$ROOT" <<'PY'
import pathlib
import sys
import tomllib

root = pathlib.Path(sys.argv[1])
for path in sorted((root / "agents").glob("*.toml")):
    data = tomllib.loads(path.read_text())
    missing = {"name", "description", "developer_instructions"} - data.keys()
    if missing:
        raise SystemExit(f"{path}: missing {sorted(missing)}")
PY

if rg -n 'CLAUDE\.md|codex:rescue|Fable|Opus|run_in_background|PushNotification' \
  "$ROOT/AGENTS.md" "$ROOT/apply.sh" "$ROOT/skills" "$ROOT/agents" "$ROOT/templates"; then
  echo "Claude-specific active reference found" >&2
  exit 1
fi

echo "verified: 5 skills, 2 custom agents, installer syntax, and active references"
