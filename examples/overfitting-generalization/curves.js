/* Conceptual scenarios, not a model-training implementation or measured study. */
(() => {
  'use strict';
  const headings={divergence:'검증 손실 상승은 과적합의 단서',improving:'새 데이터에서도 낮은 손실',crossing:'손실 격차만으로 판단하지 않기'};
  function validateScenario(scenario) {
    if (!scenario || !Object.hasOwn(headings,scenario.interpretation) || !Array.isArray(scenario.points) || scenario.points.length<2) throw new Error('Invalid scenario');
    let previous=-Infinity;
    for(const p of scenario.points) {
      if(!['progress','training','validation'].every(k=>typeof p[k]==='number'&&Number.isFinite(p[k])) || p.progress<0 || p.progress>1 || p.progress<=previous || p.training<0 || p.training>1.2 || p.validation<0 || p.validation>1.2) throw new Error('Invalid point');
      previous=p.progress;
    }
  }
  function render(data) {
    if(data.kind!=='schematic'||data.metric!=='mean_squared_error'||data.unit!=='dimensionless'||data.aggregation!=='sample_mean'||data.regularization!==false||data.evaluation!=='same_inference_mode'||JSON.stringify(data.xDomain)!=='[0,1]'||JSON.stringify(data.yDomain)!=='[0,1.2]') throw new Error('Invalid comparison conditions');
    validateScenario(data);validateScenario(data.generalization);
    for(const [key,scenario] of [['overfit',data],['generalization',data.generalization]]) {
      for(const series of ['training','validation']) document.querySelector(`#${key}-${series}-line`).setAttribute('d',scenario.points.map((p,i)=>`${i?'L':'M'}${46+p.progress*312} ${266-p[series]/1.2*208}`).join(' '));
      document.querySelector(`#${key}-heading`).textContent=headings[scenario.interpretation];
      document.querySelector(`#${key}-chart-title`).textContent=headings[scenario.interpretation];
      document.querySelector(`#${key}-chart-desc`).textContent= (scenario.interpretation==='divergence'?'초기 두 손실이 함께 감소한 뒤 검증 손실 상승. 과적합의 단서이며 격차만으로 확정하지 않음.':scenario.interpretation==='improving'?'학습에 쓰지 않은 데이터의 검증 손실도 낮아지는 경우. 검증은 일반화 성능의 추정이며 독립 테스트 결과가 아님.':'두 손실이 교차하는 경우. 격차만으로 과적합을 확정하지 않음.')+' 직접 작성한 설명용 개념도이며 실측 결과가 아님.';
    }
    document.querySelector('#chart-status').hidden=true;
    window.CurveExample.data=structuredClone(data);window.CurveExample.status='ready';
  }
  function fail() {
    document.querySelectorAll('.curve-artwork path').forEach(p=>p.removeAttribute('d'));
    const s=document.querySelector('#chart-status');s.hidden=false;s.textContent='곡선 표시 불가 · 데이터를 확인하세요.';
    document.querySelectorAll('.case-heading').forEach(e=>e.textContent='곡선 데이터를 읽지 못함');
    document.querySelectorAll('svg desc').forEach(e=>e.textContent='데이터 오류로 곡선을 표시하지 못함');
    window.CurveExample.status='error';
  }
  window.CurveExample={status:'loading',render(data){try{render(data);}catch(e){fail();throw e;}}};
  fetch('curves.json').then(r=>{if(!r.ok)throw new Error('Curve load failed');return r.json();}).then(render).catch(fail);
})();
