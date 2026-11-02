from pathlib import Path
from fractions import Fraction as F
import json, threading, http.server, functools, hashlib
from playwright.sync_api import sync_playwright
OUT=Path(__file__).resolve().parent; ROOT=OUT.parents[2]; EX=ROOT/'examples/service-summary'
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}/examples/service-summary/'
expected={'indices':[F(520,800)*100,F(102,120)*100,F(80,50)*100], 'relative_percent':[F(520-800,800)*100,F(102-120,120)*100,F(80-50,50)*100], 'failure_percent':[F(50,10000)*100,F(80,10000)*100], 'failure_pp':(F(80,10000)-F(50,10000))*100}
result={'fixed_sha':'9f73da4665ba27eb6135646a57aa4bc859a36409','independent_fraction_calculation':{k:list(map(str,v)) if isinstance(v,list) else str(v) for k,v in expected.items()},'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in EX.iterdir() if p.suffix in ['.js','.css','.html']},'screens':[]}
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox']);result['browser']=browser.version
 for w,h in [(1600,950),(1440,810),(1366,768),(1280,720)]:
  for mode in ['scroll','slides']:
   page=browser.new_page(viewport={'width':w,'height':h});errors=[];bad=[];fontrequests=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
   page.on('requestfailed',lambda r:bad.append(r.url))
   page.on('response',lambda r:bad.append(r.url) if r.status>=400 else fontrequests.append(r.url) if '.woff2' in r.url else None)
   page.goto(base+mode+'.html');page.wait_for_selector('body[data-ready=true]');frame=page.frames[1]
   data=frame.evaluate('''()=>{let boxes=s=>[...document.querySelectorAll(s)].map(e=>{let r=e.getBoundingClientRect();return {text:e.innerText,x:r.x,y:r.y,w:r.width,h:r.height,right:r.right,bottom:r.bottom}});let bounds=[],spacing=[];for(let e of document.querySelectorAll('body *')){for(let n of e.childNodes){if(n.nodeType!==3||!n.textContent.trim())continue;let range=document.createRange();range.selectNode(n);let r=range.getBoundingClientRect();let panel=e.closest('.panel');let b=panel?panel.getBoundingClientRect():{left:0,top:0,right:1440,bottom:810};if(r.left<b.left-0.5||r.right>b.right+.5||r.top<b.top-.5||r.bottom>b.bottom+.5)bounds.push(n.textContent);if(Math.abs(parseFloat(getComputedStyle(e).letterSpacing)+4/3)>.001)spacing.push(n.textContent)}}return {text:document.body.innerText,bars:boxes('.fill'),values:boxes('.value'),labels:boxes('.metric h3'),deltas:boxes('.delta'),panels:boxes('.panel'),footer:boxes('footer'),bounds,spacing,canvas:[document.documentElement.scrollWidth,document.documentElement.scrollHeight]}}''')
   data['outer']=page.evaluate('''()=>{let r=document.querySelector('.frame').getBoundingClientRect();return {width:innerWidth,height:innerHeight,scrollWidth:document.documentElement.scrollWidth,scrollHeight:document.documentElement.scrollHeight,frame:{left:r.left,top:r.top,right:r.right,bottom:r.bottom},spacing:[...document.querySelectorAll('a,span,button')].map(e=>getComputedStyle(e).letterSpacing)}}''')
   cdp=page.context.new_cdp_session(page);cdp.send('DOM.enable');cdp.send('CSS.enable');root=cdp.send('DOM.getDocument',{'depth':-1,'pierce':True})['root'];fonts=[]
   def visit(n):
    if n.get('nodeType')==1 and any(c.get('nodeType')==3 and c.get('nodeValue','').strip() for c in n.get('children',[])):
     fs=cdp.send('CSS.getPlatformFontsForNode',{'nodeId':n['nodeId']})['fonts']
     if fs:
      attrs=dict(zip(n.get('attributes',[])[::2],n.get('attributes',[])[1::2])); role='math' if 'math-number' in attrs.get('class','').split() else 'mixed' if any(c.get('nodeType')==1 for c in n.get('children',[])) else 'body'
      fonts.append({'node':n['nodeName'],'text':''.join(c.get('nodeValue','') for c in n.get('children',[]) if c.get('nodeType')==3),'role':role,'fonts':fs})
    for c in n.get('children',[]):visit(c)
    if n.get('contentDocument'):visit(n['contentDocument'])
   visit(root);data['fonts']=fonts
   name=f'{mode}-{w}x{h}';page.screenshot(path=str(OUT/(name+'.png')),full_page=True)
   heights=[60,39,60,51,60,96]; checks={'font':bool(fonts) and all(('STIX Two Math' in f['familyName'] if n['role']=='math' else 'Pretendard' in f['familyName']) and f['isCustomFont'] for n in fonts if n['role']!='mixed' for f in n['fonts']),'local_font':bool(fontrequests),'runtime':not(errors or bad),'text_bounds':not data['bounds'],'spacing':not data['spacing'] and all(abs(float(s[:-2])+4/3)<.001 for s in data['outer']['spacing']),'bar_heights':all(abs(b['h']-e)<.01 for b,e in zip(data['bars'],heights)),'bar_baseline':max(b['bottom'] for b in data['bars'])-min(b['bottom'] for b in data['bars'])<.01,'value_above_bar':all(v['bottom']<b['y'] for v,b in zip(data['values'],data['bars'])),'footer_clear':max(b['bottom'] for b in data['panels'])<data['footer'][0]['y'],'outer_width':data['outer']['scrollWidth']==w,'slide_fit':mode!='slides' or data['outer']['frame']['bottom']<=h-44,'required_semantics':all(s in data['text'] for s in ['800','520','120','102','0.5','0.8','−35.0%','−15.0%','+0.3 퍼센트포인트','+60.0%','95%','기존값 = 100','낮을수록 유리','가상','10,000','인과효과','통계적 유의성','반복 관측'])}
   # Isolate direct text nodes only after original geometry and screenshot capture.
   # This makes CDP identify prose units adjacent to nested math without aggregating descendants.
   frame.evaluate("""()=>{let nodes=[];let w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);while(w.nextNode())if(w.currentNode.textContent.trim())nodes.push(w.currentNode);for(let n of nodes){let e=document.createElement('span');e.dataset.reviewRole=n.parentElement.closest('.math-number')?'math':'body';e.textContent=n.textContent;n.replaceWith(e)}}""")
   frame.evaluate("()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))")
   isolated=[]
   def isolate(n):
    attrs=dict(zip(n.get('attributes',[])[::2],n.get('attributes',[])[1::2]))
    if attrs.get('data-review-role'):
     isolated.append({'role':attrs['data-review-role'],'text':''.join(c.get('nodeValue','') for c in n.get('children',[]) if c.get('nodeType')==3),'fonts':cdp.send('CSS.getPlatformFontsForNode',{'nodeId':n['nodeId']})['fonts']})
    for c in n.get('children',[]):isolate(c)
    if n.get('contentDocument'):isolate(n['contentDocument'])
   isolate(cdp.send('DOM.getDocument',{'depth':-1,'pierce':True})['root'])
   data['isolated_direct_text_fonts']=isolated
   checks['all_direct_text_font_roles']=len(isolated)>50 and all(n['fonts'] and all(('STIX Two Math' in f['familyName'] if n['role']=='math' else 'Pretendard' in f['familyName']) and f['isCustomFont'] for f in n['fonts']) for n in isolated)
   page.get_by_role('link',name='Slide' if mode=='scroll' else 'Scroll',exact=True).click();page.wait_for_selector('body[data-ready=true]');checks['mode_content']=page.frames[1].locator('body').inner_text()==data['text'];page.reload();page.wait_for_selector('body[data-ready=true]');checks['reload']=page.frames[1].locator('body').inner_text()==data['text'];page.get_by_role('link',name='Scroll' if mode=='scroll' else 'Slide',exact=True).click();page.wait_for_selector('body[data-ready=true]');checks['roundtrip']=page.url.endswith(mode+'.html#summary')
   page.frames[1].locator('h1').click()
   for k in ['ArrowRight','ArrowLeft','PageDown','PageUp','Home','End','Space']:page.keyboard.press(k)
   checks['iframe_keys']=page.frames[1].locator('body').inner_text()==data['text'] and page.url.endswith('#summary')
   if mode=='scroll':page.evaluate('scrollTo(0,document.body.scrollHeight)');checks['scroll_end']=page.evaluate('scrollY+innerHeight>=document.documentElement.scrollHeight-1')
   else:checks['single_slide_boundary']=page.locator('button:disabled').count()==2
   data['math_roles']=page.frames[1].evaluate("()=>[...document.querySelectorAll('.math-number')].map(e=>({text:e.innerText,family:getComputedStyle(e).fontFamily,weight:getComputedStyle(e).fontWeight,synthesis:getComputedStyle(e).fontSynthesis,spacing:getComputedStyle(e).letterSpacing}))")
   wanted=['−35.0%','280','−15.0%','18','0.5%','0.8%','+0.3','+60.0%','280','18','30']
   checks['math_result_coverage']=sorted(x['text'] for x in data['math_roles'])==sorted(wanted)
   checks['math_result_font_roles']=len([n for n in fonts if n['role']=='math'])==11 and all(x['weight']=='400' and x['synthesis']=='none' and 'STIX Two Math' in x['family'] for x in data['math_roles'])
   checks['general_body_font_roles']=len([n for n in fonts if n['role']=='body'])>30 and all('Pretendard' in f['familyName'] for n in fonts if n['role']=='body' for f in n['fonts'])
   checks['math_only_numeric']=all(not any('가'<=c<='힣' for c in x['text']) for x in data['math_roles'])
   data.update(name=name,checks=checks,errors=errors,failed_requests=bad);result['screens'].append(data);page.close()
 browser.close()
server.shutdown();result['passed']=all(all(s['checks'].values()) for s in result['screens']);(OUT/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps({'passed':result['passed'],'screens':len(result['screens']),'checks':sum(len(s['checks']) for s in result['screens']),'failures':[(s['name'],k) for s in result['screens'] for k,v in s['checks'].items() if not v]}))
