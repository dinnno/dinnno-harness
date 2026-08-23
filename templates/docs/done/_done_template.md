# done_v{N}

> 이 파일은 `templates/docs/done/_done_template.md`를 복사한 것.
> 짝: `docs/plans/plan_v{N}_*.md`

## 1. 무엇을 만들었나

(파일 경로 + 핵심 변경. plan §2 "제안한 모듈"이 실제로 어떤 모양으로 들어갔는지)

## 2. 무엇을 검증했나

(실행 커맨드, 수치 표, wandb run 링크, sim/실로봇 영상 경로. plan §3 설계대로 돌았는지)
필수: seed 수 × rollout 수와 mean±std(또는 CI). 단일 seed면 사유 명시.

## 3. 예상과의 차이

(plan §1·§3 가정 vs 실제 관찰의 갭. thesis(`RESEARCH_SPEC §1`)에 영향이 있나)
(negative를 'kill/트랙 사망'으로 쓰려면 먼저 done/_GUIDE §Kill/Pivot 4게이트 자기검증 — 미통과면 "insufficient evidence"로만.)
(thesis 영향 '있음'이면 progress.md 결정 큐에 [spec-drift] 1줄 — re-lock은 다음 (a) 단위.)

## 4. 다음 plan 후보

2-3개를 추천 순서대로. 각 후보에 가능하면 다음 한 줄씩 (필수: 후보 이름·paper-impact, 권장: 예상 소요):
negative verdict면 pivot 3형(무대 교체/scope 축소/thesis 수정) 중 해당 옵션을 후보에 포함.

- **후보 이름**: 무엇을 하는 plan인지 (≤1줄)
- **Paper impact**: `RESEARCH_SPEC §1 thesis`/§4 비교 축 또는 active bootstrap readiness gap의 어디를 움직이나
- **예상 소요**: 1-2주 단위 추정 (선택)

> 기본 `/harness`는 자동 chain 금지: 후보 제시 후 현재 단위 종료. 새 plan은 사용자 선택 또는 명시 승인된 research-bootstrap/research-loop 상위 orchestrator가 현재 closure 뒤 boundary·budget 안에서 선택할 때만 진입.

## 5. 외부 리뷰

(`done_v{N}_codex.md` 또는 사람 피드백 반영 한 줄. 라운드 규칙은 `/harness` §4 — 자동 반복 ❌, 2라운드 후 계속은 confirm)
