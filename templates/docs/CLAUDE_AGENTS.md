# Agent dispatch 규칙

`/harness` 진입 시 Claude Code가 단위 작업을 식별하고 그 단위에 맞는 agent를 자동 분배할 때 따르는 규칙. **dispatch는 자동, 단위 경계는 사람.** 단위가 끝나면 다음 단위로 자동 chain 금지.

`AGENTS.md`가 아니라 `CLAUDE_AGENTS.md`인 이유: 전자는 OpenAI Codex CLI가 작업 디렉토리에서 자동 로드하는 컨벤션. 이 파일은 Claude Code 전용 정책이므로 분리.

## 단위 × agent dispatch 매트릭스

| 단위 | 자동 dispatch | 무엇을 시키나 |
| --- | --- | --- |
| (a) spec 갱신 | 없음 (대부분) | — |
| (a) numbers 정합 필요 시 | `general-purpose` ×1 | spec §thesis와 done numbers·wandb run 결론 비교, 모순 나열 |
| (b) 새 plan 작성 | `Explore` ‖ `Plan` 항상 병렬 | Explore: 관련 함수·loss·call-graph + 이미 sweep된 `configs/exp_*` 위치. Plan: ablation 우선순위, 옵션 A/B 비교, configs-only vs 코드 변경 분기 |
| 새 프로젝트 첫 plan_v0 | `Explore` ×1 (의존성 그래프) | 시뮬레이터/distro, `libs/` vendored 패키지, 환경 mismatch 가능 지점 |
| (c) plan 구현 | 없음 (default) | — |
| (c) broad lookup 필요 시 | `Explore` ×1 | 함수 호출 그래프 같은 한 번짜리 broad 탐색 (grep 2회로 안 풀릴 때만) |
| (d) done 작성 | `general-purpose` ×1 (사후) | done 초안 직후, 결론과 evidence(numbers·wandb·ckpt)가 spec §thesis를 지지하는지 self-check |
| 모든 단위, 토큰 폭발 입력 등장 시 | **`codex:rescue` 자동** | PDF·대용량 로그·configs sweep dump 요약. 본 세션은 요약만 받아 통합 |
| plan/done/코드 외부 검증 | **수동** (사용자가 `codex:rescue` 호출) | 독립 LLM 비판. 산출물은 `plan_v{N}_*_codex.md`·`done_v{N}_codex.md` 별 파일 |

병렬 호출 규칙: 같은 단위 안에서만 병렬. 단위 경계 넘는 chain 금지. dispatch 직전 한 줄 보고 의무, 사용자 STOP 가능.

## Built-in agents

- **Explore** (read-only) — broad 코드 탐색, 의존성/call-graph. 코드 수정 ❌.
- **Plan** (read-only) — 옵션 비교, ablation 우선순위, configs vs 코드 분기 판단. 단발 사고에는 부르지 않음.
- **general-purpose** — multi-step 리서치, 정합성 점검. 1회 grep으로 끝날 일에는 부르지 않음.

호출 형식: `Agent(subagent_type="<name>", ...)`.

## Codex (`codex:rescue` skill) — 두 갈래

- **수동 (default)** — plan/done/코드 외부 검증은 사용자가 직접 `codex:rescue` 호출. 산출물은 `docs/plans/plan_v{N}_*_codex.md`, `docs/done/done_v{N}_codex.md` **별 파일**로 유지. 본 plan/done에는 "Codex 검토 반영: §3 ablation 추가" 한 줄로 머지.
- **자동 (Claude dispatch)** — 토큰 폭발 회피 목적에만 한정. 본 세션이 `codex:rescue`를 부르고 **요약만 받아 본 plan/done에 직접 통합** (별 파일 안 만듦). 외부 검증이 아니라 토큰 절약 도구이기 때문.

자동 dispatch 트리거 (휴리스틱):
- 확장자 `.pdf` 파일 분석 요청 (1개 이상)
- 단일 텍스트 파일 > 1MB (학습/평가 stdout, wandb run dump)
- `configs/exp_v*/*.yaml` 5개 이상 일괄 비교
- 외부 라이브러리 소스 한 묶음(`libs/` 아래 vendored 등) broad scan

위 조건 만족 시 "이 입력은 토큰 부담이 커서 `codex:rescue`로 보낼게 (요약만 받음)" 한 줄 보고 후 dispatch. 사용자 STOP 가능.

## 자주 하는 실수

- 단위 경계 넘는 chain (plan 작성 → 자동으로 구현 진입) ❌
- Explore에 코드 수정 시킴 ❌ (read-only)
- Plan을 (a)·(d) 같은 단발 사고에 부름 ❌
- 1회 grep으로 끝날 일에 agent 부름 ❌
- plan/done 외부 검증을 본 세션이 임의로 codex 호출 ❌ (사용자 호흡)
- PDF·대용량 로그를 본 세션이 그대로 Read ❌ (`codex:rescue`로 보내기)

## 이 파일을 고치는 트리거

"AI가 실수했을 때 프롬프트가 아니라 마구(harness)를 고친다."

- agent dispatch가 반복적으로 실패하거나 사용자가 같은 정정을 두 번 이상 하면 → 본 plan/done의 프롬프트가 아니라 **이 파일의 매트릭스/규칙 자체를 수정한다**.
- 수정은 README의 **월 1회 다이어트 사이클**에 묶어 한꺼번에. 단발 실패는 다음 사이클까지 메모로 둠.

## Writer ≠ Reviewer 분리

- **내부 self-check** (general-purpose ×1, (d) 단계) — 본 세션이 자기 산출물을 다른 역할로 다시 봄. 작성자와 약하게 분리된 reviewer.
- **외부 검증** (codex:rescue, 수동) — 본 세션과 완전히 분리된 reviewer. 산출물도 별 파일.

두 층 모두 "같은 사람이 쓰고 검토하지 말라" 원칙의 적용.
