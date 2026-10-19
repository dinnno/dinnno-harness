# writing/ — {논문 가제} ({학회} {연도})

원고 세션(`/paper`)이 읽고 갱신하는 상태 파일이다. 다음 세션은 이 파일에서 이어간다.

## 다음 시작점

- 다음 섹션: {sec}
- 답 안 된 질문: {없음 | 섹션: 질문}
- Overleaf 미업로드: `dinnno paper check`의 "Overleaf 미반영" 줄을 본다

## 섹션 상태

| 섹션 | 파일 | 단계 | 라운드 | 마지막 검토 | 남은 GAP/질문 |
|---|---|---|---|---|---|
| Abstract | `sec/0_abstract.tex` | 비어 있음 | 0 | — | |
| Introduction | `sec/1_intro.tex` | 비어 있음 | 0 | — | |
| Related Work | `sec/2_related.tex` | 비어 있음 | 0 | — | |
| Method | `sec/3_method.tex` | 비어 있음 | 0 | — | |
| Experiments | `sec/4_experiments.tex` | 비어 있음 | 0 | — | |
| Conclusion | `sec/5_conclusion.tex` | 비어 있음 | 0 | — | |

단계: 비어 있음 → 초안 → 검토 반영 중 → 안정.

## 구성

- `VENUE.md`: 학회 규정, 마감, 템플릿 출처, 사실 대장 경로(`facts:`)
- `STYLE.md`: 사용자가 확인한 문체 규칙
- `numbers.yaml` → `numbers.tex`: 원고 수치 매크로. `dinnno paper numbers`로만 만든다
- `notes/<sec>.md`: 사용자 개괄 메모 (라운드별 원문)
- `reviews/`: 섹션 검토, 모의 심사, 실제 리뷰와 rebuttal 대응표
- `.sync/base/`: 마지막으로 Overleaf와 맞춘 상태. 손대지 않는다
- `reference/`: 템플릿 예제 원본 (컴파일 대상 아님, zip 제외)

## Overleaf

- 내보내기: `dinnno paper export` → `writing/_export/<프로젝트>_overleaf.zip`. 첫 회는 New Project → Upload Project. 이후에는 출력된 파일만 같은 경로로 업로드한다.
- 받아오기: Overleaf → Menu → Download → Source → `dinnno paper import <zip>`.
- Compiler: pdfLaTeX, main document: `main.tex`.
