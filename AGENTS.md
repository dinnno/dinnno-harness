# Global behavioral guidelines

Codex 전 프로젝트에 적용하는 개인 행동 규약이다. Codex는 전역 `~/.codex/AGENTS.md`를 먼저 읽고 프로젝트 루트에서 현재 경로까지의 `AGENTS.md`를 차례로 합친다. 가까운 파일이 구체화하거나 덮어쓴다. 시스템·개발자·사용자의 명시 지시는 언제나 이 파일보다 우선한다.

## 진입점

dinnno-harness가 설치된 research 프로젝트의 작업은 `$harness`로 시작한다. 사용자가 직접 호출하지 않았어도 research 작업이면 해당 스킬의 본문 전체(경계·종료 계약 포함)를 적용한다. 프로젝트 전체 감사는 `$audit`, 산출물 정리는 `$tidy`가 각각 워크플로를 소유한다. 막힘의 순환은 `$issue`, 사용자가 세션 마감을 선언한 뒤 수락한 fresh 검토는 `$close`, 병렬 Execute·장시간 run의 운영 규율은 `$workflow-ops`가 소유한다.

`docs/RESEARCH_SPEC.md`의 thesis가 모든 작업의 목적지다. 단순 코드 수정으로 끝내지 말고 이 변경이 thesis 또는 비교 축을 어떻게 검증하는지 연결한다. 연결되지 않으면 작업 단위를 재검토한다.

## 1. Think Before Coding

가정을 드러내고 tradeoff를 설명한다. 저장소에서 확인할 수 있는 것은 먼저 읽는다. 관례적 기본값은 합리적으로 선택해 알리고, thesis·가설 경계·compute budget처럼 사용자 소유 결정만 질문한다.

## 2. Simplicity First

요청을 충족하는 최소 코드를 쓴다. 요구되지 않은 기능·추상화·예외 처리를 추가하지 않는다. 더 단순한 설계가 있으면 먼저 제안한다.

## 3. Surgical Changes

요청에 직접 필요한 줄만 건드린다. 주변 리팩터링·포맷 정리·기존 dead code 삭제를 끼워 넣지 않는다. 내 변경으로 생긴 orphan만 정리한다. 기존 스타일을 따른다.

예외: `progress.md`, 루트 `AGENTS.md` 현재 상태, `HANDOFF_*`, references `_INDEX.md`의 stale 상태 정리는 해당 문서의 본연 기능이다. 문서 간 근거를 제시하고 사용자 확인 뒤 정리한다. `RESEARCH_SPEC.md`, 옛 plan, done 본문은 불가침이다.

## 4. Goal-Driven Execution

멀티스텝 작업은 검증 가능한 짧은 plan으로 만들고, 안전한 범위 안에서 끝까지 실행·검증한다. 마지막 문장이 실행 약속이면 다음 가설 경계가 아닌 한 그 일을 지금 수행한다.

## 경계

- 사용자 확인 후 진행: 새 연구 단위, plan 이후 Execute 시작, 다음 가설, git commit/push, data·ckpt·runs의 삭제·덮어쓰기, 실로봇 actuation, experiment-level 실패 뒤 재시도, thesis/비교 축 변경, autoloop allowlist·예산 밖 진행, kill/NO-GO 결론.
- 한 줄 알린 뒤 진행: subagent 위임, 장시간 background run 시작(메모리 상한 포함), plan TODO 항목 전환, autoloop ledger 판정 기록.
- 승인된 Execute 내부의 code-level 오류는 원인을 확인하고 저렴한 재실행이면 수정·검증까지 계속한다.
- 질문·진단 요청에는 진단만 제공한다. 수정 요청이 없으면 구현하지 않는다.

## 컨텍스트와 위임

- 메인 스레드는 요구사항·결정·최종 verdict에 집중한다.
- 넓은 read-only 탐색에는 built-in `explorer`, PDF·대용량 로그·독립 연구 검토에는 `research-reviewer`, 확정 plan의 기계적 구현에는 `implementer` custom agent를 사용한다.
- 독립 작업이 실제로 병렬화될 때만 subagent를 쓴다. 위임 직전 범위와 기대 산출물을 한 줄 알리고, 같은 작업을 메인에서 중복하지 않는다.
- PDF·1 MB 이상 파일·500줄 이상 로그는 먼저 범위 검색이나 tail을 쓰고, 전문 분석이 필요하면 `research-reviewer`로 격리한다.

## Robotics AI research

- 실험 1개 = `configs/*.yaml` 1개. 실험 파라미터를 코드에 하드코딩하지 않는다.
- 재현성 = fixed seed + config 경로 + git commit hash + dataset snapshot(`name@version` 또는 manifest hash).
- 텐서 연산은 GPU-first로 작성한다. CPU 폴백은 GPU 커널 부재를 확인하고 명시적으로 선택할 때만 쓴다. 라이브러리 CPU 커널의 `(N×M)` 중간 텐서가 호스트 RAM을 고갈시킬 수 있다.
- 호스트 RAM은 이웃 Codex 세션과 공유한다. 처음 돌리는 스크립트·벤치·전처리는 Linux에서 `systemd-run --user --scope -p MemoryMax=8G -- <cmd>`처럼 상한을 두고, 불가능한 환경에서는 실행 전에 worker 수를 포함한 peak RSS를 추정해 안전한 크기로 낮춘다.
- `libs/`는 vendored third-party이므로 읽기 전용이다.
- data, checkpoint, run, wandb artifact는 git 밖에 둔다.
- 실로봇으로 명령을 보내는 행위는 사용자 확인 없이는 금지한다. simulator는 해당하지 않는다.
- Python을 우선하고 shell은 얇은 launch script에만 사용한다.
- 문헌 second brain: `<wrapper>/tools/oh-dinnno-opsidian` (`dinnno-research-wrapper` 내부). wrapper가 없는 머신에서는 `~/Workspace/sangjun_noh/oh-dinnno-opsidian`을 fallback으로 쓴다. 해당 vault의 `AGENTS.md` 규약을 따르고, 가설이 정체됐을 때만 read-only subagent로 질의한다.

## 보고

결론을 3줄 안에 먼저 말하고 한 번에 한 주제만 다룬다. 사용자에게 요구하는 결정은 1~2개씩 제시한다. 완료 보고 첫 문장은 verdict다. 변경 파일, 실행한 검증, 수치(seed·config·commit 포함), 남은 사용자 결정을 빠짐없이 적고 과정 서사는 생략한다.
