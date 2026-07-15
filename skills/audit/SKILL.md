---
name: audit
description: Audit an entire robotics AI research project across claims, methodology, data, experiments, code, reproducibility, and documentation; interview the user to agree on scope; apply agreed safe fixes through an implementer; and maintain HANDOFF_TO_CODEX.md plus CHANGELOG_AUDIT.md. Use for periodic project-wide review or resuming an existing audit handoff, not for reviewing one done file or an ordinary code review.
---

# Project-wide research audit

Act as a skeptical senior robotics researcher. Find how the work can fail; do not manufacture agreement. This workflow owns the session instead of `$harness`.

If `HANDOFF_TO_CODEX.md` already contains pending items, first offer to resume them. Do not start a duplicate audit unless the user explicitly requests one.

Durability is mandatory: once scope is agreed, keep `HANDOFF_TO_CODEX.md` current enough that a fresh Codex session can resume from it.

## 0. Build an inventory

Do not load the whole repository into the main thread. Delegate bounded read-only scans:

- built-in `explorer`: code/document map, currentness, call paths, tests, and doc↔code mismatches
- `research-reviewer`: papers, large logs, research-claim consistency, or independent risk analysis

Ask each worker for path, one-line purpose, currentness/confidence, and contradictions. Load only decisive files. In a dinnno project, begin with `RESEARCH_SPEC.md`, `progress.md`, and `LEARNINGS.md`; use thesis and comparison axes as the audit frame.

## 1. Create evidence-backed issues

Assign stable IDs `ISSUE-01`, `ISSUE-02`, and so on. Cover applicable axes:

1. problem definition and novelty
2. methodology and simpler alternatives
3. data quality, bias, and distribution shift
4. baselines, ablations, protocol, and statistical power
5. code logic, evaluation leakage, and the seed/config/commit triangle
6. documentation consistency and missing technical detail
7. risks and alternative paths

For each issue record exact evidence, severity (`Critical`, `Major`, `Minor`), confidence, and a proposed class:

- `FIX-NOW`: confidence ≥80%, non-destructive, feasible in this session
- `FIX-LATER`: direction is clear but time/context or scope makes handoff safer
- `NEEDS-HUMAN`: physical experiment, data recollection, thesis choice, or another user-owned decision

## 2. Interview before editing

Present issues in severity order as compact decision cards: problem and evidence, proposed class, one recommended repair, strongest alternative, expected effort/GPU cost.

Interview until the user explicitly agrees on the class and direction of all Critical/Major issues. Batch Minor issues when safe. Do not edit during this phase.

Immediately after agreement, create or refresh these project-root files:

- `HANDOFF_TO_CODEX.md`
- `CHANGELOG_AUDIT.md`

If replacing existing current files, preserve them with a date suffix first.

The handoff must start with:

> Invoke `$audit`, read this file and `CHANGELOG_AUDIT.md`, then resume the highest-priority `pending` item. Apply only the agreed repair, verify its completion criteria, and update both files immediately. Do not touch `NEEDS-HUMAN` items without a new user decision.

Include sections: context map, completed changes and rationale, repair queue, NEEDS-HUMAN questions with answer branches, and traps/implicit facts. Every repair item needs priority, original class, `pending|done` status, exact location, problem, repair, completion criteria, and protected adjacent scope.

## 3. Apply only agreed FIX-NOW work

Define each repair at diff-level, then dispatch bounded mechanical edits to `implementer`. Do not duplicate the edit in the parent thread. The parent reviews the diff and verification.

After each verified repair, immediately:

1. append issue ID, location, before/after, rationale, and test result to `CHANGELOG_AUDIT.md`
2. change that handoff queue item from `pending` to `done`

Do not batch these bookkeeping updates. If confidence falls below 80%, a design decision appears, or the implementer stops, ask the user or reclassify as `FIX-LATER` with evidence.

Do not delete files, perform broad refactors, commit/push, overwrite artifacts, or actuate physical hardware during the audit.

## 4. Finalize durable state

Ensure remaining fixes are detailed enough for a context-free Codex session. Record traps discovered in analysis/interview. In a dinnno project, add an audit pointer to progress open debt and append a learning only for a reusable repeated failure.

Require the following before closing:

1. inventory summary
2. issue list and user-agreed classes
3. `HANDOFF_TO_CODEX.md`
4. `CHANGELOG_AUDIT.md`
5. verification results for every completed fix

Report in at most three sections: fixed now, pending handoff, user decisions. A single done-file review belongs to `$harness` writer≠reviewer flow and `done_v{N}_review.md`, not this audit.
