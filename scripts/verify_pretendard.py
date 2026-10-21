"""Validate the shared Pretendard font in gallery and CNN scroll/slide.

Also refresh the three HTML dual-mode preview images after font changes.
The PPTX and unrelated HTML source documents are not modified.
"""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import threading

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PREVIEWS = ROOT / "previews"


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


FONT_CHECK = """() => {
  const font = getComputedStyle(document.body).fontFamily;
  const letterSpacing = getComputedStyle(document.documentElement).letterSpacing;
  const faces = [...document.fonts].filter(f =>
    f.family.replace(/["']/g, '') === 'Pretendard Variable' &&
    f.status === 'loaded'
  );
  return {font, letterSpacing, loadedFaces: faces.length,
    scrollWidth: document.documentElement.scrollWidth};
}"""


def main():
    PREVIEWS.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer(
        ("127.0.0.1", 0), partial(QuietHandler, directory=str(ROOT))
    )
    threading.Thread(target=server.serve_forever, daemon=True).start()
    checks = 0
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                headless=True, args=["--no-sandbox"]
            )
            page = browser.new_page(device_scale_factor=1)
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            pages = [
                ("templates/html/index.html", "gallery"),
                ("templates/dual-mode-learning/scroll.html", "scroll"),
                ("templates/dual-mode-learning/slides.html", "slides"),
            ]
            for width, height in ((1500, 950), (390, 844)):
                page.set_viewport_size({"width": width, "height": height})
                for path, kind in pages:
                    page.goto(
                        f"http://127.0.0.1:{server.server_port}/{path}",
                        wait_until="networkidle",
                    )
                    page.evaluate("document.fonts.ready")
                    result = page.evaluate(FONT_CHECK)
                    assert result["font"].startswith('"Pretendard Variable"'), (
                        kind, width, result
                    )
                    assert abs(
                        float(result["letterSpacing"].removesuffix("px")) + 4 / 3
                    ) < .02, (kind, width, result)
                    assert result["loadedFaces"] > 0, (
                        kind, width, "font did not load from CDN", result
                    )
                    assert result["scrollWidth"] <= width, (
                        kind, width, "horizontal overflow", result
                    )
                    if width == 1500:
                        if kind == "gallery":
                            continue
                        if kind == "scroll":
                            page.screenshot(
                                path=str(PREVIEWS / "dual-mode-scroll.jpg"),
                                type="jpeg", quality=90,
                            )
                        if kind == "slides":
                            page.locator("#slide-root .slide-sheet").first.wait_for()
                            page.screenshot(
                                path=str(PREVIEWS / "dual-mode-process-slide.jpg"),
                                type="jpeg", quality=90,
                            )
                            page.goto(
                                f"http://127.0.0.1:{server.server_port}/"
                                "templates/dual-mode-learning/slides.html"
                                "#experiment", wait_until="networkidle",
                            )
                            page.evaluate("document.fonts.ready")
                            assert page.locator("#progress").inner_text() == "4 / 5"
                            page.screenshot(
                                path=str(PREVIEWS / "dual-mode-lab-slide.jpg"),
                                type="jpeg", quality=90,
                            )
                    checks += 1
            assert not errors, errors
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
    print("PASS: shared Pretendard family, real font load, -1pt and "
          f"horizontal bounds on {checks} screen combinations")


if __name__ == "__main__":
    main()
