#!/usr/bin/env bash
# dinnno-harness installer.
#   ./apply.sh --global             # link CLAUDE.md & commands/harness.md into ~/.claude/
#   ./apply.sh /path/to/project     # copy templates into a project (skip existing)

set -euo pipefail

HARNESS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

backup_if_exists() {
  local path="$1"
  if [[ -e "$path" && ! -L "$path" ]]; then
    local bak="${path}.bak.$(date +%Y%m%d-%H%M%S)"
    mv "$path" "$bak"
    echo "backup: $path -> $bak"
  elif [[ -L "$path" ]]; then
    rm "$path"
  fi
}

install_global() {
  local target_md="$HOME/.claude/CLAUDE.md"
  local target_cmd_dir="$HOME/.claude/commands"

  mkdir -p "$HOME/.claude" "$target_cmd_dir"

  backup_if_exists "$target_md"
  ln -s "$HARNESS_DIR/CLAUDE.md" "$target_md"
  echo "linked: $target_md -> $HARNESS_DIR/CLAUDE.md"

  for cmd in "$HARNESS_DIR/commands/"*.md; do
    [[ -e "$cmd" ]] || continue
    local name
    name="$(basename "$cmd")"
    local target="$target_cmd_dir/$name"
    backup_if_exists "$target"
    ln -s "$cmd" "$target"
    echo "linked: $target -> $cmd"
  done

  local target_agents_dir="$HOME/.claude/agents"
  mkdir -p "$target_agents_dir"
  for agentf in "$HARNESS_DIR/agents/"*.md; do
    [[ -e "$agentf" ]] || continue
    local aname
    aname="$(basename "$agentf")"
    local atarget="$target_agents_dir/$aname"
    backup_if_exists "$atarget"
    ln -s "$agentf" "$atarget"
    echo "linked: $atarget -> $agentf"
  done

  echo "done. open a new Claude Code session and try /harness"
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
  echo "next: edit docs/RESEARCH_SPEC.md (fill thesis), then open a new Claude session and run /harness"
}

case "${1:-}" in
  --global)
    install_global
    ;;
  -h|--help|"")
    echo "usage:"
    echo "  $0 --global              # install ~/.claude/CLAUDE.md and /harness command"
    echo "  $0 /path/to/project      # install templates into a project"
    exit 1
    ;;
  *)
    install_project "$1"
    ;;
esac
