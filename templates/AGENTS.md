# Project: {프로젝트명}

## Thesis (1줄)

`<failure mechanism> + <principled fix>` — 채워지지 않으면 spec 작성부터 시작한다.

전체 스펙: `docs/RESEARCH_SPEC.md`
Research workflow: `$harness`

이 프로젝트는 논문 단위 research 프로젝트다. 모든 Codex 세션은 `$harness`로 진입한다. 직접 호출되지 않았더라도 research 작업이면 해당 스킬의 진입 적재와 단위 확인을 묵시 수행한다. thesis(`docs/RESEARCH_SPEC.md §1`)가 모든 단위의 목적지다.

## 현재 상태

- 한눈에: `docs/progress.md`
- 마지막 plan: `docs/plans/plan_v{N}_*.md`
- 마지막 done: `docs/done/done_v{N}.md`
- 다음 실험 후보: (한 줄)

## 핵심 디렉토리

- `configs/` — 실험별 yaml. 실험 1개 = 파일 1개.
- `src/` — datasets, models, train, eval.
- `scripts/` — train/eval/plot/test 진입점.
- `libs/` — third-party, 읽기 전용.
- `docs/` — spec, plan, done, progress, references.

## 프로젝트 고유 규칙

- (시뮬레이터, 로봇 플랫폼, 데이터셋, 평가 지표)
- (외부 의존성 — Isaac Lab, ROS 2, CUDA 등)
- 실로봇 actuation은 반드시 사용자 확인 후 실행한다.

## 명령어

```bash
# 학습 / 평가 / 플롯 / 테스트 등 자주 쓰는 명령
```

## harness 싱크

- last-sync: {설치일}
- 네이밍 매핑: 본체 이름과 이 저장소 이름이 다를 때만 한 줄씩 기록한다.

---

전역 행동 규약은 `~/.codex/AGENTS.md`를 따른다. 가까운 `AGENTS.md`는 프로젝트 맥락을 구체화하되 안전 경계를 약화하지 않는다.
