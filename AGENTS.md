# Agent / Codex instructions

## Repository scope

- Canonical repository: https://github.com/sh0427-han/design-template-library
- Repository owner: `sh0427-han` (ChatGPT GitHub connection: `배포용`)
- Do not confuse it with `sh0427-han-private` (separate private project account).
- This is an **HTML-only design reference library** for AI/ML teaching, technical presentations, papers, and engineering reports, not an application deployment repository.
- **Only HTML Scroll Mode and Slide Mode are supported outputs. Do not generate PPTX, create PPTX conversions, or synchronize to PPTX.**
- The eight standalone HTML types are reusable visual patterns, not alternative output formats; compose them into Scroll or Slide pages as needed.
- PPTX assets, generation scripts, and preview files have been removed by user request. Do not recreate them.

## Before any edit

1. Read `DESIGN_SYSTEM.md` and `TEMPLATE_CATALOG.md`.
2. Inspect the relevant source under `templates/` and preview under `previews/`.
3. Scope the change to requested artifacts. Preserve unrelated templates.

## Core rules

- One main concept per slide; use diagrams and data flows where helpful.
- Ensure technical accuracy, especially equations, tensor layouts, CNN flows and metrics.
- Use the shared HTML/CSS/JavaScript design system for Scroll and Slide; keep content and calculations consistent across modes.
- Apply **condensed character spacing of 1.0 pt (`-1pt`) to ALL HTML text** (title, body, label, caption, footer, gallery). Use shared tokens; never override individual labels/headings without explicit instruction.
- Use Pretendard Variable as the default HTML typeface via `templates/html/styles.css`.
- Preserve editable HTML/CSS/JavaScript source and functional browser interactions; do not substitute a static screenshot for working content.
- Do not insert third-party figures without a source URL near the figure.
- User/project-specific requirements take priority over the library defaults.
- Do not edit external repositories without explicit instruction.

## Adding or changing a template

1. Update HTML/CSS/JavaScript source under `templates/`; do not create or edit PPTX.
2. Rebuild outputs and previews; never assert visual verification without rendering.
3. Update `TEMPLATE_CATALOG.md` to include purpose, source, preview, and status.
4. Check title clipping, text overflow, alignment, arrow direction, responsive behavior.
5. Report changed files, tests, and remaining limitations.

## Avoid

- Do not propose future PPTX generation as a project milestone.

- Do not use templates solely for decoration, with no informational advantage.
- Do not fabricate benchmark results, model configurations, citations or sources.
- Do not automatically overwrite existing course styling because this library exists.
- Do not make commits to `sh0427-han-private` unless explicitly requested.


## Scroll / Slide dual-mode templates

- For dual-mode requests inspect `templates/dual-mode-learning/DESIGN.md` and `MODES.md` first.
- Share lesson content, math and interactive behavior between modes; separate only layout, navigation and explanatory density.
- Inherit the canonical `templates/html/styles.css` tokens and its global **-1pt** character spacing; do not re-declare conflicting colors.
- Preserve the existing Concept / Process / Comparison HTML patterns and the CNN Scroll/Slide implementation except where the task requires changes.


## Ongoing example refinement

- The eight HTML reference patterns and CNN Scroll/Slide lesson are editable, evolving reference samples.
- Do not add generic creator-facing meta notes or force subtitles onto multiple lines when avoidable.
- Prefer factual, computed visual explanation; distribute content visually across each slide.
- Validate representative desktop viewports: 1600x950, 1366x768, 1280x720.

## Titles and figure descriptions

- Use concise Korean noun-phrase or short-phrase slide titles. Avoid `~다` / `~입니다` endings in visible titles.
- Prefer short, direct figure labels and captions instead of `~입니다` sentences.
- Exclude authoring/meta commentary such as "교육용으로 직접 구현한 예제입니다" or "완성 디자인은 아닙니다" from visible slides.
- Preserve genuine figure attribution, necessary experimental conditions, and technically significant caveats.
- For Concept previews, keep the example image, pixel selection, RGB numerics, and tensor shape consistent.
