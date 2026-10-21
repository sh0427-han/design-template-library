/* Shared, deterministic CNN illustration for 02 Process and 06 Architecture.
 * Source image: assets/concept-apple-photo.jpg (local project image).
 * Fixed, hand-defined 3x3 filters; never imply learned model inference.
 * 64x64 RGB -> 16 conv+ReLU maps -> 2x2 max pool -> 32 conv+ReLU
 * maps -> channel means. Illustrated channel planes remain editable SVG.
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
  const mean = data => data.reduce((sum, v) => sum + v, 0) / data.length;
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

    const pool = conv1.map(input => {
      const out = new Float32Array(32*32);
      for(let y=0;y<32;y++) for(let x=0;x<32;x++) {
        out[y*32+x] = Math.max(
          input[(2*y)*64+2*x], input[(2*y)*64+2*x+1],
          input[(2*y+1)*64+2*x], input[(2*y+1)*64+2*x+1]
        );
      }
      return out;
    });
    // Sparse, fixed 3x3 cross-channel kernels with zero weights on other
    // input channels. This is a valid illustrative 16->32 convolution.
    const kernels = [
      [0,-0.55,0,-0.55,2.2,-0.55,0,-0.55,0],
      [-0.42,0,0,0,1.2,0,0,0,-0.42],
      [0,-0.42,0,0,1.25,0,0,-0.42,0],
      [0.08,0.08,0.08,0.08,0.36,0.08,0.08,0.08,0.08]
    ];
    const conv2 = Array.from({length:32}, (_,channel) => {
      const out = new Float32Array(32*32);
      const kernel = kernels[channel%4];
      const c0 = channel%16, c1 = (channel+5)%16;
      for(let y=0;y<32;y++) for(let x=0;x<32;x++){
        let z = 0.015;
        for(let ky=-1;ky<=1;ky++) for(let kx=-1;kx<=1;kx++){
          const weight = kernel[(ky+1)*3+kx+1];
          // Zero padding preserves 32x32 spatial shape.
          if(y+ky<0 || y+ky>=32 || x+kx<0 || x+kx>=32)continue;
          const p=(y+ky)*32+(x+kx);
          z += weight*(0.75*pool[c0][p]+0.25*pool[c1][p]);
        }
        out[y*32+x] = Math.max(0, z);
      }
      return out;
    });
    return {gray, conv1, pool, conv2, gap: conv2.map(mean)};
  }

  function heatmap(data, n, palette) {
    const cv = document.createElement('canvas');
    cv.width = cv.height = n;
    const ctx = cv.getContext('2d');
    const pixels = ctx.createImageData(n, n);
    const dark = palette==='teal' ? [31,151,143] : [30,74,142];
    const light = [242,247,253];
    for (let i = 0; i < data.length; i++) {
      const v = Math.pow(clamp(data[i] * 1.25), 0.73);
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
  function updateGap(root, result) {
    const vector=root.querySelectorAll('.paper-vector i');
    const linear=root.querySelectorAll('.linear-mini i');
    const max = Math.max(...result.gap,0.001);
    for(const elements of [vector,linear]) elements.forEach((el,i)=>{
      const intensity=clamp(result.gap[i]/max);
      el.style.backgroundColor = 'rgb('+
        Math.round(224-145*intensity)+','+
        Math.round(239-75*intensity)+','+
        Math.round(238-100*intensity)+')';
    });
    const rects=root.querySelectorAll('.gap-mini rect');
    if(rects.length>=17) {
      // Original first rect is the frame; replace the following 4x4 fill.
      for(let y=0;y<4;y++)for(let x=0;x<4;x++){
        let z=0;
        for(let j=0;j<8;j++)for(let i=0;i<8;i++)
          z += result.conv2[0][(y*8+j)*32+(x*8+i)];
        const intensity=clamp((z/64)*1.4);
        const rgb=[Math.round(235-182*intensity),Math.round(247-98*intensity),
          Math.round(246-104*intensity)];
        rects[1+y*4+x].setAttribute('fill','rgb('+rgb.join(',')+')');
      }
    }
  }
  function renderArchitecture(result) {
    const root=document.querySelector('.architecture-slide');
    if (!root) return;
    const targets=[
      ['.paper-conv .activation-stack',result.conv1,64,[0,3,6,9],'blue',true],
      ['.paper-pool .activation-stack',result.pool,32,[0,3,6,9],'teal',true],
      ['.paper-conv2 .activation-stack',result.conv2,32,[0,5,12,19,26],'blue',false]
    ];
    for(const [selector,maps,n,channels,palette,patch] of targets) {
      const svg=root.querySelector(selector);
      if(!svg)throw new Error('CNN illustration missing '+selector);
      layerStack(svg,maps,n,channels,palette,patch);
    }
    updateGap(root,result);
    const a=result.conv1[0],b=result.pool[0];
    const y=16,x=16;
    const actual=Math.max(
      a[2*y*64+2*x], a[2*y*64+2*x+1],
      a[(2*y+1)*64+2*x], a[(2*y+1)*64+2*x+1]
    );
    if(Math.abs(b[y*32+x]-actual)>1e-8)throw Error('Pooling mismatch');
    root.dataset.poolCheck='pass';
    root.dataset.computedMaps='true';
    root.dataset.gapLength=String(result.gap.length);
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
    if(!document.querySelector('.process-feature-svg,.compare-feature-svg,.architecture-slide'))return;
    const img = new Image();
    img.onload=()=> {
      try {
        const maps=compute(img);
        renderArchitecture(maps);renderSmallMotifs(maps);
      } catch(err) {console.error('Feature map rendering failed',err);}
    };
    img.onerror=()=>console.error('CNN source photograph could not load');
    img.src='assets/concept-apple-photo.jpg';
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',begin);
  else begin();
})();
