"""Validate the font comparison page's controls and original-slide isolation.

These tests check font-family CSS selection, not actual Malgun glyph appearance:
Linux runners do not include the Windows-only Malgun Gothic font.
"""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import threading

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


class Handler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def main():
    server = ThreadingHTTPServer(
        ("127.0.0.1", 0), partial(Handler, directory=str(ROOT))
    )
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                headless=True, args=["--no-sandbox"]
            )
            page = browser.new_page()
            for width, height in [(1500, 950), (390, 844)]:
                page.set_viewport_size({"width": width, "height": height})
                page.goto(
                    f"http://127.0.0.1:{server.server_port}"
                    "/templates/html/font-comparison.html",
                    wait_until="domcontentloaded",
                )
                for target, title in [
                    ("concept", "이미지의 숫자 구조"),
                    ("architecture", "CNN 아키텍처"),
                ]:
                    page.locator(f"button[data-page='{target}']").click()
                    page.wait_for_function(
                        """title => [...document.querySelectorAll('.paper-frame')].every(
                          frame => frame.contentDocument?.querySelector('h1')
                          ?.textContent.trim() === title
                        )""",
                        arg=title,
                    )
                    details = page.evaluate(
                        """() => [...document.querySelectorAll('.paper-frame')].map(f=>{
                          const doc = f.contentDocument;
                          const h1 = doc.querySelector('h1');
                          return {
                            family: getComputedStyle(h1).fontFamily,
                            spacing: getComputedStyle(h1).letterSpacing,
                            width: doc.documentElement.scrollWidth,
                            documentTitle: doc.title
                          };
                        })"""
                    )
                    assert details[0]["family"].startswith('"Malgun Gothic"'), details
                    assert details[1]["family"].startswith('"Pretendard Variable"'), details
                    assert all(abs(float(d["spacing"].removesuffix("px")) + 4/3) < .03
                               for d in details), details
                    assert page.evaluate(
                        "document.documentElement.scrollWidth <= innerWidth"
                    ), (width, target, "horizontal scroll")
                    page.locator("button[data-view='pretendard']").click()
                    assert page.locator(".sample--malgun").is_hidden()
                    assert page.locator(".sample--pretendard").is_visible()
                    page.locator("button[data-view='both']").click()
                    assert page.locator(".sample--malgun").is_visible()
                    print(f"PASS: {target} {width}x{height} — labels, fonts, controls")
            browser.close()
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
