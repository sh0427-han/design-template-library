'use strict';
const observations = [
 {name:'응답시간 95백분위수',before:800,after:520,unit:'ms',detail:'280ms 단축'},
 {name:'하루 운영 비용',before:120,after:102,unit:'달러',detail:'하루 18달러 절감'},
 {name:'실패율',before:50/10000*100,after:80/10000*100,unit:'%',detail:'실패 50 → 80건 / 10,000건',failure:true}
];
function comparison(before,after){
 if(!Number.isFinite(before)||!Number.isFinite(after)||before<0||after<0) throw new RangeError('Nonnegative finite values required');
 return {index:before===0?null:after/before*100,change:before===0?null:(after-before)/before*100,difference:after-before};
}
window.comparison=comparison;
window.reportMetrics=observations.map(m=>({...m,...comparison(m.before,m.after)}));
document.getElementById('metrics').innerHTML=window.reportMetrics.map((m,i)=>{
 const worse=m.change>0;
 const signed=(m.change>0?'+':'−')+Math.abs(m.change).toFixed(1)+'%';
 const value=n=>m.failure?n.toFixed(1):String(n);
 return `<section class="metric ${worse?'worse':'better'}" data-name="${m.name}"><div class="bars"><svg class="trend-arrow" viewBox="0 0 62 154" role="img" aria-label="${worse?'증가':'감소'}"><defs><marker id="trend-${i}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0 L10 5 L0 10 Z" fill="currentColor"/></marker></defs><path class="trend-line" d="M5 97 L57 ${157-m.index*.6}" marker-end="url(#trend-${i})"/></svg>${[['기존',m.before,100,'before'],['변경',m.after,m.index,'after']].map(([label,v,index,cls])=>`<div class="bar-column"><div class="bar-space"><b class="value">${m.failure?`${value(v)}%`:`${value(v)}<span class="unit">${m.unit}</span>`}</b><div class="fill ${cls}" style="--index:${index}" aria-hidden="true"></div></div><span class="series">${label}</span></div>`).join('')}</div><h3>${m.name}</h3><div class="delta"><span class="status">${worse?'악화':'개선'}</span>${m.failure?'+0.3<span class="status"> 퍼센트포인트</span>':`${signed}`}</div><p class="metric-detail">${m.failure?'상대 변화 '+signed+'<br>': ''}${m.detail}</p></section>`;
}).join('');
window.reportReady=Promise.all([document.fonts.load('20px "Pretendard Variable"')]).then(()=>document.fonts.ready).then(()=>true);
