# CHANGELOG — 계약 표면 변경 로그

**계약 표면**(templates의 파일명·섹션 헤더·상태값 등 commands/*.md가 이름으로 참조하는 것 + 세션 진입 시 자동 수행되는 커맨드 행동)이 바뀔 때만 한 줄 기록 (일반 변경은 git log로 충분). `/harness` §1 싱크 스텝이 이 파일을 읽는다.

형식: `날짜 — 무엇이 바뀜 — 기존 프로젝트 조치: 없음 | 매핑 한 줄 | 이관 | 기타 한 줄`

- 2026-07-10 — 하네스 싱크 도입: `templates/CLAUDE.md`에 `## harness 싱크` 섹션(last-sync 마커 + 네이밍 매핑) 신설 — 조치: 첫 싱크 때 루트 CLAUDE.md에 섹션 자동 추가
- 2026-07-27 — Opus 5 라우팅 개편: `/harness` §1 싱크 선언식→자동 체크 + 산출물 위생 스캔, §4에 모델·effort 라우팅 표 흡수(`CLAUDE-FABLE-5.md` 폐기), `/workflow-ops` 신설, `/opus-guide`에 Opus 5 분기(§1.5 델타), implementer `effort: high` — 조치: 다음 `/harness` 진입 시 자동 싱크가 `last-sync:` 마커 신설을 제안(루트 HANDOFF·날짜 suffix 산출물이 있으면 상태 정정·`/tidy` 제안 포함); 타 머신은 pull 후 `./apply.sh --global` 재실행(신규 `/workflow-ops` 심링크)
- 2026-07-29 — second brain 동기 슬롯: `templates/docs/RESEARCH_SPEC.md`에 `## 0. 현재 방향 (second brain 동기용)` 신설 + `/harness` §5에 "thesis 움직였으면 §0 갱신" 한 줄 — 조치: 다음 싱크 때 **빈 슬롯만** 삽입(placeholder `{...}` 포함 = §1 불가침의 '형식' 변경이라 저촉 ❌, **내용 작성은 그 프로젝트 세션 몫** — 싱크가 방향을 추측해 채우지 말 것). vault 미설치 머신은 빈 채로 두면 됨(읽는 쪽이 없을 뿐 무해)
- 2026-08-08 — 경계선(HARD/SOFT) 정본 이관: `/opus-guide` §1 Boundary Map → `/harness` §경계선(모델 무관 공통 계약, 압축 이관) + README에 사용자용 요약 표. `/opus-guide` §1은 포인터 스텁, Fable 세션은 opus-guide 로드 불필요로 명시 — 조치: 없음(커맨드 symlink 즉시 반영)
- 2026-08-08 — `/issue` 신설: 뫼비우스(고민·수정 순환) 박제 → vault `fable/issues/YYYY-MM-DD_{프로젝트}_{slug}.md` (+ vault CLAUDE.md에 fable/ 레이어 등재), `/harness` §2에 제안 트리거 1줄 — 조치: 타 머신은 pull 후 `./apply.sh --global` 재실행(신규 심링크), vault도 pull
- 2026-08-04 — 세션 계약 재배치: 세션 종료 계약·종료 보고(verdict 1줄+기승전결)·AFK push를 `/opus-guide` §2·§6·§7 → `/harness` §3·§5로 이관(모델 무관 계약 — 7/27 개편 후 Opus 5+/Fable 세션에 미로드되던 회귀 수정), 진입 싱크는 조건부(CHANGELOG에 last-sync보다 새 항목 있을 때만)·진입 시 산출물 위생 스캔 제거(`/tidy` 몫), `/harness` §4 Workflow 기본 고려의 Fable 한정 해제, 외부 리뷰 2라운드 confirm 규칙 §4로 이동, opus-guide 구§8→§7 — 조치: 없음(커맨드 symlink 즉시 반영, templates 불변)
