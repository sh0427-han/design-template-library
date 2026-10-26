/* Illustrative scalar loss, not a recorded training run. All geometry derives from this model. */
(() => {
  const svg = document.getElementById('loss-plot');
  const art = document.getElementById('plot-art');
  const slide = document.querySelector('.gd-slide');
  const model = {start:2.8, rate:0.28, states:6, samples:161,
    domain:[-3.4,3.4], range:[0,6.5], plot:{left:48,right:290,top:20,bottom:454}};
  const loss = theta => theta * theta / 2;
  const gradient = theta => theta;
  const x = theta => model.plot.left + (theta-model.domain[0])/(model.domain[1]-model.domain[0])*(model.plot.right-model.plot.left);
  const y = value => model.plot.bottom - (value-model.range[0])/(model.range[1]-model.range[0])*(model.plot.bottom-model.plot.top);
  const add = (tag, attrs, text) => {
    const e=document.createElementNS('http://www.w3.org/2000/svg',tag);
    for(const [name,value] of Object.entries(attrs)) e.setAttribute(name,String(value));
    if(text !== undefined) e.textContent=text;
    art.append(e);return e;
  };
  const path = (id,d,color,width=2,extra={}) => add('path',{id,d,fill:'none',stroke:color,'stroke-width':width,'stroke-linecap':'round','stroke-linejoin':'round',...extra});
  // Connected arrow body and head share the same tip, without marker bounding-box ambiguity.
  const arrow = (id,x1,y1,x2,y2,color,width=2.3) => {
    const dx=x2-x1,dy=y2-y1,len=Math.hypot(dx,dy),ux=dx/len,uy=dy/len,s=7;
    return path(id,`M${x1} ${y1} L${x2} ${y2} M${x2-ux*s-uy*4} ${y2-uy*s+ux*4} L${x2} ${y2} L${x2-ux*s+uy*4} ${y2-uy*s-ux*4}`,color,width);
  };
  const label=(id,px,py,text,cls='',anchor='start') => add('text',{id,x:px,y:py,class:cls,'text-anchor':anchor},text);
  async function render() {
    await Promise.all([document.fonts.load('400 22px "STIX Two Math"','θηL′𝑡'),document.fonts.load('800 23px "Pretendard Variable"','기울기 ABC')]);
    await document.fonts.ready;
    const points=Array.from({length:model.samples},(_,i)=>{const theta=model.domain[0]+i/(model.samples-1)*(model.domain[1]-model.domain[0]);return {theta,loss:loss(theta),x:x(theta),y:y(loss(theta))};});
    const states=[];let theta=model.start;
    for(let i=0;i<model.states;i++){states.push({theta,loss:loss(theta),gradient:gradient(theta),x:x(theta),y:y(loss(theta))});theta-=model.rate*gradient(theta);}
    arrow('y-axis',48,454,48,29,'#b7c4d5',1.5);
    arrow('x-axis',48,454,305,454,'#b7c4d5',1.5);
    label('loss-axis',48,18,'손실','plot-strong');
    label('loss-axis-math',92,18,'𝐿(𝜃)','math-number plot-strong');
    label('parameter-axis',48,478,'매개변수 θ','plot-strong','start');
    // Keep mathematical θ in the math font, ordinary Korean in Pretendard.
    document.getElementById('parameter-axis').textContent='매개변수';
    label('parameter-symbol',127,478,'𝜃','math-number plot-strong','start');
    path('loss-curve',points.map((p,i)=>`${i?'L':'M'}${p.x} ${p.y}`).join(' '),'#1b3558',3);
    const current=states[0],next=states[1];
    const tangent= [-0.55,0.40].map(delta=>({x:x(current.theta+delta),y:y(current.loss+current.gradient*delta)}));
    path('tangent',`M${tangent[0].x} ${tangent[0].y} L${tangent[1].x} ${tangent[1].y}`,'#e49a4d',2,{'stroke-dasharray':'6 4'});
    label('tangent-label',current.x-22,current.y-43,'양의 기울기','plot-amber','end');
    path('current-guide',`M${current.x} ${current.y+12} V448`,'#9bb5da',1.3,{'stroke-dasharray':'4 5'});
    path('next-guide',`M${next.x} ${next.y+12} V448`,'#9ccfca',1.3,{'stroke-dasharray':'4 5'});
    arrow('update-arrow',current.x-3.5,394,next.x+3.5,394,'#3168c8',2.5);
    label('update-label',335,421,'기울기의 반대 방향','plot-blue','end');
    label('current-label',current.x+16,current.y+6,'현재','plot-blue');
    label('next-label',next.x+15,next.y+5,'다음','plot-teal');
    for(const [i,p] of states.entries()) {
      add('circle',{id:`state-${i}`,cx:p.x,cy:p.y,r:i<2?7:4.5,fill:i===0?'#3168c8':'#26a6a1',stroke:'#fff','stroke-width':2,'data-theta':p.theta,'data-loss':p.loss});
    }
    label('repeat-label',states[4].x-30,states[4].y-35,'반복','plot-teal','end');
    path('repeat-leader',`M${states[4].x-23} ${states[4].y-29} L${states[4].x-7} ${states[4].y-9}`,'#9ccfca',1.3);
    for(const [id,state,index,cls] of [['current-symbol',current,'𝑡','plot-blue'],['next-symbol',next,'𝑡+1','plot-teal']]) {
      const text=label(id,state.x,470,'𝜃',`math-number ${cls}`,'middle');
      const sub=document.createElementNS('http://www.w3.org/2000/svg','tspan');
      sub.setAttribute('dy','5');sub.setAttribute('font-size','12');sub.textContent=index;text.append(sub);
    }
    window.gradientDescentEvidence={model,points,states,tangent};
    slide.dataset.ready='true';
  }
  render().catch(()=>{slide.dataset.ready='error';document.querySelector('.gd-failure').textContent='손실 곡선을 불러오지 못했습니다. 새로고침해 주세요.';});
})();
