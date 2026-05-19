# References (소통창고)

> 사용자가 외부 자료(arxiv / github / homepage) URL만 박는 인박스.
> `/add-ref <url>`로 행 추가 → `/harness`가 `status: pending` 발견 시 codex:rescue로 요약 dispatch → 깊이 분석이 필요한 entry는 `/blueprint-ref <name>`로 청사진 생성.
> 분석 산출물: 가벼운 카드는 `docs/references/{name}_summary.md`, 구현용 청사진은 `docs/references/blueprints/{name}.md`.
> 메인 세션은 산출물만 적재(원본 PDF·repo 등은 메인 컨텍스트 안 가져옴).
>
> status 값: `pending` → `summarized` → `blueprinted` (누적).

## Papers

| name | url | status | summary_path | blueprint_path | added |
|---|---|---|---|---|---|
| {paper-slug} | {arxiv-url} | pending | — | — | {YYYY-MM-DD} |

## Code

| name | url | status | summary_path | blueprint_path | added |
|---|---|---|---|---|---|
| {repo-slug} | {github-url} | pending | — | — | {YYYY-MM-DD} |

## Homepages / Misc

| name | url | status | summary_path | blueprint_path | added |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... |
