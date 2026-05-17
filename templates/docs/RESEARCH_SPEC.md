# Research Spec — {프로젝트명}

> Rule: "X fails → we added module" = motivation. "X fails because of principle P → only form S resolves P" = novelty.
> If you stop at the first, the method is not ready.

## 1. Thesis

한 문장: `<failure mechanism> + <principled fix>`

채울 수 없으면 중단하고 논문 더 읽기.

## 2. Naive baseline

가장 단순한 버전. 1주 내에 실제로 돌릴 수 있는 형태. 실제로 돌렸나? (예/아니오 + 결과 1줄)

## 3. Failure taxonomy

§2에서 실제로 돌려본 결과로부터 채운다. mechanism-level root cause.

| 케이스 | 빈도 | 근본 원인 (메커니즘 수준) |
|--------|------|---------------------------|
|        |      |                           |
|        |      |                           |

## 4. Comparison axes

판단할 축 2-3개. "벤치마크 X의 정확도"만 = 약함.

1.
2.
3.

## 5. Derivation

각 구성요소가 §3의 어떤 근본 원인에서 나오는지, "더 단순한 형태는 왜 안 되는지" 함께.

| 구성요소 | 어느 root cause를 해결 | 더 단순한 형태가 안 되는 이유 |
|----------|----------------------|------------------------------|
|          |                      |                              |

## 6. Ablation plan

구성요소 1개당 ablation 1개. 교체 가능 = 신규 아님.

- [ ] component A: ablation =
- [ ] component B: ablation =

## 7. Accepted failures

명시적으로 풀지 않는 것들.

-

---

## 30-sec self-check

"실제로 새로운 게 뭐냐?"를 한 문장으로 답할 수 있는가? 답에 **failure mechanism**과 **왜 이 형태여야만 하는가**가 둘 다 있는가? 아니면 motivation 단계.

## Reject if

- 기여 = "기존 방법은 X를 안 한다"
- 도출 없는 단일 모듈 추가
- Related work <5 papers 또는 모두 같은 그룹
- 어려운 과제를 "future work"로 회피
