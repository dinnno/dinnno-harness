---
description: 연구·구현이 뫼비우스(같은 고민·수정의 순환)에 빠졌을 때 그 흐름을 vault fable/issues/에 박제 — 사용자가 "뫼비우스다/막혔다/또 돈다"를 표하거나 /issue 호출 시. 인자 없이 불렸고 현재 대화에 새 막힘이 없으면 open issue 소비 모드. 해결된 교훈 1줄(LEARNINGS)·단순 TODO(plan §6)에는 쓰지 않는다.
---

# /issue — 막힘 박제 (뫼비우스 → vault)

뫼비우스의 원인 절반은 "이미 버린 옵션을 아무도 기억 못 해 다시 시도"다. 이 커맨드는 그 순환을 파일로 끊는다: 고민의 흐름을 박제 → 신선한 컨텍스트(Fable 세션·새 터미널·codex)가 그 파일만 읽고 이어받는다. 연구 설계 막힘(레이블 정의, 모듈 디자인)과 안 풀리는 버그를 구분하지 않는다 — 형식은 하나, 소비자만 "다음에 원하는 것"에서 갈린다.

vault 경로: 전역 CLAUDE.md의 Second brain vault 항목. 경로가 없는 머신이면 사용자에게 확인.

## 작성 모드 (기본 — 막힘이 발생한 세션에서)

1. `fable/issues/YYYY-MM-DD_{프로젝트}_{slug}.md` 작성 (slug는 영어 kebab-case). 아래 스키마, **이 대화에서 실제 오간 것만** — 대화에 없던 옵션·논거를 지어내 채우기 ❌, '사용자 직감'은 원문 인용.
2. **착지** — harness 프로젝트면 `progress.md` 결정 큐에 1줄: `- [ ] {날짜} [issue] {한 줄} ← fable/issues/{파일명}`. 프로젝트 밖이면 생략.
3. **보고** — 파일 경로 + "다음에 원하는 것" 1줄. vault commit/push는 사용자 몫.

```markdown
---
type: issue
project: {프로젝트명}
status: open          # open | resolved
created: {YYYY-MM-DD}
tags: [{영어 kebab}]
---
# 막힌 것 한 줄

## 왜 지금 필요한가
(안 풀리면 뭐가 멈추나)

## 고민/시도의 흐름  ← 본체
(옵션·가설별: 오간 논거, 왜 채택도 기각도 못 했나.
 도는 지점을 명시 — "A 단점 → B → B 단점 → 다시 A, k바퀴째")

## 사용자 직감 (원문 그대로)

## 다음에 원하는 것
(하나 + 이유: Fable 세션 심문 / 새 터미널이 이 파일만 읽고 재시도 / codex 독립 진단)

## 결론 (해결 세션이 채움 → status: resolved)
(무엇으로 풀렸고 어디에 반영됐나 — LEARNINGS·plan·spec)
```

## 소비 모드 (인자 없이 호출 + 현재 대화에 새 막힘 없음)

1. `fable/issues/`의 `status: open` 목록을 표로 제시(파일 / 막힌 것 한 줄 / created) → 사용자가 선택.
2. 선택 파일을 읽고 "다음에 원하는 것"대로 진행: 심문(흐름 속 전제를 공격), 재시도, codex dispatch.
3. 풀리면 결론 섹션 채움 + `status: resolved` + 교훈이면 프로젝트 `LEARNINGS.md` 1줄. 안 풀리면 이번 라운드를 흐름에 append (누적 — 덮어쓰기 ❌).

## 하지 않는 것

- 박제 없이 즉석 해결 재시도 ❌ — 이 커맨드가 불린 시점은 이미 순환 중이다. 먼저 박제.
- vault의 `wiki/`·`index.md`·`log.md` 갱신 ❌ — issues는 fable/ 박제 레이어. 정제 결론의 wiki 반영은 소비 세션 몫.
- vault git commit/push ❌ (사용자 몫).
