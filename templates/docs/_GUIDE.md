# docs/

| 파일 | 역할 | 누가 언제 갱신 |
|---|---|---|
| `RESEARCH_SPEC.md` | 불변 spec. thesis, baseline, failure taxonomy, 비교 축, ablation, accepted failures | spec 단위에서만. 실험 결과가 어긋나면 코드가 아니라 spec부터 고친다 |
| `ARCHITECTURE.md` | 코드 배치. 새 파일은 여기 자리가 있어야 만든다 | 새 모듈·폴더가 생길 때 |
| `progress.md` | 진척 인덱스: Stage, 타임라인, Ablation Matrix, 결정 큐. done을 복제하지 않고 결론과 포인터만 | done·spec 단위 끝에 한 줄 |
| `LEARNINGS.md` | 지금 유효한 규칙 20줄 이내 + 이력. 사용자 지적은 그 턴에 append | 발견 즉시 |
| `plans/plan_v{N}_{slug}.md` | 한 단위의 설계. §3 게이트 표, §6 TODO | Setup에서 작성, 실행 중 §5·§6 |
| `done/done_v{N}.md` | 한 단위의 결과와 판정 | Verdict에서 |
| `plans/plan_v{N}_codex.md` | 외부 리뷰. 라운드마다 같은 파일에 append | `plan-redteam` |
| `references/_INDEX.md` | 외부 자료 URL 인박스 | URL을 마주친 즉시 한 줄 |
| `notes/YYYY-MM-DD_{slug}.md` | 일회성 산출물(서베이, 분석 memo, loop note). 태어날 때부터 아카이브 후보 | 필요할 때. 소비되면 `dinnno tidy`로 `archive/` |
| `LOOP.md` | autoloop 전용 체크리스트와 ledger | `loop` 스킬 |

각 plan/done은 자기완결적으로 쓴다. "이전 대화에서"처럼 대화를 참조하지 않는다. 다음 세션은 파일만 읽는다.

## init 인터뷰 (placeholder가 남아 있을 때)

순서: 루트 `AGENTS.md`(시뮬레이터, 로봇, 데이터셋, 자주 쓰는 명령) → `ARCHITECTURE.md`(기존 코드가 있으면 read-only 탐색으로 실제 트리를 그린 뒤 사용자 검증) → `RESEARCH_SPEC.md` → `progress.md` Phase → `references/_INDEX.md` 시드.

원칙은 하나다. 슬롯은 사용자 발화에서 채운다. Claude가 기존 문서를 읽고 혼자 채운 spec은 잠꼬대라서, 초안은 제안으로만 내밀고 사용자가 말한 것으로 확정한다. 질문은 한 번에 하나씩, 충분히 합의된 뒤 다음 슬롯으로.

## RESEARCH_SPEC 슬롯

1. §1 thesis — `<failure mechanism> + <principled fix>` 한 문장. failure mechanism과 "왜 이 형태여야만 하는가"가 둘 다 있어야 한다.
2. §2 naive baseline — 1주 안에 돌릴 수 있는가. 아니면 §1로 돌아가 좁힌다.
3. §3 failure taxonomy — baseline을 돌린 결과로 채운다. 미실행이면 비워 둔다.
4. §4 비교 축 — "벤치마크 X 정확도만"은 약하다.
5. §5 derivation — 구성요소마다 §3의 어느 root cause에서 나왔는지.
6. §6 ablation — 구성요소당 하나. 교체 가능하면 신규가 아니다.
7. §7 accepted failures — 사용자가 명시한 것만.

끝에 `30-sec self-check`를 실제로 통과시킨다. 못 하면 §1로.

## progress.md 갱신

- plan 단위 끝: 타임라인 행 추가, 해당 ablation 행 `running`.
- done 단위 끝: `done` 컬럼, 핵심 결론, 상태. 헤더의 anchored commit·seed·ckpt 경로. Matrix 셀 값은 metrics 파일이나 eval 출력에서 옮긴다(손계산 없음).
- 세션 로그는 plan §5에 쓴다. progress에는 쌓지 않는다.
- 결정 큐: pay-grade로 미룬 결정, spec-drift, kill-candidate, 💡 아이디어. 사용자가 고르면 체크하고 Phase/타임라인으로 흡수.

## 네이밍

`plan_v0_naive.md`(baseline), `plan_v1_{component}.md`, … slug는 kebab-case 한두 단어. done은 `done_v{N}.md`로 짝을 맞춘다. `codex`는 리뷰 파일 예약어다.
