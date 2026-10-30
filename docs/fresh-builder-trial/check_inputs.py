"""Reconstruct this trial's supplied design input from its pinned baseline."""
from pathlib import Path
import hashlib,json,re,subprocess
ROOT=Path(__file__).resolve().parents[2]
manifest=json.loads((Path(__file__).parent/'input-manifest.json').read_text())
assert manifest['baseline']=='ff689f9a63b0aa350036b12a01695c8c52c7bda8'
paths=[item['path'] for item in manifest['files']]
assert len(paths)==len(set(paths))==50
assert not any(p.startswith(('examples/','previews/review/')) for p in paths)
for item in manifest['files']:
    raw=subprocess.check_output(['git','show',f"{manifest['baseline']}:{item['path']}"],cwd=ROOT)
    assert hashlib.sha256(raw).hexdigest()==item['source_sha256'],item['path']
    assert hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest()==item['source_sha256'],('frozen common input modified',item['path'])
    omitted=item.get('omitted_history_sections',[])
    if omitted:
        assert item['path']=='docs/TEMPLATE_REUSE_VALIDATION.md'
        sections=re.split(r'(?=^## )',raw.decode(),flags=re.M)
        assert set(omitted)=={'## 로지스틱 회귀 검토에서 반영한 내용','## 과적합·일반화 검토 후 공통 계약 보완'}
        raw=''.join(s for s in sections if s.splitlines()[0] not in omitted).encode()
    assert hashlib.sha256(raw).hexdigest()==item['provided_sha256'],item['path']
print('PASS 50 input files reconstructed from frozen baseline; two declared history sections omitted; no prior example files')
