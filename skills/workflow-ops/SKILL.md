---
name: workflow-ops
description: Apply dinnno operational rules for parallel research Execute stages, sweeps, autoloops, and long-running simulation, training, benchmark, or preprocessing commands. Load immediately before such work to define memory caps, process monitoring, subagent boundaries, failure handling, and durable artifact locations. This skill configures the run; it does not authorize Execute or start a workflow by itself.
---

# Parallel and long-running research operations

This skill refines `$harness` Execute. It never authorizes a hypothesis, crosses a hypothesis boundary, or owns the final Verdict.

## 1. Stage work safely

- Parallelize only independent read-heavy analysis, tests, or isolated execution. Avoid concurrent writes to the same checkout; use separate worktrees only when the setup cost is justified and the user has requested parallel agent work.
- Use `implementer` for approved mechanical edits and the parent or a fresh `research-reviewer` for verdict work. Return metrics and artifact paths to the parent; the final research decision remains there.
- Put the exact scope, expected artifact, stop condition, memory cap, and timeout in every dispatched agent prompt. Do not assume this skill's body is inherited.

## 2. Bound and monitor long runs

- Estimate peak host RAM before starting, including `workers × parent-data copy` and simultaneous stages. Keep the sum of concurrent stage caps at or below half of currently available host RAM unless the user explicitly chooses another budget.
- Prefer GPU kernels. Do not silently invoke an unbounded CPU fallback. On Linux with user systemd, run first-use scripts, benchmarks, and preprocessing under `systemd-run --user --scope -p MemoryMax={N}G -- <cmd>`.
- Start a long command with the available process-session/background mechanism. Preserve its session ID, poll without restarting it, and report progress at least once per minute while work is ongoing.
- For a subagent that cannot retain a process session reliably, require the launched script to write distinct success and failure marker files. Poll the marker and process liveness with a total wait cap from the plan; stop when the process dies or the cap expires.
- A structured-output request or parent message is not evidence that the run finished. Return only after a terminal process state or a durable completion marker.

## 3. Make orchestration resumable

- Treat an empty or failed agent result as an explicit failed stage; never filter it into apparent success.
- Validate resumed arguments before branching, especially when structured arguments may arrive as strings.
- Pass timestamps and seeds as inputs. Do not create hidden time- or randomness-dependent branches in orchestration scripts.
- Stop and report on experiment-level anomalies; do not launch an automatic replacement run.

## 4. Preserve artifacts

- Store reusable orchestration scripts in a permanent project path such as `scripts/workflows/`, not a temporary session directory.
- Never cite `/tmp`, an ephemeral worktree, or session-only paths from plans, done files, or handoffs. Copy required evidence into a durable project or run path first.
- Land sweep results in the progress ablation matrix and autoloop trials in the ledger. Before Verdict, verify that every completed stage has a durable result or an explicit failure record.
