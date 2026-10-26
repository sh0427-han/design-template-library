/* The graph and image prediction scene are conceptual, not measured results. */
(() => {
  'use strict';
  const headings={divergence:'검증 손실 최소에서 모델 선택',improving:'학습·검증 손실이 함께 감소',crossing:'손실 격차만으로 판단하지 않기'};
  function validate(data) {
    if(data.kind!=='schematic'||data.metric!=='mean_squared_error'||data.unit!=='dimensionless'||data.aggregation!=='sample_mean'||data.regularization!==false||data.evaluation!=='same_inference_mode'||JSON.stringify(data.xDomain)!=='[0,1]'||JSON.stringify(data.yDomain)!=='[0,1.2]') throw new Error('Invalid comparison conditions');
    if(!Object.hasOwn(headings,data.interpretation)||!Array.isArray(data.points)||data.points.length<2) throw new Error('Invalid curve');
    let previous=-Infinity;
    for(const p of data.points){
      if(!['progress','training','validation'].every(k=>typeof p[k]==='number'&&Number.isFinite(p[k]))||p.progress<0||p.progress>1||p.progress<=previous||p.training<0||p.training>1.2||p.validation<0||p.validation>1.2)throw new Error('Invalid point');
      previous=p.progress;
    }
  }
  function annotateSelection(data) {
    const q=id=>document.getElementById(id),points=data.points;
    const index=points.reduce((best,p,i)=>p.validation<points[best].validation?i:best,0);
    const best=points[index],x=46+best.progress*312,y=266-best.validation/1.2*208;
    const labelX=Math.max(107,Math.min(310,x-48));
    q('best-point').setAttribute('cx',x);q('best-point').setAttribute('cy',y);
    q('best-guide').setAttribute('d',`M${x} 58 V266`);
    for(const id of ['best-label','best-description'])q(id).setAttribute('x',labelX);
    // The label stays in the empty upper plot; the leader ends at the selected point.
    q('best-leader').setAttribute('d',`M${labelX} 128 H${x} V${y-8}`);
    const overfitting=data.interpretation==='divergence'&&index>0&&index<points.length-1&&points.slice(index+1).every((p,j)=>p.validation>points[index+j].validation&&p.training<points[index+j].training);
    q('overfit-region').setAttribute('x',x);q('overfit-region').setAttribute('width',358-x);
    for(const id of ['best-selection','best-guide'])q(id).removeAttribute('hidden');
    for(const id of ['overfit-region','overfit-annotation'])q(id).toggleAttribute('hidden',!overfitting);
    q('overfit-chart').dataset.bestIndex=String(index);q('overfit-chart').dataset.overfitting=String(overfitting);
  }
  function layoutDiagram() {
    const svg=document.querySelector('#generalization-diagram');
    const q=id=>svg.querySelector('#'+id);
    for(const [id,center] of [['training-images',84],['new-images',252],['predictions',252]]){
      const g=q(id);g.removeAttribute('transform');const b=g.getBBox();g.setAttribute('transform',`translate(0 ${center-b.y-b.height/2})`);
    }
    for(const id of ['trained-model','applied-model']){
      const g=q(id),r=g.querySelector('rect'),t=g.querySelector('text');t.removeAttribute('transform');const b=t.getBBox();
      t.setAttribute('transform',`translate(${Number(r.getAttribute('x'))+Number(r.getAttribute('width'))/2-b.x-b.width/2} ${Number(r.getAttribute('y'))+Number(r.getAttribute('height'))/2-b.y-b.height/2})`);
    }
    const box=e=>window.GraphAnnotations.bounds(svg,e),centerY=b=>b.y+b.height/2;
    const arrow=(id,from,to,y)=>q(id).setAttribute('d',`M${from} ${y} H${to} M${to-6} ${y-5} L${to} ${y} L${to-6} ${y+5}`);
    const training=box(q('training-images')),trained=box(q('trained-model')),inputs=box(q('new-images')),model=box(q('applied-model')),outputs=box(q('predictions'));
    arrow('training-flow',training.x+training.width+4,trained.x-4,centerY(trained));
    arrow('prediction-input-flow',inputs.x+inputs.width+4,model.x-4,centerY(model));
    arrow('prediction-output-flow',model.x+model.width+4,outputs.x-4,centerY(model));
    const x1=trained.x+trained.width/2,y1=trained.y+trained.height+4,x2=model.x+model.width/2,y2=model.y-4;
    q('model-transfer').setAttribute('d',`M${x1} ${y1} V160 H${x2} V${y2} M${x2-4} ${y2-6} L${x2} ${y2} L${x2+4} ${y2-6}`);
    svg.dataset.ready='true';
  }
  function render(data) {
    validate(data);
    for(const series of ['training','validation'])document.querySelector(`#overfit-${series}-line`).setAttribute('d',data.points.map((p,i)=>`${i?'L':'M'}${46+p.progress*312} ${266-p[series]/1.2*208}`).join(' '));
    annotateSelection(data);
    document.querySelector('#overfit-heading').textContent=headings[data.interpretation];
    document.querySelector('#overfit-chart-title').textContent=headings[data.interpretation];
    document.querySelector('#overfit-chart-desc').textContent=(data.interpretation==='divergence'?'초기 두 손실이 함께 감소한 뒤 검증 손실 최소 지점의 모델을 선택하고, 이후 학습 손실은 감소하지만 검증 손실이 상승하는 과적합 구간을 강조.':data.interpretation==='improving'?'학습 손실과 검증 손실이 함께 감소하는 경우.':'두 손실이 교차하는 경우. 격차만으로 과적합을 확정하지 않음.')+' Best model은 표시된 학습 시점들 중 검증 손실 기준 선택이며 독립 테스트 성능의 최적을 보장하지 않음. 직접 작성한 설명용 개념도이며 실측 결과가 아님.';
    window.GraphAnnotations.alignAxes({svg:document.querySelector('#overfit-chart'),yLabel:document.querySelector('#overfit-y-title'),xLabel:document.querySelector('#overfit-x-title'),left:46,right:358,top:58,bottom:266});
    document.querySelector('#chart-status').hidden=true;window.CurveExample.data=structuredClone(data);window.CurveExample.status='ready';
  }
  function fail() {
    document.querySelectorAll('.curve-artwork path').forEach(p=>p.removeAttribute('d'));
    for(const id of ['best-selection','best-guide','overfit-region','overfit-annotation'])document.getElementById(id).setAttribute('hidden','');
    delete document.querySelector('#overfit-chart').dataset.bestIndex;delete document.querySelector('#overfit-chart').dataset.overfitting;
    const s=document.querySelector('#chart-status');s.hidden=false;s.textContent='곡선 표시 불가 · 데이터를 확인하세요.';
    document.querySelector('#overfit-heading').textContent='곡선 데이터를 읽지 못함';
    document.querySelector('#overfit-chart-desc').textContent='데이터 오류로 곡선을 표시하지 못함';window.CurveExample.status='error';
  }
  window.CurveExample={status:'loading',render(data){try{render(data);}catch(e){fail();throw e;}}};
  async function start(){
    await Promise.all([document.fonts.load('400 17px "STIX Two Math"','0'),document.fonts.load('750 20px "Pretendard Variable"','학습 예측')]);await document.fonts.ready;
    layoutDiagram();const r=await fetch('curves.json');if(!r.ok)throw new Error('Curve load failed');render(await r.json());
  }
  start().catch(fail);
})();
