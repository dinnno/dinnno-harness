# Project: {프로젝트명}

## Thesis (1줄)

`<failure mechanism> + <principled fix>` — 채워지지 않으면 spec 작성부터.

전체 스펙: `docs/RESEARCH_SPEC.md`
Agent 위임 가이드: `/harness` §4 (codex 위임 / Explore / writer≠reviewer).

이 프로젝트는 research 프로젝트다. 모든 Claude 세션은 `/harness`로 진입(없이 시작했어도 본문 §1-§4 묵시 적용). thesis(`docs/RESEARCH_SPEC.md §1`)가 모든 단위의 목적지 — 단순 엔지니어링 모드 ❌, 모듈 제안·실험 설계·검증 모드 ✓.

## 현재 상태

- 한눈에: `docs/progress.md` (cross-version 타임라인 + repro 헤더)
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

## harness 싱크

- last-sync: {설치일}
- 네이밍 매핑: 본체 이름 ≠ 이 레포 이름일 때만 한 줄씩 (예: `_plan_template.md` → `plans/CLAUDE.md`). 없으면 비워둠.

---

전역 행동 규약은 `~/.claude/CLAUDE.md` 참조.
