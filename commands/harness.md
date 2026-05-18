이 세션은 dinnno-harness 워크플로우를 따른다. 한 세션 = 하나의 단위 작업 (spec 갱신 / 새 plan / plan 구현 / done 작성 중 하나).

## 1. 현황 파악

- `docs/CLAUDE_AGENTS.md` 먼저 읽어 agent dispatch 매트릭스를 적재한다.
- `docs/RESEARCH_SPEC.md` 읽고 thesis와 비교 축 확인. 없으면 사용자와 함께 작성부터.
- `docs/plans/` 안의 마지막 `plan_v{N}_*.md` 확인.
- `docs/done/` 안의 마지막 `done_v{N}.md` 확인.
- 새 프로젝트거나 코드 베이스 첫 접촉이면 `Explore` 1개 자동 dispatch — `docs/CLAUDE_AGENTS.md` 매트릭스 "새 프로젝트 첫 plan_v0" 행.

## 2. 이 세션이 할 일 판단

위 현황 기준으로 다음 중 무엇인지 사용자에게 한 줄로 확인:
- (a) spec 갱신 — spec이 실험 결과와 어긋남
- (b) 새 `plan_v{N+1}_*.md` 작성 — 마지막 plan이 닫혔고 다음 실험 시작
- (c) 진행 중 plan 구현 — plan은 있고 done은 없음
- (d) `done_v{N}.md` 작성 또는 외부 리뷰 반영 수정

단위가 명확하면 confirm 후 진행. 단위 식별 자체가 모호하면 더 깊이 물어 명확히 한 뒤에야 dispatch — 잘못된 단위로 agent 부르는 건 가장 비싼 실수.

## 3. 작업

- 해당 폴더(`docs/plans/`, `docs/done/`, `src/`, ...)의 CLAUDE.md 가이드를 따른다.
- 전역 4원칙(Think Before / Simplicity / Surgical / Goal-Driven) 준수.
- Scope 밖 파일은 건드리지 않는다.

단위별 agent dispatch (`docs/CLAUDE_AGENTS.md` 매트릭스 1차 출처):
- (a) spec 갱신: 직접 작성. numbers 정합 필요 시 `general-purpose` ×1.
- (b) 새 plan: `Explore` ‖ `Plan` 항상 병렬 dispatch.
- (c) plan 구현: 직접 작성. broad lookup 필요 시 `Explore` ×1.
- (d) done: 작성 직후 `general-purpose` ×1로 numbers vs thesis self-check.
- 모든 단위 공통: PDF·대용량 로그 등 토큰 폭발 입력은 `codex:rescue`로 자동 dispatch.
- plan/done/코드 외부 검증은 사용자가 직접 `codex:rescue` 호출 (자동 X).
- dispatch 직전 한 줄 보고, 사용자 STOP 가능.

## 4. 세션 정리

- 이번에 변경한 파일·결정 사항을 plan 또는 done 파일에 한 줄로 추가.
- 다음 세션이 이 파일만 읽고도 이어받을 수 있게.

## 하지 않는 것

- 여러 step 자동 chain. 한 세션 = 한 단위. 단위 경계 넘는 dispatch 금지(plan 작성이 끝나면 자동으로 구현·done까지 가지 않는다).
- 사용자 승인 없이 git commit/push.
- 실패 시 자동 재시도. 실패 사실을 사용자에게 보고하고 결정 받기.
