# dinnno-harness-codex

로보틱스 AI 연구용 Codex-native 개인 하네스. 전역 행동 규약, 재사용 skill 5종, custom agent 2종, 논문 단위 프로젝트 골격을 제공한다.

이 저장소는 기존 `dinnno-harness`의 독립 복사본에서 변환됐다. 원본 Claude 하네스는 수정하지 않았고, 이 복사본에는 remote도 연결하지 않았다.

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

`--global`은 다음 symlink를 만든다. 기존 일반 파일·디렉토리는 timestamp backup 후 보존한다.

```text
~/.codex/AGENTS.md              -> AGENTS.md
~/.agents/skills/{name}/        -> skills/{name}/
~/.codex/agents/{name}.toml     -> agents/{name}.toml
```

Codex는 시작할 때 `AGENTS.md` instruction chain을 구성한다. 설치나 갱신 뒤에는 새 Codex 세션을 시작한다.

## 프로젝트에 골격 설치

```bash
./apply.sh /path/to/paper-project
cd /path/to/paper-project
codex
```

기존 파일은 덮어쓰지 않는다. 설치 뒤 `docs/RESEARCH_SPEC.md`의 thesis부터 채우고 `$harness`를 호출한다.

진행 중인 프로젝트에서는 Codex에 다음처럼 요청해도 된다.

```text
~/Workspace/sangjun_noh/for_claude/dinnno-harness-codex/apply.sh $(pwd) 실행하고, $harness로 init을 시작해.
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
│   └── tidy/
├── agents/
│   ├── implementer.toml       # 확정 plan의 기계적 구현
│   └── research-reviewer.toml # read-only 독립 검토·대용량 분석
├── templates/
│   ├── AGENTS.md
│   └── docs/...
├── apply.sh
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

Claude custom slash command를 Codex custom prompt로 그대로 옮기지 않았다. custom prompt는 deprecated이므로 공유·암묵 호출·progressive disclosure가 가능한 skill로 변환했다.

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

## 업데이트와 검증

전역 파일과 skill/custom agent는 symlink이므로 이 저장소의 변경이 새 세션부터 반영된다. 프로젝트 template는 복사본이므로 재실행해도 새 파일만 추가된다. 계약 표면 변경은 `CHANGELOG.md`에 기록하고, 프로젝트에서 `$harness` 실행 시 사용자가 "하네스 업데이트했어"라고 선언해 sync한다.

```bash
./verify.sh
git status --short
```

월 1회 `AGENTS.md`와 skill을 다이어트한다. 반복 실수만 규칙으로 승격하고, 일반적인 Codex 능력을 장황하게 재설명하지 않는다.
