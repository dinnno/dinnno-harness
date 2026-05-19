이 세션은 dinnno-harness 워크플로우를 따른다. 작업의 최소 단위는 산출물 한 묶음 (spec 갱신 / 새 plan / plan 구현 / done 작성 중 하나). 기본은 한 세션 = 한 단위지만, 단위가 짧게 끝났고 사용자가 다음 단위로 명시적으로 GO 하면 같은 세션에서 이어서 한다. context 남은 토큰을 핑계로 자르지도, 자동 chain 하지도 않는다.

## 1. 현황 파악

- `docs/CLAUDE_AGENTS.md` 먼저 읽어 agent dispatch 매트릭스를 적재한다.
- `docs/RESEARCH_SPEC.md` 읽고 thesis와 비교 축 확인.
- **(a₀) init 트리거**: 프로젝트 루트 `CLAUDE.md`, `docs/RESEARCH_SPEC.md`, `docs/ARCHITECTURE.md` 중 `{...}` placeholder가 남아있거나 RESEARCH_SPEC §1 thesis가 "<failure mechanism> + <principled fix>" 형태가 아니면 (a₀) init 단위 진입. `docs/_GUIDE.md` §"Init (a₀) protocol" 따름.
- `docs/plans/` 안의 마지막 `plan_v{N}_*.md` 확인 (밑줄 시작 `_plan_template.md`는 무시).
- `docs/done/` 안의 마지막 `done_v{N}.md` 확인 (밑줄 시작 무시).
- `docs/references/_INDEX.md`의 `status: pending` 행이 있고 **현재 단위와 관련 있어 보이면** 사용자에게 한 줄 보고 후 `codex:rescue`로 분석 dispatch. summary가 생기면 메인 세션은 summary만 적재.
- 새 프로젝트거나 코드 베이스 첫 접촉이면 `Explore` 1개 자동 dispatch — `docs/CLAUDE_AGENTS.md` 매트릭스 "새 프로젝트 첫 plan_v0" 행.

## 2. 이 세션이 할 일 판단

위 현황 기준으로 다음 중 무엇인지 사용자에게 한 줄로 확인:
- (a₀) **init** — placeholder 박힌 메타 .md를 사용자와 함께 채우기 (프로젝트 루트 CLAUDE → ARCHITECTURE → RESEARCH_SPEC → progress → references 순서)
- (a) spec 갱신 — spec이 실험 결과와 어긋남
- (b) 새 `plan_v{N+1}_*.md` 작성 — 마지막 plan이 닫혔고 다음 실험 시작
- (c) 진행 중 plan 구현 — plan은 있고 done은 없음
- (d) `done_v{N}.md` 작성 또는 외부 리뷰 반영 수정

단위가 명확하면 confirm 후 진행. 단위 식별 자체가 모호하면 더 깊이 물어 명확히 한 뒤에야 dispatch — 잘못된 단위로 agent 부르는 건 가장 비싼 실수.

### 권장 진입
- (a₀) init: `docs/_GUIDE.md` §"Init (a₀) protocol" 따름. 5단계 모두 사용자 발화 기반 (≥3 round per 단계 1-3, 추측 박치기 reject).
- (a) spec 갱신: 단순 수치/문구 수정은 직행. 비교 축/thesis 손대거나 **새 spec 초안 작성**이면 plan mode 후 `docs/_GUIDE.md` §"RESEARCH_SPEC 작성/갱신 protocol"을 따른다 (사용자와 ≥3 round 인터뷰, 추측 기반 요약 박치기 reject).
- (b) 새 plan: plan mode로 설계 논의 → 합의 후 §3에서 `plan_v{N+1}_*.md` 작성. `_plan_template.md` 복사로 시작.
- (c) plan 구현: 직행. plan과 어긋나는 결정 필요해지면 그때 plan mode.
- (d) done 작성: 직행. `_done_template.md` 복사로 시작.

## 3. 작업

- 해당 폴더(`docs/`, `docs/plans/`, `docs/done/`, `docs/references/`, ...)의 `_GUIDE.md`를 따른다 (`src/` 등 코드 폴더는 기존 `CLAUDE.md` 또는 README 따름).
- **목표 지향 자기점검:** 작업 시작 전 한 줄로 자문 → "이 단위가 `RESEARCH_SPEC.md §1 thesis` 또는 §4 비교 축의 어디를 움직이나?" 답이 안 나오면 단위 자체를 의심하고 사용자에게 보고.
- **(c) plan 구현 단위 진입 시**: plan §6 TODO 적재 → 첫 미체크 항목부터 시작 (사용자가 다른 항목 지정하면 그것 우선). 세션 종료 시 §6 체크 갱신 + §5 세션 로그 한 줄 추가.
- 전역 4원칙(Think Before / Simplicity / Surgical / Goal-Driven) 준수.
- Scope 밖 파일은 건드리지 않는다.

단위별 agent dispatch는 `docs/CLAUDE_AGENTS.md` 매트릭스 따름. 공통: dispatch 직전 한 줄 보고, 사용자 STOP 가능.

## 4. 세션 정리

- 이번에 변경한 파일·결정 사항을 plan 또는 done 파일에 한 줄로 추가.
- 다음 세션이 이 파일만 읽고도 이어받을 수 있게.

## 하지 않는 것

- **자동** chain 금지: 한 단위 끝났을 때 사용자 확인 없이 다음 단위로 진입하지 않는다. plan 작성이 끝나면 "이 plan 바로 구현 시작할까, 아니면 끊을까?"를 한 줄로 묻고 응답을 기다린다.
- 사용자가 "그대로 구현 가" / "다음 단위 ㄱ" 등 명시적 GO를 주면 같은 세션에서 다음 단위 진입 OK. 진입 직전 새 단위의 §2 확인 한 줄 다시 보고.
- 사용자 승인 없이 git commit/push.
- 실패 시 자동 재시도. 실패 사실을 사용자에게 보고하고 결정 받기.
