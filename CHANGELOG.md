# CHANGELOG — 계약 표면 변경 로그

templates의 파일명·섹션 헤더·상태값 등 **commands/*.md가 이름으로 참조하는 것**이 바뀔 때만 한 줄 기록 (일반 변경은 git log로 충분). `/harness` §1 싱크 스텝이 이 파일을 읽는다.

형식: `날짜 — 무엇이 바뀜 — 기존 프로젝트 조치: 없음 | 매핑 한 줄 | 이관`

- 2026-07-10 — 하네스 싱크 도입: `templates/CLAUDE.md`에 `## harness 싱크` 섹션(last-sync 마커 + 네이밍 매핑) 신설 — 조치: 첫 싱크 때 루트 CLAUDE.md에 섹션 자동 추가
