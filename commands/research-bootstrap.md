---
description: optional Research Bootstrap outer loop — 기존 init/spec/reference/code discovery와 독립 /harness plan→Execute→Verdict task를 연결해 data↔model↔evaluation↔instrumentation을 공동 탐색하고 First Meaningful Baseline까지 만든다.
---

# /research-bootstrap — intent → observable research system

이 커맨드는 기존 `/harness` 위의 **선택형 Loop 1 orchestrator**다. 질문은 “이 연구를 실제로 측정하고 반복 개선할 수 있는 시스템으로 어떻게 만들 것인가?”다. init, spec, references, plans/done, progress, implementer, `/workflow-ops`를 대체하지 않는다. 사용자가 `(research-bootstrap)`를 명시적으로 선택하지 않으면 기존 workflow는 변하지 않는다.

Loop 1은 system discovery다. task·data·model·evaluation·instrumentation이 함께 바뀔 수 있으며, Loop 2의 one-hypothesis·one-change-axis·confirmatory 규율을 모든 탐색 행동에 강제하지 않는다. 대신 provenance, raw evidence, compute budget, destructive/real-robot gate와 연구 방향의 사람 소유는 그대로다.

## 0. Authorization과 durable state (HARD 1회)

먼저 `/harness` §1을 적재한다. 안전한 실행에 필요한 domain/repository/command context placeholder는 기존 `(a₀) init`으로 채운다. 반면 thesis·failure taxonomy·data/model/eval이 아직 discovery 대상이면 억지로 확정하지 말고 `RESEARCH_SPEC §0`에 provisional intent, 해당 슬롯에 `(미확정 — bootstrap)`을 명시한 채 시작한다. Evidence로 상위 방향을 확정하거나 바꿀 때만 기존 `(a) spec`과 human gate를 사용한다. `docs/notes/*research-bootstrap*.md`의 non-consumed note를 찾아 같은 intent의 note를 재사용하고, 동시에 `active`는 하나만 허용한다.

새 bootstrap이면 `docs/notes/YYYY-MM-DD_research-bootstrap-{slug}.md` 하나만 만든다. 상세 결과는 plan/done/run에 두고 여기에는 현재 선택과 pointer만 둔다.

```markdown
# research-bootstrap: {intent}
- bootstrap-id: {YYYYMMDD-{slug}}
- status: proposed | active | stopped | consumed
- boundary: {research intent, 허용 repo/task/env 범위}
- budget: {max tasks, GPU h, per-run cap, external-research cap}
- approved: {YYYY-MM-DD 사용자 승인 원문 또는 pending}
- transition: {pending | GO TO LOOP 2 | CONTINUE BOOTSTRAP | REDIRECT, 날짜·사용자 결정}
- current task: {idle | plan/done pointer | in-flight locator}
- provisional co-design: {task | data | model | evaluation | instrumentation pointer/1줄}
- readiness: not-reviewed | READY | READY WITH RISKS | NOT READY
- open gap: {가장 큰 bootstrap uncertainty 1줄}

| k | bootstrap question | plan | done/evidence | observed gap | next/gate | budget used |
|---|---|---|---|---|---|---|
```

상태는 `/research-loop`와 같은 최소 lifecycle을 쓴다: `proposed`는 승인/폐기만, `active`는 실행/정지/완료, `stopped`는 재승인/폐기만, `consumed`는 terminal history다. `approved: pending`인 note는 실행할 수 없다. 기록된 승인 한 번은 boundary·budget 안에서 다음 **독립 bootstrap task를 선택하고 Execute**하는 권한이다. 각 task는 완전히 닫힌 뒤 다음 task로 넘어간다. 장시간 run은 기존 `/workflow-ops`와 `/research-loop`의 durable in-flight locator·marker-first recovery 규율을 그대로 재사용한다.

## 1. FORMULATE + ACQUIRE CONTEXT

Research Intent를 현재 검증 가능한 working question으로 좁히되, 초기 선택을 immutable하게 만들지 않는다. 먼저 현재 project의 다음 evidence를 필요한 만큼 읽는다.

- init 결과와 `RESEARCH_SPEC`, `ARCHITECTURE`, progress/LEARNINGS
- 실제 repository/code path, runnable command, existing data/config/run
- 등록된 references의 summary/blueprint와 관련 benchmark·public implementation
- 과거 baseline/done이 있으면 raw result와 failure

### Second Brain

현재 bootstrap question에 관련된 근거만 bounded retrieval한다. Provider discovery, `read_only_query`, provenance/depth 보존, `--limit 8 --max-chars 12000`, empty면 동의어로 한 번 확장, nonzero/malformed면 원문 기록 후 계속하는 규율은 `/research-loop` §2 B를 재사용한다. Vault dump·project task 중 write-back은 금지한다.

Query는 현재 gap에 맞춘다. 예: evaluation/benchmark/failure, dataset/simulation/supervision, model intuition, simulator caveat, 버린 접근, 과거 practical lesson. Shallow evidence는 후보를 만들 수 있지만 강한 설계 근거로 확정하지 않는다.

### External research / benchmark discovery (조건부)

다음 knowledge gap에서만 literature, benchmark, dataset, public implementation을 조사한다.

- 재사용할 environment/evaluation 존재 여부가 불명확
- data/model/eval prior art가 설계를 materially 바꿈
- benchmark validity 또는 sim↔real 의미가 불명확
- 이미 해결된 engineering problem일 가능성
- Second Brain이 empty/error/shallow-only
- prototype failure를 local evidence만으로 해석하기 어려움

Source는 기존 `/add-ref`로 등록하고, 구현 대상으로 정한 것만 `/blueprint-ref`로 승격한다. Search 여부와 얻을 information을 bootstrap decision으로 ledger에 남긴다.

External research tool/provider가 unavailable/error/timeout이면 원문을 ledger에 남기고 source를 꾸며내거나 자동 retry하지 않는다. Source validation이 안전상 필수인 경우는 HARD, 그 외에는 confidence를 낮춰 local/Second Brain evidence로 계속하고 readiness risk에 남긴다.

## 2. CO-DESIGN — Task ↔ Data ↔ Model ↔ Evaluation ↔ Instrumentation

다섯 요소를 순차 checklist가 아니라 서로 제약하는 working system으로 다룬다.

- Task/environment: 어떤 robot behavior와 operating condition을 연구하는가?
- Data: 필요한 supervision·coverage가 sim/real에서 생성·획득 가능한가? distribution이 claim과 맞는가?
- Model/system: data와 runtime이 감당하는 가장 단순한 baseline은 무엇인가?
- Evaluation: metric·qualitative evidence가 관심 behavior를 실제로 반영하는가?
- Instrumentation: 성공/실패 원인을 분해할 rollout, stage, collision/contact, state/action, timing 로그·시각화가 있는가?

Working choice는 provisional이다. 한 prototype의 결과가 가정을 깨면 task/data/model/evaluation/instrumentation 중 필요한 여러 항목을 함께 고쳐도 된다. 선택 이유·대안·raw observation만 남기고 조기 freeze하지 않는다.

### Evaluation discovery ladder

고정 metric list를 만들지 않는다. Agent가 task semantics, rollout, logs, references와 memory를 보고 필요한 metric·instrumentation을 제안하고 싸게 prototype한다.

1. **Sanity** — 시스템이 작동하는가? catastrophic failure와 obvious behavior를 볼 수 있는가?
2. **Diagnostic** — 왜 성공/실패하는가? task에 맞는 stage/failure/trajectory observation을 발견한다.
3. **Research** — competing explanation이나 이후 방법을 비교할 primary/secondary evidence가 생겼는가?

처음부터 publication-ready metric을 요구하지 않는다. 다만 metric이 behavior와 어긋난 evidence를 무시한 채 다음 단계로 승격하지 않는다.

## 3. ENGINEERING WILD ZONE → 독립 `/harness` task

Bootstrap 안에서는 적극 탐색한다: throwaway prototype, temporary analysis/visualization, simulator instrumentation, dataset inspection, debug tool, baseline, alternative metric, repository exploration, genuinely needed refactor, cheap diagnostic run을 허용한다. 모든 행동을 미리 checklist로 고정하지 않는다.

Orchestrator는 현재 information gain이 가장 큰 bootstrap question 하나를 고르고 새 `/harness` task로 보낸다. Task는 hypothesis experiment일 필요가 없다. 예: dataset generator prototype, evaluation instrumentation, rollout visualization, benchmark integration, candidate metric 비교, baseline implementation.

첫 minimal baseline은 기존 `plan_v0_naive`와 progress Phase 0을 사용한다. 이미 v0가 있으면 덮어쓰지 않고 그 done/evidence를 출발점으로 다음 번호의 bootstrap task를 만든다.

기존 plan→Execute→Verdict를 그대로 쓴다.

- plan §1: 관련 spec limitation이 있으면 인용; 없으면 `N/A — bootstrap system-discovery task`와 현재 gap/evidence
- plan §2: 이번 task가 만드는 최소 prototype/instrumentation/diagnostic
- plan §3: expected artifact·관찰 가능한 신호·실행 command·budget·stop·provenance
- plan §4: 결과에 따라 어떤 co-design 항목을 재검토할지
- done: 실제 diff/command/raw evidence, 예상–실제 gap, 다음 bootstrap question 후보

각 task 종료 후 plan/done/progress/LEARNINGS를 기존 `/harness`대로 닫고 runtime ledger 한 행을 append한다. 결과가 예상과 달라도 실행·측정이 유효하면 bootstrap discovery이지 hypothesis failure가 아니다. Invalid run, budget 초과, destructive/real-robot, boundary 밖 방향 변경만 기존 HARD로 멈춘다.

## 4. OBSERVE — baseline maturity

Baseline을 다음처럼 구분한다.

- **Runnable**: environment, data path, train/infer, rollout/eval command가 실제 실행됨
- **Evaluable**: quantitative/qualitative evidence가 나오고 run 비교와 failure 관찰이 가능함
- **Meaningful**: 관심 behavior를 일부 포착하고 dominant failure/uncertainty를 관찰하며 다음 controlled experiment를 설계할 signal과 raw provenance가 있음

Runnable 또는 Evaluable에서 멈추면 readiness가 아니다. 관찰이 부족하면 가장 싼 instrumentation/evaluation/data/model/task revision을 다음 독립 task로 선택한다. Exit target은 perfect baseline이 아니라 **First Meaningful Baseline**이다.

## 5. Bootstrap Readiness Review

First Meaningful Baseline 후보가 생기면 대화를 모르는 fresh read-only reviewer에게 intent, canonical docs, paired baseline plan/done, raw evidence와 provenance pointer만 보낸다. Writer의 자평은 보내지 않는다. 다음을 검토한다.

1. Research question이 충분히 구체적인가?
2. Task/environment가 실제 실행 가능한가?
3. Data generation/acquisition path가 존재하는가?
4. 최소 baseline model/system이 실행되는가?
5. Evaluation이 interpretable evidence를 생성하는가?
6. Failure 진단 instrumentation이 충분한가?
7. seed/config/commit/dataset/run provenance가 남는가?
8. First Meaningful Baseline 결과가 존재하는가?
9. Loop 2에서 test 가능한 open uncertainty/hypothesis가 최소 하나 있는가?

Verdict는 `READY | READY WITH RISKS | NOT READY` 중 하나이며 evidence, uncertainty, Loop 2 risk, 남은 bootstrap task를 짧게 반환한다. Reviewer 결과와 artifact locator는 같은 bootstrap note에 append한다. `NOT READY`면 가장 큰 readiness gap을 다음 task로 선택한다. `READY WITH RISKS`는 risk를 숨기지 않고 human gate에 올린다.

## 6. Loop 1 → Loop 2 handoff (HARD)

Readiness 결과를 제시하고 사용자가 `GO TO LOOP 2 | CONTINUE BOOTSTRAP | REDIRECT` 중 하나를 결정한다. Agent가 자동 전환하지 않는다.

- `CONTINUE BOOTSTRAP`: reviewer gap에서 information gain이 가장 큰 다음 task를 agent가 선택
- `REDIRECT`: 기존 note를 `stopped`로 바꾸고 사용자 결정을 기록 → `(a) spec` 반영 → revised boundary·budget 명시 재승인 뒤에만 `active`. Intent가 완전히 달라지면 기존 note를 사유와 함께 `consumed`하고 새 note 제안
- `GO TO LOOP 2`: 현재 starting state를 아래 기존 canonical home에 고정하고 bootstrap note를 `consumed`. `RESEARCH_SPEC §1`이 provisional이면 기존 spec protocol대로 thesis 초안을 제시하고 사용자 발화로 확정한 뒤 handoff

Handoff는 새 거대 문서를 만들지 않는다.

- `RESEARCH_SPEC §0/§1/§2/§3/§4`: question/thesis, baseline, observed failure, 현재 evaluation axes
- `ARCHITECTURE.md`: task/environment, data path, baseline system, run/eval/instrumentation command·artifact 위치
- `progress.md`: Stage, First Meaningful Baseline done pointer, known limitations/open uncertainty, Loop 2 후보, repro pointer, bootstrap note/readiness review/사용자 GO decision pointer
- baseline `done`: 실제 수치·qualitative evidence·raw artifact
- bootstrap note: 위 canonical pointer와 readiness verdict만 남김

Fresh Loop 2 agent가 이 파일들만 읽고 시작할 수 있어야 한다. `GO TO LOOP 2`는 perfect/final freeze가 아니라 controlled hypothesis testing에 충분한 starting state를 기록하는 것이다. 다음 `/research-loop` boundary·budget은 별도 승인한다.

## 7. Loop 2 → Loop 1 return

Loop 2 evidence가 evaluation validity, task formulation, data acquisition assumption, instrumentation adequacy 같은 foundational setup을 흔들면 hypothesis를 억지로 반복하지 않는다. `/research-loop`는 `RE-BOOTSTRAP RECOMMENDED`와 raw evidence·영향 surface·가장 싼 bootstrap check를 제시하고 멈춘다. 사용자가 승인할 때만 이 command를 새/재개 bootstrap boundary로 시작한다.

## 하지 않는 것

- 일반 `/harness`를 multi-task engine으로 변경
- Loop 1의 모든 탐색에 one-hypothesis/one-axis/confirmatory 규율 강제
- data/model/eval 조기 immutable freeze
- fixed metric list·publication-ready evaluation 선요구
- 새 execution engine, generic state framework, plugin/schema hierarchy
- readiness verdict 뒤 자동 Loop 2 시작
