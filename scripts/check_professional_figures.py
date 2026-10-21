"""Verify derived CNN feature maps and compare/process figure continuity.

Runs a local static file server and real Chromium; only three standalone
HTML examples are tested. CNN Scroll/Slide is deliberately untouched.
"""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import threading

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
NAMES = ('architecture', 'process', 'comparison')
VIEWPORTS = ((1500,950),(1366,768),(1280,720),(900,900),(390,844))


class Handler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def main():
    srv=ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(ROOT)))
    threading.Thread(target=srv.serve_forever,daemon=True).start()
    results=[]
    try:
        with sync_playwright() as playwright:
            browser=playwright.chromium.launch(headless=True,args=['--no-sandbox'])
            page=browser.new_page()
            errors=[]
            page.on('pageerror',lambda err:errors.append(str(err)))
            for width,height in VIEWPORTS:
                page.set_viewport_size(dict(width=width,height=height))
                for name in NAMES:
                    page.goto(
                        f'http://127.0.0.1:{srv.server_port}/templates/html/{name}.html',
                        wait_until='networkidle'
                    )
                    page.wait_for_function(
                        "document.querySelector('.slide').dataset.computedMaps === 'true'"
                    )
                    info=page.evaluate("""() => {
                      const svg = [...document.querySelectorAll(
                        '.process-feature-svg,.compare-feature-svg,'+
                        '.paper-conv .activation-stack,.paper-pool .activation-stack,'+
                        '.paper-conv2 .activation-stack')];
                      return {
                        width:document.documentElement.scrollWidth,
                        figures:svg.map(el=>({
                          done:el.dataset.computed,
                          channels:Number(el.dataset.channelCount),
                          maps:el.querySelectorAll('image').length,
                          sources:[...el.querySelectorAll('image')].every(
                            e=>(e.getAttribute('href')||'').startsWith('data:image/png;'))
                        })),
                        photos:[...document.querySelectorAll('img[src*="concept-apple-photo"]')].map(
                           el=>el.complete && el.naturalWidth>0),
                        svgPhotoCount:document.querySelectorAll(
                          'svg image[href*="concept-apple-photo"]').length,
                        pools:document.querySelector('.architecture-slide')?.dataset.poolCheck,
                        gap:document.querySelector('.architecture-slide')?.dataset.gapLength,
                        noOutside:document.documentElement.scrollWidth<=innerWidth
                      };
                    }""")
                    assert info['noOutside'] and info['width']<=width,(name,width,info)
                    assert all(f['done']=='true' and f['sources'] for f in info['figures']),(
                        name,width,info)
                    if name=='architecture':
                        assert info['svgPhotoCount']==1, (name,width,'input image missing',info)
                    else:
                        assert info['photos'] and all(info['photos']),(name,width,info)
                    if name=='architecture':
                        assert info['pools']=='pass' and info['gap']=='32',(width,info)
                        assert [(f['channels'],f['maps']) for f in info['figures']]==[
                            (16,4),(16,4),(32,5)
                        ],(width,info)
                        assert page.locator('.paper-shape').all_text_contents()==[
                            '64×64×3','64×64×16','32×32×16',
                            '32×32×32','32','3 logits'
                        ]
                    else:
                        assert len(info['figures'])==1 and info['figures'][0]['channels']==16
                        if name=='comparison':
                            assert len(info['photos'])==2
                            assert page.locator('.rule-conditions span').all_text_contents()==[
                                '색상 조건','형태 조건'
                            ]
                    results.append(f'{name} {width}×{height}')
            assert not errors, errors
            browser.close()
    finally:
        srv.shutdown()
        srv.server_close()
    print(f'PASS: {len(results)} real-browser derived-figure checks, pooling relation, pictures and responsive layout')


if __name__=='__main__':
    main()
