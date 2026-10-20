"""Capture source HTML templates as true 16:9 PNG screenshots.

Requires playwright and an installed Chromium browser.
For example: python -m pip install playwright; python -m playwright install chromium
"""

import os
import shutil
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML_DIR = ROOT / "templates" / "html"
PREVIEW_DIR = ROOT / "previews"
TEMPLATE_IDS = ("concept", "process", "comparison")


def main() -> None:
    """Render three HTML slides and check canvas overflow."""
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser_executable = (
            os.environ.get("CHROMIUM_EXECUTABLE")
            or shutil.which("chromium")
            or shutil.which("chromium-browser")
        )
        kwargs = {"headless": True, "args": ["--no-sandbox"]}
        if browser_executable:
            kwargs["executable_path"] = browser_executable
        browser = playwright.chromium.launch(**kwargs)
        page = browser.new_page(
            viewport={"width": 1500, "height": 950},
            device_scale_factor=1,
        )
        for template_id in TEMPLATE_IDS:
            html = (HTML_DIR / f"{template_id}.html").read_text(encoding="utf-8")
            css = (HTML_DIR / "styles.css").read_text(encoding="utf-8")
            html = html.replace(
                '<link rel="stylesheet" href="styles.css">',
                f"<style>{css}</style>",
            )
            page.set_content(html, wait_until="load")
            slide = page.locator(".slide")
            assert slide.count() == 1
            metrics = slide.evaluate(
                """el => ({
                    width: el.clientWidth,
                    height: el.clientHeight,
                    scrollWidth: el.scrollWidth,
                    scrollHeight: el.scrollHeight
                })"""
            )
            assert metrics["scrollWidth"] <= metrics["width"] + 1, metrics
            assert metrics["scrollHeight"] <= metrics["height"] + 1, metrics
            output_path = PREVIEW_DIR / f"html-{template_id}.png"
            slide.screenshot(path=str(output_path), animations="disabled")
            print(template_id, metrics, output_path)
        browser.close()


if __name__ == "__main__":
    main()
