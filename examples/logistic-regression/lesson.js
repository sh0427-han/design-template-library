import {DEFAULT_MODEL, normalizeModel, evaluateModel, sigmoid, predict} from './model.js';

export const pages = [
  {id: 'concept', name: '확률 예측', type: 'CONCEPT', title: '로지스틱 회귀의 확률 예측',
   subtitle: '입력 특성 → 선형 점수 → 확률 변환 → 양성 확률'},
  {id: 'calculation', name: '확률 계산', type: 'STEP-BY-STEP', title: '한 샘플의 확률 계산',
   subtitle: '실제 값을 대입해 구한 점수를 확률식과 그래프로 연결'},
];
export const appendixPage = {id:'threshold',name:'부록 · 임계값 판정',type:'APPENDIX',title:'임계값에 따른 판정 변화',subtitle:'임계값(Threshold): 양성으로 판정하는 최소 확률 · 확률은 고정, 기준만 이동'};
export const getPages = includeAppendix => includeAppendix ? [...pages,appendixPage] : pages;

const state = {model: normalizeModel(DEFAULT_MODEL), selected: 3, threshold: 60};
let root;
const arrow = () => '<svg class="lr-connector" viewBox="0 0 32 16" aria-hidden="true"><path d="M2 8 H29 M23 2 L29 8 L23 14"/></svg>';
const heading = (label, title, description = '') => `<div class="lr-heading"><div class="lr-label">${label}</div><h2>${title}</h2>${description ? `<p>${description}</p>` : ''}</div>`;
const takeaway = (label, text) => `<div class="ref-takeaway"><strong>${label}</strong><span>${text}</span></div>`;
const footer = index => `<footer class="footer"><span>Design Template Library · 로지스틱 회귀</span><span>${index===2?'부록 A':`${String(index+1).padStart(2,'0')} / 02`}</span></footer>`;
const number = x => (Math.abs(x) < 0.0000000001 ? 0 : x).toFixed(2).replace('-', '−');
const percent = p => `${(p*100).toFixed(1)}%`;
const numeric = new Set(['x1','x2','w1','w2','bias','z','decimal','percent','threshold','thresholdPercent']);
const value = key => `<span${numeric.has(key)?' class="math-number"':''} data-value="${key}"></span>`;
const m = body => `<math class="math" displaystyle="true" xmlns="http://www.w3.org/1998/Math/MathML"><mrow>${body}</mrow></math>`;
const mi = x => `<mi>${x}</mi>`;
const mo = x => `<mo>${x}</mo>`;
const mn = x => `<mn>${x}</mn>`;
const symbol = (x,n) => n===undefined?mi(x):`<msub>${mi(x)}${mn(n)}</msub>`;
const mv = key => `<mn data-value="${key}"></mn>`;
const weightedTerms = () => `${symbol('w',1)}${symbol('x',1)}${mo('+')}${symbol('w',2)}${symbol('x',2)}${mo('+')}${mi('b')}`;
const weighted = () => `${mi('z')}${mo('=')}${weightedTerms()}`;
const leadingEquals = () => '<mo lspace="0">=</mo>';
const factor = key => `<mrow class="lr-factor" data-factor="${key}"><mo stretchy="false">(</mo>${mv(key)}<mo stretchy="false">)</mo></mrow>`;
const sigmoidExpression = exponent => `<mfrac>${mn(1)}<mrow>${mn(1)}${mo('+')}<msup><mi mathvariant="normal">e</mi>${exponent}</msup></mrow></mfrac>`;
const sigmoidGeneral = () => m(mi('σ')+'<mo stretchy="false">(</mo>'+mi('z')+'<mo stretchy="false">)</mo>'+mo('=')+sigmoidExpression(`<mrow>${mo('−')}${mi('z')}</mrow>`));

function concept() {
  const stage = (figure, label) => `<div class="lr-step"><div class="lr-figure">${figure}</div><div class="lr-step-label">${label}</div></div>`;
  return `<div class="lr-body"><section class="lr-panel lr-concept-panel">
    <div class="lr-concept-heading"><h2>로지스틱 회귀(Logistic Regression)</h2><span class="lr-example">이진 분류 · 확률 모델</span><p>양성(1)·음성(0) 중 양성의 확률을 예측하는 분류 모델</p></div>
    <div class="lr-flow">
      ${stage(`<div class="lr-inputs">${[1,2].map(i=>`<div><div class="lr-feature-value">${m(symbol('x',i))}</div><div class="lr-feature-weight">가중치 ${m(symbol('w',i))}</div></div>`).join('')}</div>`, '입력 특성')}
      ${arrow()}
      ${stage(`<div class="lr-score"><div class="lr-score-general">${m(weighted())}</div></div>`, '가중합 + 절편')}
      ${arrow()}
      ${stage(`<div class="lr-sigmoid-stage"><div class="lr-sigmoid-formula">${sigmoidGeneral()}</div><svg class="lr-curve" role="img" aria-label="선형 점수를 양성 확률로 변환하는 시그모이드 곡선" viewBox="0 0 300 210"></svg></div>`, '시그모이드(Sigmoid)')}
      ${arrow()}
      ${stage(`<div class="lr-probability"><strong>${m(mi('p')+mo('=')+mi('σ')+'<mo stretchy="false">(</mo>'+mi('z')+'<mo stretchy="false">)</mo>')}</strong><span>0과 1 사이의 확률</span></div>`, '확률 출력')}
    </div>
    <div class="lr-symbols"><div><span>${m(mi('x'))} 입력 특성</span><small>가중치 ${m(mi('w'))}: 특성에 곱하는 계수</small></div><div><span>${m(mi('z'))} 확률 변환 전 점수</span><small>절편 ${m(mi('b'))}: 입력과 무관하게 더하는 값</small></div><div><span>${m(mi('σ'))} 시그모이드 함수</span><small>자연상수 ${m('<mi mathvariant="normal">e</mi>')} · 실수 점수를 0~1로 변환</small></div><div><span>${m(mi('p'))} 양성 예측 확률</span><small>확률과 최종 클래스 판정은 구분</small></div></div>
    </section></div>${takeaway('확률의 의미', '입력에서 계산한 선형 점수를 양성 클래스의 확률로 변환')}`;
}

function calculation() {
  return `<div class="lr-body lr-two-columns lr-calculation">
    <section class="lr-panel lr-calc-panel lr-linear-panel">
      ${heading('01 · LINEAR SCORE', '곱하고 더해 점수 계산')}
      <div class="lr-calc-main"><div class="lr-input-chip lr-given-values"><div><span>입력</span>${m(symbol('x',1)+mo('=')+mv('x1')+mo(',')+symbol('x',2)+mo('=')+mv('x2'))}</div><div><span>가중치·절편</span>${m(symbol('w',1)+mo('=')+mv('w1')+mo(',')+symbol('w',2)+mo('=')+mv('w2')+mo(',')+mi('b')+mo('=')+mv('bias'))}</div></div>
      <div class="lr-equation-chain"><div class="lr-equation-row lr-equation-general">${m(mi('z'))}${m(leadingEquals()+weightedTerms())}</div><div class="lr-equation-row lr-equation-substitution"><span></span>${m(leadingEquals()+factor('w1')+mo('×')+factor('x1')+mo('+')+factor('w2')+mo('×')+factor('x2')+'<mo data-value="biasSign"></mo>'+mv('biasMagnitude'))}</div><div class="lr-equation-row lr-equation-result"><span></span><strong class="lr-score-output">${m(leadingEquals()+mv('z'))}</strong></div></div></div>
      <div class="lr-card-note">예시 입력·계수 · 모델 학습 과정 제외</div>
    </section>
    <div class="lr-card-transfer"><span class="lr-transfer-label">${m(mi('z'))} 전달</span></div>
    <section class="lr-panel lr-calc-panel">
      ${heading('02 · SIGMOID', '점수를 확률로 변환', '같은 점수와 확률을 식과 그래프로 연결')}
      <div class="lr-sigmoid-comparison"><div class="lr-prob-calculation"><div class="lr-input-chip lr-received-score"><span>입력 점수</span>${m(mi('z')+mo('=')+mv('z'))}</div><div class="lr-general lr-sigmoid-formula">${m(mi('p')+mo('=')+sigmoidExpression(`<mrow>${mo('−')}${mi('z')}</mrow>`))}</div>
      <div class="lr-substitute lr-sigmoid-formula">${m(mo('=')+sigmoidExpression(mv('negativeZ')))}</div>
      <div class="lr-decimal">${m(mo('≈')+mv('decimal'))}</div><div class="lr-final-prob">${value('percent')}</div></div>
      <figure class="lr-calculation-graph"><svg class="lr-curve lr-detail-curve" data-variant="detail" role="img" aria-label="계산한 점수와 확률을 축에 표시한 시그모이드 곡선" viewBox="0 0 360 260"></svg><figcaption>${m(mi('z')+mo('=')+mv('z'))} → ${m(mi('p')+mo('≈')+mv('decimal'))}</figcaption></figure></div>
      <div class="lr-card-note">${m('<mi mathvariant="normal">e</mi>'+mo('≈')+mn('2.718'))} · 표시는 반올림, 판정은 원래 확률 사용</div>
    </section>
    <svg class="lr-transfer-svg" aria-hidden="true"><path class="lr-transfer-path"/></svg></div>${takeaway('계산의 연결', `왼쪽에서 계산한 ${m(mi('z'))}를 오른쪽 확률식에 그대로 대입`)}`;
}

function threshold() {
  return `<div class="lr-body lr-two-columns lr-threshold">
    <section class="lr-panel lr-control-panel">
      ${heading('LIVE CONTROL', '샘플 확률과 판정')}
      <div class="lr-slider-row"><label for="threshold">임계값 ${m(mi('t'))}</label><output class="math-number" for="threshold" data-value="threshold"></output><input id="threshold" type="range" min="0" max="100" step="1" value="60" aria-label="양성 판정의 임계값"></div>
      <div class="lr-rule-row"><span>${m(mi('p')+mo('≥')+mi('t'))} → 양성(1)</span><span class="lr-threshold-legend"><i></i>현재 임계값</span></div>
      <div class="lr-sample-table"><div class="lr-sample-header"><span>샘플</span><div class="lr-prob-axis"><span>0%</span><span>50%</span><span>100%</span></div><span>확률 ${m(mi('p'))}</span><span>예측</span></div>
      <div class="lr-sample-rows"></div></div>
      <div class="lr-counts"><span>양성 <strong data-value="positive"></strong>개</span><span>음성 <strong data-value="negative"></strong>개</span><span class="lr-muted">버튼으로 샘플 선택</span></div>
    </section>
    <section class="lr-panel lr-decision-panel">
      ${heading('SELECTED SAMPLE', '한 샘플의 판정')}
      <div class="lr-selection-detail"><strong>샘플 ${value('sample')}</strong><span>${m(symbol('x',1)+mo('=')+mv('x1'))} · ${m(symbol('x',2)+mo('=')+mv('x2'))} · ${m(mi('z')+mo('=')+mv('z'))}</span></div>
      <div class="lr-comparison"><div class="lr-compare-block"><span>양성 확률 ${m(mi('p'))}</span><strong>${value('percent')}</strong><small>${m(mo('≈')+mv('decimal'))}</small></div><span class="lr-relation math-number" data-value="relation"></span><div class="lr-compare-block"><span>임계값 ${m(mi('t'))}</span><strong>${value('thresholdPercent')}</strong><small>${value('threshold')}</small></div></div>
      <div class="lr-decision" data-decision><span>예측 클래스</span><strong data-value="prediction"></strong><span data-value="comparison"></span></div>
      <div class="lr-card-note">임계값 변경은 판정 기준의 변경이며,<br>모델 재학습이나 확률 재계산이 아님</div>
    </section>
    </div>${takeaway('기준의 변화', '임계값을 높이면 양성 판정 수는 줄거나 같고, 각 샘플의 확률은 유지')}
    <p class="lr-sr-only sr-only" id="prediction-status" role="status" aria-live="polite"></p>`;
}

function drawCurve(row) {
  for(const svg of root.querySelectorAll('.lr-curve')) {
  const detail=svg.dataset.variant==='detail';
  const limit = detail?Math.max(4, Math.ceil(Math.abs(row.z)/4)*4):4;
  const left=detail?56:40,top=detail?30:22,width=detail?272:240,height=detail?180:150,bottom=top+height;
  const x = z => left+(z+limit)/(2*limit)*width, y = p => bottom-p*height;
  const d = Array.from({length: 161}, (_, i) => {const z=-limit+i*2*limit/160;return `${i?'L':'M'}${x(z).toFixed(3)},${y(sigmoid(z)).toFixed(3)}`;}).join(' ');
  svg.dataset.limit=String(limit);
  const yTicks=[0,.5,1].filter(p=>!detail||Math.abs(y(p)-y(row.p))>18).map(p=>`<text x="${left-10}" y="${y(p)+5}" text-anchor="end">${p}</text>`).join('');
  const xTicks=[-limit,0,limit].filter(z=>!detail||Math.abs(x(z)-x(row.z))>28).map(z=>`<text x="${x(z)}" y="${bottom+23}" text-anchor="middle">${String(z).replace('-','−')}</text>`).join('');
  svg.innerHTML = `<g class="lr-plot-grid"><path d="M${left} ${top} V${bottom} H${left+width}"/><path class="lr-midline" d="M${left} ${y(.5)} H${left+width} M${x(0)} ${top} V${bottom}"/></g>
    <g class="lr-axis-text math-number">${yTicks}${xTicks}<text x="${left+2}" y="${top-12}">𝑝</text><text x="${left+width+11}" y="${bottom+4}">𝑧</text></g>
    <path class="lr-sigmoid-path" d="${d}"/>
    ${detail?`<path class="lr-point-guides" d="M${x(row.z)} ${bottom} V${y(row.p)} H${left}"/>`:''}
    ${detail?`<g class="lr-selected-axis math-number"><text data-axis="z" x="${x(row.z)}" y="${bottom+23}" text-anchor="middle">${number(row.z)}</text><text data-axis="p" x="${left-10}" y="${y(row.p)+5}" text-anchor="end">${row.p.toFixed(3)}</text></g>`:''}
    ${detail?`<circle class="lr-curve-point" cx="${x(row.z)}" cy="${y(row.p)}" r="6"/>`:''}`;
  }
}

function drawTransfer() {
  const container=root.querySelector('.lr-calculation'),bounds=container.getBoundingClientRect();
  if(!bounds.width||!bounds.height)return;
  const scale=bounds.width/parseFloat(getComputedStyle(container).width);
  const source=container.querySelector('.lr-score-output').getBoundingClientRect(),target=container.querySelector('.lr-received-score').getBoundingClientRect();
  const panels=container.querySelectorAll('.lr-panel'),a=panels[0].getBoundingClientRect(),b=panels[1].getBoundingClientRect();
  const sx=(source.right-bounds.left)/scale+6,sy=(source.y+source.height/2-bounds.y)/scale;
  const tx=(target.left-bounds.left)/scale-8,ty=(target.y+target.height/2-bounds.y)/scale;
  const mid=((a.right+b.left)/2-bounds.left)/scale,svg=container.querySelector('.lr-transfer-svg');
  svg.setAttribute('viewBox',`0 0 ${bounds.width/scale} ${bounds.height/scale}`);
  svg.querySelector('path').setAttribute('d',`M${sx} ${sy} H${mid} V${ty} H${tx} M${tx-6} ${ty-5} L${tx} ${ty} L${tx-6} ${ty+5}`);
  const label=container.querySelector('.lr-transfer-label');label.style.top=`${(sy+ty)/2}px`;
}
export const refreshFigureLinks = () => drawTransfer();

function update(announce = false) {
  const rows=evaluateModel(state.model), row=rows[state.selected], t=state.threshold/100;
  const prediction=predict(row.p,t), positives=rows.filter(r=>predict(r.p,t)).length;
  const values={x1:number(row.input[0]),x2:number(row.input[1]),w1:number(state.model.weights[0]),w2:number(state.model.weights[1]),
    bias:number(state.model.bias),z:number(row.z),
    negativeZ:number(-row.z),
    biasSign:state.model.bias<0?'−':'+',biasMagnitude:number(Math.abs(state.model.bias)),
    percent:percent(row.p),decimal:row.p.toFixed(6),threshold:(t).toFixed(2),thresholdPercent:percent(t),
    positive:positives,negative:rows.length-positives,sample:state.selected+1,relation:prediction?'≥':'<',
    prediction:prediction?'양성(1)':'음성(0)',comparison:prediction?'확률이 기준 이상 → 양성':'확률이 기준 미만 → 음성'};
  root.querySelectorAll('[data-value]').forEach(el=>{el.textContent=values[el.dataset.value];});
  for(const el of root.querySelectorAll('[data-factor]'))el.dataset.negative=String(values[el.dataset.factor].startsWith('−'));
  const slider=root.querySelector('#threshold');
  if(slider) {
  slider.value=String(state.threshold);slider.setAttribute('aria-valuetext',`${t.toFixed(2)}, ${positives}개 양성`);
  const table=root.querySelector('.lr-sample-rows');
  if(table.children.length!==rows.length) {
    table.innerHTML=rows.map(r=>`<div class="lr-sample-row" data-sample-index="${r.index}"><button type="button" data-select="${r.index}" aria-label="샘플 ${r.index+1} 선택">${r.index+1}</button><div class="lr-sample-track"><i class="lr-sample-fill"></i><i class="lr-threshold-line"></i></div><span class="lr-sample-percent math-number"></span><span class="lr-badge"></span></div>`).join('');
  }
  rows.forEach(r=>{
    const el=table.children[r.index],pred=predict(r.p,t);
    el.dataset.probability=String(r.p);el.dataset.z=String(r.z);el.dataset.prediction=String(pred);el.dataset.selected=String(r.index===state.selected);
    el.querySelector('button').setAttribute('aria-pressed',String(r.index===state.selected));
    el.querySelector('.lr-sample-fill').style.width=`${r.p*100}%`;
    el.querySelector('.lr-threshold-line').style.left=`${state.threshold}%`;
    el.querySelector('.lr-sample-percent').textContent=percent(r.p);
    const badge=el.querySelector('.lr-badge');badge.textContent=pred?'양성 1':'음성 0';badge.dataset.prediction=String(pred);
  });
  root.querySelector('[data-decision]').dataset.prediction=String(prediction);
  }
  drawCurve(row);
  drawTransfer();
  if(announce&&slider)root.querySelector('#prediction-status').textContent=`임계값 ${t.toFixed(2)}. 양성 ${positives}개, 음성 ${rows.length-positives}개. 샘플 ${state.selected+1}은 ${values.prediction}.`;
  root.dispatchEvent(new CustomEvent('lessonstatechange',{bubbles:true}));
}

export function setThreshold(percentValue, announce=true) {
  if(!Number.isInteger(percentValue)||percentValue<0||percentValue>100)throw new RangeError('임계값은 0~100 정수입니다.');
  state.threshold=percentValue;update(announce);
}
export function setSelection(index, announce=true) {
  if(!Number.isInteger(index)||index<0||index>=state.model.samples.length)throw new RangeError('존재하는 샘플을 선택해 주세요.');
  state.selected=index;update(announce);
}

export function renderLesson(container, initial={}) {
  root=container;
  state.threshold=initial.threshold??60;state.selected=initial.sample??3;
  const activePages=getPages(initial.includeAppendix);
  const figures=[concept,calculation,threshold];
  root.innerHTML=activePages.map((page,i)=>`<section class="reference-section" id="ref-${page.id}" aria-label="${page.name}"><div class="reference-viewport"><article class="slide reference-slide logistic-slide" data-page="${page.id}"><header><div class="kicker">${page.type} / ${i===2?'A':String(i+1).padStart(2,'0')}</div><h1>${page.title}</h1><p class="subtitle">${page.subtitle}</p></header>${figures[i]()}${footer(i)}</article></div></section>`).join('');
  document.fonts.ready.then(()=>drawTransfer());
  root.addEventListener('input',event=>{if(event.target.id==='threshold')setThreshold(Number(event.target.value));});
  root.addEventListener('click',event=>{const button=event.target.closest('[data-select]');if(button)setSelection(Number(button.dataset.select));});
  update();
  window.LogisticLesson={
    get state(){return structuredClone({...state,rows:evaluateModel(state.model)});},setThreshold,setSelection,sigmoid,
    setModel(input){const next=normalizeModel(input);if(next.samples.length>6)throw new RangeError('한 화면에는 최대 6개 샘플을 표시합니다.');state.model=next;state.selected=Math.min(state.selected,next.samples.length-1);update();},
  };
  return [...root.querySelectorAll('.reference-section')];
}
