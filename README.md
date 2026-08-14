# dinnno-harness-codex

로보틱스 AI 연구용 Codex-native 개인 하네스. 전역 행동 규약, 재사용 skill 8종, custom agent 2종, 논문 단위 프로젝트 골격을 제공한다.

이 저장소는 `dinnno-harness`의 Codex 포트다. 2026-08-10 원본의 경계·문서 위생·issue/close·장시간 실행·GPU/RAM 규율까지 Codex 방식으로 동기화했다.

## 설치

Codex CLI가 없다면 설치하고 로그인한다.

```bash
npm install -g @openai/codex
codex login
```

하네스를 사용자 범위에 설치한다.

```bash
./apply.sh --global
./verify.sh
```

Windows Codex에서는 PowerShell 설치기를 쓴다.

```powershell
./apply.ps1 -Global
bash ./verify.sh
```

PowerShell 설치기는 symbolic link를 먼저 시도하고, 권한이 없으면 skill 디렉터리는 junction, 단일 파일은 hardlink로 연결한다.

`--global`은 다음 symlink를 만든다. 기존 일반 파일·디렉토리는 timestamp backup 후 보존한다.

```text
~/.codex/AGENTS.md              -> AGENTS.md
~/.agents/skills/{name}/        -> skills/{name}/
~/.codex/agents/{name}.toml     -> agents/{name}.toml
```

Codex는 시작할 때 `AGENTS.md` instruction chain을 구성한다. skill 변경은 자동 감지되지만 목록에 안 보이면 새 Codex 세션을 시작한다.

## 프로젝트에 골격 설치

```bash
./apply.sh /path/to/paper-project
cd /path/to/paper-project
codex
```

기존 파일은 덮어쓰지 않는다. 설치 뒤 `docs/RESEARCH_SPEC.md`의 thesis부터 채우고 `$harness`를 호출한다.

진행 중인 프로젝트에서는 Codex에 다음처럼 요청해도 된다.

```text
~/Workspace/dinnno-research-wrapper/tools/dinnno-harness-codex/apply.sh $(pwd) 실행하고, $harness로 init을 시작해.
```

## Codex 구조

```text
dinnno-harness-codex/
├── AGENTS.md                  # 사용자 전역 행동 규약
├── skills/                    # Codex reusable workflows
│   ├── harness/
│   ├── audit/
│   ├── add-ref/
│   ├── blueprint-ref/
│   ├── tidy/
│   ├── issue/
│   ├── close/
│   └── workflow-ops/
├── agents/
│   ├── implementer.toml       # 확정 plan의 기계적 구현
│   └── research-reviewer.toml # read-only 독립 검토·대용량 분석
├── templates/
│   ├── AGENTS.md
│   └── docs/...
├── apply.sh
├── apply.ps1                    # Windows 사용자 범위 설치
└── verify.sh
```

## Skills

Codex CLI/IDE에서 `$`로 명시 호출하거나, 요청이 description과 맞으면 Codex가 암묵 호출한다.

| skill | 용도 |
|---|---|
| `$harness` | 모든 research 세션의 진입점. 상태 적재 → 단위 확인 → Setup/Execute/Verdict |
| `$add-ref` | 논문·레포 URL을 `_INDEX.md`에 등록만 함 |
| `$blueprint-ref` | 등록 자료를 구현 수준 청사진으로 분석 |
| `$audit` | 프로젝트 전체 감사 → 사용자 합의 → 수정 → durable handoff |
| `$tidy` | 소비 완료된 세션 산출물을 삭제 없이 archive |
| `$issue` | 반복되는 막힘을 second-brain vault에 박제하고 fresh context로 인계 |
| `$close` | fresh read-only subagent가 목표 대비 산출물을 검증한 뒤 세션 종료 계약 수행 |
| `$workflow-ops` | sweep·병렬 Execute·장시간 run의 메모리 상한·모니터링·영구 산출물 규율 |

Claude custom slash command를 Codex custom prompt로 그대로 옮기지 않았다. 공유·암묵 호출·progressive disclosure가 가능한 skill로 변환했다. Codex의 skill 위치와 custom-agent TOML 형식은 공식 문서의 현재 규약을 따른다: [Build skills](https://learn.chatgpt.com/docs/build-skills), [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md).

## 기본 연구 흐름

1. 새 프로젝트에 template 설치.
2. `$harness`로 init: `AGENTS.md` → `ARCHITECTURE.md` → `RESEARCH_SPEC.md` → `progress.md` → references.
3. 한 가설을 Setup(plan) → Execute(구현·학습) → Verdict(done)로 완료.
4. plan §6과 §5 로그, done 뒤 `progress.md`를 같은 세션에서 갱신.
5. 다음 가설은 자동으로 이어가지 않고 새 세션에서 다시 `$harness`로 시작.

working baseline 이후에는 `docs/LOOP.md`의 L1–L7을 채운 뒤, 승인된 allowlist와 budget 안에서 autoloop를 수행할 수 있다.

## 원본과의 주요 매핑

| Claude 하네스 | Codex 하네스 |
|---|---|
| `CLAUDE.md` | `AGENTS.md` |
| `/command` Markdown | `.agents/skills`에 설치되는 `SKILL.md` |
| Claude subagent Markdown | `~/.codex/agents/*.toml` custom agent |
| `codex:rescue` 외부 위임 | read-only `research-reviewer` subagent |
| Fable/Opus 모델 델타 | 모델명 비종속 경계 규칙 + Codex native delegation |
| `done_vN_codex.md` | `done_vN_review.md` |
| `/issue`, `/close`, `/workflow-ops` | `$issue`, `$close`, `$workflow-ops` |

## 업데이트와 검증

전역 파일과 skill/custom agent는 symlink이므로 이 저장소의 변경이 반영된다. 프로젝트 template는 복사본이므로 재실행해도 새 파일만 추가된다. 계약 표면 변경은 `CHANGELOG.md`에 기록하고, 프로젝트의 `$harness`는 `AGENTS.md` `last-sync:`보다 새 항목이 있을 때만 구조·포인터 차이를 자동 제안한다. thesis와 과거 plan/done 본문은 동기화 대상이 아니다.

```bash
./verify.sh
git status --short
```

월 1회 `AGENTS.md`와 skill을 다이어트한다. 반복 실수만 규칙으로 승격하고, 일반적인 Codex 능력을 장황하게 재설명하지 않는다.
