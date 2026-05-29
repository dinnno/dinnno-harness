# docs/plans/

이 폴더는 `plan_v{N}_{short-name}.md` 형식의 실험별 plan을 담는다.

## 1 plan = 1 가설 = 1 세션 = 1 터미널

한 가설의 풀 사이클(Setup→Execute→Verdict)이 한 세션에서 흐른다. 이 파일은 **Setup의 산출물**. Setup 끝나면 사용자 confirm 1회 후 Execute로 진입. 학습은 Execute 안. done은 Verdict 산출물.

여러 ablation을 한 plan에 묶으면 검증이 약해진다 — 가설별로 쪼개고 각각 새 터미널.

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

## 시작 방법

새 plan은 같은 폴더의 `_plan_template.md`를 복사해서 시작한다:

```bash
cp docs/plans/_plan_template.md docs/plans/plan_v{N}_{short-name}.md
```

섹션 헤딩은 고정. 채울 내용이 없으면 "N/A — 사유"를 쓰고 비워두지 않는다.

## TODO 운영 (§6)

plan_v{N}.md §6은 day-hours 단위 working checklist. plan §1-§4가 weekly 단위 설계라면 §6은 daily 실행.

**세션 시작 시:**
- plan 적재 후 §6 보고 **첫 미체크 항목부터** 시작. 사용자가 다른 항목 지정하면 그것 우선.
- 새 항목이 떠오르면 §6 끝에 추가 (체크 박스 미체크 상태).

**세션 종료 시:**
- 끝낸 항목 체크.
- §5 세션 로그에 한 줄 추가 (`- {date} {핵심 변경 한 줄}`).
- 부분만 끝났으면 그 항목은 미체크 유지, 진행 상황을 §5에 적기.

**TODO ≠ plan 재설계:**
- §6 항목이 §1-§4와 어긋나기 시작하면 plan 자체를 다시 슬라이싱. §6에 "이번 plan의 design을 바꿔야 함" 같은 항목 박지 말 것.
- §6은 §1-§4 안에서의 실행 단위만.
