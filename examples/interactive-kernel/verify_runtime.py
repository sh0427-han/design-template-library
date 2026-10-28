"""Real HTTP Chromium verification for both CNN kernel learning modes."""
import json
import threading
from fractions import Fraction
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / 'data.json').read_text())
SIZES = ((1600, 950), (1440, 810), (1366, 768), (1280, 720))
EVIDENCE = ROOT / 'review' / 'browser-evidence'
EVIDENCE.mkdir(parents=True, exist_ok=True)


class Handler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def expected(kid):
    k = DATA['kernels'][kid]
    return [[Fraction(sum(DATA['input'][r+i][c+j]*k['numerators'][i][j]
                          for i in range(3) for j in range(3)), k['divisor'])
             for c in range(5)] for r in range(5)]


def main():
    http = ThreadingHTTPServer(('127.0.0.1', 0), partial(Handler, directory=str(ROOT.parents[1])))
    threading.Thread(target=http.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{http.server_port}/examples/interactive-kernel/'
    results = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            try:
                for mode in ('scroll', 'slides'):
                    for width, height in SIZES:
                        page = browser.new_page(viewport={'width': width, 'height': height})
                        errors = []
                        page.on('pageerror', lambda e: errors.append(str(e)))
                        page.goto(f'{base}{mode}.html?v=1&kernel=identity#kernel')
                        page.wait_for_function('window.KernelViewer?.getState()?.status === "ready"')
                        frame = page.frame_locator('iframe')
                        assert frame.locator('#input-matrix .cell').count() == 49
                        assert frame.locator('#kernel-matrix .cell').count() == 9
                        assert frame.locator('#output-matrix .cell').count() == 25
                        for kid in ('identity', 'mean', 'edge'):
                            frame.locator('#kernel-select').select_option(kid)
                            state = page.evaluate('window.KernelViewer.getState()')
                            assert state['kernelId'] == kid
                            expected_matrix = expected(kid)
                            denom = DATA['kernels'][kid]['divisor']
                            assert all(state['outputNumerators'][r][c] == int(expected_matrix[r][c] * denom)
                                       for r in range(5) for c in range(5))
                            assert all(abs(state['output'][r][c] - float(expected_matrix[r][c])) < 1e-12
                                       for r in range(5) for c in range(5))
                        frame.locator('#kernel-select').select_option('mean')
                        assert '/ 9' in frame.locator('#focus-equation').inner_text()
                        assert frame.locator('.matrix-output .cell.focus').inner_text() == '5.67'
                        frame.locator('#kernel-select').select_option('edge')
                        assert frame.locator('.matrix-output .cell.focus').inner_text() == '28'
                        page.wait_for_function('location.search.includes("kernel=edge")')
                        assert page.url.endswith('?v=1&kernel=edge#kernel')
                        frame.locator('#reset-kernel').click()
                        assert frame.locator('.matrix-output .cell.focus').inner_text() == '6'
                        info = page.evaluate('''() => {
                          const rect=document.querySelector('.frame').getBoundingClientRect();
                          return {left:rect.left,right:rect.right,bottom:rect.bottom};
                        }''')
                        assert info['left'] >= -1 and info['right'] <= width+2, info
                        if mode == 'slides':
                            assert info['bottom'] <= height+2, info
                        font = frame.locator('body').evaluate('''async () => {
                          await document.fonts.load('17px "Pretendard Variable"');
                          await document.fonts.load('18px "STIX Two Math"');
                          return {faces:Array.from(document.fonts).map(f=>[f.family,f.status]),
                            letterSpacing:getComputedStyle(document.documentElement).letterSpacing,
                            overflow:document.querySelector('.kernel-slide').scrollHeight >
                              document.querySelector('.kernel-slide').clientHeight+3};
                        }''')
                        for family in ('Pretendard Variable', 'STIX Two Math'):
                            assert any(family in name and status=='loaded'
                                       for name,status in font['faces']), (family, font)
                        assert font['letterSpacing'].startswith('-1.3'), font
                        assert not font['overflow'], font
                        assert not errors, errors
                        page.screenshot(path=str(EVIDENCE/f'{mode}-{width}x{height}.png'), full_page=True)
                        results.append({'mode':mode,'viewport':[width,height],'font':font,'status':'passed-real-url'})
                        page.close()

                page = browser.new_page(viewport={'width':1440,'height':810})
                page.goto(f'{base}slides.html?v=1&kernel=mean#kernel')
                page.wait_for_function('window.KernelViewer?.getState()?.status === "ready"')
                frame = page.frame_locator('iframe')
                assert frame.locator('#kernel-select').input_value() == 'mean'
                page.reload()
                page.wait_for_function('window.KernelViewer?.getState()?.status === "ready"')
                assert frame.locator('#kernel-select').input_value() == 'mean'
                page.locator('#scroll-mode').click()
                page.wait_for_function('window.KernelViewer?.getState()?.status === "ready"')
                assert frame.locator('#kernel-select').input_value() == 'mean'
                frame.locator('#kernel-select').focus()
                frame.locator('#kernel-select').press('End')
                page.wait_for_function('window.KernelViewer?.getState()?.kernelId === "edge"')
                assert frame.locator('#kernel-select').evaluate('e=>document.activeElement===e')
                before=page.evaluate('window.KernelViewer.getState()')
                try:
                    page.evaluate("window.KernelViewer.selectKernel('invalid')")
                    raise AssertionError('invalid selectKernel must throw')
                except Exception as e:
                    assert '알 수 없는 필터' in str(e)
                assert before == page.evaluate('window.KernelViewer.getState()')
                page.goto(f'{base}slides.html?v=999&kernel=invalid#other')
                page.wait_for_function('window.KernelViewer?.getState()?.status === "ready"')
                assert page.evaluate('window.KernelViewer.getState().kernelId')=='identity'
                assert page.locator('#url-notice').is_visible()
                page.close()

                page = browser.new_page(viewport={'width':1440,'height':810})
                page.route('**/data.json', lambda route: route.abort())
                page.goto(f'{base}slides.html')
                page.wait_for_function('window.KernelViewer?.getState()?.status === "error"')
                frame = page.frame_locator('iframe')
                assert frame.locator('#kernel-select').is_disabled()
                assert frame.locator('#output-matrix .cell').count()==0
                page.unroute('**/data.json')
                frame.locator('#retry-data').click()
                page.wait_for_function('window.KernelViewer?.getState()?.status === "ready"')
                assert frame.locator('#output-matrix .cell').count()==25
                page.close()
            finally:
                browser.close()
    finally:
        http.shutdown()
        http.server_close()
    report={'status':'passed','real_url_screens':len(results),'screens':results,
            'state_and_error_scenarios':'passed'}
    (EVIDENCE/'runtime-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    assert len(results)==8
    print('PASS real viewer URL and iframe: 8 screens, fonts and interaction')


if __name__ == '__main__':
    main()
