import {DEFAULT_MODEL, normalizeModel, evaluateModel, sigmoid, predict} from './model.js';

export const pages = [
  {id: 'concept', name: '확률 예측', type: 'CONCEPT', title: '로지스틱 회귀의 확률 예측',
   subtitle: '입력 특성 → 선형 점수 → 확률 변환 → 양성 확률'},
  {id: 'calculation', name: '확률 계산', type: 'STEP-BY-STEP', title: '한 샘플의 확률 계산',
   subtitle: '같은 입력과 계수로 가중합부터 시그모이드까지 계산'},
  {id: 'threshold', name: '임계값 판정', type: 'INTERACTIVE', title: '임계값에 따른 판정 변화',
   subtitle: '임계값(Threshold): 양성으로 판정하는 최소 확률 · 확률은 고정, 기준만 이동'},
];

const state = {model: normalizeModel(DEFAULT_MODEL), selected: 3, threshold: 60};
let root;
const sub = n => `<sub>${n}</sub>`;
const arrow = () => '<svg class="lr-connector" viewBox="0 0 32 16" aria-hidden="true"><path d="M2 8 H29 M23 2 L29 8 L23 14"/></svg>';
const heading = (label, title, description = '') => `<div class="lr-heading"><div class="lr-label">${label}</div><h2>${title}</h2>${description ? `<p>${description}</p>` : ''}</div>`;
const takeaway = (label, text) => `<div class="ref-takeaway"><strong>${label}</strong><span>${text}</span></div>`;
const footer = index => `<footer class="footer"><span>Design Template Library · 로지스틱 회귀</span><span>${String(index+1).padStart(2,'0')} / 03</span></footer>`;
const frac = (top, bottom) => `<span class="lr-fraction"><span>${top}</span><span>${bottom}</span></span>`;
const number = x => (Math.abs(x) < 0.0000000001 ? 0 : x).toFixed(2).replace('-', '−');
const signed = x => `${x < 0 ? '−' : '+'} ${number(Math.abs(x))}`;
const percent = p => `${(p*100).toFixed(1)}%`;
const value = key => `<span data-value="${key}"></span>`;

function concept() {
  const stage = (figure, label, note) => `<div class="lr-step"><div class="lr-figure">${figure}</div><div class="lr-step-label">${label}</div><p class="lr-step-note">${note}</p></div>`;
  return `<div class="lr-body"><section class="lr-panel lr-concept-panel">
    <div class="lr-concept-heading"><h2>로지스틱 회귀(Logistic Regression)</h2><p>양성(1)·음성(0) 두 클래스 중 양성의 확률을 계산하는 분류 모델</p></div>
    <div class="lr-flow">
      ${stage(`<div class="lr-inputs"><div><span>x${sub(1)}</span><strong>${value('x1')}</strong></div><div><span>x${sub(2)}</span><strong>${value('x2')}</strong></div></div>`, '입력 특성', '대상의 두 수치')}
      ${arrow()}
      ${stage(`<div class="lr-score"><span>z</span><strong>${value('z')}</strong><span>선형 점수</span></div>`, '가중합 + 절편', '입력에 계수를 곱해 합산')}
      ${arrow()}
      ${stage('<svg class="lr-curve" role="img" aria-label="선형 점수를 양성 확률로 변환하는 시그모이드 곡선" viewBox="0 0 300 210"></svg>', '시그모이드(Sigmoid)', '실수 점수 → 0과 1 사이')}
      ${arrow()}
      ${stage(`<div class="lr-probability"><span>양성 확률 p</span><strong>${value('percent')}</strong><div class="lr-prob-track"><i data-prob-fill></i></div></div>`, '확률 출력', '선택 샘플의 양성 가능성')}
    </div>
    <div class="lr-symbols"><span><strong>x</strong> 입력 특성</span><span><strong>z</strong> 확률로 변환하기 전 점수</span><span><strong>p</strong> 양성 예측 확률</span><span class="lr-example">예시 입력·계수 · 학습 과정 제외</span></div>
    </section></div>${takeaway('확률의 의미', '입력에서 계산한 선형 점수를 양성 클래스의 확률로 변환')}`;
}

function calculation() {
  return `<div class="lr-body lr-two-columns lr-calculation">
    <section class="lr-panel lr-calc-panel">
      ${heading('01 · WEIGHTED SUM', '입력과 계수의 곱', '가중치 w는 특성에 곱하는 계수,<br>절편 b는 입력과 무관하게 더하는 값')}
      <div class="lr-calc-main"><table class="lr-product-table"><thead><tr><th>입력 x</th><th>가중치 w</th><th>곱 w × x</th></tr></thead><tbody>
        <tr><td>x${sub(1)} = ${value('x1')}</td><td>${value('w1')}</td><td>${value('product1')}</td></tr>
        <tr><td>x${sub(2)} = ${value('x2')}</td><td>${value('w2')}</td><td>${value('product2')}</td></tr>
      </tbody></table><div class="lr-bias"><span>절편 b</span><strong>${value('bias')}</strong></div>
      <div class="lr-sum"><span>z = ${value('sum')}</span><strong>= ${value('z')}</strong></div></div>
      <div class="lr-card-note">일반식: z = w${sub(1)}x${sub(1)} + w${sub(2)}x${sub(2)} + b</div>
    </section>
    <section class="lr-panel lr-calc-panel">
      ${heading('02 · SIGMOID', '점수를 확률로 변환', '시그모이드(Sigmoid): 실수 점수를<br>0과 1 사이의 값으로 변환하는 함수')}
      <div class="lr-prob-calculation"><div class="lr-general">p = ${frac('1', '1 + e<sup>−z</sup>')}</div>
      <div class="lr-substitute">= ${frac('1', `1 + e<sup>${value('negativeZ')}</sup>`)}</div>
      <div class="lr-decimal">≈ ${value('decimal')}</div><div class="lr-final-prob">${value('percent')}</div></div>
      <div class="lr-card-note">e ≈ 2.718 · 표시는 반올림, 판정은 원래 확률 사용</div>
    </section>
    </div>${takeaway('계산의 연결', '왼쪽에서 계산한 z를 오른쪽 확률식에 그대로 대입')}`;
}

function threshold() {
  return `<div class="lr-body lr-two-columns lr-threshold">
    <section class="lr-panel lr-control-panel">
      ${heading('LIVE CONTROL', '샘플 확률과 판정')}
      <div class="lr-slider-row"><label for="threshold">임계값 t</label><output for="threshold" data-value="threshold"></output><input id="threshold" type="range" min="0" max="100" step="1" value="60" aria-label="양성 판정의 임계값"></div>
      <div class="lr-rule-row"><span>p ≥ t → 양성(1)</span><span class="lr-threshold-legend"><i></i>현재 임계값</span></div>
      <div class="lr-sample-table"><div class="lr-sample-header"><span>샘플</span><div class="lr-prob-axis"><span>0%</span><span>50%</span><span>100%</span></div><span>확률 p</span><span>예측</span></div>
      <div class="lr-sample-rows"></div></div>
      <div class="lr-counts"><span>양성 <strong data-value="positive"></strong>개</span><span>음성 <strong data-value="negative"></strong>개</span><span class="lr-muted">버튼으로 샘플 선택</span></div>
    </section>
    <section class="lr-panel lr-decision-panel">
      ${heading('SELECTED SAMPLE', '한 샘플의 판정')}
      <div class="lr-selection-detail"><strong>샘플 ${value('sample')}</strong><span>x${sub(1)} = ${value('x1')} · x${sub(2)} = ${value('x2')} · z = ${value('z')}</span></div>
      <div class="lr-comparison"><div class="lr-compare-block"><span>양성 확률 p</span><strong>${value('percent')}</strong><small>≈ ${value('decimal')}</small></div><span class="lr-relation" data-value="relation"></span><div class="lr-compare-block"><span>임계값 t</span><strong>${value('thresholdPercent')}</strong><small>${value('threshold')}</small></div></div>
      <div class="lr-decision" data-decision><span>예측 클래스</span><strong data-value="prediction"></strong><span data-value="comparison"></span></div>
      <div class="lr-card-note">임계값 변경은 판정 기준의 변경이며,<br>모델 재학습이나 확률 재계산이 아님</div>
    </section>
    </div>${takeaway('기준의 변화', '임계값을 높이면 양성 판정 수는 줄거나 같고, 각 샘플의 확률은 유지')}
    <p class="lr-sr-only sr-only" id="prediction-status" role="status" aria-live="polite"></p>`;
}

function drawCurve(row) {
  const svg = root.querySelector('.lr-curve');
  const limit = Math.max(4, Math.ceil(Math.abs(row.z)/4)*4);
  const x = z => 40+(z+limit)/(2*limit)*240, y = p => 172-p*150;
  const d = Array.from({length: 161}, (_, i) => {const z=-limit+i*2*limit/160;return `${i?'L':'M'}${x(z).toFixed(3)},${y(sigmoid(z)).toFixed(3)}`;}).join(' ');
  svg.dataset.limit=String(limit);
  svg.innerHTML = `<g class="lr-plot-grid"><path d="M40 22 V172 H280"/><path class="lr-midline" d="M40 97 H280 M160 22 V172"/></g>
    <g class="lr-axis-text"><text x="19" y="27">1</text><text x="9" y="102">0.5</text><text x="19" y="177">0</text><text x="40" y="194" text-anchor="middle">−${limit}</text><text x="160" y="194" text-anchor="middle">0</text><text x="280" y="194" text-anchor="middle">${limit}</text><text x="42" y="15">p</text><text x="291" y="176">z</text></g>
    <path class="lr-sigmoid-path" d="${d}"/><path class="lr-point-guides" d="M${x(row.z)} 172 V${y(row.p)} H40"/>
    <circle class="lr-curve-point" cx="${x(row.z)}" cy="${y(row.p)}" r="6"/>`;
}

function update(announce = false) {
  const rows=evaluateModel(state.model), row=rows[state.selected], t=state.threshold/100;
  const prediction=predict(row.p,t), positives=rows.filter(r=>predict(r.p,t)).length;
  const values={x1:number(row.input[0]),x2:number(row.input[1]),w1:number(state.model.weights[0]),w2:number(state.model.weights[1]),
    bias:number(state.model.bias),product1:number(row.products[0]),product2:number(row.products[1]),z:number(row.z),
    negativeZ:number(-row.z),sum:`${number(row.products[0])} ${signed(row.products[1])} ${signed(state.model.bias)}`,
    percent:percent(row.p),decimal:row.p.toFixed(6),threshold:(t).toFixed(2),thresholdPercent:percent(t),
    positive:positives,negative:rows.length-positives,sample:state.selected+1,relation:prediction?'≥':'<',
    prediction:prediction?'양성(1)':'음성(0)',comparison:prediction?'확률이 기준 이상 → 양성':'확률이 기준 미만 → 음성'};
  root.querySelectorAll('[data-value]').forEach(el=>{el.textContent=values[el.dataset.value];});
  root.querySelector('[data-prob-fill]').style.width=`${100*row.p}%`;
  const slider=root.querySelector('#threshold');slider.value=String(state.threshold);slider.setAttribute('aria-valuetext',`${t.toFixed(2)}, ${positives}개 양성`);
  const table=root.querySelector('.lr-sample-rows');
  if(table.children.length!==rows.length) {
    table.innerHTML=rows.map(r=>`<div class="lr-sample-row" data-sample-index="${r.index}"><button type="button" data-select="${r.index}" aria-label="샘플 ${r.index+1} 선택">${r.index+1}</button><div class="lr-sample-track"><i class="lr-sample-fill"></i><i class="lr-threshold-line"></i></div><span class="lr-sample-percent"></span><span class="lr-badge"></span></div>`).join('');
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
  drawCurve(row);
  if(announce)root.querySelector('#prediction-status').textContent=`임계값 ${t.toFixed(2)}. 양성 ${positives}개, 음성 ${rows.length-positives}개. 샘플 ${state.selected+1}은 ${values.prediction}.`;
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
  const figures=[concept,calculation,threshold];
  root.innerHTML=pages.map((page,i)=>`<section class="reference-section" id="ref-${page.id}" aria-label="${i+1}. ${page.name}"><div class="reference-viewport"><article class="slide reference-slide logistic-slide" data-page="${page.id}"><header><div class="kicker">${page.type} / ${String(i+1).padStart(2,'0')}</div><h1>${page.title}</h1><p class="subtitle">${page.subtitle}</p></header>${figures[i]()}${footer(i)}</article></div></section>`).join('');
  root.addEventListener('input',event=>{if(event.target.id==='threshold')setThreshold(Number(event.target.value));});
  root.addEventListener('click',event=>{const button=event.target.closest('[data-select]');if(button)setSelection(Number(button.dataset.select));});
  update();
  window.LogisticLesson={
    get state(){return structuredClone({...state,rows:evaluateModel(state.model)});},setThreshold,setSelection,sigmoid,
    setModel(input){const next=normalizeModel(input);if(next.samples.length>6)throw new RangeError('한 화면에는 최대 6개 샘플을 표시합니다.');state.model=next;state.selected=Math.min(state.selected,next.samples.length-1);update();},
  };
  return [...root.querySelectorAll('.reference-section')];
}
