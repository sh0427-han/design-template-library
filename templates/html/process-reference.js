/* #2 presentation only. Fixed-filter maps and example logits are independent
 * teaching illustrations, not one trained model's end-to-end inference. */
(() => {
  'use strict';
  const slide = document.querySelector('.process-slide');
  if (!slide) return;
  const logits = [2, 1, 0];
  const peak = Math.max(...logits);
  const exp = logits.map(value => Math.exp(value - peak));
  const total = exp.reduce((sum, value) => sum + value, 0);
  const probabilities = exp.map(value => value / total);
  const state = window.ProcessReference = {
    status: 'loading', exampleLogits: logits, probabilities,
    featureChannels: [0, 3, 6, 9], trainedInference: false,
  };
  const figure = slide.querySelector('[data-feature-state]');
  const svg = slide.querySelector('.process-feature-svg');
  const fallback = slide.querySelector('.feature-fallback');
  const photo = slide.querySelector('.process-photo');
  slide.querySelectorAll('[data-example-score]').forEach((text, i) => {text.textContent = String(logits[i]);});
  slide.querySelectorAll('.output-item').forEach((item, i) => {
    item.dataset.probability = String(probabilities[i]);
    item.dataset.highest = String(logits[i] === peak);
    item.querySelector('.probability-value').textContent = `${(probabilities[i] * 100).toFixed(1)}%`;
    item.querySelector('.probability-bar').setAttribute('width', String(220 * probabilities[i]));
  });
  const exampleDescription = [...slide.querySelectorAll('.output-item')].map(item =>
    `${item.dataset.class} ${item.querySelector('.probability-value').textContent}`).join(', ');
  slide.querySelector('.process-output-svg').setAttribute('aria-label', `예시 확률: ${exampleDescription}, 합계 100%`);
  slide.querySelector('.process-task-svg').setAttribute('aria-label', `요약된 특징 벡터를 분류 Head가 예시 점수 ${logits.join(', ')}으로 변환하는 모식도`);

  function centerArtwork(target) {
    const artwork = target.querySelector('[data-process-artwork]');
    if (!artwork) return;
    const bounds = artwork.getBBox(), box = target.viewBox.baseVal;
    artwork.setAttribute('transform', `translate(${box.width / 2 - bounds.x - bounds.width / 2} ${box.height / 2 - bounds.y - bounds.height / 2})`);
  }
  function centerAll() {
    slide.querySelectorAll('.process-art svg').forEach(centerArtwork);
  }
  function failed(reason) {
    state.status = 'error'; state.reason = reason;
    figure.dataset.featureState = 'error';
    fallback.hidden = false;
    fallback.innerHTML = '특징 맵을 불러오지 못함<br>사진·스크립트 경로 확인';
  }
  function imageFailed() {
    photo.hidden = true; slide.querySelector('.photo-fallback').hidden = false;
    failed('source_image_unavailable');
  }
  photo.addEventListener('error', imageFailed);
  if (photo.complete && !photo.naturalWidth) imageFailed();

  function enlargeMaps() {
    const images = [...svg.querySelectorAll('image')];
    const frames = [...svg.querySelectorAll('rect')];
    if (images.length !== 4 || frames.length !== 4) throw new Error('Expected four computed feature maps');
    const artwork = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    artwork.setAttribute('data-process-artwork', '');
    images.forEach((image, i) => {
      // Same upper-right depth direction and restrained plane outlines as #6.
      // Keep every computed 64x64 data URL intact; never copy its schematic data.
      const depth = 3 - i, x = 10 + depth * 15, y = 38 - depth * 10;
      const frame = frames[i];
      Object.entries({x:x-2, y:y-2, width:120, height:120, rx:1.5,
        fill:'#b7cdea', stroke:depth===0?'#4679b8':'#6e94c6',
        'stroke-width':depth===0?1.5:1.05}).forEach(([key,value]) => frame.setAttribute(key,String(value)));
      Object.entries({x, y, width:116, height:116}).forEach(([key,value]) => image.setAttribute(key,String(value)));
      image.dataset.channel = String(state.featureChannels[depth]);
      artwork.append(frame, image);
    });
    svg.replaceChildren(artwork); svg.setAttribute('viewBox', '0 0 184 164');
    figure.dataset.featureState = 'ready'; fallback.hidden = true;
    centerArtwork(svg); state.status = 'ready';
  }
  const started = performance.now();
  function awaitMaps() {
    if (state.status === 'error') return;
    const maps = window.CNNFeatureMaps;
    if (!maps) {failed('feature_engine_unavailable'); return;}
    if (maps.status === 'error') {failed('feature_calculation_failed'); return;}
    if (maps.status === 'ready') {
      try {enlargeMaps();} catch (error) {failed('feature_presentation_failed'); console.error(error);}
      return;
    }
    if (performance.now() - started > 8000) {failed('feature_loading_timeout'); return;}
    setTimeout(awaitMaps, 100);
  }
  if (state.status !== 'error') fallback.textContent = '사진에서 특징 맵 계산 중';
  centerAll(); document.fonts.ready.then(centerAll);
  window.addEventListener('resize', centerAll);
  awaitMaps();
})();
