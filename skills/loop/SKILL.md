---
name: loop
description: 사용자가 명시적으로 "loop 돌리자"고 opt-in했을 때만. 승인된 경계와 예산 안에서 가설 하나를 evidence 수집 → 경쟁 가설 → 가장 싼 판별 실험 → plan/done으로 반복하거나, config 변이 autoloop(docs/LOOP.md)을 돌린다. 기본 harness 흐름을 바꾸지 않는다.
---

# loop — 승인된 경계 안의 반복

## 인가 (사용자 확인 한 번)

`docs/notes/YYYY-MM-DD_loop-{slug}.md`에 적고 승인받는다: 질문 · thesis/축 경계 · 허용 변경 표면 · 예산(반복 수, GPU 시간, run당 상한) · 정지 조건(연속 no-improve K회, experiment-level 이상, 예산 소진). 이 승인이 경계 안의 local plan 실행을 인가한다. thesis나 축 변경, 경계 밖 표면, 예산 초과, experiment-level 이상 뒤 재실행, 실로봇, kill은 계속 사용자 확인이다. RESEARCH_SPEC §6에 선언된 ablation 행을 순서대로 도는 sweep도 같은 인가 안에서 같은 방식으로 돈다.

## 반복 (활성 가설은 한 번에 하나)

1. **evidence.** 기계가독 metric과 raw failure(로그, rollout)를 먼저 본다. done 요약만 읽고 원인을 만들지 않는다. 막히면 `research-second-brain` 스킬로 선행연구 힌트를 두세 개만 가져온다.
2. **가설.** H1과 근거, 최강 대안 H2, 둘을 가르는 가장 싼 실험, 각각의 예상 관찰을 적는다. 결과가 예상 밖이거나 임계값 근처면 같은 파일 목록을 fresh 검토자와 다른 모델(`dinnno review`)에 서로의 결론 없이 보내 해석을 받는다. 투표하지 않는다. 사실이 다르면 원천을 재확인하고, 원인 설명이 다르면 판별 실험을 고르고, 확신만 다르면 더 약한 주장을 쓴다.
3. **실행과 판정.** 기존 plan → 실행 → done 그대로. 판정어는 `exploratory support | exploratory contradiction | insufficient evidence`. thesis급 주장은 튜닝에 쓰지 않은 locked confirmatory 평가(실행 전에 고정한 metric, 기준, seed×rollout)를 통과한 뒤에만 후보가 된다.
4. note에 한 행(plan/done 포인터, 결과, 소비 예산, 다음)을 추가하고 정지 조건까지 반복한다. 긴 run은 시작 전에 note에 run id·산출물 경로·시작 시각을 적고, 세션이 끊기면 그 기록부터 확인해 같은 run을 두 번 돌리지 않는다. 평가 타당성, task 정의, 데이터 가정처럼 설정 자체가 흔들리면 멈추고 사용자에게 재설계를 제안한다.

## autoloop (config 변이)

working baseline 이후, `docs/LOOP.md`의 L1–L7이 채워졌을 때만. 변이는 allowlist 안의 yaml만 만들고, keep/rollback은 J와 guard로 판정하며, ledger 한 행과 리포트 재생성이 곧 보고다. 루프가 끝나면 champion을 튜닝에 쓰지 않은 held-out 평가로 한 번 재검증한 뒤에야 Matrix에 기입한다. 코드 변경이 필요한 변이는 결정 큐에 적고 건너뛴다.
