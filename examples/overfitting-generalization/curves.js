/* These are schematic data, never a model-training implementation. */
(() => {
  'use strict';
  const interpretation = {
    divergence: '검증 손실의 상승·격차 확대는<br><b>과적합을 살펴보는 단서</b>',
    improving: '두 손실이 함께 감소하는 예시<br><b>학습 손실 감소가 과적합을 뜻하지 않음</b>',
    crossing: '손실의 높낮이가 바뀌는 예시<br><b>격차만으로 과적합을 확정하지 않음</b>'
  };
  function render(data) {
    if (data.kind !== 'schematic' || data.metric !== 'mean_squared_error' || data.unit !== 'dimensionless' ||
        data.aggregation !== 'sample_mean' || data.regularization !== false || data.evaluation !== 'same_inference_mode' ||
        JSON.stringify(data.xDomain) !== '[0,1]' || JSON.stringify(data.yDomain) !== '[0,1.2]' ||
        !Object.hasOwn(interpretation, data.interpretation) || !Array.isArray(data.points) || data.points.length < 2) throw new Error('Invalid comparison conditions');
    let previous = -Infinity;
    for (const point of data.points) {
      if (!['progress','training','validation'].every(k => typeof point[k] === 'number' && Number.isFinite(point[k])) ||
          point.progress < 0 || point.progress > 1 || point.progress <= previous ||
          point.training < 0 || point.training > 1.2 || point.validation < 0 || point.validation > 1.2) throw new Error('Invalid curve point');
      previous = point.progress;
    }
    for (const series of ['training','validation']) {
      const path = data.points.map((p,i) => `${i ? 'L' : 'M'}${62 + p.progress * 660} ${120 - p[series] / 1.2 * 104}`).join(' ');
      document.querySelector(`#${series}-line`).setAttribute('d', path);
    }
    document.querySelector('#interpretation').innerHTML = interpretation[data.interpretation];
    document.querySelector('#chart-desc').textContent = data.interpretation === 'divergence'
      ? '초기에는 두 손실이 함께 감소. 후반에는 학습 손실 감소와 검증 손실 상승으로 격차 확대. 과적합의 단서이며 확정 판정이나 독립 테스트 결과가 아님.'
      : data.interpretation === 'improving' ? '두 손실이 함께 감소하는 설명용 예시. 학습 손실 감소만으로 과적합을 판단하지 않음.' : '두 손실이 교차하는 설명용 예시. 손실 격차만으로 과적합을 확정하지 않음.';
    document.querySelector('#chart-status').hidden = true;
    window.CurveExample.data = structuredClone(data);
    window.CurveExample.status = 'ready';
  }
  function fail(error) {
    document.querySelectorAll('#curve-artwork path').forEach(p => p.removeAttribute('d'));
    const status = document.querySelector('#chart-status');
    status.hidden = false; status.textContent = '곡선 표시 불가 · 올바른 설명용 데이터를 확인하세요.';
    document.querySelector('#interpretation').textContent = '곡선 데이터를 읽지 못해 변화 해석을 표시하지 않음';
    document.querySelector('#chart-desc').textContent = '데이터 오류로 손실 곡선을 표시하지 못함';
    window.CurveExample.status = 'error';
  }
  window.CurveExample = {status:'loading', render(data) {try {render(data);} catch(e) {fail(e);throw e;}}};
  fetch('curves.json').then(r => {if(!r.ok) throw new Error('Curve load failed');return r.json();}).then(render).catch(fail);
})();
