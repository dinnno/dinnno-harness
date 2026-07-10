# dinnno-harness

로보틱스 AI 연구용 vanilla Claude Code 하네스. 전역 행동 규약 + 논문 단위 프로젝트 골격.

## Claude Code 설치 (Ubuntu)

```bash
# Node.js 18+ 필요. 미설치 시:
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Claude Code 본체
npm install -g @anthropic-ai/claude-code

# 로그인 (브라우저 띄움)
claude
```

## 하네스 설치

```bash
# 1회: 전역 행동 규약·커맨드 5종·implementer 에이전트를 ~/.claude/에 symlink
./apply.sh --global

# 프로젝트마다: 골격을 깔기 (이미 있는 파일은 skip)
./apply.sh /path/to/paper-project
```

## Claude로 한 줄 설치 (진행 중인 프로젝트에)

진행 중인 프로젝트 디렉토리에서 `claude`를 띄운 뒤 다음을 입력:

```
~/Workspace/sangjun_noh/for_claude/dinnno-harness/apply.sh $(pwd) 실행하고, docs/RESEARCH_SPEC.md 작성 같이 시작하자.
```

→ Claude가 `apply.sh`로 templates를 깔고, 곧바로 RESEARCH_SPEC의 thesis 채우기로 진입.

## 머신당 1번 클론 (본체 모델)

dinnno-harness 본체는 **머신마다 한 번**만 클론. 프로젝트마다 클론하지 않음.

```
~/                                            # 어느 머신이든
├── .claude/
│   ├── CLAUDE.md  ───────────────────┐       # symlink (4원칙 + 도메인)
│   └── commands/*.md  ───────────────┤       # symlink (커맨드 5종)
│                                      │
└── Workspace/sangjun_noh/for_claude/  │
    ├── dinnno-harness/   ◀───────────┘       # ★ 본체 (1번 클론)
    │   ├── CLAUDE.md, commands/, apply.sh
    │   └── templates/{CLAUDE.md, gitignore, docs/...}
    │
    ├── paper-A/                               # 프로젝트 1 (자체 git)
    │   ├── CLAUDE.md, .gitignore   ← templates cp (자유 편집)
    │   └── docs/{RESEARCH_SPEC, ARCHITECTURE, _GUIDE, progress, LOOP,
    │            plans/{_GUIDE, _plan_template, ...},
    │            done/{_GUIDE, _done_template, ...},
    │            references/{_INDEX, _GUIDE, ...}}
    │
    └── paper-B/                               # 프로젝트 2
        └── ...
```

## 본체 → 프로젝트 업데이트 흐름

| 본체에서 바꾼 것 | 자동 반영? | 기존 프로젝트 |
|---|---|---|
| `CLAUDE.md`, `commands/harness.md` | ✓ symlink — 새 세션부터 즉시 | n/a |
| `templates/*` | ✗ 이미 깔린 사본은 영향 없음 | 그 프로젝트에서 `./apply.sh <경로>` 재실행 → `cp -n`이라 **새 파일만** 추가, 기존 사본은 그대로 |
| templates의 **계약 표면** (커맨드가 이름으로 참조하는 파일·섹션) | ✗ | 본체 `CHANGELOG.md`에 한 줄 필수 → 프로젝트는 다음 `/harness` 세션에서 "하네스 업데이트했어" 선언 → 싱크(`/harness` §1) |

싱크 정책 (전체 재정렬 ❌):
- 계약 표면만 맞춘다 — 기본은 프로젝트 `CLAUDE.md`의 `## harness 싱크`에 네이밍 매핑 한 줄, 파일 이관은 매핑이 쌓일 때만.
- 이력·thesis 본문 불가침 — done_v*·옛 plan·RESEARCH_SPEC 서술 재작성 ❌ (stale 배너 주석만).

## 커맨드

| 커맨드 | 언제 쓰나 |
|---|---|
| `/harness` | **모든 세션의 진입점.** 현황(spec·progress·LEARNINGS) 적재 → 단위(init/spec/experiment) confirm → Setup→Execute→Verdict |
| `/opus-guide` | 비-Fable 모델(Opus 4.8 등) 세션에서 `/harness` **직전에** 로드. 행동 보강 델타 레이어(rules-only, 워크플로 시작 ❌) |
| `/add-ref <url>` | 논문·레포 URL을 마주친 **즉시**. `references/_INDEX.md`에 등록만 (fetch·분석 ❌) |
| `/blueprint-ref <name>` | 등록된 자료를 **구현하기로 정했을 때**. codex:rescue로 구현 수준 청사진 생성 |
| `/audit` | 프로젝트 전체 정기 점검·인수인계. **Fable 5 이상 전용** — 검토→인터뷰 합의→HANDOFF 골격 생성→수정(수정마다 갱신)→Opus가 이어받음(중간에 끊겨도 그 지점부터) |

서브에이전트: `agents/implementer.md` (`model: opus`) — plan 확정 후 기계적 구현 위임용. 가이드 세션은 설계·판정만, 구현은 implementer로 (`/harness` §4).

## 자리 비움 모드 (remote)

- 1회 셋업: 세션에서 `/remote-control` 연결(claude.ai 웹/모바일에서 이 세션 모니터링·제어) + 모바일 Claude 앱 로그인 + `/config`에서 "Push when actions required" 토글.
- 이후 긴 run·(sweep) 시작 시 하네스가 전환을 제안하고, opt-in하면 HARD 지점·완료·이상 발생 시 휴대폰 push로 보고받는다 (`/harness` §3).
- 자리 비운 사이 클라우드 실행이 필요하면 `/schedule` routine(스케줄·API 트리거) — 단 로컬 파일 접근 없음(fresh clone) 주의.

## 사용 흐름

1. 새 논문 프로젝트 시작 → `./apply.sh /path/to/proj`
2. `/harness` 진입 → 첫 세션은 자동으로 **(a₀) init 단계**: placeholder 박힌 메타 .md를 사용자와 함께 채움 (프로젝트 루트 `CLAUDE.md` → `ARCHITECTURE.md` → `RESEARCH_SPEC.md` → `progress.md` → `references/_INDEX.md` 순서). 추측 박치기 reject — 사용자 발화 기반만.
3. (a₀) 후: 단위 작업 진입. 단위는 **(a) spec 갱신** 또는 **(experiment) 한 가설** — 가설 내부는 Setup(plan 작성)→Execute(구현·학습)→Verdict(done)로 자연스럽게 흐른다. **한 가설 = 한 세션 = 한 터미널**이 기본. 다음 가설로 자동 chain ❌ (새 가설은 새 터미널).
   - baseline GO 이후 국면에서는 (autoloop) — docs/LOOP.md의 Loop-Ready 체크리스트(L1–L7)로 진단 → gap은 loop-prep으로 채우고 → loop-run(루프 인가 1회 후 밤새 trial 자동 반복, keep/rollback ledger + HTML Loop Report 누적).
4. plan 구현 중에는 plan §6 TODO를 working checklist로. 세션 시작 시 첫 미체크 항목부터, 세션 종료 시 체크 갱신 + §5 세션 로그 한 줄.
5. 외부 자료(arxiv/code/homepage)는 `docs/references/_INDEX.md`에 URL만 박아두면 `/harness`가 codex:rescue로 분석 → summary만 메인 세션에 적재.
6. 진척 한눈에 보기: `docs/progress.md` (Phase + Ablation matrix).

## 다이어트 사이클 (월 1회)

1. 거추장스러운 가이드라인/줄 발견 (또는 `/claude-md-improver`로 CLAUDE.md 감사)
2. 본체 `dinnno-harness/`에서 삭제 → commit
3. 다음 새 세션부터 전역 즉시 / 새 프로젝트부터 templates 적용

## 다중 머신 / 백업

```bash
# 본체에 GitHub remote (1회)
gh repo create dinnno-harness --private --source=. --remote=origin --push

# 다른 머신
git clone <url> ~/Workspace/sangjun_noh/for_claude/dinnno-harness
cd ~/Workspace/sangjun_noh/for_claude/dinnno-harness && ./apply.sh --global

# 동기화
git -C ~/Workspace/sangjun_noh/for_claude/dinnno-harness pull
```

## vanilla 스킬 활용

이 하네스는 별도 스킬을 박지 않음. Claude Code 빌트인 + marketplace plugin 활용.

**빌트인 (설치 불필요)**: `/simplify`(코드 정리), `/init`(CLAUDE.md 생성), `/review`·`/security-review`(diff 리뷰), `/claude-md-improver`(CLAUDE.md 품질 감사 — 월간 다이어트용).

**marketplace plugins**: Claude Code에서 `/plugin`으로 검색·설치. 현재 켠 목록은 `~/.claude/settings.json`의 `enabledPlugins` 참조(이 표를 손으로 동기화하지 않음 — 표류 방지).

## 작성 원칙 (CLAUDE.md / docs)

- **Specific** — 구체적 도구/명령어
- **Structured** — 헤딩·리스트로 스캔 가능
- **Reviewed** — 월 1회 다이어트
- **Concise** — 100줄 이하