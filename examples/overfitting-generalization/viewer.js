(() => {
  'use strict';
  const frame = document.querySelector('.frame'), iframe = frame.querySelector('iframe');
  function resize() {
    const slide = document.body.dataset.mode === 'slides';
    const width = Math.min(1440, innerWidth - (slide ? 40 : 48), slide ? (innerHeight - 112) * 16 / 9 : Infinity);
    frame.style.width = `${width}px`; frame.style.height = `${width * 9 / 16}px`;
    iframe.style.transform = `scale(${width / 1440})`;
  }
  resize();addEventListener('resize', resize);
  let started = false;
  async function ready() {
    if (started || !iframe.contentDocument?.querySelector('.overfit-slide')) return;
    started = true;
    const state = document.querySelector('#load-state');
    try {
      await iframe.contentDocument.fonts.ready;
      await iframe.contentDocument.fonts.load('17px "STIX Two Math"', '0');
      const deadline = performance.now() + 8000;
      while (iframe.contentWindow.CurveExample?.status === 'loading' && performance.now() < deadline) await new Promise(r => setTimeout(r,50));
      if (iframe.contentWindow.CurveExample?.status !== 'ready') throw new Error('Curve unavailable');
      state.hidden = true;document.body.dataset.ready = 'true';
    } catch(e) {state.textContent='자료 일부를 읽지 못함 · 곡선 안내를 확인하세요.';document.body.dataset.ready='error';}
  }
  iframe.addEventListener('load', ready);
  if (iframe.contentDocument?.readyState === 'complete') ready();
})();
