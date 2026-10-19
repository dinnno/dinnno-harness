---
name: paper
description: dinnno 연구 프로젝트에서 논문 원고를 쓰는 세션을 열 때. 사용자가 "/paper", "논문 쓰자", "원고 이어서", "intro 써줘", "이 섹션 검토해줘", "Overleaf에서 고친 거 받아줘", "rebuttal 쓰자"라고 하면 쓴다. 사용자의 개괄식 메모를 tex 문장으로 옮기는 라운드를 반복하고, 수치는 metrics에서 생성한 매크로로만 쓰고, 섹션 검토는 다른 모델(Astra/Fable)에게 받고, Overleaf와는 zip으로 주고받는다. 실험 단위(plan → done)는 harness 스킬이다.
---

# paper — 원고 세션 하나

이 스킬을 부른 세션이 이 논문 원고의 팀장이다. 한 세션에서 `harness`와 `paper` 중 하나만 쓴다. 원고 세션은 plan/done을 쓰지 않는다. 진행은 `writing/README.md`의 섹션 상태 표와 "다음 시작점"에 남는다. 다음 세션은 이 대화가 아니라 그 파일을 읽고 이어간다.

원고 안의 모든 수치와 주장은 프로젝트의 실험 산출물에 근거해야 한다. 근거 없는 문장을 그럴듯하게 채우는 것이 이 스킬에서 가장 나쁜 실패다. 근거가 없으면 `\GAP{무엇이 없나}`로 남기고 사용자에게 묻는다.

## 1. 진입

`writing/`이 없으면 §2 init. 있으면 다음 순서로 한다.

1. "지난번 이후 Overleaf에서 고친 게 있나요?"를 묻는다. 있으면 Overleaf 메뉴의 Download → Source zip 경로를 받아 `dinnno paper import <zip>`부터 한다. 충돌(`CONFLICT`)이 나면 diff를 보여 주고 파일마다 어느 쪽을 살릴지 사용자에게 묻는다. 로컬에서 tex를 고치기 전에 항상 import가 먼저다. Overleaf에 올린 뒤에는 Overleaf 쪽이 원본이다.
2. import 출력의 "사용자 수정" diff가 Claude가 쓴 문장을 고친 것이면, 반복되는 패턴(용어 선택, 문장 길이, 헤지 강도, 관사·시제)을 `writing/STYLE.md` 후보로 한두 줄 제안한다. 사용자가 확인한 줄만 남긴다.
3. 읽는다: `writing/README.md`(상태 표, 다음 시작점), `writing/VENUE.md`, `writing/STYLE.md`, 다룰 섹션의 `writing/notes/<sec>.md`, `docs/RESEARCH_SPEC.md` §1·§4, 사실 대장(`writing/VENUE.md`의 `facts:` 줄이 가리키는 파일).
4. `dinnno paper check`를 돌려 남은 `\TODO`·`\GAP`·근거 없는 수치·마감 D-day를 본다.
5. "지난번 intro 3라운드까지 했고 답 안 된 질문이 2개 있습니다. 오늘은 intro를 마무리하고 method로 갈까요?"처럼 현황을 말하고 이번 세션의 섹션을 한 번 확인한다.

## 2. init (처음 한 번)

1. 학회와 연도를 묻는다. `references/venues/<venue>.md` 프리셋이 있으면 읽는다. 없으면 공식 CFP와 author guidelines를 읽어 같은 형식으로 프리셋을 먼저 만든다(학회마다 잘 안 바뀌는 성격만. 연도별 값은 프로젝트 쪽에).
2. 공식 템플릿을 받는다. 프리셋의 템플릿 출처에서 받아 `writing/`에 풀고, 받은 URL과 커밋·태그·날짜를 `VENUE.md`에 적는다. 그해 kit이 아직 없으면 직전 kit을 쓰고 "공개되면 교체 확인"을 `VENUE.md`에 적는다.
3. `templates/writing/`의 `README.md`, `VENUE.md`, `STYLE.md`, `numbers.yaml`, `notes/_template.md`를 깔고 `gitignore`는 `writing/.gitignore`로 복사한다. `preamble_addon.tex`도 쓴다. preamble_addon 내용은 템플릿의 preamble 끝에 붙인다(`\input{numbers}` 포함). 템플릿 예제 본문(예제 `sec/`, 예제 `main.bib`, `rebuttal.tex` 본문, teaser)은 `writing/reference/`로 옮겨 컴파일 대상에서 빼고, 그 자리에 섹션 제목과 `\TODO`만 있는 골격을 둔다. 예제 인용이 남으면 check가 bib 누락 ERROR를 낸다.
4. `VENUE.md`의 연도별 값(마감, 페이지 수, supplementary·rebuttal 규정, LLM 정책)은 공식 페이지에서 확인해 출처 URL과 확인 날짜를 붙인다. 확인 못 한 칸은 "미확인"으로 둔다.
5. 사실 대장을 정한다. 이미 있으면(예: `docs/CVPR_FACTS.md`) 그 파일을 `VENUE.md`의 `facts:`로 가리킨다. 없으면 `templates/PAPER_FACTS.md`를 `docs/PAPER_FACTS.md`로 복사하고, `done/`과 metrics에서 항목을 뽑는다. 이 추출이 크면 `fanout`으로 팀원에게 넘기고 팀장이 원천과 대조한다.
6. 프로젝트 `docs/ARCHITECTURE.md` 폴더 표에 `writing/` 한 줄이 없으면 넣는다.
7. `dinnno paper numbers`와 `dinnno paper export`를 돌리고, 첫 업로드 방법(Overleaf → New Project → Upload Project → zip, Compiler와 main document)을 안내한다.

## 3. 라운드 (원하는 만큼 반복)

**사용자 메모.** 사용자는 개괄식으로 생각을 나열한다. 받은 메모를 `writing/notes/<sec>.md`에 `## R{n} — {날짜}` 아래 원문 그대로 붙인다. 의도의 원본은 이 메모다. tex를 고칠 때도 메모와 어긋나면 메모가 이긴다.

**산출.** 한 응답에 네 가지를 낸다.

1. 문단 개요 표: 문단 번호, 역할(opening/challenge/insight/method/advantage/evidence/limitation), 첫 문장이 될 메시지 한 줄, 근거(사실 대장 ID, 인용 키, 또는 `GAP`).
2. `writing/sec/<sec>.tex` 본문 수정. 수치는 `numbers.tex` 매크로로만 쓴다. 매크로가 없으면 `numbers.yaml`에 원천을 추가하고 `dinnno paper numbers`를 돌린 뒤 쓴다. 원천을 모르면 `\GAP`.
3. claim-evidence map: `Claim | Evidence | Status(supported / needs evidence / weakened)`. Abstract와 Introduction의 주장은 전부 넣는다.
4. 사용자에게 묻는 질문 1~3개. 메모가 비었거나 서로 모순되거나 근거가 약한 곳이다.

섹션 규칙은 그 섹션 가이드 하나만 읽는다: `references/{abstract,introduction,related-work,method,experiments,conclusion}.md`. 예시가 필요하면 `references/examples/index.md`에서 해당 파일만. 로보틱스 실험 서술은 `references/robotics-addendum.md`. 전체 가이드를 한꺼번에 읽지 않는다. `STYLE.md`의 확정 줄은 매 라운드 적용한다.

**반복.** 사용자가 메모를 추가하거나 문장을 직접 고쳐 주면 다시 산출한다. 같은 섹션을 몇 번이고 돈다. 라운드가 끝날 때마다 `writing/README.md` 상태 표의 그 섹션 라운드 수와 남은 질문을 갱신한다.

**related work와 인용.** 후보 논문은 `research-second-brain` 스킬로 찾는다. bib 항목은 arXiv·DBLP·출판사 페이지의 공식 BibTeX만 쓰고, 기억으로 만든 bib은 넣지 않는다. 넣은 뒤 `dinnno paper check --bib`이 실재 여부를 확인한다.

## 4. 섹션 검토 (사용자가 "이 섹션 검토"라고 할 때)

1. `references/prompts/review_section.md`를 scratch에 복사하고 `{…}` 자리를 채운다. 입력은 파일 경로뿐이다. 이 세션의 해석이나 변명은 넣지 않는다.
2. `dinnno review --with codex <prompt> -o <scratch>/review_out.md`를 백그라운드로 돌린다. 두 번째 눈이 필요하면 `--with claude`도 따로 돌린다.
3. 출력 원문을 그대로 보여 주고 verdict만 맨 위로 올린다. `writing/reviews/<sec>.md`에 `## Round {r} — {날짜} — {모델}`로 append한다.
4. 무엇을 반영할지는 사용자가 고른다. 고른 것만 다음 라운드에 반영한다. `REVIEW FAILED`면 원문을 보고하고 검토를 대신 쓰지 않는다.

## 5. 제출 전 모의 심사

본문이 다 채워지고 `dinnno paper check`에 `\GAP`이 없을 때, 사용자가 원하면 한다. `references/prompts/mock_review.md`로 Astra(`--with codex`)와 Fable(`--with claude`)이 각각 따로 심사한다. 심사위원 3명(학회 심사 양식 기준)과 Devil's Advocate 구성이다. 결과는 `writing/reviews/mock_r{n}.md`에 둘 다 원문으로 둔다. 두 모델이 공통으로 짚은 것을 먼저 보고한다. "새 실험이 필요" 판정은 원고 세션에서 처리하지 않고 progress 결정 큐에 올려 harness 단위로 넘긴다.

## 6. rebuttal

실제 리뷰가 오면 `writing/reviews/official.md`에 원문을 붙이고, 지적마다 한 행인 `writing/reviews/rebuttal_matrix.md`를 만든다: `R#-n | 지적 요지 | 유형(오해/추가 설명/요청 실험/동의 못 함) | 대응 | 근거(사실 대장 ID·파일) | 원고 수정 위치`. 학회 규정(분량, 새 실험 허용 여부, 링크 금지)은 `VENUE.md`를 따른다. 행이 다 차면 `rebuttal.tex`를 쓰고, 각 문단에 대응하는 행 번호를 `%` 주석으로 남긴다.

## 7. 내보내기

`dinnno paper export`가 zip을 만들고 지난 export 이후 바뀐 파일 목록을 출력한다. 처음이면 zip 전체를 New Project로 올리게 하고, 이후에는 바뀐 파일만 Overleaf에서 같은 경로로 업로드(덮어쓰기)하게 안내한다. 사용자가 올렸다고 말하기 전에는 Overleaf 반영을 가정하지 않는다.

## 8. 종료

사용자가 "close"라고 하면 `close` 스킬(원고 세션 절)을 따른다. 아니어도 끝내기 전에 `writing/README.md`의 상태 표와 "다음 시작점"(다음 섹션, 답 안 된 질문, 미업로드 파일)을 갱신한다.

## 멈추는 지점

전역 규약의 것에 더해서: import 충돌 파일의 덮어쓰기, 학회 변경, 사실 대장의 기존 항목 수정·삭제, 원고의 주장을 실험 결과보다 강하게 쓰자는 요청(근거를 보여 주고 확인받는다). 그 밖의 라운드는 묻지 않고 돈다.

## 런타임 메모

Claude·Grok `/paper`, Codex `$paper`. LaTeX 컴파일은 이 머신에서 하지 않는다. 컴파일 오류와 페이지 수는 사용자가 Overleaf에서 보고 알려 준다.
