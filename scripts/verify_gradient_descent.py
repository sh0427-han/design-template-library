"""Independent scalar mathematics, real Chromium fonts, layout and PC4 x two modes.
Run from any directory: python scripts/verify_gradient_descent.py
Does not import or read any logistic-regression implementation or verifier.
"""
from datetime import datetime, timezone
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import hashlib
import json
import math
import subprocess
import threading
from playwright.sync_api import sync_playwright
from reference_validation import browser_options

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / 'examples/gradient-descent'
EVIDENCE = Path('/tmp/gradient-descent-review')
SIZES = ((1600, 950), (1440, 810), (1366, 768), (1280, 720))
BASE = '878b9f0fe75723bb74f0a2180fdf6dfb7effd437'

class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass
    def do_GET(self):
        if self.path == '/favicon.ico':
            self.send_response(204)
            self.end_headers()
        else:
            super().do_GET()

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def find_document(node, url):
    if node.get('documentURL') == url:
        return node
    for child in node.get('children', []) + ([node['contentDocument']] if 'contentDocument' in node else []):
        result = find_document(child, url)
        if result:
            return result

def fonts(page, frame, selector):
    """Use common CDP audit method, resolving iframe document and math roles."""
    entries = frame.evaluate('''selector => [...document.querySelectorAll(selector)].filter(e=>
      getComputedStyle(e).display!=='none' && e.getBoundingClientRect().width && e.getBoundingClientRect().height &&
      [...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()) && !e.closest('.gd-failure,.frame-status')
    ).map((e,i)=>{e.dataset.gdFont=String(i);return {id:i,text:[...e.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent).join(''),
      spacing:getComputedStyle(e).letterSpacing,weight:getComputedStyle(e).fontWeight,expected:e.closest('math.math,.math-number')?'STIX Two Math':'Pretendard Variable'}})''', selector)
    cdp = page.context.new_cdp_session(page)
    cdp.send('DOM.enable'); cdp.send('CSS.enable')
    try:
        doc = find_document(cdp.send('DOM.getDocument', {'depth': -1, 'pierce': True})['root'], frame.url)
        assert doc
        counts = {}
        for e in entries:
            assert abs(float(e['spacing'].removesuffix('px')) + 4/3) < .02, e
            if e['expected']=='STIX Two Math':assert e['weight']=='400',('math must use regular 400',e)
            node = cdp.send('DOM.querySelector', {'nodeId': doc['nodeId'], 'selector': f'[data-gd-font="{e["id"]}"]'})['nodeId']
            actual = cdp.send('CSS.getPlatformFontsForNode', {'nodeId': node})['fonts']
            assert actual, ('unpainted', e)
            for f in actual:
                assert f['familyName'] == e['expected'] and f['isCustomFont'], (e, f)
                counts[f['familyName']] = counts.get(f['familyName'], 0) + f['glyphCount']
        loads = frame.evaluate('''async()=>{const body=await Promise.all([400,700,800].map(w=>document.fonts.load(`${w} 20px "Pretendard Variable"`,'한글 ABC 0123')));
          const math=await document.fonts.load('400 24px "STIX Two Math"','𝜃𝑡𝐿η′−0123');await document.fonts.ready;
          return {body:body.map(x=>x.length),math:math.length,faces:[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family)}}''')
        assert all(loads['body']) and (loads['math'] or selector == 'body *'), loads
        return dict(text_nodes=len(entries), glyphs=counts, loaded=loads, tracking='-1pt', fallback=0)
    finally:
        cdp.detach()
        frame.evaluate("document.querySelectorAll('[data-gd-font]').forEach(e=>e.removeAttribute('data-gd-font'))")

SNAPSHOT = '''()=>[...document.querySelectorAll('.gd-slide,.gd-slide *')].filter(e=>e.getBoundingClientRect().width&&e.getBoundingClientRect().height&&getComputedStyle(e).display!=='none').map(e=>{
 const r=e.getBoundingClientRect(),origin=document.querySelector('.gd-slide').getBoundingClientRect(),s=getComputedStyle(e);return {tag:e.tagName,cls:e.getAttribute('class'),box:[r.x-origin.x,r.y-origin.y,r.width,r.height],
 style:['fontFamily','fontSize','fontWeight','lineHeight','letterSpacing','color','backgroundColor','padding','borderRadius'].map(k=>s[k])}})'''

GEOMETRY = '''()=>{
 const box=e=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y,right:r.right,bottom:r.bottom,w:r.width,h:r.height}};
 const q=s=>document.querySelector(s), slide=q('.gd-slide'),panel=q('.gd-panel'),footer=q('.footer');
 const overflow=[],outside=[],clipped=[],overlaps=[];
 for(const e of slide.querySelectorAll('*')){
   if(!e.getBoundingClientRect().width||getComputedStyle(e).display==='none'||e.closest('math'))continue;
   const r=box(e),p=box(panel),s=box(slide);
   if(r.x<s.x-1||r.right>s.right+1||r.y<s.y-1||r.bottom>s.bottom+1)outside.push(e.id||e.className||e.tagName);
   if(e instanceof HTMLElement&&e.scrollWidth>e.clientWidth+1)overflow.push(e.className);
   if(e instanceof HTMLElement&&!e.closest('.gd-failure')){
     for(const n of e.childNodes){if(n.nodeType!==3||!n.textContent.trim())continue;
       const range=document.createRange();range.selectNodeContents(n);
       for(const t of range.getClientRects())if(t.left<r.x-1||t.right>r.right+1)clipped.push(e.className||e.tagName);
     }
   }
 }
 if(box(q('.gd-steps ol')).bottom>box(q('.gd-definitions')).y-8)overlaps.push('steps vs definitions');
 if(box(q('#loss-plot')).bottom>box(panel).bottom-parseFloat(getComputedStyle(panel).paddingBottom)-1)overlaps.push('plot vs panel padding');
 if(box(q('.gd-takeaway')).bottom>box(footer).y-10)overlaps.push('takeaway/footer');
 const plot=q('#loss-plot'),vb=plot.viewBox.baseVal,ink=[];
 for(const e of plot.querySelectorAll('text')){
   const b=e.getBBox();ink.push({id:e.id,x:b.x,y:b.y,right:b.x+b.width,bottom:b.y+b.height});
   if(b.x<0||b.y<0||b.x+b.width>vb.width||b.y+b.height>vb.height)clipped.push(e.id);
 }
 const collisions=[];for(let i=0;i<ink.length;i++)for(let j=i+1;j<ink.length;j++){
   const a=ink[i],b=ink[j];if(Math.min(a.right,b.right)-Math.max(a.x,b.x)>1&&Math.min(a.bottom,b.bottom)-Math.max(a.y,b.y)>1)collisions.push([a.id,b.id]);
 }
 const math=[...slide.querySelectorAll('math')].map(e=>({text:e.textContent,display:getComputedStyle(e).fontFamily,box:box(e)}));
 for(const e of slide.querySelectorAll('math')){const r=box(e),p=box(e.parentElement);if(r.x<p.x-1||r.right>p.right+1||r.y<box(panel).y||r.bottom>box(panel).bottom)clipped.push('math '+e.textContent);} 
 return {outside,overflow,clipped,overlaps,collisions,ink,math,slide:box(slide),panel:box(panel),main:box(q('.gd-main')),steps:box(q('.gd-steps')),definitions:box(q('.gd-definitions')),takeaway:box(q('.gd-takeaway')),footer:box(footer)};
}'''

def technical(frame):
    data = frame.evaluate('window.gradientDescentEvidence')
    assert data
    # Independent specification: do not take equation, rate or expected answer from rendered labels.
    expected = [2.8 * .72**i for i in range(6)]
    px = lambda theta: 48 + (theta + 3.4) / 6.8 * 242
    py = lambda loss: 454 - loss / 6.5 * 434
    for state, theta in zip(data['states'], expected):
        loss = theta**2/2
        derivative = (((theta+1e-5)**2/2)-((theta-1e-5)**2/2))/(2e-5)
        assert math.isclose(state['theta'], theta, abs_tol=1e-12)
        assert math.isclose(state['gradient'], derivative, abs_tol=1e-9)
        assert math.isclose(state['loss'], loss, abs_tol=1e-12)
        assert abs(state['x']-px(theta)) < 1e-9 and abs(state['y']-py(loss)) < 1e-9
    assert len(data['states']) == 6 and len(data['points']) == 161
    assert frame.locator('#loss-plot').evaluate('e=>e.getBoundingClientRect().width')==345
    assert frame.locator('#loss-plot').evaluate('e=>e.getBoundingClientRect().height')==482
    assert frame.locator('#plot-context').count()==0
    for i, point in enumerate(data['points']):
        theta = -3.4 + 6.8*i/160
        assert abs(point['theta']-theta) < 1e-12
        assert abs(point['x']-px(theta)) < 1e-9 and abs(point['y']-py(theta**2/2)) < 1e-9
    assert all(a['loss'] > b['loss'] for a,b in zip(data['states'], data['states'][1:]))
    for t, delta in zip(data['tangent'], (-.55,.40)):
        assert abs(t['x']-px(2.8+delta)) < 1e-9
        assert abs(t['y']-py(2.8**2/2+2.8*delta)) < 1e-9
    # Check the actual painted path/points, not just a data API carrying correct answers.
    rendered = frame.evaluate('''()=>({states:[...document.querySelectorAll('#plot-art circle')].map(e=>({x:+e.getAttribute('cx'),y:+e.getAttribute('cy')})),
      path:document.querySelector('#loss-curve').getAttribute('d'),tangent:document.querySelector('#tangent').getAttribute('d'),arrow:document.querySelector('#update-arrow').getAttribute('d'),
      formula:document.querySelector('.gd-update math').textContent,
      labels:[...document.querySelectorAll('#plot-art text')].map(e=>e.textContent)})''')
    import re
    coords = [float(s) for s in re.findall(r'-?\d+(?:\.\d+)?(?:e[+-]?\d+)?', rendered['path'])]
    assert len(coords) == 322
    for i in range(161):
        theta = -3.4+6.8*i/160
        assert abs(coords[2*i]-px(theta)) < 1e-9 and abs(coords[2*i+1]-py(theta**2/2)) < 1e-9
    for p, theta in zip(rendered['states'], expected):
        assert abs(p['x']-px(theta)) < 1e-9 and abs(p['y']-py(theta**2/2)) < 1e-9
    tangent_nums = [float(s) for s in re.findall(r'-?\d+(?:\.\d+)?',rendered['tangent'])]
    for i,delta in enumerate((-.55,.40)):
        assert abs(tangent_nums[2*i]-px(2.8+delta)) < 1e-9
        assert abs(tangent_nums[2*i+1]-py(2.8**2/2+2.8*delta)) < 1e-9
    arrow_nums = [float(s) for s in re.findall(r'-?\d+(?:\.\d+)?',rendered['arrow'])]
    assert abs(arrow_nums[0]-(px(2.8)-3.5))<1e-9 and abs(arrow_nums[2]-(px(expected[1])+3.5))<1e-9
    assert arrow_nums[0]>arrow_nums[2] and arrow_nums[1]==arrow_nums[3]==394
    assert len(arrow_nums)==10 and arrow_nums[6:8]==arrow_nums[2:4], 'arrow head and body do not share tip'
    assert rendered['formula']=='θt+1=θt−ηL′(θt)'
    assert not any(re.search(r'\d[.,]\d', label) for label in rendered['labels'])
    # Boundary/counterexample: loss does not necessarily decrease for an arbitrary positive rate.
    signs=[]
    for theta in (-2.8,0.,2.8):
        for rate in (.05,.28,1.,2.,2.1):
            next_theta=theta-rate*theta
            if theta: assert (next_theta-theta)*theta < 0
            if theta and rate>2: assert next_theta**2/2>theta**2/2
            if rate==2: assert math.isclose(next_theta**2/2,theta**2/2,abs_tol=1e-12)
            signs.append(dict(theta=theta,rate=rate,next=next_theta))
    return {'curve_points':161,'states':6,'finite_difference':True,'painted_geometry':True,'symbolic_formula':True,'counterexamples':len(signs)}

def compare(a,b):
    assert len(a)==len(b),(len(a),len(b))
    maximum=0
    for left,right in zip(a,b):
        assert (left['tag'],left['cls'],left['style'])==(right['tag'],right['cls'],right['style'])
        error=max(abs(x-y) for x,y in zip(left['box'],right['box']))
        assert error<.3,(left,right,error)
        maximum=max(maximum,error)
    return {'elements':len(a),'styles_equal':True,'max_box_error_px':maximum}

def main():
    EVIDENCE.mkdir(exist_ok=True)
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    url=f'http://127.0.0.1:{server.server_port}/examples/gradient-descent/'
    report={'baseline_main':BASE,'scope':'one concept page, PC4 x Scroll/Slide; not all-pattern independent reuse','cases':[]}
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(**browser_options())
            report['chromium']=browser.version
            direct=browser.new_page(viewport={'width':1600,'height':950},device_scale_factor=1)
            direct.goto(url+'content.html');direct.wait_for_selector('.gd-slide[data-ready=true]')
            reference=direct.evaluate(SNAPSHOT)
            direct.close()
            for width,height in SIZES:
                for mode in ('scroll','slides'):
                    page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
                    errors=[];failed=[]
                    page.on('pageerror',lambda e:errors.append(str(e)))
                    page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
                    page.on('requestfailed',lambda r:failed.append(r.url))
                    page.on('response',lambda r:failed.append(f'{r.status} {r.url}') if r.status>=400 else None)
                    page.goto(url+mode+'.html')
                    page.wait_for_selector('.reference-viewport[data-ready=true]')
                    frame=page.locator('iframe').element_handle().content_frame()
                    audit=fonts(page,frame,'.gd-slide *')
                    ui=fonts(page,page.main_frame,'body *')
                    geometry=frame.evaluate(GEOMETRY)
                    output=EVIDENCE/f'{mode}-{width}x{height}.png';page.screenshot(path=str(output),full_page=mode=='scroll')
                    if width==1600:page.screenshot(path=str(CASE/'previews'/('slide.png' if mode=='slides' else 'scroll.png')))
                    assert not any(geometry[k] for k in ('outside','overflow','clipped','overlaps','collisions')),geometry
                    assert geometry['slide']['w']==1440 and geometry['slide']['h']==810
                    shot=frame.evaluate(SNAPSHOT)
                    identity=compare(shot,reference)
                    outer=page.evaluate('''()=>{const a=document.querySelector('.reference-viewport').getBoundingClientRect(),b=document.querySelector('iframe').getBoundingClientRect();
                      return {w:a.width,h:a.height,x:a.x,right:a.right,frame:[b.x,b.y,b.width,b.height],overflow:document.documentElement.scrollWidth>innerWidth,
                        ready:document.querySelector('.reference-viewport').dataset.ready,pages:document.querySelectorAll('iframe').length,
                        buttons:document.querySelectorAll('button').length,links:[...document.querySelectorAll('.mode-links a')].map(e=>e.getAttribute('href'))}}''')
                    assert not outer['overflow'] and outer['pages']==1 and outer['buttons']==0
                    assert outer['x']>=0 and outer['right']<=width and abs(outer['w']/outer['h']-16/9)<.002
                    assert abs(outer['w']-outer['frame'][2])<1 and abs(outer['h']-outer['frame'][3])<1
                    math_result=technical(frame)
                    assert not errors and not failed,(errors,failed)
                    output=EVIDENCE/f'{mode}-{width}x{height}.png'
                    if mode=='scroll':
                        page.evaluate('window.scrollTo(0,document.documentElement.scrollHeight)')
                        end=page.locator('.mode-status').bounding_box()
                        assert end and end['y']+end['height']<=height+1
                        page.evaluate('window.scrollTo(0,0)')
                    else:
                        assert outer['frame'][1]>=44 and outer['frame'][1]+outer['frame'][3]<=height-44+1
                    page.screenshot(path=str(output),full_page=mode=='scroll')
                    if width==1600:page.screenshot(path=str(CASE/'previews'/('slide.png' if mode=='slides' else 'scroll.png')))
                    report['cases'].append(dict(mode=mode,viewport=[width,height],fonts=audit,ui_fonts=ui,geometry=geometry,mode_identity=identity,outer=outer,math=math_result,console_errors=errors,request_failures=failed,evidence=str(output)))
                    page.close()
            # Mode round-trip + reload + keyboard activation, no hidden extra pages.
            page=browser.new_page(viewport={'width':1280,'height':720})
            page.goto(url+'scroll.html');page.wait_for_selector('[data-ready=true]')
            page.get_by_role('link',name='Slide',exact=True).focus();page.keyboard.press('Enter')
            page.wait_for_url('**/slides.html');page.wait_for_selector('[data-ready=true]')
            for key in ('ArrowRight','PageDown','End','Home'):
                page.keyboard.press(key)
            assert page.locator('iframe').count()==1
            page.reload();page.wait_for_selector('[data-ready=true]')
            page.get_by_role('link',name='Scroll',exact=True).click();page.wait_for_selector('[data-ready=true]')
            assert page.url.endswith('scroll.html')
            page.close()
            # Broken script must show a failure, never a successful empty preview.
            page=browser.new_page()
            page.route('**/gradient-descent.js',lambda route:route.abort())
            page.goto(url+'slides.html')
            page.wait_for_selector('[data-ready=error]',timeout=15000)
            assert '불러오지 못했습니다' in page.locator('.frame-status').text_content()
            report['behavior']={'mode_round_trip':True,'keyboard_links':True,'reload':True,'single_page_boundary':True,'script_failure_message':True}
            browser.close()
    finally:
        server.shutdown();server.server_close()
    # Existing canonical sources and common design rules must remain unchanged.
    paths=['AGENTS.md','DESIGN_SYSTEM.md','docs/FIGURE_PRODUCTION_STANDARD.md','docs/DESIGN_COMPONENT_RECIPES.md','docs/REFERENCE_PAGE_SPECS.md']
    paths += [str(p.relative_to(ROOT)) for p in (ROOT/'templates/html').rglob('*') if p.is_file()]
    changed=[]
    for path in paths:
        old=subprocess.check_output(['git','show',f'{BASE}:{path}'],cwd=ROOT)
        if hashlib.sha256(old).hexdigest()!=digest(ROOT/path):changed.append(path)
    assert not changed,changed
    report['canonical_and_common_rules_unchanged']=True
    source_paths=[p for p in CASE.iterdir() if p.suffix in ('.html','.css','.js')]+[Path(__file__),ROOT/'templates/html/styles.css',ROOT/'templates/html/reference-layout.css',ROOT/'templates/html/math-typography.css',ROOT/'scripts/reference_validation.py']
    report['source_sha256']={str(p.relative_to(ROOT)):digest(p) for p in source_paths}
    report['font_sha256']={str(p.relative_to(ROOT)):digest(p) for p in (ROOT/'templates/html/assets/fonts').rglob('*.woff2')}
    report['design_sha256']=digest(CASE/'DESIGN.md')
    report['preview_sha256']={p.name:digest(p) for p in (CASE/'previews').glob('*.png')}
    report.update(status='passed',created_utc=datetime.now(timezone.utc).isoformat())
    (CASE/'previews/validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('PASS: independent mathematics, actual fonts, geometry, PC4 x two modes (8 screens), failure handling; canonical sources unchanged')

if __name__=='__main__':
    main()
