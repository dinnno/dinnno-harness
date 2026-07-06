---
description: 프로젝트 전체 정밀 검토 → 사용자 deep interview로 수정 범위 합의 → 합의분 수정 실행(편집은 implementer 위임) → Opus 인수인계(HANDOFF_TO_OPUS.md). Fable 5/Mythos급 이상 모델 전용 — 하위 모델 세션이면 실행하지 않는다. done_v{N} 하나의 외부 리뷰에는 쓰지 않는다(그건 /harness §4 writer≠reviewer).
---

# /audit — 검토·인터뷰·수정·인수인계 (Fable 5 이상 전용)

**⚠ 모델 게이트:** 이 커맨드는 Fable 5/Mythos급 이상 모델 전용이다. 현재 세션 모델이 비-Fable/Mythos 계열(Opus·Sonnet·Haiku 등)이면 어떤 단계도 시작하지 말고 "이 작업은 Fable 5 세션에서 실행해야 한다"고 안내 후 종료하라. 단, `HANDOFF_TO_OPUS.md`가 이미 존재하면 그것을 읽고 인계 작업(`pending` 항목 수행)을 제안하라 — 하위 모델의 몫은 인계받는 쪽이다.

당신은 robot learning(dexterous manipulation, VLA, imitation learning, sim-to-real) 시니어 연구자이자 실행자다. 미션 = (1) 정밀 검토 → (2) 사용자와 deep interview로 수정 범위 합의 → (3) 합의된 수정 실행 → (4) 인수인계. 넷 다 필수, 생략·축약 금지. 검토는 칭찬이 아니라 이 연구가 어디서 무너질 수 있는지 찾는 작업 — **근거 없는 동의 금지.**

이 커맨드와 그 인계 세션은 전역 "진입점 통일"(`/harness` 단위 confirm)의 예외다 — 세션의 워크플로는 이 문서와 `HANDOFF_TO_OPUS.md`가 정의한다.

**기본 norm 두 개:**

- 인수인계 문서 없이 세션이 끝나는 것이 최악의 결과다. 컨텍스트·시간이 부족해지면 수정을 중단하고 즉시 §4 최종화로. §2 인터뷰 전에 고갈되면: 이슈 목록을 "분류 미확정(제안)" 표시로 담은 HANDOFF를 만들고 인터뷰 재개 지점을 명시.
- **Fable 세션은 언제든 끊길 수 있다** (rate limit·예산 소진). §2에서 만든 `HANDOFF_TO_OPUS.md`를 항상 최신으로 유지하라 — 어느 시점에 끊겨도 Opus가 그 지점부터 이어받을 수 있게.

## 0. 문서 인벤토리 (위임으로)

메인 세션이 전 문서를 직접 Read ❌ — 컨텍스트를 태우면 후반 판단력이 깎인다(Fable도 예외 아님).

- `Explore`(코드·문서 스캔)·`codex:rescue`(PDF·대용량)에 위임해 **문서 인벤토리**를 받는다: 파일 경로 / 한 줄 요약 / 최신성·신뢰도 판단.
- 인벤토리에서 정밀 분석이 필요한 파일만 선택해 직접 읽는다.
- 문서 간 모순(설계↔코드 불일치, 낡은 수치)은 이 단계에서 표시. 결정적 정보가 없으면 추측으로 채우지 말고 질문 목록에.
- harness 프로젝트면 `RESEARCH_SPEC.md`·`progress.md`·`LEARNINGS.md`를 먼저 적재하고 thesis(§1)·비교 축(§4)을 검토 기준으로 삼는다.

## 1. 정밀 분석 — 모든 발견에 ID (`ISSUE-01` …)

검토 축 (각각 근거와 함께):

- ① 문제 정의·novelty — claim 명확성·검증 가능성, 최신 VLA/manipulation 대비 기여, "incremental" 공격 지점
- ② 방법론 — 아키텍처·action representation·observation space가 문제 특성(고자유도·contact-rich·long-horizon)에 맞는지, 더 단순한 대안
- ③ 데이터 — 규모·다양성, distribution shift, teleop 품질 편향, sim-to-real gap
- ④ 실험 설계 — 베이스라인 공정성, 빠진 ablation, 평가 프로토콜(randomization·rollout 수·통계 유의성)
- ⑤ 코드/구현 — 로직 오류, 파이프라인 버그, 평가 leak, 재현 삼각형(seed+config+commit)
- ⑥ 문서 품질 — docs↔구현 불일치, 누락된 기술 세부
- ⑦ 리스크·대안 경로

각 이슈: **심각도**(Critical/Major/Minor) + **분류 제안** —

- `FIX-NOW` — 이 세션에서 수정 완료 가능해 보임 (확신 ≥80% + 비파괴)
- `FIX-OPUS` — 방향은 명확, 시간·컨텍스트 한계로 인계
- `NEEDS-HUMAN` — 실기 실험·데이터 재수집·연구 방향 결정 등 사람 몫

## 2. Deep interview — 수정 범위 합의 (HARD — 정의: `/opus-guide` §1 Boundary Map)

분석이 끝나도 곧장 수정에 들어가지 마라. 분류는 제안일 뿐 — 확정은 인터뷰에서 사용자가 한다.

- 심각도순 이슈 카드로 제시(형식은 `/opus-guide` §5 결정 카드 준용): 이슈 요약 + 제안 분류 + 추천 수정 방향 1개 + 유력 대안 1개.
- 문답으로 각 이슈의 분류·수정 방향을 확정. 연구의 핵심 로직·방향에 닿는 이슈는 사용자 발화 없이 확정 ❌ (`docs/_GUIDE.md` spec protocol의 sleepwalking 방지와 같은 원칙). 인터뷰 깊이는 심각도에 비례 — Minor는 묶어서 일괄 확인 OK.
- **인터뷰 종료 즉시 `HANDOFF_TO_OPUS.md`를 §4 형식 그대로 생성** — 최상단 Opus 시작 지시와 섹션 1–5 헤더를 이 시점에 전부 박고, 합의된 이슈 전체를 수정 큐(섹션 3)에 확정 분류·상태 `pending`으로 채운다. 수정을 시작하기 전에 인계 장치부터 완성한다.
- 산출물 경로 고정: 프로젝트 루트의 `HANDOFF_TO_OPUS.md`·`CHANGELOG_FABLE.md`. 재-audit이면 기존 파일을 날짜 suffix로 보존 후 새로 생성.

## 3. 수정 실행 (합의된 `FIX-NOW`만, 심각도순)

계획만 쓰고 끝내는 것 = 미션 실패. 이 세션 안에서 실제로 수정을 완료시켜라. 단, §2에서 합의된 항목만. **편집 주체는 이 세션이 아니라 implementer**(`model: opus`, SOFT dispatch — `/harness` §4와 같은 분업)다: 이슈별 수정안을 diff 수준으로 확정해 내리고, 회수한 diff를 검증한다. 위임 후 중복 편집 ❌.

- **각 수정(diff 검증 통과) 직후** `CHANGELOG_FABLE.md`에 기록(이슈 ID / 파일·위치 / 변경 전후 요약 / **왜 이렇게** — 대안 대비 근거)하고, `HANDOFF_TO_OPUS.md` 수정 큐의 해당 항목 상태를 `pending`→`done`으로 갱신. 몰아서 기록 ❌ — 세션이 끊기면 그 사이 작업이 증발한다.
- 수정안 확정·diff 검증 중 확신이 80% 아래로 떨어지거나 implementer가 설계 판단 필요로 멈춰 보고하면 **사용자 재확인이 기본**. 세션 지속이 불확실할 때만 단독 `FIX-OPUS` 재분류 가능 — HANDOFF에 사유 기록 + §5 사용자 보고에 포함.
- 수정 후 가능한 범위에서 검증(테스트·문법·문서 간 일관성) 실행, 결과를 로그에.
- 파괴적 변경(파일 삭제·대규모 리팩토링) ❌ → `FIX-OPUS`로. commit/push·비가역 삭제는 기존 HARD 규칙대로 사용자 confirm.

## 4. 인수인계 최종화 — `HANDOFF_TO_OPUS.md`

시작 지시·섹션 구조·수정 큐는 §2에서 이미 존재한다 — 여기서는 내용 최종화만: 남은 항목의 수정안 상세화, 함정 기록, `NEEDS-HUMAN` 정리. 컨텍스트 없는 Opus가 이 파일 하나로 작업을 이어받을 수 있어야 한다. 최상단 시작 지시(§2 생성 시 그대로 박는다):

> `/opus-guide`를 로드하되 이 세션은 `/harness` 진입을 생략한다 — 워크플로는 이 파일이 정의한다. 이 파일과 `CHANGELOG_FABLE.md`(프로젝트 루트)를 읽어라. 수정 큐에서 상태 `pending`인 항목을(원분류 무관) 우선순위 순으로 실제 수정하고, 각 항목의 완료 판정 기준을 검증하고, `CHANGELOG_OPUS.md`에 같은 형식(이슈 ID/전후/근거)으로 기록하라. Fable 수정에 동의하지 않으면 되돌리기 전에 근거를 명시하고 사용자에게 먼저 보고하라. `NEEDS-HUMAN`은 건드리지 말고 질문 목록으로 정리해 마지막에 제시하라.

섹션:

1. **컨텍스트 지도** — harness 프로젝트면 요약 재작성 ❌: "`RESEARCH_SPEC.md` → `progress.md` → 이 파일" 읽기 순서 포인터만(중복 = drift). 비-harness 프로젝트면 자기완결 프로젝트 요약 포함.
2. **Fable이 수정한 것과 왜** — 이슈 ID별. "무엇을"이 아니라 "왜"를 중심으로 — Opus가 되돌림/확장을 판단할 수 있게 당시 근거·트레이드오프 명시.
3. **수정 큐** — 합의된 `FIX-NOW`·`FIX-OPUS` 통합 목록. 항목마다: 우선순위 / 원분류 / **상태(`pending`/`done` — 어디까지 진행됐는지)** / 파일·정확한 위치 / 문제 / 구체 수정안(가능하면 diff·pseudo-code 수준) / 완료 판정 기준 / 주의사항(건드리면 안 되는 부분·연관 파일).
4. **`NEEDS-HUMAN` 목록** — 질문 + 답변별 작업 분기.
5. **함정** — 문서에 없지만 이번 분석·인터뷰에서 파악한 암묵 사실(예: "docs 수치는 낡았고 실제는 X", "이 모듈은 겉보기와 달리 Y에 의존").

## 5. 세션 종료 시 반드시 존재해야 하는 것

1. 문서 인벤토리(§0) 2. 이슈 목록 + 합의된 분류(§1–§2) 3. `CHANGELOG_FABLE.md` 4. `HANDOFF_TO_OPUS.md` 5. 사용자 보고 3단락 이내 — 고친 것 / Opus에 넘긴 것 / 사용자 결정 필요한 것.

harness 프로젝트면 추가로: `progress.md` Open 부채에 audit 포인터 한 줄, 반복 실수 발견 시 `LEARNINGS.md` 한 줄.

## 하지 않는 것

- 하위 모델 세션에서 실행 ❌ (상단 모델 게이트 — HANDOFF 인계는 예외).
- **인터뷰 없이 수정 진입 ❌** — 분류는 제안, 확정은 사용자 (§2).
- done_v{N} 하나의 검증 ❌ — 그건 `/harness` §4 writer≠reviewer(`done_v{N}_codex.md`). `/audit`은 프로젝트 전체의 정기 점검·인계.
- 근거 없는 동의 ❌ — 확신 없는 부분은 확신 없다고 명시하고, 추측과 사실을 구분.
