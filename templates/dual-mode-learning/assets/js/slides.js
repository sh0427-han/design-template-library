import { renderLessons } from './render.js';
const lesson = renderLessons(document.getElementById('slide-root'), 'slides');
const slides = [...document.querySelectorAll('.slide-sheet')];
const progress = document.getElementById('progress');
const progressFill = document.getElementById('progress-fill');
const prev = document.getElementById('prev');
const next = document.getElementById('next');
let current = Math.max(0, slides.findIndex(el => `#${el.id}` === location.hash));
function goto(index, shouldHash = true) {
  current = Math.max(0, Math.min(slides.length - 1, index));
  slides.forEach((el, i) => el.setAttribute('aria-hidden', String(i !== current)));
  progress.textContent = `${current + 1} / ${slides.length}`;
  progressFill.style.width = `${(current+1)*100/slides.length}%`;
  prev.disabled = current === 0;
  next.disabled = current === slides.length - 1;
  if (shouldHash) history.replaceState(null, '', `#${slides[current].id}`);
}
prev.addEventListener('click', () => goto(current - 1));
next.addEventListener('click', () => goto(current + 1));
window.addEventListener('keydown', event => {
  const tag = event.target?.tagName;
  if (['INPUT', 'SELECT', 'TEXTAREA', 'BUTTON'].includes(tag) || event.altKey || event.ctrlKey || event.metaKey) return;
  if (['ArrowRight', 'PageDown', ' '].includes(event.key)) { event.preventDefault(); goto(current + 1); }
  if (['ArrowLeft', 'PageUp'].includes(event.key)) { event.preventDefault(); goto(current - 1); }
  if (event.key === 'Home') { event.preventDefault(); goto(0); }
  if (event.key === 'End') { event.preventDefault(); goto(slides.length - 1); }
});
window.addEventListener('hashchange', () => {
  const id = location.hash.slice(1);
  const index = slides.findIndex(el => el.id === id);
  if (index >= 0) goto(index, false);
});
goto(current);
document.title = `${lesson.topic} | 발표 슬라이드`;
