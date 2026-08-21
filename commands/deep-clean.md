---
description: 문서 비대가 /tidy 수용량을 넘은 harness 프로젝트의 1회성 대청소 캠페인 — 사체 폴더·superseded 인계문서·plans 고아·바이트 동일 중복·git 안 바이너리 자산을 조사→분류→confirm→archive 이동(md5 재검증한 중복만 삭제 — 유일 예외)하고, 정본(progress·LEARNINGS) 다이어트와 done 결번 소급 회수까지 수행한다. 프로젝트당 별도 세션 1회. 일상 유지보수는 /tidy — 이 커맨드는 그 범위를 넘은 축적을 리셋할 때만.
---

# /deep-clean — 1회성 대청소 (조사 → 분류 confirm → 실행 → 검증)

`/tidy`가 일상 유지보수라면 이건 리셋이다. 수개월치 축적(사체 폴더·리뷰 파편·정본으로 역류한 이력)은 /tidy 관할 밖이라 이 캠페인으로만 풀린다. 원칙은 /tidy와 동일 — **삭제 ❌ 이동+인덱스, 모든 실행은 confirm 후.** 유일한 삭제 예외는 바이트 동일 중복(md5 재검증)뿐.

## 0. 전제

- 캠페인 = 전용 세션 1회. 연구 단위와 섞지 않는다. "1회"는 캠페인 단위다 — 재축적이 /tidy 수용량을 다시 넘으면 새 캠페인 가능하되, 그 반복은 크기 규율(`/harness` §1·§5) 실패 신호이므로 원인을 함께 보고한다.
- 이 커맨드의 세션은 전역 "진입점 통일"(`/harness` 단위 confirm)의 예외다 — 워크플로는 이 문서가 정의한다(`/audit`과 동형).
- 조사는 read-only — Explore/general-purpose fan-out 가능(파일 60개 넘으면 권장).
- **git 신호 주의**: docs/가 .gitignore된 프로젝트(예: 협업 레포)는 git log·ls-files 판정이 전부 무효 — mtime·내용 대조로만.
- 협업 레포는 공유 표면(타 저자 폴더·공유 카운터 슬롯)을 후보에서 제외 — 내 관할만 정리한다.

## 1. 조사 — 인벤토리 6종

각 항목을 근거(참조 grep 결과·크기·mtime)와 함께 수집:

1. **비정규 폴더** — docs/ 직하 정규 집합(plans/done/references/notes/archive/experiments) 밖 폴더(legacy/, work-plans/ 등). 현행 문서의 inbound 참조 grep.
2. **루트·docs 직하 산출물** — /tidy §1·§2와 동일 판정(superseded/consumed/stale — 내용 대조, 파일명·mtime 단독 ❌).
3. **plans/ 고아** — progress·CLAUDE.md·SPEC 어디서도 호명되지 않는 파일 + 비규약 네이밍(자유형 덤프·라운드별 리뷰 파편) 분류. done/도 동일.
4. **바이트 동일 중복** — md5 그룹핑, 그룹당 원본 1개 지정.
5. **git 안 바이너리 자산** — docs/ 내 png·html 등(규약: 실험 산출물은 git 밖).
6. **정본 비대** — progress/LEARNINGS/SPEC 크기, progress 헤더에 역류한 이력(done 결번 세대), 무효 문서를 가리키는 현행 포인터.

## 2. 분류 confirm (HARD)

그룹 단위 표로 제시: 대상 / 처분(archive 이동 · 중복 삭제 · 소급 done 회수 · 정본 다이어트 · 자산 이동 · 보류) / 근거 1줄 / 규모(파일 수·KB). 사용자 확정분만 실행 — 일괄·부분·전체 보류 모두 가능. 확신 없으면 보류가 기본값(/tidy §2와 동일 원칙).

## 3. 실행

- **이동**: `docs/archive/YYYY-MM/`(마지막 수정 월)로, 폴더는 통째. `_INDEX.md`에 파일당 1줄(폴더는 폴더당 1줄 + 내용 요약). git 추적분은 `git mv`.
- **중복 삭제**: 삭제 직전 md5 동일 재확인 후 사본만 삭제, _INDEX에 `dup-of {원본}` 1줄.
- **소급 done 회수**: done 결번 세대의 서사를 progress·plan 서술에서 추출해 `done_v{N}.md` 신설 — **기존 서술의 재배치만, 새 판정 창작 ❌.** 신설 파일 상단에 배너 의무: `> 소급 회수(/deep-clean YYYY-MM-DD) — progress·plan 서술 재배치, 신규 판정 없음`. 원문에 결론이 없으면 결번 유지 + "미회수 — 근거 부족" 보고.
- **정본 다이어트**: /tidy §6과 동일 수술(헤더는 현재 상태만, 이력·세션 로그 초과분은 `archive/rollup_YYYY-MM.md` 롤링, LEARNINGS 통폐합 — 원문 보존, _INDEX 기재). 무효 문서를 가리키는 현행 포인터는 현행 경로로 갱신.
- **자산 이동**: git 밖 목적지(runs/ 등)는 사용자 지정 — 경로 confirm 전 이동 ❌.

## 4. 검증·보고

- 파일 대차: 이동 n + 삭제(중복) m + 신설(소급 done) k — 총수가 안 맞으면 실패로 보고.
- 참조 무결성: 현행 문서에서 이동 파일명 grep → 링크 갱신, 애매하면 보고만.
- 정본 크기 before/after. **commit ❌** — 커밋 여부·시점은 사용자가 정한다.

## 하지 않는 것

- RESEARCH_SPEC·기존 `done_v*` 본문 수정 ❌ (소급 done **신설**은 OK — 신설이지 개정이 아니다).
- 판정 애매한 파일의 처분 ❌ — 보류로 남긴다.
- git commit/push ❌.
- 반복 실행 전제의 설계 ❌ — 캠페인 종료 후 유지보수는 /tidy와 크기 규율(`/harness` §1·§5) 몫이다.
