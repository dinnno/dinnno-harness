---
description: research(논문 단위) 프로젝트 세션 진입 오리엔테이션 — RESEARCH_SPEC/progress/LEARNINGS 적재 후 init/spec/experiment 단위를 confirm하고 Setup→Execute→Verdict로 진행. 일반 코딩·non-research 레포에는 쓰지 않는다.
---

이 세션은 dinnno-harness 워크플로우를 따른다. 강제 게이트가 아니라 **연구 지향 + 산출물 구조**를 주는 얇은 오리엔테이션이다. 판단은 너에게 맡긴다 — 전역 4원칙(`~/.claude/CLAUDE.md`)을 따르되 단계를 기계적으로 밟지 마라.

**모델 self-check:** 현재 세션 모델이 Fable/Mythos 계열이 아닌데(Opus·Sonnet 등) `/opus-guide`가 아직 로드 안 됐으면 §1 적재 전에 지금 로드한다(전역 CLAUDE.md 진입점 규칙의 안전망).

**기본 norm:** 한 가설 = 한 세션 = 한 터미널. 가설 *내부*는 명확화(Setup) → 구현·학습(Execute) → 판정(Verdict)으로 자연스럽게 흐른다. 가설 *경계*는 사람이 긋는다 — **다음 가설로 자동 chain ❌** (새 가설은 새 터미널).

## 1. 진입 시 적재

- `docs/RESEARCH_SPEC.md` — thesis(§1)와 비교 축(§4) 확인. 빈 슬롯/placeholder 있으면 사용자에게 경고만.
- `docs/progress.md` — 어디까지 왔는지. `docs/LEARNINGS.md` — 반복 실수 방지. 둘 중 없는 게 있으면 조용히 건너뛰지 말고 "progress/LEARNINGS 부재 → init/backfill 필요" 한 줄 경고(위 SPEC placeholder 경고와 대칭).
- progress.md 하단 결정 큐 확인 — 미결 [spec-drift]·[kill-candidate]가 있으면 단위 confirm 때 (a) spec 단위를 첫 후보로 제시. 💡 인박스 항목이 현 단위와 겹치면 한 줄 언급.
- `docs/plans/`·`docs/done/`의 마지막 `v{N}` 확인 (`_template` 무시).
- **하네스 싱크 (선언 시만)** — 사용자가 "하네스 업데이트했어"라고 선언한 세션에서만, 단위 confirm 전에: 본체 `CHANGELOG.md`에서 루트 `CLAUDE.md`의 `last-sync:` 이후 항목 확인(마커 부재 시 전 항목이 후보 + `## harness 싱크` 섹션 신설) → 계약 표면 불일치·깨진 포인터만 수술적으로 맞춘다. 기본 = 네이밍 매핑 한 줄 추가, 파일 이관은 매핑이 쌓여 지저분할 때만 제안. 수정 목록 보고 → confirm 후 적용 → `last-sync:` 갱신. **불가침:** RESEARCH_SPEC·plans·done의 본문 서술 변경 ❌ (형식·이름·포인터만), 대응 관계가 불확실하면 추측 ❌ 질문 ✓ (thesis 방향 변경은 (a) spec 단위로만).

## 2. 이 세션이 할 일 한 줄 confirm

현황으로 다음 중 무엇인지 사용자에게 한 줄로 확인하고 진입:

- **(a₀) init** — placeholder 채우기 (`docs/_GUIDE.md` §Init protocol). 루트 `CLAUDE.md`·`RESEARCH_SPEC.md`·`ARCHITECTURE.md`에 `{...}` 남았거나 thesis가 `<failure>+<fix>` 형태 아니면 여기부터.
- **(a) spec 갱신** — thesis/비교 축 변경. 영향이 크니 plan mode 권장.
- **(experiment v{N})** — 새 가설 또는 진행 중 가설 이어가기.
- **(sweep)** — 사전 승인 ablation 자동 순회. 사용자가 명시 opt-in할 때만. 대상은 `progress.md` Ablation Matrix의 pending 행 중 `RESEARCH_SPEC §6`에 선언된 것만 — 이미 승인된 가설 공간이므로 행 간 자동 진행 OK(가설 경계 신설 아님). 행당 plan §3 루프 예산 준수, 결과는 Matrix 셀에 기록, experiment-level 이상 감지 시 즉시 정지·HARD 보고, 신규 가설 생성 ❌.
- **(autoloop)** — working baseline 이후 국면의 자율 탐색 루프(변이→trial→keep/rollback 반복).
  `docs/LOOP.md` 적재 → Loop-Ready(L1–L7) 진단 먼저: 미충족 있으면 이번 단위는 **loop-prep**(미충족
  L{k} 채우기), 전부 충족이면 **loop-run** — 얇은 plan(변이 우선순위·예산·정지 조건) 작성 후 "Execute
  시작?" confirm이 곧 **루프 인가**(HARD 1회), 이후 allowlist·예산 안 trial 반복은 무질문(`docs/LOOP.md
  §운영`). 루프 안 kill/NO-GO 결론 ❌(`done/_GUIDE §Kill/Pivot`). 예산 소진 후 재인가 = 새 HARD.

단위가 모호하면 더 물어 명확히 한 뒤 시작. **모호한데 추측으로 밀어붙이는 게 가장 비싼 실수.**

세션 중 사용자가 새 연구 아이디어를 발화하면 — 지배 서사와 모순되어도 — progress.md §결정 큐+아이디어 인박스에 💡 1줄 즉시 기록(SOFT). 기록 ≠ 채택 — 그 자리에서 평가·반박하지 않는다.

## 3. 작업 흐름 (experiment)

Setup→Execute→Verdict는 게이트가 아니라 자연스러운 진행이다.

- **Setup** — 가설 명확화. `_plan_template.md` 복사 → `plan_v{N}_*.md` 작성. 결정 무게 크면 plan mode. 끝나면 "이 plan으로 Execute 시작?" 한 번 confirm.
- **Execute** — 구현 → 학습/평가. 학습이 길면 `run_in_background` + `Monitor`. plan §3에 성공 임계값·루프 예산이 있으면 그 예산 안에서 train→eval→조정(code-level만)→재실행을 무질문 반복 — "Execute 시작?" confirm이 곧 루프 인가다. plan §6 TODO 첫 미체크부터, 종료 시 체크 갱신 + §5 로그 한 줄. 단순 구현은 plan mode 불필요.
- **Verdict** — `_done_template.md` 복사 → `done_v{N}.md`. negative면 "이 가설 폐기, 새 가설은 새 터미널" 안내 후 종료. positive면 §4 다음 후보 도출(paper-impact 기준).
- **자리 비움 모드** — (sweep)·(autoloop) 진입 또는 ~30분 넘는 run 시작 시 1회 SOFT 제안: "자리 비우실 거면 remote 모드로 전환? (`/remote-control`)" opt-in 시 HARD 지점·정지 조건 도달·run 완료·이상 발생마다 PushNotification 한 줄 보고(사용자가 터미널 주시 중이면 자동 생략됨).

**자기점검:** 각 단계 직전 한 줄 자문 — "이 작업이 `RESEARCH_SPEC §1 thesis` 또는 §4 비교 축의 어디를 움직이나?" 답 안 나오면 단위 자체를 의심.

## 4. Agent 위임 (강제 아님 — 필요할 때만)

- **codex:rescue** — 토큰 무거운 입력(PDF·대용량 로그·configs 다발·`libs/` 광역 scan)이나 깊은 독립 reasoning(학습 발산 진단, 예상-실제 갭, 광역 repo audit, spec↔코드 diff). 본 세션은 요약/결론만 받는다. PDF·대용량 원본을 본 세션이 직접 Read ❌.
- **Explore** — 넓은 코드 탐색(call-graph 등). grep 두어 번으로 풀릴 일엔 부르지 않는다.
- **Plan** — 옵션 비교·ablation 우선순위 등 무게 있는 사고. 단발 판단엔 안 부른다.
- **implementer** (`model: opus`) — plan 확정 후의 기계적 구현. 가이드 세션(Fable/Opus 무관)은 설계·판정만 하고 구현은 SOFT dispatch로 내린다. 위임 후 중복 구현 ❌ — diff·결과 수치만 회수.
- **루프 도구** — (sweep)·병렬 실행에는 /loop·Workflow(worktree 격리)·Monitor 활용 가능. 구현 스테이지 agent는 model: opus(implementer 재사용), 설계·verdict 스테이지만 상위 모델. 신규 가설 생성·가설 경계 넘기에는 ❌.
- **writer ≠ reviewer** — Verdict 자기점검(`general-purpose` ×1)과 외부 검증(`codex:rescue`, 수동)은 본 세션과 분리. 외부 검증 산출물은 별 파일(`done_v{N}_codex.md`).
- `docs/references/`의 `status: pending`이 현재 단위와 관련 있으면 한 줄 보고 후 codex로 요약(summary) dispatch — 산출물·status 규약은 `docs/references/_GUIDE.md` 참조. 깊이 분석은 `/blueprint-ref <name>`.
- **Second brain 질의** — 가설이 정체될 때(연속 no-improve·done §4 후보 고갈·kill 후 pivot 탐색): vault(경로: 전역 CLAUDE.md, 부재 머신은 skip)로 Explore ×1 dispatch — vault 자체 CLAUDE.md 스키마의 query 절차를 따라 현 thesis·limitation에 매핑된 방법론 힌트 2-3개만 회수 → done §4 후보 또는 결정 큐 💡로 착지. 본 세션이 vault 직접 Read ❌. web 광역 탐색(deep-research 등)은 brain이 마른 뒤 2차.

dispatch 직전 한 줄 보고, 사용자 STOP 가능.

## 5. 세션 정리

- plan 또는 done에 이번 변경/결정 한 줄.
- done/spec 단위 끝나면 `docs/progress.md` 갱신: 타임라인 행 + Ablation 셀 + 헤더 anchored commit/Stage. 별도 단위 ❌ — done 산출물. (갱신 규칙은 progress.md 상단 주석 참조)
- pay-grade/NEEDS-HUMAN으로 미룬 연구 결정이 있었으면 progress.md 결정 큐에 1줄 — 미룬 결정은 큐에 착지해야 미룬 것이다(허공 ❌).
- done에 수치가 있는데 대응 Ablation 셀이 '미측정'인 채 세션을 닫지 않는다.
- 반복 실수/교훈 발견 시 `docs/LEARNINGS.md`에 한 줄 직접 추가.

## 하지 않는 것

- 가설 경계 자동 chain ❌ (Verdict 끝났다고 다음 가설로 자동 진입 안 함. 예외: opt-in된 (sweep) 단위 안의 사전 승인 행 간 진행).
- 사용자 승인 없이 git commit/push ❌.
- 실패 시 자동 재시도 ❌ — 실패 보고 후 결정 받기 (experiment-level 기준. code-level 조정은 §3 Execute 루프 인가 안에서 OK).
