---
name: harness
description: "Run the dinnno robotics research harness in Grok as the primary experiment and coding agent: orient from project state, confirm one bounded unit, execute an approved plan, and close experiment work with a durable Verdict while reserving init/spec/thesis/kill decisions for Fable or Mythos. Use for research work in repositories containing the dinnno docs scaffold; do not use for ordinary coding repositories, project-wide audits, or artifact cleanup."
---

# Grok research harness adapter

Use Grok as the top-level guide and coding agent. This file is an adapter over the canonical Claude harness, not a second copy of its research contract.

## Load the canonical contract

Resolve this `SKILL.md` through symlinks to its real path. From the containing `grok/skills/harness/` directory, read `../../../commands/harness.md` completely before acting. Follow its HARD/SOFT boundaries, artifact contract, Setup → Execute → Verdict lifecycle, synchronization rules, and session-close requirements.

This adapter overrides only the Claude-specific runtime mappings below. If an unmapped instruction conflicts with the canonical contract, the canonical contract wins.

## Grok runtime mappings

- Do not load `/opus-guide`; its Fable/Mythos/Opus self-check and effort caps do not apply to Grok.
- Treat this skill as `/harness`. Invoke another named slash command only when Grok discovered it as a skill or compatible command. If a required owner workflow is unavailable, stop and report it instead of reconstructing it from memory.
- Let the top-level Grok session own research orientation, experiment Setup and Verdict, design, implementation after Execute authorization, and verification. Prefer direct implementation for one bounded coding task; dispatch `dinnno-implementer` only when a mechanical assignment is independently useful. Keep design and experiment Verdict responsibility in the parent.
- Reserve init/spec changes, thesis-level Verdicts, thesis or comparison-axis changes, and kill/NO-GO judgments for a Fable/Mythos session. Stop with the relevant artifacts and decision question, then ask the user to route that decision; do not present a Grok recommendation as the final protected judgment.
- Map Claude `Explore` and `Plan` references to Grok's built-in `explore` and `plan` agents. Map `run_in_background`/`Monitor` to Grok's background command and monitor mechanisms. Never claim remote-control or push-notification support unless the current Grok runtime actually exposes it.
- Map the canonical `implementer` and `research-analyst` roles to the native Grok `dinnno-implementer` and `dinnno-research-analyst` profiles. Use Codex/Claude compatibility plugins only when `grok inspect` shows the named capability. Treat external or cross-model review as manual: do not start it or substitute a fresh Grok reviewer until the user explicitly confirms. After confirmation, use `dinnno-research-analyst` only when a fresh read-only Grok context provides sufficient independence; otherwise report that the requested review channel is unavailable.
- Interpret paths under `~/.claude/` in the canonical contract as compatibility sources that Grok may read. Resolve harness repository paths from this adapter's real path when checking `CHANGELOG.md` or installation state.

## Instruction conflict guard

At session entry, check whether the project root contains both `CLAUDE.md` and `AGENTS.md`.

- Ignore differences limited to platform names, invocation spelling (`/harness` versus `$harness`), or global-file pointers.
- If they disagree on current state, thesis, comparison axes, safety rules, artifact paths, active plan, compute assumptions, or workflow ownership, report `STATE CONFLICT` with both locators and do not enter Execute until the user identifies the canonical source.
- Treat `docs/RESEARCH_SPEC.md`, `docs/progress.md`, `docs/LEARNINGS.md`, and the active plan as the durable research state after resolving any conflict; do not let a stale project instruction silently replace them.

## Grok completion check

Before the final response, verify the same plan/done/progress obligations required by the canonical contract. Report the Grok model, config path, seed, commit, and run locator whenever experiment evidence exists. Do not commit, push, delete or overwrite research artifacts, or actuate a real robot without the canonical user confirmation.
