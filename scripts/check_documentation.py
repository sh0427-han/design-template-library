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
    print(f'PASS {len(docs)} Markdown files / {links} local links; eight final specs, source/preview hashes and Interactive reuse evidence')
if __name__=='__main__':main()
