"""Real HTTP/iframe Chromium QA with independent expected values.

Eight viewport/mode cases are distinct from 24 filter states and data/fault scenarios.
Earlier draft JPGs and the injected validation.json remain historical artifacts.
"""
from copy import deepcopy
from datetime import datetime, timezone
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import hashlib, json, sys, threading, traceback
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
sys.path.insert(0, str(REPO/'scripts'))
from reference_validation import browser_options
from verify_kernel import DATA, IDS, reference, displayed, color, fixture_data
SIZES = ((1600,950),(1440,810),(1366,768),(1280,720))
EVIDENCE = ROOT/'review/browser-evidence'
REPORT = ROOT/'review/runtime-validation.json'
ERRORS, FAILED, HTTP_ERRORS, NAV_ABORTS = [], [], [], []


class Handler(SimpleHTTPRequestHandler):
    def log_message(self,*_): pass
    def do_GET(self):
        if self.path == '/favicon.ico':
            self.send_response(204);self.end_headers();return
        super().do_GET()


def audit(page):
    owners={}
    def started(r):
        try:owners[r]=r.frame.url
        except Exception:owners[r]=''
    page.on('request',started)
    page.on('pageerror',lambda e:ERRORS.append(str(e)))
    page.on('console',lambda m:ERRORS.append(m.text) if m.type=='error' else None)
    def failed(r):
        raw={'url':r.url,'error':r.failure,'referer':r.headers.get('referer',''),'resource_type':r.resource_type,'is_navigation':r.is_navigation_request(),'owner_document_at_start':owners.get(r,'')}
        request,referrer=urlsplit(raw['url']),urlsplit(raw['referer'])
        same_origin=(request.scheme,request.netloc)==(referrer.scheme,referrer.netloc)
        bare_referrer=referrer.path.endswith('/interactive-kernel/content.html') and not referrer.query
        initial_document=(raw['is_navigation'] and request.path.endswith('/interactive-kernel/content.html') and not request.query and referrer.path.endswith(('/interactive-kernel/scroll.html','/interactive-kernel/slides.html')))
        if raw['error']=='net::ERR_ABORTED' and same_origin and (bare_referrer or initial_document):
            raw['reason']='superseded-initial-document-asset' if bare_referrer else 'superseded-initial-document'
            NAV_ABORTS.append(raw)
        else: FAILED.append(raw)
    page.on('requestfailed',failed)
    page.on('response',lambda r:HTTP_ERRORS.append({'url':r.url,'status':r.status}) if r.status>=400 else None)


def paint(frame):
    frame.evaluate('async()=>{await document.fonts.ready;await new Promise(r=>requestAnimationFrame(r));await new Promise(r=>requestAnimationFrame(r));}')


def opened(context, base, mode='slides', query='v=1&kernel=identity#kernel', audited=True):
    page=context.new_page()
    if audited: audit(page)
    page.goto(base+mode+'.html?'+query)
    page.wait_for_function("window.KernelViewer?.getState()?.status==='ready'")
    frame=page.frames[1];paint(frame)
    return page,frame


def actual_fonts(page,frame=None):
    target=frame or page
    entries=target.evaluate('''()=>{
      document.querySelectorAll('[data-kernel-font]').forEach(e=>e.removeAttribute('data-kernel-font'));
      return [...document.querySelectorAll('body *')].filter(e=>!e.closest('.sr-only,[hidden]')&&!e.matches('script,style,option,noscript')&&e.getBoundingClientRect().width&&e.getBoundingClientRect().height&&[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())).map((e,i)=>{e.dataset.kernelFont=String(i);return {index:i,text:[...e.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent).join('').trim(),math:!!e.closest('.cell,.math-value,math'),spacing:getComputedStyle(e).letterSpacing}});
    }''')
    cdp=page.context.new_cdp_session(page);cdp.send('DOM.enable');cdp.send('CSS.enable')
    root=cdp.send('DOM.getDocument',{'depth':-1,'pierce':True})['root']['nodeId']
    if frame:
        iframe=cdp.send('DOM.querySelector',{'nodeId':root,'selector':'iframe'})['nodeId']
        root=cdp.send('DOM.describeNode',{'nodeId':iframe,'depth':1,'pierce':True})['node']['contentDocument']['nodeId']
    families={};fallback=[];unpainted=[];spacing=[]
    try:
        for e in entries:
            node=cdp.send('DOM.querySelector',{'nodeId':root,'selector':f'[data-kernel-font="{e["index"]}"]'})['nodeId']
            fonts=cdp.send('CSS.getPlatformFontsForNode',{'nodeId':node})['fonts']
            expected='STIX Two Math' if e['math'] else 'Pretendard Variable'
            if not fonts:unpainted.append(e)
            for f in fonts:
                families[f['familyName']]=families.get(f['familyName'],0)+f['glyphCount']
                if f['familyName']!=expected or not f['isCustomFont']:fallback.append({**e,'font':f,'expected':expected})
            if abs(float(e['spacing'].removesuffix('px'))+4/3)>.02:spacing.append(e)
    finally: cdp.detach()
    assert not fallback and not unpainted and not spacing,(fallback,unpainted,spacing)
    return {'elements':len(entries),'actual_families':families,'fallback':fallback,'unpainted':unpainted,'bad_spacing':spacing}


GEOMETRY=r'''()=>{
 const s=document.querySelector('.kernel-slide'),p=document.querySelector('.teaching-panel'),footer=s.querySelector('footer');
 const b=e=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y,right:r.right,bottom:r.bottom,width:r.width,height:r.height,cx:r.x+r.width/2,cy:r.y+r.height/2}};
 const sb=b(s),pb=b(p),fb=b(footer),style=getComputedStyle(p),inside={x:pb.x+parseFloat(style.borderLeftWidth)+parseFloat(style.paddingLeft),y:pb.y+parseFloat(style.borderTopWidth)+parseFloat(style.paddingTop),right:pb.right-parseFloat(style.borderRightWidth)-parseFloat(style.paddingRight),bottom:pb.bottom-parseFloat(style.borderBottomWidth)-parseFloat(style.paddingBottom)};
 const visible=[...s.querySelectorAll('*')].filter(e=>!e.closest('.sr-only,[hidden]')&&!e.matches('script,style,option,noscript')&&b(e).width&&b(e).height);
 const name=e=>e.id||e.getAttribute('class')||e.tagName;
 const outside=visible.filter(e=>{const r=b(e);return r.x<sb.x-1||r.right>sb.right+1||r.y<sb.y-1||r.bottom>sb.bottom+1}).map(name);
 const padding=visible.filter(e=>e!==p&&p.contains(e)).filter(e=>{const r=b(e);return r.x<inside.x-1||r.right>inside.right+1||r.y<inside.y-1||r.bottom>inside.bottom+1}).map(name);
 const overflow=visible.filter(e=>e instanceof HTMLElement&&!e.matches('select,input')&&(e.scrollWidth>e.clientWidth+1)).map(name);
 const footerOverlap=visible.filter(e=>p.contains(e)&&b(e).bottom>fb.y-1).map(name);
 const textClipping=[];for(const e of visible){if(e instanceof SVGElement||e.closest('math')||e.matches('select,option'))continue;const r=b(e);for(const n of e.childNodes){if(n.nodeType!==3||!n.textContent.trim())continue;const range=document.createRange();range.selectNodeContents(n);for(const a of range.getClientRects())if(a.x<r.x-1||a.right>r.right+1||a.y<r.y-2||a.bottom>r.bottom+2)textClipping.push(name(e));}}
 const matrixClipping=[];for(const cell of s.querySelectorAll('.cell')){const c=b(cell);for(const e of cell.querySelectorAll('*')){const r=b(e);if(r.width&&r.height&&(r.x<c.x+0.5||r.right>c.right-0.5||r.y<c.y+0.5||r.bottom>c.bottom-0.5))matrixClipping.push(name(cell)+':'+e.tagName);}}
 const svgOutside=[];for(const svg of s.querySelectorAll('svg')){const v=svg.viewBox.baseVal;for(const e of svg.querySelectorAll('path,text')){const r=e.getBBox();if(r.x<v.x-1||r.y<v.y-1||r.x+r.width>v.x+v.width+1||r.y+r.height>v.y+v.height+1)svgOutside.push(name(e));}}
 const slots=[...s.querySelectorAll('.matrix-slot')].map(b),arrows=[...s.querySelectorAll('.flow-connector svg')].map(b);const arrowErrors=arrows.map((a,i)=>({y:Math.abs(a.cy-slots[i].cy),leftGap:a.x-slots[i].right,rightGap:slots[i+1].x-a.right}));
 return {slide:sb,panel:pb,inside,footer:fb,outside,padding,overflow,footerOverlap,textClipping,matrixClipping,svgOutside,arrowErrors,labelColor:getComputedStyle(p.querySelector('.panel-label')).color,titleColor:getComputedStyle(p.querySelector('h2')).color};
}'''


def geometry(page,frame,mode):
    result=frame.evaluate(GEOMETRY)
    for key in ('outside','padding','overflow','footerOverlap','textClipping','matrixClipping','svgOutside'):
        assert not result[key],(key,result[key])
    assert all(a['y']<=1 and a['leftGap']>=-1 and a['rightGap']>=-1 for a in result['arrowErrors']),result['arrowErrors']
    assert result['labelColor']=='rgb(49, 104, 200)' and result['titleColor']=='rgb(18, 35, 63)'
    outer=page.evaluate('''()=>{const b=e=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y,right:r.right,bottom:r.bottom}};return {frame:b(document.querySelector('.frame')),note:b(document.querySelector('.viewer-note')),width:innerWidth,height:innerHeight,documentWidth:document.documentElement.scrollWidth}}''')
    assert outer['frame']['x']>=-1 and outer['frame']['right']<=outer['width']+1 and outer['documentWidth']<=outer['width']+1,outer
    if mode=='slides':assert outer['frame']['y']>=43 and outer['frame']['bottom']<=outer['height']+1 and outer['note']['bottom']<=outer['height']+1,outer
    result['viewer']=outer;return result


def contrast(foreground,background):
    import re
    def luminance(css):
        channels=[int(n)/255 for n in re.findall(r'\d+',css)[:3]]
        linear=[c/12.92 if c<=.04045 else ((c+.055)/1.055)**2.4 for c in channels]
        return sum(c*w for c,w in zip(linear,(.2126,.7152,.0722)))
    a,b=sorted((luminance(foreground),luminance(background)))
    return (b+.05)/(a+.05)


def check_state(page,frame,data,kid):
    state=page.evaluate('window.KernelViewer.getState()');kernel=data['kernels'][kid]
    expected=reference(data['input'],kernel['numerators'],kernel['divisor']);divisor=kernel['divisor']
    assert state['status']=='ready' and state['kernelId']==kid
    assert state['input']==data['input'] and state['kernelNumerators']==kernel['numerators'] and state['divisor']==divisor
    assert state['outputNumerators']==[[int(v*divisor) for v in row] for row in expected]
    assert all(abs(state['output'][r][c]-float(expected[r][c]))<1e-12 for r in range(5) for c in range(5))
    snapshot=frame.evaluate('''()=>({selected:document.querySelector('#kernel-select').value,input:[...document.querySelectorAll('#input-matrix .cell')].map(e=>({text:e.textContent,color:getComputedStyle(e).backgroundColor,foreground:getComputedStyle(e).color})),weights:[...document.querySelectorAll('#kernel-matrix .cell')].map(e=>{const f=e.querySelector('mfrac');return {text:e.textContent,aria:e.getAttribute('aria-label'),fraction:f?[f.children[0].textContent,f.children[1].textContent]:null}}),output:[...document.querySelectorAll('#output-matrix .cell')].map(e=>({text:e.textContent,raw:Number(e.dataset.raw),numerator:Number(e.dataset.numerator),denominator:Number(e.dataset.denominator),color:getComputedStyle(e).backgroundColor,foreground:getComputedStyle(e).color})),name:document.querySelector('#role-name').textContent,description:document.querySelector('#role-description').textContent,equation:document.querySelector('#focus-equation').textContent,equationNumbers:[...document.querySelectorAll('#focus-equation mn')].map(e=>e.textContent),equationFraction:(()=>{const f=document.querySelector('#focus-equation mfrac');return f?{terms:[...f.children[0].querySelectorAll('mn')].map(e=>e.textContent),denominator:f.children[1].textContent}:null})(),result:document.querySelector('#focus-result').textContent,resultFractions:[...document.querySelectorAll('#focus-result mfrac')].map(f=>[f.children[0].textContent,f.children[1].textContent]),resultNumbers:[...document.querySelectorAll('#focus-result mn')].map(e=>e.textContent),status:document.querySelector('#kernel-status').textContent,focusCount:document.querySelectorAll('#input-matrix .cell.focus').length})''')
    assert snapshot['selected']==kid and snapshot['name']==kernel['name'] and snapshot['description']==kernel['description']
    for item,n in zip(snapshot['weights'],(n for row in kernel['numerators'] for n in row)):
        if divisor == 1:
            assert item['text'].strip().replace('−','-') == str(n)
        else:
            assert item['fraction'] is not None, 'Fraction weights require an actual MathML fraction'
            assert [v.strip() for v in item['fraction']] == [str(n),str(divisor)]
            assert item['aria'] == f'{n} 나누기 {divisor}'
    for item,n in zip(snapshot['input'],(n for row in data['input'] for n in row)):
        channel=int(n/9*255+.5);assert item['text']==str(n) and item['color']==f'rgb({channel}, {channel}, {channel})'
    contrast_values=[contrast(item['foreground'],item['color']) for item in snapshot['input']+snapshot['output']]
    assert min(contrast_values)>=4.5,('small matrix numeral contrast',min(contrast_values))
    for item,value in zip(snapshot['output'],(v for row in expected for v in row)):
        assert item['text']==displayed(value) and abs(item['raw']-float(value))<1e-12
        assert item['numerator']==int(value*divisor) and item['denominator']==divisor and item['color']==color(value)
    patch=[row[1:4] for row in data['input'][2:5]];products=[a*b for row,weights in zip(patch,kernel['numerators']) for a,b in zip(row,weights)]
    expected_sum=' + '.join(f'({n})' if n<0 else str(n) for n in products)
    numeric = lambda values: [int(v.strip().replace('−','-')) for v in values]
    if snapshot['equationNumbers']:
        if divisor == 1:
            assert numeric(snapshot['equationNumbers']) == products
        else:
            fraction = snapshot['equationFraction']; assert fraction is not None
            assert numeric(fraction['terms']) == products and fraction['denominator'].strip() == str(divisor)
    else:
        assert snapshot['equation']==(expected_sum if divisor==1 else f'({expected_sum}) / {divisor}')
    assert state['focus']['patch']==patch and state['focus']['products']==[products[i:i+3] for i in (0,3,6)]
    assert snapshot['focusCount']==9 and snapshot['status'].startswith(kernel['name'])
    focus=expected[2][1]
    assert displayed(focus) in snapshot['result']
    if divisor != 1:
        assert [[v.strip() for v in pair] for pair in snapshot['resultFractions']] == [[str(int(focus*divisor)),str(divisor)]]
        assert '≈' in snapshot['result'] if focus.denominator != 1 else ('≈' in snapshot['result'] or '=' in snapshot['result'])
    return {'kernel':kid,'focus_numerator':int(focus*divisor),'focus_denominator':divisor,'focus_display':displayed(focus),'verified_output_cells':25,'minimum_matrix_text_contrast':min(contrast_values)}


def interactions(browser,base):
    context=browser.new_context(viewport={'width':1280,'height':720});page,frame=opened(context,base)
    select=frame.locator('#kernel-select');select.focus();select.press('End')
    page.wait_for_function("window.KernelViewer.getState().kernelId==='edge'");assert select.evaluate('e=>document.activeElement===e')
    select.press('Home');page.wait_for_function("window.KernelViewer.getState().kernelId==='identity'")
    select.press('ArrowDown');page.wait_for_function("window.KernelViewer.getState().kernelId==='mean'");check_state(page,frame,DATA,'mean')
    select.press('Tab');assert frame.locator('#reset-kernel').evaluate('e=>document.activeElement===e')
    frame.locator('#reset-kernel').press('Enter');check_state(page,frame,DATA,'identity')
    frame.locator('#kernel-select').select_option('edge');page.wait_for_function("location.search.includes('kernel=edge')");page.reload();page.wait_for_function("window.KernelViewer?.getState()?.status==='ready'");frame=page.frames[1];check_state(page,frame,DATA,'edge')
    for link in ('#scroll-mode','#slide-mode'):
        page.locator(link).click();page.wait_for_function("window.KernelViewer?.getState()?.status==='ready'");frame=page.frames[1];check_state(page,frame,DATA,'edge')
    before=page.evaluate('window.KernelViewer.getState()')
    page.evaluate("()=>{const s=window.KernelViewer.getState();s.input[0][0]=999;s.output[0][0]=999;}")
    assert before==page.evaluate('window.KernelViewer.getState()')
    for invalid in ('',None,'sobel','__proto__'):
        try:page.evaluate('id=>window.KernelViewer.selectKernel(id)',invalid)
        except Exception as e:assert '알 수 없는 필터' in str(e)
        else:raise AssertionError('invalid API accepted')
        assert before==page.evaluate('window.KernelViewer.getState()')
    page.close();invalid_urls=[]
    for query in ('v=2&kernel=mean#kernel','v=1&kernel=missing#kernel','v=1&kernel=mean#other'):
        page,frame=opened(context,base,query=query);check_state(page,frame,DATA,'identity');geometry(page,frame,'slides');assert page.locator('#url-notice').is_visible();invalid_urls.append(query);page.close()
    context.close();return {'native_select_home_end_arrows_tab_enter':True,'focus_preserved':True,'reset':True,'reload_and_mode_round_trip':True,'getState_deep_copy':True,'invalid_api_atomic_cases':4,'invalid_url_cases':invalid_urls}


def custom_states(browser,base):
    result=[]
    for name,data in fixture_data().items():
        if name=='default':continue
        context=browser.new_context(viewport={'width':1440,'height':810})
        context.route('**/interactive-kernel/data.json',lambda route:route.fulfill(status=200,content_type='application/json',body=json.dumps(data)))
        page,frame=opened(context,base)
        for kid in IDS:
            frame.locator('#kernel-select').select_option(kid);paint(frame);result.append({'data':name,**check_state(page,frame,data,kid)})
        context.close()
    return result


def exceptions(browser,base):
    reports=[]
    for file in ('data.json','content.html','model.js','app.js'):
        context=browser.new_context(viewport={'width':1280,'height':720});pattern='**/interactive-kernel/'+file+'*'
        context.route(pattern,lambda route:route.fulfill(status=503,body='intentional failure'))
        page=context.new_page();page.goto(base+'slides.html')
        if file=='data.json':
            page.wait_for_function("window.KernelViewer?.getState()?.status==='error'")
            frame=page.frames[1];assert frame.locator('#output-matrix .cell').count()==0 and frame.locator('#kernel-select').is_disabled()
            context.unroute(pattern);frame.locator('#retry-data').click()
        elif file=='content.html':
            page.wait_for_function("document.body.dataset.ready==='error'")
            context.unroute(pattern)
            retry=page.get_by_role('button',name='다시 불러오기',exact=True)
            assert retry.is_visible(),'viewer content failure must have a visible retry action';retry.click()
        else:
            frame=page.frames[1];frame.locator('#retry-data').wait_for(state='visible');assert frame.locator('#kernel-select').is_disabled();assert frame.locator('#output-matrix .cell').count()==0
            context.unroute(pattern);frame.locator('#retry-data').click()
        page.wait_for_function("window.KernelViewer?.getState()?.status==='ready'")
        frame=page.frames[1];check_state(page,frame,DATA,'identity');reports.append({'failure':file,'visible_retry_and_recovery':True});context.close()
    context=browser.new_context(viewport={'width':1280,'height':720})
    context.route('**/*.woff2',lambda route:route.fulfill(status=404,body='intentional font failure'))
    page,frame=opened(context,base,audited=False)
    frame.wait_for_function("document.body.dataset.fontStatus==='fallback'")
    assert frame.locator('#font-notice').is_visible() and frame.locator('#font-notice').inner_text().strip()
    geometry(page,frame,'slides');check_state(page,frame,DATA,'identity')
    reports.append({'font_failure':'visible fallback notice and usable calculation/layout; separate from actual-font success'})
    context.close()
    context=browser.new_context(viewport={'width':1280,'height':720},reduced_motion='reduce');page,frame=opened(context,base,audited=False)
    frame.locator('#kernel-select').select_option('edge');paint(frame);assert frame.evaluate("document.getAnimations().length")==0;reports.append({'reduced_motion':True});context.close()
    context=browser.new_context(viewport={'width':1280,'height':720},java_script_enabled=False);page=context.new_page();page.goto(base+'slides.html');assert page.locator('noscript').is_visible();reports.append({'no_javascript_notice':True});context.close()
    return reports


def main():
    EVIDENCE.mkdir(parents=True,exist_ok=True);(ROOT/'previews').mkdir(exist_ok=True)
    runtime_paths=[*ROOT.glob('*.html'),*ROOT.glob('*.css'),*ROOT.glob('*.js'),ROOT/'data.json']
    before={str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest() for p in runtime_paths}
    report={'status':'running','created_utc':datetime.now(timezone.utc).isoformat(),'screen_cases':[],'filter_states':[], 'screen_cases_are_not_scenarios':True,'runtime_sha256_at_start':before}
    def save():REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    save();http=ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(REPO)));threading.Thread(target=http.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{http.server_port}/examples/interactive-kernel/'
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(**browser_options());report['chromium']=browser.version
            for width,height in SIZES:
                for mode in ('scroll','slides'):
                    context=browser.new_context(viewport={'width':width,'height':height});page,frame=opened(context,base,mode)
                    frame.evaluate("window.__originalKernelCells=[...document.querySelectorAll('.matrix-input .cell,.matrix-kernel .cell,.matrix-output .cell')]")
                    for kid in IDS:
                        frame.locator('#kernel-select').select_option(kid);paint(frame)
                        result=check_state(page,frame,DATA,kid);result.update(viewport=[width,height],mode=mode,geometry=geometry(page,frame,mode),fonts=actual_fonts(page,frame))
                        assert frame.evaluate("window.__originalKernelCells.every((e,i)=>e===[...document.querySelectorAll('.matrix-input .cell,.matrix-kernel .cell,.matrix-output .cell')][i])")
                        report['filter_states'].append(result)
                    frame.locator('#kernel-select').select_option('identity');paint(frame)
                    shot=EVIDENCE/f'{mode}-{width}x{height}.png';page.screenshot(path=str(shot),full_page=mode=='scroll')
                    if (width,height)==(1440,810):page.screenshot(path=str(ROOT/f'previews/{mode}.png'),full_page=mode=='scroll')
                    report['screen_cases'].append({'viewport':[width,height],'mode':mode,'screenshot':str(shot.relative_to(ROOT)),'viewer_fonts':actual_fonts(page)})
                    save();context.close()
            mode_comparison=[]
            for kid in IDS:
                pair=[item for item in report['filter_states'] if item['viewport']==[1440,810] and item['kernel']==kid]
                assert len(pair)==2
                left={k:v for k,v in pair[0]['geometry'].items() if k!='viewer'}
                right={k:v for k,v in pair[1]['geometry'].items() if k!='viewer'}
                assert left==right,('Scroll/Slide source layout differs',kid)
                assert pair[0]['fonts']==pair[1]['fonts'],('Scroll/Slide actual glyph use differs',kid)
                mode_comparison.append({'kernel':kid,'source_geometry_and_actual_fonts_equal':True})
            report['mode_comparison']=mode_comparison
            report['interactions']=interactions(browser,base);save()
            report['custom_data_states']=custom_states(browser,base);save()
            report['exception_scenarios']=exceptions(browser,base);save();browser.close()
        assert len(report['screen_cases'])==8 and len(report['filter_states'])==24
        assert not ERRORS and not FAILED and not HTTP_ERRORS,(ERRORS,FAILED,HTTP_ERRORS)
        assert not NAV_ABORTS,('The finalized viewer initializes content once; no superseded initial requests are expected',NAV_ABORTS)
        assert before=={str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest() for p in runtime_paths},'Runtime source changed during verification; rerun after source settles'
        report.update(status='passed',console_errors=ERRORS,failed_requests=FAILED,http_errors=HTTP_ERRORS,initial_navigation_cancellations=NAV_ABORTS)
        paths=[*ROOT.glob('*.html'),*ROOT.glob('*.css'),*ROOT.glob('*.js'),ROOT/'data.json',ROOT/'verify_kernel.py',ROOT/'verify_runtime.py']
        report['source_sha256']={str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
        report['preview_sha256']={str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'previews/scroll.png',ROOT/'previews/slides.png']}
        report['unverified']=['actual screen-reader listening','reader comprehension','mobile/tablet/other browsers','learned model performance','all exception x viewport combinations']
        save();print('PASS real Chromium: 8 screens / 24 filter states / 12 custom states / fonts, geometry, keyboard, modes and faults')
    except Exception:
        report.update(status='failed',error=traceback.format_exc());save()
        initial=ROOT/'review/initial-resume-verifier-failure.json'
        if not initial.exists():initial.write_bytes(REPORT.read_bytes())
        raise
    finally:http.shutdown();http.server_close()


if __name__=='__main__':main()
