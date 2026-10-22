/* #3 layout only. Rule definition, supervised learning and both results are
 * schematic examples, never executed rule engines or learned CNN inference.
 * Preserve the shared #2 fixed-filter engine and its computed image data. */
(() => {
  'use strict';
  const slide = document.querySelector('.comparison-slide');
  if (!slide) return;
  const state = window.ComparisonReference = {
    status:'loading', supervisedExample:true, illustrationSamples:3,
    ruleEngineExecuted:false, modelInferenceExecuted:false,
    mapSource:'fixed_directional_filters', channels:[0,3,6,9],
  };
  const svg = slide.querySelector('.compare-feature-svg');
  function centerSVG(target) {
    const g = target.querySelector('[data-map-artwork]');
    if (!g) return;
    const b = g.getBBox(), v = target.viewBox.baseVal;
    g.setAttribute('transform',`translate(${v.width/2-b.x-b.width/2} ${v.height/2-b.y-b.height/2})`);
  }
  function centerRow(row) {
    row.style.transform = '';
    const parent = row.getBoundingClientRect();
    const bounds = [...row.querySelectorAll('[data-visual-bound]')].filter(e=>e.getBoundingClientRect().width).map(e=>e.getBoundingClientRect());
    if (!bounds.length) return;
    const left = Math.min(...bounds.map(b=>b.left)), right = Math.max(...bounds.map(b=>b.right));
    const scale = parent.width / row.offsetWidth;
    row.style.transform = `translateX(${(parent.left+parent.width/2-(left+right)/2)/scale}px)`;
  }
  function linkPreparedSystem(diagram) {
    const prepared = diagram.querySelector('[data-prepared-system]');
    const applied = diagram.querySelector('[data-inference-system]');
    if (!applied) return;
    const b = diagram.getBoundingClientRect(), scale = b.width/diagram.offsetWidth;
    const a = prepared.getBoundingClientRect(), z = applied.getBoundingClientRect();
    const first = diagram.querySelector('.phase-prepare').getBoundingClientRect();
    const second = diagram.querySelector('.phase-predict').getBoundingClientRect();
    const x1 = (a.left+a.width/2-b.left)/scale, y1 = (a.bottom-b.top)/scale+3;
    const x2 = (z.left+z.width/2-b.left)/scale, y2 = (z.top-b.top)/scale-4;
    const bus = ((first.bottom+second.top)/2-b.top)/scale;
    const arrow = diagram.querySelector('.system-transfer');
    arrow.setAttribute('viewBox',`0 0 ${diagram.offsetWidth} ${diagram.offsetHeight}`);
    arrow.querySelector('path').setAttribute('d',`M${x1} ${y1} V${bus} H${x2} V${y2} M${x2-4} ${y2-5} L${x2} ${y2} L${x2+4} ${y2-5}`);
    arrow.dataset.connected = 'true';
  }
  function layout() {
    centerSVG(svg);
    slide.querySelectorAll('[data-center-row]').forEach(centerRow);
    slide.querySelectorAll('.comparison-diagram').forEach(linkPreparedSystem);
  }
  function showMaps() {
    const images = [...svg.querySelectorAll('image')], frames = [...svg.querySelectorAll('rect')];
    if (images.length!==4 || frames.length!==4) throw new Error('Expected four computed channels');
    const group = document.createElementNS('http://www.w3.org/2000/svg','g');
    group.setAttribute('data-map-artwork','');group.setAttribute('data-visual-bound','');group.setAttribute('data-inference-system','');
    images.forEach((image,i)=>{
      const depth = 3-i, x = 10+11*depth, y = 30-8*depth;
      const attrs = {x:x-2,y:y-2,width:92,height:92,rx:1.5,fill:'#b7cdea',stroke:depth===0?'#4679b8':'#6e94c6','stroke-width':depth===0?1.5:1.05};
      Object.entries(attrs).forEach(([k,v])=>frames[i].setAttribute(k,String(v)));
      Object.entries({x,y,width:88,height:88,'data-channel':state.channels[depth]}).forEach(([k,v])=>image.setAttribute(k,String(v)));
      group.append(frames[i],image);
    });
    svg.replaceChildren(group);svg.setAttribute('viewBox','0 0 136 124');
    state.status = 'ready';layout();
  }
  function failed(reason) {
    state.status = 'error';state.reason = reason;
    // Keep the editable CNN symbol when loading/calculation is unavailable.
    slide.querySelector('.map-fallback').hidden = false;
    layout();
  }
  const started = performance.now();
  function awaitMaps() {
    const engine = window.CNNFeatureMaps;
    if (!engine) {failed('engine_unavailable');return;}
    if (engine.status==='error') {failed('calculation_failed');return;}
    if (engine.status==='ready') {
      try {showMaps();} catch(error) {failed('presentation_failed');console.error(error);}
      return;
    }
    if (performance.now()-started>8000) {failed('loading_timeout');return;}
    setTimeout(awaitMaps,100);
  }
  layout();document.fonts.ready.then(layout);window.addEventListener('resize',layout);
  awaitMaps();
})();
