---
description: research(논문 단위) 프로젝트 세션 진입 오리엔테이션 — RESEARCH_SPEC/progress/LEARNINGS 적재 후 init/spec/experiment 단위를 confirm하고 Setup→Execute→Verdict로 진행. 일반 코딩·non-research 레포에는 쓰지 않는다.
---

이 세션은 dinnno-harness 워크플로우를 따른다. 강제 게이트가 아니라 **연구 지향 + 산출물 구조**를 주는 얇은 오리엔테이션이다. 판단은 너에게 맡긴다 — 전역 4원칙(`~/.claude/CLAUDE.md`)을 따르되 단계를 기계적으로 밟지 마라.

**기본 norm:** 한 가설 = 한 세션 = 한 터미널. 가설 *내부*는 명확화(Setup) → 구현·학습(Execute) → 판정(Verdict)으로 자연스럽게 흐른다. 가설 *경계*는 사람이 긋는다 — **다음 가설로 자동 chain ❌** (새 가설은 새 터미널).

## 1. 진입 시 적재

- `docs/RESEARCH_SPEC.md` — thesis(§1)와 비교 축(§4) 확인. 빈 슬롯/placeholder 있으면 사용자에게 경고만.
- `docs/progress.md` — 어디까지 왔는지. `docs/LEARNINGS.md` — 반복 실수 방지. 둘 중 없는 게 있으면 조용히 건너뛰지 말고 "progress/LEARNINGS 부재 → init/backfill 필요" 한 줄 경고(위 SPEC placeholder 경고와 대칭).
- `docs/plans/`·`docs/done/`의 마지막 `v{N}` 확인 (`_template` 무시).

## 2. 이 세션이 할 일 한 줄 confirm

현황으로 다음 중 무엇인지 사용자에게 한 줄로 확인하고 진입:

- **(a₀) init** — placeholder 채우기 (`docs/_GUIDE.md` §Init protocol). 루트 `CLAUDE.md`·`RESEARCH_SPEC.md`·`ARCHITECTURE.md`에 `{...}` 남았거나 thesis가 `<failure>+<fix>` 형태 아니면 여기부터.
- **(a) spec 갱신** — thesis/비교 축 변경. 영향이 크니 plan mode 권장.
- **(experiment v{N})** — 새 가설 또는 진행 중 가설 이어가기.
- **(sweep)** — 사전 승인 ablation 자동 순회. 사용자가 명시 opt-in할 때만. 대상은 `progress.md` Ablation Matrix의 pending 행 중 `RESEARCH_SPEC §6`에 선언된 것만 — 이미 승인된 가설 공간이므로 행 간 자동 진행 OK(가설 경계 신설 아님). 행당 plan §3 루프 예산 준수, 결과는 Matrix 셀에 기록, experiment-level 이상 감지 시 즉시 정지·HARD 보고, 신규 가설 생성 ❌.

단위가 모호하면 더 물어 명확히 한 뒤 시작. **모호한데 추측으로 밀어붙이는 게 가장 비싼 실수.**

## 3. 작업 흐름 (experiment)

Setup→Execute→Verdict는 게이트가 아니라 자연스러운 진행이다.

- **Setup** — 가설 명확화. `_plan_template.md` 복사 → `plan_v{N}_*.md` 작성. 결정 무게 크면 plan mode. 끝나면 "이 plan으로 Execute 시작?" 한 번 confirm.
- **Execute** — 구현 → 학습/평가. 학습이 길면 `run_in_background` + `Monitor`. plan §3에 성공 임계값·루프 예산이 있으면 그 예산 안에서 train→eval→조정(code-level만)→재실행을 무질문 반복 — "Execute 시작?" confirm이 곧 루프 인가다. plan §6 TODO 첫 미체크부터, 종료 시 체크 갱신 + §5 로그 한 줄. 단순 구현은 plan mode 불필요.
- **Verdict** — `_done_template.md` 복사 → `done_v{N}.md`. negative면 "이 가설 폐기, 새 가설은 새 터미널" 안내 후 종료. positive면 §4 다음 후보 도출(paper-impact 기준).
- **자리 비움 모드** — (sweep) 진입 또는 ~30분 넘는 run 시작 시 1회 SOFT 제안: "자리 비우실 거면 remote 모드로 전환? (`/remote-control`)" opt-in 시 HARD 지점·정지 조건 도달·run 완료·이상 발생마다 PushNotification 한 줄 보고(사용자가 터미널 주시 중이면 자동 생략됨).

**자기점검:** 각 단계 직전 한 줄 자문 — "이 작업이 `RESEARCH_SPEC §1 thesis` 또는 §4 비교 축의 어디를 움직이나?" 답 안 나오면 단위 자체를 의심.

## 4. Agent 위임 (강제 아님 — 필요할 때만)

- **codex:rescue** — 토큰 무거운 입력(PDF·대용량 로그·configs 다발·`libs/` 광역 scan)이나 깊은 독립 reasoning(학습 발산 진단, 예상-실제 갭, 광역 repo audit, spec↔코드 diff). 본 세션은 요약/결론만 받는다. PDF·대용량 원본을 본 세션이 직접 Read ❌.
- **Explore** — 넓은 코드 탐색(call-graph 등). grep 두어 번으로 풀릴 일엔 부르지 않는다.
- **Plan** — 옵션 비교·ablation 우선순위 등 무게 있는 사고. 단발 판단엔 안 부른다.
- **implementer** (`model: opus`) — plan 확정 후의 기계적 구현. 가이드 세션(Fable/Opus 무관)은 설계·판정만 하고 구현은 SOFT dispatch로 내린다. 위임 후 중복 구현 ❌ — diff·결과 수치만 회수.
- **루프 도구** — (sweep)·병렬 실행에는 /loop·Workflow(worktree 격리)·Monitor 활용 가능. 구현 스테이지 agent는 model: opus(implementer 재사용), 설계·verdict 스테이지만 상위 모델. 신규 가설 생성·가설 경계 넘기에는 ❌.
- **writer ≠ reviewer** — Verdict 자기점검(`general-purpose` ×1)과 외부 검증(`codex:rescue`, 수동)은 본 세션과 분리. 외부 검증 산출물은 별 파일(`done_v{N}_codex.md`).
- `docs/references/`의 `status: pending`이 현재 단위와 관련 있으면 한 줄 보고 후 codex로 요약(summary) dispatch — 산출물·status 규약은 `docs/references/_GUIDE.md` 참조. 깊이 분석은 `/blueprint-ref <name>`.

dispatch 직전 한 줄 보고, 사용자 STOP 가능.

## 5. 세션 정리

- plan 또는 done에 이번 변경/결정 한 줄.
- done/spec 단위 끝나면 `docs/progress.md` 갱신: 타임라인 행 + Ablation 셀 + 헤더 anchored commit/Stage. 별도 단위 ❌ — done 산출물. (갱신 규칙은 progress.md 상단 주석 참조)
- 반복 실수/교훈 발견 시 `docs/LEARNINGS.md`에 한 줄 직접 추가.

## 하지 않는 것

- 가설 경계 자동 chain ❌ (Verdict 끝났다고 다음 가설로 자동 진입 안 함. 예외: opt-in된 (sweep) 단위 안의 사전 승인 행 간 진행).
- 사용자 승인 없이 git commit/push ❌.
- 실패 시 자동 재시도 ❌ — 실패 보고 후 결정 받기 (experiment-level 기준. code-level 조정은 §3 Execute 루프 인가 안에서 OK).
