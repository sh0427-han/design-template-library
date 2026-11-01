"""Check this trial's first failure and corrected evidence; no render substitute."""
from pathlib import Path
import hashlib,json,subprocess
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];EXAMPLE=ROOT/'examples/service-summary'
first=json.loads((HERE/'FIRST_SNAPSHOT.json').read_text())
for path,expected in first['first_source_sha256'].items():
 raw=subprocess.check_output(['git','show',f"{first['first_commit']}:{path}"],cwd=ROOT)
 assert hashlib.sha256(raw).hexdigest()==expected,path
assert hashlib.sha256((HERE/'builder-first.bundle').read_bytes()).hexdigest()==first['bundle_sha256']
for path,expected in json.loads((HERE/'FINAL_SNAPSHOT.json').read_text())['sha256'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==expected,('changed evidence',path)
views={f'{mode}-{w}x{h}' for mode in ['scroll','slides'] for w,h in [(1600,950),(1440,810),(1366,768),(1280,720)]}
for folder,expected_pass in [('review-first',False),('review-final',True)]:
 d=json.loads((HERE/folder/'results.json').read_text());assert d['passed']==expected_pass
 assert len(d['screens'])==8 and {s['name'] for s in d['screens']}==views
 failed=[k for s in d['screens'] for k,v in s['checks'].items() if not v]
 if expected_pass:
  assert not failed
  for name,h in d['source_sha256'].items():assert hashlib.sha256((EXAMPLE/name).read_bytes()).hexdigest()==h,name
 else:assert len(failed)==8 and set(failed)=={'math_result_font_roles'}
builder=json.loads((EXAMPLE/'previews/validation.json').read_text());assert builder['passed'] and all(c['pass'] for c in builder['checks'])
assert len(builder['screens'])==8 and {s['name'] for s in builder['screens']}==views
for name,h in builder['source_hashes'].items():assert hashlib.sha256((EXAMPLE/name).read_bytes()).hexdigest()==h,name
reg=json.loads((HERE/'regression/reference-validation.json').read_text());assert reg['status']=='passed' and len(reg['cases'])==48 and reg['canonical_preview_updates']==[]
for group in ['source_sha256','canonical_preview_sha256']:
 for name,h in reg[group].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h,name
print('PASS preserved first failure, corrected 8-mode/viewport evidence, current source hashes and unchanged original48 regression')
