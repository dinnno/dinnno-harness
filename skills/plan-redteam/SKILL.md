---
name: plan-redteam
description: plan을 완성한 뒤 실행 전에, 이 대화를 모르는 다른 모델이 plan을 격추하려 시도하게 한다. thesis 정합, 모델·표현, 학습, 평가, 인과 귀속, 실행 리스크, 이력 모순의 7축을 CRITICAL/HARD/SOFT로. 결과는 대화에 원문 그대로와 plan_v{N}_codex.md에 라운드 append. 사용자가 "plan 리뷰/공격해줘"라고 할 때도.
---

# plan-redteam — fresh 모델의 plan 격추

plan을 쓴 세션은 자기 설계를 관대하게 본다. GPU 시간을 태우기 전에 다른 모델이 "이 plan은 왜 실패하는가"를 찾는다. 살아남은 plan만 실행할 가치가 있다.

## 1. 대상과 입력

- 대상: 인자가 없으면 `docs/plans/plan_v*.md` 최고 버전(`_template`, `*_codex.md` 제외). 이미 같은 번호의 done이 있으면 닫힌 단위일 수 있으니 한 줄 확인.
- 리뷰어에게 주는 것은 파일 경로 목록뿐이다: plan, `docs/RESEARCH_SPEC.md`(§1·§4 기준), `docs/progress.md`, `docs/LEARNINGS.md`, 직전 `done_v{N-1}`, 기존 `plan_v{N}_codex.md`(라운드 이어가기). 없는 파일은 "부재"로 명시한다. 이 세션의 해석과 요약은 주지 않는다.

## 2. 프롬프트 파일

세션 scratch 디렉토리에 `redteam_prompt.md`로 저장한다. 골격:

- 과제: 위 파일을 직접 읽고 plan을 적대 검토하라. 질문은 "어떻게 개선할까"가 아니라 "왜 실패하는가"다. 7축마다 격추를 시도하고, 결함이 없으면 `no finding`과 근거 한 줄.
- 7축: ① thesis 정합(SPEC §1/§4의 어느 축을 실제로 움직이나) ② 모델·표현 설계 ③ 학습 설계(objective, 데이터 규모·분포, train/eval 누수) ④ 평가 설계(metric이 주장을 증명하나, baseline 공정성, seeds×rollouts, 검정력) ⑤ 인과 귀속(confound, 빠진 ablation) ⑥ 실행·재현(config·seed 고정, 예산·정지 조건, 임계값 사전 선언) ⑦ 이력 모순(LEARNINGS, 직전 done 실측과 충돌).
- 심각도: `CRITICAL` = 실행해도 논문 주장이 성립하지 않아 재설계 · `HARD` = 그대로 실행하면 해석 불가라 실행 전 수정 · `SOFT` = 진행 가능한 개선. 차단의 기준은 하나, "이대로 실행하면 그 GPU 시간이 낭비되는가". 우아함이나 위생은 SOFT다. HARD가 많다고 좋은 리뷰가 아니다.
- 근거 규칙: 모든 finding은 `파일 §절` 인용. 일반론 대신 이 plan의 구체 수치와 자유도(데이터 크기 대 파라미터 수, 검정력, 예산 산술)를 따진다. 읽지 못한 파일은 `ACCESS FAILED`.
- 출력 형식: `## Round {r} — {날짜} — {모델}` → `READ OK:` 목록 → CRITICAL → HARD → SOFT(각: 제목, 근거 인용, 왜 치명적인가, 최소 수정 한 줄) → 축별 no-finding → verdict 한 줄 `REDESIGN | FIX FIRST (HARD n건) | EXECUTE OK`.
- read-only. 어떤 파일도 만들거나 고치지 않는다.

## 3. 실행

```bash
dinnno review --with codex <scratch>/redteam_prompt.md -o <scratch>/redteam_out.md
```

xhigh는 수 분에서 수십 분 걸리니 백그라운드로 돌리고 완료를 기다린다. `REVIEW FAILED`면 그 원문을 보고하고 멈춘다. 리뷰를 이 세션이 대신 써서 채우지 않는다. sandbox 실패가 재현됐다는 안내가 나오면 그 한 번만 `--unsafe`로 재시도한다.

## 4. 결과

- 출력 원문을 대화에 그대로 보여준다. verdict 한 줄만 맨 위로 올리고, 첫 표시에 이 세션의 요약이나 반박을 붙이지 않는다.
- `docs/plans/plan_v{N}_codex.md`에 라운드를 append한다. 신설이면 상단에 대상 plan 경로 한 줄.
- 반영은 사용자가 "타당한 지적 반영해"라고 한 뒤 일반 plan 흐름으로. 자동 재리뷰는 없고, 두 라운드 뒤에도 CRITICAL/HARD가 남으면 계속할지 묻는다. verdict가 `EXECUTE OK`여도 "이 plan으로 실행 시작?" 확인은 따로 받는다.
