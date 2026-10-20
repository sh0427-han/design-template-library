# Design Template Library

Reusable **PPTX + HTML design references** for Korean technical lectures, AI/ML education, and engineering presentations.

**Owner:** [sh0427-han](https://github.com/sh0427-han) · **Version:** v0.1 (2026-10-20)

**Global typography:** All PPTX and HTML text uses **Condensed 1.0 pt (letter-spacing: -1pt)**, including headings, body, labels and footers.

## Template gallery

| Concept | Process | Comparison |
| --- | --- | --- |
| ![Concept slide](previews/html-concept.png) | ![Process slide](previews/html-process.png) | ![Comparison slide](previews/html-comparison.png) |
| Explain one concept | Input → Process → Output | Compare methods |

## Files

| Path | Purpose |
| --- | --- |
| [DESIGN_SYSTEM.md](DESIGN_SYSTEM.md) | Shared colors, layout, typography, QA rules |
| [TEMPLATE_CATALOG.md](TEMPLATE_CATALOG.md) | Template catalog and selection guide |
| [AGENTS.md](AGENTS.md) | AI / Codex instructions |
| [templates/html/index.html](templates/html/index.html) | HTML template gallery |
| [templates/pptx/technical-slide-templates.pptx](templates/pptx/technical-slide-templates.pptx) | Editable 3-slide PowerPoint deck |
| [templates/pptx/build_templates.py](templates/pptx/build_templates.py) | PPTX source / generator |
| [docs/USAGE.md](docs/USAGE.md) | Usage and cross-project references |

## Quick start

HTML: open `templates/html/index.html` in a browser.

PPTX: open `templates/pptx/technical-slide-templates.pptx` in PowerPoint; all text and diagrams are editable. To regenerate:

```bash
pip install -r templates/pptx/requirements.txt
python templates/pptx/build_templates.py
```

To verify that **all existing PPTX text runs** and the shared HTML styles use `-1pt`:

```bash
python scripts/verify_character_spacing.py
```

## How to reference from ChatGPT / Codex

> Use `https://github.com/sh0427-han/design-template-library` as the shared design reference. Before using, inspect `DESIGN_SYSTEM.md` and `TEMPLATE_CATALOG.md`, then use the relevant template. Existing project requirements override this library.

For details, see [docs/USAGE.md](docs/USAGE.md).

## Scope

This is a **shared design library**, not an existing lecture repository. It does not automatically modify projects under the separate `sh0427-han-private` account. Source attribution is required for external figures and images.


## Dual-mode Learning (Scroll / Slide)

- [Dual-mode template](templates/dual-mode-learning/): 동일 콘텐츠를 **웹 교과서(Scroll)** 및 **16:9 발표 슬라이드(Slide)**로 표시합니다.
- [모드 선택](templates/dual-mode-learning/index.html) · [Scroll 원본](templates/dual-mode-learning/scroll.html) · [Slide 원본](templates/dual-mode-learning/slides.html)
- [Slide 예시](previews/dual-mode-lab-slide.jpg) · [Scroll 예시](previews/dual-mode-scroll.jpg)
- `templates/html/styles.css`의 공통 색상·폰트·전역 자간 **-1pt**를 재사용하며, 5개 CNN 개념 섹션과 필터 시뮬레이터의 콘텐츠/계산 로직을 공유합니다.
- AIBook [Attention 인터랙티브 예제](https://aibook.euiyun.com/chapters/attention.html#sim-editor)는 디자인·학습 흐름 참고자료이며 소스 코드를 복사하지 않았습니다.
