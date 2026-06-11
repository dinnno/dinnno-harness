References 인박스의 특정 entry를 "구현 가능한 수준"으로 깊이 분석. 메인 세션은 codex:rescue로 dispatch만 하고 산출물 경로+한 줄 요지만 적재.

## 사용법

```
/blueprint-ref <name>
```

`<name>`은 `docs/references/_INDEX.md`의 `name` 컬럼 값. 예: `/blueprint-ref 2401.12345`.

## 동작

### 1. entry 조회

`docs/references/_INDEX.md` 읽어 `<name>` 행 찾기:
- 없으면 에러: `not found: {name}. /add-ref로 먼저 등록.` 종료.
- 여러 섹션에 같은 name이 있으면 거부: `ambiguous: {name} appears in {sections}. --section 명시 필요.` 종료. (현재 버전은 `--section` 미지원, 사용자가 직접 충돌 해결)

조회한 정보: url, type (어느 섹션에서 찾았는지), 현재 status, summary_path (있으면 입력으로 활용).

### 2. 사용자 보고 + dispatch

한 줄 보고: `blueprinting: {name} ({type}) via codex:rescue`. STOP 신호 없으면 dispatch.

**codex:rescue 입력**:
- URL, type, name
- `docs/RESEARCH_SPEC.md` 본문 (thesis 매핑용)
- 기존 `summary_path` 파일이 있으면 그것도 (요약 위에 청사진 쌓기)

**codex:rescue 출력 사양 (type별)**:

#### paper
```markdown
# blueprint: {name}

## 1줄 요지
{한 문장 — 이 paper의 핵심 주장과 우리에게 왜 중요한가}

## 메서드 의사코드
{핵심 알고리즘을 우리 코드 스타일로 의사코드. 입력·출력·loop 구조 명시}

## 핵심 수식·하이퍼파라미터
{loss, regularization, key constants. 표 형태 권장}

## 실험 셋업
{데이터셋, 평가 지표, baseline. 우리가 재현 가능한 수준으로}

## thesis 비교 축 매핑
{RESEARCH_SPEC §4의 비교 축 중 어느 것을 움직이는지. 한 줄씩}

## 우리 코드 통합 포인트
{어느 파일·모듈에 어떻게 들어갈지. configs/*.yaml 분리 여부, src/ 어느 폴더, libs/ vendored 필요한지}
```

#### code
```markdown
# blueprint: {name}

## 1줄 요지
{한 문장 — 이 repo가 무엇을 하고 우리에게 왜 중요한가}

## 아키텍처 (텍스트 다이어그램)
{디렉토리 트리 + 핵심 모듈 데이터 흐름}

## 핵심 클래스·함수
{이름 / 경로 / 한 줄 역할. 표 형태}

## 의존성
{외부 라이브러리, 버전 제약, GPU/CUDA 요구사항}

## fork 전략
- fork할 부분: {모듈명 — 이유}
- 폐기할 부분: {모듈명 — 이유}
- 우리 코드로 가져올 때 어디에 둘지: {src/... 경로}

## thesis 비교 축 매핑
{한 줄씩}
```

#### homepage / 기타
```markdown
# blueprint: {name}

## 1줄 요지
{이 자료가 무엇이고 왜 봤는가}

## 의미 있는 부분
{데이터셋 다운로드 링크, 평가 프로토콜, license 등 — 의미 있는 것만}

## 판정
- [ ] 구현 대상 (이유: ...)
- [ ] 폐기 (이유: ...)
```

### 3. 산출물 저장

codex:rescue가 반환한 내용을 `docs/references/blueprints/{name}.md`에 저장. `blueprints/` 폴더 없으면 생성.

### 4. `_INDEX.md` 갱신

해당 행의:
- `status`: `blueprinted`
- `blueprint_path`: `references/blueprints/{name}.md`

`summary_path`는 건드리지 않음 (누적).

### 5. 메인 세션 적재

한 줄 보고: `blueprinted: {name} → {blueprint_path}. 요지: {1줄}`.

메인 세션은 이 한 줄과 파일 경로만 적재. 청사진 전문은 컨텍스트 밖.

## 하지 않는 것

- `_INDEX.md`에 없는 URL을 즉석 분석 ❌ (먼저 `/add-ref` 등록 필요)
- 메인 세션이 직접 URL fetch/PDF 읽기 ❌ (codex:rescue 전용 — 토큰·저작권 회피)
- 자동 재시도 ❌ (codex:rescue 실패 시 사용자 보고)

## scope 밖

- summary 생성 (그건 `/harness`의 자동 dispatch 흐름)
- `_GUIDE.md` 수정
