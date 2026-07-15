---
name: blueprint-ref
description: Turn one already-registered entry in docs/references/_INDEX.md into an implementation-level paper, code, or homepage blueprint using a read-only research-reviewer subagent, then save it under docs/references/blueprints and update the index. Use only after the user chooses a registered source as an implementation target; do not use for inbox registration or lightweight summaries.
---

# Blueprint a registered source

Accept the reference `name` used in `docs/references/_INDEX.md`.

## 1. Resolve the entry

Find the exact name and collect URL, section-derived type, status, and optional summary path.

- If absent, stop with `not found: {name}. 먼저 $add-ref로 등록.`
- If duplicated across sections, ask the user to identify the intended entry.

Read `docs/RESEARCH_SPEC.md` for thesis mapping. Read an existing summary card if present.

## 2. Dispatch read-only analysis

Announce `blueprinting: {name} ({type}) via research-reviewer`, then delegate the URL, type, name, spec, and optional summary to a `research-reviewer` subagent. Ask it to return complete Markdown, source-backed facts, explicit unknowns, and no file edits.

Require the shape matching the entry type.

### Paper

```markdown
# blueprint: {name}
## 1줄 요지
## 메서드 의사코드
## 핵심 수식·하이퍼파라미터
## 실험 셋업
## thesis 비교 축 매핑
## 우리 코드 통합 포인트
```

The pseudocode must identify inputs, outputs, and loops. Record losses, constants, dataset, metrics, baselines, config separation, target modules, and any vendored dependency without copying long source passages.

### Code repository

```markdown
# blueprint: {name}
## 1줄 요지
## 아키텍처 (텍스트 다이어그램)
## 핵심 클래스·함수
## 의존성
## fork 전략
## thesis 비교 축 매핑
```

Require exact upstream paths where verifiable, version/GPU constraints, keep/drop boundaries, and proposed integration paths. Never edit `libs/`.

### Homepage or other source

```markdown
# blueprint: {name}
## 1줄 요지
## 의미 있는 부분
## 판정
- [ ] 구현 대상
- [ ] 폐기
```

Capture dataset links, evaluation protocol, and license when relevant.

## 3. Save and index

Validate that the returned Markdown distinguishes fact from inference and maps to the current thesis. Save it to `docs/references/blueprints/{name}.md`, creating the directory if needed.

Update only the matching index row:

- status → `blueprinted`
- blueprint_path → `references/blueprints/{name}.md`
- preserve summary_path

Return `blueprinted: {name} → {path}. 요지: {one sentence}`. Keep the full blueprint out of the main-thread recap. On analysis failure, report it and stop; do not retry automatically.
