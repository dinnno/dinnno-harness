# docs/

이 폴더에 들어가는 문서들:

- `RESEARCH_SPEC.md` — 프로젝트의 불변 spec (북극성). thesis · naive baseline · failure taxonomy · comparison axes · derivation · ablation plan · accepted failures
- `ARCHITECTURE.md` — repo 디렉토리 레이아웃 (configs/src/scripts/libs/data/ckpt)
- `plans/` — 실험별 `plan_v{N}_{short-name}.md`
- `done/` — 완료 보고 `done_v{N}.md`

## 작성 규약

- RESEARCH_SPEC.md는 실험 결과로 인해 어긋나기 전에는 건드리지 않는다. 어긋나면 spec부터 고치고 plan을 다시 슬라이싱한다 (코드로 패치 금지).
- ARCHITECTURE.md는 새 디렉토리/규칙이 생길 때만 갱신.
- 각 plan/done은 자기완결적이어야 한다. "이전에 논의한 바와 같이" 같은 외부 참조 금지.
