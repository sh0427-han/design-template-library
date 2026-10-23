"""Verify both modes display the original eight pages without a second design.

Compare each mode's actual styles and normalized element bounds to a direct
render of the original. Run its existing technical checks in the embedded HTML.
"""
from pathlib import Path
import hashlib,math
from reference_validation import GEOMETRY
from validate_references import (check_concept,check_motif,check_step,check_interactive,
                                check_architecture,check_experiment,check_executive)
from process_validation import check_process
from comparison_validation import check_comparison

SIZES=((1600,950),(1440,810),(1366,768),(1280,720))
NAMES=('concept','process','comparison','step-by-step','interactive','architecture','experiment','executive-summary')
FINGERPRINT='''()=>{
 const root=document.querySelector('.reference-slide'),origin=root.getBoundingClientRect();
 const scale=origin.width/1440;
 const properties=['fontFamily','fontSize','fontWeight','lineHeight','letterSpacing','color','backgroundColor','borderRadius','paddingTop','paddingRight','paddingBottom','paddingLeft'];
 return [root,...root.querySelectorAll('*')].filter(e=>!e.closest('.sr-only')&&e.getBoundingClientRect().width&&e.getBoundingClientRect().height).map(e=>{
   const r=e.getBoundingClientRect(),s=getComputedStyle(e);
   return {tag:e.tagName,class:typeof e.className==='string'?e.className:e.className.baseVal,style:properties.map(p=>s[p]),box:[(r.x-origin.x)/scale,(r.y-origin.y)/scale,r.width/scale,r.height/scale]};
 });
}'''


def ready(frame,name):
    frame.wait_for_selector('.reference-slide');frame.evaluate('document.fonts.ready')
    if name in ('process','comparison'):frame.wait_for_function("window.CNNFeatureMaps?.status==='ready'")
    if name=='concept':frame.wait_for_function("document.querySelector('.slide').dataset.sampled==='true'")
    frame.evaluate('async()=>{await Promise.all([...document.images].map(im=>im.decode()));}')


def technical(frame,name):
    if name=='concept':return check_concept(frame)
    if name=='process':
        motif=check_motif(frame,name)
        values=frame.locator('.output-item').evaluate_all('(es)=>es.map(e=>({p:Number(e.dataset.probability),text:e.querySelector(".probability-value").textContent,width:Number(e.querySelector(".probability-bar").getAttribute("width")),track:Number(e.querySelector(".probability-track").getAttribute("width"))}))')
        weights=[math.exp(v-2) for v in (2,1,0)];expected=[v/sum(weights) for v in weights]
        for a,b in zip(values,expected):assert abs(a['p']-b)<1e-12 and abs(a['width']/a['track']-b)<1e-12 and a['text']==f'{b*100:.1f}%'
        return {**motif,'independent_softmax':expected,'flow':'same DOM styles and normalized positions as directly validated original'}
    if name=='comparison':return {**check_motif(frame,name),'comparison':check_comparison(frame,1440)}
    if name=='step-by-step':return check_step(frame,1440)
    if name=='interactive':return check_interactive(frame)
    if name=='architecture':return check_architecture(frame,1440)
    if name=='experiment':return check_experiment(frame)
    return check_executive(frame,1440)


def find_document(node,url):
    if node.get('documentURL')==url:return node
    for child in node.get('children',[])+([node['contentDocument']] if 'contentDocument' in node else []):
        found=find_document(child,url)
        if found:return found


def fonts(page,frame):
    entries=frame.evaluate('''()=>[...document.querySelectorAll('.slide *')].filter(e=>!e.closest('.sr-only')&&e.getBoundingClientRect().width&&e.getBoundingClientRect().height&&[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())).map((e,i)=>{e.dataset.modeFont=String(i);return {id:i,spacing:getComputedStyle(e).letterSpacing,text:[...e.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent).join('')}})''')
    cdp=page.context.new_cdp_session(page);cdp.send('DOM.enable');cdp.send('CSS.enable')
    document=find_document(cdp.send('DOM.getDocument',{'depth':-1,'pierce':True})['root'],frame.url)
    assert document,frame.url
    families=set();glyphs=0
    try:
        for e in entries:
            assert abs(float(e['spacing'].removesuffix('px'))+4/3)<.02,e
            node=cdp.send('DOM.querySelector',{'nodeId':document['nodeId'],'selector':f'[data-mode-font="{e["id"]}"]'})['nodeId']
            actual=cdp.send('CSS.getPlatformFontsForNode',{'nodeId':node})['fonts']
            assert actual,('unpainted text',e)
            for f in actual:
                assert f['familyName']=='Pretendard Variable' and f['isCustomFont'],(e,f)
                families.add(f['familyName']);glyphs+=f['glyphCount']
        loaded=frame.evaluate('''async()=>{const a=await Promise.all([400,700,800].map(w=>document.fonts.load(`${w} 20px "Pretendard Variable"`,'한글 ABC 0123')));return a.map(v=>v.length)}''')
        assert glyphs and all(loaded)
    finally:
        cdp.detach();frame.evaluate("document.querySelectorAll('[data-mode-font]').forEach(e=>e.removeAttribute('data-mode-font'))")
    return {'text_nodes':len(entries),'actual_family':sorted(families),'glyphs':glyphs,'korean_latin_loads':loaded,'letter_spacing':'-1pt'}


def compare(actual,expected):
    assert len(actual)==len(expected),(len(actual),len(expected))
    error=0
    for a,b in zip(actual,expected):
        assert (a['tag'],a['class'],a['style'])==(b['tag'],b['class'],b['style']),(a,b)
        delta=max(abs(x-y) for x,y in zip(a['box'],b['box']));error=max(error,delta)
        assert delta<.3,(a,b,delta)
    return {'elements':len(actual),'style_match':True,'max_box_error_px':error}


def get_frame(page,name):
    section=page.locator('#ref-'+name)
    section.wait_for(state='visible');section.scroll_into_view_if_needed()
    section.locator('iframe').wait_for(state='visible')
    page.wait_for_function('(id)=>document.getElementById(id).dataset.ready===\'true\'',arg='ref-'+name)
    frame=section.locator('iframe').element_handle().content_frame()
    ready(frame,name)
    return frame


def bounds(page,name,mode):
    result=page.locator('#ref-'+name+' .reference-viewport').evaluate('''e=>{const r=e.getBoundingClientRect(),f=e.querySelector('iframe').getBoundingClientRect();return {x:r.x,y:r.y,right:r.right,bottom:r.bottom,width:r.width,height:r.height,frame:{x:f.x,y:f.y,right:f.right,bottom:f.bottom},overflow:document.documentElement.scrollWidth>innerWidth,viewport:[innerWidth,innerHeight]}}''')
    assert not result['overflow'],result
    assert abs(result['width']/result['height']-16/9)<.002,result
    assert result['x']>=0 and result['right']<=result['viewport'][0]+1,result
    for k in ('x','y','right','bottom'):assert abs(result[k]-result['frame'][k])<1,result
    if mode=='slides':assert result['y']>=44 and result['bottom']<=result['viewport'][1]-44,result
    return result


def validate_dual_mode(browser,base,root,evidence):
    page=browser.new_page(viewport={'width':1600,'height':950});direct=browser.new_page(viewport={'width':1600,'height':950})
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    failed=[];page.on('requestfailed',lambda r:failed.append(r.url))
    cases=[];baseline={};prefix=base+'/templates/dual-mode-learning/'
    evidence.mkdir(parents=True,exist_ok=True)
    try:
        for name in NAMES:
            direct.goto(base+'/templates/html/'+name+'.html',wait_until='networkidle');ready(direct,name)
            baseline[name]=direct.evaluate(FINGERPRINT)
            if name=='process':check_process(direct,1600)
        for size in SIZES:
            page.set_viewport_size({'width':size[0],'height':size[1]})
            for mode in ('slides','scroll'):
                page.goto(prefix+mode+'.html',wait_until='networkidle')
                for name in NAMES:
                    if mode=='slides':page.evaluate('(id)=>{location.hash=id}', 'ref-'+name)
                    frame=get_frame(page,name)
                    g=frame.evaluate(GEOMETRY)
                    for key in ('outside','overflow','footerOverlap','spacing','clippedText','arrowErrors'):assert not g[key],(mode,name,size,key,g[key])
                    exact=compare(frame.evaluate(FINGERPRINT),baseline[name])
                    math=technical(frame,name)
                    case={'mode':mode,'reference':name,'viewport':list(size),'source':frame.url.split(base)[-1], 'source_design':exact,'bounds':bounds(page,name,mode),'font':fonts(page,frame),'technical':math}
                    cases.append(case)
                    if mode=='slides':page.screenshot(path=str(evidence/f'{size[0]}x{size[1]}-{name}.png'))
                    print('PASS',mode,name,*size,flush=True)
        # Input events stay within the original Interactive page; the view stores only its value.
        page.goto(prefix+'slides.html?threshold=45#ref-interactive',wait_until='networkidle')
        frame=get_frame(page,'interactive');assert frame.locator('#threshold').input_value()=='45'
        frame.locator('#threshold').focus();frame.locator('#threshold').press('ArrowRight')
        assert page.locator('#progress').inner_text()=='5 / 8'
        frame.locator('#threshold').fill('80')
        before=frame.locator('.live-cm td').all_text_contents()
        for mode in ('scroll','slides'):
            page.locator('.mode-link').click();page.wait_for_url('**/'+mode+'.html?**#ref-interactive')
            frame=get_frame(page,'interactive')
            assert frame.locator('#threshold').input_value()=='80'
            assert frame.locator('.live-cm td').all_text_contents()==before
        page.reload(wait_until='networkidle');assert get_frame(page,'interactive').locator('#threshold').input_value()=='80'
        # Keyboard navigation must also work after focus enters a reference iframe.
        page.goto(prefix+'slides.html#ref-process',wait_until='networkidle');frame=get_frame(page,'process')
        frame.locator('h1').click();frame.locator('body').press('ArrowRight');assert page.locator('#progress').inner_text()=='3 / 8'
        page.locator('body').press('End');assert page.locator('#progress').inner_text()=='8 / 8'
        page.locator('body').press('Home');assert page.locator('#progress').inner_text()=='1 / 8'
        page.goto(prefix+'scroll.html#ref-comparison',wait_until='networkidle');get_frame(page,'comparison')
        page.locator('.mode-link').click();page.wait_for_url('**/slides.html?**#ref-comparison');assert page.locator('#progress').inner_text()=='3 / 8'
        page.goto(prefix+'slides.html?threshold=invalid#experiment',wait_until='networkidle')
        assert get_frame(page,'interactive').locator('#threshold').input_value()=='60'
        assert not errors and not failed,(errors,failed)
    finally:page.close();direct.close()
    technical_checks={}
    for case in cases:
        result=case.pop('technical');technical_checks.setdefault(case['reference'],result)
        case['technical_passed']=True
    files=list((root/'templates/dual-mode-learning').rglob('*'))+list((root/'templates/html').rglob('*'))
    hashes={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files if p.is_file() and p.suffix in ('.js','.css','.html','.woff2','.png','.jpg')}
    return {'status':'passed','viewports':SIZES,'references':NAMES,'cases':cases,'technical_checks':technical_checks,'mode_roundtrip':{'reference':'interactive','threshold':80,'reload':True},'keyboard':{'iframe_navigation':True,'input_not_intercepted':True},'source_sha256':hashes,'page_errors':errors,'failed_requests':failed}
