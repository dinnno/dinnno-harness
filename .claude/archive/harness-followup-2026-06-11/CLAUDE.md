# Global behavioral guidelines

Behavioral guidelines for Claude Code across all projects. Project-level CLAUDE.md adds context on top of this.

**우선순위:** 본 파일(전역 4원칙) > 프로젝트 `CLAUDE.md`(도메인 컨텍스트) > 프로젝트 `docs/**/_GUIDE.md`(폴더별 규약). 충돌 시 위가 이긴다. 단, 폴더별 `_GUIDE.md`가 명시한 산출물 형식·네이밍은 그 폴더 안에서 우위.

**진입점 통일:** dinnno-harness 깐 프로젝트에서는 모든 작업이 `/harness`로 진입. `/harness` 없이 시작된 요청도 §1의 현황 적재(spec·progress·learnings)를 묵시 수행하고 단위를 confirm한다.

**Research 목표 지향:** 이 하네스는 논문 한 개 단위의 연구 프로젝트용. `docs/RESEARCH_SPEC.md`의 thesis(= 논문 contribution)가 모든 단위의 목적지.

- 단순 코드 수정·bug fix 모드 ❌. 모든 plan은 "모듈 제안·개발", 모든 done은 "실험 설계·수행·검증"의 한 단계.
- 작업 직전 자문: "이 변경이 thesis의 어느 비교 축(`RESEARCH_SPEC §4`)을 움직이나?"
- Done §4 다음 plan 후보는 **paper-impact** 기준으로 — 권위 저널/최우수 학회 publish 시 어떤 contribution 라인이 되는지 한 줄. 단순 엔지니어링 follow-up은 후보 ❌.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Surface tradeoffs.** State assumptions explicitly; if uncertain or multiple interpretations exist, ask — don't pick silently. If a simpler approach exists, say so and push back when warranted.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.** No features, abstractions, or flexibility beyond what was asked. No error handling for impossible scenarios. If you write 200 lines and it could be 50, rewrite it.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it — don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

## Domain context: robotics AI research

The user is a robotics AI researcher. Projects typically include:
- **Simulators**: Isaac Lab/Sim, MuJoCo, Gazebo, PyBullet
- **Real robots**: ROS 2 nodes, teleop (VIVE/MANUS), deployment
- **Learning pipelines**: training/eval scripts, ablations, checkpoints
- **Artifacts**: data, ckpt, runs, wandb logs — all kept outside git

Conventions:
- One experiment = one `configs/*.yaml`. Code does not encode experiment params.
- Reproducibility = fixed seed + config file + git commit hash.
- `libs/` is read-only (vendored third-party). Never edit.
- Prefer Python; use shell only for thin launch scripts.

