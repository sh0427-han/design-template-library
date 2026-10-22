/* Shared, deterministic fixed-filter illustration for 02 Process / 03 Comparison.
 * Source image: assets/concept-apple-photo.jpg (local project image).
 * Fixed, hand-defined 3x3 filters; never imply learned model inference.
 * 64x64 RGB -> luminance -> 16 oriented 3x3 gradient + ReLU maps.
 * This demonstration is independent of the #6 CNN architecture schematic.
 */
(() => {
  'use strict';
  const NS = 'http://www.w3.org/2000/svg';
  const WIDTH = 64;
  const directions = Array.from({length: 16}, (_, k) => {
    const angle = k * Math.PI / 8;
    return [Math.cos(angle), Math.sin(angle)];
  });
  const clamp = n => Math.max(0, Math.min(1, n));
  const pixelAt = (arr, n, x, y) =>
    arr[Math.max(0, Math.min(n - 1, y)) * n + Math.max(0, Math.min(n - 1, x))];

  function compute(image) {
    const tmp = document.createElement('canvas');
    tmp.width = tmp.height = WIDTH;
    const context = tmp.getContext('2d', {willReadFrequently: true});
    context.imageSmoothingEnabled = true;
    context.imageSmoothingQuality = 'high';
    context.drawImage(image, 0, 0, WIDTH, WIDTH);
    const rgba = context.getImageData(0, 0, WIDTH, WIDTH).data;
    const gray = new Float32Array(WIDTH * WIDTH);
    for (let i = 0; i < gray.length; i++) {
      gray[i] = (rgba[4*i] * 0.2126 + rgba[4*i+1] * 0.7152
          + rgba[4*i+2] * 0.0722) / 255;
    }

    const conv1 = directions.map(([co, si], channel) => {
      const out = new Float32Array(WIDTH * WIDTH);
      for (let y = 0; y < WIDTH; y++) {
        for (let x = 0; x < WIDTH; x++) {
          const q = (xx, yy) => pixelAt(gray, WIDTH, xx, yy);
          const gx = (q(x+1,y-1)+2*q(x+1,y)+q(x+1,y+1)
                    -q(x-1,y-1)-2*q(x-1,y)-q(x-1,y+1))/8;
          const gy = (q(x-1,y+1)+2*q(x,y+1)+q(x+1,y+1)
                    -q(x-1,y-1)-2*q(x,y-1)-q(x+1,y-1))/8;
          // A 3x3 oriented gradient kernel followed by ReLU.
          out[y*WIDTH+x] = Math.max(0, (gx*co + gy*si + (channel%4)*0.007)*3.2);
        }
      }
      return out;
    });

    return {gray, conv1};
  }

  function heatmap(data, n, palette) {
    const cv = document.createElement('canvas');
    cv.width = cv.height = n;
    const ctx = cv.getContext('2d');
    const pixels = ctx.createImageData(n, n);
    const dark = palette==='teal' ? [31,151,143] : [30,74,142];
    const light = [242,247,253];
    for (let i = 0; i < data.length; i++) {
      const v = Math.pow(clamp(data[i] * 4.5), 0.74);
      for (let c = 0; c < 3; c++) {
        pixels.data[4*i+c] = Math.round(light[c] + (dark[c]-light[c])*v);
      }
      pixels.data[4*i+3] = 255;
    }
    ctx.putImageData(pixels,0,0);
    return cv.toDataURL('image/png');
  }
  function element(tag, attrs={}) {
    const node = document.createElementNS(NS, tag);
    Object.entries(attrs).forEach(([k,v]) => node.setAttribute(k,String(v)));
    return node;
  }
  function layerStack(svg, maps, n, channels, palette, patch) {
    svg.replaceChildren();
    svg.setAttribute('viewBox','0 0 132 115');
    const shown = Math.min(channels.length,5);
    const unit = n===64?76:64;
    for(let k=shown-1;k>=0;k--) {
      const depth=k, x=16+depth*6.1, y=26-depth*5.1;
      const image=element('image',{
        x,y,width:unit,height:unit,
        href:heatmap(maps[channels[k]],n,palette),
        preserveAspectRatio:'none'
      });
      image.style.imageRendering='auto';
      svg.append(
        element('rect',{x:x-2,y:y-2,width:unit+4,height:unit+4,
          rx:3,fill:'#fff',stroke:'#7193be','stroke-width':1.4}),
        image
      );
      if(k===0 && patch) {
        // The same 2x2 area is highlighted on Conv1 and its 1x1 output
        // location in MaxPool. Pooling calculation itself is exact.
        const pitch=unit/n, sx=n===64?32:16, sy=n===64?33:16;
        svg.append(element('rect',{
          x:x+sx*pitch, y:y+sy*pitch,
          width:(n===64?2:1)*pitch+1.4,height:(n===64?2:1)*pitch+1.4,
          fill:'none',stroke:'#e49a4d','stroke-width':2
        }));
      }
    }
    svg.dataset.computed = 'true';
    svg.dataset.channelCount=String(maps.length);
    svg.dataset.imageDerived='true';
  }
  function renderSmallMotifs(result) {
    for(const selector of ['.process-feature-svg','.compare-feature-svg']){
      document.querySelectorAll(selector).forEach(svg => {
        layerStack(svg,result.conv1,64,[0,3,6,9],'blue',false);
        const slide=svg.closest('.slide');
        if(slide)slide.dataset.computedMaps='true';
      });
    }
  }
  function begin() {
    if(!document.querySelector('.process-feature-svg,.compare-feature-svg'))return;
    window.CNNFeatureMaps={status:'loading',width:WIDTH,source:'assets/concept-apple-photo.jpg'};
    const img = new Image();
    img.onload=()=> {
      try {
        const maps=compute(img);
        renderSmallMotifs(maps);
        Object.assign(window.CNNFeatureMaps,{status:'ready',result:maps});
      } catch(err) {window.CNNFeatureMaps.status='error';console.error('Feature map rendering failed',err);}
    };
    img.onerror=()=>console.error('CNN source photograph could not load');
    img.src='assets/concept-apple-photo.jpg';
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',begin);
  else begin();
})();
