"""Render and verify the eight standalone references with Chromium.

Requirements: Python Playwright and Chromium (CHROMIUM_EXECUTABLE overrides PATH).
Run: python scripts/render_previews.py
Executive only: python scripts/render_previews.py --templates executive-summary
Canonical previews are captured at 1500x950; viewport evidence and measurements
are written to --evidence-dir (default: /tmp/design-template-review).
"""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import shutil
import threading

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_IDS = (
    'concept', 'process', 'comparison', 'step-by-step',
    'interactive', 'architecture', 'experiment', 'executive-summary',
)
VIEWPORTS = ((1500, 950), (1366, 768), (1280, 720), (900, 900), (390, 844))


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


GEOMETRY = """() => {
    const slide = document.querySelector('.slide');
    const rect = e => {const r=e.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height,right:r.right,bottom:r.bottom}};
    const s=rect(slide), footer=rect(slide.querySelector('.footer'));
    const visible=[...slide.querySelectorAll('*')].filter(e=>e.getBoundingClientRect().width && e.getBoundingClientRect().height);
    const outside=visible.filter(e=>{const r=rect(e);return r.x<s.x-1 || r.right>s.right+1 || r.y<s.y-1 || r.bottom>s.bottom+1}).map(e=>e.className);
    const containers=[...slide.querySelectorAll('.content,.ref-grid,.ref-card,.concept-panel,.compare-card,.node,.arch-node,.executive-kpi,.exec-metric-group,.exec-metric-bars,.exec-impact,.exec-actions')];
    const overflow=containers.filter(e=>e.scrollWidth>e.clientWidth+1 || e.scrollHeight>e.clientHeight+1).map(e=>e.className);
    const footerOverlap=visible.filter(e=> !e.closest('footer') && !e.matches('script') && rect(e).bottom>footer.y+1).map(e=>e.className);
    const textElements=visible.filter(e=>[...e.childNodes].some(n=>n.nodeType===3 && n.textContent.trim()));
    const spacing=textElements.filter(e=>Math.abs(parseFloat(getComputedStyle(e).letterSpacing)+4/3)>.01).map(e=>e.className);
    const clippedText=[];
    for (const e of textElements) {
      if (e instanceof SVGElement) continue;
      const bounds=rect(e);
      for(const n of e.childNodes) {
        if(n.nodeType!==3 || !n.textContent.trim())continue;
        const range=document.createRange();range.selectNodeContents(n);
        for(const r of range.getClientRects()) if(r.left<bounds.x-1 || r.right>bounds.right+1) clippedText.push(e.className);
      }
    }
    const lines=selector=>{const e=slide.querySelector(selector);return +(e.getBoundingClientRect().height/(parseFloat(getComputedStyle(e).lineHeight)*parseFloat(getComputedStyle(slide).zoom))).toFixed(2)};
    const arrowErrors=[];
    for(const e of slide.querySelectorAll('.flow-arrow,.arch-arrow')) {
      if(innerWidth<=900)continue;
      const a=rect(e),p=rect(e.previousElementSibling),n=rect(e.nextElementSibling);
      if(Math.abs(a.y+a.height/2-p.y-p.height/2)>1 || Math.abs(a.y+a.height/2-n.y-n.height/2)>1)arrowErrors.push(e.className);
    }
    if(innerWidth>900 && slide.querySelector('.zoom-arrow')) {
      const a=rect(slide.querySelector('.zoom-arrow')), f=rect(slide.querySelector('.image-frame'));
      if(Math.abs(a.y+a.height/2-f.y-f.height/2)>1)arrowErrors.push('zoom-arrow');
    }
    return {slide:s,outside,overflow,footerOverlap,spacing,clippedText,arrowErrors,titleLines:lines('h1'),subtitleLines:lines('.subtitle'),pageWidth:document.documentElement.scrollWidth};
}"""


def check_interactive(page):
    # Independent oracle for all supported thresholds, including equality at .15.
    scores = (.15, .32, .48, .67, .82, .94)
    truths = (0, 1, 0, 1, 1, 0)
    results = []
    slider = page.locator('#threshold')
    for value in range(0, 101, 5):
        slider.fill(str(value))
        counts = dict(tp=0, tn=0, fp=0, fn=0)
        labels = []
        for score, truth in zip(scores, truths):
            predicted = score >= value / 100
            key = ('tp' if predicted else 'fn') if truth else ('fp' if predicted else 'tn')
            counts[key] += 1
            labels.append(key.upper())
        actual = {k: int(page.locator('#cm-' + k).inner_text()) for k in counts}
        assert actual == counts, (value, actual, counts)
        assert page.locator('.outcome').all_text_contents() == labels
        assert page.locator('#threshold-value').inner_text() == f'{value/100:.2f}'
        pct = lambda n, d: f'{100*n/d:.1f}%' if d else '정의 불가'
        assert page.locator('#precision').inner_text() == pct(counts['tp'], counts['tp']+counts['fp'])
        assert page.locator('#recall').inner_text() == pct(counts['tp'], counts['tp']+counts['fn'])
        assert abs(page.locator('.score-track').first.evaluate("e=>parseFloat(e.style.getPropertyValue('--threshold-pct'))") - value) < 1e-9
        results.append(dict(threshold=value, **counts))
    slider.focus()
    for key, expected in [('Home','0'), ('ArrowRight','5'), ('End','100'), ('ArrowLeft','95')]:
        slider.press(key)
        assert slider.input_value() == expected
    box = slider.bounding_box()
    slider.click(position={'x':box['width']/2,'y':box['height']/2})
    assert slider.input_value() == '50'
    slider.fill('60')
    return results


def check_executive(page, width):
    """Check displayed KPI values AND real vertical bar geometry independently."""
    result = page.evaluate("""() => {
      const box = el => {const r=el.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height,right:r.right,bottom:r.bottom}};
      const impact=document.querySelector('.exec-impact');
      const action=document.querySelector('.exec-action-panel');
      const groups=[...document.querySelectorAll('.exec-metric-group')];
      return {
        obsolete:document.querySelectorAll('.executive-kpis,.executive-kpi,.exec-track,.exec-bar').length,
        title:document.querySelector('h1').textContent,
        subtitle:document.querySelector('.subtitle').textContent,
        note:document.querySelector('.content > .ref-note').textContent,
        footer:[...document.querySelectorAll('.footer span')].map(e=>e.textContent),
        actions:[...document.querySelectorAll('.exec-action')].map(e=>({
          number:e.querySelector('strong').textContent,
          title:e.querySelector('b').textContent,
          detail:e.querySelector('span').lastChild.textContent
        })),
        impact:box(impact),action:box(action),
        groups:groups.map(g=>({
          box:box(g),title:g.querySelector('h3').textContent,
          before:Number(g.dataset.before),after:Number(g.dataset.after),unit:g.dataset.unit,
          delta:g.querySelector('.exec-delta').textContent,
          deltaColor:getComputedStyle(g.querySelector('.exec-delta')).color,
          values:[...g.querySelectorAll('.exec-value')].map(e=>e.textContent),
          labels:[...g.querySelectorAll('.exec-series')].map(e=>e.textContent),
          bars:[...g.querySelectorAll('.exec-fill')].map(e=>({
            ...box(e),color:getComputedStyle(e).backgroundColor,
            ratio:Number(e.style.getPropertyValue('--ratio'))
          })),
          border:getComputedStyle(g).borderStyle,
          background:getComputedStyle(g).backgroundColor
        }))
      };
    }""")
    assert result['obsolete'] == 0, (width, 'duplicate or horizontal KPI layout', result)
    expected = [
        ('월간 수동 점검',120,80,'건'),
        ('평균 처리 시간',45,30,'분/건'),
        ('월말 미처리',20,8,'건'),
    ]
    assert len(result['groups']) == 3, (width, result)
    previous = None
    for group, (title,before,after,unit) in zip(result['groups'],expected):
        assert (group['title'],group['before'],group['after'],group['unit']) == (title,before,after,unit), (width, group)
        delta=f'{(after-before)/before*100:.1f}%'.replace('-', '−')
        assert group['delta'] == delta and group['deltaColor'] == 'rgb(38, 166, 161)', (width, group)
        assert group['values'] == [f'{before}{unit}',f'{after}{unit}'], (width, group)
        assert group['labels'] == ['기존','개선안'] and len(group['bars']) == 2, (width, group)
        base,new=group['bars']
        assert base['color']=='rgb(49, 104, 200)' and new['color']=='rgb(38, 166, 161)', (width, group)
        assert abs(base['ratio']-1)<.0001 and abs(new['ratio']-after/before)<.0001, (width, group)
        assert base['height']>base['width'] and new['height']>0, (width, 'not vertical bars', group)
        assert abs(base['width']-new['width'])<1 and new['x']>base['right'], (width, 'bars not side by side', group)
        assert abs(base['bottom']-new['bottom'])<1, (width, 'unequal baselines', group)
        assert abs(new['height']/base['height']-after/before)<.002, (width, 'rendered height ratio', group)
        assert group['border']!='none' and group['background']=='rgb(255, 255, 255)', (width, group)
        if previous:
            assert group['box']['y']>previous['bottom'], (width, 'KPI cards not stacked', result)
        previous=group['box']
    assert result['title']=='점검 효율 개선안 요약'
    assert result['subtitle']=='수동 점검 부담 감소를 위한 파일럿 검토 · 효율성과 미검출 위험의 동시 평가'
    assert result['note']=='가상 시나리오 · 동일한 월간 유입량과 집계 기준 가정 · 실측 효과 아님'
    assert result['footer']==['Design Template Library · Executive-Summary','08 / 08']
    assert result['actions']==[
        dict(number='1',title='우선순위 설정',detail='점검 대상의 위험도와 처리 시점을 구분'),
        dict(number='2',title='파일럿 기준 통일',detail='동일 기준으로 도입 전·후 수치를 집계'),
        dict(number='3',title='확대 판단',detail='효율성과 미검출 위험을 함께 확인'),
    ], (width, 'Action content changed', result)
    if width>900:
        assert result['action']['x']>result['impact']['right'], (width, 'two-column layout', result)
    else:
        assert result['action']['y']>result['impact']['bottom'], (width, 'reading order', result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence-dir', type=Path, default=Path('/tmp/design-template-review'))
    parser.add_argument('--templates', nargs='+', choices=TEMPLATE_IDS, default=TEMPLATE_IDS,
                        help='Render selected templates without updating unrelated previews')
    args = parser.parse_args()
    args.evidence_dir.mkdir(parents=True, exist_ok=True)
    (ROOT/'previews').mkdir(exist_ok=True)
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    measurements = []
    interactions = []
    executive = []
    try:
        with sync_playwright() as p:
            executable = os.environ.get('CHROMIUM_EXECUTABLE') or shutil.which('chromium') or shutil.which('chromium-browser')
            browser = p.chromium.launch(headless=True, executable_path=executable, args=['--no-sandbox'])
            page = browser.new_page(device_scale_factor=1)
            errors = []
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.on('requestfailed', lambda request: errors.append(request.url))
            for width, height in VIEWPORTS:
                page.set_viewport_size(dict(width=width, height=height))
                for name in args.templates:
                    page.goto(f'http://127.0.0.1:{server.server_port}/templates/html/{name}.html')
                    page.evaluate('document.fonts.ready')
                    font_status = page.evaluate("""() => ({
                      family: getComputedStyle(
                        document.querySelector('h1')).fontFamily,
                      loaded: [...document.fonts].some(face =>
                        face.family.replace(/["']/g, '') ===
                          'Pretendard Variable' && face.status === 'loaded')
                    })""")
                    assert font_status['family'].startswith(
                        '"Pretendard Variable"'
                    ) and font_status['loaded'], (
                        name, width, 'Pretendard not applied', font_status
                    )
                    assert page.evaluate('CSS.supports("zoom", "calc(100vw / 1440px)")'), 'Browser lacks typed CSS division for zoom'
                    palette = page.evaluate("""() => {
                      const bg = el => getComputedStyle(el).backgroundColor;
                      const white = 'rgb(255, 255, 255)';
                      const cards = [...document.querySelectorAll(
                        '.reference-slide .ref-card, .reference-slide .concept-panel, ' +
                        '.reference-slide .compare-card'
                      )];
                      const takeaways = [...document.querySelectorAll('.ref-takeaway')];
                      const step = document.querySelector('.node.feature');
                      const output = document.querySelector('.node.output');
                      const ksp = [...document.querySelectorAll('.ref-chip')].some(
                        e => e.textContent.includes('K kernel')
                      );
                      return {
                        cardCount: cards.length,
                        nonwhiteCards: cards.filter(el => bg(el) !== white)
                          .map(el => el.className),
                        takeaways: takeaways.map(el => ({
                          bg: bg(el),
                          rule: getComputedStyle(el).borderLeftColor,
                          width: getComputedStyle(el).borderLeftWidth
                        })),
                        navLinks: [...document.querySelectorAll('header a')].filter(
                          e => e.textContent.includes('전체 레퍼런스')).length,
                        ksp,
                        process: step && output ? {
                          feature: bg(step), output: bg(output)
                        } : null
                      };
                    }""")
                    assert not palette['nonwhiteCards'], (
                        name, width, 'decorative card backgrounds', palette
                    )
                    assert palette['navLinks'] == 0 and not palette['ksp'], (
                        name, width, 'authoring UI present', palette
                    )
                    if name in ('concept', 'process'):
                        assert len(palette['takeaways']) == 1, (
                            name, width, 'missing takeaway', palette
                        )
                        takeaway = palette['takeaways'][0]
                        assert takeaway['bg'] == 'rgb(255, 255, 255)' and (
                            2.0 < float(takeaway['width'].removesuffix('px')) <= 4.01
                        ) and takeaway['rule'] == 'rgb(38, 166, 161)', (
                            name, width, 'takeaway does not match shared style',
                            palette
                        )
                    else:
                        assert not palette['takeaways'], (name, width, palette)
                    if name == 'process':
                        assert palette['process'] == {
                            'feature': 'rgb(234, 241, 255)',
                            'output': 'rgb(227, 246, 243)'
                        }, (name, width, 'lost meaningful stage colors', palette)
                    if name == 'executive-summary':
                        executive.append(dict(viewport=[width,height], **check_executive(page, width)))
                    m = page.evaluate(GEOMETRY)
                    for key in ('outside','overflow','footerOverlap','spacing','clippedText','arrowErrors'):
                        assert not m[key], (name, width, key, m[key])
                    assert m['pageWidth'] <= width, (name, width, m)
                    if width > 900:
                        r = m['slide']
                        assert abs(r['width']/r['height']-16/9)<.002
                        assert r['bottom'] <= height and r['right'] <= width
                        assert m['titleLines'] == 1 and m['subtitleLines'] == 1, (name, width, m)
                    measurements.append(dict(template=name, viewport=[width,height], font=font_status, **m))
                    if name == 'interactive':
                        interactions.append(dict(viewport=[width,height],thresholds=check_interactive(page)))
                    page.screenshot(path=str(args.evidence_dir/f'{name}-{width}.png'), full_page=True)
                    if width == 1500:
                        ext = 'png' if name in TEMPLATE_IDS[:3] else 'jpg'
                        options = {'quality':92} if ext == 'jpg' else {}
                        page.locator('.slide').screenshot(path=str(ROOT/'previews'/f'html-{name}.{ext}'), animations='disabled', **options)
            assert not errors, errors
            report = dict(browser=browser.version, viewports=VIEWPORTS, measurements=measurements, interactive=interactions, executive=executive, errors=errors)
            (args.evidence_dir/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
    print(f'PASS: {len(measurements)} renders; {len(interactions)} interactive viewport checks; {len(executive)} KPI checks; Pretendard loaded, no geometry, spacing or runtime errors.')


if __name__ == '__main__':
    main()

