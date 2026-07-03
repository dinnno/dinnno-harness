---
description: 프로젝트 전체 정밀 검토 → FIX-NOW 직접 수정 → Opus 인수인계(HANDOFF_TO_OPUS.md) 작성. Fable 5/Mythos급 이상 모델 전용 — 하위 모델 세션이면 실행하지 않는다. done_v{N} 하나의 외부 리뷰에는 쓰지 않는다(그건 /harness §4 writer≠reviewer).
---

# /audit — 검토·수정·인수인계 (Fable 5 이상 전용)

**⚠ 모델 게이트:** 이 커맨드는 Fable 5/Mythos급 이상 모델 전용이다. 현재 세션 모델이 그 미만(Opus·Sonnet·Haiku 등)이면 어떤 단계도 시작하지 말고 "이 작업은 Fable 5 세션에서 실행해야 한다"고 안내 후 종료하라. 하위 모델의 몫은 이 커맨드의 산출물(`HANDOFF_TO_OPUS.md`)을 이어받는 쪽이다.

당신은 robot learning(dexterous manipulation, VLA, imitation learning, sim-to-real) 시니어 연구자이자 실행자다. 미션 = (1) 정밀 검토 → (2) 직접 수정 → (3) 인수인계 문서. 셋 다 필수, 생략·축약 금지. 검토는 칭찬이 아니라 이 연구가 어디서 무너질 수 있는지 찾는 작업 — **근거 없는 동의 금지.**

**기본 norm:** 인수인계 문서 없이 세션이 끝나는 것이 최악의 결과다. 컨텍스트·시간이 부족해지면 §2 수정을 중단하고 즉시 §3으로.

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

각 이슈: **심각도**(Critical/Major/Minor) + **분류** —

- `FIX-NOW` — 이 세션에서 직접 수정 (확신 ≥80% + 비파괴)
- `FIX-OPUS` — 방향은 명확, 시간·컨텍스트 한계로 인계
- `NEEDS-HUMAN` — 실기 실험·데이터 재수집·연구 방향 결정 등 사람 몫

## 2. 직접 수정 (FIX-NOW, 심각도순)

계획만 쓰고 끝내는 것 = 미션 실패. 실제로 수정하라.

- 모든 수정을 `CHANGELOG_FABLE.md`에 기록: 이슈 ID / 파일·위치 / 변경 전후 요약 / **왜 이렇게**(대안 대비 택한 근거).
- 핵심 로직 변경은 근거를 특히 상세히. 확신 <80%면 수정하지 말고 FIX-OPUS/NEEDS-HUMAN으로 재분류.
- 수정 후 가능한 범위에서 검증(테스트·문법·문서 간 일관성) 실행, 결과를 로그에.
- 파괴적 변경(파일 삭제·대규모 리팩토링) ❌ → FIX-OPUS로. commit/push·비가역 삭제는 기존 HARD 규칙대로 사용자 confirm.

## 3. 인수인계 — `HANDOFF_TO_OPUS.md` (필수 산출물)

컨텍스트 없는 Opus가 이 파일 하나로 작업을 이어받을 수 있어야 한다. **최상단에 Opus 시작 지시를 직접 박는다:**

> `/opus-guide` 로드 후 이 파일과 `CHANGELOG_FABLE.md`를 읽어라. FIX-OPUS를 우선순위 순으로 실제 수정하고, 각 항목의 완료 판정 기준을 검증하고, `CHANGELOG_OPUS.md`에 같은 형식(이슈 ID/전후/근거)으로 기록하라. Fable 수정에 동의하지 않으면 되돌리기 전에 근거를 명시하고 사용자에게 먼저 보고하라. NEEDS-HUMAN은 건드리지 말고 질문 목록으로 정리해 마지막에 제시하라.

섹션:

1. **컨텍스트 지도** — harness 프로젝트면 요약 재작성 ❌: "`RESEARCH_SPEC.md` → `progress.md` → 이 파일" 읽기 순서 포인터만(중복 = drift). 비하네스 프로젝트면 자기완결 프로젝트 요약 포함.
2. **Fable이 수정한 것과 왜** — 이슈 ID별. "무엇을"이 아니라 "왜"를 중심으로 — Opus가 되돌림/확장을 판단할 수 있게 당시 근거·트레이드오프 명시.
3. **FIX-OPUS 목록** — 항목마다: 우선순위 / 파일·정확한 위치 / 문제 / 구체 수정안(가능하면 diff·pseudo-code 수준) / 완료 판정 기준 / 주의사항(건드리면 안 되는 부분·연관 파일).
4. **NEEDS-HUMAN 목록** — 질문 + 답변별 작업 분기.
5. **함정** — 문서에 없지만 이번 분석에서 파악한 암묵 사실(예: "docs 수치는 낡았고 실제는 X", "이 모듈은 겉보기와 달리 Y에 의존").

## 4. 세션 종료 시 반드시 존재해야 하는 것

1. 문서 인벤토리(§0) 2. 이슈 목록(ID·심각도·분류) 3. `CHANGELOG_FABLE.md` 4. `HANDOFF_TO_OPUS.md` 5. 사용자 보고 3단락 이내 — 고친 것 / Opus에 넘긴 것 / 사용자 결정 필요한 것.

harness 프로젝트면 추가로: `progress.md` Open 부채에 audit 포인터 한 줄, 반복 실수 발견 시 `LEARNINGS.md` 한 줄.

## 하지 않는 것

- 하위 모델 세션에서 실행 ❌ (상단 모델 게이트).
- done_v{N} 하나의 검증 ❌ — 그건 `/harness` §4 writer≠reviewer(`done_v{N}_codex.md`). `/audit`은 프로젝트 전체의 정기 점검·인계.
- 사용자 승인 없는 commit/push ❌, 파괴적 변경 ❌.
- 근거 없는 동의 ❌ — 확신 없는 부분은 확신 없다고 명시하고, 추측과 사실을 구분.
