---
name: fanout
description: >
  pane을 N개 열어 codex나 claude(opus)에게 일을 나눠 맡기고, 인수인계 브리프를
  파일로 넘긴 뒤 결과를 회수·통합한다. 사용자가 "pane 몇 개 열어서", "나눠서
  시켜", "병렬로 돌려", "동시에 여러 개", "codex한테 넘겨", "opus가 구현하게",
  "인수인계해서", "분담시켜", "위임" 같은 말을 하면 반드시 이 스킬을 쓴다.
  구현·조사·리뷰를 여러 갈래로 벌릴 수 있는 작업이 나왔을 때, 사용자가 pane을
  말하지 않았더라도 이 방식이 나으면 제안한다. 목적은 팀장 세션이 분해·감독·취합·
  검토만 하고 구현 토큰은 pane이 쓰게 하는 것이다. herdr 안(HERDR_ENV=1)에서만
  동작한다. 이미 시작된 pane의 상태를 보거나 herdr CLI 자체를 다루는 일은
  herdr 스킬 쪽이다.
argument-hint: "[N] [codex|opus|grok]"
---

# fanout — pane에 일을 넘기고 결과를 회수한다

이 스킬을 부르는 세션이 그 프로젝트의 **팀장**이고, pane의 에이전트가 팀원이다. 큰 구현까지 팀장이
하면 컨텍스트가 빠르게 녹는다. 이 스킬은 그런 몫을 나눈다:
**팀장은 분해·브리프·감독·취합·검토를 하고, 큰 구현 토큰은 pane의 codex나 opus가 쓴다.**
팀원 결과의 책임은 팀장에게 있다. 합치고 검증하기 전까지 그것은 결과가 아니다.

여기서 두 가지 규칙이 따라 나온다. 지키지 않으면 나누는 의미가 없다.

- **브리프는 파일로 쓰고 프롬프트에는 경로만 넘긴다.** 긴 텍스트를 터미널에 붙여넣으면
  괄호·따옴표에서 깨지고, 그 자체가 팀장의 출력 토큰이다.
- **결과도 파일로 받고 팀장은 그 파일만 읽는다.** pane 화면을 스크롤해 읽으면 절약한
  토큰이 그대로 되돌아온다. 게다가 에이전트는 대개 alternate screen에서 돌아서
  지나간 출력을 온전히 되읽을 수도 없다.

## 0. 전제

```bash
test "${HERDR_ENV:-}" = 1
```

실패하면 herdr 밖이다. pane 대신 런타임의 서브에이전트에 같은 브리프(§2)를 넘기고, 회수·통합(§6)은 똑같이 한다.

herdr CLI 문법이 헷갈리면 `herdr agent`, `herdr pane`을 인자 없이 실행해 확인한다.
이 스킬은 CLI 사용법이 아니라 **무엇을 넘기고 어떻게 회수하는가**만 다룬다.

## 1. 분해

나눌 수 있는 일인지부터 판단한다. 다음이면 나누지 말고 그렇게 말한다.

- 앞의 결과가 있어야 뒤를 시작할 수 있다 → 한 pane에 순서대로 준다.
- 같은 파일을 둘 이상이 고쳐야 한다 → 파일 충돌은 조용히 서로를 덮어쓴다.
- 전체가 30분 안에 끝난다 → 브리프 쓰는 시간이 더 든다.

나눌 때의 기준:

- **파일 소유권이 겹치지 않게.** 각 몫에 "네가 쓰는 파일" 목록을 명시할 수 있어야 한다.
  겹치는 부분이 있으면 그 부분만 팀장이 먼저 처리하고 나머지를 나눈다.
- **각 몫은 혼자 끝낼 수 있는 완결 단위.** "구현"과 "그 구현의 테스트"를 다른 pane에
  주지 않는다.
- **소유권은 무엇을 읽느냐가 아니라 무엇을 쓰느냐로 따진다.** 조사·리뷰처럼 정말 아무것도
  쓰지 않는 몫은 얼마든지 병렬로 안전하다. 그러나 재현 확인·프로파일링·벤치는 코드를 한 줄도
  안 고쳐도 `outputs/`·`runs/`·metrics·캐시에 쓴다. 같은 cwd에서 기본 출력 경로가 같으면
  서로의 결과를 덮어써 **틀린 검증 근거**를 만든다. 그런 몫은 브리프에서 pane마다 다른 출력
  경로를 지정하고, 경로를 분리할 수 없으면 나누지 말고 순차로 돌린다.
- **보통 2~4개.** 그 이상은 감독이 안 되고 blocked 하나를 놓치면 전부 대기한다.
  사용자가 N을 말했으면 그 수를 따르되, 겹침 때문에 줄여야 하면 이유를 한 줄로 말한다.

pane 수를 정한 직후 `dinnno res`로 이웃 프로젝트가 지금 쓰는 GPU·RAM을 보고 **자원을 나눈다.**
실행하는 몫마다 probe 최대치(없으면 한 줄 추정)의 1.5배를 상한으로 브리프에 적고, 그 합이
지금 여유 안에 들어가면 그대로 동시에 띄운다. 안 들어가면 몫을 줄이지 말고 순서를 나눈다.
실행이 없는 몫(문서·리뷰)은 예산에서 뺀다.

### 모델 배정

팀장(Opus 5.5 medium 이상이나 gpt-6-sol)은 30분 안에 끝나는 작은 몫은 직접 하고, 나머지를 pane에 준다.

pane의 모델은 사용자 지정이 우선이고, 없으면 몫의 종류로 정한다.

| 몫 | 모델 | `herdr agent start` 뒤에 붙이는 인자 |
|---|---|---|
| 시각화(플롯·뷰어·애니메이션) | claude opus, medium 기본 | `--kind claude -- --permission-mode auto --model opus --effort medium` |
| 보통 구현·리팩터·테스트 | claude opus medium 또는 codex gpt-6-sol 우선, gpt-5.6-sol도 가능 | `--kind claude -- --permission-mode auto --model opus --effort medium` 또는 `--kind codex -- -m gpt-6-sol -c model_reasoning_effort=<e>` |
| 매우 가벼운 치환·형식 정리 | 작업에 맞는 하위 Claude 모델 또는 codex gpt-6-luna | `--kind claude -- --permission-mode auto --model <확인한-하위-모델>` 또는 `--kind codex -- -m gpt-6-luna -c model_reasoning_effort=<e>` |
| 선행연구 조사·deep research | codex 또는 grok. **opus 금지**. 최신·트렌디한 연구 탐색에는 grok 활용 | `--kind codex -- -m gpt-6-sol -c model_reasoning_effort=<e>` 또는 `--kind grok -- --reasoning-effort high` |
| 긴 맥락 판단·설계·문서 | claude opus, medium 기본 | `--kind claude -- --permission-mode auto --model opus --effort medium` |

Claude opus는 medium이 기본이며, 시각화에도 xhigh를 고정하지 않는다. `opus` alias가 실제로
Opus 5.5를 가리키는지 실행 환경에서 확인한다. GPT effort는 별도로 몫의 난이도에 맞춘다:
단순 치환·형식 정리는 `low`나 `medium`, 보통 구현은 `high`, 설계 판단이 섞인 구현(인터페이스
결정, 수치 안정성)은 `xhigh`. 정한 값은 §7 보고 표의 모델 열에 적는다. Grok은 CLI 기본
모델을 사용하고, 실제 사용된 모델을 확인해 보고 표에 기록한다.

**Workflow 도구.** 팀장이 Claude Code이고, 몫이 파일을 쓰지 않는 병렬 검토·검증·조사(파일
수십 개 훑기, done의 주장마다 근거 대조, 후보 여러 개 독립 평가)면 pane 대신 Workflow 도구를
써도 된다. 이 문장이 그 opt-in이다. 쓰기 전에 `workflow-authoring` 스킬을 읽고, 세션의 크기 지침
안에서, 각 agent에 모델을 opus 이하로 명시한다. 파일을 쓰는 구현 몫은 항상 pane이다.

## 2. 작업 디렉토리와 브리프

git 이력을 더럽히지 않게 프로젝트 밖에 둔다.

```bash
FO="$HOME/.dinnno/fanout/$(date +%Y%m%d-%H%M)-$(basename "$PWD")"
mkdir -p "$FO"
```

몫마다 `$FO/<이름>/brief.md`를 쓴다. 이름은 `impl-loader`, `review-metrics`처럼
무슨 일인지 보이는 kebab-case로 (herdr 에이전트 이름 규칙: `[a-z][a-z0-9_-]{0,31}`, 중복 불가).

브리프가 이 스킬의 심장이다. pane의 에이전트는 이 대화를 하나도 모른다. 아래 일곱 절을
빠짐없이 채운다. 빈 절이 생기면 그건 아직 내가 분해를 덜 한 것이다.

```markdown
# <이름> 인수인계

## 1. 목적지
이 작업이 무엇에 기여하는가. 논문 프로젝트면 thesis의 어느 비교 축을 검증하는지까지.
(예: "메모리 표현 A/B 비교에서 A쪽 학습이 안 돌아가 비교 자체가 미성립인 상태다.")

## 2. 지금 상태
무엇이 되어 있고 무엇이 안 되어 있나. 추상적으로 쓰지 말고 파일 경로와 증상으로.
읽어야 할 파일을 경로로 지목한다. 이미 시도해서 실패한 것이 있으면 그것도.

## 3. 네 몫
정확히 무엇을 하는가. 완료 조건을 검증 가능한 문장으로.
(예: "configs/exp07.yaml로 1 epoch이 끝까지 돌고 metrics.json에 val_loss가 찍힌다.")

## 4. 경계
- 이 작업은 사용자가 이미 승인한 범위 안이다: <승인된 세션 단위 / plan 경로>.
  다시 확인받지 말고 진행한다. 아래 금지 항목만 승인 밖이다.
- 네가 쓰는 파일: <목록>
- 네 출력 경로(실행 결과·metrics·로그): <경로>. 다른 경로에 쓰지 마라.
- 절대 만지지 말 것: 위 목록 밖의 파일 전부. 특히 다른 pane이 동시에 작업 중인 <목록>
- git commit·push 금지. 스테이징도 하지 않는다.
- data/·ckpt/·runs/ 삭제·덮어쓰기 금지. libs/는 읽기 전용.
- 범위 밖 코드가 눈에 거슬려도 고치지 말고 report에 제안으로 적는다.

## 5. 환경
- cwd: <절대경로>
- 실행: <python 명령 / venv 활성화 방법>
- 메모리 상한: `systemd-run --user --scope -p MemoryMax=<배정값>G -- python x.py`
  임의로 올리지 마라. OOM이 나면 `dinnno res`로 이웃 탓인지 먼저 보고, 이웃 탓이면 자리가
  날 때 같은 설정으로 다시 띄운다. 제 몫이 원래 안 들어가면 report에 쓰고 멈춘다.
- GPU 우선. 라이브러리 CPU 커널은 청킹이 없어 큰 중간 텐서를 호스트 RAM에 통째로 만든다.

## 6. 산출물
다 끝나면 <$FO/<이름>/report.md>에 아래 형식으로 쓴다. 이 파일이 내가 읽는 유일한 것이다.
터미널에 길게 요약하지 말고 파일에 쓴다.

    ## 결과
    한 줄 결론.
    ## 바뀐 파일
    - path — 무엇을 왜
    ## 실행한 검증
    명령 / 출력 요약 / 통과 여부. 돌리지 않았으면 "미실행"이라고 쓴다.
    ## 막힌 것·판단이 필요한 것

## 7. 막히면
추측으로 메우지 말 것. 30분 이상 같은 자리에 있거나, 위 경계를 넘어야 풀리는 문제면
거기서 멈추고 report.md에 막힌 지점과 필요한 결정을 쓴다. 미완이어도 그게 더 쓸모 있다.
```

## 3. pane 띄우기

호출한 pane에서 갈라내고 포커스는 사용자에게 남긴다. 넓으면 오른쪽, 좁거나 길면 아래.

```bash
herdr pane layout --pane "$HERDR_PANE_ID"
herdr pane split --current --direction right --cwd "$PWD" --no-focus
```

pane id는 응답에서 꺼낸다. 사이드바 순서나 예시에서 추측하지 않는다.

```bash
PID=$(herdr pane split --current --direction down --cwd "$PWD" --no-focus \
      | python3 -c "import json,sys;print(json.load(sys.stdin)['result']['pane']['pane_id'])")
```

같은 방향으로 반복해서 쪼개면 쓸 수 없이 좁아진다. 3개 이상이면 방향을 번갈아 간다.

```bash
herdr agent start impl-loader --kind codex --pane <pane-id> -- -m gpt-6-sol -c model_reasoning_effort=high
herdr agent start vis-rollout --kind claude --pane <pane-id> -- --permission-mode auto --model opus --effort medium
herdr agent start survey-prior --kind grok --pane <pane-id> -- --reasoning-effort high
```

pane id는 나중에 닫을 때 필요하니 `$FO/<이름>/pane_id`에 적어 둔다.

모델·effort는 §1 표대로 붙인다. Grok의 모델 인자는 생략해 CLI 기본 모델을 사용한다.

claude pane에는 항상 `--permission-mode auto`를 붙인다. 안 붙이면 파일 편집과 셸 실행마다
승인 UI에 걸려 `blocked`가 된다. auto 모드는 git·삭제 같은 위험 명령은 여전히 묻는다(§5).
`--dangerously-skip-permissions`는 그것까지 통과시키므로 쓰지 않는다.

## 4. 일 보내기와 대기

프롬프트는 한 줄이다. 브리프 내용을 여기 옮기지 않는다.

`--wait`를 붙인 prompt를 백그라운드로 동시에 띄우고 셸에서 한 번에 회수한다.

```bash
names=(impl-loader review-metrics); pids=()
for n in "${names[@]}"; do
  herdr agent prompt "$n" "인수인계 파일을 읽고 그 지시대로 작업하라: $FO/$n/brief.md" \
    --wait --timeout 1800000 > "$FO/$n/wait.json" 2>&1 &
  pids+=($!)
done
for i in "${!pids[@]}"; do
  wait "${pids[$i]}" || echo "미완: ${names[$i]} — $(cat "$FO/${names[$i]}/wait.json")"
done
```

인자 없는 `wait`은 자식의 실패를 삼킨다. 타임아웃이나 `agent_prompt_stalled`가 조용히
지나가면 **아직 쓰는 중인 report를 완성본으로 읽게 된다.** 그래서 PID별로 회수한다.

미완으로 찍힌 pane은 `herdr agent get <이름>`으로 상태를 본다. 아직 `working`이면
`herdr agent wait <이름> --timeout ...`으로 이어 기다린다. **완료를 확인하기 전에는
회수·통합·재실행을 시작하지 않는다.**

**보낸 턴을 "보냈다"로 끝내지 않는다.** 보내기부터 회수(§6)와 사용자 보고(§7)까지가 한 동작이다.
위 회수 루프는 Claude Code면 `run_in_background`로 돌린다. 끝나면 런타임이 이 세션을 다시
깨우고, 그때 바로 §6으로 간다. 그런 알림이 없는 런타임(Codex, Grok)은 포그라운드로 기다린다.
사용자가 그사이 다른 이야기를 해도 미회수 몫이 있으면 응답 끝에 한 줄로 상태를 붙인다.
세션이 끊겨도 다음 세션의 `dinnno check`가 미회수 fanout을 보여 준다.

**`--wait` 없이 보내고 나중에 `herdr agent wait`을 부르면 안 된다.** 프롬프트가 도착해
에이전트가 `working`으로 넘어가기 전에 wait이 지금의 `idle`을 보고 즉시 반환한다.
아무것도 안 끝났는데 끝난 것처럼 보인다. 이 스킬을 만들며 실제로 걸린 함정이다.

## 5. blocked 처리

```bash
grep -o '"agent_status":"[a-z]*"' "$FO"/*/wait.json
```

`blocked`면 승인이나 질문 UI에 걸린 것이다. 무엇을 묻는지 본다.

```bash
herdr agent read <이름> --source recent-unwrapped --lines 60
```

**사용자에게 그대로 전달하고 대신 승인하지 않는다.** git·삭제·덮어쓰기·실로봇 명령은
사용자 확인 지점이다.

답을 받으면 **`prompt`가 아니라 `send-keys`로 그 UI에 답한다.** blocked인 에이전트에
`prompt`를 보내면 CLI가 입력을 쓰기도 전에 `agent_blocked`로 거절해서 영영 안 풀린다.

```bash
herdr agent send-keys <이름> down enter   # 선택지에서 고르기
herdr agent send-keys <이름> esc          # 취소·거절
```

키 이름이 `invalid_key`로 거절되면 표기를 바꿔 다시 시도한다. 잘못된 키는 아무 바이트도
쓰지 않고 거절되므로 시도 자체는 안전하다. UI가 풀린 뒤에야 다음 `prompt`를 보낸다.

기다리는 동안 팀장은 자기 몫(취합 준비, 검증 명령 준비)을 한다. 단 브리프에서 pane에
준 파일은 만지지 않는다. 오래 걸리는 작업이면 중간에 사용자에게 상태를 한 줄 알린다.

## 6. 회수와 통합

```bash
cat "$FO"/*/report.md
```

report가 비어 있거나 없을 때만 `herdr agent read`로 화면을 본다.

받은 report를 그대로 믿지 않는다. 팀장이 할 일은 네 가지다.

1. **주장과 산출물을 대조한다.** "검증 통과"라고 쓰여 있으면 그 명령을 팀장이 한 번
   직접 돌린다. 몇 시간짜리 run처럼 재실행이 비현실적이면 metrics·로그 파일과 대조한다.
   둘 다 안 했으면 완료로 쓰지 않는다.
2. **경계를 지켰는지 본다.** `git status`로 브리프에 없던 파일이 바뀌었는지 확인한다.
3. **몫들 사이의 모순을 찾는다.** 각자 맞는데 합치면 안 맞는 경우가 실제로 가장 많다.
   합친 상태에서 plan 게이트나 테스트를 한 번 돌린다. 몫별 검증 통과가 전체 통과는 아니다.
4. **위임 대장에 적는다.** 항상 `$FO/ledger.md`에(진행 중 plan이 있으면 §7 위임 대장에도) pane마다 한 줄: 이름 · 모델 · 브리프 경로 · report 경로 · 팀장이 돌린
   검증 · 통합(반영 / 반려: 사유 / 대기). 통합 열이 빈 행이 남아 있으면 이 fanout은 끝난 것이
   아니고, 사용자 보고에도 그렇게 쓴다. `dinnno check`는 최근 7일 fanout 중 report나 ledger가
   없거나 `대기` 행이 남은 것을 "미회수"로 띄운다. 버린 몫은 `반려: 사유`로 닫는다.

## 7. 보고

pane별로 한 줄씩, 사용자가 다음에 무엇을 결정하면 되는지로 끝낸다.

| pane | 몫 | 모델 | 결과 | 검증 | pane |
|---|---|---|---|---|---|
| impl-loader | 로더 병목 수정 | gpt-6-sol high | 완료 | 팀장이 재실행, 1 epoch 통과 | 닫음 |
| review-metrics | 지표 정의 검토 | opus (Opus 5.5 확인) medium | 판단 필요 | 미실행 (질문 1건) | 열어 둠 |
| survey-prior | 최신 선행연구 조사 | grok (실제 모델 확인 후 기록) | 완료 | 출처 대조 | 닫음 |

## 8. pane 정리

통합이 끝나면 팀장이 판단해서 필요 없는 pane을 닫는다. 사용자에게 묻지 않는다.

닫는다: report를 읽고 §6의 대조까지 마쳐 완료로 확정한 pane, 조사·리뷰처럼 산출물이 report
파일로 다 넘어온 pane.

열어 둔다: `blocked`로 사용자 결정이 남은 pane, 미완이라 이어서 시킬 pane, 사용자가 화면을
직접 보겠다고 한 pane, 실행 로그를 사용자가 봐야 판단이 서는 pane.

```bash
herdr agent get <이름>            # working이면 닫지 않는다
herdr pane close "$(cat "$FO/<이름>/pane_id")"
```

이 스킬이 만든 pane만 닫는다. 어느 pane을 닫고 남겼는지는 위 보고 표의 마지막 열에 적는다.
