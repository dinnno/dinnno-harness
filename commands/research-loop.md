---
description: optional evidence-driven outer research loop — 기존 /harness의 plan→Execute→Verdict를 그대로 반복하되, hypothesis 전에 current evidence·Second Brain·필요시 external research를 수집하고 fresh Claude/Codex 독립 해석으로 가장 싼 판별 실험을 고른다. 명시 opt-in 없이는 기존 workflow를 바꾸지 않는다.
---

# /research-loop — evidence → hypothesis → discriminating experiment

이 커맨드는 기존 `/harness` 위의 **선택형 outer loop**다. `/harness`의 experiment, plan, implementer, Execute, done, progress, `/close`를 대체하지 않는다. `docs/LOOP.md`의 config/trial autoloop도 그대로인 inner loop다.

사용자가 `(research-loop)`를 명시적으로 선택하지 않았으면 실행하지 않는다. 미사용 프로젝트와 세션은 main의 `/harness → plan → Execute → Verdict → 사용자 다음 가설 선택`을 그대로 따른다.

## 0. Loop authorization (HARD 1회)

먼저 `/harness` §1 상태를 적재한다. `active` 또는 `stopped` research-loop note가 있으면 새로 만들지 않는다. `active`는 재개 여부를 묻고, `stopped`는 멈춘 gate·남은 boundary/budget을 다시 보여 준 뒤 사용자의 명시적 재승인을 note에 기록하고 `active`로 바꿀 때만 재개한다. 새 loop면 `docs/notes/YYYY-MM-DD_research-loop-{slug}.md` 하나에 아래만 기록한다. Metrics·실험 서사는 복제하지 않고 plan/done/run 포인터만 둔다.

```markdown
# research-loop: {question}
- status: proposed | active | stopped | consumed
- thesis/axis boundary: {RESEARCH_SPEC line/axis}
- allowed change surface: {config/code/module 범위}
- budget: {max iterations, total GPU h, per-run cap, external-research cap}
- cross-model policy: {trigger 목록, periodic interval 또는 none}
- stop: {no-improve, anomaly, confidence, budget 조건}
- approved: {YYYY-MM-DD 사용자 승인 원문 또는 pending}
- current: {plan/done pointer, open uncertainty 1줄}

| k | evidence/analysis | plan | done | terminal | budget used | next/gate |
|---|---|---|---|---|---|---|
```

사용자에게 추천 boundary와 최강 대안 하나를 제시하고 승인받는다. 승인 한 번은 **그 boundary·총예산 안의 local hypothesis iteration**만 허가한다. 각 iteration은 여전히 `plan_vN → Execute → done_vN`으로 닫고 한 번에 활성 가설 하나만 둔다.

이 승인은 thesis/비교 축 변경, boundary 밖 architecture, experiment-level anomaly 후 재실행, 예산 초과, 실로봇, 파괴적 작업, kill/NO-GO를 허가하지 않는다.

## 1. OBSERVE — 해석 전에 evidence manifest

현재 plan/done과 raw artifact에서 bounded manifest를 만든다. Primary Claude의 결론이나 다음 아이디어는 넣지 않는다.

- 질문, active axis, plan의 H1/H2·threshold
- config, seed, commit, dataset snapshot, environment
- command, terminal state(`success|failed|killed|timeout`), stdout/stderr·metrics·run 경로
- failed run과 선택한 rollout video/image frame 경로
- baseline과 관련 이전 done/ablation 포인터
- Second Brain citation과 external citation(있을 때)

예정했던 stage마다 terminal row가 있어야 한다. Process handle/session ID를 보존해 같은 run을 polling 중 다시 시작하지 않는다. 빈 agent 결과·누락 stage·structured output만 있는 상태는 성공이 아니라 explicit failed stage다.

## 2. ACQUIRE EVIDENCE — hypothesis보다 먼저

### A. Current experimental evidence (매 iteration 필수)

Machine-readable metric source와 raw failure를 먼저 확인한다. `done` 요약만 읽고 원인을 만들지 않는다. Evidence가 부족하면 `insufficient evidence`로 두고 가장 싼 계측/진단 실험을 우선한다.

### B. Second Brain (provider가 있으면 bounded retrieval)

Backend나 절대 경로를 하드코딩하지 않는다. 다음 순서로 read-only provider를 찾고 실제 존재·manifest를 확인한다.

1. `SECOND_BRAIN_ROOT`
2. wrapper 안 `tools/oh-dinnno-opsidian`
3. 전역 `CLAUDE.md`에 선언된 legacy fallback

`interface/manifest.yaml`의 `read_only_query: true`와 지원 schema를 확인한 뒤 `interface/brain_query.py`를 호출한다. Query는 thesis + 관찰된 anomaly + mechanism alias/tag로 구체화하고 `--types source,concept,idea,index --limit 8 --max-chars 12000`으로 제한한다. 지원 목록에 있는 경우만 `--project-lines`를 쓴다. Empty면 동의어로 한 번만 확장한다.

보존할 provenance: query, vault commit, `brain:...@commit`, original URL, depth, provenance gap, truncated. `captured`나 provenance-gap 결과는 후보 mechanism은 만들 수 있지만 구현 세부나 강한 claim을 확정하지 못한다. Vault 전체 dump와 project task 중 wiki write-back은 금지한다.

CLI 부재, nonzero exit, malformed JSON, unsupported schema면 note에 `second-brain: unavailable/error — {원문}`을 남기고 계속한다. Vault를 우회해 직접 전부 읽지 않는다. 이 실패는 아래 external-research trigger다.

### C. External research (조건부)

다음 중 하나일 때만 현재 환경의 deep/web/literature research를 사용한다.

- current evidence가 기존 설명과 불일치
- 독립 분석의 causal explanation이 다름
- Second Brain이 empty/error/shallow-only
- 새로운 failure mechanism 또는 known method 가능성
- architecture/thesis 영향 가능성
- 같은 local explanation/실험이 반복
- novelty·prior-art 확인 필요

사용한 source는 기존 `/add-ref`·references 규약으로 URL과 버전을 남긴다. 구현 대상으로 선택한 source만 `/blueprint-ref`로 승격한다.

§3 독립 분석에서 새 external-research trigger가 생기면 이 단계로 한 번 돌아온다. 새 source를 source manifest에 추가한 뒤, 그 근거가 causal 판정을 바꿀 수 있는 분석자만 서로의 이전 결론 없이 한 번 다시 실행한다. 반복 검색·재분석은 authorization의 외부 조사 예산을 넘지 않는다.

## 3. HYPOTHESIZE — evidence-backed competing explanations

아래 trigger 중 하나면 동일 manifest를 **서로의 결론 없이 동시에** fresh `research-analyst`와 `codex:rescue`에 보낸다.

- unexpected 또는 negative result
- decision threshold 근처
- 반복 실패 또는 low-confidence interpretation
- architecture/thesis implication
- 첫 iteration과 authorization에서 정한 periodic sanity interval
- GPU experiment 비용에 비해 분석 비용이 무시 가능한 경우

두 결과를 `docs/notes/YYYY-MM-DD_rl-v{N}-analysis.md` 한 파일에 source manifest → Claude 분석 → Codex 분석 → synthesis 순으로 보존하고 `done §3` 또는 §4에서 evidence pointer로 가리킨다. 이 분석은 기존 `done §5`의 Verdict 외부 리뷰를 대체하지 않는다. Trigger가 없으면 primary 해석을 `done §3`에 쓰고 별도 파일을 만들지 않는다.

한 분석 channel이 unavailable/error면 그 사실을 analysis note에 남기고 다른 모델의 흉내로 채우지 않는다. Raw fact disagreement·architecture/thesis 영향·kill 후보처럼 독립성이 판정의 전제인 경우는 HARD로 반환한다. 그보다 낮은 위험의 iteration은 claim을 한 단계 낮추고 진행할 수 있다.

Synthesis는 voting이 아니다.

- raw fact가 다름 → source를 다시 확인; 해결 안 되면 HARD
- causal explanation이 다름 → 가장 싼 discriminating experiment
- confidence만 다름 → 더 약한 claim
- thesis/axis/architecture 영향 → HARD

새 hypothesis에는 최소한 H1, 연결 evidence, mechanism reasoning, strongest alternative H2, 해결할 uncertainty/information gain, 가장 싼 판별 test, H1/H2별 expected outcome이 있어야 한다. Eureka·researcher intuition도 허용하지만 출발 observation을 citation/pointer로 남긴다.

## 4. DESIGN → EXECUTE — 기존 lifecycle 재사용

새 schema를 만들지 않는다.

- `plan §1`: H1, evidence pointer, mechanism, H2, information gain
- `plan §2`: 한 change axis의 최소 변경
- `plan §3`: 가장 싼 discriminator, H1/H2 expected outcome, metric, threshold, budget, stop
- `plan §4`: 결과별 branch

Plan을 먼저 완성한 뒤 기존 implementer와 `/workflow-ops`로 Execute한다. Dispatch에는 scope, expected artifact, terminal status/marker, timeout, memory estimate/cap을 명시한다. GPU 경로를 우선하고 안전한 RAM 추정·상한이 없으면 시작하지 않는다. Missing/empty/timeout result를 걸러내 성공처럼 보이게 하지 말고 ledger에 실패로 기록한다.

Loop authorization 안에서는 매 local plan마다 별도 Execute confirm을 반복하지 않는다. 단, experiment-level anomaly가 생기면 raw evidence를 모은 뒤 interpretation과 다음 plan 초안까지만 만들고 **실행 전에 HARD로 반환**한다.

## 5. INTERPRET → UPDATE → NEXT

기존 `_done_template.md`로 Verdict를 작성한다.

- §2: raw result와 provenance
- §3: `supported | contradicted | insufficient evidence`, 예상–실제 gap, confounder
- §4: competing hypothesis, 다음 discriminator 후보, 필요시 independent analysis/synthesis pointer
- §5: 기존 `/harness` 규약의 별도 Verdict 외부 리뷰

기존 `/harness` §5대로 progress timeline·Matrix·Stage/repro pointer와 plan TODO/log를 같은 iteration에서 닫는다. Runtime note ledger에는 상세를 복제하지 않고 plan/done/evidence pointer, terminal state, 소비 budget, next/gate만 한 행 append한다.

다음 조건을 모두 만족할 때만 다음 local hypothesis로 이동한다.

- 현재 plan/done closure 완료
- 다음 hypothesis가 승인 boundary와 남은 budget 안
- raw fact disagreement 없음
- experiment-level anomaly, destructive/real-robot action, kill 결론 아님

그 외에는 note를 `stopped`로 바꾸고 사용자가 결정할 질문 하나와 최강 대안을 제시한다. 정상 종료면 `consumed`; 기존 `/tidy`가 archive한다.

사전 선언한 H2 outcome이 관찰된 것은 실행 failure가 아니며 유효한 Verdict다. 다만 active H1을 반증한 experiment-level 결과이므로 synthesis와 다음 plan 초안까지만 만들고, 기존 `/harness` HARD 규칙에 따라 다음 Execute 전에 사용자에게 반환한다.

## 항상 사람이 결정하는 것

- thesis/comparison axis 또는 entirely new direction
- boundary 밖 architecture/code surface
- 승인 밖 expensive run·budget 재인가
- experiment-level anomaly 후 실행/재시도
- real robot, destructive action, git commit/push
- final kill/NO-GO
- raw fact에 대한 independent reviewer disagreement

## 하지 않는 것

- 일반 `/harness`의 다음 가설 gate 변경
- 기존 `LOOP.md` 재정의
- 매 iteration 무조건 Second Brain/web/two-model 호출
- agent의 아이디어를 evidence로 둔갑
- 두 분석의 voting/평균
- 실행 failure를 hypothesis contradiction으로 기록
- 새 state machine, plugin, generator, docs hierarchy
