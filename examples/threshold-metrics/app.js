/* Both entrypoints load this content, state machine and renderer. */
(() => {
  'use strict';
  const Model=window.ThresholdMetricsModel;
  const mode=document.body.dataset.mode;
  const ids=['concept','practice'];
  const $=selector=>document.querySelector(selector);
  let dataStore=null,lastBuiltin='default',rows=new Map(),isNavigating=false;
  let state={version:1,dataset:'default',thresholdUnits:50,samples:[],status:'loading',error:null,activeSlide:'concept',predictions:[],counts:null,metrics:null,fractions:null};
  let readyResolve;
  const ready=new Promise(resolve=>{readyResolve=resolve;});
  function snapshot() {return JSON.parse(JSON.stringify({...state,threshold:state.thresholdUnits/100}));}
  function normalizeURL() {
    const query=new URLSearchParams(location.search),problems=[];
    let thresholdUnits=50,dataset='default',activeSlide=location.hash.slice(1)||'concept';
    if(query.has('v') && query.get('v')!=='1') problems.push('version');
    if(query.has('dataset')) {
      if(['default','shifted'].includes(query.get('dataset'))) dataset=query.get('dataset');
      else problems.push('dataset');
    }
    if(query.has('threshold')) {
      const t=query.get('threshold');
      if(/^\d{1,3}$/.test(t) && +t<=100) thresholdUnits=+t;
      else problems.push('threshold');
    }
    if(!ids.includes(activeSlide)) {problems.push('slide');activeSlide='concept';}
    if(problems.includes('version')) {dataset='default';thresholdUnits=50;activeSlide='concept';}
    if(problems.length) {
      const notice=$('#url-notice');notice.hidden=false;notice.textContent='잘못된 주소 값을 기본값으로 복원했습니다.';
    }
    state={...state,dataset,thresholdUnits,activeSlide};lastBuiltin=dataset;
  }
  function writeURL() {
    const query=new URLSearchParams({v:'1',dataset:state.dataset==='custom'?lastBuiltin:state.dataset,threshold:String(state.thresholdUnits)});
    const suffix='?'+query.toString()+'#'+state.activeSlide;
    history.replaceState(null,'',location.pathname+suffix);
    $('#scroll-mode').href='scroll.html'+suffix;
    $('#slide-mode').href='slides.html'+suffix;
    document.querySelectorAll('[data-go]').forEach(a=>{a.href='?'+query.toString()+'#'+a.dataset.go;a.setAttribute('aria-current',a.dataset.go===state.activeSlide?'step':'false');if(a.dataset.go!==state.activeSlide)a.removeAttribute('aria-current');});
  }
  function buildTiles() {
    rows=new Map();
    const columns=state.samples.length>14?8:7;
    [1,0].forEach(truth=>{
      const list=$(truth?'#samples-positive':'#samples-negative');list.replaceChildren();list.style.setProperty('--tile-columns',columns);
      const members=state.samples.filter(s=>s.truth===truth);
      members.forEach(sample=>{
        const tile=document.createElement('div');tile.className='sample-tile';tile.dataset.sample=sample.id;tile.dataset.truth=String(sample.truth);tile.dataset.scoreUnits=String(sample.scoreUnits);tile.setAttribute('role','listitem');
        tile.innerHTML='<div class="sample-top"><span class="sample-id"></span><span class="sample-score math-number"></span></div><div class="sample-bottom"><span class="sample-prediction"></span><span class="sample-type"></span></div><div class="sample-track" aria-hidden="true"><div class="sample-fill"></div></div>';
        tile.querySelector('.sample-id').textContent=sample.id;
        tile.querySelector('.sample-score').textContent=(sample.scoreUnits/100).toFixed(2);
        tile.querySelector('.sample-fill').style.width=sample.scoreUnits+'%';
        list.appendChild(tile);rows.set(sample.id,tile);
      });
      if(!members.length) {const p=document.createElement('p');p.className='empty-group';p.textContent='해당 샘플 없음';list.appendChild(p);}
      $(truth?'#actual-positive-count':'#actual-negative-count').textContent=members.length+'개 · 점수·실제값 고정';
    });
  }
  function render() {
    if(state.status!=='ready') return;
    const result=Model.evaluate(state.samples,state.thresholdUnits);
    state={...state,...result,error:null};
    $('#data-error').hidden=true;
    $('#threshold').disabled=false;$('#dataset').disabled=false;
    $('#threshold').value=String(state.thresholdUnits);$('#threshold-value').textContent=(state.thresholdUnits/100).toFixed(2);
    $('#threshold').setAttribute('aria-valuetext',`${(state.thresholdUnits/100).toFixed(2)}, 이 점수 이상이면 불량으로 예측`);
    $('#dataset').value=state.dataset==='custom'?lastBuiltin:state.dataset;
    const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
    result.predictions.forEach(p=>{
      const tile=rows.get(p.id),badge=tile.querySelector('.sample-prediction');
      const changed=tile.dataset.prediction!==undefined && tile.dataset.prediction!==String(p.prediction);
      tile.dataset.prediction=String(p.prediction);tile.dataset.type=p.type;tile.dataset.changed=String(changed);
      tile.style.setProperty('--threshold-pct',state.thresholdUnits+'%');
      tile.setAttribute('aria-label',`${p.id}, 점수 ${(p.scoreUnits/100).toFixed(2)}, 실제 ${p.truth?'불량':'정상'}, 예측 ${p.prediction?'불량':'정상'}, ${p.type}`);
      badge.textContent=p.prediction?'불량':'정상';tile.querySelector('.sample-type').textContent=p.type;
      badge.getAnimations().forEach(a=>a.cancel());
      if(changed && !reduced) badge.animate([{outline:'2px solid #3168C8',outlineOffset:'1px'},{outline:'2px solid transparent',outlineOffset:'1px'}],{duration:450});
    });
    Object.entries(result.counts).forEach(([key,value])=>{$('#cm-'+key).textContent=String(value);});
    Object.entries(result.fractions).forEach(([key,fraction])=>{
      const metric=$('[data-metric="'+key+'"]'),text=Model.percent(fraction),calculation=metric.querySelector('.metric-calculation');
      metric.querySelector('.metric-value').textContent=text;metric.querySelector('.calculation-result').textContent=text;
      calculation.dataset.numerator=String(fraction.numerator);calculation.dataset.denominator=String(fraction.denominator);
      calculation.querySelector('.current-fraction').removeAttribute('hidden');
      calculation.querySelector('.numerator').textContent=String(fraction.numerator);calculation.querySelector('.denominator').textContent=String(fraction.denominator);
      calculation.setAttribute('aria-label',`${fraction.numerator} / ${fraction.denominator} = ${text==='—'?'정의되지 않음':text}`);
      metric.querySelector('.metric-condition').dataset.undefined=String(fraction.denominator===0);
      if(key==='f1') metric.querySelector('.harmonic-equivalent').hidden=fraction.denominator===0;
    });
    const {tp,fp,fn,tn}=result.counts;
    $('#prediction-summary').textContent=`불량 예측 ${tp+fp} · 정상 예측 ${tn+fn}`;
    $('#evaluation-status').textContent=`임계값 ${(state.thresholdUnits/100).toFixed(2)}. 불량 예측 ${tp+fp}개, 정상 예측 ${tn+fn}개. TP ${tp}, FP ${fp}, FN ${fn}, TN ${tn}. Precision ${Model.percent(result.fractions.precision)}, Recall ${Model.percent(result.fractions.recall)}, Accuracy ${Model.percent(result.fractions.accuracy)}, F1-score ${Model.percent(result.fractions.f1)}.`;
    writeURL();alignFigure();
  }
  function fail(error) {
    state={...state,status:'error',error:String(error.message||error),samples:[],predictions:[],counts:null,metrics:null,fractions:null};
    rows=new Map();
    if($('#threshold')) {
      $('#threshold').disabled=true;$('#dataset').disabled=true;$('#threshold-value').textContent='—';
      document.querySelectorAll('.sample-grid').forEach(e=>e.replaceChildren());
      document.querySelectorAll('.cm-count,.metric-value,.calculation-result').forEach(e=>{e.textContent='—';});
      document.querySelectorAll('.current-fraction').forEach(e=>{e.setAttribute('hidden','');});
      document.querySelectorAll('.metric-calculation').forEach(e=>{delete e.dataset.numerator;delete e.dataset.denominator;e.setAttribute('aria-label','데이터 오류로 계산하지 않음');});
      $('#prediction-summary').textContent='데이터 오류로 판정하지 않음';
      $('#actual-positive-count').textContent='—';$('#actual-negative-count').textContent='—';
      $('#data-error-message').textContent='데이터를 확인할 수 없어 판정과 지표를 표시하지 않습니다. '+state.error;$('#data-error').hidden=false;
      $('#evaluation-status').textContent='데이터 오류. 판정과 성능 지표를 표시하지 않음.';
    } else {
      const lesson=$('#lesson');lesson.replaceChildren();const p=document.createElement('p');p.className='loading-state';p.textContent='자료를 불러오지 못했습니다. 같은 폴더의 콘텐츠·데이터 파일을 확인한 뒤 새로고침해 주세요.';const retry=document.createElement('button');retry.type='button';retry.textContent='다시 불러오기';retry.addEventListener('click',()=>location.reload());p.appendChild(retry);lesson.appendChild(p);
    }
    return false;
  }
  function setThreshold(value) {
    try {Model.validateThreshold(value);if(state.status!=='ready')return false;state.thresholdUnits=value;render();return true;}
    catch(error) {return fail(error);}
  }
  function setDataset(name) {
    try {
      if(!dataStore || !['default','shifted'].includes(name)) throw new Error('알 수 없는 데이터셋입니다.');
      const samples=Model.validateSamples(dataStore.datasets[name].samples);
      state={...state,status:'ready',error:null,dataset:name,samples};lastBuiltin=name;buildTiles();render();return true;
    } catch(error) {return fail(error);}
  }
  function loadSamples(samples) {
    try {const clean=Model.validateSamples(samples);state={...state,status:'ready',error:null,dataset:'custom',samples:clean};buildTiles();render();return true;}
    catch(error) {return fail(error);}
  }
  function textBounds(element) {
    const walker=document.createTreeWalker(element,NodeFilter.SHOW_TEXT),rects=[];
    while(walker.nextNode()) {if(!walker.currentNode.textContent.trim())continue;const r=document.createRange();r.selectNodeContents(walker.currentNode);rects.push(r.getBoundingClientRect());}
    return {left:Math.min(...rects.map(r=>r.left)),right:Math.max(...rects.map(r=>r.right))};
  }
  function alignFigure() {
    const figure=$('.confusion-figure');
    if(figure && figure.getBoundingClientRect().width) {
      const axis=figure.querySelector('.pred-axis'),title=textBounds(axis.querySelector('.pred-axis-label'));
      const rowLeft=Math.min(...[...figure.querySelectorAll('tbody th[scope="row"]')].map(e=>textBounds(e).left));
      const rect=figure.getBoundingClientRect(),ar=axis.getBoundingClientRect(),scale=rect.width/parseFloat(getComputedStyle(figure).width);
      const lineWidth=parseFloat(getComputedStyle(figure.querySelector('.prediction-divider')).borderRightWidth);
      figure.style.setProperty('--divider-x',((title.right+rowLeft)/2-rect.left)/scale-lineWidth/2+'px');figure.style.setProperty('--divider-y',(ar.top-rect.top)/scale+'px');figure.style.setProperty('--divider-height',ar.height/scale+'px');
    }
    const flow=$('.concept-flow'),svg=$('.concept-connectors');
    if(flow && flow.getBoundingClientRect().width) {
      const box=flow.getBoundingClientRect(),scale=box.width/flow.offsetWidth;svg.setAttribute('viewBox',`0 0 ${flow.offsetWidth} ${flow.offsetHeight}`);
      svg.querySelectorAll('path').forEach(path=>{
        const from=document.getElementById(path.dataset.from).getBoundingClientRect(),to=document.getElementById(path.dataset.to).getBoundingClientRect();
        const sx=(from.right-box.left)/scale+5,sy=(from.top+from.height/2-box.top)/scale,tx=(to.left-box.left)/scale-5,ty=(to.top+to.height/2-box.top)/scale;
        const mid=(sx+tx)/2;const d=Math.abs(sy-ty)<1?`M${sx} ${sy} H${tx}`:`M${sx} ${sy} H${mid} V${ty} H${tx}`;
        path.setAttribute('d',`${d} M${tx-6} ${ty-5} L${tx} ${ty} L${tx-6} ${ty+5}`);path.dataset.startX=sx;path.dataset.startY=sy;path.dataset.endX=tx;path.dataset.endY=ty;
      });
    }
  }
  function scalePages() {
    const notice=$('#url-notice');
    const noticeHeight=notice.hidden?0:notice.getBoundingClientRect().height+20;
    document.documentElement.style.setProperty('--notice-height',noticeHeight+'px');
    let width=Math.min(1440,innerWidth-40);
    width=Math.min(width,(innerHeight-112-noticeHeight)*16/9);
    document.documentElement.style.setProperty('--page-scale',width/1440);alignFigure();
  }
  function selectSlide(id,scroll=false) {
    if(!ids.includes(id)) id='concept';
    state.activeSlide=id;
    document.querySelectorAll('.page-frame').forEach(frame=>{const active=frame.dataset.slide===id;frame.dataset.active=String(active);frame.setAttribute('aria-hidden',mode==='slides'&&!active?'true':'false');});
    $('#page-status').textContent=`${ids.indexOf(id)+1} / 2`;$('#previous').disabled=id==='concept';$('#next').disabled=id==='practice';writeURL();scalePages();
    if(mode==='scroll'&&scroll) {isNavigating=true;document.querySelector('.page-frame[data-slide="'+id+'"]').scrollIntoView({block:'start'});requestAnimationFrame(()=>{isNavigating=false;});}
    requestAnimationFrame(alignFigure);
  }
  function bind() {
    $('#threshold').addEventListener('input',event=>setThreshold(Number(event.target.value)));
    $('#dataset').addEventListener('change',event=>setDataset(event.target.value));
    $('#retry-data').addEventListener('click',async()=>{if(dataStore)setDataset('default');else location.reload();});
    $('#previous').addEventListener('click',()=>selectSlide('concept',true));$('#next').addEventListener('click',()=>selectSlide('practice',true));
    document.querySelectorAll('[data-go]').forEach(a=>a.addEventListener('click',event=>{event.preventDefault();selectSlide(a.dataset.go,true);}));
    window.addEventListener('hashchange',()=>selectSlide(location.hash.slice(1),true));
    window.addEventListener('resize',scalePages);
    window.addEventListener('keydown',event=>{
      if(event.altKey||event.ctrlKey||event.metaKey||event.shiftKey||event.target.closest('input,select,textarea,button,a,[contenteditable="true"]'))return;
      if(['ArrowRight','ArrowDown','PageDown',' ','End'].includes(event.key)) {event.preventDefault();selectSlide('practice',true);}
      if(['ArrowLeft','ArrowUp','PageUp','Home'].includes(event.key)) {event.preventDefault();selectSlide('concept',true);}
    });
    if(mode==='scroll') window.addEventListener('scroll',()=>{
      if(isNavigating)return;const frames=[...document.querySelectorAll('.page-frame')];if(!frames.length)return;
      let active='concept';if(innerHeight+scrollY>=document.documentElement.scrollHeight-2)active='practice';else frames.forEach(frame=>{if(frame.getBoundingClientRect().top<=140)active=frame.dataset.slide;});
      if(state.activeSlide!==active)selectSlide(active);
    },{passive:true});
    new ResizeObserver(alignFigure).observe($('.confusion-figure'));
  }
  async function response(url,type) {const r=await fetch(url);if(!r.ok)throw new Error(url+'을 불러오지 못했습니다.');return type==='json'?r.json():r.text();}
  async function initialize() {
    normalizeURL();
    const requestedSlide=state.activeSlide;
    isNavigating=true;
    const [content,data]=await Promise.allSettled([response('content.html','text'),response('data.json','json')]);
    try {
      if(content.status!=='fulfilled')throw content.reason;
      $('#lesson').innerHTML=content.value;bind();scalePages();selectSlide(state.activeSlide,false);
      if(data.status!=='fulfilled')throw data.reason;
      dataStore=data.value;if(dataStore.version!==1||!dataStore.datasets)throw new Error('데이터 형식 버전이 맞지 않습니다.');
      ['default','shifted'].forEach(name=>{if(!dataStore.datasets[name])throw new Error('데이터셋이 없습니다.');Model.validateSamples(dataStore.datasets[name].samples);});
      setDataset(state.dataset);
      const fontResults=await Promise.allSettled([document.fonts.load('20px "Pretendard Variable"','임계값 정상 불량 Precision'),document.fonts.load('20px "STIX Two Math"','TP0123456789≥')]);await document.fonts.ready;
      const fontsLoaded=fontResults.every(r=>r.status==='fulfilled');state.fontStatus=fontsLoaded?'loaded':'fallback';document.body.dataset.fontStatus=state.fontStatus;
      if(!fontsLoaded) {const notice=$('#url-notice');notice.hidden=false;notice.textContent='글꼴 파일을 불러오지 못해 시스템 글꼴로 표시합니다.';}
      scalePages();selectSlide(requestedSlide,mode==='scroll');
      requestAnimationFrame(()=>{isNavigating=false;});
    } catch(error) {fail(error);}
    $('#lesson').setAttribute('aria-busy','false');document.body.dataset.ready=state.status;readyResolve(snapshot());
  }
  window.ThresholdMetrics={ready,getState:snapshot,setThreshold,setDataset,loadSamples};
  initialize();
})();
