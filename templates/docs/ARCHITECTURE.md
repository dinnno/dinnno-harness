# Architecture — {프로젝트명}

새 파일은 아래 표에 자리가 있어야 만든다. 자리가 없으면 이 문서를 먼저 고친다. 단발 스크립트가 `scripts/`에 쌓이기 시작하면 그것이 모듈이 필요하다는 신호다.

```
project/
├── configs/   experiment configs (yaml). 실험 1개 = 파일 1개
├── src/       모든 코드: datasets, models, train, eval, sim wrappers
├── scripts/   진입점만 (train.py, eval.py, plot, tests). 로직은 src/
├── libs/      third-party (submodule 또는 vendored, 읽기 전용)
├── docs/      spec, plan, done, progress
├── data/      raw + processed (git 밖)
└── ckpt/      checkpoints (git 밖)
```

## 모듈 지도

| 모듈 | 경로 | 책임 | 들어오는 것 → 나가는 것 |
|---|---|---|---|
| {dataset} | `src/datasets/…` | | |
| {model} | `src/models/…` | | |
| {train} | `src/train/…` | | |
| {eval} | `src/eval/…` | | |

## 선택 폴더 (필요할 때만)

`data_generation/`(synthetic data), `retargeting/`(human → robot hand), `teleop/`(VIVE, MANUS), `deploy/`(실로봇, ROS 2), `notebooks/`(탐색용, `src`에서 import 금지), `assets/`(URDF, mesh).

## 파이프라인

(데이터 생성 → 학습 → 평가 → 플롯까지, 실제 명령과 산출물 경로를 한 줄씩)

## 이 프로젝트의 변경 이력

- (새 모듈·폴더가 생길 때 한 줄)
