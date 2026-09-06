---
name: harness
description: dinnno 연구 프로젝트(docs/RESEARCH_SPEC.md가 있는 레포)에서 세션을 시작할 때. 현황을 읽고 이번 세션의 단위 하나를 사용자와 확인한 뒤 plan → 실행 → done으로 닫는다. 일반 코딩 레포에는 쓰지 않는다.
---

# harness — 연구 세션 하나

한 세션 = 한 단위. 단위는 가설 하나(experiment), 또는 init·spec이다. 단위 안에서는 plan → 실행 → done이 자연스럽게 흐르고, 다음 가설은 사용자가 새로 연다.

## 1. 진입

`dinnno check`를 실행한다(세션 시작 훅이 이미 `[dinnno]` 줄을 출력했으면 생략). 크기 경고, placeholder, 미동기 CHANGELOG, 미결 결정이 거기 나온다.

그다음 읽는다: `docs/RESEARCH_SPEC.md`(§1 thesis, §4 비교 축) · `docs/ARCHITECTURE.md` · `docs/progress.md`의 헤더·타임라인·Matrix와 미체크 결정 큐 · `docs/LEARNINGS.md`의 "현재 유효" 절 · 진행 중인 `docs/plans/plan_v{N}_*.md`. 옛 plan/done, 세션 로그, 이력 절은 필요한 항목만 grep한다. check가 50K 초과로 표시한 파일은 통째로 읽지 않는다.

## 2. 단위 확인 (사용자 confirm 한 번)

현황을 몇 문장으로 말하고 하나를 추천한다.

- **init** — placeholder 채우기. `docs/_GUIDE.md`의 인터뷰 규약대로 사용자 발화에서 끌어낸다.
- **spec** — thesis나 비교 축 변경. 사용자 소유 결정이라 초안은 제안일 뿐이다.
- **experiment v{N}** — 새 가설 또는 진행 중 가설 이어가기.
- **loop** — 사용자가 명시적으로 원할 때만 `loop` 스킬.

모호하면 추측하지 말고 묻는다. 세션 중 사용자가 새 아이디어를 말하면 `progress.md` 결정 큐에 💡 한 줄로 적는다. 기록이지 채택이 아니니 그 자리에서 평가하지 않는다.

## 3. experiment

**plan.** `docs/plans/_plan_template.md`를 복사해 `plan_v{N}_{slug}.md`를 쓴다. §3 게이트 표에 성공 기준을 실행 가능한 명령과 기대 출력으로 적는다. 완성되면 "이 plan으로 실행 시작?"을 추천안과 최강 대안 하나를 붙여 한 번 묻는다. 설계 결정이 크면 `plan-redteam` 스킬로 fresh 리뷰를 먼저 받을 수 있다.

**실행.** 이 세션이 직접 구현한다. 서로 독립인 파일이 여럿이면 런타임의 서브에이전트로 병렬 fan-out하되, ARCHITECTURE와 plan §2 전체를 함께 넘긴다. 긴 학습은 백그라운드로 돌리고 기다리는 동안 eval·plot·done 골격을 준비한다. plan §3 예산 안에서는 code-level 수정과 재실행을 묻지 않고 반복한다. experiment-level 이상(발산, 가설 반증, 한 번 고친 뒤 재실패)은 원문 출력과 함께 보고하고 멈춘다.

**done.** `docs/done/_done_template.md`를 복사해 `done_v{N}.md`. `dinnno gates docs/plans/plan_v{N}_*.md` 결과가 §2의 근거다. negative 결과는 kill이 아니다. 주장 범위와 실측 범위가 같은지, metric이 목표 품질과 같은 방향인지, seed×rollout이 그 효과를 감지할 수 있었는지, baseline·config·데이터가 깨끗한지 네 가지를 스스로 확인하기 전에는 "insufficient evidence"로 쓴다. kill과 thesis 변경은 사용자 결정이다.

## 4. 위임과 모델

- 설계와 verdict는 이 세션이 한다. 독립 검토는 다른 모델로 받는다: `dinnno review --with codex|claude <prompt.md>`, 또는 런타임의 fresh read-only 서브에이전트. 리뷰어에게는 파일 경로와 목표만 주고 이 세션의 결론은 주지 않는다.
- thesis, 비교 축, kill처럼 논문을 바꾸는 판단은 사용자에게 올린다. 더 큰 모델의 세션이 필요하다고 보이면 그렇게 말한다.
- 넓은 코드 탐색은 런타임의 read-only 탐색 서브에이전트에, PDF·대용량 로그 요약은 `dinnno review`에 맡긴다.

## 5. 종료

사용자가 "close/마무리"라고 하면 `close` 스킬. 아니어도 아래는 채운 뒤 끝낸다. 다음 세션은 이 대화가 아니라 이 파일들만 읽는다.

- plan §6 체크와 §5 로그 한 줄.
- done을 쓴 단위면 `progress.md` 타임라인 행, Matrix 셀, 헤더(Stage, anchored commit).
- thesis나 방법론이 움직였으면 `RESEARCH_SPEC.md` §0 현재 방향.
- 미룬 결정은 `progress.md` 결정 큐에 한 줄.

종료 보고는 결론(수치 포함)을 먼저, 그다음 실제 한 것, 예상과의 차이, 다음 후보 두세 개.

## 런타임 메모

Claude `/harness`, Codex `$harness`, Grok `/harness`. 서브에이전트, 백그라운드 실행, 병렬 워크플로는 각 런타임의 것을 쓴다. Claude에서 30분 넘는 run을 시작하면 `/remote-control` 전환을 한 줄로 안내한다.
