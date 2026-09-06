---
name: close
description: 사용자가 "세션 close/마무리"라고 할 때. plan의 게이트를 실제로 돌리고, done의 수치와 완료 주장이 산출물에 근거하는지 fresh 검토자가 확인한 뒤 종료 계약을 채운다. done이 없는 가벼운 세션은 검토 없이 정리만 한다.
---

# close — 근거 확인 후 마감

1. `dinnno gates docs/plans/plan_v{N}_*.md --record`를 실행하고 결과 표를 그대로 붙인다. FAIL이 있으면 done §2·§3에 반영한다. `PENDING`은 사용자가 직접 봐야 하는 수동 게이트다. 사용자에게 확인을 묻고, 확인 발화를 받으면 스크립트가 알려준 `확인` 줄을 plan §5에 넣은 뒤 다시 돌린다. 사용자 확인 없이 PASS로 적지 않는다. `STALE`이나 "정의 변경"이 뜨면 결과를 본 뒤 기준이 바뀐 것이니 그 사실을 done §3에 적고 현재 결과만 인정한다.
2. 이 세션이 `done_v{N}`을 썼으면 fresh 검토자에게 보낸다. 런타임의 read-only 서브에이전트 또는 `dinnno review --with codex|claude`. 입력은 파일 경로(plan, done, 산출물 경로)뿐이고, 질문은 하나다: "done §2의 수치와 완료 주장 각각에 실재하는 근거 파일(metrics, 로그, diff)이 있는가. 없는 것을 파일:줄로 나열하라." 이 세션의 요약이나 자평은 주지 않는다.
3. 근거 없는 주장은 고치거나 "미검증"으로 바꾼다. verdict가 뒤집히면 사용자에게 보고하고, done §3 재작성은 확인 후에 한다.
4. `harness` §5 종료 계약을 채우고 종료 보고를 쓴다. 검토에서 반영하지 못한 것은 보고에 적는다.

TODO 체크나 progress 갱신 여부 같은 형식 점검은 `dinnno check`가 하므로 검토자에게 시키지 않는다. git commit/push는 사용자 몫이다.
