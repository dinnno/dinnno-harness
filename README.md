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

## 무엇이 깔리는가

**전역 (`~/.claude/`)** — symlink, 본체 업데이트 자동 전파
- `~/.claude/CLAUDE.md` → 4원칙(Think Before / Simplicity / Surgical / Goal-Driven) + 로보틱스 도메인
- `~/.claude/commands/harness.md` → `/harness` 슬래시 커맨드

**프로젝트 (`/path/to/project/`)** — copy, 자유 편집
- `CLAUDE.md` — 프로젝트 thesis · 현재 plan · 핵심 디렉토리
- `.gitignore` — 로보틱스용 (data/, ckpt/, runs/, wandb/, *.pt, ...)
- `docs/CLAUDE.md` — docs/ 안내
- `docs/RESEARCH_SPEC.md` — 7섹션 spec 양식
- `docs/ARCHITECTURE.md` — configs/src/scripts/libs/data/ckpt 레이아웃
- `docs/plans/CLAUDE.md`, `docs/done/CLAUDE.md` — 폴더별 작성 가이드

## 사용 흐름

1. 새 논문 프로젝트 시작 → `./apply.sh /path/to/proj`
2. `docs/RESEARCH_SPEC.md` 작성 (thesis 채울 때까지)
3. Claude 세션 띄울 때마다 `/harness` 입력 → 현황 파악 후 그 세션의 단위 작업 진입
4. 한 세션 = 한 단위 작업 (spec 갱신 / 새 plan / plan 구현 / done 작성)

## 편집 규칙

- 본체 (`dinnno-harness/`)에서만 편집. 전역 `~/.claude/CLAUDE.md`와 `~/.claude/commands/harness.md`는 symlink — 본체 편집 후 git pull로 자동 전파.
- 프로젝트의 `CLAUDE.md`, `docs/*.md`는 copy이므로 자유 편집. 본체 변경은 새 프로젝트부터 반영.

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
