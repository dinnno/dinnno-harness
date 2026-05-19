# plan_v{N}_{short-name}

> 이 파일은 `templates/docs/plans/_plan_template.md`를 복사한 것. 모든 섹션을 채우거나 "N/A — 사유" 명시.

## 0. 짝 (paired)

- spec 줄: `docs/RESEARCH_SPEC.md §{section} L{line}` "..."
- 이전 done: `docs/done/done_v{N-1}.md` (있으면)

## 1. 타겟 limitation

(RESEARCH_SPEC §3 failure taxonomy에서 인용 한 단락. 이 plan이 어느 failure를 노리는가)

## 2. 최소 변경 (proposed module)

(파일 경로 + 시그니처 수준. "어떤 모듈을 제안하는가" — 단순 코드 수정 ❌)

## 3. 검증 설계

- ablation: (RESEARCH_SPEC §6과 매핑)
- metric: (RESEARCH_SPEC §4 비교 축)
- 실행: (커맨드, 실로봇/sim, 예상 run 시간)

## 4. 실패 시 분기

(검증 실패 시 다음 시도 1-2개 미리)

## 5. 세션 로그

- {YYYY-MM-DD} {session-summary 한 줄}

## 6. TODO (working checklist)

day-hours 단위 작업. 세션 시작 시 첫 미체크 항목부터, 세션 종료 시 체크 갱신.

- [ ] {작업 1: dataset loader 구현 + 단위 테스트}
- [ ] {작업 2: config_v1.yaml 작성}
- [ ] {작업 3: sweep 첫 5 run 돌리기}
- [ ] ...
