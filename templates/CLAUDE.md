# Project: {프로젝트명}

## Thesis (1줄)

`<failure mechanism> + <principled fix>` — 채워지지 않으면 spec 작성부터.

전체 스펙: `docs/RESEARCH_SPEC.md`

## 현재 상태

- 마지막 plan: `docs/plans/plan_v{N}_*.md`
- 마지막 done: `docs/done/done_v{N}.md`
- 다음 실험 후보: (한 줄)

## 핵심 디렉토리

- `configs/` — 실험별 yaml (실험 1개 = 파일 1개, 코드 금지)
- `src/` — datasets, models, train, eval
- `scripts/` — `train.py`, `eval.py`, 플롯, 테스트
- `libs/` — 써드파티 (읽기 전용)
- `docs/` — spec, plan, done

## 프로젝트 고유 규칙

- (예: 사용 시뮬레이터, 로봇 플랫폼, 데이터셋, 평가 지표)
- (예: 외부 의존성 — Isaac Lab 2.x, ROS 2 Humble, ...)

## 명령어

```bash
# 학습 / 평가 / 플롯 / 테스트 등 자주 쓰는 커맨드
```

---

전역 행동 규약은 `~/.claude/CLAUDE.md` 참조. 작성 원칙: Specific / Structured / Reviewed / Concise (100줄 이하).
