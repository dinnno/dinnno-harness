# Progress

<!-- 이 파일은 인덱스다. done 수치를 복제하지 않고 결론과 포인터만 적는다. 세션 로그는 plan §5에.
     헤더 Stage 줄은 현재 상태만. 파일이 50K를 넘으면 dinnno check가 경고한다. -->

Thesis → `RESEARCH_SPEC.md §1` ({한 줄})
Stage: {예: A — PoC} | spec: {v0} | last anchored commit: {hash} ({date})

## Phase

- [ ] Phase 0: Naive baseline (plan_v0 / done_v0)
- [ ] Phase 1: {module 제안 1}
- [ ] Phase 2: {ablation suite}
- [ ] Phase 3: {real-robot / sim2real}
- [ ] Phase 4: Paper draft

## 타임라인

| unit | 상태 | 한 줄 결론 (thesis position) | done |
|---|---|---|---|
| plan_v0_* | {running/closed} | {수치 아닌 판정 + thesis position} | done_v0 |

## Ablation Matrix

`RESEARCH_SPEC §6`과 1:1. 셀 = done 또는 '미측정'. 수치는 mean±std, seeds(N)×rollouts.

| ablation_id | 구성요소 | 가설 | done | 핵심 결론 | seeds(N)/rollouts | 상태 |
|---|---|---|---|---|---|---|
| A1 | {module} | {제거 시 예측} | done_v? | {결론+포인터} | {42,43,44}×{20} | pending |

## Repro 포인터

- seed {42} / config `configs/exp_*.yaml` / dataset {name}@{version} / runs `runs/*/` / env {PyTorch·CUDA}
- ckpt: {경로 또는 '학습 전 없음'}

## 결정 큐 + 아이디어 인박스

<!-- 미룬 결정, [spec-drift], [kill-candidate], 💡 아이디어(사용자·Claude, 기록≠채택). 사용자가 고르면 체크하고 Phase/타임라인으로 흡수. -->

- [ ] {YYYY-MM-DD} [{tag}] {결정 요지 한 줄} ← {출처 done_v{N}/plan}
- 💡 {YYYY-MM-DD} {아이디어 한 줄}
