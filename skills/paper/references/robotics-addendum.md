# Robotics Addendum (dinnno 로컬 추가)

`experiments.md`와 `method.md`의 일반 규칙 위에, 로보틱스·조작·HOI 논문에서 리뷰어가 반복해서 찌르는 것만 적는다.

## 수치 보고

1. 성공률은 `seeds × rollouts`(또는 에피소드 수)를 표나 캡션에 반드시 적는다. "SR 0.82"만 쓰지 않는다.
2. 불확실성 표기: seed 간 표준편차 또는 bootstrap CI 중 하나를 고르고 논문 전체에서 통일한다. 단일 seed 결과는 단일 seed라고 쓴다.
3. 차이가 CI 안에 있으면 "outperforms"가 아니라 "comparable"이다.
4. sim 결과와 real 결과는 같은 표의 같은 열에 섞지 않는다. 평가셋과 모집단이 다른 수치도 섞지 않는다.

## 실험 설정 서술

1. sim: 시뮬레이터와 버전, 물리 파라미터 중 결과에 영향을 주는 것, domain randomization 범위.
2. real: 로봇·손·센서 모델, 물체 목록(사진이나 supplementary 표), 시도 횟수, 초기 상태를 어떻게 정했는지, 실패 판정 기준.
3. baseline 공정성: 같은 데이터, 같은 관측, 같은 튜닝 예산. 재구현이면 재구현이라고 쓰고, 발표값을 옮겼으면 그렇게 쓴다.
4. oracle 정보(GT pose, GT contact 등)를 쓰는 설정은 표에 표시한다.

## 주장 범위

1. "generalizes"는 학습 분포 밖의 물체·장면·embodiment에서 잰 수치가 있을 때만 쓴다.
2. "real-world"는 실로봇 실측이 있을 때만 쓴다. sim-to-real 없이 sim만 있으면 그렇게 한정한다.
3. 실패 사례를 limitation이나 supplementary에 구체적으로 넣는다. 리뷰어는 실패 모드를 숨긴 논문을 더 의심한다.

## Supplementary

1. 롤아웃 영상은 성공과 실패를 모두 넣고, 편집하지 않은 연속 실행 하나를 포함한다.
2. 영상과 supplementary에서도 익명성 규정을 지킨다(연구실 로고, 사람 얼굴, 장비 라벨).
