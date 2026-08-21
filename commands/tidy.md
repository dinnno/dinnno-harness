---
description: harness 프로젝트에 쌓인 세션 산출물 md 정리 — superseded된 HANDOFF/CHANGELOG 날짜 버전, 소비 완료된 인계 문서, docs/ 직하 loose md, 소비 완료된 docs/notes/, 정규 집합 밖 비정규 폴더를 스캔·분류해 사용자 confirm 후 docs/archive/YYYY-MM/로 이동하고 _INDEX.md에 1줄 요약을 남긴다. 현행 문서(progress·CLAUDE.md) 안의 낡은 줄 정리는 §5 stale 검사, 정본(progress·LEARNINGS) 50K 초과 시 롤링은 §6 다이어트 패스. 루트에 md가 어지럽거나 "정리", "아카이브", "치워줘", "낡은 기록이 새어든다" 요청 시 사용. docs/plans/·done/·references/의 버전 history는 건드리지 않는다(그 인덱스는 progress.md). 수개월치 축적이 스캔 범위를 넘으면 /deep-clean.
---

# /tidy — 세션 산출물 아카이브 (스캔 → 분류 → confirm → 이동+인덱스)

세션 산출물(audit 인계본·체인지로그·분석 memo)은 소비되고 나면 루트와 docs/를 어지럽힌다. 이 커맨드는 그것들을 **삭제하지 않고** `docs/archive/`로 옮겨 history로 쌓는다. 판정 기준은 나이가 아니라 **소비 상태**다 — 오래돼도 살아있는 문서가 있고, 어제 것이어도 superseded된 문서가 있다. 이동은 사용자 confirm 후에만 (HARD).

## 1. 스캔 — 후보 수집

대상은 이 네 부류:

- **루트 세션 산출물** — `HANDOFF_TO_*.md`·`CHANGELOG_*.md`와 그 날짜 suffix 버전, audit/외부 세션이 만든 산출물 폴더(예: `plans_fable/`). `README.md`·`CLAUDE.md`는 제외.
- **docs/ 직하 loose md** — 정규 집합(`RESEARCH_SPEC`·`ARCHITECTURE`·`LEARNINGS`·`progress`·`LOOP`·`CLAUDE.md`/`_GUIDE.md`) 밖의 md — survey, deep-dive, 설계 memo 등.
- **docs/notes/** — 소비 완료된 산출물(notes는 태어날 때부터 아카이브 후보인 방 — 착지 규약은 `/harness` §4·`notes/_GUIDE.md`). 미소비(현행 문서가 아직 참조)만 남긴다.
- **비정규 폴더** — docs/ 직하의 정규 집합 밖 폴더(예: `legacy/`, `work-plans/`). **폴더 단위**로 후보에 올린다 — 내부 파일 개별 판정 ❌, 통째 이동이 기본. 내부가 크거나(수십 파일) 판정이 무거우면 `/deep-clean`으로 넘긴다.

하위 정규 폴더 중 `docs/plans/`·`done/`·`references/`·`experiments/`·`archive/`는 스캔 자체를 하지 않는다(`notes/`는 스캔 ✓).

## 2. 분류 — 상태 기반 판정

각 후보에 셋 중 하나 + 근거 한 줄. **파일명만으로 판정 ❌ — 내용을 열어 확인한다.**

- **superseded** — 같은 계열의 더 최신 현행본이 존재. 날짜 suffix 파일(`HANDOFF_TO_OPUS_2026-07-03.md` 옆에 현행 `HANDOFF_TO_OPUS.md`)이 전형.
- **consumed** — 목적을 다함. HANDOFF는 수정 큐 전 항목 `done`(+대응 CHANGELOG 반영), plan 세트는 전부 실행/폐기 확인.
- **stale** — 현행 문서 어디서도 참조되지 않고(grep으로 확인), 내용이 정규 문서(spec·progress·done·LEARNINGS)에 흡수됐거나 낡음. 오래 안 건드린 것(mtime)은 보조 신호일 뿐 단독 근거 ❌.

판정 확신이 없으면 후보에서 빼지 말고 **"보류 제안"으로 분리**해 표에 함께 올린다 — 애매한 것은 치우는 것보다 남기는 게 싸다. 현행본(예: `pending` 항목이 남은 HANDOFF)은 어떤 분류로도 후보 ❌.

## 3. Confirm (HARD)

표로 제시: 파일 / 분류 / 근거 한 줄 / 마지막 수정일. 사용자가 확정한 것만 이동 — 일괄 승인·부분 승인·전체 보류 모두 가능. confirm 없이 이동 시작 ❌.

## 4. 실행 — 이동 + 인덱스

- 이동 **전에** 각 파일을 읽어 한 줄 요약을 확보한다 — 무엇이었고 어떻게 소비됐는지. (요약이 인덱스의 값어치다: 경로만 남기면 결국 파일을 다시 열게 된다.)
- 이동: `docs/archive/YYYY-MM/` (파일 마지막 수정 월 기준). git 추적 파일은 `git mv`, 아니면 `mv`. 폴더 산출물은 통째로. 이름 충돌 시 날짜 suffix.
- `docs/archive/_INDEX.md` 갱신 — 월 섹션(`## 2026-07`) 아래 파일당 1줄, 최신이 위:

  ```
  - `원경로` → `새경로` — {superseded|consumed|stale} · 한 줄 요약
  ```

- 참조 무결성: 현행 문서가 이동한 파일을 참조하면(grep) 링크를 새 경로로 갱신. 갱신이 애매하면 고치지 말고 보고만.
- 종료 보고: 옮긴 n건 / 보류 m건 / 인덱스 경로. **commit ❌** — 커밋 여부·시점은 사용자가 정한다.

## 5. Stale 검사 — 살아있는 문서 안의 낡은 줄 (선택 패스)

§1–§4가 파일을 옮긴다면, 이 패스는 **현행 문서 안의 낡은 서술**을 찾는다 — 낡은 줄은 매 세션 로드되며 현재 판단에 새어든다. 사용자가 요청하거나 §4 종료 후 후보가 보이면 1줄 제안으로 발동.

- **대상**: `progress.md`(헤더 Stage·anchored commit이 타임라인과 어긋남 · 소비 완료됐는데 미체크인 결정 큐 항목 · 낡은 Open 부채) · 루트 `CLAUDE.md`(`## 현재 상태` 절이 실제 최신 plan/done과 다름) · `references/_INDEX.md`(끝난 단위 전용이었는데 pending으로 남은 행) · `docs/**/_GUIDE.md`·폴더 `CLAUDE.md`(커맨드 정본과 어긋난 규칙 줄 — 판정은 `/harness` 해당 절과 대조).
- **불가침**: `RESEARCH_SPEC` 본문·`done_v*`·옛 plan 서술 — spec은 stale 배너 주석 추가까지만.
- **판정은 문서 간 대조로만**: progress 헤더 vs 타임라인 마지막 행, CLAUDE.md 상태 절 vs `plans/`·`done/` 실제 최신 v{N}, 결정 큐 항목 vs Phase/Matrix 흡수 여부. mtime·감으로 판정 ❌.
- 표 제시(문서 / 해당 줄 / stale 근거 / 제안: 갱신·체크·삭제) → **confirm(HARD)** → 반영. 확신 없으면 "보류 제안"으로 분리 — §2와 같은 원칙.

## 6. 정본 다이어트 — 크기 규율 (선택 패스)

정본(progress·LEARNINGS)이 임계(≈50K)를 넘으면 발동 제안 — `/harness` §1 적재 경고와 짝이다. 파일을 옮기는 게 아니라 **정본 안의 초과분을 롤링**한다.

- **progress.md**: 헤더 Stage 줄은 현재 상태만 — 이력 서술·폐기된 ~~취소선~~ 경고·세션 로그 초과분(최근 ~20행 밖)을 롤링. 대상은 **템플릿 밖에서 증식한 서술 블록만** — 타임라인 표·Ablation Matrix는 불가침(이 파일의 본연 기능).
- **LEARNINGS.md**: 중복·정규 문서에 흡수된 교훈을 통폐합(원문은 롤링 파일에 보존), "한 줄 200자" 규약 재적용.
- 롤링 파일 = `docs/archive/rollup_YYYY-MM.md`(롤링 실행 월, progress·LEARNINGS 공용). 신설·추가분은 `_INDEX.md`에 1줄 기재(§4와 동일) — 파일 신설은 "총수 보존" 원칙의 명시적 예외다(내용 보존 이동).
- done 결번 세대가 헤더에 역류해 있으면 여기서 자르지 않는다 — 소급 회수는 `/deep-clean` 몫, 1줄 보고만.
- 표 제시 → **confirm(HARD)** → 반영. 불가침(§5와 동일: `RESEARCH_SPEC` 본문·`done_v*`·옛 plan 서술) 준수.

## 하지 않는 것

- 삭제 ❌ — 이동만. 실행 전후 파일 총수가 보존돼야 한다(§6 롤링 파일 신설만 예외 — 내용 보존 이동).
- `docs/plans/`·`done/`·`references/`·`experiments/` 내부 ❌ — harness가 의도한 history 구조이고 progress.md가 그 인덱스다 (폴더 가이드의 낡은 규칙 줄 정리만 §5 패스가 confirm 받아 수행).
- 정규 현행 문서(`RESEARCH_SPEC`·`progress`·`LEARNINGS`·`ARCHITECTURE`·`LOOP`·`README`·`CLAUDE.md`)의 **이동·아카이브** ❌ (안의 낡은 줄 정리는 §5, 초과분 롤링은 §6 패스가 confirm 받아 수행).
- git commit/push ❌.
- 인덱스 없이 이동 ❌ — _INDEX.md에 착지하지 못한 이동은 정리가 아니라 분실이다.
