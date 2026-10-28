(() => {
  'use strict';
  const frame=document.querySelector('.frame');
  const iframe=frame.querySelector('iframe');
  const valid=new Set(['identity','mean','edge']);
  const params=new URLSearchParams(location.search);
  const bad=(params.has('v')&&params.get('v')!=='1') ||
    (params.has('kernel')&&!valid.has(params.get('kernel'))) ||
    (location.hash && location.hash!=='#kernel');
  let kernelId=bad?'identity':(params.get('kernel')||'identity');
  if(bad){const note=document.querySelector('#url-notice');note.hidden=false;note.textContent='잘못된 주소 값을 기본값으로 복원했습니다.';}
  function syncURL(){
    const suffix=`?v=1&kernel=${kernelId}#kernel`;
    history.replaceState(null,'',location.pathname+suffix);
    document.querySelector('#scroll-mode').href='scroll.html'+suffix;
    document.querySelector('#slide-mode').href='slides.html'+suffix;
  }
  syncURL();
  iframe.src='content.html?v=1&kernel='+kernelId+'#kernel';
  function resize() {
    const slide=document.body.dataset.mode==='slides';
    const note=document.querySelector('#url-notice');
    const noticeHeight=note.hidden?0:note.offsetHeight;
    const width=Math.max(200,Math.min(1440,innerWidth-(slide?40:48),slide?(innerHeight-112-noticeHeight)*16/9:Infinity));
    frame.style.width=width+'px';frame.style.height=(width*9/16)+'px';
    iframe.style.transform=`scale(${width/1440})`;
  }
  addEventListener('resize',resize);resize();
  const loaded=document.querySelector('#load-state');
  iframe.addEventListener('load',async()=>{
    const app=iframe.contentWindow?.KernelInteractive;
    if(!app){loaded.textContent='필수 콘텐츠 또는 스크립트를 읽지 못했습니다.';document.body.dataset.ready='error';return;}
    try{
      const state=await app.ready;
      if(state.status==='ready') {loaded.hidden=true;document.body.dataset.ready='true';}
      else {loaded.textContent='데이터 로드 오류 · 화면의 다시 불러오기 버튼을 사용하세요.';document.body.dataset.ready='error';}
    } catch(e){loaded.textContent='자료 로드 상태를 확인하지 못했습니다.';document.body.dataset.ready='error';}
  });
  addEventListener('message',event=>{
    if(event.source!==iframe.contentWindow || event.origin!==location.origin || event.data?.type!=='kernel-state') return;
    if(event.data.status==='ready' && valid.has(event.data.kernelId)){
      kernelId=event.data.kernelId;syncURL();loaded.hidden=true;document.body.dataset.ready='true';
    } else if(event.data.status==='error'){
      document.body.dataset.ready='error';loaded.hidden=false;loaded.textContent='계산 데이터 오류 · 실습에서 복구 가능';
    }
  });
  window.KernelViewer={getState:()=>iframe.contentWindow?.KernelInteractive?.getState(),
    selectKernel:id=>iframe.contentWindow.KernelInteractive.selectKernel(id),
    reset:()=>iframe.contentWindow.KernelInteractive.reset()};
})();
