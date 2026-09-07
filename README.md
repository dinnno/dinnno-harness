# dinnno-harness

로보틱스 AI 연구용 개인 하네스. 한 소스가 Claude Code, Codex, Grok 세 런타임에 같은 규약과 스킬을 준다.

구성은 네 층뿐이다.

| 층 | 파일 | 하는 일 |
|---|---|---|
| 규약 | `AGENTS.md` (1페이지) | 멈추는 지점, 코드 규칙, 보고 스타일. 세 런타임이 같은 파일을 읽는다 |
| 스킬 | `skills/*/SKILL.md` | `harness`(세션 진입) · `close`(근거 확인 후 마감) · `plan-redteam`(다른 모델의 plan 격추) · `loop`(opt-in 반복) + vendored 도구 |
| 스크립트 | `scripts/dinnno` | `check`(상태·크기·싱크) · `gates`(plan 게이트 실행) · `tidy`(산출물 정리) · `review`(다른 모델 검토 호출) |
| 템플릿 | `templates/` | 프로젝트 문서 골격 (spec, architecture, progress, plan/done) |

판단이 필요한 일은 스킬(산문)에, 답이 정해진 일은 스크립트에 둔다. 세션 시작 훅이 `dinnno check`를 자동으로 돌린다. `dinnno review --unsafe`는 git이 추적하는 변경과 새로 생긴 파일은 잡지만, 추적하지 않는 파일의 삭제까지는 잡지 못한다.

## 설치

```bash
./apply.sh --global                 # 머신당 1회. 세 런타임에 규약·스킬·CLI·훅 연결
./apply.sh /path/to/paper-project   # 프로젝트마다. 기존 파일은 건드리지 않음
```

`--global`이 만드는 것:

| 대상 | Claude Code | Codex | Grok |
|---|---|---|---|
| 규약 | `~/.claude/CLAUDE.md` | `~/.codex/AGENTS.md` | `~/.grok/AGENTS.md` |
| 스킬 | `~/.claude/skills/*` | `~/.agents/skills/*` | `~/.grok/skills/*` |
| 훅 | `~/.claude/settings.json` | `~/.codex/hooks.json` (새 훅은 경고 후 trust 전까지 실행되지 않으니 새 세션에서 `/hooks`로 dinnno 훅을 trust. 구버전은 `[features] hooks = true` 필요) | `~/.grok/config.toml` (훅 출력이 컨텍스트에 들어가는지는 Grok 세션에서 미검증) |
| CLI | `~/.local/bin/dinnno` | 동일 | 동일 |

호출 이름: Claude·Grok `/harness`, Codex `$harness`. 프로젝트 안의 `CLAUDE.md`는 `@AGENTS.md` 한 줄이라 세 런타임이 같은 프로젝트 규약을 읽는다.

`ponytail`(최소 코드 사다리)은 기본으로 연결하지 않는다. 원하면 `./apply.sh --global --with-ponytail`.

## 세션 흐름

1. 세션 시작. 훅이 `[dinnno]` 줄로 크기 경고, placeholder, 미동기 CHANGELOG, 미결 결정을 보여준다.
2. `harness` 스킬이 SPEC, ARCHITECTURE, progress 표, 현재 plan만 읽고 단위 하나를 확인한다.
3. plan(게이트 표 포함) → 실행 → done. 큰 설계면 실행 전에 `plan-redteam`. 게이트에는 정의 해시가 붙어 결과를 본 뒤 기준을 고치면 이전 PASS가 무효가 되고, 사람이 봐야 하는 것은 `MANUAL:` 게이트로 적어 사용자 확인 발화가 있어야 PASS가 된다.
4. 마감은 `close`. `dinnno gates`가 게이트를 돌리고 fresh 검토자가 done의 근거를 확인한다.

멈추는 지점은 다섯 개다: git commit/push, 데이터·ckpt 삭제, 실로봇 명령, thesis·축 변경, kill 결론. 여기에 harness 스킬의 두 확인(이번 세션 단위, plan 실행 시작)이 더해진다. 나머지는 완주.

## 본체 갱신 → 프로젝트 반영

규약·스킬·스크립트는 symlink라 새 세션부터 바로 적용된다. 템플릿의 계약 표면(파일명·절 이름)이 바뀌면 `CHANGELOG.md`에 한 줄 적는다. 프로젝트 `AGENTS.md`의 `last-sync:` 뒤에 새 항목이 있으면 `dinnno check`가 알려주고, 반영은 세션이 confirm 받아 한다. RESEARCH_SPEC·plan·done 본문은 싱크가 건드리지 않는다.

## 기존 프로젝트를 v4로

1. `git mv CLAUDE.md AGENTS.md && echo '@AGENTS.md' > CLAUDE.md`
2. `docs/LEARNINGS.md`를 "현재 유효"(20줄 이내) / "이력"으로 나눈다.
3. `docs/progress.md`에 쌓인 세션 로그·결정 큐 이력은 세션이 confirm 받아 `docs/archive/rollup_YYYY-MM.md`로 옮긴다. `dinnno tidy`는 파일 단위 이동만 하고 파일 안을 자르지는 않는다.
4. 다음 plan부터 §3 게이트 표를 쓴다.

## Vendored 스킬

`bro`, `codebase-design`, `diagnosing-bugs`, `improve`, `improve-codebase-architecture`, `thermo-nuclear-code-quality-review`, `ponytail`. 출처·핀·라이선스는 `skills/UPSTREAM.md`. `research-second-brain`(문헌 위키 조회)은 자체 제작 스킬로 세 런타임에 같이 연결된다.

## 다른 머신

```bash
git clone <url> ~/Workspace/dinnno-research-wrapper/tools/dinnno-harness
cd ~/Workspace/dinnno-research-wrapper/tools/dinnno-harness && ./apply.sh --global
```
