---
name: harness
description: Orient and run one thesis-driven unit in a dinnno robotics research project by loading RESEARCH_SPEC, progress, learnings, and the current plan, then guiding init, spec, experiment, sweep, or autoloop work through Setup, Execute, and Verdict. Use for research work in repositories containing the dinnno docs scaffold; do not use for ordinary coding repositories or project-wide audits.
---

# Research session harness

Treat this as a thin research orientation and artifact contract, not a mechanical stage gate. Follow the active `AGENTS.md` instruction chain.

One hypothesis belongs to one session. Complete Setup → Execute → Verdict inside that hypothesis, but never create or enter the next hypothesis automatically.

## 1. Load the minimum state

Read only:

1. `docs/RESEARCH_SPEC.md`: thesis in §1 and comparison axes in §4.
2. `docs/progress.md`: stage, timeline, matrix, and decision queue.
3. `docs/LEARNINGS.md`: repeated mistakes to avoid.
4. The active `docs/plans/plan_v{N}_*.md`, if one exists.

List the latest non-template filenames in `docs/plans/` and `docs/done/`; do not load old versions unless a specific fact requires them. For an autoloop unit, also read `docs/LOOP.md`.

Warn in one line when the spec still has placeholders or progress/learnings are missing.

If the user explicitly says the harness was updated, resolve this `SKILL.md` symlink to its real path and read the harness repository's `CHANGELOG.md` (two levels above `skills/harness/`). Compare entries after project `AGENTS.md` `last-sync`. Repair only broken contract names, paths, and pointers after reporting the proposed sync. Preserve all thesis, plan, and done prose. Update `last-sync` when finished.

## 2. Confirm one unit

Summarize the current state and recommend exactly one unit. Ask for confirmation before entering it:

- `(init)`: fill scaffold placeholders. Follow `docs/_GUIDE.md` Init protocol.
- `(spec)`: change thesis or comparison axes. Treat this as a user-owned research decision.
- `(experiment v{N})`: start or resume one hypothesis.
- `(sweep)`: traverse only pre-approved pending ablations from `RESEARCH_SPEC §6` and the progress matrix. Require explicit opt-in. Stop on any experiment-level anomaly.
- `(autoloop)`: after a working baseline, diagnose `docs/LOOP.md` L1–L7. Fill missing gates as a loop-prep unit. If all gates pass, write a thin priority/budget/stop plan and obtain one Execute authorization for trials strictly inside the allowlist and budget.

Do not guess when the unit is ambiguous. During the session, append a user-stated new research idea immediately to the progress decision queue as a `💡` line. Recording is not adoption.

## 3. Run an experiment

### Setup

Copy `docs/plans/_plan_template.md` to the next `plan_v{N}_{short-name}.md`. Tie it to one spec limitation, specify the minimum module, validation, success thresholds, stop conditions, and budget. Use section 6 as the working checklist. Ask once: “이 plan으로 Execute 시작?”

### Execute

After authorization, implement, train, and evaluate within the plan. Start at the first unchecked section 6 item unless the user names another. Announce each item transition briefly.

For a long command, start it through the available background/process-session mechanism, retain its session identifier, and poll it. While it runs, prepare evaluation or Verdict artifacts inside the current hypothesis.

Inside the approved budget, fix identified code-level faults and perform cheap reruns. Stop and report raw evidence for divergence, hypothesis contradiction, a second failure after one fix, an expensive rerun, or any design change.

### Verdict

Copy `docs/done/_done_template.md` to `done_v{N}.md`. Record files, commands, seed × rollout counts, mean±std or CI, config, commit, run paths, expected-versus-observed gaps, and paper impact. Obtain an independent `research-reviewer` pass when the result affects a claim; save it as `done_v{N}_review.md`.

For a negative result, apply the four Kill/Pivot validity gates in `docs/done/_GUIDE.md`. Downgrade unsupported claims to insufficient evidence. Never conclude kill inside Execute or autoloop.

Offer two or three next-plan candidates in recommendation order, then stop. The user must choose the next hypothesis in a new session.

## 4. Delegate selectively

Announce each dispatch with scope and expected return, then do not duplicate it.

- Use built-in `explorer` for broad read-only repository mapping or call-graph work.
- Use `research-reviewer` for PDFs, large logs, broad consistency analysis, research diagnosis, or independent Verdict review. Keep the main thread on the returned summary or artifact.
- Use `implementer` only after the plan is approved, for bounded mechanical implementation. The parent retains design and verdict responsibility.
- Parallelize only independent work. Avoid concurrent write-heavy tasks.

If a pending reference is relevant to the current unit, announce a summary dispatch to `research-reviewer`. Save a ≤300-word card at `docs/references/{name}_summary.md`, update its index status to `summarized`, and load only the card into the main thread. Use `$blueprint-ref` only after the user decides the source is an implementation target.

When hypothesis generation is stalled, query the configured second-brain vault once with a read-only reviewer and map two or three methodology hints back to the current thesis. Use broad web research only after the vault is unhelpful.

## 5. Close the session

Before returning a final message:

- Check completed plan section 6 items and append one section 5 log line.
- Finish the paired done or record why the hypothesis is still running.
- After spec/done work, update progress timeline, ablation cell, Stage, anchored commit, seed, and checkpoint pointers together.
- Land deferred thesis-level decisions in the progress decision queue.
- Append a dated `LEARNINGS.md` line only for a genuinely repeated mistake or reusable lesson.

Do not commit or push without approval. Do not delete or overwrite data, checkpoints, or runs. Never actuate a real robot without explicit confirmation.
