import { renderLessons } from './render.js';
const lesson = renderLessons(document.getElementById('lesson-root'), 'scroll');
const toc = document.getElementById('toc-list');
lesson.sections.forEach(section => {
  const a = document.createElement('a');
  a.href = `#${section.id}`;
  a.textContent = section.title;
  toc.appendChild(a);
});
document.title = `${lesson.topic} | 웹 교과서`;
