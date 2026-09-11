# plan_v{N}_{short-name}

> `_plan_template.md` 복사본. 모든 절을 채우거나 "N/A — 사유".

## 0. 짝

- spec 줄: `docs/RESEARCH_SPEC.md §{section}` "..."
- 이전 done: `docs/done/done_v{N-1}.md` (있으면)

## 1. 타겟 limitation

(RESEARCH_SPEC §3에서 인용 한 단락. 이 plan이 어느 failure를 노리는가. 가설 H1과 최강 대안 H2를 한 줄씩.)

## 2. 최소 변경

(파일 경로 + 시그니처 수준. ARCHITECTURE의 어느 모듈에 들어가는지. "어떤 모듈을 제안하는가")

## 3. 검증 설계와 게이트

- ablation: (RESEARCH_SPEC §6과 매핑)
- metric: (RESEARCH_SPEC §4 비교 축)
- 실행: (커맨드, sim/실로봇, 예상 run 시간)
- 루프 예산: (최대 재시도 N회 · 최대 GPU h — 이 안에서는 code-level 조정과 재실행을 묻지 않는다)
- 정지 조건: (임계값 달성 / 예산 소진 / experiment-level 이상 — 먼저 오는 것)

게이트 표는 `dinnno gates`가 실행한다. command 셀 안의 `|`는 `\|`로 쓴다. expect는 출력에 대한 정규식이고, 비우면 exit 0만 본다. 실행 전에 기준을 적는 것이 사전등록이다. 각 게이트에는 정의 해시(#xxxxxxxx)가 붙어서, 결과를 본 뒤 기준을 고치면 이전 PASS는 무효로 표시된다. 사람이 봐야 하는 것은 `MANUAL:`로 적는다. 사용자가 확인을 말하면 plan 파일에(§5 권장) `- YYYY-MM-DD 확인 {gate}#{hash}: "사용자 발화"` 한 줄을 넣어야 PASS가 된다. `dinnno gates --record`의 기록 줄은 파일 끝에 붙는다.

| gate | command | expect |
|---|---|---|
| {eval-success} | `python scripts/eval.py --config configs/exp_v{N}.yaml --seeds 42,43,44` | `success=0\.[7-9]` |
| {unit-test} | `pytest tests/test_{module}.py -q` | `passed` |
| {grasp-visual} | `MANUAL: runs/v{N}/rollouts/*.mp4 10개를 사용자가 보고 실제 grasp인지 확인` | |

## 4. 실패 시 분기

(게이트가 실패하면 다음 시도 1–2개. H2가 맞았을 때 무엇을 하나.)

## 5. 세션 로그

- {YYYY-MM-DD} {한 줄}

## 6. TODO

- [ ] {작업 1}
- [ ] {작업 2}

## 7. 위임 대장

팀장이 pane·서브에이전트에 넘긴 몫마다 한 줄. 통합 열은 팀장이 직접 검증한 뒤에만 채운다. 위임이 없었으면 "N/A".

| 이름 | 모델 | 브리프 | report | 팀장 검증 | 통합 |
|---|---|---|---|---|---|
| {impl-loader} | {sol high} | {~/.dinnno/fanout/.../impl-loader/brief.md} | {.../report.md} | {pytest 재실행 통과 / 미실행} | {반영 / 반려: 사유 / 대기} |
