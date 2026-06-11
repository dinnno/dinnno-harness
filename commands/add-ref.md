---
description: 외부 자료 URL을 docs/references/_INDEX.md 인박스에 한 줄 등록(type 자동분류·slug 생성·중복체크). URL fetch나 내용 분석은 하지 않는다 — 분석은 /blueprint-ref.
---

사용자가 외부 자료 URL을 References 인박스 (`docs/references/_INDEX.md`)에 등록하는 커맨드.

## 사용법

```
/add-ref <url> [--name <slug>] [--type papers|code|homepages]
```

예시:
- `/add-ref https://arxiv.org/abs/2401.12345`
- `/add-ref https://github.com/foo/bar`
- `/add-ref https://example.com/dataset --name awesome-bench --type homepages`

## 동작

### 1. type 분류 / name 생성 (`--type`·`--name` 플래그 있으면 그 값 우선)

- **type**: arxiv·openreview·aclanthology·proceedings → papers / github·gitlab·bitbucket → code / 그 외 → homepages.
- **name (slug)**: arxiv → paper ID(`2401.12345`) / git host → `owner-repo` / 그 외 → `도메인-path첫토큰`. **slug 정규화: 소문자 · 슬래시→하이픈 · 비ASCII 제거** (이 규칙이 `/blueprint-ref` 이름 조회의 전제).

### 2. 중복 체크

`docs/references/_INDEX.md`를 읽어:
- 같은 URL이 이미 있으면 거부: `already in index: {existing-name} ({section})`. 종료.
- 같은 name이 다른 URL과 함께 있으면 경고하고 사용자에게 진행 여부 확인.

### 3. 행 추가

`_INDEX.md` 안에서 type에 맞는 섹션 (`## Papers` / `## Code` / `## Homepages / Misc`) 표 마지막에 행 append:

```
| {name} | {url} | pending | — | — | {YYYY-MM-DD} |
```

날짜는 시스템의 오늘 날짜 (UTC 무관, 로컬). placeholder 행 (`{paper-slug}`, `{repo-slug}`, `...`)은 건드리지 않음 — 새 행은 그 아래에 append.

### 4. 보고

한 줄: `added: {name} ({type}, pending)`

## 하지 않는 것

- URL fetch/내용 분석 ❌ (등록만 — 분석은 `/harness` 또는 `/blueprint-ref`).
- placeholder 행({...}) 삭제·변경 ❌.
- `_INDEX.md` 외 파일 수정 ❌ (`_GUIDE.md`·summary·`blueprints/` 손대지 않음 — `_INDEX.md`만).
