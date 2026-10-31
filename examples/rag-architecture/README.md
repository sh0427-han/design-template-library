# 검색 증강 생성

One editable Korean concept page, shared across [Scroll](scroll.html#rag) and [Slide](slides.html#rag).

Serve the supplied root: `python -m http.server 8000`, then open `/examples/rag-architecture/scroll.html` or `slides.html`. Keep the supplied `templates/html` assets at their relative paths.

Verify with `python examples/rag-architecture/verify.py` (Python Playwright and /usr/bin/chromium). Evidence: verification.json, eight screenshots, VALIDATION.md, READ_LOG.md. DESIGN.md and D0.md were committed before implementation.

## Current variant validation and historical evidence

The stage 4 authored title alternative and content boundary tests are documented in [the hardening report](../../docs/rag-hardening/REPORT.md). Run `python docs/rag-hardening/verify_variants.py` from the repository root for current evidence. This test injects authored variants in the browser; it adds no extra public slide or interaction.

The existing verification.json and fresh-builder-trial evidence remain PR #27 snapshots. Their pinned integrity check should be run at f368f77, not interpreted as current CSS validation. The current baseline/variant evidence lives under `docs/rag-hardening/`; first-result history remains available at the original commits.
