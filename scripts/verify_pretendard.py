"""Verify original-reference parity in Scroll/Slide and write exactly two previews."""
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
import hashlib,json,threading
from playwright.sync_api import sync_playwright
from reference_validation import browser_options
from verify_dual_mode import validate_dual_mode,get_frame,SIZES
ROOT=Path(__file__).resolve().parents[1]
PREVIEWS=ROOT/'previews'
class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self,*_):pass
    def do_GET(self):
        if self.path=='/favicon.ico':self.send_response(204);self.end_headers();return
        super().do_GET()


def main():
    PREVIEWS.mkdir(parents=True,exist_ok=True);(PREVIEWS/'review').mkdir(exist_ok=True)
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    cases=[];errors=[]
    try:
        with sync_playwright() as playwright:
            browser=playwright.chromium.launch(**browser_options())
            base=f'http://127.0.0.1:{server.server_port}'
            detailed=validate_dual_mode(browser,base,ROOT,Path('/tmp/dual-mode-review'))
            page=browser.new_page(device_scale_factor=1);page.on('pageerror',lambda e:errors.append(str(e)))
            for width,height in SIZES:
                page.set_viewport_size({'width':width,'height':height})
                for path,kind in [('templates/html/index.html','gallery'),('templates/dual-mode-learning/scroll.html','scroll'),('templates/dual-mode-learning/slides.html','slides')]:
                    page.goto(base+'/'+path,wait_until='networkidle');page.evaluate('document.fonts.ready')
                    if kind!='gallery':get_frame(page,'concept')
                    state=page.evaluate('''()=>({family:getComputedStyle(document.body).fontFamily,spacing:getComputedStyle(document.documentElement).letterSpacing,loaded:[...document.fonts].filter(f=>f.family.replace(/["']/g,'')==='Pretendard Variable'&&f.status==='loaded').length,width:document.documentElement.scrollWidth})''')
                    assert 'Pretendard Variable' in state['family'] and state['loaded']>0,state
                    assert abs(float(state['spacing'].removesuffix('px'))+4/3)<.02 and state['width']<=width,state
                    if kind=='gallery':
                        broken=page.locator('img').evaluate_all('async(es)=>{for(const e of es)e.loading="eager";await Promise.all(es.map(e=>e.decode().catch(()=>null)));return es.filter(e=>!e.complete||!e.naturalWidth).map(e=>e.src)}')
                        assert not broken,broken
                    elif width==1600:
                        page.screenshot(path=str(PREVIEWS/f'dual-mode-{kind[:-1] if kind=="slides" else kind}.jpg'),type='jpeg',quality=92)
                    cases.append({'kind':kind,'viewport':[width,height],'font':state})
            assert not errors,errors
            browser.close()
    finally:server.shutdown();server.server_close()
    names=('dual-mode-scroll.jpg','dual-mode-slide.jpg')
    assert sorted(p.name for p in PREVIEWS.glob('dual-mode-*.jpg'))==sorted(names),'Only Scroll and Slide canonical previews are supported'
    report={'status':'passed','cases':cases,'page_errors':errors,'pc_validation':detailed,'preview_sha256':{n:hashlib.sha256((PREVIEWS/n).read_bytes()).hexdigest() for n in names}}
    (PREVIEWS/'review/dual-mode-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(f'PASS {len(detailed["cases"])} original-reference layouts, two modes/two previews, actual fonts, source-design parity and state roundtrip')
if __name__=='__main__':
    try:
        main()
    except Exception:
        # Keep the diagnostic available through the Checks API as well as logs.
        # The assertion data contains only rendered reference content and paths.
        import traceback
        detail=traceback.format_exc()[-6000:]
        detail=detail.replace('%','%25').replace('\r','%0D').replace('\n','%0A')
        print('::error title=Scroll / Slide validation::'+detail,flush=True)
        raise
