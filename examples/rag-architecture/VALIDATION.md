# Independent first-result validation

Baseline ff689f9a63b0aa350036b12a01695c8c52c7bda8. D0 design commit c0410a6, created before implementation. No common documentation modified; hence no common-document D1. First implementation commit is recorded in FIRST_RESULT.md after preservation.

## Rule trace and sufficiency

| Decision | Class | Evidence | Result |
|---|---|---|---|
| One beginner concept, full name and meaning before diagram | A | DESIGN_SYSTEM concept/first-use sections; TASK | Both modes share same introduction |
| Local Pretendard, -1pt, semantic Navy/Blue/Teal | A | DESIGN_SYSTEM typography/colors; styles.css | Real CDP custom font checks and tracking pass |
| White panel, own Blue label and Navy heading | A | Recipes §2/4; DESIGN_SYSTEM title ownership | `.diagram-panel` owns `.panel-label` and `h2`; small internal boxes are graph nodes |
| Preparation separated from use; state visibly transferred | A/C | Comparison preparation/application pattern; RAG-specific graph | Two rows, storage→search and question→model-input branches |
| Nine graph nodes and two long branch links | C | TASK relationships; Figure §3/6/7 | Short adjacent horizontal arrows; branch routes use empty inter-row/bottom space |
| 40px top padding, compact panel padding, 18px secondary labels | C | DESIGN_SYSTEM permitted measured exceptions | Essential definition and full diagram fit; no content hidden |
| Shared lesson.js and mode-specific outer scale | A/C | supplied MODES/DESIGN; no iframe mandate | Same source, hash, and lesson content; only container scaling differs |
| Missing common mode contracts | Packaging issue | Coordinator correction before implementation | Supplied/read before D0 commit; not a design-rule gap |
| Missing default bundled browser | Tooling issue | First launch error | Use installed /usr/bin/chromium; real render succeeded |

D0 rules were sufficient to choose hierarchy, terminology treatment, palette, fonts, general frame, phase separation, and verification. Topic-specific graph geometry and concise wording required design judgment, as expected. No demonstrated common-rule contradiction. Missing history links and scripts are unavailable inputs, not invented evidence of absent rules. Some early height estimates in DESIGN were deliberately provisional and are superseded by the measured final layout addendum; no visual defect was hidden with clipping.

## Technical review (separate from design provenance)

Checked each claim against the task and causal graph independently of browser tests:

- Retrieval-Augmented Generation expands RAG correctly and uses retrieved external passages as context for generating an answer.
- Common dense retrieval preparation divides documents, computes semantic numeric representations, and retains a link to original passage text. The slide shows original passages retained in the store; numeric search representations alone are not presented as prose given to the generator.
- Question is used for search; returned passages and the original question both enter generation. The explicit lower branch prevents the implication that only retrieved documents reach the model.
- Retrieval accesses stored documents at answer time. The depicted pipeline does not update learned generator parameters. This does not claim that RAG systems can never also undergo training.
- Retrieval can miss relevant evidence; generation can misinterpret it. Accuracy is not guaranteed. No fabricated retrieval score, benchmark, actual response, or calculated output is shown.
- Scope assumption: a common semantic retrieval pipeline; keyword/hybrid retrieval and ranking details are omitted for beginner scope. No external fact lookup performed; this is domain review, not independent expert approval.

## Real runtime evidence

Command: `python examples/rag-architecture/verify.py` from this root. `verification.json` records final hashes and 8 cases: 1600×950,1440×810,1366×768,1280×720 × Scroll/Slide. All pass. Real installed Chromium via Playwright, local static HTTP server and original local WOFF2.

Checks: font ready/load and CDP CSS.getPlatformFontsForNode at heading/introduction/SVG phase/node/body/footer/navigation; sampled platform fonts are custom Pretendard. All visible lesson text elements have -1pt. HTML text Range bounds, SVG text bbox against nodes, panel padding, slide bounds, horizontal overflow, footer gap (~12 design px), runtime/console/request/HTTP errors. Mode-switch keyboard Enter and pointer roundtrip, hash restoration and reload. Slide stays inside all four viewports. Scroll full-page screenshots intentionally extend beyond shorter viewports and can be scrolled normally.

Eight PNGs were individually opened and visually inspected. Definition is visible, phases separated, arrows enter actual target boundaries, branch labels clear, body notes remain above final caption/footer. The small Slide uses uniform scaling; its secondary text is naturally smaller than Scroll. No visual clipping/overlap observed. No live search or calculation is claimed. Arrow path data is recorded; direction/topology additionally inspected manually, not claimed as an exhaustive collision-proof graph algorithm.

All50 manifest input hashes match. Source hashes are in verification.json. Shared dependencies remain ../../templates/html/styles.css and reference-layout.css, which load local fonts below the same shared directory.

## Limits

This validates selected flow/phase/structure relationships, not all eight patterns. No tensor/matrix/math/metrics, interactive parameter boundaries, mobile layout, actual RAG backend, real user comprehension, screen-reader listening, or user design approval tested. No external feedback received before preservation. No push, PR, merge, or deployment.

## Post-review revision — 2026-10-30

First-result evaluation above and commits c0410a6 / 93ec54e / 1b23b93 remain preserved. Independent REVIEW_FEEDBACK.md reported PASS with scope limits and no blocking defect. Its optional topic clarification was authorized after first-result preservation. Added visible `의미 기반 검색의 예` to the panel label and a short note that word-based or combined retrieval is also possible. Class C topic-specific wording; no new common rule, documentation gap, or retrospective D0 failure.

Reran `python examples/rag-architecture/verify.py` for all8 actual Chromium PC4×2 cases after the wording change. Updated verification.json and all8 screenshots now represent this post-review revision; the first versions remain in commit93ec54e5a4e9e71e53233aa9296e37cc68de3581. Same font/CDP, tracking, DOM/SVG/text bounds, padding, footer, runtime and mode-switch checks pass. All50 immutable input hashes remain unchanged. Opened the revised slides-1280x720.png: both scope phrases fit on one row, without collision or clipping; no redesign needed. Review limitations above still apply.

Separate post-review verifier portability issue (E), reported by Coordinator: the integrated repository archives its manifest at docs/fresh-builder-trial/input-manifest.json and retains original common Markdown. verify.py now explicitly prefers root INPUT_MANIFEST.json with provided_sha256 for isolated supplied inputs; if absent, it uses the archived path with source_sha256. Report records selected path/hash field; missing or mismatching inputs fail. No integrated repository was read. Local eight-case run still passes with provided_sha256. Integrated fallback execution remains for Coordinator/Reviewer to verify; the first local Chromium PASS is unchanged.

## Stage 4 hardening · separate from first-result evaluation

[Stage 4 report](../../docs/rag-hardening/REPORT.md) separates original documentation sufficiency, authored improvements and current pass/reject outcomes. Original first and post-review evaluations above are unchanged. Source/evidence for the current CSS alternative are [variant results](../../docs/rag-hardening/evidence/validation.json) and the independent current review under `docs/rag-hardening/review/`.

The `verification.json` beside this file and `docs/fresh-builder-trial/` snapshots are historical PR #27 evidence bound to f368f77, not current-CSS hashes. Their historical integrity check was run in that pinned worktree. Do not regenerate their images/JSON to relabel old evidence. Current baseline and variants use `python docs/rag-hardening/verify_variants.py`; the new independent audit checks the current baseline too.

No common rule change or demonstrated documentation navigation failure. A covers existing rules, C the local adaptations/rejection limits, E the test oracle and zoom-normalized line measurement corrections. B/D deficits were not demonstrated. All exact variant content/geometry is in this example's DESIGN.md.
