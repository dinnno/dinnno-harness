# Architecture — {프로젝트명}

로보틱스 리서치 repo 최소 레이아웃. 메뉴이지 체크리스트 아님 — 필요 없는 건 제거.

```
project/
├── configs/   experiment configs (yaml)
├── src/       datasets, models, train, eval
├── scripts/   launch, tests, plot, one-shot bash/python
├── libs/      third-party repos (submodule or vendored, read-only)
├── docs/      RESEARCH_SPEC.md, ARCHITECTURE.md, plans/, done/
├── data/      raw + processed (gitignored)
└── ckpt/      checkpoints (gitignored)
```

## 어디에 무엇을

- **configs/** — yaml만. 실험 1개 = 파일 1개. 코드 금지.
- **src/** — 모든 코드. datasets, models, training loops, eval, sim wrappers.
- **scripts/** — 진입점 (`train.py`, `eval.py`), 테스트, 플롯, setup shell.
- **libs/** — 참조 repo. 절대 편집 금지.
- **docs/** — spec, plan, done. (이 폴더의 `CLAUDE.md` 참조)

## 선택사항 (필요할 때만 추가)

- **data_generation/** — synthetic data 생성 스크립트
- **retargeting/** — HOI / human-hand → robot-hand 매핑
- **teleop/** — VIVE, MANUS, glove 드라이버
- **deploy/** — 실로봇 배포, ROS 2 노드
- **notebooks/** — 탐색용 `.ipynb`. `src`에서 import 금지
- **assets/** — URDF, mesh, texture

## 이 프로젝트의 추가/변경

- (실제 사용 중인 디렉토리만 남기고 위 표를 줄여라)
- (프로젝트 고유 폴더는 여기에 한 줄 설명 추가)
