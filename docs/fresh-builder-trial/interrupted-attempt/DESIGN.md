# RAG concept design — before implementation

Goal: a Korean adult beginner can explain that relevant external document excerpts are retrieved for a question and supplied with the question to a generator, distinguishing preparation from response. One concept unit, no numeric worked example, appendix or model execution.

## Rule provenance and pattern selection

A: DESIGN_SYSTEM.md sections 개념 설명의 기본 순서 / 용어와 약어의 첫 등장 / 단일 토큰 / 16:9 / 행간 / 카드 / Figure / PC: concept first, visible definition, tokens, local font, -1pt, explicit line heights, matching tracks, PC4.
A: docs/DESIGN_COMPONENT_RECIPES.md §4 flows and structures; docs/FIGURE_PRODUCTION_STANDARD.md §§3,6,7: stages, actual node boundaries, Blue exterior and Teal interior transitions, single paths, 3.5px endpoint gaps.
A: docs/REFERENCE_REVIEW_GUIDE.md: Chromium PC4×2, CDP actual fonts and geometry, direct visual inspection.
A: docs/REFERENCE_REUSE_WORKFLOW.md and TEMPLATE_REUSE_VALIDATION.md: design first, A–E classification, D0 evidence, shared mode content.
Selected #6 Architecture: one White architecture field, grouped phases, object boundary connectors. Selected #2 Process: ordered role flow and aligned text. Selected #3 Comparison only its preparation→application connection motif, not its two-method comparison. #1 single-panel and last caption are supporting common components. #4 numeric calculation, #5 live controls, #7 evaluation, #8 KPI are not appropriate and remain untested. All eight purposes/specifications/previews reviewed; editable sources inspected, unselected sources at HTML structure level.

## Topic-specific decisions (C)

Use two horizontal phases in one White panel. Upper lane: external documents → divide and make searchable representations → stored excerpts + search representations. Lower lane: question → retrieval → question + relevant excerpts → generation model → answer. Storage links to retrieval across the phase gap. The original question has a separate bypass into the question+excerpts node. This expresses the two input relationships explicitly. Arrows denote data flow; retrieval uses the prepared index. A searchable numerical representation is explained in everyday Korean without requiring vector/embedding terminology. The retrieval node notes using the question's search representation. No claim all RAG must be vector retrieval; this is a basic indexing architecture.

A short visible difference line: retraining changes model parameters (internal learned values); RAG retrieval supplies external text at answer time. A short limitation line: irrelevant/incorrect documents or generation errors can still lead to incorrect answers. Final Teal-rule caption focuses on question + relevant documents as generation input.

Independent unit first definition under title: 검색 증강 생성(Retrieval-Augmented Generation, RAG), with plain-language meaning before any diagram RAG abbreviation. Model: 입력 내용을 바탕으로 답변을 만드는 생성 모델. Documents and web search are assumed known per TASK.md. No mathematical variables or formulas, so STIX not needed.

## Layout and type budget

1440×810 canonical canvas. Common styles.css and reference-layout.css, then scoped rag CSS. Proposed padding 40px top, 66px sides, 30px bottom (top adjustment like #3, to fit definition without shrinking text). Header approximately 147px; content gap16; White diagram approximately400px; distinction/limitation row60px; final caption52px; footer42px. Total ≤810. Exact final measured tracks and any self-correction recorded in VALIDATION.

Title49px/1.13/800, kicker17px/1.25/800, introductory definition21px/1.38, panel phase titles24px/1.2/750, phase labels16px/1.25/800, diagram node titles21px/1.2/750, explanations18px/1.4, notes18px/1.4, caption19px/1.45, footer15px/1.4. All Pretendard Variable and -1pt. Navy headings, Blue role labels/exterior edges, Teal interior transformations and caption rule; White panel, Border edges, canvas token background. No decorative imagery or shadow on nodes. Main panel radius17, border1, padding24; small object nodes radius10, border1. Related gap8, sections16, major24.

Declared explanatory units: two `.phase-heading` containers, each with one direct `.phase-label` and one h2; each of seven process `.stage` elements has one `.stage-label` and one h3. Storage and question/context/document symbols are data objects, not independent explanatory cards; they use object names without compulsory extra labels. Exact stage number may follow final grouping; adjust declaration before verification if object roles differ. No arbitrary label duplication to pass tests.

Geometry: node rectangles are actual bounds; line endpoints computed after fonts.ready in SVG coordinate space. Horizontal arrows join side centers with3.5px clearance; storage transfer is orthogonal through empty lane gap; question bypass stays below response nodes. Text must remain inside padded nodes and panel. Diagram explanation/shape counts are symbolic, not data amounts.

Modes: same content.html in an iframe. Slide uniformly fits both window dimensions; Scroll fits width, has document navigation at top, natural vertical scroll and current section link. Only one unit so no inferred pagination. Missing dual-mode source/contracts are blocked; use accessible native links and shared source based on supplied common rules. Navigation focus Amber3px/offset4px. No animation; reduced motion is naturally satisfied. Static content should remain with JS disabled; arrow paths have static defaults and JS refines endpoints. No remote dependencies.

## Verification

Use installed Python Playwright + /usr/bin/chromium, PC1600×950,1440×810,1366×768,1280×720, both modes. Await font loading, collect CDP CSS.getPlatformFontsForNode for all visible text including SVG/navigation, verify -1pt, record request/console failures and exact SHA256. Independently test data-flow edges and both required generation inputs; inspect node/text/panel/footer containment, connector clearance and overlaps. Check navigation round trip/reload/Scroll end; resize and disabled JS. Open all eight actual screenshots. No claims of live RAG, model accuracy, novice comprehension, user approval, original eight regression, mobile or assistive-technology user testing.
