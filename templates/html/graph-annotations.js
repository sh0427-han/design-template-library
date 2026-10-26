/* Opt-in shared axis-title alignment. Existing references are not restyled. */
(() => {
  'use strict';
  function packInline(parts, gap=8) {
    let cursor=0;
    for(const part of parts) {
      const b=part.getBBox();
      part.setAttribute('x',Number(part.getAttribute('x')||0)+cursor-b.x);
      cursor+=b.width+gap;
    }
  }
  function alignAxes({svg,yLabel,xLabel,left,right,top,bottom,gap}) {
    const spacing=gap??parseFloat(getComputedStyle(svg).getPropertyValue('--gap-related'));
    if(![left,right,top,bottom,spacing].every(Number.isFinite)||right<=left||bottom<=top) throw new Error('Invalid axis geometry');
    for(const label of [yLabel,xLabel]) label.removeAttribute('transform');
    const y=yLabel.getBBox(),x=xLabel.getBBox();
    yLabel.setAttribute('transform',`translate(${left-spacing-y.y-y.height} ${(top+bottom)/2+y.x+y.width/2}) rotate(-90)`);
    xLabel.setAttribute('transform',`translate(${(left+right)/2-x.x-x.width/2} ${bottom+spacing-x.y})`);
    svg.dataset.axisAligned='true';
  }
  function bounds(svg,node) {
    const r=node.getBoundingClientRect(),s=svg.getBoundingClientRect(),v=svg.viewBox.baseVal;
    return {x:(r.x-s.x)*v.width/s.width,y:(r.y-s.y)*v.height/s.height,width:r.width*v.width/s.width,height:r.height*v.height/s.height};
  }
  window.GraphAnnotations=Object.freeze({packInline,alignAxes,bounds});
})();
