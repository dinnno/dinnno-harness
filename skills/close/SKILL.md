---
name: close
description: Verify a dinnno research session before closing it by sending the goal and artifact paths, but no self-assessment or conversation history, to a fresh read-only subagent; reconcile evidence-backed findings; then complete the $harness session contract. Use only after the user declares session close or wrap-up and accepts the review. Skip or offer to skip for lightweight question-only sessions.
---

# Close with a fresh adversarial review

The writer's context is biased toward its own result. Review “goal versus actual evidence” in a fresh subagent before completing `$harness` bookkeeping.

## 1. Dispatch a fresh reviewer

Spawn one `research-reviewer` without conversation history. Give it only:

- the full active `plan_v{N}` path, or a one-line session goal when no plan exists
- changed-file paths
- `done_v{N}`, `progress.md`, metrics, outputs, and log paths that exist

Do not pass this session's conclusion, recap, or self-evaluation.

Ask the reviewer to check:

1. success thresholds against the actual metric source
2. TODO claims against files and diff
3. completion claims lacking command output or artifacts
4. missing session log, progress timeline/matrix/header, or learning updates
5. any gap between the plan's goal/validation design and what was produced

Require findings as severity plus exact `path:line` evidence, or an explicit no-findings result.

## 2. Reconcile

Fix factual errors and contract omissions immediately and identify the changed lines. If a finding overturns the verdict through mismatched metrics or an unverified completion claim, report it and wait for the user before rewriting the done verdict.

Do not automatically repeat the review. Add one round only when a thesis-level claim was overturned.

## 3. Complete the harness close contract

Follow `$harness` §5: update TODOs, session log, paired done, progress timeline/matrix/header, current-direction block when needed, and the final verdict-first report. List any finding that could not be reconciled.

The reviewer must be fresh, read-only, and unprimed by the writer's opinion. Do not hide findings or commit/push.
