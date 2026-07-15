---
name: add-ref
description: Register a paper, code repository, dataset, benchmark, or homepage URL in a dinnno project's docs/references/_INDEX.md inbox with type classification, normalized slug, duplicate checks, and local date. Use when the user wants to save a source for later; do not fetch, summarize, or analyze the URL.
---

# Add a reference

Accept a URL plus optional `--name <slug>` and `--type papers|code|homepages` intent.

## 1. Classify and name

Honor explicit name/type first. Otherwise classify:

- arXiv, OpenReview, ACL Anthology, proceedings → `papers`
- GitHub, GitLab, Bitbucket → `code`
- everything else → `homepages`

Generate the slug as follows:

- arXiv → paper ID such as `2401.12345`
- Git host → `owner-repo`
- other → `domain-first-path-token`

Normalize to lowercase, replace slashes with hyphens, and remove non-ASCII characters. This normalization is the lookup contract used by `$blueprint-ref`.

## 2. Check duplicates

Read `docs/references/_INDEX.md`.

- If the URL already exists, stop with `already in index: {existing-name} ({section})`.
- If the generated name belongs to another URL, warn and ask whether to proceed.

## 3. Append one row

Append beneath the relevant `## Papers`, `## Code`, or `## Homepages / Misc` table:

```text
| {name} | {url} | pending | — | — | {YYYY-MM-DD} |
```

Use the system's local date. Keep placeholder rows unchanged. Modify no file other than `_INDEX.md`.

Return `added: {name} ({type}, pending)`. Do not access the URL or create summaries/blueprints.
