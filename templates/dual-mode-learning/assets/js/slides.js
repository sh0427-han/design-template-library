import { renderLessons } from './render.js';
import { updateModeLink } from './state.js';
import { alignFlowArrows } from './lab.js';
const lesson=renderLessons(document.getElementById('slide-root'),'slides');
const slides=[...document.querySelectorAll('.slide-sheet')];
const progress=document.getElementById('progress');
const prev=document.getElementById('prev'), next=document.getElementById('next');
let current=Math.max(0,slides.findIndex(el=>`#${el.id}`===location.hash));
function goto(index, shouldHash=true) {
  current=Math.max(0,Math.min(slides.length-1,index));
  slides.forEach((el,i)=>el.setAttribute('aria-hidden',String(i!==current)));
  progress.textContent=`${current+1} / ${slides.length}`;
  document.getElementById('progress-fill').style.width=`${(current+1)*100/slides.length}%`;
  prev.disabled=current===0;next.disabled=current===slides.length-1;
  if(shouldHash) { const url=new URL(location.href);url.hash=slides[current].id;history.replaceState(null,'',url); }
  updateModeLink(slides[current].id);
  requestAnimationFrame(()=>alignFlowArrows(slides[current]));
}
prev.addEventListener('click',()=>goto(current-1));
next.addEventListener('click',()=>goto(current+1));
window.addEventListener('keydown',event=>{
  if(event.target.closest('input,select,textarea,button,a,[contenteditable]') || event.altKey || event.ctrlKey || event.metaKey) return;
  if(['ArrowRight','PageDown',' '].includes(event.key)) { event.preventDefault();goto(current+1); }
  if(['ArrowLeft','PageUp'].includes(event.key)) { event.preventDefault();goto(current-1); }
  if(event.key==='Home') { event.preventDefault();goto(0); }
  if(event.key==='End') { event.preventDefault();goto(slides.length-1); }
});
window.addEventListener('hashchange',()=>{const index=slides.findIndex(el=>el.id===location.hash.slice(1));if(index>=0) goto(index,false);});
window.addEventListener('lessonstatechange',()=>updateModeLink(slides[current].id));
const stage=document.querySelector('.slide-stage');
function fit() { document.documentElement.style.setProperty('--slide-scale', Math.min((stage.clientWidth-32)/1440,(stage.clientHeight-24)/810));requestAnimationFrame(()=>alignFlowArrows(slides[current])); }
new ResizeObserver(fit).observe(stage);
fit();goto(current);
document.title=`${lesson.topic} | 발표 슬라이드`;
