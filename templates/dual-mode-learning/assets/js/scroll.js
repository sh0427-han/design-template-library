import { renderLessons } from './render.js';
import { updateModeLink } from './state.js';
const lesson=renderLessons(document.getElementById('lesson-root'),'scroll');
const toc=document.getElementById('toc-list');
lesson.sections.forEach(section=>{
  const a=document.createElement('a');a.href=`#${section.id}`;a.textContent=section.title;toc.appendChild(a);
});
const sections=[...document.querySelectorAll('.lesson-section')];
let active=lesson.sections.some(s=>s.id===location.hash.slice(1)) ? location.hash.slice(1) : lesson.sections[0].id;
function update() {
  const passed=sections.filter(s=>s.getBoundingClientRect().top<=150);
  active=(passed.at(-1)||sections[0]).id;
  for(const a of toc.querySelectorAll('a')) {
    if(a.hash===`#${active}`) a.setAttribute('aria-current','location');else a.removeAttribute('aria-current');
  }
  updateModeLink(active);
}
let scheduled=false;
window.addEventListener('scroll',()=>{if(!scheduled) { scheduled=true;requestAnimationFrame(()=>{update();scheduled=false;}); }},{passive:true});
window.addEventListener('lessonstatechange',()=>updateModeLink(active));
window.addEventListener('resize',update);
const target=sections.find(s=>s.id===location.hash.slice(1));
if(target) requestAnimationFrame(()=>{target.scrollIntoView();update();});else update();
document.title=`${lesson.topic} | 웹 교과서`;

document.querySelector('.chapter-head h1').textContent=lesson.topic;
document.querySelector('.chapter-head p').textContent=lesson.subtitle;
