# Agent / Codex instructions

## Repository scope

- Canonical repository: https://github.com/sh0427-han/design-template-library
- Repository owner: `sh0427-han` (ChatGPT GitHub connection: `배포용`)
- Do not confuse it with `sh0427-han-private` (separate private project account).
- This is a reusable **design reference library**, not an application deployment repository.

## Before any edit

1. Read `DESIGN_SYSTEM.md` and `TEMPLATE_CATALOG.md`.
2. Inspect the relevant source under `templates/` and preview under `previews/`.
3. Scope the change to requested artifacts. Preserve unrelated templates.

## Core rules

- One main concept per slide; use diagrams and data flows where helpful.
- Ensure technical accuracy, especially equations, tensor layouts, CNN flows and metrics.
- Maintain visual consistency between PPT and HTML, while respecting format-specific constraints.
- Apply **condensed character spacing of 1.0 pt (`-1pt`) to ALL text** (title, body, label, caption, footer, gallery), in both PPTX and HTML. Use shared constants; never override only for labels or headings without explicit user request.
- Preserve editability: do not rasterize PPT slide backgrounds.
- Do not insert third-party figures without a source URL near the figure.
- User/project-specific requirements take priority over the library defaults.
- Do not edit external repositories without explicit instruction.

## Adding or changing a template

1. Update editable source in `templates/html` and/or `templates/pptx`.
2. Rebuild outputs and previews; never assert visual verification without rendering.
3. Update `TEMPLATE_CATALOG.md` to include purpose, source, preview, and status.
4. Check title clipping, text overflow, alignment, arrow direction, responsive behavior.
5. Report changed files, tests, and remaining limitations.

## Avoid

- Do not use templates solely for decoration, with no informational advantage.
- Do not fabricate benchmark results, model configurations, citations or sources.
- Do not automatically overwrite existing course styling because this library exists.
- Do not make commits to `sh0427-han-private` unless explicitly requested.
