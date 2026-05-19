# references/ 사용법

## 흐름

1. **등록**: 사용자가 외부 자료 URL 보면 `/add-ref <url>` 호출. 도메인으로 Papers/Code/Homepages 자동 분류, name·날짜 자동 채움, `_INDEX.md`에 `status: pending` 행 추가.
   - 수동 추가도 가능 (slash 커맨드 안 쓰고 `_INDEX.md`에 직접 행 박기) — 같은 컬럼 형식만 지키면 됨.
2. **요약 (가벼운 카드)**: `/harness` 진입 시 `status: pending` 행 있고 **현재 작업 단위와 관련 있으면** codex:rescue로 요약 dispatch (한 줄 보고 후). 산출물: `docs/references/{name}_summary.md` — ≤300 단어 요약 + 핵심 발췌 + 우리 thesis와의 매핑 한 줄. `_INDEX.md` 갱신: `status: summarized`, `summary_path: references/{name}_summary.md`.
3. **청사진 (구현용 깊이 분석)**: 사용자가 "이건 우리 구현 대상" 결정하면 `/blueprint-ref <name>` 호출. codex:rescue dispatch, 산출물: `docs/references/blueprints/{name}.md` — 메서드 의사코드·핵심 수식·실험 셋업·thesis 비교 축·우리 코드 통합 포인트 (paper) / 아키텍처·핵심 클래스·의존성·fork할 부분 (code). `_INDEX.md` 갱신: `status: blueprinted`, `blueprint_path: references/blueprints/{name}.md`. summary_path는 유지 (누적).
4. 메인 세션은 산출물만 적재. 원본은 안 가져옴.

## status 값

- `pending` — 등록만 됨, 아직 분석 안 함
- `summarized` — 가벼운 요약 카드 생성됨
- `blueprinted` — 구현용 청사진 생성됨 (summary는 있을 수도 없을 수도)

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
