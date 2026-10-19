# CVPR (IEEE/CVF Conference on Computer Vision and Pattern Recognition)

해마다 잘 안 바뀌는 성격만 적는다. 마감, 페이지 수, 그해 정책은 프로젝트 `writing/VENUE.md`에 공식 페이지 출처와 함께 적는다.
기준: CVPR 2026 Author Guidelines(https://cvpr.thecvf.com/Conferences/2026/AuthorGuidelines), CVPR 2027 Call for Papers(https://cvpr.thecvf.com/Conferences/2027/CallForPapers). 확인 2026-10-19.

## 템플릿

- 공식 kit: https://github.com/cvpr-org/author-kit (`main` 또는 그해 태그, 예 `CVPR2026-v1(latex)`). 구성은 `main.tex`, `preamble.tex`, `cvpr.sty`, `ieeenat_fullname.bst`, `sec/`, `rebuttal.tex`.
- 리뷰 제출은 `\usepackage[review]{cvpr}`(익명, 줄 번호). camera-ready는 옵션을 바꾼다.
- Overleaf: Compiler pdfLaTeX, main document `main.tex`.

## 분량과 형식 (2026 기준, 그해 확인 필요)

- 본문 8쪽(그림·표 포함). 참고문헌만 있는 쪽은 추가 가능. 초과하면 심사 없이 리젝.
- supplementary는 선택이고 심사위원이 안 볼 수도 있다. 본문만으로 주장이 성립해야 한다. 영상, 증명, 추가 표, concurrent submission 첨부 가능. 외부 영상 링크 금지.

## 익명성

- 저자, 소속, 감사의 글, 과제 번호를 넣지 않는다. supplementary와 영상도 마찬가지다.
- 자기 논문 인용은 3인칭으로 한다. 동시 투고 중인 자기 논문은 익명본을 supplementary에 넣고 차이를 본문에 설명한다.
- 공개 코드 저장소를 인용하지 않는다("will be made publicly available"까지만). 저자를 드러내는 링크를 넣지 않는다. 의심되면 링크를 빼는 쪽이 기본이다.
- arXiv 게재와 프로젝트 페이지는 허용된다.

## rebuttal

- 1쪽 PDF, kit의 `rebuttal.tex` 사용. 1쪽을 넘거나 여백을 바꾸면 무시된다. 익명 유지, 외부 링크 금지.
- 새 기여나 리뷰어가 요청하지 않은 새 실험 결과는 넣지 않는다(심사위원이 무시하도록 안내받는다).

## 정책

- LLM 사용은 허용되지만 사실 오류, 표절, 존재하지 않는 인용의 책임은 저자에게 있다. 존재하지 않는 인용은 리젝 사유다. 원고에 숨긴 프롬프트 인젝션은 윤리 위반으로 desk reject될 수 있다.
- 저자는 요청 시 심사를 맡는다. 모든 저자는 최신 OpenReview 프로필이 필요하다.
- dual submission: 심사 기간 동안 실질적으로 같은 논문을 다른 학회나 워크숍에 내지 않는다.

## 심사위원이 보는 것 (모의 심사 기준)

CVPR 심사 양식은 해마다 문구가 조금씩 바뀌지만 축은 같다. 모의 심사는 이 축으로 한다.

1. 요약과 기여: 무엇이 새로운가, 기여가 명확히 주장되고 입증됐나.
2. 강점.
3. 약점: novelty 부족, 실험 불충분(baseline, ablation, 데이터셋), 명료성, 재현성.
4. 사전 연구 대비 위치와 빠진 인용.
5. 재현성: 구현 세부, 하이퍼파라미터, 코드 공개 의사.
6. 최종 등급: CVPR은 reject / weak reject / borderline / weak accept / accept 계열 등급과 신뢰도를 쓴다. 정확한 등급 문구는 그해 양식을 따른다.
7. rebuttal에서 답을 듣고 싶은 질문.
