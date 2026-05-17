# dinnno-harness

로보틱스 AI 연구용 vanilla Claude Code 하네스. 전역 행동 규약 + 논문 단위 프로젝트 골격.

## 설치

```bash
# 1회: 전역 행동 규약과 /harness 슬래시 커맨드를 ~/.claude/에 symlink
./apply.sh --global

# 프로젝트마다: 골격을 깔기 (이미 있는 파일은 skip)
./apply.sh /path/to/paper-project
```

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

별도 스킬을 박지 않음. 다음을 활용:
- `/simplify` — 코드 정리 (dead code, duplicate logic)
- `/init` — 새 CLAUDE.md 자동 생성
- `/claude-md-management` — CLAUDE.md 품질 점검·개선

## 작성 원칙 (CLAUDE.md / docs)

- **Specific** — 구체적 도구/명령어
- **Structured** — 헤딩·리스트로 스캔 가능
- **Reviewed** — 월 1회 다이어트
- **Concise** — 100줄 이하
