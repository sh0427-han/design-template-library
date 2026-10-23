import { references } from './lesson.js';
import { readThreshold, setThreshold } from './state.js';
// Only remove the source page's outside gutter. Never override its design rules.
const placement = `html,body{min-height:0!important;width:1440px;height:810px;overflow:hidden;background:transparent}
.reference-deck{padding:0!important;min-height:0!important}
.reference-slide{zoom:1!important}`;
export function bindKeyboard(target,navigate) {
  target.addEventListener('keydown',event=>{
    if(event.target.closest('input,select,textarea,button,a,[contenteditable]') || event.altKey || event.ctrlKey || event.metaKey) return;
    const actions={ArrowRight:1,PageDown:1,' ':1,ArrowLeft:-1,PageUp:-1,Home:'first',End:'last'};
    if(event.key in actions){event.preventDefault();navigate(actions[event.key]);}
  });
}
export function ensureFrame(section, navigate=null) {
  const frame=section.querySelector('iframe');
  if(frame.hasAttribute('src')) return;
  frame.addEventListener('load', async()=>{
    const doc=frame.contentDocument, view=frame.contentWindow;
    if(view?.location.href==='about:blank')return;
    if(!doc?.querySelector('.reference-slide')) {section.dataset.failed='true';section.querySelector('.frame-status').textContent='원본을 불러오지 못했습니다. 새로고침해 주세요.';return;}
    const style=doc.createElement('style');style.dataset.modePlacement='true';style.textContent=placement;doc.head.appendChild(style);
    // Reuse #5's original event handler and calculations, including boundary values.
    const threshold=doc.querySelector('#threshold');
    if(threshold) {
      threshold.value=String(readThreshold());threshold.dispatchEvent(new view.Event('input',{bubbles:true}));
      threshold.addEventListener('input',()=>setThreshold(Number(threshold.value)));
    }
    if(navigate) bindKeyboard(doc,navigate);
    await doc.fonts.ready;
    await Promise.all([...doc.images].map(im=>im.decode().catch(()=>null)));
    section.dataset.ready='true';
    section.dispatchEvent(new CustomEvent('referenceready',{bubbles:true}));
  });
  frame.src=section.dataset.source;
}
export function renderReferences(container,mode,navigate=null) {
  const observer=new ResizeObserver(entries=>{
    for(const {target} of entries)target.style.setProperty('--reference-scale',target.clientWidth/1440);
  });
  for(const [i,ref] of references.entries()) {
    const section=document.createElement('section');section.id=`ref-${ref.id}`;
    section.className='reference-section';section.dataset.source=`../html/${ref.file}`;
    section.setAttribute('aria-label',`${i+1}. ${ref.name} · ${ref.title}`);
    if(mode==='slides')section.setAttribute('aria-hidden','true');
    section.innerHTML=`<div class="reference-viewport"><iframe title="${ref.name} · ${ref.title}" loading="${mode==='scroll'?'lazy':'eager'}"></iframe><p class="frame-status" role="status">불러오는 중…</p></div>`;
    container.appendChild(section);observer.observe(section.querySelector('.reference-viewport'));
    if(mode==='scroll')ensureFrame(section,navigate);
  }
  return [...container.querySelectorAll('.reference-section')];
}
