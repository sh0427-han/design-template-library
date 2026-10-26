"""Independent curve arithmetic and real Chromium QA for the one-page reuse pilot."""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from datetime import datetime,timezone
import argparse,hashlib,json,math,re,threading,traceback
from playwright.sync_api import sync_playwright
from reference_validation import browser_options
from verify_dual_mode import FINGERPRINT,compare,find_document
ROOT=Path(__file__).resolve().parents[1]
CASE=ROOT/'examples/overfitting-generalization'
SIZES=((1600,950),(1440,810),(1366,768),(1280,720))

def independent(data):
    assert data['metric']=='mean_squared_error' and data['unit']=='dimensionless' and 'generalization' not in data
    assert len(data['points'])==41
    error=0
    for i,p in enumerate(data['points']):
        u=i/40
        expected={'progress':u,'training':.1+.72/math.exp(3*u),'validation':.2+.6/math.exp(4*u)+.9*u*u}
        for k,v in expected.items():error=max(error,abs(p[k]-v))
    assert error<1e-14,error
    points=data['points'];assert all(a['training']>b['training'] for a,b in zip(points,points[1:]))
    assert points[0]['validation']>points[10]['validation'] and points[20]['validation']<points[40]['validation']
    return {'points':41,'series':2,'max_independent_value_error':error,'same_loss_basis':True,'late_divergence':True,'generalization_is_image_diagram':True,'real_experiment':False}

GEOMETRY='''() => {
const s=document.querySelector('.slide'), footer=s.querySelector('footer');
const box=e=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y,right:r.right,bottom:r.bottom,width:r.width,height:r.height}};
const visible=[...s.querySelectorAll('*')].filter(e=>e.getBoundingClientRect().width&&e.getBoundingClientRect().height&&!e.matches('title,desc'));
const sb=box(s),fb=box(footer);
const outside=visible.filter(e=>{const b=box(e);return b.x<sb.x-1||b.right>sb.right+1||b.y<sb.y-1||b.bottom>sb.bottom+1}).map(e=>e.id||e.className.baseVal||e.className||e.tagName);
const containers=[...s.querySelectorAll('.definition,.curve-panel')];
const padding=containers.map(e=>{const b=box(e),st=getComputedStyle(e);const inner={x:b.x+parseFloat(st.paddingLeft)+1,y:b.y+parseFloat(st.paddingTop)+1,right:b.right-parseFloat(st.paddingRight)-1,bottom:b.bottom-parseFloat(st.paddingBottom)-1};
const escaped=[...e.querySelectorAll('*')].filter(c=>!c.matches('title,desc')&&c.getBoundingClientRect().width&&c.getBoundingClientRect().height).filter(c=>{const r=box(c);return r.x<inner.x-1||r.right>inner.right+1||r.y<inner.y-1||r.bottom>inner.bottom+1}).map(c=>c.id||c.className.baseVal||c.className||c.tagName);return {name:e.className,inner,escaped}});
const text=visible.filter(e=>[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()));const clipped=[];
for(const e of text){if(e instanceof SVGElement)continue;const b=box(e);for(const n of e.childNodes){if(n.nodeType!==3||!n.textContent.trim())continue;const r=document.createRange();r.selectNodeContents(n);for(const a of r.getClientRects())if(a.left<b.x-1||a.right>b.right+1||a.top<b.y-2||a.bottom>b.bottom+2)clipped.push(e.className||e.tagName)}}
const labels=[],labelOutside=[],collisions=[];
for(const svg of s.querySelectorAll('svg')){
 const vb=svg.viewBox.baseVal,origin=svg.getBoundingClientRect(),sx=origin.width/vb.width,sy=origin.height/vb.height;const group=[...svg.querySelectorAll('text')].map(e=>({svg:svg.id,text:e.textContent,bbox:(()=>{const b=e.getBoundingClientRect();return {x:(b.x-origin.x)/sx,y:(b.y-origin.y)/sy,width:b.width/sx,height:b.height/sy}})()}));
 labels.push(...group);labelOutside.push(...group.filter(e=>e.bbox.x<0||e.bbox.y<0||e.bbox.x+e.bbox.width>vb.width||e.bbox.y+e.bbox.height>vb.height));
 for(let i=0;i<group.length;i++)for(let j=i+1;j<group.length;j++){const a=group[i].bbox,b=group[j].bbox;if(a.x<b.x+b.width&&a.x+a.width>b.x&&a.y<b.y+b.height&&a.y+a.height>b.y)collisions.push([svg.id,group[i].text,group[j].text]);}
}
const d=[...s.querySelectorAll('.definition')];const alignment=['h2','.meaning'].map(sel=>{const a=box(d[0].querySelector(sel)),b=box(d[1].querySelector(sel));return {selector:sel,yError:Math.abs(a.y-box(d[0]).y-b.y+box(d[1]).y),heightError:Math.abs(a.height-b.height)}});
const last=box(s.querySelector('.ref-takeaway'));
const charts=[...s.querySelectorAll('.loss-chart')].map(box);
const general=s.querySelector('#general-title').nextElementSibling;const gr=document.createRange();gr.selectNodeContents(general);const generalLineYs=[];for(const r of gr.getClientRects())if(r.width&&!generalLineYs.some(y=>Math.abs(y-r.y)<2))generalLineYs.push(r.y);const graph=s.querySelector('#overfit-chart'),sg=box(graph);const norm=e=>{const r=box(e);return {cx:(r.x+r.width/2-sg.x),top:r.y-sg.y,bottom:r.bottom-sg.y}};const yAxis=norm(s.querySelector('#overfit-y-title')),xAxis=norm(s.querySelector('#overfit-x-title'));
const axisAlignment={yCenterError:Math.abs(yAxis.cx-46),yGap:58-yAxis.bottom,xCenterError:Math.abs(xAxis.cx-202),xGap:xAxis.top-266};
return {axisAlignment,generalizationLines:generalLineYs.length,subtitle:s.querySelector('.subtitle').textContent,lossDefinitionInGraph:!!s.querySelector('.curve-panel .loss-definition'),charts,removedSubjects:s.querySelectorAll('.subject').length,removedGrid:s.querySelectorAll('.grid-lines').length,slide:sb,footer:fb,content:box(s.querySelector('.content')),outside,padding,clipped,labels,labelOutside,collisions,alignment,footerGap:fb.y-last.bottom,figureCaptionGap:last.y-box(s.querySelector('.loss-panel')).bottom,title:s.querySelector('h1').textContent};
}'''

def fonts(page,frame,selector):
    entries=frame.evaluate('''sel=>[...document.querySelectorAll(sel)].filter(e=>!e.matches('title,desc')&&e.getBoundingClientRect().width&&e.getBoundingClientRect().height&&[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())).map((e,i)=>{e.dataset.fontCheck=String(i);return {id:i,math:!!e.closest('.math-number'),spacing:getComputedStyle(e).letterSpacing}})''',selector)
    cdp=page.context.new_cdp_session(page);cdp.send('DOM.enable');cdp.send('CSS.enable')
    doc=find_document(cdp.send('DOM.getDocument',{'depth':-1,'pierce':True})['root'],frame.url)
    result=[]
    for e in entries:
        assert abs(float(e['spacing'].removesuffix('px'))+4/3)<.02,e
        node=cdp.send('DOM.querySelector',{'nodeId':doc['nodeId'],'selector':f'[data-font-check="{e["id"]}"]'})['nodeId']
        actual=cdp.send('CSS.getPlatformFontsForNode',{'nodeId':node})['fonts'];expected='STIX Two Math' if e['math'] else 'Pretendard Variable'
        assert actual and all(f['familyName']==expected and f['isCustomFont'] for f in actual),(e,actual,expected)
        result.append({'expected':expected,'actual':actual})
    cdp.detach();frame.evaluate("document.querySelectorAll('[data-font-check]').forEach(e=>e.removeAttribute('data-font-check'))")
    return {'text_nodes':len(entries),'letter_spacing':'-1pt','rendered':result}

def coordinates(frame,data):
    paths=frame.evaluate("()=>Object.fromEntries(['training','validation'].map(k=>[k,document.getElementById('overfit-'+k+'-line').getAttribute('d')]))")
    maxerr=0
    for k,path in paths.items():
        points=[(float(x),float(y)) for x,y in re.findall(r'[ML]([\d.eE+\-]+) ([\d.eE+\-]+)',path)]
        assert len(points)==len(data['points'])
        for (x,y),p in zip(points,data['points']):
            expected_x=(1-p['progress'])*46+p['progress']*358
            expected_y=(1-p[k]/1.2)*266+(p[k]/1.2)*58
            maxerr=max(maxerr,abs(x-expected_x),abs(y-expected_y))
    assert maxerr<1e-10,maxerr
    return {'point_pairs':len(data['points'])*2,'max_svg_coordinate_error':maxerr}


def diagram(frame):
    result=frame.evaluate("""()=>{
      const svg=document.querySelector('#generalization-diagram'),root=svg.getBoundingClientRect(),v=svg.viewBox.baseVal;
      const box=e=>{const r=e.getBoundingClientRect();return {x:(r.x-root.x)*v.width/root.width,y:(r.y-root.y)*v.height/root.height,width:r.width*v.width/root.width,height:r.height*v.height/root.height}};
      const q=id=>svg.querySelector('#'+id);
      return {ready:svg.dataset.ready,oldGraph:!!document.querySelector('#generalization-chart'),
        images:[...svg.querySelectorAll('[data-image-id]')].map(e=>({id:e.dataset.imageId,split:e.dataset.split,cls:e.dataset.class,signature:[...e.querySelectorAll('path,ellipse')].map(x=>x.outerHTML).join(''),box:box(e)})),
        predictions:[...svg.querySelectorAll('[data-prediction-for]')].map(e=>({for:e.dataset.predictionFor,cls:e.dataset.predictedClass,text:e.textContent})),
        models:[...svg.querySelectorAll('[data-model-ref]')].map(e=>({ref:e.dataset.modelRef,box:box(e)})),
        boxes:Object.fromEntries(['training-images','trained-model','new-images','applied-model','predictions'].map(id=>[id,box(q(id))])),
        flows:Object.fromEntries(['training-flow','prediction-input-flow','prediction-output-flow','model-transfer'].map(id=>[id,q(id).getAttribute('d')]))};
    }""")
    assert result['ready']=='true' and not result['oldGraph']
    training=[i for i in result['images'] if i['split']=='training'];new=[i for i in result['images'] if i['split']=='new']
    assert len(training)==3 and len(new)==2 and len({i['id'] for i in result['images']})==5
    assert [i['cls'] for i in training]==['사과','사과','토마토']
    assert {i['id']:i['cls'] for i in new}=={'new-A':'사과','new-B':'토마토'}
    assert all(i['signature'] not in {t['signature'] for t in training} for i in new)
    expected={'new-A':'사과','new-B':'토마토'};assert {p['for']:p['cls'] for p in result['predictions']}==expected
    assert all(p['cls'] in p['text'] for p in result['predictions'])
    assert [m['ref'] for m in result['models']]==['fruit-model','fruit-model']
    boxes=result['boxes']
    for id,src,dst in [('training-flow','training-images','trained-model'),('prediction-input-flow','new-images','applied-model'),('prediction-output-flow','applied-model','predictions')]:
        values=[float(x) for x in re.findall(r'-?\d+(?:\.\d+)?',result['flows'][id])];a,b=boxes[src],boxes[dst]
        assert abs(values[0]-(a['x']+a['width']+4))<.1 and abs(values[2]-(b['x']-4))<.1
        assert abs(a['y']+a['height']/2-b['y']-b['height']/2)<.1
        assert abs(values[1]-(b['y']+b['height']/2))<.1
        assert values[2]>values[0] and values[5:7]==[values[2],values[1]]
    assert result['flows']['model-transfer']
    return {'training_images':3,'unseen_images':2,'same_model':True,'semantic_predictions':expected,'inputs_are_distinct':True,'editable_svg':True,'inference_executed':False,'flow_alignment':True}

class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*a):pass
    def do_GET(self):
        if self.path=='/favicon.ico':self.send_response(204);self.end_headers();return
        super().do_GET()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--static',action='store_true');args=ap.parse_args()
    out=CASE/'previews';out.mkdir(exist_ok=True);evidence=CASE/'review/screens';evidence.mkdir(parents=True,exist_ok=True)
    data=json.loads((CASE/'curves.json').read_text());report={'status':'running','independent':independent(data),'cases':[],'created_utc':datetime.now(timezone.utc).isoformat()}
    if args.static: print(json.dumps(report['independent']));return
    server=None
    try:
        server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start()
        with sync_playwright() as p:
            browser=p.chromium.launch(**browser_options());report['chromium']=browser.version
            base=f'http://127.0.0.1:{server.server_port}/examples/overfitting-generalization/'
            parity=None
            for width,height in SIZES:
                for mode in ('scroll','slides'):
                    page=browser.new_page(viewport={'width':width,'height':height});errors=[];failed=[];http=[]
                    page.on('pageerror',lambda e:errors.append(str(e)));page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
                    page.on('requestfailed',lambda r:failed.append(r.url));page.on('response',lambda r:http.append([r.status,r.url]) if r.status>=400 else None)
                    page.goto(base+mode+'.html#concept',wait_until='networkidle');page.wait_for_function("document.body.dataset.ready==='true'")
                    frame=page.locator('iframe').element_handle().content_frame();frame.evaluate('document.fonts.ready')
                    screen=evidence/f'{mode}-{width}x{height}.png';page.screenshot(path=str(screen),full_page=True)
                    if width==1600:page.screenshot(path=str(out/('slide.png' if mode=='slides' else 'scroll.png')),full_page=True)
                    geometry=frame.evaluate(GEOMETRY);report['cases'].append({'mode':mode,'viewport':[width,height],'geometry':geometry,'evidence':str(screen.relative_to(ROOT))})
                    for key in ['outside','clipped','labelOutside','collisions']:assert not geometry[key],(mode,width,key,geometry[key])
                    assert all(not v['escaped'] for v in geometry['padding']),(mode,width,geometry['padding'])
                    assert all(v['yError']<.1 and v['heightError']<.1 for v in geometry['alignment'])
                    assert geometry['removedSubjects']==0 and geometry['removedGrid']==0
                    assert len(geometry['charts'])==1 and all(abs(c['width']-380)<.1 and abs(c['height']-320)<.1 for c in geometry['charts'])
                    assert abs(geometry['generalizationLines']-1)<.01 and geometry['lossDefinitionInGraph']
                    assert '손실' not in geometry['subtitle'] and '검증 데이터' not in geometry['subtitle']
                    ax=geometry['axisAlignment'];assert ax['yCenterError']<.1 and ax['xCenterError']<.1 and abs(ax['yGap']-8)<.1 and abs(ax['xGap']-8)<.1,ax
                    report['cases'][-1]['generalization']=diagram(frame)
                    visible=frame.locator('body').inner_text();assert '설명용 곡선' not in visible and '실험 결과 아님' not in visible
                    assert geometry['footerGap']>=12 and geometry['figureCaptionGap']>=13,geometry
                    report['cases'][-1]['fonts']=fonts(page,frame,'.slide *');report['cases'][-1]['viewer_fonts']=fonts(page,page,'nav *, .viewer-note')
                    report['cases'][-1]['coordinates']=coordinates(frame,data)
                    fingerprint=frame.evaluate(FINGERPRINT)
                    if parity is None:parity=fingerprint
                    report['cases'][-1]['mode_parity']=compare(fingerprint,parity)
                    outer=page.locator('.frame').evaluate('e=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y,right:r.right,bottom:r.bottom,width:r.width,height:r.height,overflow:document.documentElement.scrollWidth>innerWidth}}')
                    assert not outer['overflow'] and outer['x']>=0 and outer['right']<=width+1
                    if mode=='slides':assert outer['y']>=44 and outer['bottom']<=height-44
                    assert abs(outer['width']/outer['height']-16/9)<.001
                    assert not errors and not failed and not http,(errors,failed,http)
                    report['cases'][-1].update(outer=outer,page_errors=errors,failed_requests=failed,http_errors=http)
                    print('PASS',mode,width,height,flush=True);page.close()
            page=browser.new_page(viewport={'width':1600,'height':950});page.goto(base+'slides.html',wait_until='networkidle');page.wait_for_function("document.body.dataset.ready==='true'");frame=page.locator('iframe').element_handle().content_frame()
            changes=[]
            for kind in ('improving','crossing'):
                changed=json.loads(json.dumps(data));changed['interpretation']=kind
                for point in changed['points']:
                    u=point['progress'];point['training']=.8-.5*u;point['validation']=(.95-.5*u if kind=='improving' else .4+.15*u)
                frame.evaluate('(d)=>window.CurveExample.render(d)',changed);coordinates(frame,changed)
                expected='학습·검증 손실이 함께 감소' if kind=='improving' else '손실 격차만으로 판단하지 않기'
                assert expected in frame.locator('#overfit-heading').text_content()
                g=frame.evaluate(GEOMETRY)
                assert not any(g[k] for k in ('outside','clipped','labelOutside','collisions')) and all(not x['escaped'] for x in g['padding']) and g['footerGap']>=12
                page.screenshot(path=str(evidence/f'{kind}.png'));changes.append(kind)
            rejected=[]
            for kind in ('unit','nonfinite','unordered','negative'):
                changed=json.loads(json.dumps(data))
                if kind=='unit':changed['unit']='different'
                if kind=='nonfinite':changed['points'][1]['validation']=None
                if kind=='unordered':changed['points'][1]['progress']=0
                if kind=='negative':changed['points'][1]['training']=-.1
                result=frame.evaluate('(d)=>{try{window.CurveExample.render(d);return false}catch(e){return window.CurveExample.status==="error"&&[...document.querySelectorAll(".curve-artwork path")].every(p=>!p.hasAttribute("d"))}}',changed)
                assert result,kind;rejected.append(kind)
            page.close()
            # Real mode navigation, refresh, keyboard focus, and failed data load.
            page=browser.new_page();page.goto(base+'scroll.html');page.wait_for_function("document.body.dataset.ready==='true'")
            page.keyboard.press('Tab');assert page.locator('a[href="scroll.html#concept"]').evaluate('e=>e===document.activeElement')
            page.keyboard.press('Tab');page.keyboard.press('Enter');page.wait_for_url('**/slides.html#concept');page.wait_for_function("document.body.dataset.ready==='true'")
            page.reload();page.wait_for_function("document.body.dataset.ready==='true'");page.locator('a[href="scroll.html#concept"]').click();page.wait_for_url('**/scroll.html#concept')
            page.close()
            page=browser.new_page();page.route('**/curves.json',lambda r:r.fulfill(status=503,body='unavailable'));page.goto(base+'slides.html');page.wait_for_function("document.body.dataset.ready==='error'");f=page.locator('iframe').element_handle().content_frame();assert '표시 불가' in f.locator('#chart-status').inner_text();page.screenshot(path=str(evidence/'failure.png'));page.close()
            report['behavior']={'changed_datasets':changes,'rejected_datasets':rejected,'mode_roundtrip':True,'keyboard_links':True,'reload':True,'failed_data_message':True}
            browser.close();report['status']='passed'
    except Exception:
        report.update(status='blocked' if not server else 'failed',error=traceback.format_exc());raise
    finally:
        if server:server.shutdown();server.server_close()
        source=list(CASE.glob('*.html'))+list(CASE.glob('*.css'))+list(CASE.glob('*.js'))+[CASE/'curves.json',CASE/'DESIGN.md',Path(__file__),ROOT/'templates/html/graph-annotations.js']
        report['source_sha256']={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in source}
        report['preview_sha256']={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in out.glob('*.png')}
        (out/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('PASS overfitting: 8 PC screens, actual fonts, independent curves, parity and changed data')
if __name__=='__main__':main()
