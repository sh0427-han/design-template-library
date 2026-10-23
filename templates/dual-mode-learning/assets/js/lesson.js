// The editable reference pages are the only source of figures, text and math.
export const references = [
  { id:'concept', name:'Concept', title:'이미지와 픽셀', file:'concept.html' },
  { id:'process', name:'Process', title:'입력에서 예측까지', file:'process.html' },
  { id:'comparison', name:'Comparison', title:'규칙 기반과 머신러닝', file:'comparison.html' },
  { id:'step-by-step', name:'Step-by-Step', title:'필터의 곱셈과 합산', file:'step-by-step.html' },
  { id:'interactive', name:'Interactive', title:'임계값과 예측 변화', file:'interactive.html' },
  { id:'architecture', name:'Architecture', title:'CNN 구조와 차원', file:'architecture.html' },
  { id:'experiment', name:'Experiment', title:'혼동행렬과 평가 지표', file:'experiment.html' },
  { id:'executive-summary', name:'Executive Summary', title:'지표와 후속 조치', file:'executive-summary.html' },
];
export function currentReference() {
  const hash=location.hash.slice(1);
  const legacy={motivation:'concept',locality:'step-by-step',pipeline:'process',experiment:'interactive',takeaway:'comparison'};
  const id=hash.startsWith('ref-') ? hash.slice(4) : (legacy[hash] || hash);
  return references.find(r=>r.id===id) || references[0];
}
