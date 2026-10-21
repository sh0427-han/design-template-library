"""Verify only #5 across six viewports, all 21 thresholds and accessible controls.
Run: python scripts/check_interactive.py
Requires Playwright, system Chromium and curl. Font cache uses TLS-verified CDN bytes.
"""
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
import hashlib,json,os,shutil,subprocess,threading
import render_previews
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
SIZES=[(1600,950),(1440,810),(1366,768),(1280,720),(900,900),(390,844)]
SAMPLES=[(.15,0),(.32,1),(.48,0),(.67,1),(.82,1),(.94,0)]
CHECK="""() => {
 const slide=document.querySelector('.slide'),box=e=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y,right:r.right,bottom:r.bottom,width:r.width,height:r.height}};
 const table=slide.querySelector('.live-cm');
 const textBounds=e=>{const w=document.createTreeWalker(e,NodeFilter.SHOW_TEXT),rs=[];while(w.nextNode()){if(!w.currentNode.textContent.trim())continue;const r=document.createRange();r.selectNodeContents(w.currentNode);rs.push(r.getBoundingClientRect());}return {left:Math.min(...rs.map(r=>r.left)),right:Math.max(...rs.map(r=>r.right))}};
 const line=box(slide.querySelector('.live-pred-divider'));
 const axisRight=textBounds(table.querySelector('.pred-axis-label')).right;
 const labelsLeft=Math.min(...[...table.querySelectorAll('tbody th[scope="row"]')].map(e=>textBounds(e).left));
 const containers=[...slide.querySelectorAll('.live-card,.live-grid,.live-metric,.live-metric header,.live-metric-calculation,.score-row,.sample-prediction,h1,h2')];
 const overflow=containers.filter(e=>e.scrollWidth>e.clientWidth+2||e.scrollHeight>e.clientHeight+2).map(e=>e.className||e.tagName);
 const text=[...slide.querySelectorAll('*')].filter(e=>!e.closest('.sr-only')&&[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()));
 return {slide:box(slide),cards:[...slide.querySelectorAll('.live-card')].map(box),footer:box(slide.querySelector('footer')),content:box(slide.querySelector('.content')),
  pageWidth:document.documentElement.scrollWidth,overflow,
  captionLast:slide.querySelector('.content').lastElementChild.matches('.ref-takeaway'),
  countsOrder:[...table.querySelectorAll('[data-code]')].map(e=>e.dataset.code),
  labels:[...table.querySelectorAll('th[scope="col"],th[scope="row"]')].map(e=>e.textContent),
  dividerGaps:{left:line.x+line.width/2-axisRight,right:labelsLeft-line.x-line.width/2},
  badTypography:text.filter(e=>{const s=getComputedStyle(e);return Math.abs(parseFloat(s.letterSpacing)+4/3)>.02||!s.fontFamily.startsWith('"Pretendard Variable"')}).map(e=>e.className),
  fontsLoaded:[...document.fonts].filter(f=>f.family.replace(/["']/g,'')==='Pretendard Variable'&&f.status==='loaded').length};
}"""
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*_):pass

def main():
 out=Path('/tmp/interactive-draft-review');out.mkdir(exist_ok=True)
 evidence=ROOT/'previews/review/interactive-validation.json'
 report={'status':'running','math_checks':0,'screens':[],'font_delivery':'TLS-verified curl CDN cache, fulfilled at original URLs; no trust changes'}
 evidence.write_text(json.dumps(report))
 cache=Path('/tmp/experiment-verified-fonts');cache.mkdir(exist_ok=True)
 manifest_path=cache/'manifest.json';manifest=json.loads(manifest_path.read_text()) if manifest_path.exists() else {};assets={}
 def font(route):
  url=route.request.url;assert url.startswith('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/')
  path=cache/hashlib.sha256(url.encode()).hexdigest()
  if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest()!=manifest.get(url):
   subprocess.run(['curl','--fail','--silent','--show-error','--location','--proto','=https','--tlsv1.2','--max-time','45',url,'-o',str(path)],check=True)
   manifest[url]=hashlib.sha256(path.read_bytes()).hexdigest();manifest_path.write_text(json.dumps(manifest))
  assets[url]=manifest[url]
  route.fulfill(body=path.read_bytes(),headers={'content-type':'text/css' if '.css' in url else 'font/woff2','access-control-allow-origin':'*'})
 server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
 threading.Thread(target=server.serve_forever,daemon=True).start()
 try:
  with sync_playwright() as p:
   browser=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_EXECUTABLE') or shutil.which('chromium'),headless=True)
   report['browser']=browser.version
   page=browser.new_page();errors=[];failures=[]
   page.on('pageerror',lambda e:errors.append(str(e)));page.on('requestfailed',lambda r:failures.append(r.url));page.route('https://cdn.jsdelivr.net/**',font)
   for width,height in SIZES:
    page.set_viewport_size({'width':width,'height':height})
    page.goto(f'http://127.0.0.1:{server.server_port}/templates/html/interactive.html',wait_until='networkidle');page.evaluate('document.fonts.ready')
    thresholds=[]
    for threshold in range(0,101,5):
     page.locator('#threshold').fill(str(threshold))
     expected={'tp':0,'tn':0,'fp':0,'fn':0};types=[];predictions=[]
     for score,truth in SAMPLES:
      prediction=score>=threshold/100;key=('tp' if prediction else 'fn') if truth else ('fp' if prediction else 'tn')
      expected[key]+=1;types.append(key.upper());predictions.append('이상' if prediction else '정상')
     assert {k:int(page.locator('#cm-'+k).inner_text()) for k in expected}==expected
     assert page.locator('.outcome').all_text_contents()==types
     assert page.locator('.sample-prediction').all_text_contents()==predictions
     assert page.locator('.sample-truth').all_text_contents()==['이상' if truth else '정상' for _,truth in SAMPLES]
     pct=lambda n,d:f'{100*n/d:.1f}%' if d else '정의 불가'
     tp,fp,fn=expected['tp'],expected['fp'],expected['fn']
     precision,recall=pct(tp,tp+fp),pct(tp,tp+fn)
     assert page.locator('#precision').inner_text()==precision and page.locator('#recall').inner_text()==recall
     assert page.locator('#precision-calculation').inner_text()==f'{tp} / ({tp} + {fp}) = {precision}'
     assert page.locator('#recall-calculation').inner_text()==f'{tp} / ({tp} + {fn}) = {recall}'
     assert page.locator('#threshold-value').inner_text()==f'{threshold/100:.2f}'
     assert page.locator('#threshold').get_attribute('aria-valuetext').startswith(f'{threshold/100:.2f}')
     assert page.locator('#score-summary').inner_text()==f"이상 예측 {tp+fp}개 · 정상 예측 {expected['tn']+fn}개"
     assert page.locator('#evaluation-status').inner_text().startswith(f'임계값 {threshold/100:.2f}. TP {tp}, FP {fp}, FN {fn}, TN {expected["tn"]}.')
     # Undefined precision is wider than the percentages: check every state for clipping.
     assert not page.evaluate(CHECK)['overflow'],(width,threshold,page.evaluate(CHECK)['overflow'])
     thresholds.append({'threshold':threshold/100,**expected,'precision':precision,'recall':recall});report['math_checks']+=1
    slider=page.locator('#threshold');slider.focus()
    for key,value in [('Home','0'),('ArrowRight','5'),('End','100'),('ArrowLeft','95')]:
     slider.press(key);assert slider.input_value()==value
    b=slider.bounding_box();slider.click(position={'x':b['width']/2,'y':b['height']/2});assert slider.input_value()=='50'
    slider.fill('60');page.locator('h1').click()
    r=page.evaluate(CHECK)
    assert r['countsOrder']==['TP','FP','FN','TN'] and r['labels']==['실제 이상','실제 정상','예측 이상','예측 정상']
    assert abs(r['dividerGaps']['left']-r['dividerGaps']['right'])<.25 and min(r['dividerGaps'].values())>2
    assert not r['badTypography'] and r['fontsLoaded']>0
    assert r['captionLast'] and r['pageWidth']<=width
    assert r['content']['bottom']<r['footer']['y']+1
    if width>900:
     assert abs(r['slide']['width']/r['slide']['height']-16/9)<.002
     assert r['slide']['right']<=width+1 and r['slide']['bottom']<=height+1
     assert r['cards'][0]['right']<r['cards'][1]['x']
    else: assert r['cards'][0]['bottom']<r['cards'][1]['y']
    # Keep the repository's existing generic geometry and interaction checks usable.
    shared=page.evaluate(render_previews.GEOMETRY)
    for key in ['outside','overflow','footerOverlap','spacing','clippedText','arrowErrors']:assert not shared[key],(width,key,shared[key])
    page.locator('.slide').screenshot(path=str(out/f'interactive-{width}.png'),animations='disabled')
    if width==1600:
     page.locator('.slide').screenshot(path=str(ROOT/'previews/html-interactive.jpg'),quality=94,animations='disabled')
     # Native range paint can differ by subpixel after pointer/keyboard use.
     page.locator('.slide').screenshot(path=str(out/'interactive-content.png'),mask=[page.locator('#threshold')],animations='disabled')
    report['screens'].append({'viewport':[width,height],**r,'thresholds':thresholds,'shared_geometry':shared})
    print('PASS',width,height,flush=True)
   # Reuse proof: replace only the sample array in a browser response, keeping
   # the checked-in lesson unchanged. Class totals and formulas must follow it.
   original=(ROOT/'templates/html/interactive-reference.js').read_text()
   reused=original.replace('{score:0.15,truth:0}', '{score:0.15,truth:1}').replace('{score:0.94,truth:0}', '{score:0.60,truth:0}')
   assert reused!=original
   page.route('**/interactive-reference.js',lambda route:route.fulfill(body=reused,content_type='application/javascript'))
   reuse_samples=[(.15,1),(.32,1),(.48,0),(.67,1),(.82,1),(.60,0)]
   report['reuse']={'sample_count':6,'actual_anomaly':4,'actual_normal':2,'checks':0,'viewports':[]}
   for width,height in [SIZES[0],SIZES[-1]]:
    page.set_viewport_size({'width':width,'height':height});page.reload(wait_until='networkidle');page.evaluate('document.fonts.ready')
    assert page.locator('#sample-note').inner_text()=='예시 6개 · 양성: 이상'
    assert page.locator('#live-context').inner_text()=='실제 정상 2개 · 실제 이상 4개'
    for threshold in range(0,101,5):
     page.locator('#threshold').fill(str(threshold));expected={'tp':0,'fp':0,'fn':0,'tn':0};labels=[];predictions=[]
     for score,truth in reuse_samples:
      prediction=score>=threshold/100;key=('tp' if prediction else 'fn') if truth else ('fp' if prediction else 'tn')
      expected[key]+=1;labels.append(key.upper());predictions.append('이상' if prediction else '정상')
     assert {k:int(page.locator('#cm-'+k).inner_text()) for k in expected}==expected
     assert page.locator('.outcome').all_text_contents()==labels
     assert page.locator('.sample-prediction').all_text_contents()==predictions
     for metric,extra in [('precision','fp'),('recall','fn')]:
      value=pct(expected['tp'],expected['tp']+expected[extra])
      assert page.locator('#'+metric).inner_text()==value
      assert page.locator('#'+metric+'-calculation').inner_text()==f"{expected['tp']} / ({expected['tp']} + {expected[extra]}) = {value}"
     assert not page.evaluate(CHECK)['overflow']
     report['reuse']['checks']+=1
    page.locator('#threshold').fill('60');report['reuse']['viewports'].append({'viewport':[width,height],**page.evaluate(CHECK)})
    page.locator('.slide').screenshot(path=str(out/f'interactive-reuse-{width}.png'),animations='disabled')
   # Shareable HTML: inline local dependencies; only the original web font
   # remains remote, with the normal system-font fallback when offline.
   portable=(ROOT/'templates/html/interactive.html').read_text()
   for name in ['styles.css','reference-types.css','reference-layout.css']:
    portable=portable.replace(f'<link rel="stylesheet" href="{name}">', '<style>\n'+(ROOT/'templates/html'/name).read_text()+'\n</style>')
   portable=portable.replace('<script src="interactive-reference.js" defer></script>','')
   portable=portable.replace('</body>','<script>\n'+original+'\n</script></body>')
   portable='<!-- Generated by scripts/check_interactive.py; edit templates/html sources. -->\n'+portable
   (ROOT/'previews/review/interactive-live.html').write_text(portable)
   page.set_viewport_size({'width':1600,'height':950})
   page.goto(f'http://127.0.0.1:{server.server_port}/previews/review/interactive-live.html',wait_until='networkidle');page.evaluate('document.fonts.ready');page.locator('h1').click()
   assert page.locator('#precision-calculation').inner_text()=='2 / (2 + 1) = 66.7%'
   assert page.locator('#live-context').inner_text()=='실제 정상 3개 · 실제 이상 3개'
   page.locator('.slide').screenshot(path=str(out/'interactive-portable.png'),animations='disabled')
   portable_pixels=page.locator('.slide').screenshot(mask=[page.locator('#threshold')],animations='disabled')
   assert portable_pixels==(out/'interactive-content.png').read_bytes()
   page.locator('#threshold').fill('100');assert page.locator('#precision').inner_text()=='정의 불가'
   report['portable_html']={'path':'previews/review/interactive-live.html','content_pixels_match':True,'native_range_excluded_from_pixel_comparison':True,'interaction_checked':True}
   assert not errors and not failures,(errors,failures)
   report.update(status='passed',page_errors=errors,request_failures=failures,font_assets=assets);browser.close()
 except Exception as exc:
  report.update(status='failed',error=str(exc));raise
 finally:
  server.shutdown();server.server_close();evidence.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':main()
