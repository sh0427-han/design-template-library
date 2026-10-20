import { lesson } from './lesson.js';
import { image, kernels, convolution, mountLab } from './lab.js';

function grid(matrix, options = {}) {
  const { active = false, selected = false, className = '' } = options;
  const n = matrix.length;
  return `<div class="teaching-matrix size-${n} ${className}" aria-label="${n}x${n} 수치 행렬">
    ${matrix.flatMap((row, y) => row.map((v, x) => {
      const focus = selected && x < 3 && y < 3;
      const value = Number.isInteger(v) ? String(v) : v.toFixed(2);
      const tone = active ? (v > 0 ? 'pos' : v < 0 ? 'neg' : 'zero') : (v ? 'ink' : 'light');
      return `<span class="teaching-cell ${tone}${focus ? ' focus' : ''}">${value}</span>`;
    })).join('')}</div>`;
}

function previewCard(key, label, detail) {
  const values = convolution(kernels[key]);
  return `<article class="feature-preview"><div class="preview-heading"><strong>${label}</strong><small>${detail}</small></div>
    ${grid(values, {active:true, className:'compact-grid'})}</article>`;
}

const contents = {
  motivation: () => `<div class="learning-content motivation-layout">
    <div class="explain-visual"><div class="panel-label">INPUT / 5×5 PIXELS</div><div class="picture-demo">
    ${grid(image,{selected:true})}<div class="picture-legend"><span class="legend-key"></span>선택된 3×3 이웃 픽셀</div></div></div>
    <div class="explain-detail"><div class="panel-label">WHY LOCAL PATTERNS?</div>
      <h3>픽셀 하나가 아니라<br>주변 관계를 계산</h3>
      <div class="numbered-note"><span>01</span><div><b>입력</b><p>밝기 값이 0과 1로 표현된 5×5 이미지</p></div></div>
      <div class="numbered-note"><span>02</span><div><b>관찰</b><p>이웃한 3×3 픽셀의 밝기 차이</p></div></div>
      <div class="numbered-note"><span>03</span><div><b>추출</b><p>필터의 응답을 새 숫자 배열로 저장</p></div></div>
    </div></div><div class="teaching-insight">핵심 원리 <strong>주변 픽셀의 관계가 이미지의 특징을 결정합니다.</strong></div>`,
  locality: () => `<div class="learning-content locality-layout"><article class="local-visual">
    <div class="panel-label">FIRST WINDOW / X=1, Y=1</div>${grid(image,{selected:true})}
    <div class="position-label">주황색 3×3 영역에 같은 필터를 적용</div></article>
    <article class="math-card"><div class="panel-label">3×3 AVERAGE KERNEL</div>
      <div class="small-math-grid">${grid(Array.from({length:3},()=>[1,1,1]))}<span class="math-division">÷ 9</span></div>
      <div class="calculation-path"><span>6개의 1</span><span>× 1</span><span>÷ 9</span><strong>0.67</strong></div>
      <div class="math-bottom">이동 후 다음 영역은 <strong>4 ÷ 9 ≈ 0.44</strong></div>
    </article></div><div class="teaching-insight">Weight Sharing <strong>필터의 값은 그대로 두고, 입력 영역만 이동합니다.</strong></div>`,
  flow: () => `<div class="learning-content process-block"><div class="process-graphic">
    <article class="process-panel"><div class="panel-label">INPUT</div><strong>5 × 5</strong>
      ${grid(image,{className:'tiny-grid'})}<small>25개 픽셀</small></article>
    <div class="diagram-arrow" aria-hidden="true">→</div>
    <article class="process-panel process-center"><div class="panel-label">KERNEL</div><strong>3 × 3</strong>
      ${grid(Array.from({length:3},()=>[1,1,1]),{className:'tiny-grid'})}<small>Stride 1 · Padding 0</small></article>
    <div class="diagram-arrow" aria-hidden="true">→</div>
    <article class="process-panel process-result"><div class="panel-label">FEATURE MAP</div><strong>3 × 3</strong>
      ${grid(convolution(kernels.average),{active:true,className:'tiny-grid'})}<small>9개 출력값</small></article>
  </div><div class="size-equation"><div><span>OUTPUT SIZE</span><strong>(5 − 3) ÷ 1 + 1 = 3</strong></div><p>출력은 가로·세로 각각 3칸</p></div></div>`,
  lab: () => '<div data-lab></div>',
  summary: () => `<div class="learning-content feature-block"><div class="feature-gallery">
    ${previewCard('average','평균 필터','주변 밝기의 평균')}
    ${previewCard('vertical','세로 경계 필터','좌우 밝기 차이')}
    ${previewCard('identity','중앙 픽셀','원래 값 유지')}
  </div><div class="feature-flow"><span>INPUT IMAGE</span><b>→</b><span>LEARNED FILTERS</span><b>→</b><span>FEATURE MAPS</span><b>→</b><span>NEXT CNN LAYER</span></div></div>`,
};

export function renderLessons(container, mode) {
  lesson.sections.forEach((section, index) => {
    const el = document.createElement('section');
    el.className = mode === 'slides' ? 'slide-sheet' : 'lesson-section';
    el.classList.add(`kind-${section.kind}`);
    el.id = section.id;
    if (mode === 'slides') el.setAttribute('aria-hidden', 'true');
    el.innerHTML = `<div class="section-kicker">${section.eyebrow}</div>
      <h2 class="lesson-title">${section.title}</h2>
      <p class="lesson-lead">${section.lead}</p>
      ${contents[section.kind]()}
      <div class="lesson-body">${section.body}</div>
      <div class="scroll-note"><strong>조금 더 알아보기</strong><div>${section.scrollOnly}</div></div>
      ${mode === 'slides' ? `<span class="slide-number">${String(index+1).padStart(2,'0')} / ${String(lesson.sections.length).padStart(2,'0')}</span>` : ''}`;
    container.appendChild(el);
    if (section.kind === 'lab') mountLab(el.querySelector('[data-lab]'));
  });
  return lesson;
}
