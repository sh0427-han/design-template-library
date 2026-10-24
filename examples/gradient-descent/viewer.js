const viewport=document.querySelector('.reference-viewport');
const frame=document.querySelector('iframe');
const status=document.querySelector('.frame-status');
new ResizeObserver(()=>viewport.style.setProperty('--scale',viewport.clientWidth/1440)).observe(viewport);
frame.addEventListener('load',async()=>{
  try {
    const doc=frame.contentDocument;
    if(!doc?.querySelector('.gd-slide')) throw new Error('Missing concept');
    const style=doc.createElement('style');style.dataset.modePlacement='true';
    style.textContent='html,body{min-height:0!important;width:1440px;height:810px;overflow:hidden;background:transparent}.reference-deck{padding:0!important;min-height:0!important}.reference-slide{zoom:1!important}';doc.head.append(style);
    await doc.fonts.ready;
    if(doc.querySelector('.gd-slide').dataset.ready!=='true') {
      await new Promise((resolve,reject)=>{
        const observer=new MutationObserver(()=>{
          const state=doc.querySelector('.gd-slide').dataset.ready;
          if(state==='true'){observer.disconnect();resolve();}
          if(state==='error'){observer.disconnect();reject(new Error('Plot failed'));}
        });observer.observe(doc.querySelector('.gd-slide'),{attributes:true,attributeFilter:['data-ready']});
        setTimeout(()=>{observer.disconnect();reject(new Error('Concept timeout'));},10000);
      });
    }
    await document.fonts.load('400 14px "Pretendard Variable"','Scroll Slide 경사하강법');await document.fonts.ready;
    viewport.dataset.ready='true';
  } catch {viewport.dataset.ready='error';status.textContent='슬라이드를 불러오지 못했습니다. 새로고침해 주세요.';}
});
frame.src='content.html';
