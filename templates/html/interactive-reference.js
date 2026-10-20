/* Recomputes the six displayed outcomes from the same threshold. */
(() => {
  const samples = [
    {score:0.15,truth:0}, {score:0.32,truth:1},
    {score:0.48,truth:0}, {score:0.67,truth:1},
    {score:0.82,truth:1}, {score:0.94,truth:0},
  ];
  const slider = document.getElementById('threshold');
  const readout = document.getElementById('threshold-value');
  const list = document.getElementById('score-list');
  function update() {
    const threshold = Number(slider.value) / 100;
    readout.textContent = threshold.toFixed(2);
    let tp = 0, tn = 0, fp = 0, fn = 0;
    list.innerHTML = '';
    samples.forEach((item, index) => {
      const prediction = Number(item.score >= threshold);
      const label = item.truth === 1
        ? (prediction === 1 ? 'TP' : 'FN')
        : (prediction === 1 ? 'FP' : 'TN');
      if (label === 'TP') tp++; if (label === 'TN') tn++;
      if (label === 'FP') fp++; if (label === 'FN') fn++;
      const row = document.createElement('div');
      row.className = 'score-row';
      row.innerHTML = `<strong>#${index+1}</strong>
        <div class="score-track" style="--threshold-pct:${threshold*100}%">
        <div class="score-fill" style="width:${item.score*100}%"></div></div>
        <span class="truth">${item.score.toFixed(2)} / ${item.truth?'이상':'정상'}</span>
        <span class="outcome ${label.toLowerCase()}">${label}</span>`;
      list.appendChild(row);
    });
    for (const [key,value] of Object.entries({tp,tn,fp,fn}))
      document.getElementById('cm-'+key).textContent=String(value);
    const pct=(n,d)=>d? (100*n/d).toFixed(1)+'%' : '정의 불가';
    document.getElementById('precision').textContent=pct(tp,tp+fp);
    document.getElementById('recall').textContent=pct(tp,tp+fn);
  }
  slider.addEventListener('input', update);
  update();
})();
