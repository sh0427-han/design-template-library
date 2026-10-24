"""Verify the single symbolic concept page, its math, fonts and two display modes."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import hashlib, json, math, re, shutil, threading, traceback
from datetime import datetime, timezone
from playwright.sync_api import sync_playwright
from reference_validation import actual_fonts, browser_options

ROOT=Path(__file__).resolve().parents[1]
LESSON=ROOT/'examples/logistic-regression'
OUT=Path('/tmp/logistic-reuse-review')
SIZES=[(1600,950),(1440,810),(1366,768),(1280,720)]

GEOMETRY = r'''id => {
 const slide=document.querySelector(`[data-page="${id}"]`),s=slide.getBoundingClientRect(),scale=s.width/1440;
 const rect=e=>{const r=e.getBoundingClientRect();return {x:(r.x-s.x)/scale,y:(r.y-s.y)/scale,width:r.width/scale,height:r.height/scale,right:(r.right-s.x)/scale,bottom:(r.bottom-s.y)/scale}};
 const visible=[...slide.querySelectorAll('*')].filter(e=>!e.closest('.sr-only')&&e.getBoundingClientRect().width&&e.getBoundingClientRect().height);
 const overflow=[],clippedText=[],paddingErrors=[];
 for(const e of visible) {
  const b=rect(e);
  if(b.x < -1 || b.right > 1441 || b.y < -1 || b.bottom > 811)overflow.push(e.getAttribute('class')||e.tagName);
  if(e instanceof SVGElement)continue;
  for(const n of e.childNodes)if(n.nodeType===3&&n.textContent.trim()){
   const range=document.createRange();range.selectNodeContents(n);
   for(const r of range.getClientRects())if(r.left<e.getBoundingClientRect().left-1*scale||r.right>e.getBoundingClientRect().right+1*scale)clippedText.push(e.getAttribute('class')||e.tagName);
  }
 }
 const panels=[...slide.querySelectorAll('.lr-panel')];
 for(const card of panels){
  const b=rect(card),css=getComputedStyle(card),p={left:parseFloat(css.paddingLeft)+1,right:parseFloat(css.paddingRight)+1,top:parseFloat(css.paddingTop)+1,bottom:parseFloat(css.paddingBottom)+1};
  for(const child of card.children){const c=rect(child);if(c.x<b.x+p.left-1||c.right>b.right-p.right+1||c.y<b.y+p.top-1||c.bottom>b.bottom-p.bottom+1)paddingErrors.push(child.className);}
 }
 const footer=rect(slide.querySelector('footer')),caption=rect(slide.querySelector('.ref-takeaway'));
 const texts=visible.filter(e=>[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()));
 const styles=texts.map(e=>{const c=getComputedStyle(e);return {text:e.textContent.trim(),size:c.fontSize,weight:c.fontWeight,lineHeight:c.lineHeight,spacing:c.letterSpacing,color:c.color}});
 const fingerprints=[...slide.querySelectorAll('*')].filter(e=>!e.closest('.sr-only')).map(e=>{
  const c=getComputedStyle(e);return {tag:e.tagName,classes:e.getAttribute('class'),text:e.childElementCount?'':e.textContent.trim(),box:rect(e),style:[c.fontFamily,c.fontSize,c.fontWeight,c.lineHeight,c.letterSpacing,c.color,c.backgroundColor,c.borderRadius,c.padding,c.gap]};
 });
 return {overflow,clippedText,paddingErrors,footer,caption,panels:panels.map(rect),styles,fingerprints,
  frame:{width:s.width,height:s.height},pageWidth:document.documentElement.scrollWidth,viewport:innerWidth,
  captionGap:Math.min(...panels.map(p=>caption.y-rect(p).bottom)),footerGap:footer.y-caption.bottom,
  labelY:[...slide.querySelectorAll('.lr-step-label')].map(e=>rect(e).y),
  symbolAxisErrors:[...slide.querySelectorAll('.lr-symbols > div')].map((e,i)=>{const a=rect(e),b=rect(slide.querySelectorAll('.lr-step')[i]);return Math.abs(a.x+a.width/2-b.x-b.width/2)}),
  inputCenters:[...slide.querySelectorAll('.lr-feature-value')].map(e=>{const a=rect(e.querySelector('math')),b=rect(e.parentElement),c=getComputedStyle(e.parentElement);return {error:Math.abs(a.x+a.width/2-b.x-b.width/2),paddingX:parseFloat(c.paddingLeft),paddingY:parseFloat(c.paddingTop)}}),
  arrowAxisErrors:[...slide.querySelectorAll('.lr-connector')].map(a=>{const b=rect(a),p=rect(a.previousElementSibling.querySelector('.lr-figure')),n=rect(a.nextElementSibling.querySelector('.lr-figure'));return Math.max(Math.abs(b.y+b.height/2-p.y-p.height/2),Math.abs(b.y+b.height/2-n.y-n.height/2));}),
  headingGaps:[...slide.querySelectorAll('.lr-heading,.lr-concept-heading')].map(e=>getComputedStyle(e).rowGap),
  conceptValueCount:slide.querySelectorAll('[data-value]').length,
  curve:slide.querySelector('.lr-sigmoid-path').getAttribute('d'),
  unwanted:slide.querySelectorAll('.lr-curve-point,.lr-point-guides,input,[data-page="calculation"],[data-page="threshold"]').length,
  fractions:[...slide.querySelectorAll('.lr-sigmoid-formula mfrac')].map(e=>({numerator:rect(e.children[0]),denominator:rect(e.children[1])}))};
}'''
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *_): pass
    def do_GET(self):
        if self.path == '/favicon.ico':
            self.send_response(204); self.end_headers(); return
        super().do_GET()

def compare_design(a, b):
    assert len(a) == len(b)
    maximum = 0
    for x, y in zip(a, b):
        assert (x['tag'],x['classes'],x['text'],x['style']) == (y['tag'],y['classes'],y['text'],y['style']), (x,y)
        # Elements without a rendered box have no meaningful position relative
        # to a slide that moves with the surrounding Scroll layout.
        if not any(x['box'][k] or y['box'][k] for k in ('width','height')):continue
        error = max(abs(x['box'][k]-y['box'][k]) for k in x['box'])
        # The SVG text glyph bounds may differ slightly with a scaled text paint.
        assert error < (1 if x['tag'] in ('svg','g','path','circle','text') else .3), (error,x,y)
        maximum=max(maximum,error)
    return maximum


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    for path in OUT.glob('*.png'):path.unlink()
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    report={'status':'running','started_utc':datetime.now(timezone.utc).isoformat(),'cases':[]}
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(**browser_options());report['browser']=browser.version
            page=browser.new_page(device_scale_factor=1)
            errors=[];failed=[];http=[]
            page.on('pageerror',lambda e:errors.append(str(e)))
            page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
            page.on('requestfailed',lambda r:failed.append(r.url))
            page.on('response',lambda r:http.append(f'{r.status} {r.url}') if r.status>=400 else None)
            base=f'http://127.0.0.1:{server.server_port}/examples/logistic-regression'
            baseline={}
            for width,height in SIZES:
                page.set_viewport_size({'width':width,'height':height})
                for mode in ['slides','scroll']:
                    page.goto(f'{base}/{mode}.html',wait_until='networkidle')
                    page.wait_for_function('document.documentElement.dataset.ready==="true"')
                    page.evaluate('()=>document.fonts.ready')
                    assert page.locator('[data-page]').count()==1
                    assert page.locator('.footer').inner_text().strip().endswith('01 / 01')
                    assert page.locator('.appendix-link').count()==0
                    if mode=='slides':
                        assert page.locator('#progress').inner_text()=='1 / 1'
                        assert page.locator('#prev').is_disabled() and page.locator('#next').is_disabled()
                    else:assert page.locator('#toc-list a').count()==1
                    geometry=page.evaluate(GEOMETRY,'concept')
                    for key in ['overflow','clippedText','paddingErrors']:assert not geometry[key],(mode,width,key,geometry[key])
                    assert not geometry['unwanted'] and geometry['conceptValueCount']==0
                    assert geometry['pageWidth']<=width and abs(geometry['frame']['width']/geometry['frame']['height']-16/9)<.00001
                    assert geometry['captionGap']>=13 and geometry['footerGap']>=14
                    assert max(p['bottom'] for p in geometry['panels'])<geometry['caption']['y']
                    assert max(geometry['labelY'])-min(geometry['labelY'])<.02 and max(geometry['arrowAxisErrors'])<.02
                    assert len(geometry['symbolAxisErrors'])==4 and max(geometry['symbolAxisErrors'])<.02
                    assert len(geometry['inputCenters'])==2 and all(c['error']<.02 and c['paddingX']>=24 and c['paddingY']>=16 for c in geometry['inputCenters'])
                    bad=[s for s in geometry['styles'] if s['spacing']=='normal' or abs(float(s['spacing'].removesuffix('px'))+4/3)>=.02 or s['lineHeight']=='normal']
                    assert not bad,bad
                    assert all(g=='8px' for g in geometry['headingGaps'])
                    assert geometry['fractions'] and all(f['numerator']['bottom']<f['denominator']['y'] for f in geometry['fractions'])
                    points=[tuple(map(float,pair)) for pair in re.findall(r'[ML]([\d.-]+),([\d.-]+)',geometry['curve'])]
                    assert len(points)==161
                    for i,(x,y) in enumerate(points):
                        z=-4+i/20
                        assert abs(x-(40+(z+4)/8*240))<.001
                        assert abs(y-(172-150/(1+math.exp(-z))))<.001
                    formulas=page.evaluate("""()=>({score:[...document.querySelector('.lr-score-general').querySelectorAll('mi')].map(e=>e.textContent),sigmoid:document.querySelector('.lr-sigmoid-formula').textContent,probability:document.querySelector('.lr-probability strong').textContent})""")
                    assert formulas['score']==['z','w','x','w','x','b']
                    assert formulas['sigmoid']=='σ(z)=11+e−z' and formulas['probability']=='p=σ(z)',formulas
                    fonts=actual_fonts(page,'.logistic-lesson *',math_family='STIX Two Math')
                    assert fonts['elements']>0 and not any(fonts[k] for k in ['fallback','unpainted','bad_spacing']),fonts
                    assert min(fonts['loaded']['counts'])>0 and fonts['loaded']['math']['count']>0
                    assert fonts['families'].get('STIX Two Math',0)>0 and fonts['families'].get('Pretendard Variable',0)>0
                    fp=geometry.pop('fingerprints')
                    if mode=='slides':baseline[width]=fp;parity_error=0
                    else:parity_error=compare_design(baseline[width],fp)
                    report['cases'].append(dict(mode=mode,template='concept',viewport=[width,height],geometry=geometry,fonts=fonts,max_mode_box_error=parity_error))
                    page.locator('[data-page="concept"]').screenshot(path=str(OUT/f'{mode}-concept-{width}x{height}.png'),animations='disabled')
                    if width==1600:page.screenshot(path=str(LESSON/f'previews/{"slide" if mode=="slides" else mode}.jpg'),type='jpeg',quality=94,animations='disabled')
                    print('PASS',mode,'concept',width,height,flush=True)
            for mode in ['slides','scroll']:
                page.goto(f'{base}/{mode}.html?appendix=1&threshold=72&sample=4#ref-calculation',wait_until='networkidle')
                page.wait_for_function('document.documentElement.dataset.ready==="true"')
                assert page.locator('[data-page]').count()==1 and page.url.endswith('#ref-concept')
                assert 'appendix=' not in page.url and 'threshold=' not in page.url and 'sample=' not in page.url
                assert page.locator('input,.appendix-link').count()==0
                page.locator('.mode-link').click();page.wait_for_function('document.documentElement.dataset.ready==="true"')
                page.reload(wait_until='networkidle');page.wait_for_function('document.documentElement.dataset.ready==="true"')
                assert page.locator('[data-page]').count()==1 and page.url.endswith('#ref-concept')
            page.goto(f'{base}/slides.html#ref-threshold',wait_until='networkidle');page.wait_for_function('document.documentElement.dataset.ready==="true"')
            for key in ['End','Home','ArrowRight','ArrowLeft','PageDown','PageUp',' ']:
                page.keyboard.press(key);assert page.url.endswith('#ref-concept')
            assert not errors and not failed and not http,(errors,failed,http)
            report.update(status='passed',main_pages=1,appendix_pages=0,concept_is_symbolic=True,curve_points=161,legacy_urls_normalized=True,keyboard=True,mode_roundtrip=True,page_errors=errors,failed_requests=failed,http_errors=http)
            shutil.copyfile(OUT/'slides-concept-1600x950.png',LESSON/'review/concept.png')
            browser.close()
    except Exception as exc:
        report.update(status='failed',error=str(exc));raise
    finally:
        server.shutdown();server.server_close()
        sources=[p for p in LESSON.iterdir() if p.suffix in ('.html','.css','.js')]
        sources += [ROOT/'templates/html/styles.css',ROOT/'templates/html/reference-layout.css',ROOT/'templates/html/math-typography.css',ROOT/'templates/html/assets/fonts/pretendard/PretendardVariable.woff2',ROOT/'templates/html/assets/fonts/stix-two-math/STIXTwoMath-Regular.woff2']
        sources += list((ROOT/'templates/dual-mode-learning/assets/css').glob('*.css'))
        sources += [Path(__file__).resolve(),ROOT/'scripts/reference_validation.py']
        report['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(sources)}
        report['design_sha256']=hashlib.sha256((LESSON/'DESIGN.md').read_bytes()).hexdigest()
        report['preview_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((LESSON/'previews').glob('*.jpg'))}
        report['review_preview_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((LESSON/'review').glob('*.png'))}
        report['finished_utc']=datetime.now(timezone.utc).isoformat()
        (LESSON/'previews/validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('PASS 8 concept layouts; 161 curve points; real fonts, one-page navigation and legacy URLs')

if __name__=='__main__':
    try:main()
    except Exception:
        detail=traceback.format_exc()[-6000:].replace('%','%25').replace('\r','%0D').replace('\n','%0A')
        print('::error title=Logistic reuse validation::'+detail,flush=True);raise
