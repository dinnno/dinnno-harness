---
description: research(논문 단위) 프로젝트 세션 진입 오리엔테이션 — 상태가 불명확할 때만 bounded Project Reconciliation 후 init/spec/experiment 또는 opt-in research-bootstrap/research-loop 단위를 confirm하고 Setup→Execute→Verdict로 진행. 일반 코딩·non-research 레포에는 쓰지 않는다.
---

이 세션은 dinnno-harness 워크플로우를 따른다. 강제 게이트가 아니라 **연구 지향 + 산출물 구조**를 주는 얇은 오리엔테이션이다. 판단은 너에게 맡긴다 — 전역 4원칙(`~/.claude/CLAUDE.md`)을 따르되 단계를 기계적으로 밟지 마라. 모델 무관 공통 경계는 아래 §경계선 — 그 밖에서는 완주가 기본이다.

**모델 self-check:** 현재 세션 모델이 Fable/Mythos 계열이 아닌데(Opus·Sonnet 등) `/opus-guide`가 아직 로드 안 됐으면 §1 적재 전에 지금 로드한다(전역 CLAUDE.md 진입점 규칙의 안전망).

**기본 norm:** 한 가설 = 한 세션 = 한 터미널. 가설 *내부*는 명확화(Setup) → 구현·학습(Execute) → 판정(Verdict)으로 자연스럽게 흐른다. 가설 *경계*는 사람이 긋는다 — **다음 가설로 자동 chain ❌** (새 가설은 새 터미널). Opt-in `/research-bootstrap`은 한 번에 독립 engineering/research task 하나, `/research-loop`는 활성 가설 하나를 각각 plan→Execute→Verdict로 완전히 닫는다. 승인 boundary·budget 안에서 **다음 단위를 고르는 주체는 상위 orchestrator**이며 `/harness` 자체는 chain하지 않는다.

## 경계선 — 멈춤은 두 모드뿐 (HARD/SOFT, 모든 모델 공통 정본)

경계에서는 멈추고, 경계 안에서는 완주한다. (2026-08-08 `/opus-guide` §1에서 이관 — 사용자용 요약은 본체 README §경계선)

- **HARD — 물어보고 대기:** ① 단위 진입 confirm(§2) ② "이 plan으로 Execute 시작?"(§3 — opt-in research-bootstrap/research-loop는 boundary·총예산 승인 1회가 그 안의 local plan Execute를 인가) ③ 가설/단위 경계 — `/harness` 내부 자동 chain ❌ (승인된 sweep/상위 loop만 다음 독립 단위 선택) ④ git commit/push ⑤ data·ckpt·runs 비가역 삭제·덮어쓰기 ⑥ 실로봇 명령 전송(sim 제외) ⑦ experiment-level 실패(발산 loss·가설 반증 결과·1회 수정 후 재실패) 후 재시도 — code-level(원인 규명된 오류, plan 불변)이라도 재실행이 비싸면(수 시간 GPU) 보고 먼저 ⑧ pay-grade — thesis/§4 축을 바꾸는 판단은 플래그 후 정지, 결정 큐 착지(§5) ⑨ (autoloop) 인가 밖 — allowlist 밖 변이·코드 변경·예산 소진 후 재개 ⑩ 상위 loop 인가 밖 — bootstrap/loop boundary 밖 surface·총예산 소진·raw fact disagreement ⑪ Loop 1↔Loop 2 transition/re-bootstrap ⑫ kill/NO-GO — 4게이트(`done/_GUIDE` §Kill/Pivot) 통과해도 사용자 전결.
- **SOFT — 한 줄 알리고 진행:** agent dispatch · 백그라운드 run 시작(메모리 상한값 동봉 — 전역 CLAUDE.md 호스트 RAM 규약) · plan §6 항목 전환 · (autoloop) trial 판정 ledger 1행.
- 그 외 Execute 안은 완주 — HARD 아닌 곳의 "계속할까요?" 금지. 과잉 confirm은 과잉 자율만큼 나쁜 실패다.
- 사용자가 문제 설명·질문 중이면(변경 요청 아님) 산출물은 진단 — 보고하고 멈춘다. 요청 없는 수정은 scope 변경(HARD).

## 1. 진입 시 적재

- `docs/RESEARCH_SPEC.md` — thesis(§1)와 비교 축(§4) 확인. 빈 슬롯/placeholder 있으면 사용자에게 경고만.
- `docs/progress.md` — 어디까지 왔는지. `docs/LEARNINGS.md` — 반복 실수 방지. 둘 중 없는 게 있으면 조용히 건너뛰지 말고 "progress/LEARNINGS 부재 → init/backfill 필요" 한 줄 경고(위 SPEC placeholder 경고와 대칭). 적재한 정본이 50K를 넘으면 1줄 경고(진입 차단 ❌) — progress·LEARNINGS는 "`/tidy` §6 다이어트 권장", SPEC은 "(a) spec 단위에서 재슬라이싱 검토 권장"(§6 불가침이라 tidy로 못 푼다).
- progress.md 하단 결정 큐 확인 — 미결 [spec-drift]·[kill-candidate]가 있으면 단위 confirm 때 (a) spec 단위를 첫 후보로 제시. 💡 인박스 항목이 현 단위와 겹치면 한 줄 언급.
- `docs/plans/`·`docs/done/`의 마지막 `v{N}` 확인 (`_template` 무시). 진행 중 단위를 이어가는 세션이면 해당 `plan_v{N}` 적재.
- `docs/notes/*research-bootstrap*.md`와 `*research-loop*.md`의 모든 non-consumed note에서 먼저 `status`·`current/in-flight`·intent/axis header를 읽는다. `active` 또는 in-flight는 stale docs와 무관하게 항상 알리고 recovery를 우선한다. 그 뒤에만 `proposed|stopped`의 현재 intent/thesis/axis 관련성을 판단해 pointer를 알린다. 같은 종류의 `active`가 둘 이상이면 실행하지 말고 하나를 남길 사용자 결정을 받는다. 일반 단위를 선택하면 기존 workflow를 그대로 따르고, 상위 loop를 재개할 때만 해당 command의 계약을 로드한다.
- `docs/references/_INDEX.md`의 `status: pending` 행 스캔 — 현재 단위와 관련 있으면 처리 규약은 §4.
- 이 커맨드가 이름으로 참조하는 섹션·파일(`done/_GUIDE` §Kill/Pivot, progress.md §결정 큐+아이디어 인박스, `docs/LOOP.md` 등)이 프로젝트에 없으면 조용히 건너뛰지 말고 신설을 제안한다.
- **하네스 싱크 (조건부)** — 루트 `CLAUDE.md`의 `last-sync:` 마커(= 마지막 반영 CHANGELOG 항목: 날짜+요지)가 가리키는 항목 **뒤에** 본체 `CHANGELOG.md` 항목이 있을 때만 발동 — append-only·날짜순이라 위치 비교로 충분(마커가 날짜뿐인 구형식이면 그 날짜 포함 이후 항목 전부 후보) (본체 루트 = `dirname`×2 of `readlink ~/.claude/commands/harness.md` — 심링크가 아니거나 결과가 현재 레포 자신이면 skip; 마커 부재·placeholder(`{설치일}` 등)면 발동). 발동 시: 미반영 항목의 계약 표면 불일치·깨진 포인터만 수술적으로 목록화(첫 싱크면 `## harness 싱크` 섹션 신설) → 항목별 적용(confirm)/보류 확정 → 어느 결말이든 `last-sync:`를 마지막 반영 항목(날짜 + 요지 몇 단어)으로 갱신, 보류분만 `- 보류: {항목} — {사유}` 한 줄. 기본 = 네이밍 매핑 한 줄, 파일 이관은 매핑이 쌓일 때만 제안. **불가침:** RESEARCH_SPEC·plans·done 본문 서술 변경 ❌ (= plan_v{N}·done_v{N} 산출물 문서 본문 — 폴더 가이드 `_GUIDE.md`·폴더 `CLAUDE.md`는 싱크 대상 ✓; 허용 범위는 형식·이름·포인터만), 대응이 불확실하면 추측 ❌ 질문 ✓ (thesis 방향 변경은 (a) spec 단위로만). 산출물 위생(날짜 suffix HANDOFF·loose md 정리)은 진입 시 스캔하지 않는다 — `/tidy` 몫.

## 1.5 Project Reconciliation — 불명확할 때만 최초 routing

Loop 0는 research loop가 아니라 “실제 현재 상태가 무엇이며 Loop 1/2 중 어디서 시작할까?”를 답하는 read-only triage다. §1에서 durable state를 신뢰할 수 있으면 실행하지 않고 바로 §2로 간다.

**우선 복구:** `proposed|active|stopped` Loop 1/2 note 또는 in-flight record가 있으면 먼저 알리고 해당 lifecycle/recovery 계약을 따른다. 명확한 active authorization은 full reconciliation과 재승인을 생략한다. Loop 0가 duplicate loop/run을 만들지 않는다.

**fast trust check:** progress의 Stage·anchored commit, latest plan/done pairing, 현재 HEAD/worktree와 anchor의 관계, active note를 싼 pointer 수준으로 대조한다. 서로 일치하고 phase가 명확하면 종료한다. 다음 중 하나면 그때만 bounded reconciliation을 수행한다: 기존 project 첫 harness 적용, canonical state 부재/placeholder, 장기 중단 재개, anchor 이후 material branch/worktree·외부 변경, docs↔code/config/run 불일치 신호, current phase/Loop 1·2 판별 불가.

전부 읽지 말고 routing에 필요한 conflict만 확장한다.

- intent/declared: RESEARCH_SPEC, progress, latest plan/done, ARCHITECTURE와 project instruction
- executable: current code entry point, configs, environment, data-generation/train/eval command·path
- evidence: latest successful runs의 machine-readable metrics, checkpoint/raw artifact pointer와 terminal evidence
- history: anchored commit 이후 git history/worktree, 관련 old plan/done/archive, LEARNINGS/issues
- memory: registered references; intent나 최근 결정 이유가 repo에 없을 때만 bounded Second Brain retrieval

큰 data/run/log 전체 scan·새 실행·engineering·canonical rewrite는 금지한다. Second Brain은 관련 state evidence만 읽고 hypothesis를 만들지 않으며 provider failure는 원문을 남기고 fail-soft. Web/deep research는 기본 금지이고 routing에 필수인 기존 reference identity/version 확인만 최소 허용한다.

대화에 compact **Current State Map**을 만든다. 각 항목은 locator+`READY|PARTIAL|MISSING|AMBIGUOUS`: research intent/question, task/environment, data path, model/training, evaluation, instrumentation, baseline, experimental evidence, provenance, open uncertainty, authorized loop/state. README·docs를 truth로 가정하지 말고 선언과 observed evidence가 다르면 `STATE CONFLICT`로 양쪽을 그대로 보여 준다. 자동으로 더 최신처럼 보이는 값을 canonical로 승격하지 않는다.

Routing recommendation은 셋뿐이다.

- `BOOTSTRAP REQUIRED → Loop 1`: meaningful baseline 부재, provisional task/data/model/eval, diagnostic/instrumentation/provenance 부족으로 controlled science 불가
- `RESEARCH READY → Loop 2`: First Meaningful Baseline 상당 evidence, interpretable evaluation/failure, 충분한 provenance와 testable uncertainty 존재
- `AMBIGUOUS → Human`: routing을 바꾸는 conflict를 evidence로 못 풀면 locator와 함께 질문 1–3개만 제시

빈 project도 같은 mechanism에서 `BOOTSTRAP REQUIRED`다. 기존 project 최초 routing과 Loop 1↔2 transition은 recommendation+근거를 보여 주고 §2에서 사용자 승인을 받는다. Loop 0 자체는 research/engineering을 시작하지 않고 기본적으로 파일도 쓰지 않는다. 결정을 미루기로 합의한 경우에만 progress 결정 큐에 `[reconcile]` source pointer 1줄을 남긴다. 승인 후 실제 state 생성·canonical 갱신은 선택된 `/research-bootstrap` 또는 `/research-loop`가 소유한다.

## 2. 이 세션이 할 일 한 줄 confirm

현황으로 다음 중 무엇인지 사용자에게 한 줄로 확인하고 진입:

- **(a₀) init** — placeholder 채우기 (`docs/_GUIDE.md` §Init protocol). 루트 `CLAUDE.md`·`ARCHITECTURE.md`의 실행 필수 context가 비었으면 여기부터. 기본 research workflow는 `RESEARCH_SPEC` thesis도 합의하지만, 명시 opt-in research-bootstrap은 아직 discovery 대상인 spec 슬롯을 `(미확정 — bootstrap)`으로 드러내고 진행할 수 있다.
- **(a) spec 갱신** — thesis/비교 축 변경. 영향이 크니 plan mode 권장.
- **(research-bootstrap)** — init/spec/reference/code discovery와 독립 `/harness` task를 잇는 optional Loop 1. 사용자가 명시 opt-in하면 `/research-bootstrap`을 로드해 engineering boundary·총예산을 승인한다. Data/model/evaluation/instrumentation은 provisional하게 공동 탐색하고, First Meaningful Baseline readiness 뒤 Loop 2 전환은 별도 HARD다. 미선택 시 기존 init/spec/experiment 흐름 변화 없음.
- **(experiment v{N})** — 새 가설 또는 진행 중 가설 이어가기.
- **(sweep)** — 사전 승인 ablation 자동 순회. 사용자가 명시 opt-in할 때만. 대상은 `progress.md` Ablation Matrix의 pending 행 중 `RESEARCH_SPEC §6`에 선언된 것만 — 이미 승인된 가설 공간이므로 행 간 자동 진행 OK(가설 경계 신설 아님). 행당 plan §3 루프 예산 준수, 결과는 Matrix 셀에 기록, experiment-level 이상 감지 시 즉시 정지·HARD 보고, 신규 가설 생성 ❌.
- **(autoloop)** — working baseline 이후 국면의 자율 탐색 루프(변이→trial→keep/rollback 반복).
  `docs/LOOP.md` 적재 → Loop-Ready(L1–L7) 진단 먼저: 미충족 있으면 이번 단위는 **loop-prep**(미충족
  L{k} 채우기), 전부 충족이면 **loop-run** — 얇은 plan(변이 우선순위·예산·정지 조건) 작성 후 "Execute
  시작?" confirm이 곧 **루프 인가**(HARD 1회), 이후 allowlist·예산 안 trial 반복은 무질문(`docs/LOOP.md
  §운영`). 루프 안 kill/NO-GO 결론 ❌(`done/_GUIDE §Kill/Pivot`). 예산 소진 후 재인가 = 새 HARD.
- **(research-loop)** — evidence acquisition→competing hypothesis→판별 experiment의 optional outer loop. 사용자가 명시 opt-in했을 때만 `/research-loop`를 로드해 boundary·총예산을 1회 승인한다. 각 iteration은 기존 plan→Execute→Verdict와 한 change axis를 그대로 유지하고, experiment-level anomaly·thesis/축·boundary 밖·예산 초과·kill은 계속 HARD. 미선택 시 기존 workflow 변화 없음.

단위가 모호하면 더 물어 명확히 한 뒤 시작. **모호한데 추측으로 밀어붙이는 게 가장 비싼 실수.** confirm 때 현재 세션 모델·effort가 §4 라우팅 권장과 어긋나면 한 줄 안내: "이 단위는 {모델·effort} 권장 — `/model`·`/effort`로 전환하거나 그대로 진행"(effort는 `echo $CLAUDE_EFFORT`로 확인, 전환 실행은 사용자 몫).

세션 중 사용자가 새 연구 아이디어를 발화하면 — 지배 서사와 모순되어도 — progress.md §결정 큐+아이디어 인박스에 💡 1줄 즉시 기록(SOFT). 기록 ≠ 채택 — 그 자리에서 평가·반박하지 않는다(사용자가 물으면 평가 OK — 전역 §1 push-back의 의도적 지역 예외). **Claude의 근거 있는 제안도 같은 채널** — "이 근거로 이렇게 해보면?"이 떠오르면 💡 `[claude]` 태그 + 근거 1줄로 착지(세션당 1~2개), 착지 ≠ 채택.

사용자가 막힘의 순환(뫼비우스 — 같은 고민·수정이 계속 돎)을 표하면 `/issue` 박제를 제안하고, 수락 시 실행한다(제안은 SOFT, 실행은 수락 후 — 규약은 그 커맨드).

사용자가 Claude의 실수를 지적하거나 재발 방지를 요구하면 — **그 턴에서 즉시** `docs/LEARNINGS.md`에 1줄 append하고 쓴 줄을 그대로 보여준다(SOFT). 세션 끝으로 미루기 ❌ — 보여주지 않았으면 쓰지 않은 것이다.

## 3. 작업 흐름 (experiment)

Setup→Execute→Verdict는 게이트가 아니라 자연스러운 진행이다.

- **Setup** — 가설 명확화. `_plan_template.md` 복사(부재 시 프로젝트 CLAUDE.md 네이밍 매핑 또는 직전 plan_v{N-1} 골격 재사용) → `plan_v{N}_*.md` 작성. plan의 절 구성이 템플릿과 다르면 커맨드의 `plan §번호` 참조는 절 **이름**(TODO·세션 로그·성공 임계값 등)으로 대응한다 — 번호는 템플릿 기준 보조 표기. 결정 무게 크면 plan mode. 끝나면 "이 plan으로 Execute 시작?" 한 번 confirm — 추천안 + **최강 대안 1개**(채택 안 한 이유 1줄)를 같이 내민다.
- **Execute** — 구현 → 학습/평가. 코드는 ponytail 사다리로 최소화(`~/.claude/skills/ponytail` — 재현성 규약(configs·seed)이 사다리보다 우위, implementer 규율과 동일). 학습이 길면 `run_in_background` + `Monitor`. plan §3에 성공 임계값·루프 예산이 있으면 그 예산 안에서 train→eval→조정(code-level만)→재실행을 무질문 반복 — "Execute 시작?" confirm이 곧 루프 인가다. plan §6 TODO 첫 미체크부터, 종료 시 체크 갱신 + §5 로그 한 줄. 단순 구현은 plan mode 불필요.
- **Verdict** — `_done_template.md` 복사(부재 시 동일 fallback) → `done_v{N}.md`. negative면 "이 가설 폐기, 새 가설은 새 터미널" 안내 후 종료. positive면 §4 다음 후보 도출(paper-impact 기준).
- **자리 비움 모드** — (sweep)·(autoloop) 진입 또는 ~30분 넘는 run 시작 시 1회 통보(질문·답 대기 ❌): "긴 run 시작 — 자리 비우실 거면 `/remote-control`로 remote 전환". opt-in돼 있으면 HARD 지점·정지 조건 도달·run 완료·이상 발생마다 PushNotification 한 줄(≤200자, actionable fact 먼저; (autoloop) trial 단위는 예외 — `LOOP.md` §운영대로 keep·이상·정지 시에만; 사용자가 터미널 주시 중이면 자동 생략됨) — 자리 비운 사용자를 침묵 속에 기다리게 하지 않는다.

**자기점검:** 각 단계 직전 한 줄 자문 — "이 작업이 `RESEARCH_SPEC §1 thesis`/§4 비교 축 또는 활성 research-bootstrap의 어느 readiness gap을 움직이나?" 답 안 나오면 단위 자체를 의심.

## 4. Agent 위임 + 모델·effort 라우팅 (강제 아님 — 필요할 때만)

**라우팅 원칙:** 모델·effort는 토큰 단가가 아니라 "단위의 오판 손실 × 빈도"로 고른다 — init/spec·thesis 수준 verdict·kill 판정 = Fable/Mythos 세션(effort xhigh, 전역 기본) · experiment Setup·Verdict = 가이드 세션(현재 세션 — Fable이든 Opus 5+`/opus-guide`든 OK, 미스매치 안내 대상 아님) · 기계적 구현 = implementer(opus·effort high) · 독립 검증·대용량 입력·깊은 web 조사 = codex:rescue(gpt-5.6-sol) · web 광역 리서치 = deep-research류 스킬(부재 머신은 general-purpose + WebSearch fan-out, 산출물 파일은 `docs/notes/`로 착지 + references 등록 또는 done §4 후보로 표면화). Opus 계열 세션·에이전트의 effort는 **high가 상한** — xhigh/max는 spec-수준 판단만(그 위로는 성능 하락 + 비용 급증). (sweep)·병렬화 가능한 Execute(다중 파일 구현·검증 fan-out)는 세션 모델 무관 **Workflow 사용을 기본 고려** — 이 커맨드 로드가 그 opt-in을 구성하며, 운영 규칙은 그때 `/workflow-ops`를 로드(lazy).

**Specialist engineering skills:** 설치된 skill은 optional tool이다. Primary agent가 현재 단위에 실질적 가치가 있을 때만 자율 선택하며, 작은 config 수정·명확한 bugfix에는 호출하지 않는다. 현재 승인 범위 안의 진단·설계·review는 그 Setup/Execute/Verdict 안에서 계속하고, 새롭거나 범위 밖 follow-up만 별도 bounded `/harness` task로 돌린다. Skill/subagent finding은 evidence가 아니라 lead이므로 원문을 재확인한다. 외부 skill은 thesis·비교 축·evaluation·Loop 전환·예산·kill/NO-GO 권한을 갖지 않는다.

- **codex:rescue** (gpt-5.6-sol) — 토큰 무거운 입력(PDF·대용량 로그·configs 다발·`libs/` 광역 scan)이나 깊은 독립 reasoning(학습 발산 진단, 예상-실제 갭, 광역 repo audit, spec↔코드 diff). 본 세션은 요약/결론만 받는다. PDF·대용량 원본을 본 세션이 직접 Read ❌.
- **Explore** — 넓은 코드 탐색(call-graph 등). grep 두어 번으로 풀릴 일엔 부르지 않는다. `graphify-out/` 그래프가 있는 repo는 Explore 전에 `/graphify query`가 먼저다(스킬·CLI 설치 머신 한정 — 미설치면 무시).
- **Plan** — 옵션 비교·ablation 우선순위 등 무게 있는 사고. 단발 판단엔 안 부른다.
- **implementer** (`model: opus`·effort high) — plan 확정 후의 기계적 구현. 가이드 세션(Fable/Opus 무관)은 설계·판정만 하고 구현은 SOFT dispatch로 내린다. 위임 후 중복 구현 ❌ — diff·결과 수치만 회수.
- **루프 도구** — (sweep)·병렬 실행에는 /loop·Workflow(worktree 격리) 활용 — 장시간 실행·스크립트 견고성 규칙은 `/workflow-ops`. 구현 스테이지 agent는 implementer 재사용, 설계·verdict 스테이지만 상위 모델(effort는 위 라우팅 상한 준수). 신규 가설 생성·가설 경계 넘기에는 ❌.
- **writer ≠ reviewer** — Verdict 자기점검(`general-purpose` ×1)과 외부 검증(`codex:rescue`, 수동)은 본 세션과 분리. 외부 검증 산출물은 별 파일(`done_v{N}_codex.md`) — 리뷰 라운드는 그 **한 파일에 이어 쓴다**, 라운드마다 새 파일 ❌ (plan 리뷰도 동일: `plan_v{N}_codex.md` 하나). 리뷰 라운드 자동 반복 ❌ — 2라운드 후에도 지적이 남으면 계속 여부를 confirm (HARD), thesis-level claim이 뒤집혔으면 즉시 1라운드 추가.
- `docs/references/`의 `status: pending`이 현재 단위와 관련 있으면 한 줄 보고 후 codex로 요약(summary) dispatch — 산출물·status 규약은 `docs/references/_GUIDE.md` 참조. 깊이 분석은 `/blueprint-ref <name>`.
- **Second brain 질의** — 가설이 정체될 때(연속 no-improve·done §4 후보 고갈·kill 후 pivot 탐색): vault(경로: 전역 CLAUDE.md, 부재 머신은 skip)로 Explore ×1 dispatch — vault 자체 CLAUDE.md 스키마의 query 절차를 따라 현 thesis·limitation에 매핑된 방법론 힌트 2-3개만 회수 → done §4 후보 또는 결정 큐 💡로 착지. 본 세션이 vault 직접 Read ❌. web 광역 탐색(deep-research 등)은 brain이 마른 뒤 2차.

- **일회성 산출물 착지** — 서베이·분석 memo 등 단위 산출물(plan/done)이 아닌 파일은 `docs/notes/YYYY-MM-DD_{slug}.md`(폴더 부재 시 생성). plans/·docs 직하 착지 ❌ — notes/는 소비 후 `/tidy`가 자유롭게 아카이브하는 방이다(`notes/_GUIDE.md`). 정규 홈이 있는 산출물은 제 경로 유지(references 요약·`blueprints/`, `/audit`의 루트 HANDOFF/CHANGELOG) — notes 대상 아님.

dispatch 직전 한 줄 보고, 사용자 STOP 가능.

## 5. 세션 정리

사용자가 "세션 close/마무리"를 선언하면 아래 정리 **전에** `/close`(fresh 서브에이전트의 목표 대비 산출물 적대 검토)를 제안하고, 수락 시 실행한다(제안은 SOFT — 규약은 그 커맨드, `/issue`와 동형).

**세션 종료 계약** (모델 무관 — 모든 세션): plan §6 체크·§5 로그 한 줄·(done 단위 후) progress.md 3종 갱신이 비어 있는 채로 종료 멘트 ❌ — "다음 세션에서" 금지, 다음 세션은 이 대화가 아니라 그 파일들만 읽는다.

**종료 보고 = verdict 1줄 + 기승전결** (모든 단위 공통. 단락당 2~4문장, 완전한 문장으로 — 화살표 체인·조각문·헤징 ❌. 문체는 전역 보고 스타일이 우위 — 비전공자가 들어도 이해되는 쉬운 말로, 각 단락 결론을 일상어로 먼저):

- **verdict 1줄** — 수치 포함("v3 유지: success 71%→84%"). 실패면 "failed" + 해당 원문 출력 인용, 미검증 "done" ❌.
- **기** — 이 세션의 단위·가설과 왜 (thesis·§4 축 또는 bootstrap readiness gap의 어디를 노렸나).
- **승** — 실제로 한 것 (파일 경로·실행·위임 회수).
- **전** — 예상과의 갭과 판정 근거.
- **결** — 다음 세션 후보 2~3개 추천 순 (done §4 표면화) — 사용자가 이 단락에서 바로 다음 세션을 고른다.

- plan 또는 done에 이번 변경/결정 한 줄.
- done/spec 단위 끝나면 `docs/progress.md` 갱신: 타임라인 행 + 헤더 anchored commit/Stage, 선언된 ablation과 대응하면 Matrix 셀. Bootstrap non-ablation task는 Matrix를 억지로 만들지 않고 Phase 0·repro/open debt를 갱신. 별도 단위 ❌ — done 산출물. (갱신 규칙은 progress.md 상단 주석 참조)
- 이번 단위에서 thesis·방법론이 **움직였으면** `RESEARCH_SPEC`의 `현재 방향 (second brain 동기용)` 블록 갱신 — 단위 종류 무관(spec·experiment Verdict·audit 확정·Execute 중 사용자 override 피벗 전부). second brain은 **이 블록만** 읽고 거기서 논문 검색 쿼리 시드가 유도된다 → 수치·경과·이력 ❌, 현재값 한 줄씩. 안 움직였으면 손대지 않는다.
- pay-grade/NEEDS-HUMAN으로 미룬 연구 결정이 있었으면 progress.md 결정 큐에 1줄 — 미룬 결정은 큐에 착지해야 미룬 것이다(허공 ❌).
- 선언된 ablation의 done에 수치가 있는데 대응 Matrix 셀이 '미측정'인 채 세션을 닫지 않는다.
- progress.md 헤더(Stage·anchored commit) 갱신 시 직전 단위는 타임라인 행으로 흡수 — 머리만 갱신하고 꼬리를 방치하지 않는다(하네스 상태 문서 정리는 Surgical 예외, 전역 CLAUDE.md §3). 루트 `HANDOFF_TO_*.md` 큐 항목을 이번 세션이 완료했으면 상태 즉시 flip.
- 반복 실수/교훈 발견 시 `docs/LEARNINGS.md`에 한 줄 직접 추가.
- 정리 임계 신호(루트 세션 산출물 ≥2 · docs 직하 loose md ≥3 · notes/에 소비 완료 후보)가 보이면 `/tidy`를 1줄 제안(SOFT — 실행은 수락 후).

## 하지 않는 것

- `/harness` 내부 자동 chain ❌ (Verdict 끝나면 현재 단위 종료. 승인된 sweep 또는 활성 research-bootstrap/research-loop orchestrator만 boundary·budget 안에서 **새 독립 단위**를 선택).
- 사용자 승인 없이 git commit/push ❌.
- 실패 시 자동 재시도 ❌ — 실패 보고 후 결정 받기 (experiment-level 기준. code-level 조정은 §3 Execute 루프 인가 안에서 OK).
