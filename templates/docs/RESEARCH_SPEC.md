# Research Spec — {프로젝트명}

> "X fails → we added module" = motivation. "X fails because of principle P → only form S resolves P" = novelty.
> 첫 번째에서 멈춰 있으면 method가 아직 준비되지 않은 것이다.

## 0. 현재 방향 (second brain 동기용)

> 문헌 위키가 읽는 블록. 현재값만 한 줄씩, 이력·수치·경과는 쓰지 않는다. thesis나 방법론이 움직인 단위 직후 갱신. 괄호 안 문구는 그대로 둔다.

- **agenda line:** `{vault research-agenda의 대응 항목명 — 없으면 "신규"}`
- **방향:** {무엇을 푸는가 — 120자 이내}
- **방법론:** {어떤 형태로 푸는가 — 120자 이내}
- **갱신:** {YYYY-MM-DD}

## 1. Thesis

한 문장: `<failure mechanism> + <principled fix>`. 채울 수 없으면 논문을 더 읽는다.

## 2. Naive baseline

가장 단순한 버전. 1주 안에 실제로 돌릴 수 있는 형태. 실제로 돌렸나? (예/아니오 + 결과 한 줄)

## 3. Failure taxonomy

§2를 돌린 결과로 채운다. mechanism 수준의 root cause.

| 케이스 | 빈도 | 근본 원인 (메커니즘 수준) |
|--------|------|---------------------------|
|        |      |                           |

## 4. Comparison axes

판단할 축 2–3개. "벤치마크 X의 정확도"만이면 약하다.

1.
2.
3.

## 5. Derivation

| 구성요소 | 어느 root cause를 해결 | 더 단순한 형태가 안 되는 이유 |
|----------|----------------------|------------------------------|
|          |                      |                              |

## 6. Ablation plan

구성요소 1개당 ablation 1개. 교체 가능하면 신규가 아니다.

- [ ] component A: ablation =
- [ ] component B: ablation =

## 7. Accepted failures

명시적으로 풀지 않는 것.

-

## 미결 질문

- (intent 단계에서 아직 답이 없는 것. 답이 나오면 위 슬롯으로 옮기고 지운다)

---

## 30-sec self-check

"실제로 새로운 게 뭐냐"를 한 문장으로 답할 수 있는가. 그 답에 failure mechanism과 "왜 이 형태여야만 하는가"가 둘 다 있는가. 아니면 아직 motivation 단계다.

## Reject if

- 기여 = "기존 방법은 X를 안 한다"
- 도출 없는 단일 모듈 추가
- Related work 5편 미만 또는 전부 같은 그룹
- 어려운 과제를 "future work"로 회피
