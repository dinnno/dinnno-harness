# references/ 사용법

## 흐름

1. 사용자: 외부 자료 보면 `_INDEX.md`에 한 행 추가 (URL + name + `status: pending`).
2. `/harness` 진입 시: `_INDEX.md`에 `status: pending` 행이 있고 **현재 작업 단위와 관련 있으면** codex:rescue로 분석 dispatch (사용자에게 한 줄 보고 후).
3. codex:rescue 산출물: `docs/references/{name}_summary.md` (≤300 단어 요약 + 핵심 발췌 + 우리 thesis와의 매핑 한 줄).
4. `_INDEX.md` 갱신: `status: analyzed`, `summary_path: references/{name}_summary.md`.
5. 메인 세션은 이후 summary만 적재. 원본은 안 가져옴.

## 무엇을 _INDEX.md에 박나

- 우리 thesis와 관련된 paper (해당 분야 SOTA, 우리가 비교할 baseline)
- 우리가 참조하거나 fork할 가능성 있는 code repo
- 데이터셋/벤치마크 homepage
- 우리 thesis와의 관련성이 **있을 수 있는** 자료. "확실히 안 쓸 거"는 박지 마.

## 무엇을 박지 않나

- 우리 코드 내부 docs (이미 `docs/`에 있음)
- 일회성 quick-look (URL만 보고 끝)

## codex:rescue가 분석하면 안 되는 자료

- 사용자가 명시적으로 분석 요청 안 한 PDF로 인터넷에 떠도는 paper (저작권 회피 + 의미 없는 토큰 소비). 사용자 의도 확인 후만 dispatch.
