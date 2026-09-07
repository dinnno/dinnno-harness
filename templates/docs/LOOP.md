# LOOP — autoloop spec (config 변이 루프)

> working baseline 전에는 열 일이 없다. `loop` 스킬의 autoloop 모드에서만 읽는다.
> 체크리스트 L1–L7을 채우는 것이 곧 루프 spec이다. 전부 채워지고 사용자 승인 한 줄이 있어야 돈다.

## Loop-Ready 체크리스트

- [ ] **L1 검증된 baseline** — ckpt {경로} / config {경로} / commit {hash} / J = {mean±std, seeds(N)×rollouts}. 재현 실행 1회가 선언 오차 안이면 ledger 0행(anchor).
- [ ] **L2 판정 함수 J + guard** — J: {metric, 방향} / keep: {J ≥ J_best + δ} / seed 정책 {N} / guard: {hard-floor 지표 0–2개}. 검산: 목표–baseline gap이 노이즈 σ의 몇 배인가, N seeds로 δ를 감지할 power가 0.8을 넘나, J↑가 실제 품질↑인지 어떻게 확인했나.
- [ ] **L3 변이 표면** — 허용 필드와 범위 {field: 범위}. 전부 `configs/*.yaml`에 실재하고 config만 바꾼 dry-run이 1회 성공. allowlist 밖 변이는 루프 밖.
- [ ] **L4 예산** — trial당 {상한} / 총 {trial 수 또는 시간} / 정지: 연속 {K}회 no-improve, experiment-level 이상, 소진.
- [ ] **L5 keep/rollback** — `configs/loop/trial_{k}.yaml` + trial별 `runs/`. keep = champion 갱신, rollback = 승격 없음. mock trial 1회로 두 경로 확인.
- [ ] **L6 결과 → Matrix** — eval 기계가독 요약 {경로/형식}. 요약 → 셀(mean±std, seeds×rollouts) 변환 1회 시연.
- [ ] **L7 Loop Report** — ledger와 runs 요약을 self-contained HTML 하나({경로})로 매 trial 뒤 재생성. 표시 지표는 사용자와 합의하고 발화를 여기 한 줄로.
- 사용자 승인: {YYYY-MM-DD "발화 한 줄"}

## 운영

밤당 5–15 trial 전제. 변이는 랜덤이 아니라 plan에 적은 우선순위 순. 1) allowlist 안에서 `trial_{k}.yaml` 작성 2) 백그라운드 실행, 대기 중 다음 변이와 done 골격 준비 3) eval 요약 → J·guard → keep/rollback 4) ledger 한 행 + 리포트 재생성 5) 정지 조건까지 반복. code-level 실패는 고치고 계속, experiment-level 이상은 즉시 정지. 루프 안에서 kill 결론을 내리지 않는다. 세션이 죽으면 ledger 마지막 행부터 재개. 루프가 끝나면 champion을 튜닝에 쓰지 않은 held-out 평가로 1회 재검증한 뒤 Matrix에 기입한다.

## Champion

- champion: {config / ckpt / J / ledger row k}

## Ledger (append-only, 1 trial = 1행)

| k | date | 변이(diff 요약) | J (mean±std) | guard | verdict | runs 경로 |
|---|---|---|---|---|---|---|
| 0 | | baseline (anchor) | | | anchor | |
