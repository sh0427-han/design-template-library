"""Check all Markdown file links and final design / rendered-source contracts."""
from pathlib import Path
import hashlib,json,re
ROOT=Path(__file__).resolve().parents[1]

def main():
    links=0;docs=list(ROOT.rglob('*.md'));broken=[]
    for doc in docs:
        text=doc.read_text();body=re.sub(r'```[\s\S]*?```','',text)
        assert not re.search(r'templates/pptx|technical-slide-templates\.pptx|build_templates\.py|CHARACTER_SPACING_PT',text),(doc,'obsolete output instruction')
        for match in re.finditer(r'!?\[[^\]]*\]\((<[^>]+>|[^\s)]+)(?:\s+"[^"]*")?\)',body):
            target=match.group(1).strip('<>');target=target.split('#')[0].split('?')[0]
            if not target or re.match(r'^[a-z]+:',target):continue
            links+=1
            if not (doc.parent/target).exists():broken.append((str(doc.relative_to(ROOT)),target))
    assert not broken,broken
    required=['README.md','TEMPLATE_CATALOG.md','DESIGN_SYSTEM.md','docs/FIGURE_PRODUCTION_STANDARD.md','docs/REFERENCE_PAGE_SPECS.md','docs/REFERENCE_REUSE_WORKFLOW.md']
    assert all((ROOT/p).is_file() for p in required)
    specs=(ROOT/'docs/REFERENCE_PAGE_SPECS.md').read_text()
    for number,name in enumerate(['Concept','Process','Comparison','Step-by-Step','Interactive','Architecture','Experiment','Executive Summary'],1):assert f'## {number:02d} {name}' in specs
    assert all(s in specs for s in ['8,192','64×64×3','32×32×16','16×16×32','TP=4','FP=1','FN=2','TN=5','72.7%','−6'])
    catalog=(ROOT/'TEMPLATE_CATALOG.md').read_text();assert 'PR #10' in catalog and 'PR #11' in catalog and 'Flatten' in catalog
    validation=json.loads((ROOT/'previews/review/reference-validation.json').read_text())
    assert validation['status']=='passed' and len(validation['cases'])==48
    assert {(c['template'],tuple(c['viewport'])) for c in validation['cases']}=={(n,tuple(s)) for n in validation['templates'] for s in validation['viewports']}
    for path,expected in validation['source_sha256'].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==expected,('rendered source changed',path)
    for path,expected in validation['canonical_preview_sha256'].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==expected,('preview changed',path)
    interactive=json.loads((ROOT/'previews/review/interactive-validation.json').read_text())
    assert interactive['status']=='passed' and interactive['math_checks']==126 and interactive['reuse']['checks']==42
    assert interactive['portable_html']['content_within_tolerance'] and interactive['offline_portable']['default']['fallback_elements']==0
    pilot_root=ROOT/'examples/logistic-regression'
    pilot=json.loads((pilot_root/'previews/validation.json').read_text())
    assert pilot['status']=='passed' and len(pilot['cases'])==40 and pilot['math_checks']==606 and pilot['alternate_data_checks']==404
    assert pilot['main_pages']==2 and pilot['appendix_pages']==1 and pilot['appendix_opt_in']
    assert pilot['concept_is_symbolic'] and pilot['concept_is_invariant'] and pilot['result_transfer']
    assert {(c['scope'],c['mode'],c['template'],tuple(c['viewport'])) for c in pilot['cases']}=={(scope,m,n,s) for scope,names in [('main',('concept','calculation')),('with_appendix',('concept','calculation','threshold'))] for m in ('slides','scroll') for n in names for s in ((1600,950),(1440,810),(1366,768),(1280,720))}
    for path,expected in pilot['source_sha256'].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==expected,('pilot rendered source changed',path)
    assert hashlib.sha256((pilot_root/'DESIGN.md').read_bytes()).hexdigest()==pilot['design_sha256'],'pilot design changed after validation'
    assert sorted(p.name for p in (pilot_root/'previews').glob('*.jpg'))==['scroll.jpg','slide.jpg']
    for name,expected in pilot['preview_sha256'].items():
        assert hashlib.sha256((pilot_root/'previews'/name).read_bytes()).hexdigest()==expected,('pilot preview changed',name)
    assert set(pilot['review_preview_sha256'])=={'concept.png','calculation.png','threshold.png'}
    for name,expected in pilot['review_preview_sha256'].items():
        assert hashlib.sha256((pilot_root/'review'/name).read_bytes()).hexdigest()==expected,('pilot review image changed',name)
    print(f'PASS {len(docs)} Markdown files / {links} local links; eight final specs, source/preview hashes and Interactive reuse evidence')
if __name__=='__main__':main()
