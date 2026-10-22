"""Independent math, visible alignment and failure-path checks for #2 only."""
import math,re
from pathlib import Path
from reference_validation import GEOMETRY,actual_fonts

LAYOUT = '''() => {
 const box=e=>{const b=e.getBoundingClientRect();return {x:b.x,y:b.y,right:b.right,bottom:b.bottom,width:b.width,height:b.height,cx:b.x+b.width/2,cy:b.y+b.height/2}};
 const nodes=[...document.querySelectorAll('.flow > .node')];
 const cards=nodes.map(node=>{
  const figure=node.querySelector('.process-figure'),graphic=node.querySelector('[data-process-artwork]')||node.querySelector('.process-photo');
  const shape=box(graphic),f=box(figure),n=box(node),s=getComputedStyle(node),scale=n.width/parseFloat(s.width);
  return {stage:node.dataset.stage,card:n,label:box(node.querySelector('.node-step')),figure:f,artwork:shape,
   title:box(node.querySelector('.node-title')),description:box(node.querySelector('.node-desc')),
   background:s.backgroundColor,border:s.borderTopColor,borderWidth:s.borderTopWidth,
   cxError:Math.abs(shape.cx-f.cx),cyError:Math.abs(shape.cy-f.cy),
   paddingEscapes:shape.x<n.x+(parseFloat(s.paddingLeft)+parseFloat(s.borderLeftWidth))*scale-1||shape.right>n.right-(parseFloat(s.paddingRight)+parseFloat(s.borderRightWidth))*scale+1};
 });
 const arrows=[...document.querySelectorAll('.process-connector svg')].map(svg=>{
  const m=svg.getScreenCTM(),a=new DOMPoint(1,8).matrixTransform(m),b=new DOMPoint(27,8).matrixTransform(m);
  return {start:{x:a.x,y:a.y},end:{x:b.x,y:b.y},d:svg.querySelector('path').getAttribute('d'),stroke:getComputedStyle(svg.querySelector('path')).stroke};
 });
 const outputs=[...document.querySelectorAll('.output-item')].map(g=>({name:g.dataset.class,probability:Number(g.dataset.probability),text:g.querySelector('.probability-value').textContent,
  width:Number(g.querySelector('.probability-bar').getAttribute('width')),track:Number(g.querySelector('.probability-track').getAttribute('width')),highest:g.dataset.highest==='true',fill:getComputedStyle(g.querySelector('.probability-bar')).fill}));
 const maps=[...document.querySelectorAll('.process-feature-svg image')].map(e=>({channel:Number(e.dataset.channel),x:Number(e.getAttribute('x')),y:Number(e.getAttribute('y')),width:Number(e.getAttribute('width')),height:Number(e.getAttribute('height')),href:e.getAttribute('href')}));
 return {cards,arrows,outputs,exampleLogits:window.ProcessReference.exampleLogits,maps,
  photos:document.querySelectorAll('img').length,featureImages:document.querySelectorAll('.process-feature-svg image').length,
  figureNotes:[...document.querySelectorAll('.figure-note')].map(e=>e.textContent),
  captionLast:document.querySelector('.content').lastElementChild.classList.contains('ref-takeaway'),
  zoom:parseFloat(getComputedStyle(document.querySelector('.slide')).zoom)};
}'''

def check_process(page,width,logits=(2,1,0)):
    page.wait_for_function("window.ProcessReference?.status==='ready'")
    page.evaluate('document.fonts.ready')
    r=page.evaluate(LAYOUT)
    assert r['photos']==1 and r['featureImages']==4
    assert [c['stage'] for c in r['cards']]==['input','feature','task','output']
    assert page.locator('.node-step').all_text_contents()==['INPUT','FEATURE','TASK','OUTPUT']
    assert page.locator('.node-title').all_text_contents()==['입력 이미지','CNN','Task Head','예측 결과']
    descriptions=[' '.join(text.split()) for text in page.locator('.node-desc').all_inner_texts()]
    assert descriptions==['RGB 픽셀 데이터','이미지에서 특징 추출','특징을 목적에 맞게 처리','클래스별 예측 확률']
    assert page.locator('h1').inner_text()=='CNN의 예측 흐름'
    assert page.locator('.subtitle').inner_text()=='이미지 → 특징 추출 → 목적별 처리 → 예측 결과'
    assert r['captionLast']
    assert r['figureNotes']==['예시 확률']
    assert page.locator('[data-stage="feature"] figcaption').count()==0
    assert '고정 필터' in page.locator('.process-feature-svg').get_attribute('aria-label')
    assert '학습된 모델의 추론 결과가 아님' in page.locator('.process-feature-svg').get_attribute('aria-label')
    assert page.locator('.process-task-svg text').all_text_contents()==['분류 처리']
    assert page.locator('.process-task-svg rect').count()==1 and page.locator('.process-task-svg circle').count()==0
    assert page.locator('[data-example-score]').count()==0
    assert page.locator('.ref-takeaway span').inner_text()=='CNN은 이미지에서 특징을 추출하고, Task Head는 이를 목적에 맞는 예측으로 변환'
    assert page.locator('.feature-fallback').is_hidden()
    assert page.locator('.process-feature-svg').get_attribute('data-image-derived')=='true'
    assert page.evaluate('window.CNNFeatureMaps.width')==64
    assert page.evaluate('window.ProcessReference.trainedInference') is False
    assert r['exampleLogits']==list(logits)
    for c in r['cards']:
        highlighted=c['stage']=='feature'
        assert c['background']==('rgb(234, 241, 255)' if highlighted else 'rgb(255, 255, 255)'),c
        assert c['border']==('rgb(49, 104, 200)' if highlighted else 'rgb(221, 228, 239)'),c
        assert float(c['borderWidth'].removesuffix('px'))>0,c
    # Chromium snaps borders to device pixels under CSS zoom; compare all four
    # rendered widths instead of requiring an unsnapped CSS declaration value.
    borders=[float(c['borderWidth'].removesuffix('px')) for c in r['cards']]
    assert max(borders)-min(borders)<.01,borders
    assert [m['channel'] for m in r['maps']]==[9,6,3,0]
    assert len({m['href'] for m in r['maps']})==4,'Representative channels must have distinct computed patterns'
    for i,m in enumerate(r['maps']):
        assert m['width']==m['height']==116
        if i:
            assert m['x']==r['maps'][i-1]['x']-15 and m['y']==r['maps'][i-1]['y']+10
        m.pop('href')  # Do not embed image bytes in the validation report.
    exp=[math.exp(v-max(logits)) for v in logits];expected=[v/sum(exp) for v in exp]
    assert [o['name'] for o in r['outputs']]==['사과','토마토','기타']
    for o,p,z in zip(r['outputs'],expected,logits):
        assert abs(o['probability']-p)<1e-12 and abs(o['width']/o['track']-p)<1e-12,o
        assert o['text']==f'{p*100:.1f}%' and o['highest']==(z==max(logits))
        if o['highest']:assert o['fill']=='rgb(38, 166, 161)'
    assert abs(sum(o['probability'] for o in r['outputs'])-1)<1e-12
    assert abs(sum(float(o['text'][:-1]) for o in r['outputs'])-100)<1e-9
    for c in r['cards']:
        assert c['cxError']<1 and c['cyError']<1 and not c['paddingEscapes'],c
    heights=[c['card']['height'] for c in r['cards']];assert max(heights)-min(heights)<1
    for key in ['label','figure','title','description']:
        offsets=[c[key]['y']-c['card']['y'] for c in r['cards']]
        assert max(offsets)-min(offsets)<1,(key,'relative card alignment',offsets)
    if width>900:
        for key in ['card','label','title','description']:
            ys=[c[key]['y'] for c in r['cards']];assert max(ys)-min(ys)<1,(key,ys)
        ys=[c['artwork']['cy'] for c in r['cards']];assert max(ys)-min(ys)<1,ys
    for i,a in enumerate(r['arrows']):
        assert list(map(float,re.findall(r'-?\d+(?:\.\d+)?',a['d'])))==[1,8,27,21,2,27,8,21,14]
        assert a['stroke']=='rgb(49, 104, 200)'
        before,after=r['cards'][i],r['cards'][i+1]
        if width>900:
            assert before['card']['right']<a['start']['x']<a['end']['x']<after['card']['x']
            assert max(abs(a['start']['y']-before['artwork']['cy']),abs(a['end']['y']-after['artwork']['cy']))<1,a
        else:
            assert before['card']['bottom']<a['start']['y']<a['end']['y']<after['card']['y'],a
            assert max(abs(a['start']['x']-before['card']['cx']),abs(a['end']['x']-after['card']['cx']))<1,a
    assert len(r['arrows'])==3 and page.locator('.process-task-svg .internal-arrow').count()==2
    face=page.locator('.process-feature-svg image').last.bounding_box()
    assert face['width']/r['zoom']>=(90 if width>900 else 80)
    return {**r,'independent_softmax':expected,'displayed_total_percent':100.0,'four_computed_maps':True}


def check_process_robustness(browser,base_url,evidence_dir):
    """Fresh contexts isolate deliberate failures from the normal error gate."""
    root=Path(__file__).resolve().parents[1];results=[]
    for width,height in [(1600,950),(390,844)]:
        for scenario in ['no_javascript','engine_unavailable','presentation_unavailable','photo_unavailable','canvas_unavailable','changed_logits']:
            context=browser.new_context(viewport={'width':width,'height':height},java_script_enabled=scenario!='no_javascript')
            page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
            if scenario in ('engine_unavailable','presentation_unavailable'):
                name='assets/cnn-feature-maps.js' if scenario=='engine_unavailable' else 'process-reference.js'
                page.route('**/'+name,lambda route:route.fulfill(status=404,body='',content_type='application/javascript'))
            elif scenario=='photo_unavailable':
                page.route('**/concept-apple-photo.jpg',lambda route:route.fulfill(status=404,body=''))
            elif scenario=='canvas_unavailable':
                page.add_init_script('HTMLCanvasElement.prototype.getContext=()=>null')
            elif scenario=='changed_logits':
                original=(root/'templates/html/process-reference.js').read_text()
                changed=original.replace('const logits = [2, 1, 0];','const logits = [1, 2, 0];')
                assert changed!=original
                page.route('**/process-reference.js',lambda route:route.fulfill(body=changed,content_type='application/javascript'))
            try:
                page.goto(base_url+'/templates/html/process.html',wait_until='networkidle');page.evaluate('document.fonts.ready')
                if scenario in ('engine_unavailable','photo_unavailable','canvas_unavailable'):
                    page.wait_for_function("window.ProcessReference?.status==='error'")
                if scenario=='changed_logits':
                    detail=check_process(page,width,(1,2,0));assert detail['outputs'][1]['highest']
                else:
                    assert page.locator('.feature-fallback').is_visible(),scenario
                    assert page.locator('.feature-fallback').inner_text().strip()
                    assert page.locator('.process-task-svg').is_visible() and page.locator('.process-output-svg').is_visible()
                    assert page.locator('.probability-value').all_text_contents()==['66.5%','24.5%','9.0%']
                    if scenario=='photo_unavailable':assert page.locator('.photo-fallback').is_visible()
                    detail={'visible_feature_fallback':page.locator('.feature-fallback').inner_text(),'task_and_output_retained':True}
                fonts=actual_fonts(page);assert not fonts['fallback'] and not fonts['unpainted'] and not fonts['bad_spacing']
                geometry=page.evaluate(GEOMETRY)
                for key in ['outside','overflow','footerOverlap','spacing','clippedText','arrowErrors']:assert not geometry[key],(scenario,width,key,geometry[key])
                assert geometry['pageWidth']<=width and not errors,(scenario,width,errors)
                page.locator('.slide').screenshot(path=str(evidence_dir/f'process-{scenario}-{width}.png'),animations='disabled')
                results.append({'scenario':scenario,'viewport':[width,height],'passed':True,'detail':detail,'actual_font_families':fonts['families']})
            finally:context.close()
    return results
