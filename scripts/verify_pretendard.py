"""Validate the shared Pretendard font in gallery and CNN scroll/slide.

Also refresh the three HTML dual-mode preview images after font changes.
Gallery and the two modes use the same bundled font; their content is preserved.
"""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import threading
import json

from playwright.sync_api import sync_playwright
from reference_validation import browser_options

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
    cases = []
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(**browser_options())
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
                        kind, width, "local Pretendard did not load", result
                    )
                    assert result["scrollWidth"] <= width, (
                        kind, width, "horizontal overflow", result
                    )
                    if width == 1500:
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
                    cdp=page.context.new_cdp_session(page)
                    cdp.send('DOM.enable');cdp.send('CSS.enable')
                    root=cdp.send('DOM.getDocument')['root']['nodeId']
                    selector='.slide-sheet[aria-hidden="false"] h2' if kind=='slides' else 'h1'
                    heading=cdp.send('DOM.querySelector',{'nodeId':root,'selector':selector})['nodeId']
                    assert heading,(kind,selector)
                    fonts=cdp.send('CSS.getPlatformFontsForNode',{'nodeId':heading})['fonts']
                    assert fonts and all(f['familyName']=='Pretendard Variable' and f['isCustomFont'] for f in fonts),(kind,fonts)
                    cdp.detach();checks += 1
                    cases.append({'kind':kind,'viewport':[width,height],'font':result,'actual_heading_fonts':fonts})
            assert not errors, errors
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
    (PREVIEWS/'review/dual-mode-validation.json').write_text(json.dumps({'status':'passed','cases':cases,'page_errors':errors},ensure_ascii=False,indent=2)+'\n')
    print("PASS: shared Pretendard family, real font load, -1pt and "
          f"horizontal bounds on {checks} screen combinations")


if __name__ == "__main__":
    main()
