"""Check the Markdown-first logistic lesson: math, real fonts, geometry and both modes."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import hashlib, json, math, re, shutil, threading, traceback
from datetime import datetime, timezone

from playwright.sync_api import sync_playwright
from reference_validation import actual_fonts, browser_options

ROOT = Path(__file__).resolve().parents[1]
LESSON = ROOT / 'examples/logistic-regression'
OUT = Path('/tmp/logistic-reuse-review')
SIZES = [(1600, 950), (1440, 810), (1366, 768), (1280, 720)]
PAGES = ['concept', 'calculation', 'threshold']
DEFAULT = dict(weights=[1.2, -.8], bias=.1, samples=[[-1, 1], [-.5, .5], [.25, .5], [1, .5], [1.5, .25], [2, .5]])
ALTERNATE = dict(weights=[.8, -.4], bias=-.2, samples=[[-1, 0], [0, 0], [1, .5], [2, 1]])
CONCEPT_BASELINE = None

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
  noteY:[...slide.querySelectorAll('.lr-card-note')].map(e=>rect(e).y),
  headingGaps:[...slide.querySelectorAll('.lr-heading,.lr-concept-heading')].map(e=>getComputedStyle(e).rowGap),
  rows:[...slide.querySelectorAll('.lr-sample-row')].map(rect),
  sliderGap:slide.querySelector('.lr-slider-row')?rect(slide.querySelector('.lr-slider-row')).y-rect(slide.querySelector('.lr-heading')).bottom:null,
  thresholdLines:[...slide.querySelectorAll('.lr-threshold-line')].map(e=>({relativeX:(e.getBoundingClientRect().x-e.parentElement.getBoundingClientRect().x)/scale,trackWidth:e.parentElement.getBoundingClientRect().width/scale})),
  curves:[...slide.querySelectorAll('.lr-curve')].map(svg=>({variant:svg.dataset.variant||'concept',limit:Number(svg.dataset.limit),x:svg.querySelector('.lr-curve-point')?Number(svg.querySelector('.lr-curve-point').getAttribute('cx')):null,y:svg.querySelector('.lr-curve-point')?Number(svg.querySelector('.lr-curve-point').getAttribute('cy')):null,path:svg.querySelector('.lr-sigmoid-path').getAttribute('d'),axis:Object.fromEntries([...svg.querySelectorAll('[data-axis]')].map(e=>[e.dataset.axis,e.textContent]))})),
  conceptValueCount:slide.querySelectorAll('[data-value]').length,
  calculationInputs:[...slide.querySelectorAll('.lr-input-chip')].map(e=>{const c=getComputedStyle(e);return {box:rect(e),style:[c.backgroundColor,c.color,c.fontSize,c.borderRadius,c.padding],rows:[...e.querySelectorAll(':scope > div')].map(rect)}}),
  equationRows:[...slide.querySelectorAll('.lr-equation-row')].map(e=>{const math=e.querySelectorAll('math'),body=math[math.length-1];return {box:rect(e),body:rect(body),sign:rect(body.querySelector('mo')),overflow:body.getBoundingClientRect().right>e.getBoundingClientRect().right+.5*scale}}),
  transfer:slide.querySelector('.lr-transfer-svg')?{container:rect(slide.querySelector('.lr-calculation')),source:rect(slide.querySelector('.lr-score-output')),target:rect(slide.querySelector('.lr-received-score')),label:rect(slide.querySelector('.lr-transfer-label')),path:slide.querySelector('.lr-transfer-path').getAttribute('d'),sourceValue:slide.querySelector('.lr-score-output [data-value="z"]').textContent,targetValue:slide.querySelector('.lr-received-score [data-value="z"]').textContent}:null,
  fractions:[...slide.querySelectorAll('.lr-sigmoid-formula mfrac')].map(e=>({numerator:rect(e.children[0]),denominator:rect(e.children[1])}))};
}'''

class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *_): pass
    def do_GET(self):
        if self.path == '/favicon.ico':
            self.send_response(204); self.end_headers(); return
        super().do_GET()

def expected(model):
    result = []
    for x in model['samples']:
        z = sum(w*v for w, v in zip(model['weights'], x)) + model['bias']
        p = 1/(1+math.exp(-z))
        result.append((z, p))
    return result

def math_check(page, model):
    global CONCEPT_BASELINE
    data = page.evaluate('''() => ({state:window.LogisticLesson.state,
      concept:{text:document.querySelector('[data-page="concept"]').textContent.replace(/\\s+/g,' ').trim(),path:document.querySelector('[data-page="concept"] .lr-sigmoid-path').getAttribute('d')},
      values:Object.fromEntries([...document.querySelectorAll('[data-page]')].filter(el=>el.dataset.page!=='concept').map(el=>[el.dataset.page,[...el.querySelectorAll('[data-value="percent"]')].map(e=>e.textContent)])),
      displayed:[...document.querySelectorAll('.lr-sample-row')].map(e=>({p:Number(e.dataset.probability),prediction:Number(e.dataset.prediction),label:e.querySelector('.lr-sample-percent').textContent,fill:parseFloat(e.querySelector('.lr-sample-fill').style.width)})),
      counts:document.querySelector('[data-value="positive"]')?[Number(document.querySelector('[data-value="positive"]').textContent),Number(document.querySelector('[data-value="negative"]').textContent)]:null})''')
    if CONCEPT_BASELINE is None:CONCEPT_BASELINE=data['concept']
    assert data['concept']==CONCEPT_BASELINE,'concept page changed with example data'
    rows = expected(model); state = data['state']; t = state['threshold']/100
    assert len(state['rows']) == len(rows)
    if data['counts'] is not None:assert len(data['displayed'])==len(rows)
    for (z, p), actual in zip(rows, state['rows']):
        assert abs(actual['z']-z)<1e-12 and abs(actual['p']-p)<1e-12, actual
    for (z,p),dom in zip(rows,data['displayed']):
        # CSSOM serializes percentage widths to a bounded number of digits.
        assert abs(dom['p']-p)<1e-12 and abs(dom['fill']-100*p)<.0001, dom
        assert dom['prediction'] == int(p >= t), (t, z, p, dom)
        assert dom['label'] == f'{100*p:.1f}%', dom
    positives = sum(p >= t for _, p in rows)
    if data['counts'] is not None:assert data['counts'] == [positives, len(rows)-positives]
    else:assert not data['displayed']
    selected = state['selected']; formatted = f'{100*rows[selected][1]:.1f}%'
    assert all(values and set(values)=={formatted} for values in data['values'].values()), data['values']
    # Read the substituted factors and bias, not just the model's output.
    num=lambda x: f'{0 if abs(x)<1e-10 else x:.2f}'.replace('-', '−')
    x=model['samples'][selected]
    displayed=page.evaluate('''()=>Object.fromEntries(['x1','x2','w1','w2','bias','biasSign','biasMagnitude','z','negativeZ','decimal'].map(key=>[key,[...document.querySelectorAll(`[data-value="${key}"]`)].map(e=>e.textContent)]))''')
    expect=dict(x1=num(x[0]),x2=num(x[1]),w1=num(model['weights'][0]),w2=num(model['weights'][1]),bias=num(model['bias']),biasSign='−' if model['bias']<0 else '+',biasMagnitude=num(abs(model['bias'])),z=num(rows[selected][0]),negativeZ=num(-rows[selected][0]),decimal=f'{rows[selected][1]:.6f}')
    assert all(values and set(values)=={expect[key]} for key,values in displayed.items()),(displayed,expect)
    factors=page.evaluate('''()=>[...document.querySelectorAll('[data-factor]')].map(e=>({key:e.dataset.factor,negative:e.dataset.negative==='true',parentheses:[...e.children].filter(n=>n.tagName==='mo').map(n=>getComputedStyle(n).display!=='none')}))''')
    for factor in factors:
        negative=expect[factor['key']].startswith('−')
        assert factor['negative']==negative and factor['parentheses']==[negative,negative],factor
    assert page.locator('[data-page="concept"] [data-value], [data-page="concept"] .lr-curve-point, [data-page="concept"] .lr-point-guides').count()==0
    curves=page.evaluate('''()=>[...document.querySelectorAll('.lr-curve')].map(e=>({detail:e.dataset.variant==='detail',limit:Number(e.dataset.limit),x:e.querySelector('.lr-curve-point')?Number(e.querySelector('.lr-curve-point').getAttribute('cx')):null,y:e.querySelector('.lr-curve-point')?Number(e.querySelector('.lr-curve-point').getAttribute('cy')):null,axis:[...e.querySelectorAll('[data-axis]')].map(t=>t.textContent)}))''')
    z,p=rows[selected]
    assert len(curves)==2
    for c in curves:
        if not c['detail']:
            assert c['limit']==4 and c['x'] is None and c['y'] is None and not c['axis'];continue
        left,width,bottom,height=56,272,210,180
        assert abs(c['x']-(left+(z+c['limit'])/(2*c['limit'])*width))<1e-10
        assert abs(c['y']-(bottom-p*height))<1e-10
        if c['detail']:assert c['axis']==[num(z),f'{p:.3f}'],c
    return data

def go(page, name):
    page.evaluate('(name)=>{location.hash="ref-"+name}', name)
    page.wait_for_function('(name)=>document.body.dataset.mode==="scroll" || document.getElementById("ref-"+name).getAttribute("aria-hidden")==="false"', arg=name)
    page.locator(f'#ref-{name}').scroll_into_view_if_needed()
    page.evaluate('()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))')

def compare_design(a, b):
    assert len(a) == len(b)
    maximum = 0
    for x, y in zip(a, b):
        assert (x['tag'],x['classes'],x['text'],x['style']) == (y['tag'],y['classes'],y['text'],y['style']), (x,y)
        # Hidden positive-factor parentheses have no rendered box; their zero
        # client origin is unrelated to the containing slide's scroll offset.
        if not any(x['box'][k] or y['box'][k] for k in ('width','height')):continue
        error = max(abs(x['box'][k]-y['box'][k]) for k in x['box'])
        # The SVG text glyph bounds may differ slightly with a scaled text paint.
        assert error < (1 if x['tag'] in ('svg','g','path','circle','text') else .3), (error,x,y)
        maximum=max(maximum,error)
    return maximum

def check_transfer(geometry, expected_z):
    bridge=geometry['transfer'];assert bridge and bridge['path'],bridge
    points=list(map(float,re.findall(r'-?[\d.]+',bridge['path'])))
    c,s,t=bridge['container'],bridge['source'],bridge['target']
    expected_link=[s['right']-c['x']+6,s['y']+s['height']/2-c['y'],(geometry['panels'][0]['right']+geometry['panels'][1]['x'])/2-c['x'],t['y']+t['height']/2-c['y'],t['x']-c['x']-8]
    assert len(points)==11 and max(abs(a-b) for a,b in zip(points[:5],expected_link))<.15,(points,expected_link)
    assert abs(points[7]-points[4])<.001 and abs(points[8]-points[3])<.001
    formatted=f'{0 if abs(expected_z)<1e-10 else expected_z:.2f}'.replace('-','−')
    assert bridge['sourceValue']==bridge['targetValue']==formatted
    assert geometry['panels'][0]['right']<bridge['label']['x'] and bridge['label']['right']<geometry['panels'][1]['x']

def main():
    OUT.mkdir(parents=True,exist_ok=True); (LESSON/'previews').mkdir(exist_ok=True)
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    report={'status':'running','started_utc':datetime.now(timezone.utc).isoformat(),'cases':[]}
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(**browser_options());report['browser']=browser.version
            base=f'http://127.0.0.1:{server.server_port}/examples/logistic-regression'
            errors=[];failed=[];http=[]
            page=browser.new_page(device_scale_factor=1)
            page.on('pageerror',lambda e:errors.append(str(e)))
            page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
            page.on('requestfailed',lambda r:failed.append(r.url))
            page.on('response',lambda r:http.append(f'{r.status} {r.url}') if r.status>=400 else None)
            baseline={}
            for width,height in SIZES:
                page.set_viewport_size({'width':width,'height':height})
                for mode,include_appendix in [(m,a) for m in ['slides','scroll'] for a in [False,True]]:
                    scope='with_appendix' if include_appendix else 'main'
                    page.goto(f'{base}/{mode}.html'+('?appendix=1' if include_appendix else ''),wait_until='networkidle');page.wait_for_function('document.documentElement.dataset.ready==="true"')
                    assert page.locator('[data-page]').count()==(3 if include_appendix else 2)
                    math_check(page,DEFAULT)
                    for name in (PAGES if include_appendix else PAGES[:2]):
                        go(page,name);geometry=page.evaluate(GEOMETRY,name)
                        for key in ['overflow','clippedText','paddingErrors']:assert not geometry[key],(mode,name,width,key,geometry[key])
                        assert geometry['pageWidth']<=width and abs(geometry['frame']['width']/geometry['frame']['height']-16/9)<.00001
                        assert geometry['captionGap']>=13 and geometry['footerGap']>=14,(mode,name,geometry['captionGap'],geometry['footerGap'])
                        assert max(p['bottom'] for p in geometry['panels'])<geometry['caption']['y']
                        bad_typography=[s for s in geometry['styles'] if s['spacing']=='normal' or abs(float(s['spacing'].removesuffix('px'))+4/3)>=.02 or s['lineHeight']=='normal']
                        assert not bad_typography,bad_typography
                        assert all(g=='8px' for g in geometry['headingGaps'])
                        assert all(abs(p['y']-geometry['panels'][0]['y'])<.02 and abs(p['height']-geometry['panels'][0]['height'])<.02 for p in geometry['panels'])
                        if name=='concept':
                            assert max(geometry['labelY'])-min(geometry['labelY'])<.02 and max(geometry['arrowAxisErrors'])<.02
                            assert len(geometry['symbolAxisErrors'])==4 and max(geometry['symbolAxisErrors'])<.02,geometry['symbolAxisErrors']
                            assert len(geometry['inputCenters'])==2 and all(c['error']<.02 and c['paddingX']>=24 and c['paddingY']>=16 for c in geometry['inputCenters']),geometry['inputCenters']
                        for curve in geometry['curves']:
                            left,plot_width,bottom,plot_height=(56,272,210,180) if curve['variant']=='detail' else (40,240,172,150)
                            z,prob=expected(DEFAULT)[3]
                            if curve['variant']=='detail':
                                assert abs(curve['x']-(left+(z+curve['limit'])/(2*curve['limit'])*plot_width))<1e-10
                                assert abs(curve['y']-(bottom-prob*plot_height))<1e-10
                            else:assert curve['x'] is None and curve['y'] is None and geometry['conceptValueCount']==0
                            assert curve['path'].count('L')==160
                            points=[tuple(map(float,pair)) for pair in re.findall(r'[ML]([\d.-]+),([\d.-]+)',curve['path'])]
                            for i in [0,40,80,120,160]:
                                z=-curve['limit']+i*2*curve['limit']/160
                                assert abs(points[i][0]-(left+i/160*plot_width))<.001 and abs(points[i][1]-(bottom-plot_height/(1+math.exp(-z))))<.001
                            if curve['variant']=='detail':assert curve['axis']=={'z':'0.90','p':'0.711'}
                        if name in ('concept','calculation'):
                            assert geometry['fractions'] and all(f['numerator']['bottom']<f['denominator']['y'] for f in geometry['fractions'])
                        if name=='calculation':
                            assert max(geometry['noteY'])-min(geometry['noteY'])<.02
                            chips=geometry['calculationInputs'];assert len(chips)==2 and chips[0]['style']==chips[1]['style']
                            assert len(chips[0]['rows'])==2 and chips[0]['rows'][1]['y']-chips[0]['rows'][0]['bottom']>=7.9
                            equations=geometry['equationRows'];assert len(equations)==3 and not any(e['overflow'] for e in equations)
                            assert max(e['body']['x'] for e in equations)-min(e['body']['x'] for e in equations)<.02
                            assert max(e['sign']['x'] for e in equations)-min(e['sign']['x'] for e in equations)<.02
                            assert all(b['box']['y']-a['box']['bottom']>=13.9 for a,b in zip(equations,equations[1:]))
                            check_transfer(geometry,expected(DEFAULT)[3][0])
                        if name=='threshold':
                            assert abs(geometry['sliderGap']-16)<.02
                            for line in geometry['thresholdLines']:assert abs(line['relativeX']+1-.6*line['trackWidth'])<.03
                        fonts=actual_fonts(page,'.logistic-lesson *',math_family='STIX Two Math');assert fonts['elements']>0 and not any(fonts[k] for k in ['fallback','unpainted','bad_spacing']),fonts
                        assert min(fonts['loaded']['counts'])>0 and fonts['loaded']['math']['count']>0
                        assert fonts['families'].get('STIX Two Math',0)>0 and fonts['families'].get('Pretendard Variable',0)>0
                        fp=geometry.pop('fingerprints')
                        key=(width,name,scope)
                        if mode=='slides':baseline[key]=fp;parity_error=0
                        else:parity_error=compare_design(baseline[key],fp)
                        report['cases'].append(dict(mode=mode,scope=scope,template=name,viewport=[width,height],geometry=geometry,fonts=fonts,max_mode_box_error=parity_error))
                        page.locator(f'[data-page="{name}"]').screenshot(path=str(OUT/f'{mode}-{name}-{width}x{height}{"-appendix" if include_appendix else ""}.png'),animations='disabled')
                        print('PASS',scope,mode,name,width,height,flush=True)
                    if width==1600 and not include_appendix:
                        go(page,'concept');page.screenshot(path=str(LESSON/f'previews/{"slide" if mode=="slides" else mode}.jpg'),type='jpeg',quality=94,animations='disabled')

            page.set_viewport_size({'width':1600,'height':950})
            page.goto(f'{base}/slides.html',wait_until='networkidle');page.wait_for_function('document.documentElement.dataset.ready==="true"')
            page.keyboard.press('End');assert '#ref-calculation' in page.url and page.locator('[data-page]').count()==2
            page.locator('.mode-link').click();page.wait_for_function('document.documentElement.dataset.ready==="true"')
            assert '/scroll.html' in page.url and 'appendix=1' not in page.url and page.locator('[data-page]').count()==2
            math_check(page,DEFAULT)
            page.locator('.appendix-link').click();page.wait_for_function('document.documentElement.dataset.ready==="true"')
            assert 'appendix=1' in page.url and '#ref-threshold' in page.url and page.locator('[data-page]').count()==3
            page.locator('.appendix-link').click();page.wait_for_function('document.documentElement.dataset.ready==="true"')
            assert 'appendix=1' not in page.url and '#ref-calculation' in page.url and page.locator('[data-page]').count()==2
            page.goto(f'{base}/slides.html?appendix=1#ref-threshold',wait_until='networkidle');page.wait_for_function('document.documentElement.dataset.ready==="true"')
            original=page.evaluate(GEOMETRY,'threshold');expected_positions=original['rows']
            checks=0
            for t in range(101):
                page.locator('#threshold').evaluate('(e,t)=>{e.value=t;e.dispatchEvent(new Event("input",{bubbles:true}))}',t)
                math_check(page,DEFAULT);checks+=len(DEFAULT['samples'])
            fixed=page.evaluate(GEOMETRY,'threshold')
            for a,b in zip(expected_positions,fixed['rows']):assert max(abs(a[k]-b[k]) for k in a)<.02
            for selected in range(6):
                page.locator(f'[data-select="{selected}"]').click();math_check(page,DEFAULT)
                go(page,'calculation');check_transfer(page.evaluate(GEOMETRY,'calculation'),expected(DEFAULT)[selected][0]);go(page,'threshold')
            page.locator('#threshold').focus();page.keyboard.press('Home');assert math_check(page,DEFAULT)['counts']==[6,0]
            page.keyboard.press('End');assert math_check(page,DEFAULT)['counts']==[0,6]
            assert page.evaluate('location.hash')=='#ref-threshold'
            page.evaluate('window.LogisticLesson.setThreshold(50)');page.locator('[data-select="2"]').click()
            tie=math_check(page,DEFAULT);assert tie['displayed'][2]['prediction']==1
            page.evaluate('window.LogisticLesson.setThreshold(51)');assert math_check(page,DEFAULT)['displayed'][2]['prediction']==0
            page.evaluate('window.LogisticLesson.setThreshold(72)');page.locator('[data-select="3"]').click()
            assert math_check(page,DEFAULT)['displayed'][3]['prediction']==0
            page.locator('.mode-link').click();page.wait_for_function('document.documentElement.dataset.ready==="true"')
            assert '/scroll.html' in page.url and 'appendix=1' in page.url and 'threshold=72' in page.url and 'sample=4' in page.url and '#ref-threshold' in page.url
            math_check(page,DEFAULT);page.reload(wait_until='networkidle');page.wait_for_function('document.documentElement.dataset.ready==="true"')
            assert window_state(page)==(72,3)
            page.locator('.mode-link').click();page.wait_for_function('document.documentElement.dataset.ready==="true"');assert window_state(page)==(72,3)
            # Test native slider focus separately from slide-level navigation.
            page.locator('#threshold').focus();page.keyboard.press('ArrowRight');assert window_state(page)==(73,3) and page.evaluate('location.hash')=='#ref-threshold'
            page.locator('#threshold').evaluate('(e)=>e.blur()');page.keyboard.press('Home');assert page.evaluate('location.hash')=='#ref-concept'
            page.keyboard.press('End');assert page.evaluate('location.hash')=='#ref-threshold'
            page.evaluate('(m)=>window.LogisticLesson.setModel(m)',ALTERNATE);reuse=0
            for t in range(101):
                page.evaluate('(t)=>window.LogisticLesson.setThreshold(t)',t);math_check(page,ALTERNATE);reuse+=len(ALTERNATE['samples'])
            geometry=page.evaluate(GEOMETRY,'threshold');assert not geometry['paddingErrors'] and not geometry['clippedText']
            selected=page.evaluate('window.LogisticLesson.state.selected');z,prob=expected(ALTERNATE)[selected]
            point=page.locator('.lr-curve-point').first
            assert abs(float(point.get_attribute('cx'))-(56+(z+4)/8*272))<1e-10 and abs(float(point.get_attribute('cy'))-(210-prob*180))<1e-10
            go(page,'calculation');check_transfer(page.evaluate(GEOMETRY,'calculation'),z);go(page,'threshold')
            assert page.evaluate('window.LogisticLesson.sigmoid(-1000)')==0 and page.evaluate('window.LogisticLesson.sigmoid(1000)')==1
            for mutation in ['m.weights=[1]', 'm.samples=[]', 'm.bias=Infinity', 'm.samples[0][0]=NaN', 'm.samples=Array(7).fill([0,0])']:
                rejected=page.evaluate('''mutation=>{const before=JSON.stringify(window.LogisticLesson.state),m=structuredClone(window.LogisticLesson.state.model);try{new Function('m',mutation)(m);window.LogisticLesson.setModel(m);return false}catch{return before===JSON.stringify(window.LogisticLesson.state)}}''',mutation)
                assert rejected,mutation
            page.goto(f'{base}/slides.html?threshold=no&sample=99#unknown',wait_until='networkidle');page.wait_for_function('document.documentElement.dataset.ready==="true"')
            assert window_state(page)==(60,3) and '#ref-concept' in page.url
            assert not errors and not failed and not http,(errors,failed,http)
            report.update(status='passed',main_pages=2,appendix_pages=1,appendix_opt_in=True,concept_is_symbolic=True,concept_is_invariant=True,result_transfer=True,math_checks=checks,alternate_data_checks=reuse,threshold_states=101,keyboard=True,tie_is_positive=True,mode_roundtrip=True,invalid_data_rejections=5,extreme_logits=[-1000,1000],page_errors=errors,failed_requests=failed,http_errors=http)
            (LESSON/'review').mkdir(exist_ok=True)
            for name in PAGES:
                shutil.copyfile(OUT/f'slides-{name}-1600x950{"-appendix" if name=="threshold" else ""}.png',LESSON/f'review/{name}.png')
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
    print(f'PASS {len(report["cases"])} lesson layouts; {checks} default / {reuse} alternate predictions; real fonts and two-mode state')

def window_state(page):
    state=page.evaluate('window.LogisticLesson.state');return state['threshold'],state['selected']

if __name__=='__main__':
    try:main()
    except Exception:
        detail=traceback.format_exc()[-6000:].replace('%','%25').replace('\r','%0D').replace('\n','%0A')
        print('::error title=Logistic reuse validation::'+detail,flush=True);raise
