import functools,http.server,threading,json,hashlib
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[3]; OUT=Path(__file__).resolve().parent
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
results=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for mode in ['scroll','slides']:
  for w,h in [(1600,950),(1440,810),(1366,768),(1280,720)]:
   page=browser.new_page(viewport={'width':w,'height':h}); errors=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   page.on('requestfailed',lambda r:errors.append(r.url))
   page.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
   page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
   url=f'http://127.0.0.1:{server.server_port}/examples/rag-architecture/{mode}.html#rag'
   page.goto(url);page.evaluate('document.fonts.ready');page.wait_for_function("document.body.dataset.ready==='true'")
   data=page.evaluate('''()=>{
    const box=e=>{let r=e.getBoundingClientRect();return {x:r.x,y:r.y,right:r.right,bottom:r.bottom,width:r.width,height:r.height}}, slide=box(document.querySelector('#lesson'));
    const text=[...document.querySelectorAll('body *')].filter(e=>!['SCRIPT','STYLE','TITLE','DESC','NOSCRIPT'].includes(e.tagName.toUpperCase())&&[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())).map(e=>({tag:e.tagName,text:e.textContent,bounds:box(e),spacing:getComputedStyle(e).letterSpacing,color:getComputedStyle(e).color,fill:getComputedStyle(e).fill,fontSize:getComputedStyle(e).fontSize}));
    const outside=text.filter(t=>t.bounds.width&&t.bounds.height&&t.bounds.y>44&&(t.bounds.x<slide.x-1||t.bounds.right>slide.right+1||t.bounds.bottom>slide.bottom+1));
    const nodes=[...document.querySelectorAll('[data-node]')].map(g=>{let r=g.querySelector('rect').getBBox();return {id:g.dataset.node,rect:{x:r.x,y:r.y,width:r.width,height:r.height},texts:[...g.querySelectorAll('text')].map(t=>{let b=t.getBBox();return {text:t.textContent,x:b.x,y:b.y,width:b.width,height:b.height,inside:b.x>=r.x&&b.x+b.width<=r.x+r.width&&b.y>=r.y&&b.y+b.height<=r.y+r.height}})}});
    const footer=box(document.querySelector('footer')),caption=box(document.querySelector('.ref-takeaway'));
    return {slide,text,outside,nodes,footer,caption,spacingFailures:text.filter(t=>Math.abs(parseFloat(t.spacing)+4/3)>.01),scopeText:document.querySelector('.panel-overline').innerText,scopeBounds:box(document.querySelector('.scope-note')),labelBounds:box(document.querySelector('.panel-label')),horizontalOverflow:document.documentElement.scrollWidth>innerWidth,content:document.querySelector('#lesson').textContent};
   }''')
   cdp=page.context.new_cdp_session(page);cdp.send('DOM.enable');cdp.send('CSS.enable');root=cdp.send('DOM.getDocument')['root']['nodeId'];fonts=[]
   for selector in ['h1','.subtitle','svg text','.box .sub','.notes p','footer span','#switch','.panel-label','.scope-note']:
    node=cdp.send('DOM.querySelector',{'nodeId':root,'selector':selector})['nodeId'];fonts.append({'selector':selector,'fonts':cdp.send('CSS.getPlatformFontsForNode',{'nodeId':node})['fonts']})
   page.screenshot(path=str(OUT/f'{mode}-{w}x{h}.png'),full_page=True)
   page.keyboard.press('Tab');focused=page.evaluate("document.activeElement.id==='switch'");page.keyboard.press('Enter');page.wait_for_load_state();page.wait_for_function("document.body.dataset.ready==='true'");switched=page.url.endswith(('slides' if mode=='scroll' else 'scroll')+'.html#rag')
   page.locator('#switch').click();page.wait_for_load_state();page.reload();page.wait_for_function("document.body.dataset.ready==='true'");restored=page.url==url
   if mode=='scroll':page.evaluate('scrollTo(0,document.body.scrollHeight)')
   footerReachable=page.locator('footer').bounding_box()['y']+page.locator('footer').bounding_box()['height']<=h+1
   scopeOK='의미 기반 검색의 예' in data['scopeText'] and '단어 검색 또는 두 방식을 섞은 검색도 가능' in data['scopeText'] and data['labelBounds']['right']<data['scopeBounds']['x']
   ok=scopeOK and not errors and not data['outside'] and not data['spacingFailures'] and not data['horizontalOverflow'] and all(t['inside'] for n in data['nodes'] for t in n['texts']) and all(f['fonts'] and all(x['isCustomFont'] and 'Pretendard' in x['familyName'] for x in f['fonts']) for f in fonts) and focused and switched and restored and footerReachable and (mode=='scroll' or data['slide']['bottom']<=h)
   results.append({'mode':mode,'viewport':[w,h],'pass':ok,'errors':errors,'fonts':fonts,'keyboardFocus':focused,'switched':switched,'restored':restored,'footerReachable':footerReachable,**data});page.close()
 browser.close()
report={'independentReviewer':True,'browser':browser.version,'cases':results,'pass':all(x['pass'] for x in results),'hashes':{f:hashlib.sha256((ROOT/'examples/rag-architecture'/f).read_bytes()).hexdigest() for f in ['lesson.js','lesson.css','scroll.html','slides.html']}}
(OUT/'audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));server.shutdown()
print(json.dumps({'pass':report['pass'],'cases':[{'mode':x['mode'],'viewport':x['viewport'],'pass':x['pass'],'errors':x['errors']} for x in results]},indent=2))

raise SystemExit(0 if report['pass'] else 1)
