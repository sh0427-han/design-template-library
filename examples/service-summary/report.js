'use strict';
const observations = [
 {name:'응답시간',qualifier:'95백분위수',before:800,after:520,unit:'ms',detail:'280ms 단축'},
 {name:'하루 운영 비용',before:120,after:102,unit:'달러',detail:'하루 18달러 절감'},
 {name:'실패율',before:50/10000*100,after:80/10000*100,unit:'%',detail:'10,000건당 실패 30건 증가',failure:true}
];
function comparison(before,after){
 if(!Number.isFinite(before)||!Number.isFinite(after)||before<0||after<0) throw new RangeError('Nonnegative finite values required');
 return {index:before===0?null:after/before*100,change:before===0?null:(after-before)/before*100,difference:after-before};
}
window.comparison=comparison;
window.reportMetrics=observations.map(m=>({...m,...comparison(m.before,m.after)}));
document.getElementById('metrics').innerHTML=window.reportMetrics.map(m=>{
 const worse=m.change>0;
 const maximum=Math.max(m.before,m.after);
 const signed=(m.change>0?'+':'−')+Math.abs(m.change).toFixed(1)+'%';
 const value=n=>m.failure?n.toFixed(1):String(n);
 return `<section class="metric ${worse?'worse':'better'}" data-name="${m.name}"><p class="metric-qualifier"${m.qualifier?'':' aria-hidden="true"'}>${m.qualifier||''}</p><div class="bars">${[['기존',m.before,'before'],['변경',m.after,'after']].map(([label,v,cls])=>`<div class="bar-column"><div class="bar-space"><b class="value">${m.failure?`${value(v)}%`:`${value(v)}<span class="unit">${m.unit}</span>`}</b><div class="fill ${cls}" style="--ratio:${maximum===0?0:v/maximum}" aria-hidden="true"></div></div><span class="series">${label}</span></div>`).join('')}</div><div class="metric-heading"><h3>${m.name}</h3></div><div class="delta"><span class="status">${worse?'악화':'개선'}</span>${signed}</div><p class="metric-detail">${m.detail}</p></section>`;
}).join('');
window.reportReady=Promise.all([document.fonts.load('20px "Pretendard Variable"')]).then(()=>document.fonts.ready).then(()=>true);
