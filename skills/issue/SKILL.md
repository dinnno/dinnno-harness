---
name: issue
description: Break a looping robotics-research or implementation deadlock by recording only the actual decision history in the configured second-brain vault under fable/issues, then hand it to a fresh Codex context. Use when the user says the same concern or fix keeps looping, or explicitly invokes $issue. With no new deadlock in the current conversation, list and consume open issue files instead. Do not use for a simple TODO or a one-line learning.
---

# Preserve a looping issue

The purpose is to stop discarded options from being rediscovered after context loss. Use the second-brain vault path configured in the active global `AGENTS.md`. If it cannot be resolved, ask the user for the vault location.

## Write mode

1. Create `fable/issues/YYYY-MM-DD_{project}_{slug}.md`, with an English kebab-case slug. Include only facts, options, and arguments that actually occurred in this conversation. Quote a user intuition exactly only when it was stated; never invent missing branches.
2. In a dinnno project, append `- [ ] {date} [issue] {one line} ← fable/issues/{filename}` to the `progress.md` decision queue.
3. Report the path and the single requested next action. Do not commit or push the vault.

Use this schema:

```markdown
---
type: issue
project: {project}
status: open
created: {YYYY-MM-DD}
tags: [{english-kebab-tag}]
---
# {blocked point in one line}

## 왜 지금 필요한가
{what remains blocked}

## 고민/시도의 흐름
{option-by-option evidence and the exact loop, for example A drawback → B → B drawback → A}

## 사용자 직감 (원문 그대로)
{verbatim intuition, or "없음"}

## 다음에 원하는 것
{one of: fresh Codex interrogation, fresh retry from this file, independent research-reviewer diagnosis; include why}

## 결론
{the resolving session fills this and changes status to resolved}
```

## Consume mode

When invoked without a new deadlock in the current conversation:

1. List `status: open` files from `fable/issues/` as file, title, and creation date; let the user select one.
2. Read only the selected file and follow `다음에 원하는 것`. For a fresh subagent diagnosis, use no inherited conversation context and provide only the issue path and desired output.
3. If resolved, fill `결론`, set `status: resolved`, and append one project `LEARNINGS.md` line when the resolution is reusable. If unresolved, append this round to the flow instead of overwriting history.

Always preserve the issue before another attempted solution. Do not update vault `wiki/`, `index.md`, or `log.md`, and do not commit or push.
