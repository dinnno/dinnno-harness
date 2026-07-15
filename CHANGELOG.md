# Changelog

프로젝트 template의 파일명·섹션·status처럼 skill이 직접 참조하는 계약 표면만 기록한다.

## 2026-07-15 — Codex native port

- 전역/프로젝트 지침을 `CLAUDE.md`에서 `AGENTS.md`로 변경.
- slash command 5종을 `skills/{name}/SKILL.md`로 변경. 호출 표면은 `/name`에서 `$name`으로 변경.
- Claude 전용 `opus-guide`는 제거하고 핵심 경계·완결성 규칙을 전역 `AGENTS.md`와 `$harness`에 통합.
- `codex:rescue`·Explore·implementer 위임을 Codex의 `research-reviewer`·`explorer`·`implementer` custom/built-in agent로 매핑.
- 외부 리뷰 산출물을 `done_v{N}_codex.md`에서 `done_v{N}_review.md`로 변경.
- audit 인계 산출물을 `HANDOFF_TO_CODEX.md`와 `CHANGELOG_AUDIT.md`로 변경.
- 사용자 설치 경로를 `~/.codex/AGENTS.md`, `~/.agents/skills`, `~/.codex/agents`로 변경.
