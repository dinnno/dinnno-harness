---
description: 최신 plan_v{N}을 Execute 전에 fresh Codex(gpt-5.6-sol·xhigh)가 적대 심층 검토 — thesis 정합·모델 설계·학습·평가·인과 귀속을 CRITICAL/HARD/SOFT로 공격하고 프로젝트 파일은 수정하지 않는다. 결과는 대화에 원문 + plan_v{N}_codex.md 라운드 append. plan 작성 직후 "Execute 시작?" confirm 전, 또는 사용자가 "codex로 plan 리뷰/공격해줘" 요청 시. done 리뷰·코드 리뷰에는 쓰지 않는다.
---

# /plan-redteam — plan 적대 심층 리뷰 (fresh Codex)

plan을 쓴 세션은 자기 설계를 관대하게 본다. Execute에 GPU-시간을 태우기 전에 **이 대화를 모르는 fresh Codex**가 plan을 격추하려 시도한다 — writer≠reviewer(`/harness` §4)의 plan판, `/close`와 동형. 리뷰어의 임무는 개선 제안이 아니라 **격추**다: 살아남은 plan만 Execute할 가치가 있다.

## 1. 대상·source manifest

- 대상: 인자 없으면 `docs/plans/plan_v*.md` 최고 버전(`_template`·`*_codex.md` 제외, `sort -V`). 인자로 경로·버전 지정 가능.
- 최신 done_v{M} ≥ plan_v{N}이면 이미 닫힌 단위일 수 있다 — 한 줄 경고 후 대상 confirm.
- **source manifest** = 파일 경로 목록. Claude의 해석·요약·자평은 어떤 형태로도 동봉 ❌ (오염 방지 — fresh여야 의미가 있다):
  - `docs/plans/plan_v{N}_*.md` (필수)
  - `docs/RESEARCH_SPEC.md` — §1 Thesis·§4 비교 축을 기준으로 지정 (필수)
  - `docs/progress.md` · `docs/LEARNINGS.md`
  - 직전 `done_v{N-1}` (있으면 — 직전 실측과의 모순 검사용)
  - 기존 `plan_v{N}_codex.md` (있으면 — 라운드 이어가기·중복 지적 방지)
- 없는 파일은 manifest에서 빼고 프롬프트에 "부재"를 명시한다 — Codex가 추측으로 채우지 않게.
- 프로젝트 규약은 `-C <프로젝트 루트>` 실행으로 Codex가 `AGENTS.md`를 네이티브 적재한다. AGENTS.md 부재 프로젝트만 루트 `CLAUDE.md`를 manifest에 추가.

## 2. 리뷰 프롬프트 — 파일로 작성

프롬프트는 세션 scratchpad에 `redteam_prompt.md`로 저장하고 CLI에는 **경로만** 넘긴다 — 긴 본문을 셸 인자로 넘기면 특수문자에서 잘린 채 조용히 일부만 전달된다. 골격(XML 블록):

- `<task>` — manifest 파일을 직접 읽고 plan_v{N}을 적대 검토하라. 질문은 "어떻게 개선할까"가 아니라 **"이 plan은 왜 실패하는가"**다. 아래 7축 각각에서 실제로 격추를 시도하고, 정말 결함이 없으면 그 축에 `no finding` + 근거 1줄.
- 검토 축 7:
  - ① **thesis 정합** — plan이 RESEARCH_SPEC §1/§4의 어느 축을 실제로 움직이나. 못 움직이면 단위 자체가 무의미
  - ② **모델·표현 설계** — 아키텍처·입력 표현·귀납 편향이 타겟 limitation과 정합하나
  - ③ **학습 설계** — objective·데이터 규모/분포·최적화·**정보 누수**(train/eval 경계)
  - ④ **평가 설계** — 메트릭이 주장을 실제 증명하나 · baseline 공정성 · seeds×rollouts·통계 검정력
  - ⑤ **인과 귀속** — 성공/실패의 원인을 confound 없이 분리하나 · 빠진 ablation
  - ⑥ **실행·재현 리스크** — config·seed 고정 · 루프 예산·정지 조건 · 성공 임계값의 사전 선언 여부
  - ⑦ **이력 모순** — LEARNINGS·직전 done의 실측과 충돌하는 가정
- 심각도 (finding마다 하나 — `/harness` §경계선의 차단 의미와 동형):
  - `CRITICAL` — thesis-level 결함: 실행해서 결과가 나와도 논문 주장이 성립 안 함 → plan 재설계
  - `HARD` — Execute 전 필수 수정: 그대로 실행하면 해석 불가·재실험 확정
  - `SOFT` — 비차단 개선: 진행 가능(다음 단위로 이월해도 되는 것 포함)
- 심각도 보정 — 차단(CRITICAL/HARD)의 유일한 기준은 **"이대로 실행하면 그 실험·GPU-시간이 낭비되는가"**다. 완벽성·우아함·엔지니어링 위생은 낭비를 만들지 않는 한 SOFT. 역방향도 같다 — 사소해 보여도 결과 해석을 무효화하면 HARD로 올려라. 심각도 인플레이션은 리뷰 실패다 — HARD가 많다고 좋은 리뷰가 아니다(`/harness` §경계선의 "과잉 confirm = 과잉 자율만큼 나쁜 실패"와 동형).
- `<grounding_rules>` — 모든 finding은 `파일 §절` 인용 근거 필수. 일반론("~하면 좋습니다") ❌ — 이 plan의 구체 수치·차원·자유도를 실제로 따져라(데이터 크기 vs 파라미터 수, 통계 검정력, 예산 산술 등). 읽지 못한 파일은 지어내지 말고 `ACCESS FAILED`로 보고.
- `<structured_output_contract>` — 정확히 이 순서: `## Round {r} — {날짜} — {모델}` → `READ OK:` 접근 확인 목록(+`ACCESS FAILED:`) → CRITICAL → HARD → SOFT findings(각: 제목 · 근거 인용 · 왜 치명적인가 · 최소 수정 1줄) → 축별 no-finding → verdict 1줄: `REDESIGN | FIX FIRST (HARD n건) | EXECUTE OK`.
- 무수정 계약 — read-only 검토. 어떤 파일도 수정·생성 ❌.

## 3. 호출 — Codex host adapter (`/harness` §4 정본 준수)

실행 시작 시각을 먼저 기록한다(④ 무수정 검증용).

```bash
codex exec -s read-only -C <프로젝트루트> -m gpt-5.6-sol -c model_reasoning_effort=xhigh \
  --skip-git-repo-check -o <scratch>/redteam_out.md \
  "다음 파일을 읽고 그 안의 지시를 그대로 수행하라: <scratch>/redteam_prompt.md — read-only 검토다. 어떤 파일도 수정하지 마라." \
  > <scratch>/redteam_log.txt 2>&1
```

- xhigh는 수 분~수십 분 — background 실행 + 완료 통지 대기, 주기 폴링 ❌.
- 정상 sandbox(read-only)가 host에서 재현 가능하게 실패하면(예: `bwrap ... Operation not permitted` — Codex가 파일을 못 읽어 거부·날조) 원문 오류를 로그에 남기고 **이번 invocation 하나만** `-s danger-full-access`로 fallback. unsafe mode를 기본값으로 저장 ❌.
- **성공 판정 4종** (research-loop §3 계약과 동일 — 전부 만족해야 성공):
  ① exit success ② `-o` 출력 non-empty ③ 출력의 `READ OK`가 필수 파일(plan·SPEC)을 포함 ④ 무수정 — `git -C <루트> status --porcelain` 결과가 실행 전과 동일(fallback이었다면 `find <루트> -newermt '<시작시각>' -type f -not -path '*/.git/*'`도 확인).
  하나라도 실패 = **`CODEX CHANNEL FAILED`** — Claude가 리뷰를 흉내 내 채우지 ❌, 원문 오류와 함께 보고하고 정지.

## 4. 결과 착지

- Codex 출력 **원문 그대로** 대화에 표시 — 맨 위에 verdict 1줄만 뽑아 올리고, 첫 표시에 Claude의 요약·반박·재배열 ❌ (사용자가 물으면 그때 해석).
- `docs/plans/plan_v{N}_codex.md`에 라운드 append(`/harness` §4 리뷰 1파일 규칙 — 라운드마다 새 파일 ❌). 신설 시 대상 plan 경로 1줄 헤더.
- 반영은 이 커맨드 밖 — 사용자가 "타당한 지적 반영해" 지시 후 일반 Setup 흐름으로. plan 자동 수정 ❌.
- 라운드 규칙은 `/harness` §4 그대로: 자동 재리뷰 ❌ · 2라운드 후에도 CRITICAL/HARD 잔존 시 계속 여부 confirm(HARD) · thesis-level claim 뒤집힘 시 즉시 1라운드 추가.

## 하지 않는 것

- 프로젝트 파일 수정 ❌ — 유일한 쓰기는 `plan_v{N}_codex.md` append(Codex가 아니라 Claude가 수행).
- 이 세션의 자평·결론을 Codex에 전달 ❌.
- `CODEX CHANNEL FAILED`를 Claude 대필로 채우기 ❌.
- done 리뷰 ❌ — 그건 `/harness` §4의 `done_v{N}_codex.md` 흐름.
- Execute 시작 ❌ — verdict가 `EXECUTE OK`여도 "이 plan으로 Execute 시작?" confirm은 별도(HARD).
