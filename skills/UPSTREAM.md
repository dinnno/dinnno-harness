# Vendored skill provenance

External skills are pinned snapshots. They never auto-update; review the upstream diff and update by hand.

| Local skill | Source | Pinned revision | License | Local modifications |
|---|---|---|---|---|
| `bro` | [`luchasarie/bro-skill`](https://github.com/luchasarie/bro-skill/blob/01e51f8092973be58eff3b7271282bd8488a02ae/SKILL.md) | `01e51f8092973be58eff3b7271282bd8488a02ae` (2026-07-25) | MIT | None; examples and installer omitted. |
| `paper` (references only) | [`Master-cai/Research-Paper-Writing-Skills`](https://github.com/Master-cai/Research-Paper-Writing-Skills/tree/77e7c2c1ba06f7d71844873147665437a03aac1b/research-paper-writing/references) | `77e7c2c1ba06f7d71844873147665437a03aac1b` (2026-06-23) | MIT | `references/` 원문 그대로. SKILL.md는 dinnno가 새로 썼고 `robotics-addendum.md`, `venues/`, `prompts/`는 로컬 추가. 검증 장치(주장-근거 대조, 인용 실재 확인, 다중 심사위원 모의 심사, rebuttal 대응표)는 [`Imbad0202/academic-research-skills`](https://github.com/Imbad0202/academic-research-skills)(CC BY-NC 4.0)의 아이디어를 파일 복사 없이 다시 구현했다. |

License text: `skills/licenses/bro-skill-MIT.txt`, `skills/licenses/research-paper-writing-MIT.txt`. 2026-09-24에 쓰지 않던 vendored 스킬(diagnosing-bugs, codebase-design, improve, improve-codebase-architecture, thermo-nuclear-code-quality-review, ponytail)을 제거했다. 필요하면 git 이력에서 되살린다.
