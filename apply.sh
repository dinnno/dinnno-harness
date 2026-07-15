#!/usr/bin/env bash
# dinnno-harness-codex installer.
#   ./apply.sh --global          # link global AGENTS.md, skills, and custom agents
#   ./apply.sh /path/to/project  # copy project templates without overwriting

set -euo pipefail

HARNESS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

backup_if_exists() {
  local path="$1"
  if [[ -L "$path" ]]; then
    rm "$path"
  elif [[ -e "$path" ]]; then
    local bak="${path}.bak.$(date +%Y%m%d-%H%M%S)"
    mv "$path" "$bak"
    echo "backup: $path -> $bak"
  fi
}

link_path() {
  local source="$1"
  local target="$2"
  backup_if_exists "$target"
  ln -s "$source" "$target"
  echo "linked: $target -> $source"
}

install_global() {
  mkdir -p "$HOME/.codex/agents" "$HOME/.agents/skills"

  link_path "$HARNESS_DIR/AGENTS.md" "$HOME/.codex/AGENTS.md"

  local skill_dir name
  for skill_dir in "$HARNESS_DIR/skills/"*; do
    [[ -f "$skill_dir/SKILL.md" ]] || continue
    name="$(basename "$skill_dir")"
    link_path "$skill_dir" "$HOME/.agents/skills/$name"
  done

  local agent_file
  for agent_file in "$HARNESS_DIR/agents/"*.toml; do
    [[ -f "$agent_file" ]] || continue
    link_path "$agent_file" "$HOME/.codex/agents/$(basename "$agent_file")"
  done

  echo 'done. start a new Codex session and invoke $harness'
}

install_project() {
  local target="$1"
  if [[ ! -d "$target" ]]; then
    mkdir -p "$target"
    echo "created: $target"
  fi
  target="$(cd "$target" && pwd)"

  cp -rn "$HARNESS_DIR/templates/." "$target/"
  if [[ -e "$target/gitignore" && ! -e "$target/.gitignore" ]]; then
    mv "$target/gitignore" "$target/.gitignore"
  elif [[ -e "$target/gitignore" ]]; then
    rm "$target/gitignore"
  fi

  echo "installed into: $target"
  echo 'next: edit docs/RESEARCH_SPEC.md, start Codex, and invoke $harness'
}

case "${1:-}" in
  --global)
    install_global
    ;;
  -h|--help|"")
    echo "usage:"
    echo "  $0 --global              # install user guidance, skills, and agents"
    echo "  $0 /path/to/project      # install project templates"
    exit 1
    ;;
  *)
    install_project "$1"
    ;;
esac
