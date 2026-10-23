"""PC mode-conversion regression: real glyphs, bounds, independent math and URL state.

Used by verify_pretendard.py so the existing CI entrypoint runs these checks too.
"""
from pathlib import Path
import hashlib

SIZES = ((1600,950),(1440,810),(1366,768),(1280,720))
IDS = ('motivation','locality','pipeline','experiment','takeaway')
INPUT = [[1,2,3,1,0],[4,5,6,2,1],[7,8,9,3,1],[2,1,0,4,2],[1,3,2,1,0]]
KERNELS = {
    'vertical': ([[1,0,-1]]*3,1),
    'average': ([[1,1,1]]*3,9),
    'identity': ([[0,0,0],[0,1,0],[0,0,0]],1),
}

def independent(key,position):
    k,d=KERNELS[key];y,x=divmod(position,3)
    terms=[INPUT[y+dy][x+dx]*k[dy][dx] for dy in range(3) for dx in range(3)]
    return terms,sum(terms)/d

GEOMETRY = '''(selector) => {
 const root=document.querySelector(selector), b=e=>e.getBoundingClientRect();
 const header=b(root.querySelector('.lesson-header')), content=b(root.querySelector('.lesson-content'));
 const takeaway=b(root.querySelector('.lesson-takeaway')), footer=b(root.querySelector('.lesson-footer'));
 const visible=[...root.querySelectorAll('*')].filter(e=>b(e).width&&b(e).height);
 const problems=[];
 for(const e of visible){
   if(e.closest('.scroll-note')&&getComputedStyle(root).zoom!=='1'&&!b(e).width)continue;
   const r=b(e), frame=b(root);
   if(r.left<frame.left-1||r.right>frame.right+1)problems.push(['horizontal',e.className]);
   if(root.classList.contains('slide-sheet')&&(r.top<frame.top-1||r.bottom>frame.bottom+1))problems.push(['vertical',e.className]);
   for(const node of e.childNodes){
     if(node.nodeType!==3||!node.textContent.trim())continue;
     const range=document.createRange();range.selectNodeContents(node);
     for(const t of range.getClientRects())if(t.left<r.left-1||t.right>r.right+1)problems.push(['text',e.className,node.textContent]);
   }
 }
 const tops=[...root.querySelectorAll('.lesson-content > *')].filter(e=>b(e).height);
 const flow=[...root.querySelectorAll('.matrix-flow .teaching-matrix')].map(e=>b(e).y+b(e).height/2);
 const arrows=[...root.querySelectorAll('.flow-connector')].map(e=>{
   const a=b(e.previousElementSibling.querySelector('.teaching-matrix')),c=b(e.nextElementSibling.querySelector('.teaching-matrix')),r=b(e.querySelector('svg'));
   return {y:r.y+r.height/2,left:a.y+a.height/2,right:c.y+c.height/2};
 });
 const comparisons=[...root.querySelectorAll('.feature-preview')].map(e=>({top:b(e).top,height:b(e).height,heading:b(e.querySelector('h3')).top,matrix:b(e.querySelector('.teaching-matrix')).top,result:b(e.querySelector('.comparison-value')).top}));
 return {problems,headerBottom:header.bottom,contentTop:content.top,firstFigureTop:tops.length?b(tops[0]).top:0,lastDetailBottom:tops.length?b(tops.at(-1)).bottom:0,captionTop:takeaway.top,captionBottom:takeaway.bottom,footerTop:footer.top,flowCenters:flow,arrows,comparison:comparisons,viewportOverflow:document.documentElement.scrollWidth>innerWidth};
}'''


def fonts(page,selector):
    entries=page.evaluate('''selector=>[...document.querySelectorAll(`${selector} *`)].filter(e=>e.getBoundingClientRect().width&&e.getBoundingClientRect().height&&[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())&&!e.matches('option')).map((e,i)=>{e.dataset.modeFont=String(i);return {id:i,text:[...e.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent).join(''),spacing:getComputedStyle(e).letterSpacing}})''',selector)
    cdp=page.context.new_cdp_session(page);cdp.send('DOM.enable');cdp.send('CSS.enable')
    root=cdp.send('DOM.getDocument',{'depth':-1})['root']['nodeId'];families=set();glyphs=0
    try:
        for e in entries:
            assert abs(float(e['spacing'].removesuffix('px'))+4/3)<.02,e
            node=cdp.send('DOM.querySelector',{'nodeId':root,'selector':f'[data-mode-font="{e["id"]}"]'})['nodeId']
            actual=cdp.send('CSS.getPlatformFontsForNode',{'nodeId':node})['fonts']
            for f in actual:
                assert f['familyName']=='Pretendard Variable' and f['isCustomFont'],(e,f)
                families.add(f['familyName']);glyphs+=f['glyphCount']
        loaded=page.evaluate('''async()=>{const results=await Promise.all([400,700,800].map(w=>document.fonts.load(`${w} 20px "Pretendard Variable"`,'한글 ABC 0123')));return results.map(a=>a.length)}''')
        assert glyphs and families and all(loaded),(glyphs,families,loaded)
    finally:
        cdp.detach()
        page.evaluate("document.querySelectorAll('[data-mode-font]').forEach(e=>e.removeAttribute('data-mode-font'))")
    return {'text_nodes':len(entries),'actual_family':sorted(families),'glyphs':glyphs,'korean_latin_loads':loaded,'letter_spacing':'-1pt'}


def geometry(page,selector):
    g=page.evaluate(GEOMETRY,selector)
    assert not g['problems'] and not g['viewportOverflow'],g
    assert g['firstFigureTop']>=g['headerBottom']+8,g
    assert g['lastDetailBottom']<=g['captionTop']-8,g
    assert g['captionBottom']<=g['footerTop']-8,g
    if g['flowCenters']:assert max(g['flowCenters'])-min(g['flowCenters'])<1,g
    for a in g['arrows']:assert max(abs(a['y']-a['left']),abs(a['y']-a['right']))<1,a
    if g['comparison']:
        for key in ('top','height','heading','matrix','result'):
            values=[b[key] for b in g['comparison']];assert max(values)-min(values)<1,(key,g)
    return g


def check_math(page,root):
    values=page.locator(root+' .teaching-matrix.input .teaching-cell').first
    assert values.count()
    inputs=page.locator(root+' .teaching-matrix.input').first.locator('.teaching-cell').evaluate_all('(es)=>es.map(e=>Number(e.dataset.value))')
    assert inputs==sum(INPUT,[])
    products=page.locator(root+' [data-product]').evaluate_all('(es)=>es.map(e=>Number(e.dataset.product))')
    assert products==independent('vertical',0)[0],products
    out=page.locator(root+' .teaching-matrix.output .teaching-cell').evaluate_all('(es)=>es.map(e=>Number(e.dataset.value))')
    assert out==[independent('vertical',p)[1] for p in range(9)],out
    return {'input':INPUT,'products':products,'output':[out[i:i+3] for i in range(0,9,3)],'bias':0,'padding':0,'stride':1,'kernel_flipped':False}


def check_lab(page,mode_url):
    page.goto(mode_url+'#experiment',wait_until='networkidle');page.evaluate('document.fonts.ready')
    lab=page.locator('#experiment [data-lab]');states=[]
    for key in KERNELS:
        lab.locator('[data-role="kernel"]').select_option(key)
        # Start each filter at first position; native input focus must not navigate slides.
        for _ in range(8):
            if lab.locator('[data-role="prev"]').is_enabled():lab.locator('[data-role="prev"]').click()
        for pos in range(9):
            expected,value=independent(key,pos)
            actual=lab.locator('[data-product]').evaluate_all('(es)=>es.map(e=>Number(e.dataset.product))')
            assert actual==expected,(key,pos,actual,expected)
            output=lab.locator('.output .teaching-cell').evaluate_all('(es)=>es.map(e=>Number(e.dataset.value))')
            assert output==[independent(key,p)[1] for p in range(9)],(key,pos,output)
            active=lab.locator('.output .active');assert active.count()==1 and float(active.get_attribute('data-value'))==value
            selected=lab.locator('.input .focus').evaluate_all('(es)=>es.map(e=>Number(e.dataset.value))')
            y,x=divmod(pos,3);assert selected==[INPUT[y+dy][x+dx] for dy in range(3) for dx in range(3)]
            formatted=str(int(value)) if value==int(value) else f'{value:.2f}'
            assert lab.locator('[data-role="formula"] strong').inner_text()=='= '+formatted.replace('-','−')
            assert ('position='+str(pos)) in page.url
            assert ('filter='+key) in page.locator('.mode-link').get_attribute('href')
            states.append({'filter':key,'position':pos,'output':value})
            if pos<8:lab.locator('[data-role="next"]').click()
        assert lab.locator('[data-role="next"]').is_disabled()
    lab.locator('[data-role="reset"]').click()
    assert lab.locator('[data-role="kernel"]').input_value()=='vertical'
    assert lab.locator('[data-role="prev"]').is_disabled()
    return states


def validate_dual_mode(browser,base,root,evidence):
    page=browser.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    cases=[];prefix=base+'/templates/dual-mode-learning/'
    evidence.mkdir(parents=True,exist_ok=True)
    try:
        for size in SIZES:
            page.set_viewport_size({'width':size[0],'height':size[1]})
            for mode in ('slides','scroll'):
                page.goto(prefix+mode+'.html',wait_until='networkidle');page.evaluate('document.fonts.ready')
                for section in IDS:
                    if mode=='slides':page.evaluate('(id)=>{location.hash=id}',section)
                    else:page.locator('#'+section).scroll_into_view_if_needed()
                    page.wait_for_timeout(40)
                    selector='#'+section
                    case={'mode':mode,'section':section,'viewport':list(size),'geometry':geometry(page,selector),'font':fonts(page,selector)}
                    if section=='locality':case['math']=check_math(page,selector)
                    if section=='takeaway':
                        for key in KERNELS:
                            actual=page.locator(selector+f' [data-filter="{key}"] .teaching-cell').evaluate_all('(es)=>es.map(e=>Number(e.dataset.value))')
                            assert actual==[independent(key,p)[1] for p in range(9)],(key,actual)
                    cases.append(case)
                    if mode=='slides':page.screenshot(path=str(evidence/f'{size[0]}x{size[1]}-{section}.png'))
            page.goto(prefix+'slides.html#locality',wait_until='networkidle')
            page.locator('body').click(position={'x':5,'y':100});page.keyboard.press('ArrowRight')
            assert page.locator('#progress').inner_text()=='3 / 5'
            page.keyboard.press('End');assert page.locator('#progress').inner_text()=='5 / 5'
            page.keyboard.press('Home');assert page.locator('#progress').inner_text()=='1 / 5'
        page.set_viewport_size({'width':1440,'height':810})
        states={mode:check_lab(page,prefix+mode+'.html') for mode in ('slides','scroll')}
        assert states['slides']==states['scroll']
        # Keep a nondefault filter and middle position through both mode switches and reload.
        page.goto(prefix+'slides.html?filter=average&position=4#experiment',wait_until='networkidle')
        page.locator('[data-role="kernel"]').focus();page.keyboard.press('ArrowRight')
        assert page.locator('#progress').inner_text()=='4 / 5'
        # Native select arrows may change the option; the presentation must stay put.
        page.locator('[data-role="kernel"]').select_option('average')
        for mode in ('scroll','slides'):
            page.locator('.mode-link').click();page.wait_for_url('**/'+mode+'.html?**#experiment')
            page.wait_for_timeout(80)
            assert page.locator('#experiment [data-role="kernel"]').input_value()=='average'
            assert page.locator('#experiment [data-role="position"]').inner_text()=='5 / 9'
            assert page.url.endswith('#experiment')
        page.reload(wait_until='networkidle');assert page.locator('[data-role="position"]').inner_text()=='5 / 9'
        page.goto(prefix+'slides.html?filter=invalid&position=99#experiment',wait_until='networkidle')
        assert page.locator('[data-role="kernel"]').input_value()=='vertical'
        assert page.locator('[data-role="position"]').inner_text()=='1 / 9'
        assert not errors,errors
    finally:page.close()
    files=list((root/'templates/dual-mode-learning').rglob('*'))+[root/'templates/html/styles.css']
    hashes={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files if p.is_file() and p.suffix in ('.js','.css','.html')}
    return {'status':'passed','viewports':SIZES,'cases':cases,'lab_states':states,'mode_roundtrip':{'filter':'average','position':4,'section':'experiment','reload':True},'keyboard':{'arrows_home_end':True,'select_not_intercepted':True},'source_sha256':hashes,'page_errors':errors}
