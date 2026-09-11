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

이 스킬을 부르는 세션이 그 프로젝트의 **팀장**이고, pane의 에이전트가 팀원이다. 팀장이 구현까지
하면 컨텍스트가 빠르게 녹는다. 이 스킬은 역할을 나눈다:
**팀장은 분해·브리프·감독·취합·검토를 하고, 구현 토큰은 pane의 codex나 opus가 쓴다.**
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

실패하면 herdr 밖이라고 말하고 멈춘다. 다른 방식으로 대체하지 않는다.

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

pane 수를 정한 직후 **메모리 예산을 나눈다.** pane마다 8G를 잡으면 4개일 때 32G이고,
호스트 RAM은 옆 세션과 공유라 OOM 하나가 그 데스크톱의 세션 전부를 죽인다.

```bash
free -g | awk '/Mem:/{print "available:", $7"G"}'
```

상한의 합이 가용의 절반을 넘지 않게 나누고, 그 값을 각 브리프에 적는다. 실행이 없는
몫(문서·리뷰)은 예산에서 뺀다.

### 모델 배정

팀장(Fable 5.1 high 또는 gpt-6-astra medium)은 **구현하지 않는다.** 분해·브리프·감독·
검토·질문 응대·가이드만 한다. 구현 토큰은 전부 pane이 쓴다.

pane의 모델은 사용자 지정이 우선이고, 없으면 몫의 종류로 정한다.

| 몫 | 모델 | `herdr agent start` 뒤에 붙이는 인자 |
|---|---|---|
| 시각화(플롯·뷰어·애니메이션) | claude opus xhigh | `--kind claude -- --model opus --effort xhigh` |
| 보통 구현·리팩터·테스트 | claude opus 또는 codex gpt-5.6-sol. effort는 아래 기준 | `--kind claude -- --model opus --effort <e>` 또는 `--kind codex -- -m gpt-5.6-sol -c model_reasoning_effort=<e>` |
| 선행연구 조사·deep research | codex 또는 grok. **opus 금지** | `--kind codex -- -m gpt-5.6-sol -c model_reasoning_effort=high` 또는 `--kind grok -- -m grok-4.6 --reasoning-effort high` |
| 긴 맥락 판단·설계·문서 | claude opus | `--kind claude -- --model opus` |

effort는 몫마다 정한다. 단순 치환·형식 변환·스크립트 하나면 `low`나 `medium`, 보통 구현은
`high`, 설계 판단이 섞인 구현(인터페이스 결정, 수치 안정성)은 `xhigh`. 정한 값은 §7 보고 표의
모델 열에 적는다. 시각화의 opus xhigh는 내리지 않는다.

**Workflow 도구.** 팀장이 Claude Code이고, 몫이 파일을 쓰지 않는 병렬 검토·검증·조사(파일
수십 개 훑기, done의 주장마다 근거 대조, 후보 여러 개 독립 평가)면 pane 대신 Workflow 도구를
써도 된다. 이 문장이 그 opt-in이다. 쓰기 전에 `workflow-authoring` 스킬을 읽고, 크기 지침
(15 agents) 안에서, 각 agent에 모델을 opus 이하로 명시한다. 파일을 쓰는 구현 몫은 항상 pane이다.

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
  이 값은 지금 동시에 도는 pane 수로 나눠 배정한 것이다. 임의로 올리지 마라. 더 필요하면
  report에 쓰고 멈춘다. (호스트 RAM은 다른 세션과 공유다. OOM 하나가 그 데스크톱 세션
  전부를 죽인다.)
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
herdr agent start impl-loader --kind codex --pane <pane-id> -- -m gpt-5.6-sol -c model_reasoning_effort=high
herdr agent start vis-rollout --kind claude --pane <pane-id> -- --model opus --effort xhigh
herdr agent start survey-prior --kind grok --pane <pane-id> -- -m grok-4.6 --reasoning-effort high
```

pane id는 나중에 닫을 때 필요하니 `$FO/<이름>/pane_id`에 적어 둔다.

모델·effort는 §1 표대로 붙인다. 붙이지 않으면 각 CLI의 기본값(코덱스는 `~/.codex/config.toml`)이 쓰인다.

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
   직접 돌린다. 돌리지 않은 검증은 완료로 쓰지 않는다.
2. **경계를 지켰는지 본다.** `git status`로 브리프에 없던 파일이 바뀌었는지 확인한다.
3. **몫들 사이의 모순을 찾는다.** 각자 맞는데 합치면 안 맞는 경우가 실제로 가장 많다.
   합친 상태에서 plan 게이트나 테스트를 한 번 돌린다. 몫별 검증 통과가 전체 통과는 아니다.
4. **위임 대장에 적는다.** 진행 중 plan이 있으면 그 파일의 "위임 대장" 절에, 없으면
   `$FO/ledger.md`에 pane마다 한 줄: 이름 · 모델 · 브리프 경로 · report 경로 · 팀장이 돌린
   검증 · 통합(반영 / 반려: 사유 / 대기). 통합 열이 빈 행이 남아 있으면 이 fanout은 끝난 것이
   아니고, 사용자 보고에도 그렇게 쓴다.

## 7. 보고

pane별로 한 줄씩, 사용자가 다음에 무엇을 결정하면 되는지로 끝낸다.

| pane | 몫 | 모델 | 결과 | 검증 | pane |
|---|---|---|---|---|---|
| impl-loader | 로더 병목 수정 | sol high | 완료 | 팀장이 재실행, 1 epoch 통과 | 닫음 |
| review-metrics | 지표 정의 검토 | opus medium | 판단 필요 | 미실행 (질문 1건) | 열어 둠 |

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
