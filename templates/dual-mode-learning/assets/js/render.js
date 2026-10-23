import { lesson } from './lesson.js';
import { image, kernels, convolution, matrixHtml, productHtml, flowHtml, arrow, mountLab, alignFlowArrows } from './lab.js';
const kernel=kernels.vertical;
const contents = {
  motivation: () => `<div class="motivation-layout">
    <article class="figure-card input-card"><div class="panel-label">INPUT · 단일 채널</div><h3>이웃한 3×3 픽셀</h3>${matrixHtml(image,'input',{x:0,y:0})}<p class="figure-note">파란 테두리: 함께 계산할 영역</p></article>
    <article class="figure-card relation-card"><div class="panel-label">LOCAL PATTERN</div><h3>주변 관계를 계산하는 필터</h3>
    <div class="explanation-row"><span>01</span><div><b>입력</b><p>5×5 배열에서 작은 영역 선택</p></div></div>
    <div class="explanation-row"><span>02</span><div><b>계산</b><p>3×3 커널의 대응 가중치를 곱하고 합산</p></div></div>
    <div class="explanation-row"><span>03</span><div><b>응답</b><p>밝기 변화에 대한 반응을 출력 한 칸에 기록</p></div></div></article></div>`,
  locality: () => `<div class="figure-card"><div class="panel-label">첫 위치 · 입력 1행 1열 → 출력 1행 1열</div><div class="work-layout">${flowHtml(kernel)}<aside class="calculation"><h3>9개 원소별 곱</h3>${productHtml(kernel)}<div class="sum-result"><span>1 + 0 − 3 + 4 + 0 − 6 + 7 + 0 − 9</span><strong>= −6</strong></div></aside></div></div>`,
  flow: () => `<div class="figure-card process-card"><div class="process-graphic">
    <article class="process-panel"><div class="panel-label">INPUT</div><h3>5 × 5</h3>${matrixHtml(image,'input',{x:0,y:0})}<small>단일 채널 · 25개 값</small></article>
    <span class="flow-connector" aria-hidden="true">${arrow()}</span>
    <article class="process-panel process-center"><div class="panel-label">FILTER APPLICATION</div><h3>3 × 3 커널</h3>${matrixHtml(kernel.data,'kernel')}<small>Stride 1 · Padding 0</small></article>
    <span class="flow-connector" aria-hidden="true">${arrow()}</span>
    <article class="process-panel"><div class="panel-label">FEATURE MAP</div><h3>3 × 3</h3>${matrixHtml(convolution(kernel),'output',{x:0,y:0})}<small>각 위치의 계산값 · 9개</small></article></div>
    <div class="size-equation"><span>출력 한 변</span><strong>(5 + 2 × 0 − 3) / 1 + 1 = 3</strong><span>가로·세로 각각 3칸</span></div></div>`,
  lab: () => '<div data-lab></div>',
  summary: () => `<div class="feature-gallery">${Object.entries(kernels).map(([key,k])=>`<article class="figure-card feature-preview" data-filter="${key}"><div class="panel-label">${key.toUpperCase()} FILTER</div><h3>${k.label}</h3><p class="filter-description">${key==='vertical' ? '좌측 합 − 우측 합' : key==='average' ? '주변 값의 평균' : '중앙의 원래 값 유지'}</p>${matrixHtml(convolution(k),'output')}<div class="comparison-value"><span>좌상단 출력</span><strong>${convolution(k)[0][0].toFixed(0).replace('-','−')}</strong></div></article>`).join('')}</div>`,
};
export function renderLessons(container, mode) {
  lesson.sections.forEach((section,index)=>{
    const el=document.createElement('section');
    el.className=`${mode==='slides' ? 'slide-sheet' : 'lesson-section'} kind-${section.kind}`;
    el.id=section.id;
    if(mode==='slides') el.setAttribute('aria-hidden','true');
    el.innerHTML=`<header class="lesson-header"><div class="section-kicker">${section.eyebrow}</div><h2 class="lesson-title">${section.title}</h2><p class="lesson-lead">${section.lead}</p></header>
      <div class="lesson-content">${contents[section.kind]()}<div class="lesson-details">${section.detail}</div><div class="scroll-note"><b>조금 더 알아보기</b><p>${section.scrollOnly}</p></div></div>
      <div class="lesson-takeaway"><span>핵심</span><strong>${section.takeaway}</strong></div>
      <footer class="lesson-footer"><span>CONVOLUTION · S1 / P0</span><span>${String(index+1).padStart(2,'0')} / ${String(lesson.sections.length).padStart(2,'0')}</span></footer>`;
    container.appendChild(el);
    if(section.kind==='lab') mountLab(el.querySelector('[data-lab]'));
  });
  document.fonts.ready.then(()=>requestAnimationFrame(()=>alignFlowArrows(container)));
  window.addEventListener('resize',()=>requestAnimationFrame(()=>alignFlowArrows(container)));
  return lesson;
}
