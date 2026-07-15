---
name: tidy
description: Scan a dinnno research project for consumed or superseded session artifacts, classify them by content and references, obtain user confirmation, then move approved items into docs/archive/YYYY-MM and update an archive index without deleting history. Use when root/docs Markdown has become cluttered; never touch plans, done, references, experiments, or current canonical docs.
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

Verify before/after artifact counts. Report moved count, held count, and index path in three lines or fewer. Do not commit or push.
