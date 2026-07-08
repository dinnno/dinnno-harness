# docs/done/

이 폴더는 plan별 완료 보고 `done_v{N}.md`를 담는다. 짝: `plans/plan_v{N}_*.md`.

**Verdict의 산출물.** Execute 끝(학습/평가 완료) 시 진입. 이 파일 §3에서 가설이 **negative로 판정**되면 세션 종료 안내 — "이 가설 폐기. 새 가설은 새 터미널 + `/harness`". positive면 §4 다음 후보 도출 후 세션 종료. 어느 쪽이든 **다음 가설로 자동 chain ❌**.

## 각 done에 들어가는 것

1. **무엇을 만들었나** — 추가/수정한 파일 경로와 핵심 변경
2. **무엇을 검증했나** — 실제 돌린 커맨드, 결과 수치, 실로봇/sim 영상 경로
3. **예상과의 차이** — plan에서 가정한 것과 실제 관찰의 갭
4. **다음 plan 후보** — 이 결과가 가리키는 다음 실험 1-2개

## 리뷰 사이클

done 작성 후 외부 리뷰어(다른 LLM 또는 사람)에게 가장 매서운 피드백을 받는다:
- 모듈이 정말 limitation을 극복하는가, 아니면 그렇게 보이기만 하는가?
- ablation은 실제인가, 공연인가?
- 숨은 결합·죽은 가지·암묵적 가정?

피드백 반영해서 done을 갱신. 리뷰어가 더 이상 할 말이 없을 때까지.

## Kill/Pivot 판정 — negative verdict의 자격 요건

negative 결과 ≠ kill. "이 트랙/방향은 죽었다"는 주장은 done §3에서 아래 4게이트 자기검증을
통과해야 admissible:

1. **Scope coverage** — 주장 범위 = 실측 범위인가 (3축 중 0.5축 실측으로 3축 kill ❌).
2. **Instrument validity** — 판정 metric이 목표 품질과 양의 상관임을 확인했나 (proxy가 품질과
   음의 상관이면 그 negative는 무효).
3. **Statistical power** — 이 seed×rollout 수로 그 효과 크기를 감지할 수 있었나 (power가 낮으면
   "감지 실패"지 "부재의 증명"이 아니다).
4. **Provenance** — 유효 baseline·오염 없는 config·올바른 데이터에서 나온 결과인가.

- 하나라도 미통과 → verdict를 **"insufficient evidence — 게이트 {k} 미통과"로 다운그레이드**.
  done §4 첫 후보는 그 게이트를 메우는 실험.
- 전부 통과 → admissible이지만 **pay-grade** — thesis/축을 움직이므로 이 세션이 결론 내지 않는다.
  `progress.md` 결정 큐에 `[kill-candidate]` 1줄 착지 + 상위 세션/사용자 결정 (HARD).
- kill 전에 **pivot 3형**을 done §4에 항상 병기: ① 무대 교체(같은 thesis, 다른 task/env/데이터)
  ② scope 축소(claim을 실측 범위로 좁혀 유지 — spec §7 accepted failures에 추가)
  ③ thesis 수정((a) spec 단위 — pay-grade). kill은 세 pivot이 모두 기각된 뒤의 사용자 전결.
- (autoloop)·Execute 루프 안에서는 이 protocol 발동 자체가 금지 — 증거만 쌓고, 판정은 Verdict에서.

## Spec과의 불일치

이 plan의 결과가 `docs/RESEARCH_SPEC.md`와 모순되면 코드로 패치하지 말고 spec을 먼저 고쳐라. 그 다음 영향받은 plan을 다시 슬라이싱.

## 시작 방법

새 done은 같은 폴더의 `_done_template.md`를 복사해서 시작한다:

```bash
cp docs/done/_done_template.md docs/done/done_v{N}.md
```

섹션 헤딩은 고정. 채울 내용이 없으면 "N/A — 사유"를 쓰고 비워두지 않는다.
