# harness-diet 2026-06-11 — 변경 기록 & 복원 가이드

harness-legacy-scan 리포트의 **low-risk(dietSafe) 항목만** 적용. baseline commit: `e59f2a4`.
이 폴더의 7개 스냅샷은 편집 직전 원본이다. 영구 삭제 없음 — 모든 제거 콘텐츠는 여기 보존.

## 적용한 변경 (7개 파일)

| 파일 | 변경 | 줄 수 |
|---|---|---|
| `CLAUDE.md` | §1·§2 bullet→압축(구체줄 보존), "Writing guidelines" 섹션 제거(README가 canonical) | 92→72 |
| `templates/CLAUDE.md` | 작성원칙 재기재 구절 삭제(전역참조 포인터 보존) | 39→39 |
| `commands/harness.md` | description 프런트매터 추가, summary dispatch에 `_GUIDE.md` 단일출처 포인터 | 50→54 |
| `commands/add-ref.md` | description 추가, type/name 압축(slug 정규화 보존), "하지않는것"+"scope밖" 병합 | 62→49 |
| `commands/blueprint-ref.md` | description 추가, ambiguous 분기 1줄로(가드 보존), 두 섹션 병합 | 122→122 |
| `README.md` | 다이어트 사이클 간략화, plugins 표→`enabledPlugins` 참조 포인터(drift 방지) | 136→114 |
| `templates/gitignore` | `.hdf5/.safetensors/.onnx/.bag/.mcap/.usd/.usda` 추가, 비디오는 `runs/**`·`outputs/**` 스코프 | 30→42 |

## 적용하지 않음 (human-approval 필요 — 별도 승인 후)

- `CLAUDE.md:9-15` research 목표지향 블록 이동, `:73-86` domain 블록 SPLIT
- `CLAUDE.md:55-71` §4 Goal-Driven TDD 예시 도메인화
- `CLAUDE.md:39-53` §3 Surgical 압축(가드 손실 위험)
- `CLAUDE.md:5-7` 진입점/우선순위 일반화

## 복원

```bash
cd ~/Workspace/sangjun_noh/for_claude/dinnno-harness
# 전체 되돌리기 (커밋 전이라면)
git checkout -- CLAUDE.md templates/CLAUDE.md commands/ README.md templates/gitignore
# 또는 개별 파일을 스냅샷에서
cp .claude/archive/harness-diet-2026-06-11/CLAUDE.md CLAUDE.md
```
