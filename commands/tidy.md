---
description: harness 프로젝트에 쌓인 세션 산출물 md 정리 — superseded된 HANDOFF/CHANGELOG 날짜 버전, 소비 완료된 인계 문서, docs/ 직하 loose md를 스캔·분류해 사용자 confirm 후 docs/archive/YYYY-MM/로 이동하고 _INDEX.md에 1줄 요약을 남긴다. 루트에 md가 어지럽거나 "정리", "아카이브", "치워줘" 요청 시 사용. docs/plans/·done/·references/의 버전 history는 건드리지 않는다(그 인덱스는 progress.md).
---

# /tidy — 세션 산출물 아카이브 (스캔 → 분류 → confirm → 이동+인덱스)

세션 산출물(audit 인계본·체인지로그·분석 memo)은 소비되고 나면 루트와 docs/를 어지럽힌다. 이 커맨드는 그것들을 **삭제하지 않고** `docs/archive/`로 옮겨 history로 쌓는다. 판정 기준은 나이가 아니라 **소비 상태**다 — 오래돼도 살아있는 문서가 있고, 어제 것이어도 superseded된 문서가 있다. 이동은 사용자 confirm 후에만 (HARD).

## 1. 스캔 — 후보 수집

대상은 이 두 부류만:

- **루트 세션 산출물** — `HANDOFF_TO_*.md`·`CHANGELOG_*.md`와 그 날짜 suffix 버전, audit/외부 세션이 만든 산출물 폴더(예: `plans_fable/`). `README.md`·`CLAUDE.md`는 제외.
- **docs/ 직하 loose md** — 정규 집합(`RESEARCH_SPEC`·`ARCHITECTURE`·`LEARNINGS`·`progress`·`CLAUDE.md`/`_GUIDE.md`) 밖의 md — survey, deep-dive, 설계 memo 등.

하위 정규 폴더(`docs/plans/`·`done/`·`references/`·`experiments/`·`archive/`)는 스캔 자체를 하지 않는다.

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
- 종료 보고 3줄 이내: 옮긴 n건 / 보류 m건 / 인덱스 경로. **commit ❌** — 커밋 여부·시점은 사용자가 정한다.

## 하지 않는 것

- 삭제 ❌ — 이동만. 실행 전후 파일 총수가 보존돼야 한다.
- `docs/plans/`·`done/`·`references/`·`experiments/` 내부 ❌ — harness가 의도한 history 구조이고 progress.md가 그 인덱스다.
- 정규 현행 문서(`RESEARCH_SPEC`·`progress`·`LEARNINGS`·`ARCHITECTURE`·`README`·`CLAUDE.md`) ❌.
- git commit/push ❌.
- 인덱스 없이 이동 ❌ — _INDEX.md에 착지하지 못한 이동은 정리가 아니라 분실이다.
