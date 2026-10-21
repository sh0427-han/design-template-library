/* One threshold drives sample predictions, counts and displayed substitutions. */
(() => {
  const samples = [
    {score:0.15,truth:0}, {score:0.32,truth:1},
    {score:0.48,truth:0}, {score:0.67,truth:1},
    {score:0.82,truth:1}, {score:0.94,truth:0},
  ];
  const slider = document.getElementById('threshold');
  const readout = document.getElementById('threshold-value');
  const list = document.getElementById('score-list');
  const positives = samples.filter(item => item.truth === 1).length;
  document.getElementById('sample-note').textContent=`예시 ${samples.length}개 · 양성: 이상`;
  document.getElementById('live-context').textContent=`실제 정상 ${samples.length-positives}개 · 실제 이상 ${positives}개`;
  const pct = (n,d) => d ? (100*n/d).toFixed(1)+'%' : '정의 불가';
  function update() {
    const threshold = Number(slider.value)/100;
    readout.textContent = threshold.toFixed(2);
    slider.setAttribute('aria-valuetext', `${threshold.toFixed(2)}, 이 점수 이상이면 이상으로 예측`);
    const counts = {tp:0,tn:0,fp:0,fn:0};
    list.innerHTML = '';
    samples.forEach((item,index) => {
      const prediction = Number(item.score >= threshold);
      const type = item.truth ? (prediction ? 'TP' : 'FN') : (prediction ? 'FP' : 'TN');
      counts[type.toLowerCase()]++;
      const truth = item.truth ? '이상' : '정상', predicted = prediction ? '이상' : '정상';
      const row = document.createElement('div');
      row.className = 'score-row'; row.setAttribute('role','listitem');
      row.setAttribute('aria-label', `샘플 ${index+1}, 점수 ${item.score.toFixed(2)}, 실제 ${truth}, 예측 ${predicted}, ${type}`);
      row.innerHTML = `<strong>#${index+1}</strong>
        <div class="score-track" aria-hidden="true" style="--threshold-pct:${threshold*100}%"><div class="score-fill" style="width:${item.score*100}%"></div></div>
        <span class="score-number">${item.score.toFixed(2)}</span><span class="sample-truth">${truth}</span>
        <span class="sample-prediction">${predicted}</span><span class="outcome ${type.toLowerCase()}">${type}</span>`;
      list.appendChild(row);
    });
    for (const [key,value] of Object.entries(counts)) document.getElementById('cm-'+key).textContent=String(value);
    const {tp,tn,fp,fn} = counts;
    const precision=pct(tp,tp+fp),recall=pct(tp,tp+fn);
    document.getElementById('precision').textContent=precision;
    document.getElementById('recall').textContent=recall;
    document.getElementById('precision-calculation').textContent=`${tp} / (${tp} + ${fp}) = ${precision}`;
    document.getElementById('recall-calculation').textContent=`${tp} / (${tp} + ${fn}) = ${recall}`;
    document.getElementById('score-summary').textContent=`이상 예측 ${tp+fp}개 · 정상 예측 ${tn+fn}개`;
    document.getElementById('evaluation-status').textContent=`임계값 ${threshold.toFixed(2)}. TP ${tp}, FP ${fp}, FN ${fn}, TN ${tn}. Precision ${precision}, Recall ${recall}.`;
  }
  slider.addEventListener('input',update); update();

  // Reuse #7's text-boundary alignment rather than attaching the rule to a cell.
  const figure=document.querySelector('.live-cm-wrap');
  const axis=figure.querySelector('.pred-axis');
  function textBounds(element) {
    const walker=document.createTreeWalker(element,NodeFilter.SHOW_TEXT),rects=[];
    while(walker.nextNode()) {
      if(!walker.currentNode.textContent.trim()) continue;
      const range=document.createRange();range.selectNodeContents(walker.currentNode);rects.push(range.getBoundingClientRect());
    }
    return {left:Math.min(...rects.map(r=>r.left)),right:Math.max(...rects.map(r=>r.right))};
  }
  function alignDivider() {
    const title=textBounds(axis.querySelector('.pred-axis-label'));
    const left=Math.min(...[...figure.querySelectorAll('tbody th[scope="row"]')].map(e=>textBounds(e).left));
    const box=figure.getBoundingClientRect(),axisBox=axis.getBoundingClientRect();
    const scale=box.width/parseFloat(getComputedStyle(figure).width);
    const lineWidth=parseFloat(getComputedStyle(figure.querySelector('.live-pred-divider')).borderRightWidth);
    figure.style.setProperty('--divider-x',`${((title.right+left)/2-box.left)/scale-lineWidth/2}px`);
    figure.style.setProperty('--divider-y',`${(axisBox.top-box.top)/scale}px`);
    figure.style.setProperty('--divider-height',`${axisBox.height/scale}px`);
  }
  document.fonts.ready.then(alignDivider);new ResizeObserver(alignDivider).observe(figure);window.addEventListener('resize',alignDivider);
})();
