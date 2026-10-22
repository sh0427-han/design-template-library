"""Render canonical #4 Step-by-Step preview using repository CSS and real Pretendard.

Run from repository root: python scripts/render_step_pretendard.py
Requires: playwright and an installed Chromium. CDN network must be available.
No fallback-font screenshots are accepted as the canonical preview.
"""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import threading

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PREVIEW = ROOT / "previews" / "html-step-by-step.jpg"
REPORT = ROOT / "previews" / "review" / "step-pretendard-validation.json"
SCREEN_SIZES = ((1600, 950), (1440, 810), (1366, 768), (1280, 720), (900, 900), (390, 844))


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


GET_LAYOUT = """() => {
  const box = e => {const r=e.getBoundingClientRect(); return {x:r.x,y:r.y,right:r.right,bottom:r.bottom,cx:r.x+r.width/2,cy:r.y+r.height/2}};
  const slide=document.querySelector('section.slide');
  const panels=[...document.querySelectorAll('.calc-panel')];
  const feet=[...document.querySelectorAll('.calc-footnote')];
  const titles=[...document.querySelectorAll('.calc-item-title')];
  const rootStyle=getComputedStyle(document.documentElement);
  const slideStyle=getComputedStyle(slide);
  const loaded=[...document.fonts].filter(f=>f.family.replace(/["']/g,'')==='Pretendard Variable' && f.status==='loaded');
  return {
    computedFont:slideStyle.fontFamily,
    letterSpacing:rootStyle.letterSpacing,
    loadedFaces:loaded.length,
    loadedFonts:loaded.map(f=>({family:f.family,weight:f.weight,status:f.status})),
    pageScrollWidth:document.documentElement.scrollWidth,
    slide:box(slide), panels:panels.map(box), footer:box(document.querySelector('.footer')),
    lines:feet.map(box), titleBoxes:titles.map(box),
    imagesBroken:[...document.images].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src),
    selectedInput:[...document.querySelectorAll('.input5 .focus-rf')].map(e=>e.textContent.trim()),
    selectedOutput:document.querySelector('.output3 .focus-out').textContent.trim(),
    products:[...document.querySelectorAll('.product3 strong')].map(e=>e.textContent.trim()),
    equation:document.querySelector('.calc-equation').textContent.trim()
  };
}"""


def main():
    PREVIEW.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    report=[]
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True,args=['--no-sandbox'])
            page=browser.new_page(device_scale_factor=1)
            errors=[]
            page.on('pageerror',lambda exc:errors.append(str(exc)))
            for width,height in SCREEN_SIZES:
                page.set_viewport_size({'width':width,'height':height})
                page.goto(f'http://127.0.0.1:{server.server_port}/templates/html/step-by-step.html',wait_until='networkidle',timeout=60000)
                page.evaluate('document.fonts.ready')
                # Load actual Korean and Latin glyphs for representative text weights.
                fontcheck=page.evaluate("""async () => {
                    const family='"Pretendard Variable"';
                    const weights=[400,600,700,800];
                    const requests=await Promise.all(weights.map(w=>document.fonts.load(`${w} 22px ${family}`, '필터의 곱셈과 합산 Input ∑ ⊙')));
                    await document.fonts.ready;
                    return {
                        loadedCounts:requests.map(a=>a.length),
                        koreanSupported:document.fonts.check(`700 22px ${family}`,'필터의 곱셈과 합산'),
                        faces:[...document.fonts].filter(f=>f.family.replace(/["']/g,'')==='Pretendard Variable' && f.status==='loaded').length
                    };
                }""")
                assert min(fontcheck['loadedCounts']) > 0 and fontcheck['koreanSupported'] and fontcheck['faces'] > 0, (
                    width,'CDN Pretendard not loaded; refusing fallback screenshot',fontcheck)
                s=page.evaluate(GET_LAYOUT)
                assert s['computedFont'].startswith('"Pretendard Variable"'),(width,'font-family',s)
                assert abs(float(s['letterSpacing'].removesuffix('px')) + 4/3)<.02,(width,'tracking',s)
                assert s['pageScrollWidth']<=width+1,(width,'horizontal page overflow',s)
                assert s['products']==['1','0','−3','4','0','−6','7','0','−9'],(width,'products',s)
                assert s['selectedInput']==['1','2','3','4','5','6','7','8','9'],(width,'receptive field',s)
                assert s['selectedOutput']=='−6', (width,'output cell',s)
                assert not s['imagesBroken'],(width,'broken assets',s)
                if width>=1000:
                    assert abs(s['lines'][0]['y']-s['lines'][1]['y']) <= 1, (width,'footer dividers misaligned',s['lines'])
                    assert s['panels'][0]['right']<s['panels'][1]['x'], (width,'panels overlap')
                    assert max(x['bottom'] for x in s['panels'])<=s['footer']['y']+1,(width,'footer collision')
                report.append({'viewport':[width,height],'fontcheck':fontcheck,'layout':s})
                # True 1440x810 slide image at natural slide pixels; never a scaled local fallback.
                if width==1600:
                    page.locator('section.slide').screenshot(path=str(PREVIEW),type='jpeg',quality=94,animations='disabled')
            assert not errors,errors
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
    REPORT.write_text(json.dumps({'script':'scripts/render_step_pretendard.py','font':'Pretendard Variable v1.3.9 via repository CSS','result':'PASS','viewports':report},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'PASS Pretendard loaded + 6 viewport checks: {PREVIEW} ({PREVIEW.stat().st_size} bytes)')


if __name__=='__main__':
    main()