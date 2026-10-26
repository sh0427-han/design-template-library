"""Preview the user-requested heading hierarchy; do not finalize Markdown rules."""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
import hashlib,json,threading
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
from reference_validation import GEOMETRY,browser_options
from verify_dual_mode import NAMES,SIZES,get_frame

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'previews/heading-review'
ROLES={
 'concept':('.concept-panel h2,.concept-step-label','.concept-panel .card-label'),
 'process':('.node-title','.node-step'),
 'comparison':('.compare-card h2','.comparison-heading .pill,.phase-heading h3'),
 'step-by-step':('.calc-heading','.calc-step'),
 'interactive':('.live-card > h2,.live-metric h3','.ref-k'),
 'architecture':('.arch-title','.arch-phase-band span,.arch-step-roles b,.arch-operation'),
 'experiment':('.experiment-card > h2,.metric h3','.ref-k'),
 'executive-summary':('.exec-impact h2,.exec-action-panel h2,.exec-metric-head h3,.exec-action b','.ref-k'),
 'overfitting-generalization':('.concept-card h2,#overfit-heading,#generalization-heading','.definition-label'),
}
CARD_PAIRS={
 'concept':[('.concept-panel','.card-label','h2',1)],
 'process':[('.node','.node-step','.node-title',4)],
 'comparison':[('.compare-card','.comparison-heading .pill','h2',2)],
 'step-by-step':[('.calc-panel','.calc-step','.calc-heading',2)],
 'interactive':[('.live-card','.ref-k','h2',2)],
 'architecture':[('.arch-stage','.arch-operation','.arch-title',6)],
 'experiment':[('.experiment-card','.ref-k','h2',2)],
 'executive-summary':[('.exec-impact,.exec-action-panel','.ref-k','h2',2)],
 'overfitting-generalization':[('.concept-card','.definition-label','h2',2)],
}
COLORS={'title':'rgb(18, 35, 63)','label':'rgb(49, 104, 200)'}
INSPECT="""es=>es.map(e=>{const s=getComputedStyle(e),r=e.getBoundingClientRect();return {text:e.textContent.trim(),color:e instanceof SVGElement?s.fill:s.color,font:s.fontFamily,size:s.fontSize,weight:s.fontWeight,lineHeight:s.lineHeight,spacing:s.letterSpacing,visible:r.width>0&&r.height>0}})"""

class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
 def do_GET(self):
  if self.path=='/favicon.ico':self.send_response(204);self.end_headers();return
  super().do_GET()

def inspect(frame,name):
 rows=[];pairs=[]
 for card_selector,label_selector,title_selector,count in CARD_PAIRS[name]:
  cards=frame.locator(card_selector);assert cards.count()==count,(name,card_selector,cards.count())
  for i in range(count):
   card=cards.nth(i);label=card.locator(label_selector);title=card.locator(title_selector)
   assert label.count()==1 and title.count()==1,(name,i,'missing or duplicated card label/title')
   ls=label.evaluate_all(INSPECT)[0];ts=title.evaluate_all(INSPECT)[0]
   assert ls['visible'] and ls['color']==COLORS['label'] and ts['visible'] and ts['color']==COLORS['title'],(name,i,ls,ts)
   pairs.append({'card':card_selector,'label':ls['text'],'title':ts['text'],'own_label':True,'own_title':True})
 for role,selector in [('title','h1,'+ROLES[name][0]),('label','.kicker'+(','+ROLES[name][1] if ROLES[name][1] else ''))]:
  nodes=frame.locator(selector).evaluate_all(INSPECT);assert nodes,(name,role)
  for node in nodes:
   assert node['visible'] and node['color']==COLORS[role],(name,role,node)
   assert 'Pretendard' in node['font'] and abs(float(node['spacing'].removesuffix('px'))+4/3)<.02,node
   rows.append({'role':role,**node})
 g=frame.evaluate(GEOMETRY)
 for key in ('outside','overflow','footerOverlap','spacing','clippedText','arrowErrors'):assert not g[key],(name,key,g[key])
 return rows,g,pairs

def gallery():
 names=list(NAMES)+['overfitting-generalization']
 labels=['Concept','Process','Comparison','Step-by-Step','Interactive','Architecture','Experiment','Executive Summary','과적합과 일반화']
 cards=[];contact=Image.new('RGB',(1920,1170),'white');draw=ImageDraw.Draw(contact)
 for i,(name,label) in enumerate(zip(names,labels)):
  ext='png' if name in ('concept','process','comparison') else 'jpg'
  src=ROOT/f'previews/html-{name}.{ext}' if name in NAMES else OUT/'overfitting.png'
  url='../'+src.name if name in NAMES else src.name
  prefix='../../templates/dual-mode-learning/' if name in NAMES else '../../examples/overfitting-generalization/'
  anchor='ref-'+name if name in NAMES else 'concept'
  cards.append(f'<article><small>{i+1:02d}</small><h2>{label}</h2><a href="{url}"><img src="{url}" width="1440" height="810" alt="{label} 제목 색상 적용 화면"></a><p><a href="{prefix}scroll.html#{anchor}">Scroll</a> · <a href="{prefix}slides.html#{anchor}">Slide</a> · <a href="{url}">원본 크기</a></p></article>')
  im=Image.open(src).convert('RGB');im.thumbnail((630,354));x=(i%3)*640;y=(i//3)*390
  draw.text((x+10,y+6),f'{i+1:02d} {name}',fill='#12233f');contact.paste(im,(x+5,y+30))
 contact.save(OUT/'contact.jpg',quality=92)
 html='''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>제목 색상 · 검토용 9종</title><link rel="stylesheet" href="../../templates/html/styles.css"><style>body{display:block;padding:28px;min-height:100vh}header{max-width:1500px;margin:0 auto 24px}h1{font-size:34px;margin:8px 0}header p{color:var(--muted)}main{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px;max-width:1500px;margin:auto}article{border:1px solid var(--border);border-radius:16px;background:white;padding:18px}small,a{color:var(--blue)}article h2{font-size:24px;color:var(--navy);margin:5px 0 14px}img{width:100%;height:auto;display:block}article p{margin:12px 0 0}a{font-weight:700} @media(max-width:900px){main{grid-template-columns:1fr}}</style></head><body><header><div class="kicker">HEADING COLOR REVIEW</div><h1>핵심 제목은 Navy, 분류·단계 라벨은 Blue</h1><p>8종 레퍼런스와 과적합 자료의 적용 시안 · 공통 Markdown 규칙은 검토 후 확정</p></header><main>'''+''.join(cards)+'</main></body></html>'
 (OUT/'index.html').write_text(html)

def main():
 OUT.mkdir(parents=True,exist_ok=True);server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
 threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}'
 report={'status':'running','markdown_finalized':False,'scope':'8 original references + overfitting; PC4 x Scroll/Slide','role_colors':COLORS,'cases':[]}
 errors=[];failed=[];baseline={}
 try:
  with sync_playwright() as p:
   browser=p.chromium.launch(**browser_options());report['chromium']=browser.version
   page=browser.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.on('requestfailed',lambda r:failed.append(r.url))
   for width,height in SIZES:
    page.set_viewport_size({'width':width,'height':height})
    for mode in ('slides','scroll'):
     page.goto(base+'/templates/dual-mode-learning/'+mode+'.html',wait_until='networkidle')
     for name in NAMES:
      if mode=='slides':page.evaluate('(id)=>{location.hash=id}','ref-'+name)
      frame=get_frame(page,name);rows,g,pairs=inspect(frame,name)
      if name not in baseline:baseline[name]=rows
      assert rows==baseline[name],(name,mode,width,'role style mismatch')
      report['cases'].append({'reference':name,'mode':mode,'viewport':[width,height],'headings':rows,'card_pairs':pairs,'geometry':g})
     page.goto(base+'/examples/overfitting-generalization/'+mode+'.html',wait_until='networkidle');page.wait_for_function("document.body.dataset.ready==='true'")
     frame=page.locator('iframe').element_handle().content_frame();frame.evaluate('document.fonts.ready');name='overfitting-generalization';rows,g,pairs=inspect(frame,name)
     if name not in baseline:baseline[name]=rows
     assert rows==baseline[name],(name,mode,width,'role style mismatch')
     report['cases'].append({'reference':name,'mode':mode,'viewport':[width,height],'headings':rows,'card_pairs':pairs,'geometry':g})
     if width==1600 and mode=='slides':frame.locator('.slide').screenshot(path=str(OUT/'overfitting.png'))
     print('PASS heading roles',mode,width,height,flush=True)
   assert not errors and not failed,(errors,failed);assert len(report['cases'])==72
   gallery();page.goto(base+'/previews/heading-review/index.html',wait_until='networkidle');page.evaluate('document.fonts.ready')
   assert page.locator('article').count()==9
   assert page.locator('img').evaluate_all('es=>es.every(e=>e.complete&&e.naturalWidth>0)')
   browser.close();report['status']='passed';report['page_errors']=errors;report['failed_requests']=failed
 finally:
  server.shutdown();server.server_close()
  paths=[ROOT/'templates/html'/f'{n}.html' for n in NAMES]+[ROOT/'templates/html/comparison-reference.css',ROOT/'examples/overfitting-generalization/lesson.css',ROOT/'examples/overfitting-generalization/content.html',Path(__file__),OUT/'change-scope.json']
  report['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
  report['preview_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [*(ROOT/'previews').glob('html-*.*'),OUT/'overfitting.png',OUT/'contact.jpg'] if p.is_file()}
  (OUT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print('PASS 72 heading-role screens; 9-source preview gallery; Markdown pending user review')

if __name__=='__main__':main()
