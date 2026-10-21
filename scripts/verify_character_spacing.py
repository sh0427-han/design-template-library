"""Verify the shared HTML -1pt character spacing without PPTX dependencies.

Usage:
    python scripts/verify_character_spacing.py

The CSS source check complements the Chromium rendered-layout checks.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS_PATH = ROOT / "templates/html/styles.css"


def verify_html() -> None:
    """Confirm that the shared CSS applies -1pt to all HTML text."""
    css = CSS_PATH.read_text(encoding="utf-8")
    assert "--character-spacing: -1pt;" in css
    assert re.search(
        r"\bhtml\s*\{\s*letter-spacing:\s*var\(--character-spacing\);",
        css,
    )
    declarations = re.findall(r"(?<!-)\bletter-spacing\s*:\s*([^;]+);", css)
    assert declarations == ["var(--character-spacing)"], declarations
    assert '"Pretendard Variable"' in css
    print("PASS HTML: Pretendard and global -1pt spacing")


if __name__ == "__main__":
    verify_html()
