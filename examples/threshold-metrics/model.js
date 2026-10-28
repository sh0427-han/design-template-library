/* Synthetic score evaluation. Integer units keep the inclusive boundary exact. */
(function (root) {
  'use strict';
  function validateSamples(input) {
    if (!Array.isArray(input) || input.length > 16) throw new Error('샘플은 최대 16개인 배열이어야 합니다.');
    const ids = new Set();
    return input.map(item => {
      if (!item || typeof item.id !== 'string' || !item.id.trim() || ids.has(item.id)) throw new Error('샘플 ID는 비어 있지 않은 고유 문자열이어야 합니다.');
      if (!Number.isInteger(item.scoreUnits) || item.scoreUnits < 0 || item.scoreUnits > 100) throw new Error('점수 단위는 0~100 정수여야 합니다.');
      if (item.truth !== 0 && item.truth !== 1) throw new Error('실제값은 숫자 0 또는 1이어야 합니다.');
      ids.add(item.id);
      return {id:item.id, scoreUnits:item.scoreUnits, truth:item.truth};
    });
  }
  function validateThreshold(value) {
    if (!Number.isInteger(value) || value < 0 || value > 100) throw new Error('임계값 단위는 0~100 정수여야 합니다.');
    return value;
  }
  function evaluate(samples, thresholdUnits) {
    validateThreshold(thresholdUnits);
    const counts = {tp:0,fp:0,fn:0,tn:0};
    const predictions = samples.map(sample => {
      const prediction = Number(sample.scoreUnits >= thresholdUnits);
      const type = sample.truth ? (prediction ? 'TP' : 'FN') : (prediction ? 'FP' : 'TN');
      counts[type.toLowerCase()]++;
      return {...sample,prediction,type};
    });
    const {tp,fp,fn,tn}=counts;
    const fractions={
      precision:{numerator:tp,denominator:tp+fp},
      recall:{numerator:tp,denominator:tp+fn},
      accuracy:{numerator:tp+tn,denominator:samples.length},
      f1:{numerator:2*tp,denominator:2*tp+fp+fn}
    };
    const metrics=Object.fromEntries(Object.entries(fractions).map(([name,f])=>[name,f.denominator ? f.numerator/f.denominator : null]));
    return {predictions,counts,fractions,metrics};
  }
  function percent(fraction) {
    return fraction.denominator ? (Math.round(fraction.numerator*1000/fraction.denominator)/10).toFixed(1)+'%' : '—';
  }
  const api={validateSamples,validateThreshold,evaluate,percent};
  root.ThresholdMetricsModel=api;
  if(typeof module==='object' && module.exports) module.exports=api;
})(globalThis);
