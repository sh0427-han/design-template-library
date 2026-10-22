"""Verify only #5 across six viewports, all 21 thresholds and accessible controls.
Run: python scripts/check_interactive.py
Requires Playwright and system Chromium. Uses the bundled official Pretendard font.
"""
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
import base64,hashlib,json,os,re,threading,traceback
import render_previews
from reference_validation import actual_fonts, browser_options
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
 const containers=[...slide.querySelectorAll('.live-card,.live-grid,.live-metric,.live-metric header,.live-metric-calculation,.sample-group,.sample-groups,.group-label,.score-summary,.threshold-panel,.threshold-control,.score-row,.sample-prediction,h1,h2')];
 const overflow=containers.filter(e=>e.scrollWidth>e.clientWidth+2||e.scrollHeight>e.clientHeight+2).map(e=>e.className||e.tagName);
 const cardContentEscapes=[];
 for(const card of slide.querySelectorAll('.live-card')) {
  const r=box(card),s=getComputedStyle(card),scale=r.width/parseFloat(s.width);
  const left=r.x+(parseFloat(s.paddingLeft)+parseFloat(s.borderLeftWidth))*scale,right=r.right-(parseFloat(s.paddingRight)+parseFloat(s.borderRightWidth))*scale;
  const top=r.y+(parseFloat(s.paddingTop)+parseFloat(s.borderTopWidth))*scale,bottom=r.bottom-(parseFloat(s.paddingBottom)+parseFloat(s.borderBottomWidth))*scale;
  for(const child of card.children) {const b=box(child);if(b.x<left-1||b.right>right+1||b.y<top-1||b.bottom>bottom+1)cardContentEscapes.push(child.className||child.tagName);}
 }
 const summary=box(slide.querySelector('#score-summary')),control=box(slide.querySelector('.live-card'));
 const text=[...slide.querySelectorAll('*')].filter(e=>!e.closest('.sr-only')&&[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()));
 return {slide:box(slide),cards:[...slide.querySelectorAll('.live-card')].map(box),footer:box(slide.querySelector('footer')),content:box(slide.querySelector('.content')),
  pageWidth:document.documentElement.scrollWidth,overflow,cardContentEscapes,summaryBottomGap:control.bottom-summary.bottom,
  groups:[...slide.querySelectorAll('.sample-group')].map(g=>({truth:Number(g.dataset.truth),count:g.querySelector('.group-label span').textContent,samples:[...g.querySelectorAll('.score-row')].map(r=>Number(r.dataset.sample))})),
  captionLast:slide.querySelector('.content').lastElementChild.matches('.ref-takeaway'),
  countsOrder:[...table.querySelectorAll('[data-code]')].map(e=>e.dataset.code),
  labels:[...table.querySelectorAll('th[scope="col"],th[scope="row"]')].map(e=>e.textContent),
  dividerGaps:{left:line.x+line.width/2-axisRight,right:labelsLeft-line.x-line.width/2},
  badTypography:text.filter(e=>{const s=getComputedStyle(e);return Math.abs(parseFloat(s.letterSpacing)+4/3)>.02||!s.fontFamily.startsWith('"Pretendard Variable"')}).map(e=>e.className),
  fontsLoaded:[...document.fonts].filter(f=>f.family.replace(/["']/g,'')==='Pretendard Variable'&&f.status==='loaded').length};
}"""
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*_):pass

def sample_text(page,selector):
 return page.locator('.score-row').evaluate_all('(rows,selector)=>rows.sort((a,b)=>Number(a.dataset.sample)-Number(b.dataset.sample)).map(row=>row.querySelector(selector).textContent)',selector)

def rendered_fonts(page):
 r=actual_fonts(page)
 assert not r['fallback'] and not r['unpainted'] and not r['bad_spacing'],r
 return {'text_elements':r['elements'],'rendered_families':r['families'],'fallback_elements':0}


def main():
 out=Path('/tmp/interactive-draft-review');out.mkdir(exist_ok=True)
 evidence=ROOT/'previews/review/interactive-validation.json'
 font_path=ROOT/'templates/html/assets/fonts/pretendard/PretendardVariable.woff2'
 font_bytes=font_path.read_bytes();font_hash=hashlib.sha256(font_bytes).hexdigest()
 assert font_hash=='9599f12fd42fc0bce1cd50b47a0c022e108d7aa64dd0d1bb0ed44f3282d900b4'
 report={'status':'running','math_checks':0,'screens':[],'font_delivery':'Original Pretendard Variable v1.3.9 from common local CSS; no CDN required','font_asset':{'path':str(font_path.relative_to(ROOT)),'sha256':font_hash,'bytes':len(font_bytes)}}
 evidence.write_text(json.dumps(report))
 server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
 threading.Thread(target=server.serve_forever,daemon=True).start()
 try:
  with sync_playwright() as p:
   browser=p.chromium.launch(**browser_options())
   report['browser']=browser.version
   page=browser.new_page();errors=[];failures=[]
   page.on('pageerror',lambda e:errors.append(str(e)));page.on('requestfailed',lambda r:failures.append(r.url))
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
     assert sample_text(page,'.outcome')==types
     assert sample_text(page,'.sample-prediction')==predictions
     assert sample_text(page,'.sample-truth')==['이상' if truth else '정상' for _,truth in SAMPLES]
     assert page.locator('.score-row').evaluate_all('(rows)=>rows.every(r=>r.dataset.prediction===(r.querySelector(".sample-prediction").textContent==="이상"?"1":"0")&&r.dataset.type===r.querySelector(".outcome").textContent)')
     pct=lambda n,d:f'{100*n/d:.1f}%' if d else '정의 불가'
     tp,fp,fn=expected['tp'],expected['fp'],expected['fn']
     precision,recall=pct(tp,tp+fp),pct(tp,tp+fn)
     assert page.locator('#precision').inner_text()==precision and page.locator('#recall').inner_text()==recall
     assert page.locator('#precision-calculation').inner_text()==f'{tp} / ({tp} + {fp}) = {precision}'
     assert page.locator('#recall-calculation').inner_text()==f'{tp} / ({tp} + {fn}) = {recall}'
     assert page.locator('#threshold-value').inner_text()==f'{threshold/100:.2f}'
     markers=page.locator('.score-track').evaluate_all('(tracks)=>tracks.map(t=>parseFloat(t.style.getPropertyValue("--threshold-pct")))')
     assert len(markers)==6 and all(abs(marker-threshold)<1e-8 for marker in markers)
     assert page.locator('#threshold').get_attribute('aria-valuetext').startswith(f'{threshold/100:.2f}')
     assert page.locator('#score-summary').inner_text()==f"이상 예측 {tp+fp}개 · 정상 예측 {expected['tn']+fn}개"
     assert page.locator('#evaluation-status').inner_text().startswith(f'임계값 {threshold/100:.2f}. TP {tp}, FP {fp}, FN {fn}, TN {expected["tn"]}.')
     # Undefined precision is wider than the percentages: check every state for clipping.
     geometry=page.evaluate(CHECK)
     assert not geometry['overflow'] and not geometry['cardContentEscapes'],(width,threshold,geometry)
     thresholds.append({'threshold':threshold/100,**expected,'precision':precision,'recall':recall});report['math_checks']+=1
    undefined_fonts=rendered_fonts(page)
    slider=page.locator('#threshold')
    slider.fill('60');page.evaluate('window.savedSample=document.querySelector("[data-sample=\\"4\\"]")')
    slider.fill('70')
    assert page.locator('.score-row[data-changed="true"]').evaluate_all('(rows)=>rows.map(r=>Number(r.dataset.sample))')==[4]
    assert page.evaluate('window.savedSample===document.querySelector("[data-sample=\\"4\\"]")')
    assert page.locator('[data-sample="4"] .sample-prediction').inner_text()=='정상'
    if width==1600:
     page.locator('.slide').screenshot(path=str(out/'interactive-threshold-070.png'),animations='disabled')
    slider.focus()
    for key,value in [('Home','0'),('ArrowRight','5'),('End','100'),('ArrowLeft','95')]:
     slider.press(key);assert slider.input_value()==value
    b=slider.bounding_box();slider.click(position={'x':b['width']/2,'y':b['height']/2});assert slider.input_value()=='50'
    slider.fill('60');page.locator('h1').click()
    r=page.evaluate(CHECK)
    assert r['countsOrder']==['TP','FP','FN','TN'] and r['labels']==['실제 이상','실제 정상','예측 이상','예측 정상']
    assert abs(r['dividerGaps']['left']-r['dividerGaps']['right'])<.25 and min(r['dividerGaps'].values())>2
    assert not r['badTypography'] and r['fontsLoaded']>0
    assert r['captionLast'] and r['pageWidth']<=width
    assert r['groups']==[{'truth':1,'count':'3개','samples':[2,4,5]},{'truth':0,'count':'3개','samples':[1,3,6]}]
    rule=page.locator('.decision-rule').bounding_box();legend=page.locator('.threshold-legend').bounding_box()
    assert page.locator('.decision-rule').inner_text()=='점수 ≥ 임계값 → 이상'
    if width>520: assert rule['x']+rule['width']+12<legend['x']
    else: assert rule['y']+rule['height']+2<legend['y']
    assert not r['cardContentEscapes']
    assert page.locator('.ref-takeaway strong').inner_text()=='임계값 = 이상으로 판정하는 최소 점수'
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
     # Canonical previews belong to validate_references.py. This scenario has
     # exercised the native slider, so keep its screenshots as test evidence.
     # Native range paint can differ by subpixel after pointer/keyboard use.
     page.locator('.slide').screenshot(path=str(out/'interactive-content.png'),mask=[page.locator('#threshold')],animations='disabled')
    report['screens'].append({'viewport':[width,height],**r,'thresholds':thresholds,'shared_geometry':shared,'rendered_fonts':{'default':rendered_fonts(page),'undefined_precision':undefined_fonts}})
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
     assert sample_text(page,'.outcome')==labels
     assert sample_text(page,'.sample-prediction')==predictions
     for metric,extra in [('precision','fp'),('recall','fn')]:
      value=pct(expected['tp'],expected['tp']+expected[extra])
      assert page.locator('#'+metric).inner_text()==value
      assert page.locator('#'+metric+'-calculation').inner_text()==f"{expected['tp']} / ({expected['tp']} + {expected[extra]}) = {value}"
     geometry=page.evaluate(CHECK)
     assert not geometry['overflow'] and not geometry['cardContentEscapes'],(width,threshold,geometry)
     assert geometry['groups']==[{'truth':1,'count':'4개','samples':[1,2,4,5]},{'truth':0,'count':'2개','samples':[3,6]}]
     report['reuse']['checks']+=1
    page.locator('#threshold').fill('60');report['reuse']['viewports'].append({'viewport':[width,height],**page.evaluate(CHECK)})
    page.locator('.slide').screenshot(path=str(out/f'interactive-reuse-{width}.png'),animations='disabled')
   # Check the reported card-boundary regression when the bundled font is missing.
   fallback=browser.new_page()
   fallback.on('pageerror',lambda e:errors.append(str(e)))
   fallback.route('**/assets/fonts/pretendard/PretendardVariable.woff2',lambda route:route.fulfill(status=404,body=''))
   report['font_fallback']=[]
   for width,height in SIZES:
    fallback.set_viewport_size({'width':width,'height':height})
    fallback.goto(f'http://127.0.0.1:{server.server_port}/templates/html/interactive.html',wait_until='networkidle');fallback.evaluate('document.fonts.ready')
    for threshold in ['60','100']:
     fallback.locator('#threshold').fill(threshold);geometry=fallback.evaluate(CHECK)
     assert geometry['fontsLoaded']==0
     assert not geometry['overflow'] and not geometry['cardContentEscapes'],('font fallback',width,threshold,geometry)
     assert geometry['pageWidth']<=width and geometry['content']['bottom']<geometry['footer']['y']+1
     report['font_fallback'].append({'viewport':[width,height],'threshold':int(threshold)/100,**geometry})
    if width==1600:fallback.locator('.slide').screenshot(path=str(out/'interactive-font-fallback.png'),animations='disabled')
   fallback.close()
   page.emulate_media(reduced_motion='reduce');page.locator('#threshold').fill('60');page.locator('#threshold').fill('70')
   assert page.locator('.sample-prediction').evaluate_all('(badges)=>badges.every(b=>b.getAnimations().length===0)')
   report['prediction_transition']={'from':.60,'to':.70,'changed_default_sample':4,'dom_identity_retained':True,'reduced_motion_checked':True}
   page.emulate_media(reduced_motion='no-preference')
   # Compare two fresh default renders so previous live animations do not leave
   # different compositor layers around rounded edges in the reference capture.
   page.unroute('**/interactive-reference.js')
   page.set_viewport_size({'width':1600,'height':950})
   page.goto(f'http://127.0.0.1:{server.server_port}/templates/html/interactive.html',wait_until='networkidle');page.evaluate('document.fonts.ready');page.locator('h1').click()
   page.locator('.slide').screenshot(path=str(out/'interactive-content.png'),mask=[page.locator('#threshold')],animations='disabled')
   # Shareable HTML includes all CSS, JS, font bytes and the original license.
   portable=(ROOT/'templates/html/interactive.html').read_text()
   for name in ['styles.css','reference-types.css','reference-layout.css']:
    css=(ROOT/'templates/html'/name).read_text()
    if name=='styles.css':css=re.sub(r'@import\s+url\([^;]+\);','',css)
    portable=portable.replace(f'<link rel="stylesheet" href="{name}">', '<style>\n'+css+'\n</style>')
   portable=portable.replace('assets/fonts/pretendard/PretendardVariable.woff2','data:font/woff2;base64,'+base64.b64encode(font_bytes).decode())
   portable=portable.replace('<script src="interactive-reference.js" defer></script>','')
   portable=portable.replace('</body>','<script>\n'+original+'\n</script></body>')
   license_text=(font_path.parent/'LICENSE').read_text()
   portable='<!-- Generated by scripts/check_interactive.py; edit templates/html sources. -->\n<!-- Bundled Pretendard Variable v1.3.9\n'+license_text+'\n-->\n'+portable
   (ROOT/'previews/review/interactive-live.html').write_text(portable)
   page.set_viewport_size({'width':1600,'height':950})
   page.goto(f'http://127.0.0.1:{server.server_port}/previews/review/interactive-live.html',wait_until='networkidle');page.evaluate('document.fonts.ready');page.locator('h1').click()
   assert page.locator('#precision-calculation').inner_text()=='2 / (2 + 1) = 66.7%'
   assert page.locator('#live-context').inner_text()=='실제 정상 3개 · 실제 이상 3개'
   page.locator('.slide').screenshot(path=str(out/'interactive-portable.png'),animations='disabled')
   portable_pixels=page.locator('.slide').screenshot(mask=[page.locator('#threshold')],animations='disabled')
   comparison=page.evaluate('''async ({expected,actual}) => {
    const load=src=>new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>resolve(im);im.onerror=reject;im.src='data:image/png;base64,'+src});
    const a=await load(expected),b=await load(actual);
    if(a.width!==b.width||a.height!==b.height)throw new Error('Preview dimensions differ');
    const canvas=document.createElement('canvas');canvas.width=a.width;canvas.height=a.height;const ctx=canvas.getContext('2d',{willReadFrequently:true});
    ctx.drawImage(a,0,0);const x=ctx.getImageData(0,0,a.width,a.height).data;ctx.clearRect(0,0,a.width,a.height);ctx.drawImage(b,0,0);const y=ctx.getImageData(0,0,a.width,a.height).data;
    let maxChannelDelta=0,differentPixels=0;
    for(let i=0;i<x.length;i+=4){let delta=0;for(let c=0;c<4;c++)delta=Math.max(delta,Math.abs(x[i+c]-y[i+c]));maxChannelDelta=Math.max(maxChannelDelta,delta);if(delta)differentPixels++;}
    return {maxChannelDelta,differentPixels,totalPixels:a.width*a.height};
   }''',{'expected':base64.b64encode((out/'interactive-content.png').read_bytes()).decode(),'actual':base64.b64encode(portable_pixels).decode()})
   # Rounded-edge rasterization can vary by 1–2 levels after live updates.
   assert comparison['maxChannelDelta']<=2 and comparison['differentPixels']<=comparison['totalPixels']*.001,comparison
   page.locator('#threshold').fill('100');assert page.locator('#precision').inner_text()=='정의 불가'
   report['portable_html']={'path':'previews/review/interactive-live.html','content_within_tolerance':True,'pixel_comparison':comparison,'max_channel_tolerance':2,'max_changed_fraction':.001,'native_range_excluded_from_pixel_comparison':True,'interaction_checked':True}
   # Load the generated bytes in a fresh offline context. Managed Chromium
   # disallows file:// navigation; set_content verifies the offline document
   # without changing that policy or claiming to have tested the file origin.
   offline=browser.new_context(offline=True,viewport={'width':1600,'height':950})
   offline_page=offline.new_page();offline_page.on('pageerror',lambda e:errors.append(str(e)))
   offline_page.on('requestfailed',lambda r:failures.append(r.url))
   offline_page.set_content((ROOT/'previews/review/interactive-live.html').read_text(),wait_until='load');offline_page.evaluate('document.fonts.ready')
   report['offline_portable']={'method':'Generated HTML bytes loaded by set_content; file:// navigation blocked by managed browser policy','default':rendered_fonts(offline_page)}
   offline_page.locator('#threshold').fill('100');assert offline_page.locator('#precision').inner_text()=='정의 불가'
   report['offline_portable']['undefined_precision']=rendered_fonts(offline_page)
   offline.close()
   assert not errors and not failures,(errors,failures)
   report.update(status='passed',page_errors=errors,request_failures=failures);browser.close()
 except Exception as exc:
  report.update(status='failed',error=traceback.format_exc())
  if os.environ.get('GITHUB_ACTIONS')=='true':
   # Keep actionable failure evidence in the Checks API, even when the runner's
   # external log/artifact download endpoint is unavailable to the client.
   diagnostic=report['error'].replace('%','%25').replace('\r','%0D').replace('\n','%0A')
   print('::error title=Interactive verification failed::'+diagnostic,flush=True)
  raise
 finally:
  server.shutdown();server.server_close();evidence.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':main()
