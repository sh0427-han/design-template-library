"""Validate and render the FINAL eight references with local Pretendard.
Run: python scripts/validate_references.py
Optional: --templates process comparison --evidence-dir /tmp/reference-review
No CDN interception, TLS bypass, learned-model claims, or static-image substitution.
"""
from argparse import ArgumentParser
from datetime import datetime,timezone
from fractions import Fraction
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
import hashlib,json,math,struct,threading
from playwright.sync_api import sync_playwright
from reference_validation import NAMES,SIZES,GEOMETRY,CARD_PADDING,EXPERIMENT_GEOMETRY,actual_fonts,browser_options,check_executive
from process_validation import check_process,check_process_robustness
ROOT=Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*_):pass
    def do_GET(self):
        if self.path=='/favicon.ico':
            self.send_response(204);self.end_headers();return
        super().do_GET()

def check_concept(page):
    """Verify real RGB planes, ROI source, four-stage flow and pixel numbers."""
    r=page.evaluate('''() => {
        const im=document.querySelector('#concept-image');
        const cv=document.createElement('canvas');
        cv.width=cv.height=80;
        const ctx=cv.getContext('2d',{willReadFrequently:true});
        ctx.imageSmoothingEnabled=true;
        ctx.imageSmoothingQuality='high';
        ctx.drawImage(im,0,0,80,80);
        const full=ctx.getImageData(0,0,80,80).data;
        const rgba=ctx.getImageData(52,38,4,4).data;
        const colors=Array.from({length:16},(_,i)=>[...rgba.slice(i*4,i*4+3)]);
        const box=e=>{const b=e.getBoundingClientRect();return {
            x:b.x,y:b.y,right:b.right,bottom:b.bottom,width:b.width,
            height:b.height,cx:b.x+b.width/2,cy:b.y+b.height/2}};
        const selected=document.querySelector('.pixel-block .selected');
        const cells=[...document.querySelectorAll('.pixel-plane-rgb .pixel-block > span')];
        const cropPlanes=[...document.querySelectorAll('.pixel-stack > .pixel-plane')].map(node=>{
            const grid=node.querySelector('.pixel-block,.pixel-channel-grid');
            const planeCells=[...grid.querySelectorAll(':scope > span')];
            return {
                name:node.dataset.cropPlane,box:box(node),grid:box(grid),
                cells:planeCells.map(e=>e.style.backgroundColor),
                rawValues:planeCells.map(e=>e.dataset.rawValue||null),
                selected:planeCells.filter(e=>e.classList.contains('selected')).length
            };
        });
        const planes=[...document.querySelectorAll('.channel-canvas')].map(canvas=>{
            const c=canvas.getContext('2d',{willReadFrequently:true});
            const data=c.getImageData(0,0,80,80).data;
            const channel={R:0,G:1,B:2}[canvas.dataset.channel];
            let errors=0;
            for(let i=0;i<6400;i++){
                for(let k=0;k<3;k++){
                    if(data[i*4+k] !== (k===channel?full[i*4+k]:0)) errors++;
                }
                if(data[i*4+3]!==255)errors++;
            }
            return {name:canvas.dataset.channel,width:canvas.width,
                height:canvas.height,errors,box:box(canvas),
                layer:box(canvas.closest('.channel-layer'))};
        });
        const roi=document.querySelector('.matrix-roi');
        const rbox=box(roi),cbox=box(document.querySelector('.channel-layer[data-plane="R"] canvas'));
        const pixelGrid=box(document.querySelector('.pixel-block'));
        const heightText=document.querySelector('.dimension-text-h');
        const widthText=document.querySelector('.dimension-text-w');
        const flow=document.querySelector('.concept-flow');
        const rgbBox=box(document.querySelector('.selected-color'));
        return {
            state:document.querySelector('.concept-slide').dataset.sampled,
            imageComplete:im.complete && im.naturalWidth>0,
            planeROIs:document.querySelectorAll('.matrix-roi').length,
            photoROIs:document.querySelectorAll('.photo-roi').length,
            matrixParent:roi.closest('.channel-layer').dataset.plane,
            matrixROI:{
                left:(rbox.x-cbox.x)/cbox.width,
                top:(rbox.y-cbox.y)/cbox.height,
                width:rbox.width/cbox.width,height:rbox.height/cbox.height
            },
            colors,painted:cells.map(e=>e.style.backgroundColor),cropPlanes,
            cropStack:box(document.querySelector('.pixel-stack')),
            cropBadges:[...document.querySelectorAll('.pixel-stack .plane-badge')]
                .map(e=>({label:e.textContent.trim(),box:box(e),
                    background:getComputedStyle(e).backgroundColor,
                    display:getComputedStyle(e).display,
                    font:getComputedStyle(e).fontSize,
                    plane:e.closest('.pixel-plane').dataset.cropPlane})),
            cropOutlines:['G','B'].map(channel=>{
                const node=document.querySelector('.pixel-plane-'+channel.toLowerCase());
                return {name:channel,base:getComputedStyle(node.querySelector('.pixel-channel-grid')).outlineColor,
                    badge:getComputedStyle(node.querySelector('.plane-badge')).backgroundColor};
            }),
            selectedIndex:cells.indexOf(selected),
            declaredIndex:Number(selected.dataset.selectedIndex),
            selectedTitle:selected.title,
            channels:[...document.querySelectorAll('.channel-value .number')]
                .map(e=>Number(e.textContent)),
            numberWidths:[...document.querySelectorAll('.channel-value .number')]
                .map(e=>({scroll:e.scrollWidth,client:e.clientWidth})),
            bars:[...document.querySelectorAll('.channel-value .bar')]
                .map(e=>parseFloat(e.style.width)),
            rgb:document.querySelector('#selected-rgb').textContent,
            hex:document.querySelector('#selected-hex').textContent,
            swatch:getComputedStyle(document.querySelector('.selected-color .swatch')).backgroundColor,
            selectedColor:getComputedStyle(selected).backgroundColor,
            selectedStyle:{
                border:getComputedStyle(selected).borderColor,
                outline:getComputedStyle(selected).outlineStyle,
                shadow:getComputedStyle(selected).boxShadow,
                zIndex:getComputedStyle(selected).zIndex
            },
            planes,
            axes:[...document.querySelectorAll('.stack-axis')].map(e=>e.textContent.trim()),
            cAxis:box(document.querySelector('.stack-axis-c')),
            hText:box(heightText),wText:box(widthText),pixelGrid,
            cropCLabelCount:document.querySelectorAll('.pixel-stack .pixel-channel-indicator').length,
            dimensionLines:document.querySelectorAll('.pixel-stack .dimension-width,.pixel-stack .dimension-height').length,
            hBorder:getComputedStyle(heightText).borderRightWidth,
            wBorder:getComputedStyle(widthText).borderBottomWidth,
            visualCenters:(()=>{
                const figureBox=selector=>box(document.querySelector(selector));
                const cropParts=[heightText,widthText,
                    document.querySelector('.pixel-plane-rgb .pixel-block'),
                    document.querySelector('.pixel-plane-g .pixel-channel-grid'),
                    document.querySelector('.pixel-plane-b .pixel-channel-grid')].map(box);
                const cropLeft=Math.min(...cropParts.map(x=>x.x));
                const cropRight=Math.max(...cropParts.map(x=>x.right));
                const centerOf=selector=>figureBox(selector).cx;
                return {
                    photo:centerOf('.photo-wrap')-centerOf('.image-frame'),
                    matrix:centerOf('.channel-stack')-centerOf('.matrix-frame'),
                    crop:(cropLeft+cropRight)/2-centerOf('.pixel-frame'),
                    detail:centerOf('.pixel-detail')-centerOf('.detail-frame')
                };
            })(),
            arrows:[...flow.querySelectorAll(':scope > .flow-link')].map(box),
            steps:[...flow.querySelectorAll(':scope > .concept-step')].map(box),
            figures:['.image-frame','.matrix-frame','.pixel-frame','.detail-frame']
                .map(s=>box(document.querySelector(s))),
            labels:[...flow.querySelectorAll('.concept-step-label')].map(e=>e.textContent.trim()),
            notes:[...flow.querySelectorAll('.concept-step-note')].map(e=>e.textContent.trim()),
            panelCount:document.querySelectorAll('.concept-panel').length,
            panel:box(document.querySelector('.concept-panel')),
            detailInside:document.querySelector('.rgb-step').closest('.concept-panel')===
                document.querySelector('.matrix-step').closest('.concept-panel'),
            rgbBox,summary:document.querySelector('.concept-flow-summary').textContent,
            cropChannels:{
                planeNames:[...document.querySelectorAll('.pixel-stack > .pixel-plane')]
                    .map(e=>e.dataset.cropPlane),
                box:box(document.querySelector('.pixel-stack')),
                frame:box(document.querySelector('.pixel-frame')),
                note:document.querySelector('.pixel-step .concept-step-note').textContent.trim()
            },
            merge:{
                copy:document.querySelector('.merge-copy').textContent.trim(),
                values:['merge-r','merge-g','merge-b'].map(id=>Number(document.getElementById(id).textContent)),
                swatch:getComputedStyle(document.querySelector('.merge-swatch')).backgroundColor,
                elementCount:document.querySelectorAll('.merge-channel').length,
                box:box(document.querySelector('.concept-flow-summary'))
            },
            footer:box(document.querySelector('.footer')),
            viewport:innerWidth
        };
    }''')
    assert r['state']=='true' and r['imageComplete']
    assert r['panelCount']==1 and r['detailInside']
    assert len(r['steps'])==4 and len(r['arrows'])==3
    assert r['labels']==[
        '입력 이미지','R · G · B 행렬 3장','일부 영역 확대','선택한 1픽셀']
    assert r['notes']==[
        '하나의 RGB 사진','같은 H×W, ROI 선택',
        '4×4×3 = 48개 값','한 위치 = RGB 3개 값']
    assert r['photoROIs']==0 and r['planeROIs']==1
    assert r['matrixParent']=='R'
    assert [(p['name'],p['width'],p['height'],p['errors']) for p in r['planes']]==[
        ('B',80,80,0),('G',80,80,0),('R',80,80,0)]
    assert r['planes'][0]['layer']['x']>r['planes'][1]['layer']['x']>r['planes'][2]['layer']['x']
    assert r['planes'][0]['layer']['y']<r['planes'][1]['layer']['y']<r['planes'][2]['layer']['y']
    assert all(abs(p['layer']['width']-r['planes'][0]['layer']['width'])<1 for p in r['planes'])
    assert all(abs(p['layer']['height']-r['planes'][0]['layer']['height'])<1 for p in r['planes'])
    for key,val in [('left',.65),('top',.475),('width',.05),('height',.05)]:
        assert abs(r['matrixROI'][key]-val)<.02,(r['viewport'],key,r['matrixROI'])
    assert r['axes']==['C = 3','H','W']
    assert r['cAxis']['bottom']<r['planes'][0]['layer']['y'],(r['viewport'],r['cAxis'])
    # getBoundingClientRect reports scaled coordinates; check border line endpoints,
    # not merely the midpoint of either dimension label.
    unscaled_grid=122 if r['viewport']<=520 else 130
    scale=r['pixelGrid']['width']/unscaled_grid
    tol=max(.75,1.5*scale)
    # No C=3 in the crop and no dimension guide lines.
    # Left three-channel stack must still retain its C=3.
    assert r['cropCLabelCount']==0 and r['dimensionLines']==0
    assert float(r['hBorder'].removesuffix('px'))==0
    assert float(r['wBorder'].removesuffix('px'))==0
    b_grid=r['cropPlanes'][0]['grid']
    assert abs(r['hText']['cy']-r['pixelGrid']['cy'])<=tol
    assert abs(r['wText']['cx']-b_grid['cx'])<=tol
    assert r['hText']['right']<=r['pixelGrid']['x']-6*scale
    assert r['wText']['y']>=max(p['grid']['bottom'] for p in r['cropPlanes'])+5*scale
    assert r['wText']['bottom']<=r['cropChannels']['box']['bottom']+2
    assert r['pixelGrid']['width']<=130*scale+.1
    assert all(abs(value)<3.1 for value in r['visualCenters'].values()),(
        r['viewport'],r['visualCenters'])
    # Explicit corner badges must be entirely visible, correctly labelled
    # and color-matched to their OWN panel outlines.
    badges=r['cropBadges']
    assert [(b['plane'],b['label']) for b in badges]==[
        ('B','B'),('G','G'),('RGB','R')],(r['viewport'],badges)
    assert r['cropOutlines']==[
        {'name':'G','base':'rgb(39, 148, 103)','badge':'rgb(39, 148, 103)'},
        {'name':'B','base':'rgb(66, 126, 197)','badge':'rgb(66, 126, 197)'}]
    for i,b in enumerate(badges):
        plane=r['cropPlanes'][i]['grid']
        assert b['display']=='grid' and float(b['font'].removesuffix('px'))>=9
        assert plane['right']-b['box']['right']>=0
        assert b['box']['x']>=plane['x'] and b['box']['y']>=plane['y']
        assert b['box']['bottom']<=plane['bottom']
    # Text labels must not touch the rear planes or each other.
    def overlaps(a,b):
        return (a['x']<b['right'] and a['right']>b['x']
                and a['y']<b['bottom'] and a['bottom']>b['y'])
    for label in [r['hText'],r['wText']]:
        assert not any(overlaps(label,p['grid']) for p in r['cropPlanes']),(
            r['viewport'],label,r['cropPlanes'])
    assert not overlaps(r['hText'],r['wText'])
    for badge in badges:
        assert not overlaps(badge['box'],r['wText'])
        assert not overlaps(badge['box'],r['hText'])
    assert not any(overlaps(a['box'],b['box'])
                   for i,a in enumerate(badges) for b in badges[i+1:])
    # Badge visibility: rear top-right tabs cannot be covered by front grids.
    assert all(not any(overlaps(badges[i]['box'],p['grid'])
                       for p in r['cropPlanes'][i+1:])
               for i in range(2))
    assert len(r['colors'])==16 and r['selectedIndex']==r['declaredIndex']==6
    assert r['painted']==['rgb('+', '.join(map(str,c))+')' for c in r['colors']]
    rgb=r['colors'][6]
    assert r['channels']==rgb
    assert page.locator('.pixel-plane-rgb').evaluate(
        "e=>getComputedStyle(e,'::after').content")=='none'
    assert r['cropChannels']['planeNames']==['B','G','RGB']
    crop=r['cropPlanes']
    assert [p['name'] for p in crop]==['B','G','RGB']
    assert all(len(p['cells'])==16 for p in crop)
    assert [p['selected'] for p in crop]==[0,0,1]
    assert crop[2]['cells']==r['painted']
    # Independent calculation of the JS display-only tint (Math.round).
    # Python round() uses ties-to-even; JS uses floor(x + 0.5) for x >= 0.
    def tint_channel(value,tint):
        level=.22+value/255*.78
        return tuple(math.floor(255+(v-255)*level+.5) for v in tint)
    def css_rgb(rgb):
        return 'rgb('+', '.join(map(str,rgb))+')'
    green_tint=(39,148,103)  # exact CSS G outline #279467
    blue_tint=(66,126,197)   # exact CSS B outline #427ec5
    assert crop[1]['cells']==[
        css_rgb(tint_channel(color[1],green_tint)) for color in r['colors']]
    assert crop[0]['cells']==[
        css_rgb(tint_channel(color[2],blue_tint)) for color in r['colors']]
    assert crop[1]['rawValues']==[str(c[1]) for c in r['colors']]
    assert crop[0]['rawValues']==[str(c[2]) for c in r['colors']]
    assert crop[2]['rawValues']==[None]*16
    assert all(tint_channel(a,t)[i]>=tint_channel(b,t)[i]
               for index,t in [(1,green_tint),(2,blue_tint)]
               for a,b in zip(sorted(c[index] for c in r['colors'])[:-1],
                              sorted(c[index] for c in r['colors'])[1:])
               for i in range(3))
    assert all(abs(p['grid']['width']-crop[2]['grid']['width'])<1
               and abs(p['grid']['height']-crop[2]['grid']['height'])<1
               for p in crop)
    assert crop[0]['box']['x']>crop[1]['box']['x']>crop[2]['box']['x']
    assert crop[0]['box']['y']<crop[1]['box']['y']<crop[2]['box']['y']
    # Compare relative layer offsets at the actual responsive scale.
    offset=(14 if r['viewport']<=520 else 17)*scale
    assert abs(crop[1]['box']['x']-crop[2]['box']['x']-offset)<1
    assert abs(crop[2]['box']['y']-crop[1]['box']['y']-offset)<1
    assert abs(crop[0]['box']['x']-crop[2]['box']['x']-2*offset)<1
    assert abs(crop[2]['box']['y']-crop[0]['box']['y']-2*offset)<1
    # Crop stack is the figure envelope; the deleted C label no longer sits above B.
    assert r['cropChannels']['box']['right']<=r['cropChannels']['frame']['right']+2
    assert all(p['box']['x']>=r['cropChannels']['frame']['x']-1
               and p['box']['right']<=r['cropChannels']['frame']['right']+1
               and p['box']['y']>=r['cropChannels']['frame']['y']-1
               and p['box']['bottom']<=r['cropChannels']['frame']['bottom']+1
               for p in crop)
    assert r['cropChannels']['note']=='4×4×3 = 48개 값'
    assert r['cropChannels']['frame']['y']<=r['cropChannels']['box']['y']
    assert r['cropChannels']['box']['bottom']<=r['cropChannels']['frame']['bottom']+1
    assert r['merge']['copy']=='같은 위치의 R/G/B 값을 조합하면'
    assert r['merge']['elementCount']==3 and r['merge']['values']==rgb
    assert r['selectedTitle']=='RGB ('+', '.join(map(str,rgb))+')'
    assert r['rgb']=='RGB ('+', '.join(map(str,rgb))+')'
    assert r['hex']=='#'+''.join(f'{v:02X}' for v in rgb)
    assert r['swatch']==r['selectedColor']==r['merge']['swatch']==(
        'rgb('+', '.join(map(str,rgb))+')')
    assert r['pixelGrid']['width']<150*scale
    assert r['rgbBox']['width']>=48*scale
    style=r['selectedStyle']
    assert style['border']=='rgb(255, 255, 255)' and style['outline']=='none'
    assert style['zIndex']=='8'
    assert 'rgb(255, 255, 255) 0px 0px 0px 2px' in style['shadow'],style
    assert 'rgb(18, 35, 63) 0px 0px 0px 5px' in style['shadow'],style
    assert all(abs(a-100*b/255)<.001 for a,b in zip(r['bars'],rgb))
    assert all(n['scroll']<=n['client']+1 for n in r['numberWidths'])
    assert 'H × W × 3' not in r['summary']
    assert '1픽셀의 색' in r['summary']
    assert 'R' in r['summary'] and 'G' in r['summary'] and 'B' in r['summary']
    assert r['merge']['box']['x']>=r['panel']['x']
    assert r['merge']['box']['right']<=r['panel']['right']
    assert r['rgbBox']['x']>=r['panel']['x'] and r['rgbBox']['right']<=r['panel']['right']
    assert r['panel']['bottom']<r['footer']['y']
    if r['viewport']>900:
        assert max(f['cy'] for f in r['figures'])-min(f['cy'] for f in r['figures'])<1.5
        assert all(r['steps'][i]['right']<r['steps'][i+1]['x'] for i in range(3))
    else:
        assert all(r['figures'][i]['bottom']<r['figures'][i+1]['y'] for i in range(3))
        assert all(r['arrows'][i]['cy']>r['figures'][i]['bottom'] and
                   r['arrows'][i]['cy']<r['figures'][i+1]['y'] for i in range(3))
    return {'resample':[80,80],'roi':[52,38,4,4],'roi_on_matrix':True,
            'selected_index':6,'selected_xy':[54,39],'rgb':rgb,'hex':r['hex'],
            'rgb_planes_order':['B','G','R'],
            'plane_pixel_checks':80*80*4*3,'rgb_planes_are_real_samples':True,
            'all_16_colors_match':True,'single_panel_four_stages':True,
            'crop_channel_depth':3,'crop_stack_order':['B','G','RGB'],
            'crop_rgb_16_match':True,'crop_g_16_match':True,
            'crop_b_16_match':True,'merge_uses_same_rgb':True,
            'shape':'H×W×3','patch_values':48,'matrix_roi_normalized':r['matrixROI'],
            'text_axis_alignment_px':{
                'w_center_on_b':round(r['wText']['cx']-b_grid['cx'],3),
                'h_center_on_rgb':round(r['hText']['cy']-r['pixelGrid']['cy'],3),
                'w_gap_below_stack':round(r['wText']['y']-max(p['grid']['bottom'] for p in crop),3),
                'h_gap_left_rgb':round(r['pixelGrid']['x']-r['hText']['right'],3)},
            'crop_c_label_removed':True,'crop_guides_removed':True,
            'crop_display_tints':{'G':'#279467','B':'#427ec5'},
            'crop_display_formula':'rgb(255+(base-255)*(0.22+0.78*v/255))',
            'crop_plane_badges':['B','G','R'],
            'figure_center_errors_px':r['visualCenters'],
            'selected_halo_px':2,'selected_navy_outline_px':5}

def check_motif(page,name):
    points=[0,1,63,64,65,32*64+32,4095]
    r=page.evaluate('''async(points)=>{const im=document.querySelector('img'),cv=document.createElement('canvas');cv.width=cv.height=64;const ctx=cv.getContext('2d',{willReadFrequently:true});ctx.imageSmoothingEnabled=true;ctx.imageSmoothingQuality='high';ctx.drawImage(im,0,0,64,64);const state=window.CNNFeatureMaps;const svg=document.querySelector('.process-feature-svg,.compare-feature-svg');const painted=[];for(const e of svg.querySelectorAll('image')){const img=new Image();img.src=e.getAttribute('href');await img.decode();ctx.clearRect(0,0,64,64);ctx.drawImage(img,0,0);const raw=ctx.getImageData(0,0,64,64).data;painted.push(points.map(p=>[...raw.slice(p*4,p*4+3)]));}ctx.clearRect(0,0,64,64);ctx.drawImage(im,0,0,64,64);return {rgba:[...ctx.getImageData(0,0,64,64).data],samples:state.result.conv1.map(channel=>points.map(p=>channel[p])),painted,channels:state.result.conv1.length,photos:[...document.querySelectorAll('img')].map(e=>e.getAttribute('src')),status:state.status}}''',points)
    assert r['status']=='ready' and r['channels']==16
    lum=[struct.unpack('f',struct.pack('f',(r['rgba'][4*i]*.2126+r['rgba'][4*i+1]*.7152+r['rgba'][4*i+2]*.0722)/255))[0] for i in range(4096)]
    def q(x,y):return lum[max(0,min(63,y))*64+max(0,min(63,x))]
    expected=[]
    for channel in range(16):
        values=[];a=channel*math.pi/8
        for pos in points:
            y,x=divmod(pos,64)
            gx=(q(x+1,y-1)+2*q(x+1,y)+q(x+1,y+1)-q(x-1,y-1)-2*q(x-1,y)-q(x-1,y+1))/8
            gy=(q(x-1,y+1)+2*q(x,y+1)+q(x+1,y+1)-q(x-1,y-1)-2*q(x,y-1)-q(x+1,y-1))/8
            values.append(max(0,(gx*math.cos(a)+gy*math.sin(a)+(channel%4)*.007)*3.2))
        expected.append(values)
    assert all(abs(a-b)<1e-6 for aa,bb in zip(expected,r['samples']) for a,b in zip(aa,bb))
    painted=[]
    for channel in [9,6,3,0]:
        colors=[]
        for value in r['samples'][channel]:
            v=min(1,max(0,value*4.5))**.74
            colors.append([math.floor(a+(b-a)*v+.5) for a,b in zip([242,247,253],[30,74,142])])
        painted.append(colors)
    assert painted==r['painted']
    assert len(r['photos'])==(2 if name=='comparison' else 1)
    if name=='comparison':assert page.locator('.rule-conditions span').all_text_contents()==['색상 조건','형태 조건']
    return {'independent_gradient_samples':16*len(points),'painted_pixels':4*len(points),'channels':16,'boundary':'replicate','learned_inference':False}

def ints(page,selector):return [int(s.replace('−','-')) for s in page.locator(selector).all_text_contents()]

def check_step(page,width):
    values=ints(page,'.input5 > div');k=ints(page,'.kernel3 > div');assert len(values)==25 and len(k)==18 and k[:9]==k[9:]
    kernel=k[:9];patch=[values[y*5+x] for y in range(3) for x in range(3)]
    products=[a*b for a,b in zip(patch,kernel)]
    out=[sum(values[(y+ky)*5+x+kx]*kernel[ky*3+kx] for ky in range(3) for kx in range(3)) for y in range(3) for x in range(3)]
    assert ints(page,'.patch3 > div')==patch and ints(page,'.product3 strong')==products
    assert ints(page,'.output3 > div')==out and out[0]==sum(products)==-6
    assert ints(page,'.input5 .focus-rf')==patch and len(page.locator('.input5 .focus-rf').all())==9
    assert page.locator('.calc-equation').inner_text()=='1 + 0 − 3 + 4 + 0 − 6 + 7 + 0 − 9 = −6'
    equation=page.locator('.calc-equation').evaluate('''e=>{const range=document.createRange();range.selectNodeContents(e);const b=range.getBoundingClientRect(),card=e.closest('.calc-panel'),c=card.getBoundingClientRect(),s=getComputedStyle(card),scale=c.width/parseFloat(s.width);return {left:b.left,right:b.right,innerLeft:c.left+(parseFloat(s.paddingLeft)+parseFloat(s.borderLeftWidth))*scale,innerRight:c.right-(parseFloat(s.paddingRight)+parseFloat(s.borderRightWidth))*scale}}''')
    assert equation['left']>=equation['innerLeft']-1 and equation['right']<=equation['innerRight']+1,equation
    if width>900:
        feet=page.locator('.calc-footnote').evaluate_all('(es)=>es.map(e=>e.getBoundingClientRect().top)');assert abs(feet[0]-feet[1])<1
    return {'input':[values[i:i+5] for i in range(0,25,5)],'kernel':[kernel[i:i+3] for i in range(0,9,3)],'products':products,'output':[out[i:i+3] for i in range(0,9,3)],'stride':1,'padding':0,'bias':0,'kernel_flipped':False}

def check_interactive(page):
    samples=[(.15,0),(.32,1),(.48,0),(.67,1),(.82,1),(.94,0)];states=[]
    for t in range(0,101,5):
        page.locator('#threshold').fill(str(t));c=dict(tp=0,fp=0,fn=0,tn=0);expected=[]
        for score,truth in samples:
            p=score>=t/100;key=('tp' if p else 'fn') if truth else ('fp' if p else 'tn');c[key]+=1;expected.append(key.upper())
        assert {key:int(page.locator('#cm-'+key).inner_text()) for key in c}==c
        labels=page.locator('.score-row').evaluate_all('(rows)=>rows.sort((a,b)=>Number(a.dataset.sample)-Number(b.dataset.sample)).map(r=>r.querySelector(".outcome").textContent)');assert labels==expected
        for metric,extra in [('precision','fp'),('recall','fn')]:
            n,d=c['tp'],c['tp']+c[extra];pct=f'{n/d*100:.1f}%' if d else '정의 불가'
            assert page.locator('#'+metric).inner_text()==pct
            assert page.locator('#'+metric+'-calculation').inner_text()==f'{n} / ({n} + {c[extra]}) = {pct}'
        states.append({'threshold':t/100,**c})
    assert page.locator('.sample-group').evaluate_all('(es)=>es.map(e=>e.dataset.truth)')==['1','0']
    page.locator('#threshold').fill('60');page.locator('h1').click()
    return {'states':states,'matrix_order':page.locator('.live-cm td').evaluate_all('(es)=>es.map(e=>e.dataset.code)')}

def check_architecture(page,width):
    r=page.evaluate('''()=>{const cx=e=>{const b=e.getBoundingClientRect();return b.x+b.width/2};const cy=e=>{const b=e.getBoundingClientRect();return b.y+b.height/2};const stages=[...document.querySelectorAll('.arch-stage')];return {titles:stages.map(e=>e.querySelector('.arch-title').textContent),shapes:stages.map(e=>e.querySelector('.arch-shape').textContent),photos:document.querySelectorAll('[data-art="input"] image').length,inputRects:document.querySelectorAll('[data-art="input"] rect').length,inner:[...document.querySelectorAll('[data-internal-arrow]')].map(e=>e.getAttribute('d')),outer:[...document.querySelectorAll('.arch-connector path')].map(e=>e.getAttribute('d')),centers:stages.map(e=>({title:cx(e.querySelector('.arch-title')),shape:cx(e.querySelector('.arch-shape')),figure:cx(e.querySelector('[data-artwork]')),graphic:cx(e.querySelector('.arch-graphic'))})),probabilities:[...document.querySelectorAll('[data-art="softmax"] text')].map(e=>e.textContent),blockShapes:[...document.querySelectorAll('[data-art="block1"] text,[data-art="block2"] text')].map(e=>e.textContent)}}''')
    assert r['titles']==['INPUT','CONV BLOCK 1','CONV BLOCK 2','FLATTEN','FC LAYER','SOFTMAX']
    conv=lambda n,k,s,p:(n+2*p-k)//s+1
    b1=conv(conv(64,3,1,1),2,2,0);b2=conv(conv(b1,3,1,1),2,2,0);flat=b2*b2*32
    assert (b1,b2,flat)==(32,16,8192)
    assert r['shapes']==['64×64×3','32×32×16','16×16×32','8,192','3 logits','3 probabilities']
    assert r['photos']==1 and r['inputRects']==0 and len(r['inner'])==3 and len(r['outer'])==5
    for d in r['inner']+r['outer']:
        import re
        parts=re.findall(r'-?\d+(?:\.\d+)?',d);v=list(map(float,parts));assert len(v)==9
        # M from,y H tip M shoulder,upper L tip,y L shoulder,lower
        assert v[2]==v[5] and v[1]==v[6] and v[0]<v[2] and v[3]==v[7] and v[4]<v[1]<v[8]
    if width>520:
        for c in r['centers']:assert max(abs(c['figure']-c['graphic']),abs(c['title']-c['shape']),abs(c['shape']-c['graphic']))<2,c
    e=[math.exp(v) for v in [2,1,0]];expected=[round(v/sum(e)*100,1) for v in e]
    actual=[float(s[:-1]) for s in r['probabilities'] if s.endswith('%')];assert actual==expected and abs(sum(actual)-100)<.1
    return {**r,'computed_block_outputs':[[b1,b1,16],[b2,b2,32]],'flatten':flat,'example_logits':[2,1,0],'softmax_percent':actual,'feature_maps':'schematic; not trained inference'}

def check_experiment(page):
    r=page.evaluate(EXPERIMENT_GEOMETRY)
    assert r['labels']=={'columns':['실제 이상','실제 정상'],'rows':['예측 이상','예측 정상']}
    assert [(c['code'],c['count']) for c in r['counts']]==[('TP',4),('FP',1),('FN',2),('TN',5)]
    tp,fp,fn,tn=4,1,2,5;precision=Fraction(tp,tp+fp);recall=Fraction(tp,tp+fn)
    vals={'accuracy':Fraction(tp+tn,12),'precision':precision,'recall':recall,'f1':Fraction(2*tp,2*tp+fp+fn)}
    assert vals['f1']==2*precision*recall/(precision+recall)
    fractions={'accuracy':'9/12','precision':'4/5','recall':'4/6','f1':'8/11'}
    equations={'accuracy':('(TP + TN) / (TP + TN + FP + FN)',['TP + TN','TP + TN + FP + FN']),'precision':('TP / (TP + FP)',['TP','TP + FP']),'recall':('TP / (TP + FN)',['TP','TP + FN']),'f1':('2TP / (2TP + FP + FN)',['2TP','2TP + FP + FN'])}
    for m in r['metrics']:
        pct=f'{float(vals[m["name"]])*100:.1f}%';assert m['value']==pct and m['calculation']==f'= {fractions[m["name"]]} = {pct}'
        assert (m['formula'],m['fraction'])==equations[m['name']]
    assert page.locator('.metric-alternate').inner_text().replace('\n',' ')=='= 2 × Precision × Recall / (Precision + Recall)'
    assert not r['overflow'] and not r['badTypography'] and r['fontsLoaded']>0
    assert abs(r['dividerGaps']['left']-r['dividerGaps']['right'])<.25
    assert all(max(c['xErrors'])<2 and c['yError']<2 for c in r['centering'])
    assert max([r['axisErrors']['gt'],r['axisErrors']['prediction'],*r['axisErrors']['columns'],*r['axisErrors']['rows']])<2
    return r

def write_compatibility_reports(report):
    """Keep legacy report URLs on the same execution as the full 48-case proof."""
    groups={
        'process-validation.json':['process'],
        'concept-architecture-validation.json':['concept','architecture'],
        'professional-figures-validation.json':['process','comparison','architecture'],
        'step-pretendard-validation.json':['step-by-step'],
        'experiment-validation.json':['experiment'],
        'executive-summary-validation.json':['executive-summary'],
    }
    for filename,names in groups.items():
        subset={**report,'derived_from':'reference-validation.json (same final-source execution)',
                'templates':names,'cases':[c for c in report['cases'] if c['template'] in names]}
        (ROOT/'previews/review'/filename).write_text(json.dumps(subset,ensure_ascii=False,indent=2)+'\n')

def main(argv=None):
    parser=ArgumentParser(description=__doc__);parser.add_argument('--templates',nargs='+',choices=NAMES,default=list(NAMES));parser.add_argument('--evidence-dir',type=Path,default=Path('/tmp/reference-integration-review'));parser.add_argument('--report',type=Path)
    parser.add_argument('--update-previews',nargs='*',choices=NAMES,help='Only regenerate these canonical previews; default is every selected template')
    args=parser.parse_args(argv);args.evidence_dir.mkdir(parents=True,exist_ok=True)
    updated_previews=args.templates if args.update_previews is None else args.update_previews
    assert set(updated_previews)<=set(args.templates),'Preview targets must be selected templates'
    report_path=args.report or ROOT/'previews/review'/('reference-validation.json' if len(args.templates)==8 else 'selected-reference-validation.json');report_path.parent.mkdir(parents=True,exist_ok=True)
    report={'status':'running','started_utc':datetime.now(timezone.utc).isoformat(),'viewports':[list(v) for v in SIZES],'templates':list(args.templates),'cases':[],'font_delivery':'original local Pretendard v1.3.9, no CDN interception','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'templates/html').rglob('*') if p.is_file() and p.suffix in ('.html','.css','.js','.woff2','.png','.jpg')}}
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start()
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(**browser_options());report['browser']=browser.version
            page=browser.new_page();errors=[];failed=[];http=[]
            page.on('pageerror',lambda e:errors.append(str(e)));page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None);page.on('requestfailed',lambda r:failed.append(r.url));page.on('response',lambda r:http.append(f'{r.status} {r.url}') if r.status>=400 and 'favicon' not in r.url else None)
            for width,height in SIZES:
                for name in args.templates:
                    page.set_viewport_size({'width':width,'height':height});page.goto(f'http://127.0.0.1:{server.server_port}/templates/html/{name}.html',wait_until='networkidle');page.evaluate('document.fonts.ready')
                    if name in ('process','comparison'):page.wait_for_function("window.CNNFeatureMaps?.status==='ready'")
                    if name=='concept':page.wait_for_function("document.querySelector('.slide').dataset.sampled==='true'")
                    if name=='concept':technical=check_concept(page)
                    elif name in ('process','comparison'):
                        technical=check_motif(page,name)
                        if name=='process':technical['prediction_flow']=check_process(page,width)
                    elif name=='step-by-step':technical=check_step(page,width)
                    elif name=='interactive':technical=check_interactive(page)
                    elif name=='architecture':technical=check_architecture(page,width)
                    elif name=='experiment':technical=check_experiment(page)
                    else:technical=check_executive(page,width)
                    fonts=actual_fonts(page);assert not fonts['fallback'] and not fonts['unpainted'] and not fonts['bad_spacing'],(name,width,fonts)
                    assert min(fonts['loaded']['counts'])>0 and fonts['loaded']['faces']
                    geometry=page.evaluate(GEOMETRY)
                    padding=page.evaluate(CARD_PADDING);assert not any(p['escaped'] for p in padding),(name,width,padding)
                    geometry['card_padding']=padding
                    for key in ['outside','overflow','footerOverlap','spacing','clippedText','arrowErrors']:assert not geometry[key],(name,width,key,geometry[key])
                    assert geometry['pageWidth']<=width
                    if width>900:
                        b=geometry['slide'];assert b['right']<=width+1 and b['bottom']<=height+1 and abs(b['width']/b['height']-16/9)<.002
                    broken=page.locator('img').evaluate_all('(es)=>es.filter(e=>!e.complete||!e.naturalWidth).map(e=>e.src)');assert not broken,broken
                    page.locator('.slide').screenshot(path=str(args.evidence_dir/f'{name}-{width}x{height}.png'),animations='disabled')
                    if width==1600 and name in updated_previews:
                        ext='png' if name in ('concept','process','comparison') else 'jpg';kwargs={'quality':94} if ext=='jpg' else {}
                        page.locator('.slide').screenshot(path=str(ROOT/f'previews/html-{name}.{ext}'),animations='disabled',**kwargs)
                    report['cases'].append({'template':name,'viewport':[width,height],'technical':technical,'fonts':fonts,'geometry':geometry})
                    print('PASS',name,width,height,flush=True)
            if 'process' in args.templates:
                report['process_robustness']=check_process_robustness(browser,f'http://127.0.0.1:{server.server_port}',args.evidence_dir)
            assert not errors and not failed and not http,(errors,failed,http)
            report.update(status='passed',page_errors=errors,failed_requests=failed,http_errors=http);browser.close()
    except Exception as exc:report.update(status='failed',error=str(exc));raise
    finally:
        server.shutdown();server.server_close()
        report['canonical_preview_sha256']={str(path.relative_to(ROOT)):hashlib.sha256(path.read_bytes()).hexdigest() for name in args.templates for path in [ROOT/f'previews/html-{name}.{"png" if name in ("concept","process","comparison") else "jpg"}'] if path.exists()}
        report['finished_utc']=datetime.now(timezone.utc).isoformat()
        report['canonical_preview_updates']=list(updated_previews)
        report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
        if len(args.templates)==8 and report_path.name=='reference-validation.json':write_compatibility_reports(report)
    print(f'PASS {len(report["cases"])} final-source viewports; report: {report_path}')

if __name__=='__main__':main()
