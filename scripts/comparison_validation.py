"""Check #3's preparation/application meaning, matching rows and live geometry."""
import math,re
from reference_validation import GEOMETRY

LAYOUT = r'''() => {
 const box=e=>{const b=e.getBoundingClientRect();return {x:b.x,y:b.y,right:b.right,bottom:b.bottom,width:b.width,height:b.height,cx:b.x+b.width/2,cy:b.y+b.height/2}};
 const union=es=>{const bs=es.map(box);const x=Math.min(...bs.map(b=>b.x)),r=Math.max(...bs.map(b=>b.right));return {left:x,right:r,cx:(x+r)/2}};
 const cards=[...document.querySelectorAll('.compare-card')].map(card=>{
  const prep=card.querySelector('.phase-prepare'),predict=card.querySelector('.phase-predict');
  const photo=card.querySelector('.inference-photo'),system=card.querySelector('[data-inference-system]'),result=card.querySelector('.inference-result');
  const transfer=card.querySelector('.system-transfer'),d=transfer.querySelector('path').getAttribute('d');
  const rows=[...card.querySelectorAll('[data-center-row]')].map(row=>({
   box:box(row.parentElement),art:union([...row.querySelectorAll('[data-visual-bound]')].filter(e=>e.getBoundingClientRect().width))
  }));
  const arrows=[...predict.querySelectorAll('.comparison-arrow')].map(svg=>{
   const m=svg.getScreenCTM(),a=new DOMPoint(1,8).matrixTransform(m),b=new DOMPoint(30,8).matrixTransform(m);
   return {a:{x:a.x,y:a.y},b:{x:b.x,y:b.y},stroke:getComputedStyle(svg.querySelector('path')).stroke,d:svg.querySelector('path').getAttribute('d')};
  });
  return {method:card.dataset.method,box:box(card),background:getComputedStyle(card).backgroundColor,
   heading:box(card.querySelector('.comparison-heading')),label:box(card.querySelector('.pill')),
   scale:card.getBoundingClientRect().width/card.offsetWidth,
   title:box(card.querySelector('h2')),intro:box(card.querySelector('.comparison-heading p')),
   prep:box(prep),predict:box(predict),prepLabel:box(prep.querySelector('h3')),predictLabel:box(predict.querySelector('h3')),
   photo:box(photo),photoSource:photo.getAttribute('src'),photoLoaded:photo.complete&&photo.naturalWidth>0,
   prepared:box(card.querySelector('[data-prepared-system]')),system:box(system),result:box(result),
   resultText:result.innerText,rows,arrows,
   transfer:{d,stroke:getComputedStyle(transfer.querySelector('path')).stroke,matrix:[transfer.getScreenCTM().a,transfer.getScreenCTM().b,transfer.getScreenCTM().c,transfer.getScreenCTM().d,transfer.getScreenCTM().e,transfer.getScreenCTM().f]},
   phaseLabels:[...card.querySelectorAll('.phase-heading')].flatMap(e=>[box(e.querySelector('h3')),box(e.querySelector('span'))]),
   criteria:[...card.querySelectorAll('.compare-criteria > div')].map(e=>({box:box(e),label:e.querySelector('dt').textContent,text:e.querySelector('dd').textContent,body:box(e.querySelector('dd'))})),
   foot:[...card.querySelectorAll('.compare-foot p')].map(e=>({box:box(e),label:e.querySelector('b').textContent,body:box(e.querySelector('span'))}))
  };
 });
 const maps=[...document.querySelectorAll('.compare-feature-svg image')].map(e=>({channel:Number(e.dataset.channel),x:Number(e.getAttribute('x')),y:Number(e.getAttribute('y'))}));
 return {cards,maps,state:window.ComparisonReference,sampleLabels:[...document.querySelectorAll('.training-sample > span')].map(e=>e.textContent),
  sampleClasses:[...document.querySelectorAll('.training-sample')].map(e=>e.dataset.class),
  samplePatterns:[...document.querySelectorAll('.training-sample svg')].map(e=>e.innerHTML),
  photoCount:document.querySelectorAll('img').length,trainingPhotos:document.querySelectorAll('.training-data img,.training-data image').length};
}'''

def check_comparison(page,width,photo_source='assets/concept-apple-photo.jpg'):
    page.wait_for_function("window.ComparisonReference?.status==='ready'")
    page.evaluate('document.fonts.ready')
    r=page.evaluate(LAYOUT)
    assert r['state']['supervisedExample'] and not r['state']['ruleEngineExecuted'] and not r['state']['modelInferenceExecuted']
    assert r['state']['mapSource']=='fixed_directional_filters'
    assert [c['method'] for c in r['cards']]==['rule','ml']
    assert r['sampleLabels']==r['sampleClasses']==['사과','사과','토마토']
    assert len(set(r['samplePatterns']))==3 and r['trainingPhotos']==0
    r.pop('samplePatterns')
    assert r['photoCount']==2
    assert [m['channel'] for m in r['maps']]==[9,6,3,0]
    for a,b in zip(r['maps'],r['maps'][1:]):assert a['x']-b['x']==11 and b['y']-a['y']==8
    assert page.locator('.phase-heading h3').all_text_contents()==['01 준비','02 예측']*2
    assert page.locator('.comparison-heading h2').all_text_contents()==['사람이 규칙을 정의','데이터에서 판단 기준을 학습']
    assert page.locator('.rule-conditions small').all_text_contents()==['색상','형태']
    assert page.locator('.rule-conditions span').all_text_contents()==['붉은색 영역','둥근 윤곽']
    assert '일러스트 예시' in page.locator('[data-method="ml"] .phase-prepare').inner_text()
    assert '고정 필터 설명용' in page.locator('[data-method="ml"] .phase-predict').inner_text()
    assert '학습된 모델의 실측 활성화가 아님' in page.locator('.compare-feature-svg').get_attribute('aria-label')
    assert page.locator('.map-fallback').is_hidden()
    assert page.locator('h1').inner_text()=='규칙 기반과 머신러닝'
    left,right=r['cards']
    assert left['photoSource']==right['photoSource']==photo_source
    if photo_source.startswith('data:'):
        left['photoSource']=right['photoSource']='embedded concept-apple-photo.jpg'
    assert left['resultText'].split()==['사과','판정','예시'] and right['resultText'].split()==['사과','예측','예시']
    expected=[
     ['개발자가 조건 직접 정의','규칙·임계값 수정','조건을 명확히 정의할 수 있는 환경'],
     ['학습 데이터로 모델 파라미터 추정','데이터·학습 설정 보완 후 재학습','대표성 있는 데이터와 성능 검증 필요']]
    for c,texts in zip(r['cards'],expected):
        assert c['background']=='rgb(255, 255, 255)' and c['photoLoaded']
        assert [d['label'] for d in c['criteria']]==['판단 기준','기준 변경','적용 조건']
        assert [d['text'] for d in c['criteria']]==texts
        assert [d['label'] for d in c['foot']]==['장점','한계']
        # Separate the method label, title and introduction, including at zoom.
        gaps=[(c['title']['y']-c['label']['bottom'])/c['scale'],
              (c['intro']['y']-c['title']['bottom'])/c['scale']]
        assert min(gaps)>=7.5,(width,c['method'],'crowded heading',gaps)
        assert c['heading']['y']<=c['label']['y'] and c['intro']['bottom']<=c['heading']['bottom']+0.5
        section_gap=(c['prep']['y']-c['intro']['bottom'])/c['scale']
        assert section_gap>=15.5,(width,c['method'],'preparation crowds introduction',section_gap)
        assert c['prep']['bottom']<c['predict']['y']
        for row in c['rows']:
            assert abs(row['art']['cx']-row['box']['cx'])<1,(width,c['method'],'actual figure center',row)
            assert row['art']['left']>=c['box']['x']+10 and row['art']['right']<=c['box']['right']-10,(width,c['method'],'figure escapes card',row)
        for a in c['arrows']:
            assert a['stroke']=='rgb(49, 104, 200)' and a['a']['x']<a['b']['x']
            assert abs(a['a']['y']-c['photo']['cy'])<1 and abs(a['b']['y']-c['system']['cy'])<1,(width,'flow axis',c)
        # Arrow shaft and head meet at the same tip; connector remains between nodes.
        first,last=c['arrows']
        assert c['photo']['right']<first['a']['x']<first['b']['x']<c['system']['x'],(width,'input connector overlap',c)
        assert c['system']['right']<last['a']['x']<last['b']['x']<c['result']['x'],(width,'output connector overlap',c)
        assert c['transfer']['stroke']=='rgb(38, 166, 161)'
        numbers=list(map(float,re.findall(r'-?\d+(?:\.\d+)?',c['transfer']['d'])))
        assert len(numbers)==11 and all(math.isfinite(v) for v in numbers),numbers
        # Parse points explicitly: M x1 y1 V bus H x2 V tipY M hx hy L tx ty L rx ry.
        x1,y1,bus,x2,y2,hx,hy,tx,ty,rx,ry=numbers
        assert (tx,ty)==(x2,y2) and hx<x2<rx and hy==ry<y2
        m11,m12,m21,m22,dx,dy=c['transfer']['matrix']
        point=lambda x,y:(m11*x+m21*y+dx,m12*x+m22*y+dy)
        start=point(x1,y1);tip=point(x2,y2);bus_point=point(x2,bus)
        assert abs(start[0]-c['prepared']['cx'])<1 and 0<start[1]-c['prepared']['bottom']<7
        assert abs(tip[0]-c['system']['cx'])<1 and 0<c['system']['y']-tip[1]<8
        assert c['prep']['bottom']<=bus_point[1]<=c['predict']['y']
        for label in c['phaseLabels']:
            assert not (label['x']<tip[0]<label['right'] and label['y']<tip[1] and label['bottom']>bus_point[1]),(width,'transfer crosses phase label',label)
    for key in ['width','height']:assert abs(left['box'][key]-right['box'][key])<1,(width,'card size',key)
    for key in ['label','title','intro','prep','predict','prepLabel','predictLabel','photo','result']:
        assert abs((left[key]['y']-left['box']['y'])-(right[key]['y']-right['box']['y']))<1,(width,'matching vertical offsets',key)
    assert abs(left['photo']['width']-right['photo']['width'])<1
    for ca,cb in zip(left['criteria'],right['criteria']):
        assert abs(ca['box']['height']-cb['box']['height'])<1
        assert abs((ca['box']['y']-left['box']['y'])-(cb['box']['y']-right['box']['y']))<1
        assert abs((ca['body']['x']-left['box']['x'])-(cb['body']['x']-right['box']['x']))<1
    for fa,fb in zip(left['foot'],right['foot']):assert abs((fa['box']['y']-left['box']['y'])-(fb['box']['y']-right['box']['y']))<1
    if width>900:assert left['box']['right']<right['box']['x'] and abs(left['box']['y']-right['box']['y'])<1
    else:assert left['box']['bottom']<right['box']['y']
    return r

def check_comparison_resize(browser,base_url):
    """Same document, loaded maps/font: reflow transfers without a page reload."""
    page=browser.new_page(viewport={'width':1600,'height':950});result=[]
    try:
        page.goto(base_url+'/templates/html/comparison.html',wait_until='networkidle')
        page.wait_for_function("window.ComparisonReference?.status==='ready'")
        for width,height in [(390,844),(600,900),(900,900),(1280,720),(1600,950)]:
            page.set_viewport_size({'width':width,'height':height})
            page.evaluate('async()=>{await document.fonts.ready;await new Promise(r=>requestAnimationFrame(r));await new Promise(r=>requestAnimationFrame(r));}')
            check_comparison(page,width)
            geometry=page.evaluate(GEOMETRY)
            for key in ['outside','overflow','footerOverlap','spacing','clippedText','arrowErrors']:
                assert not geometry[key],('live resize',width,key,geometry[key])
            assert geometry['pageWidth']<=width
            result.append({'viewport':[width,height],'passed':True})
    finally:page.close()
    return result
