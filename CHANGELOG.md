# Changelog

프로젝트 template의 파일명·섹션·status처럼 skill이 직접 참조하는 계약 표면만 기록한다.

## 2026-08-14 — Codex parity refresh through Claude harness 2026-08-10

- `$issue`, `$close`, `$workflow-ops` 3종 신설. 기존 프로젝트 조치: 전역 `./apply.sh --global` 재실행.
- `$harness`에 HARD/SOFT 경계 정본, 조건부 자동 sync, pending reference·누락 계약면 탐지, Codex 아이디어 inbox, 사용자 지적 즉시 LEARNINGS, Setup 최강 대안, 2라운드 리뷰 상한, fresh close, 현재 방향 갱신, GPU/RAM 가드를 통합. 기존 프로젝트 조치: 새 세션부터 전역 skill은 자동 반영.
- `RESEARCH_SPEC.md`에 `현재 방향 (second brain 동기용)` 블록을 추가. 기존 프로젝트 조치: 다음 sync에서 빈 블록만 삽입하고 내용은 프로젝트 세션에서 확정.
- `LEARNINGS.md` 즉시 append 규칙, `progress.md`의 `[codex]` 아이디어 형식, done 외부 리뷰 규칙, references status 정본 포인터, docs 가이드 문서 목록·init 완료 조건을 갱신. 기존 프로젝트 조치: 다음 sync에서 해당 가이드·주석·포인터만 수술적으로 반영.
- 새 프로젝트의 `AGENTS.md` `last-sync:`를 설치 시 현재 CHANGELOG 항목으로 stamp. 기존 프로젝트 조치: 없음.

## 2026-07-15 — Codex native port

- 전역/프로젝트 지침을 `CLAUDE.md`에서 `AGENTS.md`로 변경.
- slash command 5종을 `skills/{name}/SKILL.md`로 변경. 호출 표면은 `/name`에서 `$name`으로 변경.
- Claude 전용 `opus-guide`는 제거하고 핵심 경계·완결성 규칙을 전역 `AGENTS.md`와 `$harness`에 통합.
- `codex:rescue`·Explore·implementer 위임을 Codex의 `research-reviewer`·`explorer`·`implementer` custom/built-in agent로 매핑.
- 외부 리뷰 산출물을 `done_v{N}_codex.md`에서 `done_v{N}_review.md`로 변경.
- audit 인계 산출물을 `HANDOFF_TO_CODEX.md`와 `CHANGELOG_AUDIT.md`로 변경.
- 사용자 설치 경로를 `~/.codex/AGENTS.md`, `~/.agents/skills`, `~/.codex/agents`로 변경.
