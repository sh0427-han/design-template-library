"""Verify global condensed 1.0 pt character spacing in HTML and PPTX.

Usage:
    python scripts/verify_character_spacing.py

The HTML check validates the shared CSS source. Use the Playwright renderer
separately to confirm computed styles and visual overflow.
"""

from __future__ import annotations

import re
from pathlib import Path
from xml.etree import ElementTree
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
CSS_PATH = ROOT / "templates/html/styles.css"
PPTX_PATH = ROOT / "templates/pptx/technical-slide-templates.pptx"
EXPECTED_SPACING_PT = -1.0
XML_SPACING = str(round(EXPECTED_SPACING_PT * 100))
NAMESPACE = "{http://schemas.openxmlformats.org/drawingml/2006/main}"


def verify_html() -> None:
    """Confirm CSS inherits a single global -1pt text-spacing setting."""
    css = CSS_PATH.read_text(encoding="utf-8")
    assert "--character-spacing: -1pt;" in css
    assert re.search(
        r"\bhtml\s*\{\s*letter-spacing:\s*var\(--character-spacing\);",
        css,
    )
    declarations = re.findall(r"(?<!-)\bletter-spacing\s*:\s*([^;]+);", css)
    assert declarations == ["var(--character-spacing)"], declarations
    print("PASS HTML: -1pt applied globally with no component overrides")


def verify_pptx() -> None:
    """Confirm every editable text run in every slide uses spc=-100."""
    checked = 0
    with ZipFile(PPTX_PATH) as archive:
        slides = sorted(
            n for n in archive.namelist()
            if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)
        )
        assert slides, "No slide XML files found"
        for slide_path in slides:
            root = ElementTree.fromstring(archive.read(slide_path))
            runs = root.findall(f".//{NAMESPACE}r")
            for run in runs:
                run_properties = run.find(f"{NAMESPACE}rPr")
                assert run_properties is not None, slide_path
                actual = run_properties.get("spc")
                assert actual == XML_SPACING, (
                    f"{slide_path}: expected {XML_SPACING}, got {actual}"
                )
                checked += 1
    assert checked > 0
    print(f"PASS PPTX: {checked} text runs across {len(slides)} slides")


def main() -> None:
    verify_html()
    verify_pptx()


if __name__ == "__main__":
    main()
