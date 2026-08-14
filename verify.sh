#!/usr/bin/env bash

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

bash -n "$ROOT/apply.sh"

required=(
  "$ROOT/AGENTS.md"
  "$ROOT/apply.ps1"
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
  "$ROOT/CHANGELOG.md"
)

for path in "${required[@]}"; do
  [[ -f "$path" ]] || { echo "missing: $path" >&2; exit 1; }
done

skills=(harness audit add-ref blueprint-ref tidy issue close workflow-ops)

for skill in "${skills[@]}"; do
  file="$ROOT/skills/$skill/SKILL.md"
  metadata="$ROOT/skills/$skill/agents/openai.yaml"
  [[ -f "$file" ]] || { echo "missing: $file" >&2; exit 1; }
  [[ -f "$metadata" ]] || { echo "missing: $metadata" >&2; exit 1; }
  grep -Eq "^name: ${skill}[[:space:]]*$" "$file" || { echo "bad skill name: $file" >&2; exit 1; }
  grep -q '^description: .' "$file" || { echo "missing description: $file" >&2; exit 1; }
  grep -q '^  display_name: ".' "$metadata" || { echo "missing display_name: $metadata" >&2; exit 1; }
  grep -q '^  short_description: ".' "$metadata" || { echo "missing short_description: $metadata" >&2; exit 1; }
  grep -Fq "\$$skill" "$metadata" || { echo "default prompt must mention \$$skill: $metadata" >&2; exit 1; }
  if grep -Eq '\{TODO\}|TODO:[[:space:]]*(fill|write|implement)' "$file"; then
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

if command -v rg >/dev/null 2>&1 && rg --version >/dev/null 2>&1; then
  scanner=(rg -n)
else
  scanner=(grep -RInE)
fi

if "${scanner[@]}" 'CLAUDE\.md|codex:rescue|Fable|Opus|run_in_background|PushNotification' \
  "$ROOT/AGENTS.md" "$ROOT/apply.sh" "$ROOT/skills" "$ROOT/agents" "$ROOT/templates"; then
  echo "Claude-specific active reference found" >&2
  exit 1
fi

echo "verified: ${#skills[@]} skills, 2 custom agents, installer syntax, and active references"
