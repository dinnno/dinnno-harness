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
# 1회: 전역 행동 규약과 /harness 슬래시 커맨드를 ~/.claude/에 symlink
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
│   └── commands/harness.md  ─────────┤       # symlink (/harness)
│                                      │
└── Workspace/sangjun_noh/for_claude/  │
    ├── dinnno-harness/   ◀───────────┘       # ★ 본체 (1번 클론)
    │   ├── CLAUDE.md, commands/, apply.sh
    │   └── templates/{CLAUDE.md, gitignore, docs/...}
    │
    ├── paper-A/                               # 프로젝트 1 (자체 git)
    │   ├── CLAUDE.md, .gitignore   ← templates cp (자유 편집)
    │   └── docs/{RESEARCH_SPEC, ARCHITECTURE, _GUIDE, progress,
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

## 사용 흐름

1. 새 논문 프로젝트 시작 → `./apply.sh /path/to/proj`
2. `/harness` 진입 → 첫 세션은 자동으로 **(a₀) init 단계**: placeholder 박힌 메타 .md를 사용자와 함께 채움 (프로젝트 루트 `CLAUDE.md` → `ARCHITECTURE.md` → `RESEARCH_SPEC.md` → `progress.md` → `references/_INDEX.md` 순서). 추측 박치기 reject — 사용자 발화 기반만.
3. (a₀) 후: 단위 작업 진입. 단위는 **(a) spec 갱신** 또는 **(experiment) 한 가설** — 가설 내부는 Setup(plan 작성)→Execute(구현·학습)→Verdict(done)로 자연스럽게 흐른다. **한 가설 = 한 세션 = 한 터미널**이 기본. 다음 가설로 자동 chain ❌ (새 가설은 새 터미널).
4. plan 구현 중에는 plan §6 TODO를 working checklist로. 세션 시작 시 첫 미체크 항목부터, 세션 종료 시 체크 갱신 + §5 세션 로그 한 줄.
5. 외부 자료(arxiv/code/homepage)는 `docs/references/_INDEX.md`에 URL만 박아두면 `/harness`가 codex:rescue로 분석 → summary만 메인 세션에 적재.
6. 진척 한눈에 보기: `docs/progress.md` (Phase + Ablation matrix).

## 다이어트 사이클 (월 1회)

1. 사용 중 거추장스러운 가이드라인/줄 발견
2. 본체 `dinnno-harness/`에서 그 줄 삭제 → commit
3. 다음 새 세션부터 전역 즉시 적용 / 새 프로젝트부터 templates 적용

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

이 하네스는 별도 스킬을 박지 않음. Claude Code 빌트인과 marketplace plugin을 활용.

**빌트인 (설치 불필요)**
- `/simplify` — 코드 정리 (dead code, duplicate logic, reuse)
- `/init` — 새 CLAUDE.md 자동 생성
- `/review`, `/security-review` — diff 리뷰

**marketplace plugins (사용자가 직접 설치)**

Claude Code 안에서 `/plugin` 입력 → marketplace에서 검색 → 설치, 또는 `~/.claude/settings.json`의 `enabledPlugins`에 추가:

| Plugin | 용도 | 출처 |
|--------|------|------|
| `claude-md-management` | `/claude-md-improver` (CLAUDE.md 품질 점검), `/revise-claude-md` | `claude-plugins-official` |
| `code-review` | `/code-review` (PR/diff 리뷰) | `claude-plugins-official` |
| `skill-creator` | 필요한 skill을 그때그때 만들 때 | `claude-plugins-official` |
| `claude-code-setup` | `/claude-automation-recommender` (hooks/permissions 자동화 추천) | `claude-plugins-official` |
| `session-report` | 세션 종료 시 작업 리포트 | `claude-plugins-official` |

설치 예시 (`~/.claude/settings.json`):
```json
"enabledPlugins": {
  "claude-md-management@claude-plugins-official": true,
  "code-review@claude-plugins-official": true,
  "skill-creator@claude-plugins-official": true
}
```

## 작성 원칙 (CLAUDE.md / docs)

- **Specific** — 구체적 도구/명령어
- **Structured** — 헤딩·리스트로 스캔 가능
- **Reviewed** — 월 1회 다이어트
- **Concise** — 100줄 이하
=