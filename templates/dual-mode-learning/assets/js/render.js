import { lesson } from './lesson.js';
import { mountLab } from './lab.js';

export function renderLessons(container, mode) {
  lesson.sections.forEach((section, idx) => {
    const el = document.createElement('section');
    el.className = mode === 'slides' ? 'slide-sheet' : 'lesson-section';
    el.id = section.id;
    if (mode === 'slides') el.setAttribute('aria-hidden', 'true');
    const kindContents = {
      concept: `<div class="concept-card"><strong>KEY CONCEPT</strong>${section.body}</div>`,
      flow: `<div class="flow-graphic">
        <div class="flow-step"><div class="number">INPUT</div><b>5 × 5</b><p>25개 픽셀의 숫자</p></div>
        <div class="flow-arrow">→</div>
        <div class="flow-step"><div class="number">PROCESS</div><b>3 × 3 Kernel</b><p>원소별 곱의 합</p></div>
        <div class="flow-arrow">→</div>
        <div class="flow-step"><div class="number">OUTPUT</div><b>3 × 3</b><p>Feature Map</p></div>
      </div><div class="lesson-body">${section.body}</div>`,
      lab: `<div id="lab-${mode}" data-lab></div><div class="lesson-body" style="margin-top:12px">${section.body}</div>`,
      summary: `<div class="takeaway">${section.body}</div>`,
    };
    el.innerHTML = `<div class="section-kicker">${section.eyebrow}</div>
      <h2 class="lesson-title">${section.title}</h2>
      <p class="lesson-lead">${section.lead}</p>
      ${kindContents[section.kind]}
      <div class="scroll-note"><strong>조금 더 알아보기</strong><div>${section.scrollOnly}</div></div>
      ${section.kind === 'lab' ? '<p class="source-note">교육용 고정 필터를 사용한 직접 구현 예제입니다.</p>' : ''}
      ${mode === 'slides' ? `<span class="slide-number">${String(idx + 1).padStart(2,'0')} / ${String(lesson.sections.length).padStart(2,'0')}</span>` : ''}`;
    container.appendChild(el);
    if (section.kind === 'lab') mountLab(el.querySelector('[data-lab]'));
  });
  return lesson;
}
