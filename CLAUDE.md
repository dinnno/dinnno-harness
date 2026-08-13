# Global behavioral guidelines

Behavioral guidelines for Claude Code across all projects. Project-level CLAUDE.md adds context on top of this.

**우선순위:** 본 파일(전역 4원칙) > 커맨드 문서(`/harness` 등 — 세션 워크플로 정본) > 프로젝트 `CLAUDE.md`(도메인 컨텍스트) > 프로젝트 `docs/**/_GUIDE.md` 또는 폴더 `CLAUDE.md`(폴더별 규약). 충돌 시 위가 이긴다. 단, 그 폴더별 규약이 명시한 산출물 형식·네이밍은 그 폴더 안에서 우위.

**진입점 통일:** dinnno-harness 깐 프로젝트에서는 모든 작업이 `/harness`로 진입. `/harness` 없이 시작된 요청도 본문 전체(§경계선 포함 §1–§5)를 묵시 적용한다(현황 적재·단위 confirm·세션 종료 계약 포함). (예외: `/audit`과 그 `HANDOFF_TO_OPUS.md` 인계 세션, `/issue` 파일만 읽고 재시도하는 세션은 해당 문서의 워크플로를 따른다.) 현재 세션 모델이 Fable/Mythos 계열이 아니면(Opus·Sonnet 등) 다른 작업을 시작하기 전에 `/opus-guide`를 먼저 로드한다.

**Research 목표 지향:** 이 하네스는 논문 한 개 단위의 연구 프로젝트용. `docs/RESEARCH_SPEC.md`의 thesis(= 논문 contribution)가 모든 단위의 목적지.

- 단순 코드 수정·bug fix 모드 ❌. 모든 plan은 "모듈 제안·개발", 모든 done은 "실험 설계·수행·검증"의 한 단계.
- 작업 직전 자문: "이 변경이 thesis의 어느 비교 축(`RESEARCH_SPEC §4`)을 움직이나?"
- Done §4 다음 plan 후보는 **paper-impact** 기준으로 — 권위 저널/최우수 학회 publish 시 어떤 contribution 라인이 되는지 한 줄. 단순 엔지니어링 follow-up은 후보 ❌.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

**보고 스타일 (모든 모델·모든 세션):** 결론 먼저 3줄 이내, 상세는 사용자가 파고들 때. 한 번에 한 주제 — 여러 주제면 "지금은 X만" 선언. 사용자에게 요구하는 결정은 1~2개씩. 하네스 내부 용어(HARD/SOFT·pay-grade 등)는 처음 쓸 때 1줄 정의. 줄글 정보 폭탄 ❌.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.** State assumptions explicitly; if uncertain or multiple interpretations exist, ask — don't pick silently. If a simpler approach exists, say so and push back when warranted. If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.** No features, abstractions, or flexibility beyond what was asked. No error handling for impossible scenarios. If you write 200 lines and it could be 50, rewrite it.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it — don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

예외 — 하네스 상태 문서(`progress.md`·`HANDOFF_*`·references `_INDEX.md`)의 stale 상태 블록 정리는 "인접 개선"이 아니라 그 문서의 본연 기능이다. 발견 시 정리를 제안하고 confirm 후 수행한다(이력 문서 done_v*·RESEARCH_SPEC 본문은 불가침 그대로).

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

## Domain context: robotics AI research

The user is a robotics AI researcher. Projects typically include:
- **Simulators**: Isaac Lab/Sim, MuJoCo, Gazebo, PyBullet
- **Real robots**: ROS 2 nodes, teleop (VIVE/MANUS), deployment
- **Learning pipelines**: training/eval scripts, ablations, checkpoints
- **Artifacts**: data, ckpt, runs, wandb logs — all kept outside git

Conventions:
- One experiment = one `configs/*.yaml`. Code does not encode experiment params.
- Reproducibility = fixed seed + config file + git commit hash + dataset snapshot (git 밖 `data/`는 name@version 또는 manifest hash로 고정).
- Real-robot actuation(물리 하드웨어로 명령 전송)은 사용자 confirm 없이 ❌ — 파일 삭제보다 높은 비가역 리스크 (sim은 해당 없음).
- **GPU-first**: 텐서 연산은 GPU 경로로 작성. CPU 폴백은 GPU 커널 부재를 확인한 뒤 명시적 선택일 때만 — 라이브러리 CPU 커널은 대개 청킹이 없어 (N×M) 중간 텐서를 호스트 RAM에 통째로 만든다.
- **호스트 RAM은 이웃 세션과 공유**: 한 프로세스의 OOM이 같은 데스크톱 스코프의 다른 프로젝트 세션을 전부 끌고 내려간다. 처음 돌리는 스크립트·벤치·전처리는 `systemd-run --user --scope -p MemoryMax=8G -- python x.py`, 그 외엔 실행 전 peak RSS 한 줄 추정(`--workers` 기본값 + `mp.spawn` Pool은 부모 데이터를 worker 수만큼 복사).
- `libs/` is read-only (vendored third-party). Never edit.
- Prefer Python; use shell only for thin launch scripts.
- Second brain vault: `<wrapper>/tools/oh-dinnno-opsidian` (dinnno-research-wrapper 안, 예: `~/Workspace/dinnno-research-wrapper/tools/oh-dinnno-opsidian`) — 연구 문헌 위키(자체 CLAUDE.md 스키마, 머신당 1클론·프로젝트마다 ❌). wrapper 미배치 머신은 `~/Workspace/sangjun_noh/oh-dinnno-opsidian`이 fallback. 질의 규약은 `/harness` §4.
