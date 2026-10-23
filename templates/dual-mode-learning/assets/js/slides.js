import { references, currentReference } from './lesson.js';
import { updateModeLink, setReference } from './state.js';
import { renderReferences, ensureFrame, bindKeyboard } from './render.js';
let current=references.findIndex(r=>r.id===currentReference().id);
const prev=document.getElementById('prev'),next=document.getElementById('next');
const navigate=action=>goto(action==='first'?0:action==='last'?references.length-1:current+action);
const sections=renderReferences(document.getElementById('slide-root'),'slides',navigate);
function goto(index,save=true) {
  current=Math.max(0,Math.min(references.length-1,index));
  sections.forEach((section,i)=>section.setAttribute('aria-hidden',String(i!==current)));
  ensureFrame(sections[current],navigate);
  const ref=references[current];
  document.getElementById('progress').textContent=`${current+1} / ${references.length}`;
  document.getElementById('current-title').textContent=ref.name;
  prev.disabled=current===0;next.disabled=current===references.length-1;
  if(save)setReference(ref.id);else updateModeLink(ref.id);
  document.title=`${ref.name} | Slide`;
}
prev.addEventListener('click',()=>navigate(-1));next.addEventListener('click',()=>navigate(1));
bindKeyboard(document,navigate);
window.addEventListener('hashchange',()=>goto(references.findIndex(r=>r.id===currentReference().id),false));
window.addEventListener('referencestatechange',()=>updateModeLink(references[current].id));
goto(current);
