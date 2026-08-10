# BACKLOG — 의도적 보류 (월간 다이어트에서 소비)

fresh agent 적대 리뷰(2026-08-08)에서 나온 소형 발견 중 보류분. 다이어트 사이클 때 하나씩 소비하고 지운다.

- [ ] apply.sh가 `templates/CLAUDE.md`의 `{설치일}` placeholder를 채우지 않음 — 신규 프로젝트 첫 세션이 전 CHANGELOG 대조 싱크를 강제당함. sed stamp 1줄이면 해소.
- [ ] plan §3 정지 조건(experiment-level 이상) 도달 후 순서 불명 — "보고·대기 → 사용자 지시로 Verdict 진입"을 어디에든 1줄 명시.
- [ ] done §4 후보 개수 표기 불일치 — done/_GUIDE "1-2개" vs 템플릿·harness "2-3개". "2-3개"로 통일.
- [ ] implementer가 background run 완료를 감지할 수단 없음(tools에 Monitor 부재) — 마커 폴링 규칙 1줄 또는 tools 조정.
- [ ] apply.sh 헤더 주석 stale — "link CLAUDE.md & commands/harness.md"라지만 실제는 커맨드 전체 + agents/.
- [ ] README가 `/claude-md-improver`를 빌트인으로 분류 — 실제는 claude-md-management plugin 소속.
- [ ] init(a₀) 완료 기준 "검출된 placeholder 모두 해소"의 파일 범위 불명 — 트리거와 같은 3개 파일(CLAUDE·SPEC·ARCHITECTURE)로 한정 명시 (progress.md 헤더 `{hash}`는 첫 commit 전 해소 불가).

2차 최종 검증(2026-08-08)에서 추가된 보류분:

- [ ] (sweep)의 "행당 plan §3 루프 예산" 귀속 불명 — sweep 진입 시 얇은 plan 1개(행 목록+행당 예산)를 (autoloop)와 대칭으로 명시.
- [ ] CHANGELOG 07-27 조치문의 위생 스캔 지시가 현행 §1(위생은 /tidy 몫)과 모순 — "(위생 부분은 08-04로 대체)" 괄호 1줄.
- [ ] "§4 라우팅 표"라 부르지만 실제는 산문 — "라우팅 규칙"으로 개칭 또는 실제 표로 (CHANGELOG·README·harness §4).
- [ ] done/_GUIDE "들어가는 것" 목록이 4개인데 템플릿 필수 헤딩은 5개(§5 외부 리뷰) — _GUIDE에 5번 추가.
- [ ] README 자동 반영 표가 `commands/harness.md`만 표기 — 실제는 커맨드 9종 전체 + agents/.
- [ ] 전역 Surgical 예외 목록에 루트 CLAUDE.md "현재 상태" 절 누락 — /tidy §5 대상과 불일치.
- [ ] RESEARCH_SPEC §0 슬롯의 init 시 해소 주체·시점 침묵 — init protocol 3단계에 "§0은 §1 확정 직후 현재값으로 시드" 1줄.
- [ ] 호스트 RAM 가드를 PreToolUse 훅으로 기계적 강제 검토 — 문서 규칙은 서브에이전트 경계를 못 넘는 게 실측(2026-08-10 OOM). 단 정당한 대형 학습을 죽이지 않는 판별식 + `.claude/settings.json` 템플릿 신설(= apply.sh 표면 증가)이 비용.
