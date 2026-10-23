"""Shared browser checks for the final eight HTML references."""

GEOMETRY = """() => {
    const slide = document.querySelector('.slide');
    const rect = e => {const r=e.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height,right:r.right,bottom:r.bottom}};
    const s=rect(slide), footer=rect(slide.querySelector('.footer'));
    const visible=[...slide.querySelectorAll('*')].filter(e=>!e.closest('.sr-only') && e.getBoundingClientRect().width && e.getBoundingClientRect().height);
    const outside=visible.filter(e=>{const r=rect(e);return r.x<s.x-1 || r.right>s.right+1 || r.y<s.y-1 || r.bottom>s.bottom+1}).map(e=>e.className);
    const containers=[...slide.querySelectorAll('.content,.ref-grid,.ref-card,.concept-panel,.compare-card,.node,.arch-node,.executive-kpi,.exec-metric-group,.exec-metric-bars,.exec-impact,.exec-chart,.exec-comparison,.exec-actions')];
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

def check_executive(page, width):
    """Check KPI values, normalized heights and shared grouped-chart axes."""
    result = page.evaluate("""() => {
      const box = el => {const r=el.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height,right:r.right,bottom:r.bottom}};
      const impact=document.querySelector('.exec-impact');
      const action=document.querySelector('.exec-action-panel');
      const groups=[...document.querySelectorAll('.exec-metric-group')];
      return {
        obsolete:document.querySelectorAll('.executive-kpis,.executive-kpi,.exec-track,.exec-bar').length,
        title:document.querySelector('h1').textContent,
        subtitle:document.querySelector('.subtitle').textContent,
        noteCount:document.querySelectorAll('.exec-scenario-note').length,
        footer:[...document.querySelectorAll('.footer span')].map(e=>e.textContent),
        actions:[...document.querySelectorAll('.exec-action')].map(e=>({
          number:e.querySelector('strong').textContent,
          title:e.querySelector('b').textContent,
          detail:e.querySelector('span').lastChild.textContent
        })),
        impact:box(impact),action:box(action),
        impactBackground:getComputedStyle(impact).backgroundColor,
        impactBorder:getComputedStyle(impact).borderStyle,
        ticks:[...document.querySelectorAll('.exec-y-axis span')].map(e=>({
          label:e.textContent,ratio:Number(e.style.getPropertyValue('--tick')),box:box(e)
        })),
        groups:groups.map(g=>({
          box:box(g),title:g.querySelector('h3').textContent,
          titleBox:box(g.querySelector('h3')),
          valueBoxes:[...g.querySelectorAll('.exec-value')].map(box),
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
    assert result['impactBorder']!='none' and result['impactBackground']=='rgb(255, 255, 255)', (width, result)
    assert [(t['label'],t['ratio']) for t in result['ticks']]==[('100%',1),('50%',.5),('0',0)], (width, result)
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
        assert group['titleBox']['y']>base['bottom'], (width, 'category not below x-axis', group)
        assert abs(group['titleBox']['x']+group['titleBox']['width']/2-(base['x']+new['right'])/2)<1, (width, 'category not centered on pair', group)
        for value,bar in zip(group['valueBoxes'],group['bars']):
            assert value['bottom']<=bar['y'], (width, 'value overlaps bar', group)
        assert group['valueBoxes'][0]['right']<group['valueBoxes'][1]['x'], (width, 'value labels overlap', group)
        for tick in result['ticks']:
            tick_y=tick['box']['y']+tick['box']['height']/2
            assert abs(tick_y-(base['bottom']-base['height']*tick['ratio']))<1, (width, 'axis scale mismatch', group)
        if previous:
            assert group['box']['x']>previous['box']['right'], (width, 'groups not ordered across x-axis', result)
            assert abs(base['bottom']-previous['bars'][0]['bottom'])<1, (width, 'no common baseline', result)
            assert abs(base['height']-previous['bars'][0]['height'])<1, (width, 'unequal normalized scale', result)
        previous=group
    assert result['title']=='점검 효율 개선안 요약'
    assert result['subtitle']=='수동 점검 부담 감소를 위한 파일럿 검토 · 효율성과 미검출 위험의 동시 평가'
    assert result['noteCount'] == 0, (
        width, 'obsolete hypothetical-data footnote still present', result
    )
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

# Canonical preview sizes and rendering requirements.
SIZES = ((1600,950),(1440,810),(1366,768),(1280,720),(900,900),(390,844))
NAMES = ('concept','process','comparison','step-by-step','interactive','architecture','experiment','executive-summary')


def browser_options():
    import os,shutil
    executable=os.environ.get('CHROMIUM_EXECUTABLE') or shutil.which('chromium') or shutil.which('chromium-browser')
    return dict(headless=True,**({'executable_path':executable} if executable else {}))


def actual_fonts(page, selector='.slide *'):
    """Check CSS tracking AND the fonts Chromium actually used for each text node."""
    # A multi-page viewer keeps hidden slides in the DOM. Clear the previous
    # audit's IDs so CDP cannot accidentally resolve a hidden element instead.
    entries=page.evaluate('''selector => {
      document.querySelectorAll('[data-font-audit]').forEach(e=>e.removeAttribute('data-font-audit'));
      return [...document.querySelectorAll(selector)].filter(e=>!e.closest('.sr-only')&&e.getBoundingClientRect().width&&e.getBoundingClientRect().height&&[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())).map((e,i)=>{e.dataset.fontAudit=String(i);const s=getComputedStyle(e);return {index:i,tag:e.tagName,className:typeof e.className==='string'?e.className:e.className.baseVal,text:[...e.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent).join('').trim(),spacing:s.letterSpacing,requested:s.fontFamily}});
    }''', selector)
    cdp=page.context.new_cdp_session(page);cdp.send('DOM.enable');cdp.send('CSS.enable')
    root=cdp.send('DOM.getDocument',{'depth':-1})['root']['nodeId'];families={};fallback=[];unpainted=[]
    try:
        for entry in entries:
            node=cdp.send('DOM.querySelector',{'nodeId':root,'selector':f'[data-font-audit="{entry["index"]}"]'})['nodeId']
            fonts=cdp.send('CSS.getPlatformFontsForNode',{'nodeId':node})['fonts']
            entry['actual']=fonts
            if not fonts:unpainted.append(entry)
            for f in fonts:
                families[f['familyName']]=families.get(f['familyName'],0)+f['glyphCount']
                if f['familyName']!='Pretendard Variable' or not f['isCustomFont']:fallback.append(entry)
    finally:cdp.detach()
    spacing=[e for e in entries if abs(float(e['spacing'].removesuffix('px'))+4/3)>.02]
    loaded=page.evaluate('''async()=>{const weights=[400,600,700,800];const counts=await Promise.all(weights.map(w=>document.fonts.load(`${w} 22px "Pretendard Variable"`,'한글 ABC 0123')));await document.fonts.ready;return {counts:counts.map(f=>f.length),faces:[...document.fonts].filter(f=>f.family.replace(/["']/g,'')==='Pretendard Variable'&&f.status==='loaded').map(f=>({family:f.family,weight:f.weight,status:f.status}))}}''')
    return {'elements':len(entries),'families':families,'fallback':fallback,'unpainted':unpainted,'bad_spacing':spacing,'loaded':loaded}

EXPERIMENT_GEOMETRY="""() => {
 const slide=document.querySelector('.slide');
 const box=e=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y,right:r.right,bottom:r.bottom,width:r.width,height:r.height}};
 const cx=e=>{const r=box(e);return r.x+r.width/2},cy=e=>{const r=box(e);return r.y+r.height/2};
 const table=slide.querySelector('table');
 const cell=code=>table.querySelector(`[data-code="${code}"]`);
 const codes=['FP','TP','TN','FN'];
 const centering=codes.map(code=>{
  const e=cell(code),label=e.querySelector('.cm-code'),count=e.querySelector('.cm-count');
  const ranges=[label,count].map(el=>{const r=document.createRange();r.selectNodeContents(el);return r.getBoundingClientRect()});
  return {code,xErrors:ranges.map(r=>Math.abs(r.x+r.width/2-cx(e))),
   yError:Math.abs((box(label).y+box(count).bottom)/2-cy(e)),box:box(e)};
 });
 const labels={columns:[...table.querySelectorAll('.column-label')].map(e=>e.textContent),rows:[...table.querySelectorAll('tbody th[scope="row"]')].map(e=>e.textContent)};
 const axisErrors={gt:Math.abs(cx(table.querySelector('.gt-axis'))-(cx(cell('FP'))+cx(cell('TP')))/2),
 prediction:Math.abs(cy(table.querySelector('.pred-axis'))-(cy(cell('FP'))+cy(cell('TN')))/2),
 columns:[Math.abs(cx(document.getElementById('gt-normal'))-cx(cell('FP'))),Math.abs(cx(document.getElementById('gt-anomaly'))-cx(cell('TP')))],
 rows:[Math.abs(cy(document.getElementById('pred-anomaly'))-cy(cell('FP'))),Math.abs(cy(document.getElementById('pred-normal'))-cy(cell('TN')))]};
 const textBounds=e=>{
  const walker=document.createTreeWalker(e,NodeFilter.SHOW_TEXT),rs=[];
  while(walker.nextNode()){if(!walker.currentNode.textContent.trim())continue;const r=document.createRange();r.selectNodeContents(walker.currentNode);rs.push(r.getBoundingClientRect());}
  return {left:Math.min(...rs.map(r=>r.left)),right:Math.max(...rs.map(r=>r.right))};
 };
 const line=box(slide.querySelector('.prediction-divider'));
 const titleRight=textBounds(table.querySelector('.pred-axis-label')).right;
 const labelsLeft=Math.min(...[...table.querySelectorAll('tbody th[scope="row"]')].map(e=>textBounds(e).left));
 const dividerGaps={left:line.x+line.width/2-titleRight,right:labelsLeft-line.x-line.width/2};
 const all=[...slide.querySelectorAll('*')].filter(e=>!e.classList.contains('sr-only')&&e.tagName!=='TR');
 const overflow=all.filter(e=>e.clientWidth>0&&(e.scrollWidth>e.clientWidth+2||e.scrollHeight>e.clientHeight+2)).map(e=>({name:e.className||e.tagName,client:[e.clientWidth,e.clientHeight],scroll:[e.scrollWidth,e.scrollHeight]}));
 const text=all.filter(e=>[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()));
 const badTypography=text.filter(e=>{const s=getComputedStyle(e);return Math.abs(parseFloat(s.letterSpacing)+4/3)>.02||!s.fontFamily.startsWith('"Pretendard Variable"')}).map(e=>e.className||e.tagName);
 const cards=[...slide.querySelectorAll('.experiment-card')];
 const metrics=[...slide.querySelectorAll('.metric')].map(e=>({name:e.dataset.metric,box:box(e),value:e.querySelector('.metric-value').textContent,formula:e.querySelector('.metric-equation').getAttribute('aria-label'),fraction:[...e.querySelectorAll('.fraction > span')].map(e=>e.textContent),calculation:e.querySelector('.metric-calculation').textContent}));
 return {slide:box(slide),content:box(slide.querySelector('.content')),footer:box(slide.querySelector('footer')),
 cards:cards.map(box),table:box(table),labels,axisErrors,centering,metrics,overflow,badTypography,
 pageWidth:document.documentElement.scrollWidth,
 dividerGaps,
 counts:[...table.querySelectorAll('[data-code]')].map(e=>({code:e.dataset.code,count:Number(e.querySelector('.cm-count').textContent),headers:e.getAttribute('headers'),background:getComputedStyle(e).backgroundColor})),
 dividers:{gt:getComputedStyle(table.querySelector('.gt-axis')).borderBottomWidth,prediction:getComputedStyle(slide.querySelector('.prediction-divider')).borderRightWidth},
 fontsLoaded:[...document.fonts].filter(f=>f.family.replaceAll('"','').replaceAll("'",'')==='Pretendard Variable'&&f.status==='loaded').length};
}"""

CARD_PADDING = '''() => [...document.querySelectorAll('.ref-card,.concept-panel,.compare-card,.calc-panel,.experiment-card')].map(card=>{
 const r=card.getBoundingClientRect(),s=getComputedStyle(card),scale=r.width/parseFloat(s.width);
 const left=r.left+(parseFloat(s.paddingLeft)+parseFloat(s.borderLeftWidth))*scale,right=r.right-(parseFloat(s.paddingRight)+parseFloat(s.borderRightWidth))*scale;
 const top=r.top+(parseFloat(s.paddingTop)+parseFloat(s.borderTopWidth))*scale,bottom=r.bottom-(parseFloat(s.paddingBottom)+parseFloat(s.borderBottomWidth))*scale;
 const escaped=[...card.children].filter(e=>!e.closest('.sr-only')&&e.getBoundingClientRect().width&&e.getBoundingClientRect().height).filter(e=>{const b=e.getBoundingClientRect();return b.left<left-1||b.right>right+1||b.top<top-1||b.bottom>bottom+1}).map(e=>typeof e.className==='string'?e.className:e.tagName);
 return {card:card.className,escaped};
})'''
