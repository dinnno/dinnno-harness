---
name: vis
description: >
  마음에 든 시각화(그림·플롯·HTML 뷰어·롤아웃 영상·궤적 애니메이션)를
  ~/Workspace/vis/<프로젝트>/<날짜>/ 아래에 PNG·MP4·원본과 재현 정보까지 함께
  보관한다. 사용자가 "이거 저장해줘", "이건 남기자", "맘에 든다", "킵", "좋다
  이거", "vis에 넣어", "나중에 쓰게 저장", "논문에 쓸 것 같아" 같은 반응을
  보이면 반드시 이 스킬을 쓴다. 시각화를 보여준 직후에도, 비교 축을 판가름하는
  결과 그림이면 저장할지 한 줄로 제안한다. 시각화를 새로 만드는 스킬이 아니라
  이미 만들어진 것을 나중에 논문·슬라이드에 쓸 수 있게 보관하는 스킬이다.
argument-hint: "[슬러그]"
---

# vis — 마음에 든 시각화를 나중에 쓸 수 있게 보관한다

시각화는 세션 안에서 한 번 보고 사라진다. 몇 달 뒤 논문이나 발표 자료를 만들 때
"그때 그 그림"을 다시 만들려면 어떤 스크립트가 어떤 config·seed로 뽑았는지를 찾아야
하는데, 대개 못 찾는다. 이 스킬은 그림과 **그림을 다시 만들 수 있는 정보**를 같이 남긴다.

시각화를 만드는 스킬이 아니다. 이미 있는 것을 보관한다.

## 저장 위치

```
/home/jun/Workspace/vis/<프로젝트>/<YYYY-MM-DD>/
    NOTES.md
    ee-traj-vs-baseline.png
    ee-traj-vs-baseline.html
    rollout-fail-cases.mp4
```

프로젝트 이름은 `~/Workspace/` 바로 아래 디렉토리 이름으로 자동 판별된다.

## 저장하기

```bash
VIS=~/Workspace/dinnno-research-wrapper/tools/dinnno-harness/skills/vis/vis-save.sh

bash "$VIS" --slug ee-traj-vs-baseline \
  --caption "베이스라인 대비 말단 궤적 — IK 수렴 실패가 t=1.2s 구간에 몰린다" \
  --source "scripts/plot_traj.py · configs/exp07.yaml · seed 0 · a3f91c2" \
  outputs/exp07/traj.html
```

`bash "$VIS" --help`로 나머지 옵션을 본다.

## 잘 정해야 하는 것은 세 가지뿐

**slug** — 파일 이름이 된다. 무엇을 보여주는 그림인지 이름만으로 알게 짓는다.
`plot1`, `result-final` 말고 `ee-traj-vs-baseline`, `success-rate-by-seed`.

**caption** — 제목이 아니라 **이 그림에서 읽어낸 사실**을 쓴다. 이게 이 스킬의 값어치다.

- 나쁨: "궤적 플롯"
- 좋음: "베이스라인 대비 말단 궤적 — IK 수렴 실패가 t=1.2s 구간에 몰린다"

몇 달 뒤 NOTES.md를 훑으며 슬라이드에 쓸지 말지를 이 한 줄로 판단하게 된다.
그림이 비교 축과 연결되면 그 연결도 적는다.

**source** — 재현 정보. 추측해서 채우지 않는다. 방금 이 세션에서 만든 그림이면 이미 알고
있고, 모르면 아는 것만 적는다. commit은 실제로 확인한다:

```bash
git rev-parse --short HEAD
```

## 형식별로 무엇이 저장되나

| 원본 | 남는 것 |
|---|---|
| png · jpg · svg · pdf | 그대로 복사 |
| html (정적 플롯) | html 원본 + PNG 스냅샷 |
| html (애니메이션) | 위 + `--record 8`로 8초 화면 녹화 mp4 |
| mp4 · webm · mov · gif | mp4 + 첫 프레임 png |
| PNG 프레임이 든 디렉토리 | mp4 |

HTML 원본을 함께 남기는 이유는 나중에 각도·범위·색을 바꿔 다시 뽑을 수 있기 때문이다.

plotly·three.js·meshcat처럼 렌더가 느린 뷰어는 스냅샷이 빈 화면으로 찍힐 수 있다.
그때는 `--wait 8000`으로 대기를 늘린다.

`--record`는 **실제 화면에 브라우저 창을 잠깐 띄워** 녹화한다. 사용자가 다른 작업 중일 수
있으니 쓰기 전에 한 줄로 알린다. 이미 mp4나 프레임 시퀀스가 있으면 그쪽이 항상 낫다.

## 여러 장

슬러그가 다르면 호출을 나눈다. 한 호출에 여러 소스를 주는 것은 **같은 그림의 다른 형식**
일 때만이다 (예: 같은 결과의 html과 mp4).

## 저장한 뒤

저장 경로와 파일 이름만 짧게 알린다. NOTES.md 내용을 다시 읊지 않는다.
