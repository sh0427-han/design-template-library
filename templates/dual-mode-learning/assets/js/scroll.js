import { references, currentReference } from './lesson.js';
import { updateModeLink } from './state.js';
import { renderReferences } from './render.js';
const target=currentReference().id;
const sections=renderReferences(document.getElementById('lesson-root'),'scroll');
const toc=document.getElementById('toc-list');
references.forEach((ref,i)=>{
  const a=document.createElement('a');a.href=`#ref-${ref.id}`;
  a.innerHTML=`<span>${String(i+1).padStart(2,'0')}</span><span>${ref.name}</span>`;toc.appendChild(a);
});
let active=target;
function update() {
  const reached=sections.filter(s=>s.getBoundingClientRect().top<=140);
  active=(reached.at(-1)||sections[0]).id.slice(4);
  for(const a of toc.querySelectorAll('a')) {
    if(a.hash===`#ref-${active}`)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current');
  }
  updateModeLink(active);
}
let queued=false;
window.addEventListener('scroll',()=>{if(!queued){queued=true;requestAnimationFrame(()=>{update();queued=false;});}},{passive:true});
window.addEventListener('referencestatechange',()=>updateModeLink(active));
window.addEventListener('resize',update);
requestAnimationFrame(()=>{document.getElementById(`ref-${target}`).scrollIntoView();update();});
