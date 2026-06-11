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

### 1. type 자동 분류 (URL 도메인 기준)

- `arxiv.org`, `openreview.net`, `aclanthology.org`, `proceedings.*` → **papers**
- `github.com`, `gitlab.com`, `bitbucket.org` → **code**
- 그 외 → **homepages**

`--type` 플래그가 있으면 무조건 그 값 사용.

### 2. name 자동 생성

- arxiv abs URL: paper ID 추출 (예: `https://arxiv.org/abs/2401.12345` → `2401.12345`)
- arxiv pdf URL도 동일 ID 추출
- github/gitlab/bitbucket: `owner-repo` (슬래시 → 하이픈, 소문자, 비ASCII는 제거)
- 그 외: 도메인 + path 첫 토큰 (예: `https://example.com/foo/bar` → `example.com-foo`)

`--name` 플래그가 있으면 무조건 그 값 사용.

### 3. 중복 체크

`docs/references/_INDEX.md`를 읽어:
- 같은 URL이 이미 있으면 거부: `already in index: {existing-name} ({section})`. 종료.
- 같은 name이 다른 URL과 함께 있으면 경고하고 사용자에게 진행 여부 확인.

### 4. 행 추가

`_INDEX.md` 안에서 type에 맞는 섹션 (`## Papers` / `## Code` / `## Homepages / Misc`) 표 마지막에 행 append:

```
| {name} | {url} | pending | — | — | {YYYY-MM-DD} |
```

날짜는 시스템의 오늘 날짜 (UTC 무관, 로컬). placeholder 행 (`{paper-slug}`, `{repo-slug}`, `...`)은 건드리지 않음 — 새 행은 그 아래에 append.

### 5. 보고

한 줄: `added: {name} ({type}, pending)`

## 하지 않는 것

- URL fetch — 페이지 내용은 읽지 않음. 등록만.
- 자동 분석 dispatch — 분석은 `/harness` 또는 `/blueprint-ref`가 따로 트리거.
- placeholder 행 ({...}) 삭제 또는 변경.
- `_INDEX.md` 외 파일 수정.

## scope 밖

- 이 커맨드는 `_INDEX.md`만 건드린다. `_GUIDE.md`, `summary`, `blueprints/` 모두 손대지 않음.
