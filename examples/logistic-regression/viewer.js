import {getPages, renderLesson, refreshFigureLinks} from './lesson.js';

try {
  const mode=document.body.dataset.mode;
  const query=new URLSearchParams(location.search),rawThreshold=query.get('threshold'),rawSample=query.get('sample');
  const includeAppendix=query.get('appendix')==='1',pages=getPages(includeAppendix);
  const threshold=rawThreshold!==null&&/^(100|\d{1,2})$/.test(rawThreshold)?Number(rawThreshold):60;
  const sample=rawSample!==null&&/^[1-6]$/.test(rawSample)?Number(rawSample)-1:3;
  const sections=renderLesson(document.querySelector('[data-lesson-root]'),{threshold,sample,includeAppendix});
  const indexFromHash=()=>Math.max(0,pages.findIndex(p=>location.hash===`#ref-${p.id}`));
  let current=indexFromHash();
  const observer=new ResizeObserver(entries=>{for(const {target} of entries)target.style.setProperty('--reference-scale',target.clientWidth/1440);refreshFigureLinks();});
  sections.forEach(s=>observer.observe(s.querySelector('.reference-viewport')));

  function save() {
    const state=window.LogisticLesson.state,url=new URL(location.href);
    url.searchParams.set('threshold',String(state.threshold));url.searchParams.set('sample',String(state.selected+1));url.hash=`ref-${pages[current].id}`;
    history.replaceState(null,'',url);
    const target=new URL(mode==='slides'?'scroll.html':'slides.html',url);target.search=url.search;target.hash=url.hash;
    document.querySelector('.mode-link').href=target.href;
    const appendixTarget=new URL(url);appendixTarget.searchParams.delete('appendix');
    if(!includeAppendix){appendixTarget.searchParams.set('appendix','1');appendixTarget.hash='ref-threshold';}
    else if(current===2)appendixTarget.hash='ref-calculation';
    const appendixLink=document.querySelector('.appendix-link');appendixLink.href=appendixTarget.href;appendixLink.textContent=includeAppendix?'본편 2장으로':'선택 부록 · 임계값';
  }
  function navigate(index,scroll=true) {
    current=Math.max(0,Math.min(pages.length-1,index));
    if(mode==='slides') {
      sections.forEach((s,i)=>{s.setAttribute('aria-hidden',String(i!==current));s.inert=i!==current;});
      document.getElementById('prev').disabled=current===0;document.getElementById('next').disabled=current===pages.length-1;
      document.getElementById('current-title').textContent=pages[current].name;
      document.getElementById('progress').textContent=current===2?'부록 A':`${current+1} / 2${includeAppendix?' · 부록 포함':''}`;
    } else {
      document.querySelectorAll('#toc-list a').forEach((a,i)=>{if(i===current)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current');});
      if(scroll)sections[current].scrollIntoView();
    }
    save();
    refreshFigureLinks();
  }
  if(mode==='slides') {
    document.getElementById('prev').addEventListener('click',()=>navigate(current-1));
    document.getElementById('next').addEventListener('click',()=>navigate(current+1));
    document.addEventListener('keydown',event=>{
      if(event.target.closest('input,select,textarea,button,a,[contenteditable]')||event.altKey||event.ctrlKey||event.metaKey)return;
      const targets={ArrowRight:current+1,PageDown:current+1,' ':current+1,ArrowLeft:current-1,PageUp:current-1,Home:0,End:pages.length-1};
      if(event.key in targets){event.preventDefault();navigate(targets[event.key]);}
    });
  } else {
    const toc=document.getElementById('toc-list');
    toc.innerHTML=pages.map((p,i)=>`<a href="#ref-${p.id}"><span>${i===2?'A':String(i+1).padStart(2,'0')}</span><span>${p.name}</span></a>`).join('');
    let scheduled=false;
    window.addEventListener('scroll',()=>{if(!scheduled){scheduled=true;requestAnimationFrame(()=>{
      scheduled=false;
      const atEnd=document.documentElement.scrollHeight-innerHeight-scrollY<=2;
      const reached=sections.filter(s=>s.getBoundingClientRect().top<=140);
      navigate(atEnd?sections.length-1:Math.max(0,sections.indexOf(reached.at(-1)||sections[0])),false);
    });}},{passive:true});
  }
  window.addEventListener('hashchange',()=>navigate(indexFromHash()));
  document.addEventListener('lessonstatechange',save);
  navigate(current);
  await document.fonts.ready;
  await new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)));
  if(mode==='scroll')navigate(current);
  document.documentElement.dataset.ready='true';
} catch(error) {
  document.documentElement.dataset.ready='error';
  const message=document.createElement('p');message.className='lr-load-error';message.setAttribute('role','alert');message.textContent='자료를 불러오지 못했습니다. 새로고침 후 다시 확인해 주세요.';document.body.prepend(message);
  console.error(error);
}
