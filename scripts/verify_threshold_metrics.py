"""Independent integer/Fraction oracle and Chromium QA for the fourth reuse test.

No production JavaScript calculation is used to construct expected answers.
Screen cases (16) and threshold/data scenarios are separate report fields.
"""
from argparse import ArgumentParser
from datetime import datetime, timezone
from fractions import Fraction
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import hashlib, json, re, subprocess, threading, traceback
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / 'examples/threshold-metrics'
BASELINE = 'ef9783e910f07a5e2c9343da17573e1a7cf30225'
SIZES = ((1600, 950), (1440, 810), (1366, 768), (1280, 720))
METRICS = ('precision', 'recall', 'accuracy', 'f1')
NORMAL_ERRORS, NORMAL_FAILED_REQUESTS, NORMAL_HTTP_ERRORS = [], [], []


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def percent(numerator, denominator):
    """Exact decimal half-up rounding; never round P/R before computing F1."""
    if not denominator:
        return '—'
    tenths, remainder = divmod(numerator * 1000, denominator)
    tenths += 2 * remainder >= denominator
    return f'{tenths // 10}.{tenths % 10}%'


def oracle(samples, threshold):
    counts = dict.fromkeys(('tp', 'fp', 'tn', 'fn'), 0)
    predictions = []
    for item in samples:
        predicted = int(item['scoreUnits'] >= threshold)
        code = ('tp' if predicted else 'fn') if item['truth'] else ('fp' if predicted else 'tn')
        counts[code] += 1
        predictions.append({**item, 'prediction': predicted, 'type': code.upper()})
    tp, fp, tn, fn = (counts[k] for k in ('tp', 'fp', 'tn', 'fn'))
    fractions = {'precision': (tp, tp + fp), 'recall': (tp, tp + fn),
                 'accuracy': (tp + tn, len(samples)), 'f1': (2 * tp, 2 * tp + fp + fn)}
    values = {k: Fraction(n, d) if d else None for k, (n, d) in fractions.items()}
    if values['precision'] is not None and values['recall'] is not None:
        p, r = values['precision'], values['recall']
        if p + r:
            assert values['f1'] == 2 * p * r / (p + r)
    return {'counts': counts, 'predictions': predictions, 'fractions': fractions,
            'ratios': values, 'display': {k: percent(*fraction) for k, fraction in fractions.items()}}


def protected_sources():
    paths = ['templates/', 'examples/logistic-regression/', 'examples/gradient-descent/',
             'examples/overfitting-generalization/']
    changed = subprocess.check_output(['git', 'diff', '--name-only', BASELINE, '--', *paths], cwd=ROOT).decode().splitlines()
    assert not changed, ('protected prior source changed', changed)
    return {'baseline': BASELINE, 'protected_directories': paths, 'changed_paths': changed,
            'checked_before_regression_generates_previews': True}


def read_data():
    data = json.loads((CASE / 'data.json').read_text())
    assert data['version'] == 1 and set(data['datasets']) == {'default', 'shifted'}
    for name, dataset in data['datasets'].items():
        samples = dataset['samples']
        assert 12 <= len(samples) <= 16
        assert len({s['id'] for s in samples}) == len(samples)
        assert len({s['scoreUnits'] for s in samples}) == len(samples)
        assert all(isinstance(s['id'], str) and s['id'].strip() and type(s['truth']) is int and s['truth'] in (0, 1)
                   and type(s['scoreUnits']) is int and 0 <= s['scoreUnits'] <= 100 for s in samples)
        assert {s['truth'] for s in samples} == {0, 1}
    default, shifted = (data['datasets'][k]['samples'] for k in ('default', 'shifted'))
    assert len(default) == len(shifted) == 14
    assert sum(s['truth'] for s in default) == 7 and sum(s['truth'] for s in shifted) == 4
    assert oracle(default, 50)['counts'] == dict(tp=5, fp=3, tn=4, fn=2)
    assert oracle(shifted, 50)['counts'] == dict(tp=3, fp=4, tn=6, fn=1)
    assert next(s for s in oracle(default, 50)['predictions'] if s['id'] == 'D03')['prediction'] == 1
    return data


def node_crosscheck(data):
    """Run the production model, but compare to separately derived Python truths."""
    script = r"""const fs=require('fs'), model=require(process.argv[1]), data=JSON.parse(fs.readFileSync(0,'utf8'));
const cases=[];
for(const [dataset,info] of Object.entries(data.datasets)){
 const samples=model.validateSamples(info.samples);
 for(let threshold=0;threshold<=100;threshold++){
  const result=model.evaluate(samples,threshold);
  cases.push({dataset,threshold,...result,display:Object.fromEntries(Object.entries(result.fractions).map(([k,v])=>[k,model.percent(v)]))});
 }
}
const custom=[[],[{id:'P',scoreUnits:50,truth:1}],[{id:'N',scoreUnits:50,truth:0}],[{id:'ZERO',scoreUnits:0,truth:1},{id:'ONE',scoreUnits:100,truth:0}]];
const special=[];
for(const samples of custom)for(const threshold of [0,49,50,51,100]){const result=model.evaluate(model.validateSamples(samples),threshold);special.push({samples,threshold,...result,display:Object.fromEntries(Object.entries(result.fractions).map(([k,v])=>[k,model.percent(v)]))});}
const invalid=[null,{},[{id:'a',scoreUnits:-1,truth:0}],[{id:'a',scoreUnits:101,truth:0}],[{id:'a',scoreUnits:0.5,truth:0}],[{id:'a',scoreUnits:50,truth:2}],[{id:'',scoreUnits:50,truth:1}],[{id:'a',scoreUnits:50,truth:0},{id:'a',scoreUnits:80,truth:1}]];
let rejected=0;for(const samples of invalid){try{model.validateSamples(samples);}catch(e){rejected++;}}
let rejectedThresholds=0;for(const t of [-1,101,0.5,NaN,Infinity,'50']){try{model.validateThreshold(t);}catch(e){rejectedThresholds++;}}
process.stdout.write(JSON.stringify({cases,special,rejected,rejectedThresholds}));
"""
    result = subprocess.run(['node', '-e', script, str(CASE/'model.js')], input=json.dumps(data), capture_output=True, text=True, check=True)
    results = json.loads(result.stdout)
    for actual in results['cases'] + results['special']:
        samples = actual.get('samples', data['datasets'][actual.get('dataset', 'default')]['samples'])
        expected = oracle(samples, actual['threshold'])
        assert actual['counts'] == expected['counts'] and actual['display'] == expected['display']
        assert [(s['id'],s['prediction'],s['type']) for s in actual['predictions']] == [(s['id'],s['prediction'],s['type']) for s in expected['predictions']]
        for key in METRICS:
            n,d = expected['fractions'][key]
            assert actual['fractions'][key] == {'numerator': n, 'denominator': d}
            assert actual['metrics'][key] is None if not d else abs(actual['metrics'][key] - float(expected['ratios'][key])) < 1e-14
    assert len(results['cases']) == 202 and len(results['special']) == 20
    assert results['rejected'] == 8 and results['rejectedThresholds'] == 6
    return {'production_model_vs_independent_python_states': 202, 'special_states': 20,
            'rejected_invalid_samples': 8, 'rejected_invalid_thresholds': 6,
            'expected_answers_from_production_code': False}


SNAPSHOT = """() => ({
 state:window.ThresholdMetrics.getState(),
 threshold:document.querySelector('#threshold').value,
 readout:document.querySelector('#threshold-value').textContent.trim(),
 tiles:[...document.querySelectorAll('.sample-tile')].map(e=>({id:e.dataset.sample,
 truth:Number(e.dataset.truth),scoreUnits:Number(e.dataset.scoreUnits),prediction:Number(e.dataset.prediction),
 type:e.dataset.type,text:e.textContent,aria:e.getAttribute('aria-label'),
 groupTruth:Number(e.closest('.sample-group').dataset.truth),
 scorePercent:parseFloat(e.querySelector('.sample-fill').style.width),thresholdPercent:parseFloat(e.style.getPropertyValue('--threshold-pct')),
 predictionColor:getComputedStyle(e.querySelector('.sample-prediction')).color,
 typeColor:getComputedStyle(e.querySelector('.sample-type')).color,
 trackWidth:e.querySelector('.sample-track').getBoundingClientRect().width,
 fillWidth:e.querySelector('.sample-fill').getBoundingClientRect().width})),
 counts:Object.fromEntries(['tp','fp','tn','fn'].map(k=>[k,document.querySelector('#cm-'+k).textContent.trim()])),
 metrics:Object.fromEntries(['precision','recall','accuracy','f1'].map(k=>{const e=document.querySelector('[data-metric="'+k+'"]'),c=e.querySelector('.metric-calculation'),f=c.querySelector('mfrac');return [k,{
 value:e.querySelector('.metric-value').textContent.trim(),text:e.textContent,
 numerator:c.dataset.numerator,denominator:c.dataset.denominator,
 renderedFraction:f?[...f.children].map(x=>x.textContent.trim()):null,
 calculation:c.textContent,aria:c.getAttribute('aria-label')}]}))
})"""


def check_snapshot(page, samples, threshold):
    expected = oracle(samples, threshold)
    actual = page.evaluate(SNAPSHOT)
    state = actual['state']
    assert state['status'] == 'ready' and state['thresholdUnits'] == threshold
    assert state['threshold'] == threshold / 100
    assert actual['threshold'] == str(threshold) and actual['readout'] == f'{threshold / 100:.2f}'
    assert state['counts'] == expected['counts']
    assert {k: int(v) for k, v in actual['counts'].items()} == expected['counts']
    wanted = {s['id']: s for s in expected['predictions']}
    assert len(actual['tiles']) == len(wanted)
    for sample in actual['tiles']:
        item = wanted[sample['id']]
        assert all(sample[k] == item[k] for k in ('truth', 'scoreUnits', 'prediction', 'type')), (sample, item)
        assert sample['groupTruth'] == item['truth']
        assert sample['scorePercent'] == item['scoreUnits'] and sample['thresholdPercent'] == threshold
        assert abs(sample['fillWidth']-sample['trackWidth']*item['scoreUnits']/100)<.15
        assert sample['predictionColor'] == ('rgb(49, 104, 200)' if item['prediction'] else 'rgb(100, 116, 139)')
        assert sample['typeColor'] == ('rgb(18, 107, 101)' if item['type'] in ('TP','TN') else 'rgb(148, 86, 22)')
        assert sample['id'] in sample['text'] and f"{sample['scoreUnits'] / 100:.2f}" in sample['text']
        assert ('불량' if sample['prediction'] else '정상') in sample['text'] and sample['type'] in sample['text']
        assert sample['aria'] and sample['id'] in sample['aria'] and sample['type'] in sample['aria']
    for key in METRICS:
        metric = actual['metrics'][key]
        n, d = expected['fractions'][key]
        value = expected['ratios'][key]
        assert metric['value'] == expected['display'][key], (threshold, key, metric, expected)
        assert int(metric['numerator']) == n and int(metric['denominator']) == d
        assert metric['renderedFraction'] == [str(n), str(d)], (key, metric)
        if d:
            assert abs(state['metrics'][key] - float(value)) < 1e-14
            assert expected['display'][key] in metric['calculation']
        else:
            assert state['metrics'][key] is None
            assert '분모' in metric['text'] or '정의' in metric['text'], metric
        assert state['fractions'][key] == {'numerator': n, 'denominator': d}
        assert 'NaN' not in metric['text'] and 'Infinity' not in metric['text']
    return {'thresholdUnits': threshold, 'counts': expected['counts'], 'display': expected['display']}


def formula_semantics(page):
    actual=page.evaluate("""()=>Object.fromEntries(['precision','recall','accuracy','f1'].map(k=>{const e=document.querySelector('[data-metric="'+k+'"]'),f=e.querySelector('.metric-formula mfrac');return [k,{fraction:[...f.children].map(n=>n.textContent.replace(/\\s+/g,'')),meaning:e.querySelector('.metric-meaning').textContent.trim()}];}))""")
    expected={'precision':['TP','TP+FP'],'recall':['TP','TP+FN'],'accuracy':['TP+TN','N'],'f1':['2TP','2TP+FP+FN']}
    assert {key:value['fraction'] for key,value in actual.items()}==expected,actual
    harmonic=page.locator('.harmonic-equivalent mfrac').evaluate('(e)=>[...e.children].map(n=>n.textContent.replace(/\\s+/g,""))')
    normalized=[part.replace('Precision','P').replace('Recall','R').replace('×','') for part in harmonic]
    assert normalized==['2PR','P+R'],harmonic
    assert all(value['meaning'] for value in actual.values())
    return {'metric_formulas':actual,'conditional_harmonic_equivalent':harmonic}


GEOMETRY = r"""id => {
 const s=document.getElementById(id), box=e=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y,right:r.right,bottom:r.bottom,width:r.width,height:r.height}};
 const sb=box(s),scale=sb.width/1440,fb=box(s.querySelector('footer'));
 const visible=[...s.querySelectorAll('*')].filter(e=>!e.closest('.sr-only,[hidden],noscript')&&!e.matches('title,desc,script,style,option')&&box(e).width&&box(e).height);
 const name=e=>e.id||e.getAttribute('class')||e.tagName;
 const outside=visible.filter(e=>{const r=box(e);return r.x<sb.x-1||r.right>sb.right+1||r.y<sb.y-1||r.bottom>sb.bottom+1}).map(name);
 const overflow=visible.filter(e=>e instanceof HTMLElement && !e.matches('input,select') && e.scrollWidth>e.clientWidth+1).map(name);
 const footerOverlap=visible.filter(e=>!e.closest('footer')&&box(e).bottom>fb.y+1).map(name);
 const text=visible.filter(e=>[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()));
 const spacing=text.filter(e=>Math.abs(parseFloat(getComputedStyle(e).letterSpacing)+4/3)>.02).map(name);
 const textClipping=[];
 for(const e of text){if(e instanceof SVGElement||e.closest('math')||e.matches('select,option'))continue;const b=box(e);for(const n of e.childNodes){if(n.nodeType!==3||!n.textContent.trim())continue;const r=document.createRange();r.selectNodeContents(n);for(const a of r.getClientRects())if(a.left<b.x-1||a.right>b.right+1||a.top<b.y-2||a.bottom>b.bottom+2)textClipping.push(name(e));}}
 const panels=[...s.querySelectorAll('.teaching-panel')].map(p=>{const b=box(p),st=getComputedStyle(p),inside={x:b.x+(parseFloat(st.paddingLeft)+parseFloat(st.borderLeftWidth))*scale,right:b.right-(parseFloat(st.paddingRight)+parseFloat(st.borderRightWidth))*scale,y:b.y+(parseFloat(st.paddingTop)+parseFloat(st.borderTopWidth))*scale,bottom:b.bottom-(parseFloat(st.paddingBottom)+parseFloat(st.borderBottomWidth))*scale};
 const escaped=[...p.querySelectorAll('*')].filter(e=>!e.closest('.sr-only,[hidden]')&&!e.matches('title,desc,script,style,option')&&box(e).width&&box(e).height).filter(e=>{const r=box(e);return r.x<inside.x-1||r.right>inside.right+1||r.y<inside.y-1||r.bottom>inside.bottom+1}).map(name);
 const labels=[...p.querySelectorAll('.panel-label')].filter(e=>e.closest('.teaching-panel')===p),titles=[...p.querySelectorAll('.panel-title')].filter(e=>e.closest('.teaching-panel')===p);
 return {escaped,labelCount:labels.length,titleCount:titles.length,labelColor:getComputedStyle(labels[0]).color,titleColor:getComputedStyle(titles[0]).color};});
 const metricEscaped=[];
 for(const p of s.querySelectorAll('.metric')){const b=box(p),st=getComputedStyle(p),inside={x:b.x+(parseFloat(st.paddingLeft)+1)*scale,right:b.right-(parseFloat(st.paddingRight)+1)*scale,y:b.y+(parseFloat(st.paddingTop)+1)*scale,bottom:b.bottom-(parseFloat(st.paddingBottom)+1)*scale};
 for(const e of p.querySelectorAll('*')){if(e.closest('[hidden]')||getComputedStyle(e).display==='none')continue;const r=box(e);if(r.width&&r.height&&(r.x<inside.x-1||r.right>inside.right+1||r.y<inside.y-1||r.bottom>inside.bottom+1))metricEscaped.push(p.dataset.metric+':'+name(e));}}
 const svgOutside=[],svgCollisions=[];
 for(const svg of s.querySelectorAll('svg')){const boundary=box(svg),texts=[...svg.querySelectorAll('text')].filter(e=>box(e).width&&box(e).height);for(const e of texts){const r=box(e);if(r.x<boundary.x-1||r.right>boundary.right+1||r.y<boundary.y-1||r.bottom>boundary.bottom+1)svgOutside.push(name(e));}for(let i=0;i<texts.length;i++)for(let j=i+1;j<texts.length;j++){const a=box(texts[i]),b=box(texts[j]);if(a.x<b.right-.5&&a.right>b.x+.5&&a.y<b.bottom-.5&&a.bottom>b.y+.5)svgCollisions.push([name(texts[i]),name(texts[j])]);}}
 const bar=document.querySelector('.viewer-bar'),barBottom=bar?box(bar).bottom:0;
 return {slide:sb,scale,outside,overflow,footerOverlap,spacing,textClipping,panels,metricEscaped,svgOutside,svgCollisions,
 viewportContainment:{top:sb.y,bottom:sb.bottom,barBottom,height:innerHeight,fullyVisible:sb.y>=barBottom-.5&&sb.bottom<=innerHeight+.5},
 heading:s.querySelector('h1').textContent,footerText:s.querySelector('footer').textContent,
 htmlOverflow:document.documentElement.scrollWidth>innerWidth+1};
}"""


def geometry(page, slide):
    result = page.evaluate(GEOMETRY, slide)
    assert result['slide']['width'] > 0 and result['slide']['height'] > 0
    for key in ('outside', 'overflow', 'footerOverlap', 'spacing', 'textClipping', 'svgOutside', 'svgCollisions','metricEscaped'):
        assert not result[key], (slide, key, result[key])
    assert not result['htmlOverflow']
    assert result['viewportContainment']['fullyVisible'], (slide, 'screenshot viewport clips the source', result['viewportContainment'])
    assert len(result['panels']) == 1
    for panel in result['panels']:
        assert not panel['escaped'], (slide, 'inner padding', panel)
        assert panel['labelCount'] == panel['titleCount'] == 1
        assert panel['labelColor'] == 'rgb(49, 104, 200)' and panel['titleColor'] == 'rgb(18, 35, 63)'
    return result


MATRIX = r"""() => {
 const t=document.querySelector('#practice table'),b=e=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y,right:r.right,bottom:r.bottom,cx:r.x+r.width/2,cy:r.y+r.height/2,width:r.width,height:r.height}};
 const text=e=>{const w=document.createTreeWalker(e,NodeFilter.SHOW_TEXT),rects=[];while(w.nextNode()){if(!w.currentNode.textContent.trim())continue;const r=document.createRange();r.selectNodeContents(w.currentNode);rects.push(r.getBoundingClientRect());}return {left:Math.min(...rects.map(r=>r.left)),right:Math.max(...rects.map(r=>r.right))};};
 const cell=k=>t.querySelector('#cm-'+k).closest('td');
 const tp=cell('tp'),fp=cell('fp'),fn=cell('fn'),tn=cell('tn');
 const cols=[...t.querySelectorAll('th[scope=col]')],rows=[...t.querySelectorAll('th[scope=row]')],gt=t.querySelector('th[scope=colgroup]'),axis=t.querySelector('th[scope=rowgroup]');
 const divider=t.parentElement.querySelector('.prediction-divider,.live-pred-divider,.matrix-divider');
 const axisText=text(axis),rowLeft=Math.min(...rows.map(e=>text(e).left)),line=b(divider);
 return {caption:!!t.querySelector('caption'),columnText:cols.map(e=>e.textContent),rowText:rows.map(e=>e.textContent),
 cells:[tp,fp,fn,tn].map(e=>({headers:e.getAttribute('headers'),background:getComputedStyle(e).backgroundColor,code:e.textContent.trim(),ids:(e.getAttribute('headers')||'').split(/\s+/).map(id=>!!document.getElementById(id))})),
 colErrors:[Math.abs(b(cols[0]).cx-b(tp).cx),Math.abs(b(cols[1]).cx-b(fp).cx)],
 rowErrors:[Math.abs(b(rows[0]).cy-b(tp).cy),Math.abs(b(rows[1]).cy-b(fn).cy)],
 gtError:Math.abs(b(gt).cx-(b(tp).x+b(fp).right)/2),axisError:Math.abs(b(axis).cy-(b(tp).y+b(fn).bottom)/2),
 dividerError:Math.abs((line.cx-axisText.right)-(rowLeft-line.cx)),dividerHeightError:Math.abs(line.height-b(axis).height),
 countCenterErrors:[tp,fp,fn,tn].map(e=>{const n=e.querySelector('strong,.cm-count');return Math.abs(b(n).cx-b(e).cx)})};
}"""


def matrix(page):
    result = page.evaluate(MATRIX)
    assert result['caption'] and len(result['columnText']) == len(result['rowText']) == 2
    assert '불량' in result['columnText'][0] and '정상' in result['columnText'][1]
    assert '불량' in result['rowText'][0] and '정상' in result['rowText'][1]
    for key in ('colErrors', 'rowErrors', 'countCenterErrors'):
        assert max(result[key]) < 2, (key, result)
    assert result['gtError'] < 2 and result['axisError'] < 2
    assert result['dividerError'] < .25 and result['dividerHeightError'] < 1
    assert all(c['headers'] and all(c['ids']) for c in result['cells'])
    assert result['cells'][0]['background'] == result['cells'][3]['background']
    assert result['cells'][1]['background'] == result['cells'][2]['background']
    assert result['cells'][0]['background'] != result['cells'][1]['background']
    return result


def connectors(page):
    result = page.evaluate(r"""() => {
      const svg=document.querySelector('.concept-connectors'),r=svg.getBoundingClientRect(),v=svg.viewBox.baseVal,sx=r.width/v.width,sy=r.height/v.height;
      return [...svg.querySelectorAll('path[data-from][data-to]')].map(path=>{const a=document.getElementById(path.dataset.from).getBoundingClientRect(),b=document.getElementById(path.dataset.to).getBoundingClientRect(),start=[+path.dataset.startX,+path.dataset.startY],end=[+path.dataset.endX,+path.dataset.endY];return {id:path.id,from:path.dataset.from,to:path.dataset.to,start,end,d:path.getAttribute('d'),expectedStart:[(a.right-r.left)/sx+5,(a.y+a.height/2-r.top)/sy],expectedEnd:[(b.x-r.left)/sx-5,(b.y+b.height/2-r.top)/sy]};});
    }""")
    assert len(result) == 4
    for connection in result:
        assert connection['end'][0] > connection['start'][0], connection
        assert max(abs(a-b) for a,b in zip(connection['start'],connection['expectedStart'])) < 1
        assert max(abs(a-b) for a,b in zip(connection['end'],connection['expectedEnd'])) < 1
        numbers=[float(n) for n in re.findall(r'-?\d+(?:\.\d+)?(?:e[+\-]?\d+)?',connection['d'],re.I)]
        assert max(abs(a-b) for a,b in zip(numbers[:2],connection['start'])) < 1e-8
        # Each editable arrow head ends in left-offset points around the target.
        x,y=connection['end'];expected=[x-6,y-5,x,y,x-6,y+5]
        assert max(abs(a-b) for a,b in zip(numbers[-6:],expected)) < 1e-8
    return result


def paint(page):
    page.evaluate('async()=>{await document.fonts.ready;await new Promise(r=>requestAnimationFrame(r));await new Promise(r=>requestAnimationFrame(r));}')


def audit_page(page):
    page.on('pageerror', lambda error: NORMAL_ERRORS.append(str(error)))
    page.on('console', lambda message: NORMAL_ERRORS.append(message.text) if message.type == 'error' else None)
    page.on('requestfailed', lambda request: NORMAL_FAILED_REQUESTS.append(request.url))
    page.on('response', lambda response: NORMAL_HTTP_ERRORS.append({'url': response.url, 'status': response.status}) if response.status >= 400 else None)


def open_case(context, origin, mode, slide='practice', query='v=1&dataset=default&threshold=50', *, audit=True):
    page = context.new_page()
    if audit:
        audit_page(page)
    page.goto(f'{origin}/examples/threshold-metrics/{mode}.html?{query}#{slide}')
    page.wait_for_function('!!window.ThresholdMetrics')
    page.evaluate('async()=>{await window.ThresholdMetrics.ready;}')
    page.wait_for_function("window.ThresholdMetrics.getState().status==='ready'")
    page.locator('#' + slide).scroll_into_view_if_needed()
    paint(page)
    return page


def fingerprint(page, slide):
    return page.evaluate("""id=>{const s=document.getElementById(id),r=s.getBoundingClientRect(),scale=r.width/1440;return [...s.querySelectorAll('h1,.subtitle,.teaching-panel,.panel-label,.panel-title,.sample-tile,table,[data-metric],math,.ref-takeaway,footer')].map(e=>{const b=e.getBoundingClientRect(),c=getComputedStyle(e);return {tag:e.tagName,id:e.id,className:e.getAttribute('class'),text:e.textContent.replace(/\\s+/g,' ').trim(),style:Object.fromEntries(['fontFamily','fontSize','fontWeight','lineHeight','letterSpacing','color','backgroundColor','padding','borderRadius'].map(k=>[k,c[k]])),rect:[(b.x-r.x)/scale,(b.y-r.y)/scale,b.width/scale,b.height/scale]};});}""", slide)


def threshold_scenarios(browser, origin, data):
    scenarios = []
    from reference_validation import actual_fonts
    for mode in ('scroll', 'slides'):
        context = browser.new_context(viewport={'width': 1440, 'height': 810})
        page = open_case(context, origin, mode)
        for dataset, dataset_info in data['datasets'].items():
            page.evaluate('(d)=>window.ThresholdMetrics.setDataset(d)', dataset)
            page.evaluate("window.__initialTiles=[...document.querySelectorAll('.sample-tile')];window.__initialTilePositions=window.__initialTiles.map(e=>{const b=e.getBoundingClientRect();return [b.x,b.y,b.width,b.height];});")
            samples, previous = dataset_info['samples'], None
            for threshold in range(101):
                page.evaluate('(t)=>window.ThresholdMetrics.setThreshold(t)', threshold)
                result = check_snapshot(page, samples, threshold)
                result.update(mode=mode, dataset=dataset)
                scenarios.append(result)
                assert page.evaluate("window.__initialTiles.every((e,i)=>e===document.querySelectorAll('.sample-tile')[i])")
                assert page.evaluate("window.__initialTiles.every((e,i)=>{const b=e.getBoundingClientRect(),a=[b.x,b.y,b.width,b.height];return a.every((v,j)=>Math.abs(v-window.__initialTilePositions[i][j])<.2);})")
                if previous:
                    c, p = result['counts'], previous['counts']
                    assert c['tp'] <= p['tp'] and c['tp'] + c['fp'] <= p['tp'] + p['fp']
                previous = result
            for threshold in (0, 100):
                page.evaluate('(t)=>window.ThresholdMetrics.setThreshold(t)', threshold)
                paint(page); geometry(page, 'practice'); matrix(page)
        context.close()
    assert len(scenarios) == 404
    return scenarios


def custom_scenarios(browser, origin):
    context = browser.new_context(viewport={'width': 1440, 'height': 810})
    page = open_case(context, origin, 'slides')
    fixtures = {
        'no_actual_negative': [{'id': f'P{i}', 'scoreUnits': n, 'truth': 1} for i, n in enumerate((0, 50, 99))],
        'no_actual_positive': [{'id': f'N{i}', 'scoreUnits': n, 'truth': 0} for i, n in enumerate((0, 50, 99))],
        'score_endpoints': [{'id': 'ZERO', 'scoreUnits': 0, 'truth': 1}, {'id': 'ONE', 'scoreUnits': 100, 'truth': 0}],
        'empty_evaluation': [],
    }
    results = []
    for label, samples in fixtures.items():
        page.evaluate('(s)=>window.ThresholdMetrics.loadSamples(s)', samples)
        for threshold in (0, 49, 50, 51, 100):
            page.evaluate('(t)=>window.ThresholdMetrics.setThreshold(t)', threshold)
            results.append({'fixture': label, **check_snapshot(page, samples, threshold)})
            paint(page);geometry(page, 'practice')
    invalid = [None, {}, [{'id': 'bad', 'scoreUnits': -1, 'truth': 1}],
               [{'id': 'bad', 'scoreUnits': 101, 'truth': 1}],
               [{'id': 'bad', 'scoreUnits': .5, 'truth': 1}],
               [{'id': 'bad', 'scoreUnits': 40, 'truth': 2}],
               [{'id': '', 'scoreUnits': 40, 'truth': 1}],
               [{'id': 'dup', 'scoreUnits': 40, 'truth': 1}, {'id': 'dup', 'scoreUnits': 80, 'truth': 0}]]
    for samples in invalid:
        page.evaluate("window.ThresholdMetrics.setDataset('default')")
        page.evaluate('(s)=>window.ThresholdMetrics.loadSamples(s)', samples)
        result = page.evaluate(SNAPSHOT)
        assert result['state']['status'] == 'error' and result['state']['counts'] is None and result['state']['metrics'] is None
        assert not result['tiles'] and set(result['counts'].values()) == {'—'}
        assert all(m['value'] == '—' for m in result['metrics'].values())
        assert page.locator('#threshold').is_disabled()
        assert page.locator('.current-fraction:visible').count()==0
    page.evaluate("window.ThresholdMetrics.setDataset('default')")
    assert page.evaluate("window.ThresholdMetrics.getState().status") == 'ready'
    clone = page.evaluate("()=>{const s=window.ThresholdMetrics.getState(),n=s.samples[0].scoreUnits;s.samples[0].scoreUnits=999;s.counts.tp=999;const t=window.ThresholdMetrics.getState();return {sampleUnchanged:t.samples[0].scoreUnits===n,countUnchanged:t.counts.tp!==999};}")
    assert all(clone.values())
    context.close()
    return {'valid_custom_states': results, 'invalid_fixtures': len(invalid), 'error_clears_prior_success': True,
            'recovery_with_valid_dataset': True, 'getState_deep_copy': clone}


def interaction_scenarios(browser, origin, data):
    context = browser.new_context(viewport={'width': 1440, 'height': 810})
    page = open_case(context, origin, 'slides')
    slider = page.locator('#threshold')
    assert slider.get_attribute('type') == 'range' and slider.get_attribute('aria-valuetext')
    assert page.get_by_role('slider').count() == 1
    assert page.get_by_role('slider',name='임계값').count()==1
    assert page.get_by_role('combobox',name='데이터셋').count()==1
    assert page.locator('#evaluation-status[role=status][aria-live=polite]').count()==1
    slider.focus();slider.press('Home');check_snapshot(page, data['datasets']['default']['samples'], 0)
    slider.press('End');check_snapshot(page, data['datasets']['default']['samples'], 100)
    slider.press('ArrowLeft');check_snapshot(page, data['datasets']['default']['samples'], 99)
    assert urlparse(page.url).fragment == 'practice'
    slider_box = slider.bounding_box();page.mouse.click(slider_box['x'] + slider_box['width'] / 4, slider_box['y'] + slider_box['height'] / 2)
    pointer_value = int(slider.input_value());assert 15 <= pointer_value <= 35
    check_snapshot(page, data['datasets']['default']['samples'], pointer_value)
    page.evaluate("window.ThresholdMetrics.setDataset('shifted');window.ThresholdMetrics.setThreshold(51)")
    before = check_snapshot(page, data['datasets']['shifted']['samples'], 51)
    page.reload();page.evaluate('async()=>await window.ThresholdMetrics.ready');check_snapshot(page, data['datasets']['shifted']['samples'], 51)
    page.get_by_role('link', name='Scroll', exact=True).click()
    page.wait_for_function('!!window.ThresholdMetrics');page.evaluate('async()=>await window.ThresholdMetrics.ready')
    check_snapshot(page, data['datasets']['shifted']['samples'], 51)
    assert urlparse(page.url).fragment == 'practice'
    page.get_by_role('link', name='Slide', exact=True).click()
    page.wait_for_function('!!window.ThresholdMetrics');page.evaluate('async()=>await window.ThresholdMetrics.ready')
    check_snapshot(page, data['datasets']['shifted']['samples'], 51)
    page.locator('body').click(position={'x': 5, 'y': 5});page.keyboard.press('Home');paint(page)
    assert urlparse(page.url).fragment == 'concept'
    page.keyboard.press('PageDown');paint(page);assert urlparse(page.url).fragment == 'practice'
    page.get_by_role('link', name='Scroll', exact=True).click();page.wait_for_function('!!window.ThresholdMetrics');page.evaluate('async()=>await window.ThresholdMetrics.ready')
    page.evaluate('window.scrollTo(0,document.documentElement.scrollHeight)');page.wait_for_timeout(150)
    assert urlparse(page.url).fragment == 'practice'
    assert page.locator('[aria-current]').count() >= 1
    page.close()
    invalid_urls = ('v=2&dataset=default&threshold=50', 'v=1&dataset=missing&threshold=50',
                    'v=1&dataset=default&threshold=0.50', 'v=1&dataset=default&threshold=-1',
                    'v=1&dataset=default&threshold=101', 'v=1&dataset=default&threshold=NaN')
    url_results = []
    for query in invalid_urls:
        page = open_case(context, origin, 'slides', 'concept', query)
        state = page.evaluate('window.ThresholdMetrics.getState()')
        assert state['status'] == 'ready' and state['thresholdUnits'] == 50 and state['dataset'] == 'default'
        qs = parse_qs(urlparse(page.url).query);assert qs['v'] == ['1'] and qs['dataset'] == ['default'] and qs['threshold'] == ['50']
        url_results.append({'input': query, 'canonical_url': page.url.split('/threshold-metrics/')[-1]});page.close()
    page=context.new_page();audit_page(page)
    page.goto(f'{origin}/examples/threshold-metrics/slides.html?v=1&dataset=default&threshold=50#unknown')
    page.wait_for_function('!!window.ThresholdMetrics');page.evaluate('async()=>await window.ThresholdMetrics.ready')
    assert urlparse(page.url).fragment=='concept'
    assert page.locator('#url-notice').is_visible()
    page.close()
    context.close()
    return {'native_keyboard_home_end_arrow': True, 'pointer_threshold': pointer_value,
            'mode_round_trip_and_reload': before, 'navigation_keys_leave_native_controls_alone': True,
            'scroll_final_section_sync': True, 'invalid_url_cases': url_results,'invalid_hash_normalized_with_notice':True}


def exceptional_scenarios(browser, origin):
    context = browser.new_context(viewport={'width': 1280, 'height': 720}, reduced_motion='reduce')
    page = open_case(context, origin, 'slides')
    page.evaluate('window.ThresholdMetrics.setThreshold(51)');paint(page)
    assert page.evaluate("document.querySelector('#practice').getAnimations({subtree:true}).length") == 0
    geometry(page, 'practice');context.close()
    fallback = browser.new_context(viewport={'width': 1280, 'height': 720})
    fallback.route('**/*.woff2', lambda route: route.fulfill(status=404, body='intentional font failure'))
    page = open_case(fallback, origin, 'slides', audit=False);geometry(page, 'practice');matrix(page)
    fallback.close()
    failure = browser.new_context(viewport={'width': 1280, 'height': 720})
    failure.route('**/threshold-metrics/data.json', lambda route: route.fulfill(status=503, body='intentional data failure'))
    page = failure.new_page();page.goto(f'{origin}/examples/threshold-metrics/slides.html#practice')
    page.wait_for_function("window.ThresholdMetrics?.getState().status==='error'")
    assert page.locator('#threshold').is_disabled()
    assert all(page.locator('[data-metric="'+key+'"] .metric-value').inner_text().strip() == '—' for key in METRICS)
    alerts=page.locator('[role=alert]').all_text_contents();assert any(t.strip() for t in alerts)
    failure.close()
    content_failure=browser.new_context(viewport={'width':1280,'height':720})
    content_failure.route('**/threshold-metrics/content.html',lambda route:route.fulfill(status=503,body='intentional content failure'))
    page=content_failure.new_page();page.goto(f'{origin}/examples/threshold-metrics/slides.html')
    page.wait_for_function("window.ThresholdMetrics?.getState().status==='error'")
    assert page.get_by_role('button',name='다시 불러오기',exact=True).is_visible()
    assert '불러오지 못' in page.locator('#lesson').inner_text()
    content_failure.close()
    script_failure=browser.new_context(viewport={'width':1280,'height':720})
    script_failure.route('**/threshold-metrics/app.js',lambda route:route.fulfill(status=503,body='intentional script failure'))
    page=script_failure.new_page();page.goto(f'{origin}/examples/threshold-metrics/slides.html')
    page.wait_for_function("document.body.dataset.ready==='error'")
    assert page.get_by_role('button',name='다시 불러오기',exact=True).is_visible()
    assert '스크립트' in page.locator('#lesson').inner_text()
    assert page.locator('[data-metric]').count()==0
    script_failure.close()
    nojs=browser.new_context(viewport={'width':1280,'height':720},java_script_enabled=False)
    page=nojs.new_page();page.goto(f'{origin}/examples/threshold-metrics/slides.html')
    assert page.locator('noscript').inner_text().strip();nojs.close()
    return {'reduced_motion': True, 'font_failure_layout_separate_from_normal_font_success': True,
            'data_load_failure_clears_success_and_disables_control': True,'content_load_failure_and_retry':True,
            'app_script_load_failure_and_retry':True,'no_javascript_notice': True,
            'exception_viewport':[1280,720],'exception_mode':'slides',
            'screen_reader_listening': 'not_performed'}


def contact_sheet(screens):
    from PIL import Image, ImageDraw
    canvas = Image.new('RGB', (1280, 8 * 395), 'white');draw = ImageDraw.Draw(canvas)
    for index, path in enumerate(screens):
        image = Image.open(path).convert('RGB');image.thumbnail((632, 365))
        x, y = index % 2 * 640, index // 2 * 395
        draw.text((x+8, y+5), path.stem, fill='black');canvas.paste(image, (x+4,y+25))
    target=CASE/'review/contact.jpg';canvas.save(target,quality=85);return target


def main():
    parser=ArgumentParser();parser.add_argument('--static',action='store_true');args=parser.parse_args()
    evidence=CASE/'previews';evidence.mkdir(parents=True,exist_ok=True)
    report_path=evidence/('static-validation.json' if args.static else 'validation.json')
    report={'status':'running','baseline_commit':BASELINE,'created_utc':datetime.now(timezone.utc).isoformat(),
            'screen_cases':[],'threshold_scenarios':[],'screen_cases_are_not_scenario_counts':True}
    def save():report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    save()
    try:
        report['protected_sources']=protected_sources();data=read_data()
        report['independent_oracle']='Python integer truth table, exact Fraction, decimal half-up at display only'
        report['node_crosscheck']=node_crosscheck(data)
        report['static_threshold_checks']=202
        for dataset in data['datasets'].values():
            previous=None
            for threshold in range(101):
                expected=oracle(dataset['samples'],threshold)
                if previous:assert expected['counts']['tp']<=previous['counts']['tp'] and expected['counts']['tp']+expected['counts']['fp']<=previous['counts']['tp']+previous['counts']['fp']
                previous=expected
        report['precision_monotonicity_assumed']=False
        report['precision_counterexample']={'threshold_50':oracle(data['datasets']['default']['samples'],50)['display']['precision'],'threshold_51':oracle(data['datasets']['default']['samples'],51)['display']['precision']}
        if args.static:
            report.update(status='static_passed',browser_validation='not_performed');save();print('PASS threshold static oracle / 202 states / protected originals');return
        from playwright.sync_api import sync_playwright
        from reference_validation import actual_fonts,browser_options
        class Quiet(SimpleHTTPRequestHandler):
            def log_message(self,*_):pass
            def do_GET(self):
                if self.path=='/favicon.ico':self.send_response(204);self.end_headers();return
                super().do_GET()
        server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start();origin=f'http://127.0.0.1:{server.server_port}'
        NORMAL_ERRORS.clear();NORMAL_FAILED_REQUESTS.clear();NORMAL_HTTP_ERRORS.clear()
        screens=[];fingerprints={}
        try:
            with sync_playwright() as p:
                browser=p.chromium.launch(**browser_options());report['chromium']=browser.version
                for size in SIZES:
                    for mode in ('scroll','slides'):
                        context=browser.new_context(viewport=dict(zip(('width','height'),size)))
                        for slide in ('concept','practice'):
                            page=open_case(context,origin,mode,slide)
                            result={'viewport':list(size),'mode':mode,'slide':slide,'geometry':geometry(page,slide)}
                            fonts=actual_fonts(page,'#'+slide+' *',math_family='STIX Two Math')
                            assert not fonts['fallback'] and not fonts['unpainted'] and not fonts['bad_spacing'],fonts
                            result['fonts']=fonts
                            ui_fonts=actual_fonts(page,'.viewer-bar *,.slide-controls *',math_family='STIX Two Math')
                            assert not ui_fonts['fallback'] and not ui_fonts['unpainted'] and not ui_fonts['bad_spacing'],ui_fonts
                            result['viewer_fonts']=ui_fonts
                            duplicate_ids=page.evaluate("()=>{const ids=[...document.querySelectorAll('[id]')].map(e=>e.id);return ids.filter((id,i)=>ids.indexOf(id)!==i);}")
                            assert not duplicate_ids,duplicate_ids
                            if slide=='practice':result.update(default=check_snapshot(page,data['datasets']['default']['samples'],50),matrix=matrix(page),formulas=formula_semantics(page))
                            else:result['connectors']=connectors(page)
                            if size==(1440,810):fingerprints[(mode,slide)]=fingerprint(page,slide)
                            folder=CASE/'review/screens';folder.mkdir(parents=True,exist_ok=True);shot=folder/f'{mode}-{slide}-{size[0]}x{size[1]}.png'
                            page.screenshot(path=str(shot));screens.append(shot)
                            if size==(1440,810):page.screenshot(path=str(evidence/f'{mode}-{slide}.png'))
                            report['screen_cases'].append(result);save();page.close()
                        context.close()
                assert len(report['screen_cases'])==16
                mode_comparison=[]
                for slide in ('concept','practice'):
                    left,right=(fingerprints[(mode,slide)] for mode in ('scroll','slides'))
                    assert len(left)==len(right)
                    maximum=0
                    for a,b in zip(left,right):
                        assert all(a[k]==b[k] for k in ('tag','id','className','text','style')),(slide,a,b)
                        maximum=max(maximum,max(abs(x-y) for x,y in zip(a['rect'],b['rect'])))
                    assert maximum<1,(slide,maximum)
                    mode_comparison.append({'slide':slide,'elements':len(left),'max_normalized_box_error':maximum,'styles_and_content_equal':True})
                report['mode_comparison']=mode_comparison
                report['threshold_scenarios']=threshold_scenarios(browser,origin,data);save()
                report['custom_data_scenarios']=custom_scenarios(browser,origin);save()
                report['interaction_scenarios']=interaction_scenarios(browser,origin,data);save()
                report['exception_scenarios']=exceptional_scenarios(browser,origin);save();browser.close()
        finally:server.shutdown();server.server_close()
        assert not NORMAL_ERRORS and not NORMAL_FAILED_REQUESTS and not NORMAL_HTTP_ERRORS,(NORMAL_ERRORS,NORMAL_FAILED_REQUESTS,NORMAL_HTTP_ERRORS)
        report.update(page_errors=NORMAL_ERRORS,failed_requests=NORMAL_FAILED_REQUESTS,http_errors=NORMAL_HTTP_ERRORS)
        contact=contact_sheet(screens)
        sources=[*CASE.glob('*.html'),*CASE.glob('*.css'),*CASE.glob('*.js'),CASE/'data.json',CASE/'DESIGN.md',Path(__file__).resolve(),ROOT/'.github/workflows/validate-threshold-metrics.yml']
        report['source_sha256']={str(path.relative_to(ROOT)):sha(path) for path in sources}
        report['preview_sha256']={str(path.relative_to(ROOT)):sha(path) for path in [*evidence.glob('*.png'),contact]}
        report['full_resolution_screenshot_count']=len(screens)
        report['unverified']=['actual model training/production performance','reader comprehension study','screen reader listening','mobile/tablet','other pattern new-topic reuse']
        report['status']='passed';save();print('PASS threshold Chromium: 16 screens / 404 threshold states / independent exact metrics / modes, faults and protected sources')
    except Exception:
        report.update(status='failed',error=traceback.format_exc());save();raise


if __name__=='__main__':main()
