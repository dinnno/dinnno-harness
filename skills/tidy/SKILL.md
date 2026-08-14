---
name: tidy
description: Scan a dinnno research project for consumed or superseded session artifacts, classify them by content and references, obtain user confirmation, then move approved items into docs/archive/YYYY-MM and update an archive index without deleting history; optionally repair confirmed stale state lines in canonical status and guide documents. Use when root/docs Markdown has become cluttered or current guidance has drifted; never rewrite historical plan, done, or spec prose.
---

# Archive consumed session artifacts

Never delete. Preserve file count and history.

## 1. Scan only allowed candidates

Collect:

- root session artifacts such as `HANDOFF_TO_*.md`, `CHANGELOG_*.md`, dated variants, and audit-output directories
- loose Markdown directly under `docs/` outside the canonical set: `RESEARCH_SPEC.md`, `ARCHITECTURE.md`, `LEARNINGS.md`, `progress.md`, `AGENTS.md`, `_GUIDE.md`

Do not scan inside `docs/plans/`, `docs/done/`, `docs/references/`, `docs/experiments/`, or `docs/archive/`. Never consider root `README.md` or `AGENTS.md`.

## 2. Classify from content

Read each candidate and search live references before assigning:

- `superseded`: a newer current artifact of the same lineage exists
- `consumed`: all handoff/repair work is complete and reflected elsewhere
- `stale`: no live references and its useful content was absorbed or became obsolete
- `hold`: evidence is ambiguous or the artifact remains active

Modification time is supporting evidence only. A pending handoff is never an archive candidate.

## 3. Confirm moves

Show a table with file, proposed class, evidence, and last modification date. Ask the user to approve all, some, or none. This confirmation is mandatory.

## 4. Move and index

For each approved item:

1. Read it once more and write a one-line “what it was and how it was consumed” summary.
2. Move it to `docs/archive/YYYY-MM/` using its modification month. Preserve tracked history with `git mv`; use a date suffix on name collision.
3. Add a newest-first entry under the matching month in `docs/archive/_INDEX.md`:

```text
- `old/path` → `new/path` — {superseded|consumed|stale} · {one-line summary}
```

4. Update live links to the new path only when unambiguous; otherwise report them.

Verify before/after artifact counts. Report moved count, held count, and index path in three lines or fewer.

## 5. Repair stale live state separately

When the user requests it or the archive scan exposes a stale line, compare only these live surfaces:

- `progress.md`: Stage/anchored commit versus the latest timeline row, consumed-but-open decision items, and obsolete open debt
- root `AGENTS.md` current-state lines versus the latest real plan/done files
- `references/_INDEX.md`: a pending row whose owning unit is complete
- `docs/**/_GUIDE.md` and folder `AGENTS.md`: a rule that conflicts with the current `$harness` contract

Judge only from document-to-document evidence, never modification time or intuition. Show document, exact stale line, evidence, and proposed update/check/removal; obtain confirmation before editing. Treat uncertain candidates as hold.

Do not rewrite `RESEARCH_SPEC.md`, historical plans, or done prose. A spec may receive only a stale-warning comment. Folder guides may be corrected in this pass but remain excluded from archive moves. Do not commit or push.
