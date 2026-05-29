# docs/

이 폴더에 들어가는 문서들:

- `RESEARCH_SPEC.md` — 프로젝트의 불변 spec (북극성). thesis · naive baseline · failure taxonomy · comparison axes · derivation · ablation plan · accepted failures
- `ARCHITECTURE.md` — repo 디렉토리 레이아웃 (configs/src/scripts/libs/data/ckpt)
- `progress.md` — Phase + Ablation matrix 트래킹. 한눈에 진척 보기.
- `plans/` — 실험별 `plan_v{N}_{short-name}.md`
- `done/` — 완료 보고 `done_v{N}.md`
- `references/` — 외부 자료(arxiv/code/homepage) 인박스. `_INDEX.md`에 URL만 박으면 `codex:rescue`가 분석해서 summary 저장.

## 작성 규약

- RESEARCH_SPEC.md는 실험 결과로 인해 어긋나기 전에는 건드리지 않는다. 어긋나면 spec부터 고치고 plan을 다시 슬라이싱한다 (코드로 패치 금지).
- ARCHITECTURE.md는 새 디렉토리/규칙이 생길 때만 갱신.
- 각 plan/done은 자기완결적이어야 한다. "이전에 논의한 바와 같이" 같은 외부 참조 금지.

## RESEARCH_SPEC 작성/갱신 protocol

`RESEARCH_SPEC.md`는 짧고 진하게(7개 슬롯) 쓴다. 기존에 긴 design doc·논문 노트·과한 spec이 있어도 **그걸 요약해서 박지 말 것 — 무조건 reject**. 다음 순서로 사용자와 깊게 합의한 결과만 슬롯에 적는다.

**합의 깊이 (강제 카운터 아님, 가이드):**

각 슬롯은 사용자와 충분히 문답해 합의된 뒤 닫는다 — 한 번 묻고 끝내지 마라. 사용자가 "넘어가자" 하면, 아직 모호한 점이 있으면 "X가 아직 불명확한데 정말 OK?"를 한 번 더 확인하고 그래도 OK면 진행. **핵심은 round 횟수가 아니라 sleepwalking 방지** — Claude 혼자 채우지 않고 사용자 발화에서 끌어냈는가.

**순서:**

1. **인풋 적재** — 사용자에게 "참고할 기존 문서/논문 경로" 묻고 1개씩 적재. PDF·1MB 이상이면 `codex:rescue` 자동 dispatch (요약만 받음).
2. **§1 thesis** — "<failure mechanism> + <principled fix>" 한 문장을 **사용자가 직접 발화**할 때까지 묻는다. Claude는 초안 제시 OK지만 사용자 발화로 확정. 매 round에서 failure mechanism과 "왜 이 형태여야만 하는가" 둘 다 있는지 점검.
3. **§2 naive baseline 가용성** — "1주 안에 돌릴 수 있나?"를 묻고 No면 §1로 회귀해서 좁힘.
4. **§3 failure taxonomy** — 미실행이면 비워두고 "naive baseline 돌린 후 채울 것" 메모.
5. **§4 비교 축** — "벤치마크 X 정확도만" 패턴 검출되면 reject.
6. **§5 derivation** — 각 구성요소 ↔ §3 근본 원인 매핑. 1대1 안 되면 §5 회귀.
7. **§6 ablation** — 구성요소당 ablation 1개. "교체 가능 = 신규 아님" 체크.
8. **§7 accepted failures** — 사용자가 명시적으로 발화한 것만.

**Anti-pattern (무조건 reject):**

- 기존 design doc 한 번 읽고 7슬롯 자동 채워 `RESEARCH_SPEC.md`에 박기. Sleep walking. 사용자와 round 없이 박은 spec은 발견 즉시 폐기하고 §1부터 다시.
- 기존 spec이 과하게 길다는 이유로 "축약 버전"을 만드는 것. 축약 아니고 **사용자 발화 재구성**이어야 함.

**자기점검:** spec 작성 단위 끝에 `RESEARCH_SPEC.md §30-sec self-check`를 실제로 통과시켜야 함. 통과 안 되면 §1로 회귀.

## Init (a₀) protocol

`apply.sh` 직후 또는 placeholder 남은 상태에서 `/harness` 진입 시. 5단계 순서. 모든 단계에서 **추측 박치기 reject** (사용자 발화 기반만).

1. **프로젝트 루트 `CLAUDE.md`** — 도메인 컨텍스트 인터뷰. 묻기: 시뮬레이터·로봇 플랫폼·데이터셋·자주 쓰는 명령어. 충분히 합의될 때까지.
2. **`docs/ARCHITECTURE.md`** — 기존 코드 있으면 `Explore` ×1로 실제 트리 매핑 → 사용자 검증. 신규면 사용자가 계획한 구조 묻기. 충분히 합의될 때까지.
3. **`docs/RESEARCH_SPEC.md`** — §"RESEARCH_SPEC 작성/갱신 protocol" 따름 (가장 무거움).
4. **`docs/progress.md` Phase** — RESEARCH_SPEC §6 채워진 후 Phase mile stone 정의. 한 번 합의로 OK (가볍게).
5. **`docs/references/_INDEX.md`** — "지금 참조하는 paper/repo 있나" 한 번 묻고 시드. 없으면 OK.

**완료**: 검출된 placeholder 모두 해소 + progress.md Phase 1개 이상 + references 한 번 물어봄. 자동 chain ❌, 사용자 GO 시 (b)로 진입.

**Anti-pattern**: 5개 질문 한 번에 폭격 / 코드 보고 도메인 추측 후 사용자에게 확인만 / Explore 결과를 사용자 검증 없이 박기.

## progress.md 갱신 protocol

`docs/progress.md`는 한눈에 진척 보기용. 갱신 규칙:

- **spec 단위 끝**: Phase 리스트와 Ablation Matrix 행 초기 생성/조정.
- **plan 단위 끝**: 해당 ablation_id의 `plan` 컬럼에 파일명 박고 상태를 `running`.
- **done 단위 끝**: `done` 컬럼·`핵심 수치`·상태(`done`) 갱신. Phase 체크박스 충족 시 체크.
- 각 갱신은 done/plan 단위 작업 마지막 한 줄로. 별도 단위가 아니라 단위의 산출물.
