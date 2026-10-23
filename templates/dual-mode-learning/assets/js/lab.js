import { readLabState, saveLabState } from './state.js';
// Same editable input and edge kernel as reference #4; one channel, S1/P0/bias0.
export const image = [
  [1,2,3,1,0], [4,5,6,2,1], [7,8,9,3,1], [2,1,0,4,2], [1,3,2,1,0],
];
export const kernels = {
  vertical: { label: '세로 경계', data: [[1,0,-1],[1,0,-1],[1,0,-1]], divisor: 1 },
  average: { label: '평균', data: [[1,1,1],[1,1,1],[1,1,1]], divisor: 9 },
  identity: { label: '중앙 픽셀', data: [[0,0,0],[0,1,0],[0,0,0]], divisor: 1 },
};
export const formatNumber = value => (Number.isInteger(value) ? String(value) : value.toFixed(2)).replace('-', '−');
export function products(kernel, x=0, y=0) {
  return kernel.data.flatMap((row, ky) => row.map((weight, kx) => ({
    input: image[y+ky][x+kx], weight, value: image[y+ky][x+kx]*weight,
  })));
}
export function convolution(kernel) {
  return Array.from({length:3}, (_,y) => Array.from({length:3}, (_,x) =>
    products(kernel,x,y).reduce((sum,p) => sum+p.value,0) / kernel.divisor));
}
export function matrixHtml(matrix, kind='input', position=null) {
  const columns = matrix[0].length;
  return `<div class="teaching-matrix size-${columns} ${kind}" role="group" aria-label="${columns}열 ${matrix.length}행 ${kind === 'input' ? '입력' : kind === 'output' ? '출력' : '커널'} 행렬">${matrix.flatMap((row,y) => row.map((value,x) => {
    const selected = position && (kind==='input' ? x>=position.x && x<position.x+3 && y>=position.y && y<position.y+3 : kind==='output' && x===position.x && y===position.y);
    const tone = kind==='input' ? 'input-value' : value>0 ? 'pos' : value<0 ? 'neg' : 'zero';
    return `<span class="teaching-cell ${tone}${selected ? (kind==='input' ? ' focus' : ' active') : ''}" data-value="${value}" aria-label="${y+1}행 ${x+1}열 ${formatNumber(value)}">${formatNumber(value)}</span>`;
  })).join('')}</div>`;
}
export function productHtml(kernel, x=0, y=0) {
  return `<div class="product-grid">${products(kernel,x,y).map(p => `<div><small>${formatNumber(p.input)} × ${formatNumber(p.weight)}</small><strong data-product="${p.value}">${formatNumber(p.value)}</strong></div>`).join('')}</div>`;
}
export function flowHtml(kernel, position={x:0,y:0}) {
  return `<div class="matrix-flow">
    <div class="matrix-node"><h3>입력 5×5</h3>${matrixHtml(image,'input',position)}</div>
    <span class="flow-connector" aria-hidden="true">${arrow()}</span>
    <div class="matrix-node"><h3>커널 3×3</h3>${matrixHtml(kernel.data,'kernel')}<small>${kernel.divisor===9 ? '곱의 합 ÷ 9' : '대응 원소의 곱을 합산'}</small></div>
    <span class="flow-connector" aria-hidden="true">${arrow()}</span>
    <div class="matrix-node"><h3>출력 3×3</h3>${matrixHtml(convolution(kernel),'output',position)}</div></div>`;
}
export function arrow() {
  return '<svg viewBox="0 0 32 16" aria-hidden="true"><path d="M1 8H30M24 2L30 8L24 14"/></svg>';
}
// Center arrows on the rendered matrices, rather than on label/card rectangles.
export function alignFlowArrows(root=document) {
  for (const flow of root.querySelectorAll('.matrix-flow,.process-graphic')) {
    const scale=flow.closest('.slide-sheet') ? flow.closest('.slide-sheet').getBoundingClientRect().width/1440 : 1;
    for (const link of flow.querySelectorAll('.flow-connector')) {
      const svg=link.querySelector('svg');svg.style.transform='';
      if(getComputedStyle(flow).gridTemplateColumns.split(' ').length===1) continue;
      const a=link.previousElementSibling?.querySelector('.teaching-matrix')?.getBoundingClientRect();
      const b=link.nextElementSibling?.querySelector('.teaching-matrix')?.getBoundingClientRect();
      if(!a?.width || !b?.width) continue;
      const r=svg.getBoundingClientRect();
      const target=(a.y+a.height/2+b.y+b.height/2)/2;
      svg.style.transform=`translateY(${(target-r.y-r.height/2)/scale}px)`;
    }
  }
}
export function mountLab(container) {
  let {filter, position:index} = readLabState();
  container.innerHTML = `<div class="lab-root figure-card">
    <div class="lab-header"><span class="panel-label">LIVE · CONVOLUTION</span><label class="lab-tools">필터 선택 <select data-role="kernel">${Object.entries(kernels).map(([key,k])=>`<option value="${key}">${k.label}</option>`).join('')}</select></label></div>
    <div class="work-layout"><div data-role="flow"></div><aside class="calculation"><h3>9개 원소별 곱</h3><div data-role="products"></div><div class="sum-result" data-role="formula" aria-live="polite"></div></aside></div>
    <div class="lab-footer"><div class="position-controls"><button type="button" data-role="prev">← 이전 위치</button><span data-role="position"></span><button type="button" data-role="next">다음 위치 →</button></div><span class="lab-status" data-role="result" aria-live="polite"></span><button type="button" data-role="reset">초기화</button></div></div>`;
  const $ = role => container.querySelector(`[data-role="${role}"]`);
  $('kernel').value=filter;
  function draw(persist=false) {
    const x=index%3, y=Math.floor(index/3), kernel=kernels[filter];
    const sum=products(kernel,x,y).reduce((a,p)=>a+p.value,0);
    $('flow').innerHTML=flowHtml(kernel,{x,y});
    $('products').innerHTML=productHtml(kernel,x,y);
    $('formula').innerHTML=`<span>곱의 합 ${formatNumber(sum)}${kernel.divisor===9 ? ' ÷ 9' : ''}</span><strong>= ${formatNumber(sum/kernel.divisor)}</strong>`;
    $('position').textContent=`${index+1} / 9`;
    $('result').textContent=`입력 시작: ${y+1}행 ${x+1}열 → 출력: ${y+1}행 ${x+1}열 · 값 ${formatNumber(sum/kernel.divisor)}`;
    $('prev').disabled=index===0; $('next').disabled=index===8;
    requestAnimationFrame(()=>alignFlowArrows(container));
    if (persist) saveLabState(filter,index);
  }
  $('kernel').addEventListener('change', e => { filter=e.target.value; draw(true); });
  $('prev').addEventListener('click', () => { index=Math.max(0,index-1); draw(true); });
  $('next').addEventListener('click', () => { index=Math.min(8,index+1); draw(true); });
  $('reset').addEventListener('click', () => { filter='vertical';index=0;$('kernel').value=filter;draw(true); });
  draw();
}
