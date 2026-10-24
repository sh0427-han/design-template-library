// One concept page; both display modes render the same editable source.
export const pages = [{id:'concept',name:'확률 예측',type:'CONCEPT',title:'로지스틱 회귀의 확률 예측',subtitle:'입력 특성 → 선형 점수 → 확률 변환 → 양성 확률'}];
const arrow = () => '<svg class="lr-connector" viewBox="0 0 32 16" aria-hidden="true"><path d="M2 8 H29 M23 2 L29 8 L23 14"/></svg>';
const takeaway = (label,text) => `<div class="ref-takeaway"><strong>${label}</strong><span>${text}</span></div>`;
const m = body => `<math class="math" displaystyle="true" xmlns="http://www.w3.org/1998/Math/MathML"><mrow>${body}</mrow></math>`;
const mi = x => `<mi>${x}</mi>`;
const mo = x => `<mo>${x}</mo>`;
const mn = x => `<mn>${x}</mn>`;
const symbol = (x,n) => n===undefined?mi(x):`<msub>${mi(x)}${mn(n)}</msub>`;
const weighted = () => `${mi('z')}${mo('=')}${symbol('w',1)}${symbol('x',1)}${mo('+')}${symbol('w',2)}${symbol('x',2)}${mo('+')}${mi('b')}`;
const sigmoidExpression = exponent => `<mfrac>${mn(1)}<mrow>${mn(1)}${mo('+')}<msup><mi mathvariant="normal">e</mi>${exponent}</msup></mrow></mfrac>`;
const sigmoidGeneral = () => m(mi('σ')+'<mo stretchy="false">(</mo>'+mi('z')+'<mo stretchy="false">)</mo>'+mo('=')+sigmoidExpression(`<mrow>${mo('−')}${mi('z')}</mrow>`));

function concept() {
  const stage = (figure, label) => `<div class="lr-step"><div class="lr-figure">${figure}</div><div class="lr-step-label">${label}</div></div>`;
  return `<div class="lr-body"><section class="lr-panel lr-concept-panel">
    <div class="lr-concept-heading"><h2>로지스틱 회귀(Logistic Regression)</h2><span class="lr-example">이진 분류 · 확률 모델</span><p>양성(1)·음성(0) 중 양성의 확률을 예측하는 분류 모델</p></div>
    <div class="lr-flow">
      ${stage(`<div class="lr-inputs">${[1,2].map(i=>`<div><div class="lr-feature-value">${m(symbol('x',i))}</div></div>`).join('')}</div>`, '입력 특성')}
      ${arrow()}
      ${stage(`<div class="lr-score"><div class="lr-score-parameters"><span>가중치</span>${m(symbol('w',1)+mo(',')+symbol('w',2))}<span>· 절편</span>${m(mi('b'))}</div><div class="lr-score-general">${m(weighted())}</div><div class="lr-score-meaning">${m(mi('z'))}<span>확률 변환 전 점수</span></div></div>`, '가중합 + 절편')}
      ${arrow()}
      ${stage(`<div class="lr-sigmoid-stage"><div class="lr-sigmoid-formula">${sigmoidGeneral()}</div><svg class="lr-curve" role="img" aria-label="선형 점수를 양성 확률로 변환하는 시그모이드 곡선" viewBox="0 0 300 210"></svg></div>`, '시그모이드(Sigmoid)')}
      ${arrow()}
      ${stage(`<div class="lr-probability"><strong>${m(mi('p')+mo('=')+mi('σ')+'<mo stretchy="false">(</mo>'+mi('z')+'<mo stretchy="false">)</mo>')}</strong><span>0과 1 사이의 확률</span></div>`, '확률 출력')}
    </div>
    <div class="lr-symbols"><div><span>${m(mi('x'))} 입력 특성</span><small>대상의 속성을 수치로 표현</small></div><div><span>${m(mi('w'))} 특성에 곱하는 가중치</span><small>절편 ${m(mi('b'))}: 입력과 무관하게 더하는 값</small></div><div><span>${m(mi('σ'))} 시그모이드 함수</span><small>자연상수 ${m('<mi mathvariant="normal">e</mi>')} · 실수 점수를 0~1로 변환</small></div><div><span>${m(mi('p'))} 양성 예측 확률</span><small>확률과 최종 클래스 판정은 구분</small></div></div>
    </section></div>${takeaway('확률의 의미', '입력에서 계산한 선형 점수를 양성 클래스의 확률로 변환')}`;
}


function drawCurve(svg) {
  const x=z=>40+(z+4)/8*240,y=p=>172-p*150;
  const d=Array.from({length:161},(_,i)=>{const z=-4+i/20;return `${i?'L':'M'}${x(z).toFixed(3)},${y(1/(1+Math.exp(-z))).toFixed(3)}`;}).join(' ');
  svg.innerHTML=`<g class="lr-plot-grid"><path d="M40 22 V172 H280"/><path class="lr-midline" d="M40 ${y(.5)} H280 M${x(0)} 22 V172"/></g>
    <g class="lr-axis-text math-number">${[0,.5,1].map(p=>`<text x="30" y="${y(p)+5}" text-anchor="end">${p}</text>`).join('')}${[-4,0,4].map(z=>`<text x="${x(z)}" y="195" text-anchor="middle">${String(z).replace('-','−')}</text>`).join('')}<text x="42" y="10">𝑝</text><text x="291" y="176">𝑧</text></g>
    <path class="lr-sigmoid-path" d="${d}"/>`;
}

export function renderLesson(container) {
  const page=pages[0];
  container.innerHTML=`<section class="reference-section" id="ref-concept" aria-label="${page.name}"><div class="reference-viewport"><article class="slide reference-slide logistic-slide" data-page="concept"><header><div class="kicker">CONCEPT / 01</div><h1>${page.title}</h1><p class="subtitle">${page.subtitle}</p></header>${concept()}<footer class="footer"><span>Design Template Library · 로지스틱 회귀</span><span>01 / 01</span></footer></article></div></section>`;
  drawCurve(container.querySelector('.lr-curve'));
  return [...container.querySelectorAll('.reference-section')];
}
