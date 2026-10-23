// One editable model for every figure, equation, sample row and output mode.
export const DEFAULT_MODEL = {
  weights: [1.2, -0.8], bias: 0.1,
  samples: [[-1, 1], [-0.5, 0.5], [0.25, 0.5], [1, 0.5], [1.5, 0.25], [2, 0.5]],
};

export function normalizeModel(input) {
  const finite = x => typeof x === 'number' && Number.isFinite(x);
  if (!Array.isArray(input?.weights) || input.weights.length !== 2 ||
      !input.weights.every(finite) || !finite(input.bias) ||
      !Array.isArray(input.samples) || !input.samples.length ||
      !input.samples.every(x => Array.isArray(x) && x.length === 2 && x.every(finite))) {
    throw new TypeError('두 개의 유한한 계수와 입력, 유한한 절편, 하나 이상의 샘플이 필요합니다.');
  }
  const model = {weights: [...input.weights], bias: input.bias, samples: input.samples.map(x => [...x])};
  if (model.samples.some(x => !Number.isFinite(model.weights[0]*x[0] + model.weights[1]*x[1] + model.bias))) {
    throw new RangeError('입력과 계수의 가중합이 유한한 범위를 벗어났습니다.');
  }
  return model;
}

export function sigmoid(z) {
  if (!Number.isFinite(z)) throw new RangeError('점수는 유한한 수여야 합니다.');
  if (z >= 0) return 1 / (1 + Math.exp(-z));
  const exp = Math.exp(z);
  return exp / (1 + exp);
}

export function evaluateModel(model) {
  return model.samples.map((input, index) => {
    const products = input.map((x, i) => x * model.weights[i]);
    const z = products[0] + products[1] + model.bias;
    return {index, input: [...input], products, z, p: sigmoid(z)};
  });
}

export function predict(p, threshold) { return p >= threshold ? 1 : 0; }
