---
name: harness
description: Orient and run one thesis-driven unit in a dinnno robotics research project by loading RESEARCH_SPEC, progress, learnings, references, and the current plan, then guiding init, spec, experiment, sweep, or autoloop work through Setup, Execute, and Verdict. Use for research work in repositories containing the dinnno docs scaffold; do not use for ordinary coding repositories or project-wide audits.
---

# Research session harness

Treat this as a thin research orientation and artifact contract, not a mechanical stage gate. Follow the active `AGENTS.md` instruction chain. One hypothesis belongs to one session: complete Setup → Execute → Verdict inside it, but never create or enter the next hypothesis automatically.

## Boundaries

Stop only at these HARD boundaries:

1. confirming the session unit
2. authorizing Execute after the plan
3. crossing to a new hypothesis, except pre-approved rows inside an opted-in sweep
4. git commit or push
5. destructive deletion or overwrite of data, checkpoints, or runs
6. real-robot actuation
7. retry after experiment-level failure: diverged loss, contradictory result, or a second failure after one fix; also report before any expensive multi-hour rerun
8. changing the thesis or comparison axes
9. leaving an autoloop allowlist, changing code inside the loop, or continuing after its budget
10. a kill or NO-GO conclusion, even after the four validity gates

Announce and continue at SOFT boundaries: subagent dispatch, background run start with its memory cap, plan checklist transition, and one autoloop ledger verdict. Inside an authorized Execute, finish cheap plan-preserving fixes and reruns without asking again. When the user asks only for diagnosis, report the diagnosis and do not edit.

## 1. Load the minimum state

Read:

1. `docs/RESEARCH_SPEC.md`: current-direction block, thesis, and comparison axes.
2. `docs/progress.md`: stage, timeline, matrix, decision queue, and idea inbox.
3. `docs/LEARNINGS.md`: repeated mistakes to avoid.
4. The active `docs/plans/plan_v{N}_*.md`, when a unit is in progress.
5. `docs/references/_INDEX.md`: scan `status: pending` rows and load only rows relevant to this unit.

List the latest non-template filenames in `docs/plans/` and `docs/done/`; do not load old versions without a specific need. For an autoloop unit, also read `docs/LOOP.md`.

Warn in one line when the spec has placeholders or progress/learnings are missing. If a referenced contract surface such as `docs/LOOP.md`, the decision queue, idea inbox, or `docs/done/_GUIDE.md` Kill/Pivot section is absent, propose creating it instead of silently skipping it.

### Harness sync

Resolve this skill's real `SKILL.md` path. The harness repository root is two parents above `skills/harness/`. Skip sync if resolution fails or the current project is the harness repository itself.

Compare the project root `AGENTS.md` `last-sync:` marker with the harness `CHANGELOG.md`. The marker identifies the last applied entry by date plus a short title; a date-only legacy marker makes all entries on and after that date candidates. A missing or placeholder marker makes every entry a candidate.

Only when newer entries exist:

1. List contract-name, section, status, and pointer differences caused by those entries.
2. Ask once which proposed changes to apply or defer.
3. Update only structure, names, and pointers. Preserve all `RESEARCH_SPEC.md`, historical plan, and done prose; folder `_GUIDE.md` and folder `AGENTS.md` remain syncable contract files.
4. Advance `last-sync:` to the final examined entry whether it was applied, already matched, or explicitly deferred. Record only deferred items as `- 보류: {entry} — {reason}`.

Artifact hygiene is owned by `$tidy`; do not scan loose handoff files during ordinary entry.

## 2. Confirm exactly one unit

Summarize the state and recommend one unit. Obtain confirmation before entering it:

- `(init)`: fill placeholders in root `AGENTS.md`, `docs/RESEARCH_SPEC.md`, and `docs/ARCHITECTURE.md`; follow `docs/_GUIDE.md` Init protocol.
- `(spec)`: change thesis or comparison axes. Treat it as a user-owned research decision.
- `(experiment v{N})`: start or resume one hypothesis.
- `(sweep)`: require explicit opt-in. Write one thin plan listing pre-approved pending ablation rows and a per-row budget. Traverse only rows declared in `RESEARCH_SPEC §6`; stop on experiment-level anomalies and never generate a new hypothesis.
- `(autoloop)`: after a working baseline, diagnose `docs/LOOP.md` L1–L7. Fill missing gates as loop-prep. If all pass, write a thin priority/budget/stop plan; one Execute confirmation authorizes only trials inside that allowlist and budget.

Do not guess when the unit is ambiguous.

During the session:

- Append a user-stated research idea immediately to the progress idea inbox as `💡`. Recording is not adoption; do not evaluate it unless asked.
- Codex may add at most one or two grounded ideas per session as `💡 [codex] {idea} — {one-line evidence}`. This is also not adoption.
- When the user identifies a Codex mistake or asks to prevent recurrence, append one dated line to `docs/LEARNINGS.md` in that turn and show the exact line written.
- When the same concern or fix loops, propose `$issue`; run it only after the user accepts.

## 3. Run the confirmed unit

### Setup

Copy `docs/plans/_plan_template.md` to the next `plan_v{N}_{short-name}.md`. If the template is absent, use the root `AGENTS.md` naming map or the previous plan's structure. Tie the plan to one spec limitation and specify the minimum module, validation, success thresholds, stop conditions, and budget.

Section numbers in this skill refer to the template. If a project plan differs, map by heading meaning such as success thresholds, session log, and TODO. End Setup by asking once, “이 plan으로 Execute 시작?” Include the recommended plan and its strongest alternative with one sentence explaining why it was not chosen.

### Execute

After authorization, implement, train, and evaluate within the plan. Start at the first unchecked TODO unless the user names another. Announce each TODO transition briefly.

Before a first-run script, benchmark, preprocessing job, or unknown-memory command, estimate peak host RAM including worker/process multiplication. Use a bounded scope such as `systemd-run --user --scope -p MemoryMax={N}G -- <cmd>` on Linux when available. Prefer the GPU implementation and do not silently fall back to an unbounded CPU kernel.

Run long commands through the available process-session/background mechanism, retain the session identifier, poll it, and keep the user updated during long waits. Invoke `$workflow-ops` before parallel Execute, a sweep, or a long-running multi-stage workflow.

Inside the approved budget, fix identified code-level faults and perform cheap reruns. Stop with raw evidence at an experiment-level anomaly or HARD boundary. After the user chooses, enter Verdict or revise the plan; do not silently restart the experiment.

### Verdict

Copy `docs/done/_done_template.md` to `done_v{N}.md`, using the same fallback rule if absent. Record files, commands, seed × rollout counts, mean±std or CI, config, commit, run paths, expected-versus-observed gaps, and paper impact.

Obtain an independent `research-reviewer` pass when the result affects a paper claim and save it as `done_v{N}_review.md`. Do not repeat review automatically. After two rounds with findings still open, ask whether to continue; add one immediate round only when a thesis-level claim was overturned.

For a negative result, apply the four Kill/Pivot validity gates in `docs/done/_GUIDE.md`. Downgrade unsupported claims to insufficient evidence. Never conclude kill inside Execute or autoloop.

Offer two or three next-plan candidates in recommendation order, based on paper impact, then stop. The user chooses the next hypothesis in a new session.

## 4. Delegate selectively

Announce each dispatch with scope and expected return, then do not duplicate it.

- Use built-in `explorer` for broad read-only repository mapping.
- Use `research-reviewer` for PDFs, large logs, broad consistency analysis, research diagnosis, reference summarization, or independent Verdict review.
- Use `implementer` only after the plan is approved, for bounded mechanical implementation. The parent retains design and verdict responsibility.
- Parallelize only independent work; avoid concurrent write-heavy tasks. Let custom agents inherit the parent model unless their agent file intentionally pins a setting.

If a pending reference is relevant, announce a summary dispatch. Save a ≤300-word card at `docs/references/{name}_summary.md`, update its row to `summarized`, and load only that card into the main thread. Use `$blueprint-ref` only after the user selects the source as an implementation target.

When hypothesis generation stalls, query the configured second-brain vault once with a read-only reviewer and map two or three methodology hints to the current thesis. Use broad web research only if the vault is unhelpful.

## 5. Close the session

When the user declares session close or wrap-up, propose `$close` before bookkeeping. Run it only after acceptance; lightweight question-only sessions may explicitly skip the fresh review.

Before the final message:

1. Check completed plan TODOs and append one session-log line.
2. Finish the paired done or record why the hypothesis remains active.
3. After spec/done work, update the progress timeline, ablation cell, Stage, anchored commit, seed, and checkpoint pointers together. A done metric must not leave its matrix cell as unmeasured.
4. If thesis or methodology moved, update `RESEARCH_SPEC.md` `현재 방향 (second brain 동기용)` with current values only, not history or metrics.
5. Land deferred thesis-level decisions in the progress decision queue and immediately flip completed root handoff items.
6. Append a learning only for a reusable or repeated failure.

Do not end with empty TODO/log/progress bookkeeping or defer it to “the next session.”

Report a one-line verdict with measured numbers, then four short paragraphs: the unit and thesis axis; what actually changed or ran; the expected-versus-observed gap and evidence; two or three ranked next-session candidates. Never claim done without execution output or a concrete diff.
