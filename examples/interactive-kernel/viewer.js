(() => {
  'use strict';
  const frame=document.querySelector('.frame');
  const iframe=frame.querySelector('iframe');
  const stage=document.querySelector('.stage');
  const loaded=document.querySelector('#load-state');
  const feedback=document.querySelector('#load-feedback');
  const retry=document.querySelector('#retry-content');
  const notice=document.querySelector('#url-notice');
  const valid=new Set(['identity','mean','edge']);
  const params=new URLSearchParams(location.search);
  const bad=(params.has('v')&&params.get('v')!=='1') ||
    (params.has('kernel')&&!valid.has(params.get('kernel'))) ||
    (location.hash && location.hash!=='#kernel');
  let kernelId=bad?'identity':(params.get('kernel')||'identity');
  let viewerError=null;
  let loadDeadline;
  let settlement=0;
  document.body.dataset.ready='loading';
  frame.dataset.viewerState='loading';
  if(bad){notice.hidden=false;notice.textContent='잘못된 주소 값을 기본값으로 복원했습니다.';}

  function syncURL(){
    const suffix=`?v=1&kernel=${kernelId}#kernel`;
    history.replaceState(null,'',location.pathname+suffix);
    document.querySelector('#scroll-mode').href='scroll.html'+suffix;
    document.querySelector('#slide-mode').href='slides.html'+suffix;
  }
  function app(){
    try{return iframe.contentWindow?.KernelInteractive||null;}
    catch(_error){return null;}
  }
  function hasLesson(){
    try{return Boolean(iframe.contentDocument?.querySelector('.kernel-slide'));}
    catch(_error){return false;}
  }
  function resize(){
    const slide=document.body.dataset.mode==='slides';
    const bar=document.querySelector('.mode-bar').getBoundingClientRect().height;
    const foot=document.querySelector('.viewer-note').getBoundingClientRect().height;
    const noticeHeight=notice.hidden?0:notice.getBoundingClientRect().height;
    const feedbackHeight=feedback.hidden?0:feedback.getBoundingClientRect().height;
    const stageHeight=Math.max(0,innerHeight-bar-foot-noticeHeight-feedbackHeight);
    stage.style.height=stageHeight+'px';
    const gutter=slide?24:48;
    const width=Math.max(0,Math.min(1440,innerWidth-(slide?40:48),(stageHeight-gutter)*16/9));
    frame.style.width=width+'px';frame.style.height=(width*9/16)+'px';
    iframe.style.transform=`scale(${width/1440})`;
  }
  function fail(message){
    clearTimeout(loadDeadline);
    viewerError=message;
    document.body.dataset.ready='error';
    loaded.hidden=false;loaded.textContent=message;
    feedback.hidden=false;retry.hidden=false;
    frame.dataset.viewerState=hasLesson()?'error':'unavailable';
    resize();
  }
  async function settle(){
    // The placeholder has no lesson; only the single versioned navigation is actionable.
    try{if(iframe.contentWindow.location.href==='about:blank')return;}catch(_error){}
    const current=++settlement;
    const lesson=app();
    if(!lesson){fail('필수 콘텐츠 또는 스크립트를 불러오지 못했습니다. 다시 불러오세요.');return;}
    try{
      await lesson.ready;
      // Match the shared viewer contract: reveal the actual source after font readiness.
      await iframe.contentDocument.fonts.ready;
      if(current!==settlement||lesson!==app())return;
      const state=lesson.getState();
      if(state.status!=='ready'){
        fail('계산 데이터를 불러오지 못했습니다. 실습의 복구 버튼 또는 다시 불러오기를 사용하세요.');return;
      }
      clearTimeout(loadDeadline);
      viewerError=null;kernelId=state.kernelId;syncURL();
      loaded.hidden=true;retry.hidden=true;feedback.hidden=true;
      document.body.dataset.ready='true';frame.dataset.viewerState='ready';
      resize();
    }catch(_error){fail('자료 로드 상태를 확인하지 못했습니다. 다시 불러오세요.');}
  }
  retry.addEventListener('click',()=>location.reload());
  iframe.addEventListener('load',settle);
  iframe.addEventListener('error',()=>fail('필수 콘텐츠를 불러오지 못했습니다. 다시 불러오세요.'));
  addEventListener('message',event=>{
    if(event.source!==iframe.contentWindow||event.origin!==location.origin||event.data?.type!=='kernel-state')return;
    if(event.data.status==='ready'&&valid.has(event.data.kernelId))settle();
    else if(event.data.status==='error')fail('계산 데이터 오류 · 실습의 복구 버튼 또는 다시 불러오기를 사용하세요.');
  });
  window.KernelViewer={
    getState:()=>{
      if(viewerError)return {status:'error',kernelId,input:null,kernelNumerators:null,divisor:null,outputNumerators:null,output:null,focus:null,error:viewerError};
      if(document.body.dataset.ready!=='true')return {status:'loading',kernelId};
      return app()?.getState()||{status:'loading',kernelId};
    },
    selectKernel:id=>{const lesson=app();if(!lesson||viewerError)throw new Error('현재 자료가 준비되지 않았습니다.');return lesson.selectKernel(id);},
    reset:()=>{const lesson=app();if(!lesson)throw new Error('현재 자료가 준비되지 않았습니다.');return lesson.reset();}
  };
  addEventListener('resize',resize);
  const observer=new ResizeObserver(resize);
  [notice,feedback,document.querySelector('.mode-bar'),document.querySelector('.viewer-note')].forEach(element=>observer.observe(element));
  document.fonts.ready.then(resize);
  syncURL();resize();
  loadDeadline=setTimeout(()=>fail('자료 응답을 기다리는 시간이 초과됐습니다. 다시 불러오세요.'),8000);
  iframe.src='content.html?v=1&kernel='+kernelId+'#kernel';
})();
