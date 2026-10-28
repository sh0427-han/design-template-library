/* Browser state and rendering. The arithmetic is only in KernelModel. */
(() => {
  'use strict';
  const Model = window.KernelModel;
  const $ = selector => document.querySelector(selector);
  let dataset = null;
  let readyResolve;
  let state = {
    status:'loading', kernelId:'identity', input:null, kernelNumerators:null,
    divisor:null, outputNumerators:null, output:null, focus:null, error:null
  };
  const ready = new Promise(resolve => { readyResolve = resolve; });
  const deepClone = value => JSON.parse(JSON.stringify(value));
  const ids = ['identity','mean','edge'];

  function parseURL() {
    const params = new URLSearchParams(location.search);
    const bad = (params.has('v') && params.get('v') !== '1') ||
      (params.has('kernel') && !ids.includes(params.get('kernel'))) ||
      (location.hash && location.hash !== '#kernel');
    state.kernelId = bad ? 'identity' : (params.get('kernel') || 'identity');
    if (bad) $('#url-notice')?.removeAttribute('hidden');
    if (bad) {
      const note = document.createElement('p');note.className='url-alert';
      note.id='url-notice';note.textContent='올바르지 않은 주소를 기본 필터로 복원했습니다.';
      $('#panel-title').after(note);
    }
  }

  function updateURL() {
    const suffix = `?v=1&kernel=${state.kernelId}#kernel`;
    history.replaceState(null, '', location.pathname + suffix);
    if (window.parent !== window) {
      window.parent.postMessage({type:'kernel-state', kernelId:state.kernelId, status:state.status}, location.origin);
    }
  }

  function createCells(host, length) {
    host.replaceChildren();
    for (let i=0;i<length;i++) {
      const cell=document.createElement('span');cell.className='cell';
      cell.dataset.index=String(i);host.appendChild(cell);
    }
  }

  function initCells() {
    createCells($('#input-matrix'),49);
    createCells($('#kernel-matrix'),9);
    createCells($('#output-matrix'),25);
    state.input.forEach((row,r) => row.forEach((n,c) => {
      const cell=$('#input-matrix').children[r*7+c];
      const channel=Math.round(n/9*255);
      cell.textContent=String(n);cell.style.backgroundColor=`rgb(${channel}, ${channel}, ${channel})`;
      cell.style.color=channel>150?'#12233f':'#fff';
      if (r>=2&&r<=4&&c>=1&&c<=3) cell.classList.add('focus');
    }));
  }

  function render() {
    if (!dataset || !Model || state.status !== 'ready') return;
    const result = Model.evaluate(dataset, state.kernelId);
    state = {...state, ...result, status:'ready', error:null};
    $('#data-error').hidden=true;
    $('#kernel-select').disabled=false;$('#reset-kernel').disabled=false;
    $('#kernel-select').value=state.kernelId;
    const entries=state.kernelNumerators.flat();
    entries.forEach((n,i)=>{
      const cell=$('#kernel-matrix').children[i];
      cell.textContent=state.divisor===1?String(n):`${n}/${state.divisor}`;
      cell.classList.toggle('fraction',state.divisor!==1);
      cell.setAttribute('aria-label',state.divisor===1?String(n):`${n} 나누기 ${state.divisor}`);
    });
    state.output.forEach((row,r)=>row.forEach((value,c)=>{
      const cell=$('#output-matrix').children[r*5+c];
      cell.textContent=Model.formatValue(value);
      cell.style.backgroundColor=Model.colorFor(value);
      const rgb=Model.colorFor(value).match(/\d+/g).map(Number);
      const brightness=(.2126*rgb[0]+.7152*rgb[1]+.0722*rgb[2])/255;
      cell.style.color=brightness<.55?'#fff':'#12233f';
      cell.classList.toggle('focus',r===2 && c===1);
      cell.setAttribute('aria-label',`출력 ${r+1}행 ${c+1}열, ${value<0?'음수 ':value>0?'양수 ':'0, '}${Model.formatValue(value)}`);
      cell.dataset.raw=String(value);cell.dataset.numerator=String(state.outputNumerators[r][c]);
      cell.dataset.denominator=String(state.divisor);
    }));
    const f=state.focus;
    const sumText=f.products.flat().map(n=>n<0?`(${n})`:String(n)).join(' + ');
    $('#focus-equation').textContent=f.denominator===1?sumText:`(${sumText}) / ${f.denominator}`;
    $('#focus-result').textContent=f.denominator===1?`= ${f.display}`:
      `= ${f.numerator}/${f.denominator} ≈ ${f.display}`;
    $('#kernel-summary').textContent=state.kernelId==='mean'?'각 셀 가중치 1/9':
      state.kernelId==='edge'?'좌우 변화에 반응':'중앙 값 유지 · 다른 셀 가중치 0';
    $('#role-name').textContent=state.kernelName;
    $('#role-description').textContent=state.kernelDescription;
    $('#kernel-matrix').setAttribute('aria-label',`${state.kernelName}: ${entries.map(n=>n+'/'+state.divisor).join(', ')}`);
    $('#output-matrix').setAttribute('aria-label',`${state.kernelName}의 5행 5열 결과`);
    $('#kernel-status').textContent=`${state.kernelName}. 선택된 출력 3행 2열은 ${f.numerator} 나누기 ${f.denominator}, 값 ${f.display}.`;
    document.body.dataset.ready='true';
    updateURL();
  }

  function errorState(error) {
    state={...state,status:'error',input:null,kernelNumerators:null,divisor:null,
      outputNumerators:null,output:null,focus:null,error:String(error?.message||error)};
    dataset=null;
    $('#kernel-select').disabled=true;$('#reset-kernel').disabled=true;
    for(const id of ['input-matrix','kernel-matrix','output-matrix']) $('#'+id).replaceChildren();
    $('#focus-equation').textContent='—';$('#focus-result').textContent='—';
    $('#kernel-summary').textContent='계산 없음';$('#role-name').textContent='데이터 오류';
    $('#role-description').textContent='현재 결과를 표시하지 않습니다.';
    $('#data-error-message').textContent='입력·필터 데이터가 유효하지 않습니다. '+state.error;
    $('#data-error').hidden=false;$('#kernel-status').textContent='데이터 오류. 계산을 표시하지 않음.';
    document.body.dataset.ready='error';
    if(window.parent!==window)window.parent.postMessage({type:'kernel-state',status:'error'},location.origin);
  }

  async function load() {
    state={...state,status:'loading',error:null};
    $('#kernel-select').disabled=true;$('#reset-kernel').disabled=true;
    try {
      if(!Model) throw new Error('수학 계산 스크립트를 사용할 수 없습니다.');
      const response=await fetch('data.json',{cache:'no-store'});
      if(!response.ok) throw new Error(`데이터 응답 ${response.status}`);
      dataset=Model.validateData(await response.json());
      state={...state,status:'ready',input:dataset.input,error:null};
      initCells();render();
    } catch(error) { errorState(error); }
    readyResolve(getState());
  }

  function getState() { return deepClone(state); }
  function selectKernel(id) {
    if (!ids.includes(id)) throw new RangeError(`알 수 없는 필터 ID: ${String(id)}`);
    if (state.status !== 'ready') throw new Error('현재 데이터가 준비되지 않았습니다.');
    const previous=state.kernelId;
    try {state.kernelId=id;render();} catch(e) {state.kernelId=previous;errorState(e);throw e;}
    return getState();
  }
  function reset() {
    state.kernelId='identity';
    if(state.status!=='ready') return load();
    render();return getState();
  }
  window.KernelInteractive={ready,getState,selectKernel,reset};
  $('#kernel-select').addEventListener('change',event=>selectKernel(event.target.value));
  $('#reset-kernel').addEventListener('click',reset);
  $('#retry-data').addEventListener('click',()=>{
    if (!Model) { location.reload();return; }
    state.kernelId='identity';load();
  });
  parseURL();load();
})();
