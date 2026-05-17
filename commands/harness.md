이 세션은 dinnno-harness 워크플로우를 따른다. 한 세션 = 하나의 단위 작업 (spec 갱신 / 새 plan / plan 구현 / done 작성 중 하나).

## 1. 현황 파악

- `docs/RESEARCH_SPEC.md` 읽고 thesis와 비교 축 확인. 없으면 사용자와 함께 작성부터.
- `docs/plans/` 안의 마지막 `plan_v{N}_*.md` 확인.
- `docs/done/` 안의 마지막 `done_v{N}.md` 확인.

## 2. 이 세션이 할 일 판단

위 현황 기준으로 다음 중 무엇인지 사용자에게 한 줄로 확인:
- (a) spec 갱신 — spec이 실험 결과와 어긋남
- (b) 새 `plan_v{N+1}_*.md` 작성 — 마지막 plan이 닫혔고 다음 실험 시작
- (c) 진행 중 plan 구현 — plan은 있고 done은 없음
- (d) `done_v{N}.md` 작성 또는 외부 리뷰 반영 수정

## 3. 작업

- 해당 폴더(`docs/plans/`, `docs/done/`, `src/`, ...)의 CLAUDE.md 가이드를 따른다.
- 전역 4원칙(Think Before / Simplicity / Surgical / Goal-Driven) 준수.
- Scope 밖 파일은 건드리지 않는다.

## 4. 세션 정리

- 이번에 변경한 파일·결정 사항을 plan 또는 done 파일에 한 줄로 추가.
- 다음 세션이 이 파일만 읽고도 이어받을 수 있게.

## 하지 않는 것

- 여러 step 자동 chain. 한 세션 = 한 단위.
- 사용자 승인 없이 git commit/push.
- 실패 시 자동 재시도. 실패 사실을 사용자에게 보고하고 결정 받기.
