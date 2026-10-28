"""Independent Python arithmetic and Chromium smoke checks for the new lesson."""
import json
import subprocess
from fractions import Fraction
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
BASE = 'http://127.0.0.1:8765/examples/interactive-kernel/'
DATA = json.loads((ROOT / 'data.json').read_text())
VIEWPORTS = [(1600, 950), (1440, 810), (1366, 768), (1280, 720)]


def reference(input_rows, kernel, denominator):
    # Distinct implementation from JS: Python Fraction, slice+zip dot products.
    values = []
    for r in range(5):
        row = []
        for c in range(5):
            cells = [input_rows[r+i][c:c+3] for i in range(3)]
            terms = (a*b for x,y in zip(cells,kernel) for a,b in zip(x,y))
            row.append(Fraction(sum(terms),denominator))
        values.append(row)
    return values


expected={}
for key,k in DATA['kernels'].items():
    expected[key] = reference(DATA['input'], k['numerators'], k['divisor'])
assert expected['identity'][2][1] == 6
assert expected['mean'][2][1] == Fraction(51, 9)
assert expected['edge'][2][1] == 28
assert min(map(min,expected['edge'])) == -28
assert max(map(max,expected['edge'])) == 28

js = '''const M = require('./model.js'); const d = require('./data.json');
const result = Object.fromEntries(['identity','mean','edge'].map(id => [id,M.evaluate(d,id)]));
console.log(JSON.stringify(result));'''
actual=json.loads(subprocess.check_output(['node','-e',js],cwd=ROOT,text=True))
for key,mat in expected.items():
    obj=actual[key]
    assert obj['outputNumerators'] == [[int(v * DATA['kernels'][key]['divisor']) for v in row] for row in mat]
    assert all(abs(obj['output'][r][c]-float(mat[r][c]))<1e-12 for r in range(5) for c in range(5))
    focus=obj['focus']
    assert focus['numerator'] == int(mat[2][1] * focus['denominator'])
    assert sum(sum(row) for row in focus['products']) == focus['numerator']

records=[]; errors=[]
# Chromium blocks network/file navigations. Inject the edited content and JS.
html = (ROOT/'content.html').read_text()
import re
html = re.sub(r'<link[^>]+>', '', html)
html = re.sub(r'<script src="(?:model|app)\.js"[^>]*></script>', '', html)
html = html.replace('</head>', '<style>'+ (ROOT/'lesson.css').read_text()+'</style></head>')
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
    for mode in ('scroll','slides'):
        for width,height in VIEWPORTS:
            page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
            page.on('pageerror',lambda e:errors.append(str(e)))
            page.set_content(html)
            page.evaluate("data => { window.fetch = async () => ({ok:true,json:async()=>data}); window.history.replaceState=()=>{}; }", DATA)
            page.add_script_tag(content=(ROOT/'model.js').read_text())
            page.add_script_tag(content=(ROOT/'app.js').read_text())
            page.wait_for_function("document.body.dataset.ready === 'true'",timeout=8000)
            focus=page.locator('.matrix-output .cell.focus')
            assert focus.inner_text() == '6'
            rect=page.locator('.kernel-slide').evaluate("e=>({scrollWidth:e.scrollWidth,clientWidth:e.clientWidth,scrollHeight:e.scrollHeight,clientHeight:e.clientHeight})")
            assert rect['scrollHeight']<=rect['clientHeight']+3,rect
            assert rect['scrollWidth']<=rect['clientWidth']+3,rect
            page.locator('#kernel-select').select_option('mean')
            assert focus.inner_text() == '5.67'
            assert page.locator('#focus-result').inner_text() == '= 51/9 ≈ 5.67'
            page.locator('#kernel-select').select_option('edge')
            assert focus.inner_text() == '28'
            for r in range(5):
                for c in range(5):
                    cell=page.locator('.matrix-output .cell').nth(r*5+c)
                    assert int(cell.get_attribute('data-numerator'))==int(expected['edge'][r][c]),(r,c)
            page.locator('#reset-kernel').click()
            assert focus.inner_text() == '6'
            page.screenshot(path=str(ROOT/'previews'/f'{mode}-{width}x{height}.png'),full_page=True)
            records.append({'mode':mode,'viewport':[width,height],'content':rect,'status':'passed-injected'})
            page.close()
    browser.close()
assert not errors,errors
report={'status':'partial','math':{'filters':3,'cells':75,'focus':{'identity':'6','mean':'51/9','edge':'28'}},'screens':records,'console_errors':errors,'limitations':['Chromium navigation blocked by administrator: content injected via set_content; real iframe/viewer and network paths not validated','Local staging does not contain canonical font assets; font load check pending','Independent agent reviewer not available']}
(ROOT/'previews'/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print('PASS math and injected Chromium',len(records),'screens')
