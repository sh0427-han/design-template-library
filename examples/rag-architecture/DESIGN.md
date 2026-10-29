# RAG concept — pre-implementation design

Audience: adult beginners who know documents and web search. One independent learning unit, in Korean, shared by Scroll and Slide. Goal: explain that externally retrieved passages accompany a question into a generator, distinguishing preparation from answering.

## Provenance and selection

Baseline ff689f9a63b0aa350036b12a01695c8c52c7bda8; input hashes in INPUT_MANIFEST.json. Rules: DESIGN_SYSTEM sections concept first, first-use terminology, semantic colors, typography, frame, arrows; docs/DESIGN_COMPONENT_RECIPES §2/4/6; FIGURE_PRODUCTION_STANDARD §3/6/7/10/13; REFERENCE_REVIEW_GUIDE PC4; TEMPLATE_REUSE_VALIDATION A–E. Process #2 supplies explicit role flow and consistent tracks; Comparison #3 supplies preparation/application separation and connecting stored state; Architecture #6 supplies one panel with editable structural diagram. All eight previews inspected. No copied CNN data or calculations.

Concept, Step-by-Step, Interactive, Experiment, Executive Summary not selected: no pixel inspection, numeric calculation, parameter control, evaluation dataset, or KPI reporting needed. This does not validate those patterns.

## Content and terms

Title: 검색 증강 생성의 흐름. Introduction: 검색 증강 생성(Retrieval-Augmented Generation, RAG); relevant external documents used to generate an answer. Avoid unnecessary vector/embedding/LLM jargon. Explain search representation as numbers representing meaning. Generator = model that writes an answer. Model retraining = changing learned parameters (학습된 내부 값을 바꿈). Retrieval = reading external documents at question time. State that relevant retrieval and faithful generation can fail; accuracy is not automatic.

Figure: documents → chunks → meaning representation → saved passages + representations; saved collection feeds search. Question → search → original question + retrieved passages → generator → answer. A separate question branch reaches assembled input; document store is not an arrow into model training. Schematic, no live retrieval or claimed results.

## Layout contract

1440×810 canvas, padding 40px 66px 30px (top exception to preserve two-row diagram and full definition). Header category 17/800, title 49/1.13/700, definition 21/1.38. One White panel radius17/border1/padding24; label 16/800 Blue, title 25/1.2 Navy. Declared explanation unit `.diagram-panel` owns `.panel-label` and `h2`; internal diagram nodes are small functional nodes with Navy titles and role annotations, not independent full cards. Figure width1258 height390, SVG labels 19–23; all Pretendard and inherited -1pt. Two phase labels Blue, processing arrows Blue, preparation-to-use link Teal. Small storage/input surfaces use pale colors with semantic purpose. No card shadows.

Height budget: top40 + header147 + content-gap16 + panel430 + caveats58 + takeaway48 + footer41 + bottom30 =910 is too large; therefore panel includes its own phase titles, use header132 + gap16 + panel390 + caveats54 + takeaway48 + footer40 + top40 + bottom30 =850. Final planned diagram panel 350 and header128 yields806. Figure itself is 300 high; phase labels and nodes are in one editable SVG. Actual bounds determine self-correction before final preservation; do not hide overflow.

Shared canvas styling from ../../templates/html/styles.css and reference-layout.css. A common lesson fragment is loaded by both entrypoints. Slide fits remaining height below44px mode bar; Scroll fits width and allows natural vertical scrolling. Single page hash #rag persists; no meaningless next/previous enabled controls. Focus outline Amber. No animated or simulated retrieval.

## Verification

Real Playwright Chromium, PC1600×950/1440×810/1366×768/1280×720 × both modes. Await local WOFF2; inspect CDP platform fonts, all text tracking, DOM text ranges and SVG bounds, panel padding, footer clearance, connector endpoints, console/network failures, mode roundtrip/reload, keyboard focus. Open all screenshots. Verify immutable inputs via hashes and record source digests. Technical claims reviewed independently against TASK requirements; no quantitative claims to calculate. External research only if technical uncertainty requires it; provenance separate.

## Final implementation addendum (before first-result preservation)

Measured implementation uses SVG viewBox1258×292 inside a panel with padding16px24px12px, title25/1.2, label16/1.25, title gaps8/12. This supersedes provisional height estimates above. Canvas remains1440×810, top40/side66/bottom30, title49, subtitle21 over two explicit introduction lines. SVG graph nodes: preparation y0,h74 and response y148,h80; external stage gap44px; connectors stop3.5px before node bounds. Storage-to-search uses y108; original-question branch uses y270. Nine functional nodes total; node titles21, secondary18, phase19, branch17. The branch paths are longer because they represent nonadjacent dependencies, not decorative process arrows. Flow text is semantic HTML/SVG, not an image.

Notes are two equal columns with24px gap; body18/1.4, label19, gap4. Content gap12; final caption20/1.45 with11px17px padding; footer gap12 and padding-top11. All colors are shared tokens. `.rag-slide` uses overflow:visible; measured bounds rather than clipping enforce fit. Slide scale min(1,(width−40)/1440,(height−88)/810), Scroll min(1,(width−48)/1440). Native anchor provides accessible mode switching; one-page navigation has no inert arrows. JavaScript-disabled fallback is visible. No motion exists.
