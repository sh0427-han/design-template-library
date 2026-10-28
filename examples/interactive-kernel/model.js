/* Domain-specific, side-effect-free cross-correlation model. */
(function (root) {
  'use strict';
  const IDS = ['identity', 'mean', 'edge'];
  const FOCUS = Object.freeze({ row: 2, col: 1 });
  const INPUT_SIZE = 7;

  function validateMatrix(matrix, height, width, rule, label) {
    if (!Array.isArray(matrix) || matrix.length !== height ||
        matrix.some(row => !Array.isArray(row) || row.length !== width ||
          row.some(value => !rule(value)))) {
      throw new TypeError(`${label}: ${height}×${width} 유효한 정수 행렬이 필요합니다.`);
    }
    return matrix.map(row => row.slice());
  }

  function validateData(data) {
    if (!data || typeof data !== 'object' || !data.kernels) {
      throw new TypeError('입력 데이터 또는 필터 목록이 없습니다.');
    }
    const input = validateMatrix(data.input, INPUT_SIZE, INPUT_SIZE,
      n => Number.isInteger(n) && n >= 0 && n <= 9, '입력');
    const kernels = {};
    IDS.forEach(id => {
      const k = data.kernels[id];
      if (!k || typeof k.name !== 'string' || !k.name.trim() ||
          typeof k.description !== 'string' || !k.description.trim() ||
          !Number.isSafeInteger(k.divisor) || k.divisor <= 0) {
        throw new TypeError(`${id}: 필터 정보 또는 양의 정수 분모 오류`);
      }
      kernels[id] = {
        name: k.name,
        description: k.description,
        divisor: k.divisor,
        numerators: validateMatrix(k.numerators, 3, 3,
          n => Number.isSafeInteger(n) && n >= -2 && n <= 2,
          `${id} 커널`)
      };
    });
    return { input, kernels };
  }

  function correlate(input, numerators, divisor = 1) {
    if (!Array.isArray(input) || input.length < 3 ||
        !Number.isSafeInteger(divisor) || divisor <= 0) {
      throw new TypeError('교차상관 입력 또는 분모 오류');
    }
    const width = input[0]?.length;
    if (!Number.isInteger(width) || width < 3 || input.some(row =>
      !Array.isArray(row) || row.length !== width ||
      row.some(n => !Number.isSafeInteger(n)))) {
      throw new TypeError('동일 길이의 정수 입력 행렬이 필요합니다.');
    }
    const kernel = validateMatrix(numerators, 3, 3,
      Number.isSafeInteger, '커널');
    const outputNumerators = [];
    for (let r = 0; r <= input.length - 3; r++) {
      const outputRow = [];
      for (let c = 0; c <= width - 3; c++) {
        let sum = 0;
        for (let i = 0; i < 3; i++) {
          for (let j = 0; j < 3; j++) {
            sum += input[r+i][c+j] * kernel[i][j];
          }
        }
        if (!Number.isSafeInteger(sum)) throw new RangeError('정수 안전 범위를 초과했습니다.');
        outputRow.push(sum);
      }
      outputNumerators.push(outputRow);
    }
    return {
      outputNumerators,
      output: outputNumerators.map(row => row.map(value => value / divisor))
    };
  }

  function formatValue(value) {
    if (!Number.isFinite(value)) throw new TypeError('유한한 수만 표시할 수 있습니다.');
    const shown = Math.round((value + Number.EPSILON) * 100) / 100;
    return Object.is(shown, -0) ? '0' : Number.isInteger(shown) ? String(shown) : shown.toFixed(2);
  }

  function colorFor(value) {
    if (!Number.isFinite(value)) throw new TypeError('색상 값 오류');
    const t = Math.min(1, Math.abs(value) / 36);
    const anchor = value < 0 ? [38,166,161] : [49,104,200];
    const rgb = anchor.map(channel => Math.round(255 + (channel - 255) * t));
    return `rgb(${rgb.join(', ')})`;
  }

  function evaluate(data, kernelId) {
    if (!IDS.includes(kernelId)) throw new RangeError('알 수 없는 필터 ID입니다.');
    const valid = validateData(data);
    const selected = valid.kernels[kernelId];
    const { outputNumerators, output } = correlate(
      valid.input, selected.numerators, selected.divisor);
    const { row, col } = FOCUS;
    const patch = valid.input.slice(row, row+3).map(values => values.slice(col, col+3));
    const products = patch.map((values,i) => values.map((n,j) => n*selected.numerators[i][j]));
    const numerator = products.flat().reduce((sum,n) => sum+n,0);
    const raw = numerator / selected.divisor;
    if (numerator !== outputNumerators[row][col]) throw new Error('선택 영역 계산 불일치');
    return {
      input: valid.input,
      kernelId,
      kernelName: selected.name,
      kernelDescription: selected.description,
      kernelNumerators: selected.numerators,
      divisor: selected.divisor,
      outputNumerators,
      output,
      focus: { row, col, patch, products, numerator,
        denominator: selected.divisor, raw, display: formatValue(raw) }
    };
  }

  const api = Object.freeze({ validateData, correlate, evaluate, colorFor, formatValue });
  root.KernelModel = api;
  if (typeof module === 'object' && module.exports) module.exports = api;
})(globalThis);
