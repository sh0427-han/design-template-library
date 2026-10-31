"""Independent geometry audit of authored fixtures, separate assertions from Coordinator."""
from pathlib import Path
import functools,http.server,threading,json,hashlib
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[3]; OUT=Path(__file__).resolve().parent
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
rows=[]
# Fixture text is deliberately explicit; no importing/executing the Coordinator verifier.
LONG='외부 문서를 찾아 활용하는 검색 증강 생성의 질문 응답 흐름'
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for case in ['long-original','long-reflow','description-original','description-reflow','overload-reject']:
  for mode in ['scroll','slides']:
   for w,h in [(1600,950),(1440,810),(1366,768),(1280,720)]:
    page=browser.new_page(viewport={'width':w,'height':h});errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('requestfailed',lambda r:errors.append(r.url))
    page.goto(f'http://127.0.0.1:{server.server_port}/examples/rag-architecture/{mode}.html');page.wait_for_function("document.body.dataset.ready==='true'")
    page.evaluate('''({caseName,title})=>{
     if(caseName.startsWith('long'))document.querySelector('h1').textContent=title;
     if(caseName==='long-reflow')document.querySelector('#lesson').classList.add('title-two-column');
     if(caseName.startsWith('description')){
      let g=document.querySelector('[data-node="chunks"]'),sub=g.querySelector('.sub');
      sub.innerHTML='<tspan x="489" dy="0">문서를 의미가 이어지는</tspan><tspan x="489" dy="20">짧은 조각으로 나누기</tspan>';
      if(caseName==='description-reflow'){
       for(let n of [...document.querySelectorAll('[data-node]')].slice(0,4)){n.querySelector('rect').setAttribute('height',90);if(n!==g)for(let t of n.querySelectorAll('text'))t.setAttribute('y',+t.getAttribute('y')+8)}
       sub.setAttribute('y',54);sub.lastElementChild.setAttribute('dy',22);
       document.querySelector('.arrows').setAttribute('transform','translate(0 8)');
       document.querySelector('.transfer').setAttribute('d','M992 93.5 V124 H425 V144.5 M420 138.5 L425 144.5 L430 138.5');
       document.querySelector('.transfer-label').setAttribute('y',117);
      }
     }
     if(caseName==='overload-reject')document.querySelector('.notes p').append(' 문서의 출처와 검색 품질, 최신성 및 응답 근거를 추가로 자세히 설명합니다.'.repeat(30));
    }''',{'caseName':case,'title':LONG})
    measured=page.evaluate('''()=>{
     let rect=e=>{let b=e.getBoundingClientRect();return {left:b.left,top:b.top,right:b.right,bottom:b.bottom,width:b.width,height:b.height}}, slide=document.querySelector('#lesson'),canvas=rect(slide),z=canvas.width/1440;
     let title=document.querySelector('h1'),subtitle=document.querySelector('.subtitle'),a=rect(title),b=rect(subtitle),foot=rect(document.querySelector('footer'));
     let texts=[...document.querySelectorAll('[data-node="chunks"] text')],box=document.querySelector('[data-node="chunks"] rect').getBBox();
     let bounds=texts.map(t=>{let q=t.getBBox();return {text:t.textContent,x:q.x,y:q.y,width:q.width,height:q.height,inside:q.x>=box.x+5&&q.x+q.width<=box.x+box.width-5&&q.y>=box.y+3&&q.y+q.height<=box.y+box.height-3}});
     let notes=rect(document.querySelector('.notes')),caption=rect(document.querySelector('.ref-takeaway'));
     return {zoom:z,title:a,subtitle:b,titleLines:a.height/z/parseFloat(getComputedStyle(title).lineHeight),fonts:[getComputedStyle(title).fontSize,getComputedStyle(subtitle).fontSize,getComputedStyle(texts[1]).fontSize],tracking:getComputedStyle(texts[1]).letterSpacing,columnsSeparate:a.right<=b.left||a.bottom<=b.top,footerInside:foot.bottom<=canvas.bottom+1,footerInViewport:foot.bottom<=innerHeight+1,notesBeforeCaption:notes.bottom<=caption.top,captionBeforeFooter:caption.bottom<=foot.top,nodeBounds:bounds,nodeTextsSeparate:bounds[0].y+bounds[0].height<=bounds[1].y,canvas,foot};
    }''')
    expected=case not in ['description-original','overload-reject']
    fit=measured['footerInside'] and measured['notesBeforeCaption'] and measured['captionBeforeFooter'] and measured['columnsSeparate'] and measured['nodeTextsSeparate'] and all(t['inside'] for t in measured['nodeBounds'])
    zoom=min(1,(w-40)/1440,(h-88)/810) if mode=='slides' else min(1,(w-48)/1440)
    ok=fit==expected and abs(measured['zoom']-zoom)<.001 and measured['fonts']==['49px','21px','18px'] and abs(float(measured['tracking'][:-2])+4/3)<.01 and not errors
    if mode=='slides' and expected:ok=ok and measured['footerInViewport']
    if w==1280:page.screenshot(path=str(OUT/f'{case}-{mode}.png'),full_page=True)
    rows.append({'case':case,'mode':mode,'viewport':[w,h],'pass':ok,'fit':fit,'expectedFit':expected,'errors':errors,**measured});page.close()
 browser.close()
server.shutdown()
report={'pass':all(r['pass'] for r in rows),'cases':rows,'hashes':{f:hashlib.sha256((ROOT/'examples/rag-architecture'/f).read_bytes()).hexdigest() for f in ['lesson.js','lesson.css','scroll.html','slides.html']}}
(OUT/'variants.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'pass':report['pass'],'failures':[r for r in rows if not r['pass']]},ensure_ascii=False))
raise SystemExit(0 if report['pass'] else 1)
