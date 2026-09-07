---
name: research-second-brain
description: 축적된 연구 위키(oh-dinnno-opsidian)를 vault 전체를 읽지 않고 read-only로 조회한다. prior art·유사 연구·데이터셋·베이스라인·failure mode·representation 선택지·"예전에 본 그 논문"이 필요할 때, 그리고 새 연구 단위(init/spec)를 열며 선행연구를 훑을 때 사용. 위키 자체를 편집(캡처·정리·점검)하려는 요청에는 쓰지 않는다 — 그건 vault 디렉토리 안의 /capture·/ingest·/query·/lint·/interview.
---

# Research Second Brain

Sangjun의 git-backed 로보틱스 연구 위키를 **어느 프로젝트 세션에서든** 조회한다.
`index.md`·`thesis-map.md` 전체는 ~155KB라 절대 통째로 읽지 않는다 — 아래 CLI가 heading section 단위로 스캔·랭킹해 예산 안에서 잘라 준다.

## 조회

```bash
~/.claude/skills/research-second-brain/brain.sh "<구체적 질의>" \
  --project-lines <optional-line> \
  --types source,concept,idea,index \
  --limit 8 --max-chars 12000
```

런처가 vault root(`SECOND_BRAIN_ROOT` → CWD 상위 탐색 → 알려진 후보)와 pyyaml 가능한 인터프리터를 알아서 잡는다. 경로를 직접 쓰지 말 것.

project lines: `hoi-transformer`, `neural-grasp-critic`, `pi-touch`, `3d-flow-diffusion-policy`, `force-conditioned-humanoid`.

## 결과 사용 규칙

1. 반환된 `wiki_locator`(file:line) 중 **더 필요한 heading만** 추가로 Read한다.
2. 인용은 `brain:...@<vault_git_commit>`과 `original_url`을 **함께** 단다.
3. `depth: captured`는 얕은 캡처다 — method/loss/평가 세부를 구현 근거로 단정하지 말고 원 논문을 확인한다. `summarized`만 깊은 근거.
4. `provenance_gap: true`는 원 URL 미상 legacy source — 출처 미검증으로 취급.
5. `truncated: true`면 예산에 잘린 것 — 필요하면 질의를 좁혀 재조회.
6. 결과가 비면 method alias·태그·한국어/영문 병기로 **한 번만** 넓혀 재시도. 없으면 "위키에 없다"고 답하고 **지어내지 않는다**.
7. 조회는 read-only다. 프로젝트 작업 중 위키 수정은 사용자가 명시적으로 요청할 때만.

## harness 세션에서

`/harness` §4의 "Second brain 질의"가 이 스킬의 호출 지점이다 — 가설 정체(연속 no-improve · done §4 후보 고갈 · kill 후 pivot 탐색) 시 Explore ×1로 dispatch하고, 회수물은 방법론 힌트 2-3개로 압축해 done §4 후보나 결정 큐 💡에 착지시킨다. 본 세션이 vault를 직접 광범위하게 Read하지 않는다.
