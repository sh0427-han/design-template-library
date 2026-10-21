"""Render only Concept and Architecture and verify their responsive geometry.

Requires: pip install playwright && python -m playwright install chromium
Outputs canonical screenshots and 4-viewport JSON evidence.
"""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import threading

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SIZES = ((1500, 950), (1366, 768), (1280, 720), (390, 844))
NAMES = ("concept", "architecture")


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


CHECK = """() => {
  const slide = document.querySelector('.slide');
  const rect = e => {
    const r = e.getBoundingClientRect();
    return {x:r.x,y:r.y,right:r.right,bottom:r.bottom,
      width:r.width,height:r.height};
  };
  const sr = rect(slide);
  const footer = rect(slide.querySelector('.footer'));
  const boxes = [...slide.querySelectorAll('.concept-stage,.value-panel,.visual-panel,.image-frame,.pixel-frame,.paper-pipeline,.paper-stage,.architecture-notes,.architecture-notes > div,.concept-panel,.ref-card')];
  const overflow = boxes.filter(e => e.scrollWidth > e.clientWidth + 2 ||
    e.scrollHeight > e.clientHeight + 2).map(e => e.className);
  const bodyChildren = [...slide.children].filter(e => e !== slide.querySelector('.footer'));
  const overlap = bodyChildren.filter(e => rect(e).bottom > footer.y + 1)
    .map(e => e.className);
  const photo = slide.querySelector('#concept-image');
  const img = slide.querySelector('.image-frame');
  const arrow = slide.querySelector('.zoom-arrow');
  const pixels = slide.querySelector('.pixel-frame');
  let arrows = null, labelSpacing = null, pixelRGB = null;
  if (img && arrow && pixels) {
    const mid = e => {const r=rect(e);return r.y+r.height/2};
    arrows=[Math.abs(mid(arrow)-mid(img)),Math.abs(mid(arrow)-mid(pixels))];
    const label=slide.querySelector('.image-unit .figure-label');
    labelSpacing=rect(label).y-rect(img).bottom;
    const color=slide.querySelector('.pixel-block .selected');
    const canvas=document.createElement('canvas');canvas.width=canvas.height=80;
    const ctx=canvas.getContext('2d');
    ctx.imageSmoothingEnabled=true;ctx.imageSmoothingQuality='high';
    ctx.drawImage(photo,0,0,80,80);
    pixelRGB=[...ctx.getImageData(54,39,1,1).data].slice(0,3);
    const shown=slide.querySelector('#selected-rgb').textContent;
    if(shown !== 'RGB (' + pixelRGB.join(', ') + ')')
      throw new Error('RGB labels do not match the photo: '+shown+' vs '+pixelRGB);
    if(getComputedStyle(color).backgroundColor !== 'rgb(' + pixelRGB.join(', ') + ')')
      throw new Error('Selected cell color does not match sampled RGB');
  }
  return {slide:sr,footer,overflow,overlap,pageWidth:document.documentElement.scrollWidth,
    imgLoaded:photo?photo.complete&&photo.naturalWidth>0:null,
    sampled:slide.dataset.sampled||null,arrows,labelSpacing,pixelRGB,
    spacing:getComputedStyle(slide.querySelector('h1')).letterSpacing,
    stages:slide.querySelectorAll('.paper-stage').length,
    gaps:slide.querySelectorAll('.paper-vector i').length,
    logits:slide.querySelectorAll('.paper-logits span').length,
    shapes:[...slide.querySelectorAll('.paper-shape')].map(e=>e.textContent.trim())};
}"""


def main():
    (ROOT / 'previews').mkdir(exist_ok=True)
    report = []
    server = ThreadingHTTPServer(
        ('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT))
    )
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
            page = browser.new_page(device_scale_factor=1)
            page_errors = []
            page.on('pageerror', lambda error: page_errors.append(str(error)))
            for width, height in SIZES:
                page.set_viewport_size({'width': width, 'height': height})
                for name in NAMES:
                    page.goto(
                        f'http://127.0.0.1:{server.server_port}'
                        f'/templates/html/{name}.html',
                        wait_until='networkidle',
                    )
                    page.evaluate('document.fonts.ready')
                    if name == 'concept':
                        page.wait_for_function(
                            "document.querySelector('.concept-slide').dataset.sampled === 'true'"
                        )
                    result = page.evaluate(CHECK)
                    assert not result['overflow'], (name,width,'overflow',result)
                    assert not result['overlap'], (name,width,'footer overlap',result)
                    assert result['pageWidth'] <= width, (name,width,'horizontal scroll',result)
                    assert abs(float(result['spacing'].removesuffix('px'))+4/3) < .02, (
                        name,width,'letter spacing',result
                    )
                    if name == 'concept':
                        assert result['imgLoaded'] and result['sampled']=='true'
                        assert max(result['arrows']) < 2.1, (name,width,'arrow',result)
                        assert 0 <= result['labelSpacing'] <= 25, result
                    else:
                        assert result['stages']==6 and result['gaps']==32 and result['logits']==3
                        assert result['shapes']==[
                            '64×64×3','64×64×16','32×32×16',
                            '32×32×32','32','3 logits'
                        ],result
                    if width > 900:
                        box = result['slide']
                        assert abs(box['width']/box['height']-16/9)<.002, result
                        assert box['right']<=width and box['bottom']<=height, result
                    report.append({'name':name,'viewport':[width,height],**result})
                    if width == 1500:
                        target = ROOT / 'previews' / (
                            'html-concept.png' if name=='concept'
                            else 'html-architecture.jpg'
                        )
                        options = {} if name=='concept' else {'quality':92}
                        page.locator('section.slide').screenshot(
                            path=str(target), animations='disabled', **options
                        )
            assert not page_errors, page_errors
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
    destination=ROOT/'previews'/'review'/'concept-architecture-validation.json'
    destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_text(
        json.dumps({'tested_viewports':SIZES,'results':report},ensure_ascii=False,indent=2)+'\n',
        encoding='utf-8'
    )
    print('PASS: 8 Chromium render checks + photo RGB verification')


if __name__=='__main__':
    main()
