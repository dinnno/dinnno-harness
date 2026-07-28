---
description: research 하네스의 다이나믹 워크플로우·장시간 실행 운영 규칙(rules-only, lazy) — (sweep)·병렬 Execute에서 Workflow/루프 도구를 쓰기 직전에 로드. 워크플로를 시작하지 않는다. efficient-retarget 실전(2026-07)에서 검증된 워크어라운드의 승격판.
---

# /workflow-ops — 워크플로·장시간 실행 운영 규칙

`/harness` §4의 루프 도구 라인을 구체화한다. 여기 규칙은 실전에서 에이전트 사망·산출물 증발로 학습된 것들이다 — 어기면 같은 방식으로 죽는다.

## 1. 스테이지 모델링

- 구현 스테이지 = implementer 재사용(`model: opus`·effort high). 설계·verdict 스테이지만 상위 모델 — effort는 `/harness` §4 라우팅 상한(Opus 계열 high, xhigh 이상은 spec-수준 전용)을 따른다. agent()의 model/effort 오버라이드는 확신 있을 때만 — 기본은 상속.
- Workflow 안에서 신규 가설 생성·가설 경계 넘기 ❌ (`/harness` §4). verdict의 최종 판정은 가이드 세션 몫 — 워크플로는 수치·아티팩트만 회수한다.
- worktree 격리는 파일을 병렬로 만지는 스테이지에만 (셋업 비용 있음).

## 2. 장시간 실행 (sim·학습)

- **이 문서의 규칙은 서브에이전트에 자동 상속되지 않는다** — 코디네이터가 §2·§3의 해당 조항을 각 스테이지 agent() 프롬프트에 명시적으로 주입한다.
- **서브에이전트 안에서 Monitor는 비차단** — 대기 수단으로 무용(실전: 에이전트 2개 사망 원인). 완료 마커 파일 polling으로 대기: `timeout 550 bash -c 'until [ -f <marker> ]; do sleep 15; done'`을 Bash 10분 캡 안에서 체이닝(**Bash 도구 `timeout` 파라미터를 600000으로 올릴 것** — 기본 120초면 한 창이 5배로 쪼개진다). 마커는 실행 스크립트가 종료 시 성공/실패 구분해 기록, polling 사이 프로세스 생존 확인(`kill -0`), 총 대기 상한 = plan §3 예산 — 상한 도달·프로세스 사망 시 대기를 멈추고 실패로 보고한다.
- 실행 진행 중 도구 호출 없이 턴 종료 ❌ — 하네스가 에이전트를 즉시 종료한다.
- structured-output enforce 신호를 받아도 실행 중이면 응답하지 말고 차단 대기를 계속한다.
- 이 절은 워크플로 서브에이전트 한정 — 메인 세션에서는 `run_in_background` + Monitor가 정상 동작(`/harness` §3).

## 3. 스크립트 견고성

- agent() 결과는 사망 대비 `.filter(Boolean)` / try-catch (실측: StructuredOutput 없이 죽는 빈도 ~2/16).
- resume 시 args가 JSON 문자열로 도착할 수 있다 — 파싱 가드 없으면 조건부 스테이지가 조용히 스킵된다.
- 스크립트 안에서 Date.now()/Math.random() 사용 불가 — 타임스탬프·시드는 args로 주입.

## 4. 산출물 규율

- workflow 스크립트를 세션 디렉토리에 방치 ❌ — 프로젝트 영구 경로(예: `scripts/workflows/`)에 저장한다. 세션 디렉토리는 증발한다(실전 사례: 재사용 템플릿이 세션과 함께 소멸).
- **영구 문서(HANDOFF·plan·done)에 /tmp·세션 스코프 경로 인용 ❌** — 인용 전 프로젝트 영구 경로로 복사.
- 스윕 결과는 progress.md Ablation Matrix 셀로, trial 로그는 ledger로 — 워크플로 종료 시 회수 누락이 없는지 가이드 세션이 확인한다.
