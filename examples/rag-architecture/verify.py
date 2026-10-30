"""Run from repository root: python examples/rag-architecture/verify.py."""
import functools, hashlib, http.server, json, threading
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args): pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
reports=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 for mode in ['scroll','slides']:
  for w,h in [(1600,950),(1440,810),(1366,768),(1280,720)]:
   page=browser.new_page(viewport={'width':w,'height':h},device_scale_factor=1)
   errors=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
   page.on('requestfailed',lambda r:errors.append(r.url))
   page.on('response',lambda r:errors.append(f'{r.status} {r.url}') if r.status>=400 else None)
   page.goto(f'http://127.0.0.1:{server.server_port}/examples/rag-architecture/{mode}.html#rag')
   page.wait_for_function("document.body.dataset.ready==='true'")
   page.evaluate("document.fonts.load('21px \"Pretendard Variable\"')")
   measurements=page.evaluate('''() => {
    const slide=document.querySelector('#lesson'), r=slide.getBoundingClientRect(), z=r.width/1440;
    const nodes=[...document.querySelectorAll('#lesson *')].filter(e=>[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()));
    const bounds=[], spacing=[], textOverflow=[];
    for(const e of nodes){if(e instanceof SVGElement)continue;const range=document.createRange();range.selectNodeContents(e);const b=range.getBoundingClientRect(),a=e.getBoundingClientRect();if(b.left<a.left-1||b.right>a.right+1||b.top<a.top-2||b.bottom>a.bottom+2)textOverflow.push(e.textContent)}
    for(const e of nodes){const b=e.getBoundingClientRect();if(b.width&&b.height){if(b.left<r.left-1||b.right>r.right+1||b.top<r.top-1||b.bottom>r.bottom+1)bounds.push(e.textContent);if(Math.abs(parseFloat(getComputedStyle(e).letterSpacing)+4/3)>.01)spacing.push(e.textContent)}}
    const texts=[...document.querySelectorAll('svg text')].map(e=>({text:e.textContent,bbox:Object.fromEntries(['x','y','width','height'].map(k=>[k,e.getBBox()[k]]))}));
    const nodeOverflow=[];for(const g of document.querySelectorAll('[data-node]')){const rect=g.querySelector('rect').getBBox();for(const t of g.querySelectorAll('text')){const b=t.getBBox();if(b.x<rect.x+6||b.x+b.width>rect.x+rect.width-6||b.y<rect.y+3||b.y+b.height>rect.y+rect.height-3)nodeOverflow.push(t.textContent)}}
    const footer=document.querySelector('footer').getBoundingClientRect(),take=document.querySelector('.ref-takeaway').getBoundingClientRect();
    const panel=document.querySelector('.diagram-panel').getBoundingClientRect(),svg=document.querySelector('svg.pipeline').getBoundingClientRect();
    const panelPadding={left:(svg.left-panel.left)/z,right:(panel.right-svg.right)/z,bottom:(panel.bottom-svg.bottom)/z};
    const arrowChecks=[...document.querySelectorAll('.arrows path')].map(p=>({d:p.getAttribute('d'),bbox:JSON.stringify(p.getBBox())}));
    return {textOverflow,panelPadding,arrowChecks,scale:z,slide:{x:r.x,y:r.y,width:r.width,height:r.height,bottom:r.bottom},bounds,spacing,nodeOverflow,texts,footerGap:(footer.top-take.bottom)/z,horizontalOverflow:document.documentElement.scrollWidth>innerWidth,bodyText:slide.innerText};
   }''')
   cdp=page.context.new_cdp_session(page);cdp.send('DOM.enable');cdp.send('CSS.enable')
   root=cdp.send('DOM.getDocument')['root']['nodeId'];fonts=[]
   for sel in ['h1','.subtitle','.phase text','.box text','.notes p','footer span','.modebar a']:
    node=cdp.send('DOM.querySelector',{'nodeId':root,'selector':sel})['nodeId']
    fonts.append({'selector':sel,'fonts':cdp.send('CSS.getPlatformFontsForNode',{'nodeId':node})['fonts']})
   page.screenshot(path=str(OUT/f'{mode}-{w}x{h}.png'),full_page=True)
   page.locator('#switch').focus();focus=page.evaluate("getComputedStyle(document.activeElement).outlineStyle")
   page.keyboard.press('Enter');page.wait_for_load_state();page.wait_for_function("document.body.dataset.ready==='true'")
   roundtrip=page.url.endswith('#rag')
   page.locator('#switch').click();page.wait_for_load_state();page.reload();page.wait_for_function("document.body.dataset.ready==='true'")
   roundtrip=roundtrip and page.url.endswith(mode+'.html#rag')
   goodfonts=all(x['fonts'] and all('Pretendard' in f['familyName'] and f['isCustomFont'] for f in x['fonts']) for x in fonts)
   ok=not errors and not measurements['bounds'] and not measurements['spacing'] and not measurements['nodeOverflow'] and not measurements['textOverflow'] and min(measurements['panelPadding'].values())>=11 and measurements['footerGap']>=10 and not measurements['horizontalOverflow'] and goodfonts and roundtrip and focus=='solid'
   if mode=='slides':ok=ok and measurements['slide']['bottom']<=h
   reports.append({'mode':mode,'viewport':[w,h],'pass':ok,'errors':errors,'fonts':fonts,'roundtrip':roundtrip,'keyboardFocus':focus,**measurements})
   page.close()
 browser.close()
# Isolated trial uses provided (history-redacted) inputs. Integrated repository
# uses original common documents and the archived manifest's source hashes.
manifest_path=ROOT/'INPUT_MANIFEST.json'
hash_field='provided_sha256'
if not manifest_path.is_file():
 manifest_path=ROOT/'docs/fresh-builder-trial/input-manifest.json'
 hash_field='source_sha256'
manifest=json.loads(manifest_path.read_text())
input_changes=[f['path'] for f in manifest['files'] if not (ROOT/f['path']).is_file() or hashlib.sha256((ROOT/f['path']).read_bytes()).hexdigest()!=f[hash_field]]
result={'input_manifest':str(manifest_path.relative_to(ROOT)),'input_hash_field':hash_field,'browser':'real Playwright Chromium','cases':reports,'input_changes':input_changes,'source_sha256':{n:hashlib.sha256((OUT/n).read_bytes()).hexdigest() for n in ['lesson.js','lesson.css','scroll.html','slides.html']},'pass':all(r['pass'] for r in reports) and not input_changes}
(OUT/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps({'pass':result['pass'],'cases':[{k:r[k] for k in ['mode','viewport','pass','bounds','nodeOverflow','footerGap','errors']} for r in reports],'input_changes':input_changes},ensure_ascii=False,indent=2))
server.shutdown()
raise SystemExit(0 if result['pass'] else 1)
