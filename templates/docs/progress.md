# Progress

<!-- 자기완결 갱신 규칙: done/spec 단위 끝에 한 줄 — 타임라인 행 + Ablation 셀 + 헤더(anchored commit/Stage).
     이 파일은 "여러 done에 흩어진 cross-version 상태의 인덱스"다. done 수치를 복제하지 말고 결론+포인터만(done보다 짧게).
     상세 규칙: docs/_GUIDE.md(또는 폴더 CLAUDE.md) §progress.md 갱신 protocol. -->

Thesis → `RESEARCH_SPEC.md §1` ({한 줄})
Stage: {예: A — PoC} | spec: {v0} | last anchored commit: {hash}({date})

## Phase

최종 goal(`RESEARCH_SPEC §1 thesis` = paper contribution)까지의 mile stone.

- [ ] Phase 0: Naive baseline (plan_v0 / done_v0)
- [ ] Phase 1: {module 제안 1}
- [ ] Phase 2: {ablation suite}
- [ ] Phase 3: {real-robot / sim2real}
- [ ] Phase 4: Paper draft

## 타임라인 (cross-version 인덱스)

| unit | 상태 | 한 줄 결론 (thesis position) | done |
|---|---|---|---|
| plan_v0_* | {closed/locked/running} | {수치 아닌 판정 + thesis position} | done_v0 |

## Ablation Matrix

`RESEARCH_SPEC §6`과 1:1. 셀 = done 또는 '미측정'. (seed 명시. sim/real·ckpt 컬럼은 그 stage 도달 시 추가)

| ablation_id | 구성요소 | 가설 | done | 핵심 결론 | seed | 상태 |
|---|---|---|---|---|---|---|
| A1 | {module} | {제거 시 예측} | done_v? | {결론+포인터} | {42} | pending/running/done |

## Repro 포인터 + Open 부채

- seed {42} / config `configs/exp_*.yaml` (실험1개=yaml1개) / runs `runs/*/` / env {PyTorch·CUDA·주요 lib}
- last anchored commit {hash} — ⚠ uncommitted 있으면 재현 삼각형(seed+config+commit) 미완결, 커밋 권장.
- ckpt: {경로 또는 '학습 전 없음'}
- Open 검증 부채: {예: done_v{N}_codex.md 미작성, 조건부 spec rewrite 후보}

## 다음 결정 대기

(done §4 후보 중 사용자 선택 대기. 선택되면 Phase/타임라인/Matrix로 흡수)
