"""RAG-only authored content fixtures; no production interaction or layout engine."""
from pathlib import Path
import functools,http.server,threading,json,hashlib
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent/'evidence';OUT.mkdir(exist_ok=True)
LONG='외부 문서를 찾아 활용하는 검색 증강 생성의 질문 응답 흐름'
CASES=['baseline','long-original','long-reflow','description-original','description-reflow','overload-reject']
EXPECTED={'baseline':True,'long-original':True,'long-reflow':True,'description-original':False,'description-reflow':True,'overload-reject':False}
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start()
rows=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for case in CASES:
  for mode in ['scroll','slides']:
   for w,h in [(1600,950),(1440,810),(1366,768),(1280,720)]:
    page=browser.new_page(viewport={'width':w,'height':h});errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
    page.goto(f'http://127.0.0.1:{server.server_port}/examples/rag-architecture/{mode}.html#rag');page.wait_for_function("document.body.dataset.ready==='true'");page.evaluate('document.fonts.ready')
    page.evaluate('''({name,title})=>{
     if(name.startsWith('long')){document.querySelector('h1').textContent=title;if(name==='long-reflow')document.querySelector('#lesson').classList.add('title-two-column')}
     if(name.startsWith('description')){const n=document.querySelector('[data-node="chunks"]'),t=n.querySelector('.sub');t.innerHTML='<tspan x="489" dy="0">문서를 의미가 이어지는</tspan><tspan x="489" dy="20">짧은 조각으로 나누기</tspan>';if(name==='description-reflow'){
      for(const g of [...document.querySelectorAll('[data-node]')].slice(0,4)){g.querySelector('rect').setAttribute('height','90');if(g!==n)for(const text of g.querySelectorAll('text'))text.setAttribute('y',Number(text.getAttribute('y'))+8)}
      t.setAttribute('y','54');t.lastElementChild.setAttribute('dy','22');
      document.querySelector('.arrows').setAttribute('transform','translate(0 8)');
      document.querySelector('.transfer').setAttribute('d','M992 93.5 V124 H425 V144.5 M420 138.5 L425 144.5 L430 138.5');
      document.querySelector('.transfer-label').setAttribute('y','117');
     }}
     if(name==='overload-reject')document.querySelector('.notes p').append(document.createTextNode(' 문서의 출처와 검색 품질, 최신성 및 응답 근거를 추가로 자세히 설명합니다.'.repeat(30)));
    }''',{'name':case,'title':LONG})
    data=page.evaluate('''()=>{
     const r=e=>{let b=e.getBoundingClientRect();return {x:b.x,y:b.y,right:b.right,bottom:b.bottom,width:b.width,height:b.height}},s=document.querySelector('#lesson'),b=r(s),z=b.width/1440,footer=r(document.querySelector('footer')),caption=r(document.querySelector('.ref-takeaway')),panel=r(document.querySelector('.diagram-panel')),notes=r(document.querySelector('.notes')),head=r(document.querySelector('header'));
     const issues=[];if(footer.bottom>b.bottom+1)issues.push('footer-outside-canvas');if(notes.bottom>caption.y+1)issues.push('notes-caption-overlap');if(head.bottom>panel.y+1)issues.push('header-panel-overlap');if(caption.bottom>footer.y+1)issues.push('caption-footer-overlap');
     for(const g of document.querySelectorAll('[data-node]')){const box=g.querySelector('rect').getBBox();for(const t of g.querySelectorAll('text')){let q=t.getBBox();if(q.x<box.x+5||q.x+q.width>box.x+box.width-5||q.y<box.y+3||q.y+q.height>box.y+box.height-3)issues.push('node-text-outside:'+g.dataset.node+':'+JSON.stringify({x:q.x,y:q.y,width:q.width,height:q.height,text:t.textContent}))}}
     const text=[...document.querySelectorAll('#lesson *')].filter(e=>e.getClientRects().length&&[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())&&!['title','desc'].includes(e.tagName));
     for(const e of text){const q=r(e);if(q.x<b.x-1||q.right>b.right+1||q.bottom>b.bottom+1)issues.push('text-outside-canvas');if(Math.abs(parseFloat(getComputedStyle(e).letterSpacing)+4/3)>.01)issues.push('tracking')}
     const h=document.querySelector('h1'),cs=getComputedStyle(h),sub=document.querySelector('.subtitle'); if(s.classList.contains('title-two-column')&&r(h).right>r(sub).x-1)issues.push('title-definition-overlap');
     if(s.classList.contains('title-two-column')&&r(h).height/z/parseFloat(cs.lineHeight)>2.1)issues.push('title-over-two-lines');
     return {issues:[...new Set(issues)],scale:z,titleFont:cs.fontSize,subtitleFont:getComputedStyle(sub).fontSize,titleLines:r(h).height/z/parseFloat(cs.lineHeight),title:r(h),subtitle:r(sub),footer,canvas:b,notes,caption};
    }''')
    c=page.context.new_cdp_session(page);c.send('DOM.enable');c.send('CSS.enable');root=c.send('DOM.getDocument')['root']['nodeId'];fonts=[]
    for sel in ['h1','.subtitle','[data-node="chunks"]','.notes p']:
     node=c.send('DOM.querySelector',{'nodeId':root,'selector':sel})['nodeId'];fonts+=c.send('CSS.getPlatformFontsForNode',{'nodeId':node})['fonts']
    font_ok=bool(fonts) and all(x['isCustomFont'] and 'Pretendard' in x['familyName'] for x in fonts)
    scale=min(1,(w-40)/1440,(h-88)/810) if mode=='slides' else min(1,(w-48)/1440)
    invariant=abs(data['scale']-scale)<.001 and data['titleFont']=='49px' and data['subtitleFont']=='21px'
    fit=not data['issues']
    if mode=='slides' and data['footer']['bottom']>h+1:fit=False
    if (w,h)==(1280,720):page.screenshot(path=str(OUT/f'{case}-{mode}.png'),full_page=True)
    rows.append({'case':case,'mode':mode,'viewport':[w,h],'fit':fit,'expectedFit':EXPECTED[case],'pass':fit==EXPECTED[case] and font_ok and invariant and not errors,'font_ok':font_ok,'unchanged_font_and_scale':invariant,'errors':errors,**data});page.close()
 browser.close()
report={'pass':all(r['pass'] for r in rows),'longTitle':LONG,'cases':rows,'source_sha256':{f:hashlib.sha256((ROOT/'examples/rag-architecture'/f).read_bytes()).hexdigest() for f in ['lesson.css','lesson.js','slides.html','scroll.html']}}
(OUT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');server.shutdown()
print(json.dumps({'pass':report['pass'],'summary':{c:[{'fit':r['fit'],'expected':r['expectedFit'],'issues':r['issues'],'lines':r['titleLines']} for r in rows if r['case']==c and r['mode']=='slides' and r['viewport']==[1280,720]] for c in CASES}},ensure_ascii=False,indent=2))
raise SystemExit(0 if report['pass'] else 1)
