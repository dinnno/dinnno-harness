# LOOP — 자율 탐색 루프 spec

> working baseline(첫 GO 실험) 전에는 이 파일을 열 일 없다. `(autoloop)` 단위 진입 시에만 적재.
> 이 파일 = ① Loop-Ready 체크리스트 ② 루프 spec ③ ledger. 체크리스트를 채우는 것이 곧 spec 작성이다.

## Loop-Ready 체크리스트 (L1–L7)

전 항목 ✓ + 사용자 승인 1줄이 loop-run의 전제. 미충족 항목은 **loop-prep** 단위(plan/done 짝)로
채운다 — loop-prep plan §0 짝 자리에 `LOOP.md L{k}` 인용 OK, paper-impact는 검증 처리량
(시간당 검증되는 가설 수)으로 서술.

- [ ] **L1 검증된 baseline** — ckpt {경로} / config {경로} / commit {hash} / J = {mean±std, seeds(N)×rollouts}
  판정: 이 고정 셋 재현 실행 1회가 선언 오차 내 → ledger 0행(anchor)으로 기록됨.
- [ ] **L2 판정 함수 J + guard** — J: {metric, 방향} / keep: {J ≥ J_best + δ, δ=} / seed 정책: {N, tie-break}
  / guard: {hard-floor 지표 0–2개 — 위반 시 J 무관 rollback. 3개 이상 필요하면 J가 아직 없다는 신호 → L2 미충족}
  사전 유효성 검산 (수치 1줄씩, 빈 슬롯 = 미충족):
  - 도달가능성: {목표–baseline gap = 노이즈 σ의 {x}배}
  - 검정력: {N seeds에서 δ 감지 power ≈ {값} (≥0.8?)}
  - 도구 타당성: {J↑=품질↑ 확인 방법·결과 — 예: 검증 셋 상·하위 5개 수동 대조}
- [ ] **L3 변이 표면 (allowlist)** — 파라미터 전부 configs/*.yaml. 변이 허용: {field: 범위/타입, ...}
  판정: 각 필드가 실제 yaml에 존재 + config만 바꾼 dry-run 1회 성공. allowlist 밖 변이 = 루프 밖(HARD).
- [ ] **L4 예산** — trial당 {상한} / 총 {최대 trial 수 or 시간} / 정지: 연속 {K}회 no-improve ·
  experiment-level 이상 · 소진 (먼저 오는 것). 판정: 숫자 3개 + trial 1회 실측이 상한 안.
- [ ] **L5 keep/rollback** — 격리: configs/loop/trial_{k}.yaml + trial별 runs/. keep = champion 갱신,
  rollback = 승격 없음(baseline 오염 0). 판정: mock trial 1회로 두 경로의 파일시스템 상태 확인.
- [ ] **L6 결과→Matrix 배선** — eval 기계가독 요약: {경로/형식, 예: runs/*/metrics.json}. 판정: 요약→셀
  (mean±std, seeds×rollouts) 변환 경로 실재 + 1회 시연.
- [ ] **L7 Loop Report (시각화)** — ledger·runs 요약 → **self-contained HTML 1개** {경로, 예:
  runs/loop/report.html} 매 trial 뒤 자동 재생성(append-only ledger 전체를 렌더 = 여러 run에 걸친
  누적 히스토리). 표시 지표·차트 구성(J 추이·champion 궤적·guard·예산 소진 등)은 loop-run 전
  **사용자와 합의**하고 합의 발화를 여기 1줄 기록. 판정: mock ledger 2행으로 리포트 생성 1회 +
  사용자 "이 형태 OK" 발화.
- 사용자 승인: {YYYY-MM-DD "사용자 발화 1줄"}

## 운영 (loop-run trial 사이클)

싼 ~100회/밤이 아니라 **비싼 밤당 ~5–15 trial** 전제 — 변이는 랜덤 탐색이 아니라 이번 run의
plan에 적은 **우선순위 목록** 순.

1. 변이 생성: allowlist 안에서 `configs/loop/trial_{k}.yaml` 직접 작성(yaml 1개는 기계적 구현 아님 —
   implementer 위임 불필요). 코드 변경이 필요한 변이는 스킵 + progress 결정 큐에 1줄.
2. 실행: Codex의 background/process session으로 시작하고 session ID를 보존해 poll한다. 대기 중 다음 변이 후보·done 골격 준비.
3. 판정: eval 요약 → J·guard → keep(champion 갱신) / rollback.
4. ledger 1행 append + Loop Report(L7) 재생성(SOFT — 이 둘이 곧 보고). AFK push는 keep·이상·정지
   시에만(매 trial ❌).
5. 정지 조건까지 1–4 반복. code-level 실패(원인 규명·재실행 쌈)는 고치고 계속,
   experiment-level 이상은 즉시 정지(HARD).

**Verdict**: done_v{N}에 ledger 요약(trial 수·best J·champion) + Loop Report 경로 + champion
held-out 재검증 1회 + Matrix 셀 일괄 기입. 루프 안 kill 결론 ❌ — negative streak은 증거일 뿐(`done/_GUIDE §Kill/Pivot`).
세션이 죽으면 ledger 마지막 행부터 재개 — 잔여 예산으로, `$harness` 단위 confirm이 재개 confirm.

## Champion

- champion: {config / ckpt / J / ledger row k}

## Ledger (append-only, 1 trial = 1행)

| k | date | 변이(diff 요약) | J (mean±std) | guard | verdict | runs 경로 |
|---|---|---|---|---|---|---|
| 0 | | baseline (anchor) | | | anchor | |
