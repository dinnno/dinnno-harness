# docs/plans/

이 폴더는 `plan_v{N}_{short-name}.md` 형식의 실험별 plan을 담는다.

## 1 plan = 1 실험 = 1~2주 = 1 PR

크기가 안 맞으면 쪼개라. 한 plan이 여러 ablation을 동시에 다루면 검증이 약해진다.

## 각 plan에 들어가는 것

1. **타겟 limitation** — `docs/RESEARCH_SPEC.md`의 해당 줄을 그대로 인용
2. **최소 모듈/변경** — 무엇을 추가/수정하는지, 시그니처 수준
3. **검증** — ablation, metric, 실로봇 run 등 구체적인 검증 방법
4. **실패 시 분기** — 검증이 실패하면 무엇을 다음으로 시도할지

## 네이밍

- `plan_v0_naive.md` — naive baseline (RESEARCH_SPEC §2와 짝)
- `plan_v1_{component-name}.md` — 첫 ablation
- `plan_v2_{component-name}.md` — 다음
- ...

short-name은 kebab-case slug. 핵심 모듈/작업을 한두 단어로 (`tactile-encoder`, `retarget-hand`, `multi-step-rollout`).

## 자기완결성

각 plan 파일은 독립된 Claude 세션에서 실행될 수 있어야 한다. "이전 대화에서" 같은 외부 참조 금지. 필요한 파일 경로·문맥은 plan 안에 다 적는다.
