# Stage 4 independent review — 2026-10-31

**PASS within the tested authored variants and rejection bounds. No blocking defect in the supported final fixtures. Common design Markdown changes required: zero.** This does not revise stage 3's first PASS or its partial Architecture #6 reuse finding.

## Evidence and independence

Reviewer read PLAN, stage 3 first/final reviews, repository instructions, relevant DESIGN_SYSTEM / component recipes / catalog / Architecture source and preview, current RAG source/design, and Coordinator's final verifier/evidence. Some broad common-document output was truncated; relevant typography, height allocation, text bounds, PC and flow sections were read separately. No claim of an exhaustive library audit is made.

Reviewer changed only this `review/` directory. `audit.py` reuses the prior independent reviewer audit without overwriting its location; it was run against current source. `variants.py` is a separate geometry audit with explicit matching fixtures and independent assertions; it does not import or execute the Coordinator verifier. Shared-host process separation is the independence boundary, not security isolation. Coordinator supplied final fixture coordinates after initial test failures; Reviewer independently evaluated them.

Commands, both exit 0:

- `python docs/rag-hardening/review/audit.py`: baseline **8/8 PASS**, PC 1600×950, 1440×810, 1366×768, 1280×720 × Scroll/Slide.
- `python docs/rag-hardening/review/variants.py`: five variant conditions × PC4×2 = **40/40 expected outcomes**. This includes correct rejection, not 40 fitting layouts.

Coordinator's `../evidence/validation.json` separately reports 48 expected outcomes. All four runtime source hashes match between that report, independent `audit.json`, and independent `variants.json`. Baseline audit checks actual CDP Pretendard, global −1pt, node containment, overflow, visible scope clarification, keyboard/pointer switching, reload/hash restoration, footer reachability and browser errors. Variant audit adds independent title/definition separation, zoom-normalized title line counts, chunk text bounds and title/description separation, note/caption/footer order, canvas containment, unchanged 49/21/18px fonts and unchanged viewport zoom. Variant font identity is additionally covered by Coordinator's sampled CDP checks; the independent variant audit itself checks computed sizes and tracking, not CDP identity.

All eight independent baseline PNGs and all ten independent smallest-PC variant PNGs were directly opened. Five corresponding Coordinator Slide PNGs were also opened. No screenshot was substituted for editable implementation.

## Baseline sufficiency, adaptations and current support

| Case | Original condition | Current finding |
| --- | --- | --- |
| Existing RAG lesson | Previously passed | Independent current baseline 8/8 PASS; no visual or navigation regression |
| `외부 문서를 찾아 활용하는 검색 증강 생성의 질문 응답 흐름` | Already fits in one title line | `long-original` 8/8 fit. Existing layout is sufficient for this string. No defect was repaired here |
| Same long title with author class | Optional alternative | `long-reflow` 8/8 fit; title uses two lines and definition occupies the adjacent track. Same fonts/zoom; clear separation. It is not evidence that the original needed repair |
| Chunk description `문서를 의미가 이어지는` / `짧은 조각으로 나누기` | Second line protrudes below the original 74px node | Original rejected 8/8; authored 90px preparation row accepted 8/8. Text is preserved, not shortened or shrunk |
| Notes extended by the 30-repeat overload fixture | Exceeds canvas/footer budget | Correctly rejected 8/8. Visible overflow is evidence of unsupported content, not an accepted page |

The supported node fixture increases all four preparation rectangles to 90px, preserves their common top and bottom edges, and moves the three single-line text pairs down 8px. Chunk title baseline stays 30; its two description baselines are 54/76. The first row's arrows move to y45, the new node center. The storage-to-search path starts 3.5px below the enlarged storage box, travels at y124, and still terminates 3.5px above search at y148; its label moves to 117. Direct inspection shows preserved direction and no label/edge collision. The chunk's title sits higher than neighboring single-description titles to accommodate its extra line; the common node boundaries and centered connectors remain aligned. No figure/font scaling was used to gain room.

At 1280×720 Slide the independently measured reflow description bounds end around SVG y79.85, inside the 90px box; original description ends around 79.85 outside the 74px box. Title/description blocks remain separate. The common viewport scale remains about 0.78025, so 18px supporting text is about 14px onscreen. Projection-distance or low-vision readability is not established.

## A–E classification and documentation judgment

| Class | Finding |
| --- | --- |
| A — already documented common rule | DESIGN_SYSTEM first-use terminology, typography/−1pt, line-height versus spacing, height allocation, zoom-normalized actual bounds, and avoiding shrinking excess content; component recipes §3 PC/text handling and §4 flow. These rules were sufficient to guide the tested decisions |
| B — needed common rule found only in source | None demonstrated. The exact RAG node dimensions, title track ratio and dependency route are example geometry, not missing common rules |
| C — example-specific content/layout decision | Optional two-column title, 90px preparation row, revised SVG text/connector coordinates and exact supported/rejected strings. Keep these in the example design and fixture record |
| D — actual common omission/contradiction | None demonstrated. Do not add common rules merely because a fixture exposed a local height problem. Common MD edits required: 0 |
| E — implementation/verification error | Initial stage4 verifier incorrectly expected the selected long title to fail and computed title line count from a scaled rect without dividing by zoom. Both were corrected. Initial 74px description adaptation remained outside the box and was replaced by the 90px fixture. These are subsequent local test/implementation findings, not retrospective stage3 failures |

No documentation-navigation failure was reproduced. Existing common guidance was located directly. The initial false expectation is now honestly recorded as baseline sufficiency; no longer title was introduced just to force a failure.

## Scope and preservation

The CSS author class is available in the RAG example but is not automatically selected. Node expansion and overload rejection are authored browser fixtures and verification policy, not production content parsing, runtime rejection UI, or an automatic layout engine. Reloading the production page restores its original lesson. Overflow requires editing, another explicit layout, or separately authorized content division; this work does not silently generate pages.

The overload fixture proves one concrete rejection point; it does not establish a universal character limit or exhaustive maximum. The two variants were tested separately; combined changes, arbitrary long words, more nodes, negative values/axes, mobile, all eight patterns and novice comprehension were not validated. #6 remains partial structural reuse, not its full representation-specific track/grouping pattern.

`git diff --name-only f368f77b11834c446cde9a69d3b355fdf7fdf48f -- docs/fresh-builder-trial templates DESIGN_SYSTEM.md docs/DESIGN_COMPONENT_RECIPES.md` was empty at review. Stage3 first/final snapshots and common/reference source are preserved. Historical `check_evidence.py` concerns frozen source provenance and must not be presented as current runtime validation; the current runtime evidence is the fresh audits above. This review does not claim a fresh run of the entire unrelated reference suite; Coordinator owns that broader regression evidence.
