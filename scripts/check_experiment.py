"""Render #7 only; independently check counts, metrics, alignment and typography.

Run from the repository root: python scripts/check_experiment.py
Chromium uses CDN bytes obtained through TLS-verified curl and a temporary cache.
This leaves browser/system trust and the production HTML CDN import unchanged.
"""
from fractions import Fraction
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import threading
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
SIZES=[(1600,950),(1440,810),(1366,768),(1280,720),(900,900),(390,844)]
FONT_PREFIX='https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/'
CHECK="""() => {
 const slide=document.querySelector('.slide');
 const box=e=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y,right:r.right,bottom:r.bottom,width:r.width,height:r.height}};
 const cx=e=>{const r=box(e);return r.x+r.width/2},cy=e=>{const r=box(e);return r.y+r.height/2};
 const table=slide.querySelector('table');
 const cell=code=>table.querySelector(`[data-code="${code}"]`);
 const codes=['FP','TP','TN','FN'];
 const centering=codes.map(code=>{
  const e=cell(code),label=e.querySelector('.cm-code'),count=e.querySelector('.cm-count');
  const ranges=[label,count].map(el=>{const r=document.createRange();r.selectNodeContents(el);return r.getBoundingClientRect()});
  return {code,xErrors:ranges.map(r=>Math.abs(r.x+r.width/2-cx(e))),
   yError:Math.abs((box(label).y+box(count).bottom)/2-cy(e)),box:box(e)};
 });
 const labels={columns:[...table.querySelectorAll('.column-label')].map(e=>e.textContent),rows:[...table.querySelectorAll('tbody th[scope="row"]')].map(e=>e.textContent)};
 const axisErrors={gt:Math.abs(cx(table.querySelector('.gt-axis'))-(cx(cell('FP'))+cx(cell('TP')))/2),
 prediction:Math.abs(cy(table.querySelector('.pred-axis'))-(cy(cell('FP'))+cy(cell('TN')))/2),
 columns:[Math.abs(cx(document.getElementById('gt-normal'))-cx(cell('FP'))),Math.abs(cx(document.getElementById('gt-anomaly'))-cx(cell('TP')))],
 rows:[Math.abs(cy(document.getElementById('pred-anomaly'))-cy(cell('FP'))),Math.abs(cy(document.getElementById('pred-normal'))-cy(cell('TN')))]};
 const textBounds=e=>{
  const walker=document.createTreeWalker(e,NodeFilter.SHOW_TEXT),rs=[];
  while(walker.nextNode()){if(!walker.currentNode.textContent.trim())continue;const r=document.createRange();r.selectNodeContents(walker.currentNode);rs.push(r.getBoundingClientRect());}
  return {left:Math.min(...rs.map(r=>r.left)),right:Math.max(...rs.map(r=>r.right))};
 };
 const line=box(slide.querySelector('.prediction-divider'));
 const titleRight=textBounds(table.querySelector('.pred-axis-label')).right;
 const labelsLeft=Math.min(...[...table.querySelectorAll('tbody th[scope="row"]')].map(e=>textBounds(e).left));
 const dividerGaps={left:line.x+line.width/2-titleRight,right:labelsLeft-line.x-line.width/2};
 const all=[...slide.querySelectorAll('*')].filter(e=>!e.classList.contains('sr-only')&&e.tagName!=='TR');
 const overflow=all.filter(e=>e.clientWidth>0&&(e.scrollWidth>e.clientWidth+2||e.scrollHeight>e.clientHeight+2)).map(e=>({name:e.className||e.tagName,client:[e.clientWidth,e.clientHeight],scroll:[e.scrollWidth,e.scrollHeight]}));
 const text=all.filter(e=>[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()));
 const badTypography=text.filter(e=>{const s=getComputedStyle(e);return Math.abs(parseFloat(s.letterSpacing)+4/3)>.02||!s.fontFamily.startsWith('"Pretendard Variable"')}).map(e=>e.className||e.tagName);
 const cards=[...slide.querySelectorAll('.experiment-card')];
 const metrics=[...slide.querySelectorAll('.metric')].map(e=>({name:e.dataset.metric,box:box(e),value:e.querySelector('.metric-value').textContent,formula:e.querySelector('.metric-equation').getAttribute('aria-label'),fraction:[...e.querySelectorAll('.fraction > span')].map(e=>e.textContent),calculation:e.querySelector('.metric-calculation').textContent}));
 return {slide:box(slide),content:box(slide.querySelector('.content')),footer:box(slide.querySelector('footer')),
 cards:cards.map(box),table:box(table),labels,axisErrors,centering,metrics,overflow,badTypography,
 pageWidth:document.documentElement.scrollWidth,
 dividerGaps,
 counts:[...table.querySelectorAll('[data-code]')].map(e=>({code:e.dataset.code,count:Number(e.querySelector('.cm-count').textContent),headers:e.getAttribute('headers'),background:getComputedStyle(e).backgroundColor})),
 dividers:{gt:getComputedStyle(table.querySelector('.gt-axis')).borderBottomWidth,prediction:getComputedStyle(slide.querySelector('.prediction-divider')).borderRightWidth},
 fontsLoaded:[...document.fonts].filter(f=>f.family.replaceAll('"','').replaceAll("'",'')==='Pretendard Variable'&&f.status==='loaded').length};
}"""

class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*_):pass

def main():
    output=Path('/tmp/experiment-review');output.mkdir(exist_ok=True)
    cache=Path('/tmp/experiment-verified-fonts');cache.mkdir(exist_ok=True)
    manifest_path=cache/'manifest.json'
    manifest=json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    assets={}
    evidence=ROOT/'previews/review/experiment-validation.json'
    report={'status':'running','font_delivery':'CDN bytes fetched by curl with TLS verification; Playwright route fulfills the original URLs; no TLS bypass or trust changes','cases':[]}
    evidence.write_text(json.dumps(report))
    def serve_font(route):
        url=route.request.url
        assert url.startswith(FONT_PREFIX),url
        path=cache/hashlib.sha256(url.encode()).hexdigest()
        if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest()!=manifest.get(url):
            subprocess.run(['curl','--fail','--silent','--show-error','--location','--proto','=https','--tlsv1.2','--max-time','45',url,'-o',str(path)],check=True)
            manifest[url]=hashlib.sha256(path.read_bytes()).hexdigest()
            manifest_path.write_text(json.dumps(manifest,indent=2))
        assets[url]=manifest[url]
        content_type='text/css' if '.css' in url else 'font/woff2'
        route.fulfill(body=path.read_bytes(),headers={'content-type':content_type,'access-control-allow-origin':'*'})
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_EXECUTABLE') or shutil.which('chromium'),headless=True)
            report['browser']=browser.version
            page=browser.new_page(device_scale_factor=1);errors=[];failures=[];http_errors=[]
            page.route('https://cdn.jsdelivr.net/**',serve_font)
            page.on('pageerror',lambda e:errors.append(str(e)))
            page.on('requestfailed',lambda r:failures.append({'url':r.url,'failure':r.failure}))
            page.on('response',lambda r:http_errors.append(f'{r.status} {r.url}') if r.status>=400 and '/templates/' in r.url else None)
            for width,height in SIZES:
                page.set_viewport_size({'width':width,'height':height})
                page.goto(f'http://127.0.0.1:{server.server_port}/templates/html/experiment.html',wait_until='networkidle')
                page.evaluate('document.fonts.ready')
                r=page.evaluate(CHECK)
                page.locator('.slide').screenshot(path=str(output/f'experiment-{width}x{height}.png'),animations='disabled')
                assert all(0<float(width.removesuffix('px'))<=2 for width in r['dividers'].values()),r['dividers']
                assert abs(r['dividerGaps']['left']-r['dividerGaps']['right'])<.25 and min(r['dividerGaps'].values())>2,r['dividerGaps']
                assert page.locator('.experiment-card .ref-k').all_text_contents()==['CONFUSION MATRIX','METRICS']
                assert page.locator('.metric-description').all_text_contents()==['전체 샘플 중 맞힌 비율','이상 예측 중 실제 이상 비율','실제 이상 중 찾아낸 비율','정밀도·재현율의 조화평균']
                assert page.locator('h1').inner_text()=='혼동행렬과 평가 지표'
                assert page.locator('.subtitle').inner_text()=='12개 샘플로 보는 혼동행렬과 분류 성능'
                assert r['labels']=={'columns':['실제 이상','실제 정상'],'rows':['예측 이상','예측 정상']}
                assert [(c['code'],c['count']) for c in r['counts']]==[('TP',4),('FP',1),('FN',2),('TN',5)]
                assert [c['headers'] for c in r['counts']]==['pred-anomaly gt-anomaly','pred-anomaly gt-normal','pred-normal gt-anomaly','pred-normal gt-normal']
                counts={c['code']:c['count'] for c in r['counts']};tp,tn,fp,fn=(counts[k] for k in ['TP','TN','FP','FN'])
                assert tp+tn+fp+fn==12 and tn+fp==6 and tp+fn==6
                precision=Fraction(tp,tp+fp);recall=Fraction(tp,tp+fn)
                values={'accuracy':Fraction(tp+tn,12),'precision':precision,'recall':recall,'f1':2*precision*recall/(precision+recall)}
                assert values['f1']==Fraction(2*tp,2*tp+fp+fn)
                fractions={'accuracy':f'{tp+tn}/12','precision':f'{tp}/{tp+fp}','recall':f'{tp}/{tp+fn}','f1':f'{2*tp}/{2*tp+fp+fn}'}
                equations={'accuracy':('(TP + TN) / (TP + TN + FP + FN)',['TP + TN','TP + TN + FP + FN']),'precision':('TP / (TP + FP)',['TP','TP + FP']),'recall':('TP / (TP + FN)',['TP','TP + FN']),'f1':('2TP / (2TP + FP + FN)',['2TP','2TP + FP + FN'])}
                for m in r['metrics']:
                    value=f"{100*float(values[m['name']]):.1f}%"
                    assert m['value']==value
                    assert m['calculation']==f"= {fractions[m['name']]} = {value}"
                    assert (m['formula'],m['fraction'])==equations[m['name']]
                harmonic=page.locator('.metric-alternate').inner_text().replace('\n',' ')
                assert harmonic=='= 2 × Precision × Recall / (Precision + Recall)'
                assert page.locator('.error-explanations p').all_text_contents()==['FP: 정상인데 이상으로 예측','FN: 이상인데 정상으로 예측']
                colors={c['code']:c['background'] for c in r['counts']}
                assert colors['TP']==colors['TN']=='rgb(227, 246, 243)'
                assert colors['FP']==colors['FN']=='rgb(255, 240, 224)'
                assert max([r['axisErrors']['gt'],r['axisErrors']['prediction'],*r['axisErrors']['columns'],*r['axisErrors']['rows']])<2,r['axisErrors']
                assert all(max(c['xErrors'])<2 and c['yError']<2 for c in r['centering']),r['centering']
                assert not r['overflow'],(width,r['overflow'])
                assert not r['badTypography'],r['badTypography']
                assert r['fontsLoaded']>0,'Actual Pretendard glyphs did not load'
                assert r['pageWidth']<=width
                assert r['content']['bottom']<=r['footer']['y']+1
                if width>900:
                    assert abs(r['slide']['width']/r['slide']['height']-16/9)<.002
                    assert r['slide']['right']<=width+1 and r['slide']['bottom']<=height+1
                    assert r['cards'][0]['right']<r['cards'][1]['x']
                    assert abs(r['cards'][0]['y']-r['cards'][1]['y'])<1
                    assert abs(r['cards'][0]['bottom']-r['cards'][1]['bottom'])<1
                else:
                    assert r['cards'][0]['bottom']<r['cards'][1]['y']
                if width==1600:
                    page.locator('.slide').screenshot(path=str(ROOT/'previews/html-experiment.jpg'),quality=94,animations='disabled')
                report['cases'].append({'viewport':[width,height],**r})
                print('PASS',width,height,flush=True)
            assert not errors and not failures and not http_errors,(errors,failures,http_errors)
            report.update(status='passed',font_assets=assets,page_errors=errors,request_failures=failures,http_errors=http_errors)
            browser.close()
    except Exception as exc:
        report.update(status='failed',error=str(exc));raise
    finally:
        server.shutdown();server.server_close()
        evidence.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':main()
