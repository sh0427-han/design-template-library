#!/usr/bin/env python3
"""Run from any cwd: python /path/to/examples/service-summary/verify.py.
Requires Python playwright and Chromium (CHROMIUM_PATH optional); no remote access.
"""
from pathlib import Path
from fractions import Fraction
import os,json,hashlib,threading,http.server,functools,shutil
from playwright.sync_api import sync_playwright
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OUT=ROOT/'docs/user-screen-review/evidence'; OUT.mkdir(parents=True,exist_ok=True)
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}/'+HERE.relative_to(ROOT).as_posix()+'/'
report={'checks':[],'screens':[],'math':{},'source_hashes':{},'input_integrity':[]}
def check(name,value,detail=None):
 report['checks'].append({'name':name,'pass':bool(value),'detail':detail})
for f in sorted(HERE.iterdir()):
 if f.suffix in ['.html','.css','.js','.py']:report['source_hashes'][f.name]=hashlib.sha256(f.read_bytes()).hexdigest()
manifest=ROOT/'INPUT_MANIFEST.json'
if manifest.exists():
 for f in json.loads(manifest.read_text())['files']:
  actual=hashlib.sha256((ROOT/f['path']).read_bytes()).hexdigest()
  report['input_integrity'].append({'path':f['path'],'unchanged':actual==f['provided_sha256']})
 check('All supplied inputs unchanged',all(x['unchanged'] for x in report['input_integrity']))
else:
 report['input_integrity_note']='Input manifest absent in this host repository; original supplied-input integrity not checked.'
report['shared_hashes']={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [ROOT/'templates/html/styles.css',ROOT/'templates/html/math-typography.css',ROOT/'templates/html/assets/fonts/stix-two-math/STIXTwoMath-Regular.woff2',ROOT/'templates/html/assets/fonts/pretendard/PretendardVariable.woff2']}
indices=[Fraction(520,800)*100,Fraction(102,120)*100,Fraction(80,50)*100]
changes=[x-100 for x in indices]
report['math']={'indices':list(map(float,indices)),'relative_changes':list(map(float,changes)),'failure_rates_percent':[float(Fraction(50,10000)*100),float(Fraction(80,10000)*100)],'percentage_point_difference':float((Fraction(80,10000)-Fraction(50,10000))*100),'extra_failures':80-50,'latency_ms_difference':520-800,'daily_cost_difference':102-120,'method':'Python fractions, independently from implementation JS'}
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH') or shutil.which('chromium'),headless=True,args=['--no-sandbox'])
 report['browser']=browser.version
 for w,h in [(1600,950),(1440,810),(1366,768),(1280,720)]:
  for mode in ['scroll','slides']:
   page=browser.new_page(viewport={'width':w,'height':h},device_scale_factor=1)
   errors=[];requests=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
   page.on('requestfailed',lambda r:errors.append(r.url+': '+str(r.failure)))
   page.on('response',lambda r:requests.append({'url':r.url.replace(base,'./'),'status':r.status}) if r.status>=400 or '.woff2' in r.url else None)
   page.goto(base+mode+'.html#summary');page.wait_for_selector('body[data-ready="true"]')
   f=page.frames[1];f.evaluate('document.fonts.ready')
   data=f.evaluate('''() => {
    const rect=e=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height,right:r.right,bottom:r.bottom}};
    const leaves=[...document.querySelectorAll('body *')].filter(e=>[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()));
    const clipping=[];const spacing=[];
    for(const e of leaves){const s=getComputedStyle(e);if(Math.abs(parseFloat(s.letterSpacing)+4/3)>.001)spacing.push(e.outerHTML);const range=document.createRange();range.selectNodeContents(e);const t=range.getBoundingClientRect();const panel=e.closest('.panel');if(panel){const r=panel.getBoundingClientRect();if(t.left<r.left+24-.5||t.right>r.right-24+.5||t.top<r.top+20-.5||t.bottom>r.bottom-20+.5)clipping.push({tag:e.tagName,text:e.textContent,box:rect(e),panel:rect(panel)})}if(t.right>1440+.5||t.bottom>810+.5||t.left<0||t.top<0)clipping.push({outside:true,text:e.textContent});}
    return {metrics:window.reportMetrics,bars:[...document.querySelectorAll('.fill')].map(rect),panels:[...document.querySelectorAll('.panel')].map(rect),footer:rect(document.querySelector('footer')),clipping,spacing,scrollWidth:document.documentElement.scrollWidth,scrollHeight:document.documentElement.scrollHeight,labels:[...document.querySelectorAll('.panel')].map(e=>({label:getComputedStyle(e.querySelector('.panel-label')).color,title:getComputedStyle(e.querySelector('h2')).color,labelCount:e.querySelectorAll('.panel-label').length})),text:document.body.innerText};
   }''')
   math_roles=f.evaluate("[...document.querySelectorAll('.math-number')].map(e=>({text:e.textContent,weight:getComputedStyle(e).fontWeight,synthesis:getComputedStyle(e).fontSynthesis,tracking:getComputedStyle(e).letterSpacing}))")
   # Audit each direct text run separately, so mixed prose/math parents cannot hide wrong-role fonts.
   audit="""() => {const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);const texts=[];let n;while(n=w.nextNode())if(n.textContent.trim()&&!['SCRIPT','STYLE'].includes(n.parentElement.tagName))texts.push(n);for(const t of texts){const span=document.createElement('span');span.dataset.fontRole=t.parentElement.closest('.math-number')?'math':'prose';t.replaceWith(span);span.append(t);}}"""
   f.evaluate(audit);page.evaluate(audit)
   cdp=page.context.new_cdp_session(page);cdp.send('DOM.enable');cdp.send('CSS.enable')
   root=cdp.send('DOM.getDocument',{'depth':-1,'pierce':True})['root']
   nodes=[]
   def walk(n):
    if n.get('nodeType')==1 and any(c.get('nodeType')==3 and c.get('nodeValue','').strip() for c in n.get('children',[])):nodes.append(n)
    for c in n.get('children',[]):walk(c)
    if 'contentDocument' in n:walk(n['contentDocument'])
   walk(root)
   fonts=[]
   for n in nodes:
    a=cdp.send('CSS.getPlatformFontsForNode',{'nodeId':n['nodeId']})['fonts']
    if a:
     attrs=dict(zip(n.get('attributes',[])[::2],n.get('attributes',[])[1::2]));fonts.append({'tag':n['nodeName'],'role':attrs.get('data-font-role','unclassified'),'text':''.join(c.get('nodeValue','') for c in n.get('children',[]) if c.get('nodeType')==3),'fonts':a})
   cleanup="document.querySelectorAll('[data-font-role]').forEach(e=>e.replaceWith(...e.childNodes))"
   f.evaluate(cleanup);page.evaluate(cleanup)
   key=f'{mode}-{w}x{h}'
   check(key+' actual role-specific fonts',len(fonts)>20 and all(v['role'] in ['math','prose'] and all(('STIX Two Math' if v['role']=='math' else 'Pretendard') in ff['familyName'] and ff['isCustomFont'] for ff in v['fonts']) for v in fonts),fonts)
   check(key+' math coverage and regular glyphs',not math_roles,math_roles)
   check(key+' local WOFF2',all(any(font in r['url'] and r['status']==200 for r in requests) for font in ['PretendardVariable.woff2']),requests)
   check(key+' no direction arrows or numeric y-axis',f.locator('.trend-arrow,.axis').count()==0)
   check(key+' red deterioration',f.locator('.worse .fill.after').evaluate("e=>getComputedStyle(e).backgroundColor")=='rgb(200, 68, 68)')
   check(key+' no authoring meta visible',not any(t in data['text'] for t in ['가상','실제 자료 아님','실측 성과','관측한 예시']))
   check(key+' no errors',not errors and all(r['status']<400 for r in requests),errors)
   check(key+' spacing',not data['spacing'],data['spacing'])
   check(key+' text inside panel padding/canvas',not data['clipping'],data['clipping'])
   check(key+' arithmetic',all(abs(m['index']-float(indices[i]))<1e-9 and abs(m['change']-float(changes[i]))<1e-9 for i,m in enumerate(data['metrics'])))
   bars=data['bars'];check(key+' bar heights',all(abs(b['height']-expected)<.1 for b,expected in zip(bars,[120,78,120,102,75,120])),bars)
   check(key+' bar baseline',max(b['bottom'] for b in bars)-min(b['bottom'] for b in bars)<.1)
   check(key+' panel/footer clearance',max(r['bottom'] for r in data['panels'])+14<data['footer']['y'])
   check(key+' role colors',all(l=={'label':'rgb(49, 104, 200)','title':'rgb(18, 35, 63)','labelCount':1} for l in data['labels']))
   check(key+' consistent relative change units',f.locator('.delta').all_inner_texts()==['개선−35.0%','개선−15.0%','악화+60.0%'] and '퍼센트포인트' not in data['text'])
   check(key+' required values',all(s in data['text'] for s in ['800','520','120','102','0.5','0.8','35.0%','15.0%','+60.0%','10,000건당 실패 30건 증가','변화율은 모두 기존값 대비(%)','10,000','95%','통계적 유의성']))
   outer=page.evaluate('''()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,height:innerHeight,scrollHeight:document.documentElement.scrollHeight,frame:(()=>{const r=document.querySelector('.frame').getBoundingClientRect();return{x:r.x,y:r.y,right:r.right,bottom:r.bottom,width:r.width,height:r.height}})(),spacing:[...document.querySelectorAll('a,button,span')].map(e=>getComputedStyle(e).letterSpacing)})''')
   check(key+' outer layout',outer['scrollWidth']==w and outer['frame']['right']<=w and (mode!='slides' or outer['frame']['bottom']<=h-44),outer)
   check(key+' navigation spacing',all(abs(float(s[:-2])+4/3)<.001 for s in outer['spacing']))
   page.screenshot(path=str(OUT/(key+'.png')),full_page=True)
   report['screens'].append({'name':key,'geometry':data,'outer':outer,'capture':key+'.png'})
   other='Slide' if mode=='scroll' else 'Scroll'
   page.get_by_role('link',name=other,exact=True).click();page.wait_for_selector('body[data-ready="true"]')
   check(key+' mode roundtrip contents',page.frames[1].locator('body').inner_text()==data['text'] and page.url.endswith('#summary'))
   page.reload();page.wait_for_selector('body[data-ready="true"]');check(key+' reload',page.frames[1].locator('body').inner_text()==data['text'])
   for k in ['ArrowRight','ArrowLeft','PageDown','PageUp','Home','End','Space']:page.keyboard.press(k)
   check(key+' one-page keyboard boundary',page.frames[1].locator('.metric').count()==3 and page.url.endswith('#summary'))
   page.close()
 page=browser.new_page();page.goto(base+'content.html');page.wait_for_selector('.metric')
 boundary=page.evaluate('''()=>({zero:comparison(0,3),equal:comparison(10,10),half:comparison(20,10),double:comparison(20,40),invalid:(()=>{try{comparison(-1,3);return false}catch{return true}})()})''')
 check('alternate data and zero denominator',boundary=={'zero':{'index':None,'change':None,'difference':3},'equal':{'index':100,'change':0,'difference':0},'half':{'index':50,'change':-50,'difference':-10},'double':{'index':200,'change':100,'difference':20},'invalid':True},boundary)
 failure=browser.new_page()
 failure.route('**/content.html',lambda route:route.fulfill(status=500,body='Unavailable'))
 failure.goto(base+'slides.html');failure.wait_for_function("document.querySelector('.loading').textContent.includes('불러오지 못했습니다')")
 check('failed content has visible recovery message',failure.locator('.loading').is_visible() and failure.locator('body').get_attribute('data-ready') is None)
 browser.close()
server.shutdown()
report['passed']=all(c['pass'] for c in report['checks'])
(OUT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
failed=[c['name'] for c in report['checks'] if not c['pass']]
print(json.dumps({'passed':report['passed'],'checks':len(report['checks']),'failed':failed},ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
