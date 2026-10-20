// Convolution demonstrator: one input channel, stride=1, padding=0.
const image = [
  [1, 1, 1, 1, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 1, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 1, 1, 1, 1],
];
const kernels = {
  average: { label: '평균 필터 (1/9)', data: [[1,1,1],[1,1,1],[1,1,1]], divisor: 9 },
  vertical: { label: '세로 경계 필터', data: [[-1,0,1],[-1,0,1],[-1,0,1]], divisor: 1 },
  identity: { label: '중앙 픽셀 통과', data: [[0,0,0],[0,1,0],[0,0,0]], divisor: 1 },
};
function convolution(kernel) {
  const output = [];
  for (let y = 0; y < 3; y++) {
    const row = [];
    for (let x = 0; x < 3; x++) {
      let sum = 0;
      for (let ky = 0; ky < 3; ky++) {
        for (let kx = 0; kx < 3; kx++) {
          sum += image[y + ky][x + kx] * kernel.data[ky][kx];
        }
      }
      row.push(sum / kernel.divisor);
    }
    output.push(row);
  }
  return output;
}
function formatNumber(value) {
  return Number.isInteger(value) ? String(value) : value.toFixed(2);
}
function matrixHtml(matrix, columns, kind, selectedPosition, offset) {
  const cells = matrix.flatMap((row, y) => row.map((value, x) => {
    const inSelection = columns === 5 && x >= selectedPosition.x &&
      x < selectedPosition.x + 3 && y >= selectedPosition.y && y < selectedPosition.y + 3;
    const outSelection = columns === 3 && kind === 'output' &&
      x === selectedPosition.x && y === selectedPosition.y;
    const color = kind === 'input' ? (value ? 'color:#fff;background:#62758f' : 'color:#3e5068;background:#e8edf4') : '';
    return `<div class="cell${inSelection ? ' selected' : ''}${outSelection ? ' active' : ''}" style="${color}" aria-label="${x + offset}열 ${y + offset}행, 값 ${formatNumber(value)}">${formatNumber(value)}</div>`;
  }));
  return `<div class="matrix in${columns}${kind === 'output' ? ' output' : ''}">${cells.join('')}</div>`;
}
export function mountLab(container) {
  let filter = 'average';
  let index = 0;
  container.innerHTML = `<div class="lab-root">
    <div class="lab-header"><span class="lab-name">LIVE · Convolution Lab</span>
    <div class="lab-tools"><label for="kernel-${container.id}">필터</label><select id="kernel-${container.id}" data-role="kernel">
    ${Object.entries(kernels).map(([key, v]) => `<option value="${key}">${v.label}</option>`).join('')}
    </select></div></div>
    <div class="lab-grid">
      <div class="lab-pane"><h4>INPUT · 5×5</h4><div data-role="input"></div></div>
      <div class="lab-pane"><h4>KERNEL · 3×3</h4><div data-role="filter"></div></div>
      <div class="lab-pane"><h4>OUTPUT · 3×3</h4><div data-role="output"></div></div>
    </div>
    <div class="lab-footer"><div><button type="button" data-role="prev">← 이전 위치</button> <button type="button" data-role="next">다음 위치 →</button></div>
      <button type="button" data-role="reset" aria-label="필터와 위치를 초기화">초기화</button><span class="lab-result" data-role="result" aria-live="polite"></span></div>
    <div class="lab-hint">주황색 영역이 현재 연산할 입력 부분입니다. (Stride=1, Padding=0)</div>
    <div class="lab-formula" data-role="formula"></div>
  </div>`;
  const $ = role => container.querySelector(`[data-role="${role}"]`);
  function draw() {
    const x = index % 3;
    const y = Math.floor(index / 3);
    const kernel = kernels[filter];
    const output = convolution(kernel);
    const pos = {x, y};
    $('input').innerHTML = matrixHtml(image, 5, 'input', pos, 1);
    $('filter').innerHTML = matrixHtml(kernel.data, 3, 'filter', pos, 1);
    $('output').innerHTML = matrixHtml(output, 3, 'output', pos, 1);
    $('result').textContent = `위치 (${x+1}, ${y+1}) · 출력값 ${formatNumber(output[y][x])}`;
    $('formula').textContent = `3×3 원소별 곱의 합 ÷ ${kernel.divisor} = ${formatNumber(output[y][x])}`;
    $('prev').disabled = index === 0;
    $('next').disabled = index === 8;
  }
  $('kernel').addEventListener('change', event => { filter = event.target.value; draw(); });
  $('reset').addEventListener('click', () => {
    filter = 'average'; index = 0; $('kernel').value = filter; draw();
  });
  $('prev').addEventListener('click', () => { index = Math.max(0, index - 1); draw(); });
  $('next').addEventListener('click', () => { index = Math.min(8, index + 1); draw(); });
  draw();
}
