'use strict';
const slide=document.body.dataset.mode==='slide';
const frame=document.querySelector('.frame'), iframe=document.querySelector('iframe');
if(location.hash!=='#summary')history.replaceState(null,'','#summary');
function resize(){const width=slide?Math.min(1440,innerWidth-40,(innerHeight-112)*16/9):Math.min(1440,innerWidth-48);frame.style.width=width+'px';frame.style.height=width*9/16+'px';iframe.style.transform=`scale(${width/1440})`;}
resize();addEventListener('resize',resize);
iframe.addEventListener('load',async()=>{try{await iframe.contentWindow.reportReady;if(!iframe.contentDocument.querySelectorAll('.metric').length)throw Error('Missing report');frame.classList.add('ready');document.body.dataset.ready='true';}catch(e){document.querySelector('.loading').textContent='보고서를 불러오지 못했습니다. 새로고침해 주세요.';}});
iframe.addEventListener('error',()=>document.querySelector('.loading').textContent='보고서를 불러오지 못했습니다. 새로고침해 주세요.');
// An iframe HTTP error can finish before a deferred listener is attached.
setTimeout(()=>{if(!frame.classList.contains('ready'))document.querySelector('.loading').textContent='보고서를 불러오지 못했습니다. 새로고침해 주세요.';},8000);
