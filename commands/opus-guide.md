---
description: 비-Fable 모델 세션용 행동 보강 규칙(델타 레이어) — /harness 진입 전에 로드. 워크플로를 시작하지 않는다(rules-only). HARD/SOFT 경계선 정본은 /harness §경계선(모델 무관 — 여기 아님). Opus 5+ 세션은 §1.5(Opus 5 델타)만 의미 있다(나머지는 기본 행동), §2–§7 전체 적용은 Opus 4.8 이하·Sonnet 등. Fable/Mythos 세션은 로드 불필요.
---

# /opus-guide — 비-Fable 모델용 행동 보강

시스템 프롬프트의 복사가 아니라, Fable 5는 자연히 지키지만 다른 모델은 놓치기 쉬운 행동을 "그 순간의 트리거"로 굳힌 델타 레이어다. 워크플로를 시작하지 않는다 — 로드 후 `/harness`로 진입하라 (예외: `HANDOFF_TO_OPUS.md` 인계 세션은 `/harness` 대신 그 파일의 지시를 따른다).

**모델 분기:** §2–§7은 Opus 4.8 이하의 지시 추종력에 캘리브레이션됐다. **Opus 5+ 세션은 §1.5(Opus 5 델타)만 취하고 §2–§7은 기본 행동으로 간주하라** — Opus 5는 과잉 보강 지시와 충돌하며, 지시를 단순하게 둘수록 성능이 오른다. 단, HARD/SOFT 경계선·세션 종료 계약·종료 보고(기승전결)·AFK push는 모델 델타가 아니라 **모델 무관 사용자 계약**이다 — 정본은 `/harness` §경계선·§3·§5이고 모든 모델 세션에 적용된다(이 문서에는 없다).

**우선순위:** 전역 `~/.claude/CLAUDE.md`(4원칙) > 커맨드 문서(`/harness` 등) > 프로젝트 `CLAUDE.md` > 폴더 `_GUIDE.md` > **이 문서**. 충돌 시 항상 하네스가 이긴다. 이 문서는 하네스가 침묵하거나 미분화한 영역만 채운다. 규칙 본문은 영어(비-Fable 모델의 지시 추종력·원문 대조용), 리드는 한국어.

## 1. Boundary Map — `/harness` §경계선으로 이관 (2026-08-08)

HARD/SOFT 경계선은 모델 무관 공통 계약이라 이 문서에 없다 — 정본은 `/harness` §경계선. (autoloop) 인가의 세부 범위는 `docs/LOOP.md` L3 allowlist·L4 예산, kill/NO-GO 게이트는 `done/_GUIDE` §Kill/Pivot 그대로.

## 1.5 Opus 5 델타 — Opus 5+는 이것만 추가로

- Effort: high is the ceiling for implementation and routine verdicts; raise to xhigh/max only for spec-level judgment (measured: past high, quality drops while cost multiplies).
- Completion claims: never report "done" without the run log or artifact path attached; a verification that did not run is reported as "미실행", never as done.
- Factuality: numbers or claims taken from external papers/docs do not enter a done file without source-text confirmation — dispatch codex for the check.
- Harness convention that survives the slim-down: every done §2 metric still goes in a table with seed, config path, commit hash + plot file path + one line naming the `RESEARCH_SPEC` §4 axis it supports (the paper-grade rule, in full). "개선됐다" 같은 산문 수치 금지.

## 2. Turn Completeness — 턴과 세션의 완결

- Before ending any turn: if your last paragraph is a plan, a promise ("이제 ~하면 됩니다", "I'll…"), or leaves an unchecked plan §6 item — do that work now. Stop only at a HARD point or on input only the user can provide.
- 완결성 ≠ chain: if the remaining work belongs to the *next* hypothesis, do NOT do it — write it into done §4 as a candidate. 중도 포기와 자동 chain은 둘 다 실패다.
- Your final message must restate every deliverable of the turn: files written (paths), metrics measured, verdicts reached. Text between tool calls is invisible to the user.
- Never wrap up because the session feels long. If context was summarized mid-session, Read the current `plan_v{N}` §6 first, then resume from the first unchecked item.
- 세션 종료 계약·종료 보고 형식은 `/harness` §5 (모델 무관 — 여기 아님).

## 3. Context Economy — 적재가 곧 후반 완주율

컨텍스트 낭비는 후반 턴의 지시 유지력을 직접 깎는다.

- Session entry loads only the `/harness` §1 list: `RESEARCH_SPEC.md`, `progress.md`, `LEARNINGS.md`, current plan (+ `plans/`·`done/` 마지막 v{N}은 파일명 확인만, 싱크 체크는 §1 규정 범위만 — 위생 스캔은 `/tidy` 몫) (an (autoloop) unit additionally loads docs/LOOP.md). Past done/plan: refer via progress timeline pointers; open a specific section only when a specific number is needed.
- Before any Read — PDF, file over ~1 MB, or log over ~500 lines: do not Read here. Dispatch codex:rescue (logs: try tail/grep first). 임계값은 초기 추정치 — 어긋난 사례는 LEARNINGS에 적고 수치만 조정.
- Read only the range you need from large files. Never re-read a file you just edited.

## 4. State-Change Guard — 증거 없이 상태를 바꾸지 않는다

- Before rm / kill / config edit / checkpoint overwrite / restart / sending a command to a real robot: state in one line what evidence ties THIS action to THIS cause. A familiar-looking error is not evidence — verify before acting on pattern recognition.
- Failure levels — `/harness` "실패 시 자동 재시도 ❌"의 세분이다(하네스의 '실패'는 experiment-level을 뜻한다). **code-level** (import error, typo, shape mismatch; cause identified, plan unchanged) *and* rerun is cheap → fix and continue, no asking. **experiment-level** (diverging loss, hypothesis-contradicting result, second failure after one fix) → report with raw output and wait (HARD). 원인이 code-level이라도 재실행이 비싸면(수 시간 GPU 이상) 재실행 전 보고 (HARD).

## 5. Question Discipline — 묻기 전에 세 갈래

- Before asking: (1) answerable from the repo? → read it. (2) conventional default exists? → pick it, note the choice in one line. (3) genuinely user-owned (spec slot, hypothesis boundary, compute budget)? → ask, batched at the next HARD point (진행을 막는 질문은 즉시 — §2).
- **결정 카드:** at every HARD point needing a user decision (unit confirm, Execute start, done §4 selection): recommendation ×1 + 이유 1줄 + strongest alternative ×1 + 각 후보의 예상 소요·GPU 시간. 사용자가 1분 안에 결정할 수 없는 형태로 내밀지 마라.
- Exception — init/spec units: slots are filled only from the user's own words; your draft is a proposal, not a fill (sleepwalking 방지, `docs/_GUIDE.md` 참조).

## 6. Delegation & Waiting — 위임했으면 두 번 안 하고, 기다리지 않는다

- Delegation triggers: `/harness` §4를 따른다. After delegating a search, never redo it yourself. The subagent's final message is invisible to the user — carry its conclusion into your own final message.
- A command likely to run over ~2 minutes: `run_in_background` + `Monitor`, never foreground-wait. While training runs, prepare the Verdict *inside the current hypothesis*: eval/plot scripts, done §1 skeleton, summary dispatch for related pending references (SOFT announce). When the monitored run completes: chain eval → compare against plan §3 성공 임계값 → draft done §1–§2. In an (autoloop) unit the completion chain is eval → J·guard → keep/rollback → ledger line → next trial (LOOP.md §운영). If the comparison shows an experiment-level anomaly, report raw output and wait (HARD) instead of finalizing. 할 일이 없으면 그렇게 보고하고 대기.
- AFK push 계약은 `/harness` §3 자리 비움 모드 (모델 무관 — 여기 아님).

## 7. 압축 체크리스트

1. Last paragraph a plan or promise? Do it now — unless it's the next hypothesis (→ done §4).
2. Every deliverable restated in the final message?
3. plan §6 / §5 log / progress.md updated before closing?
4. Context summarized? Re-read plan §6, resume from first unchecked.
5. About to Read a PDF / >1 MB / >500-line log? → codex:rescue.
6. About to rm/kill/edit config/overwrite ckpt? Evidence→cause→action in one line first.
7. Experiment-level failure? Report raw output, wait. Code-level & cheap rerun? Fix, continue.
8. About to ask? repo→read · default→pick&note · user-owned→decision card at next HARD point.
9. Delegated? Don't redo it; carry the conclusion into your final message.
10. Run >2 min? Background + Monitor; prepare Verdict while waiting; on completion, chain eval→plan §3 threshold→done draft.
11. First sentence = verdict with numbers; failures verbatim; no arrow chains.
12. Thesis/axis-changing judgment? Flag for a higher-tier session and stop.
