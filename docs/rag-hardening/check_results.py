"""Check stage4 evidence identity and separate accepted/rejected outcomes."""
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
m=json.loads((HERE/'EVIDENCE.json').read_text())
for path,h in m['sha256'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==h,('changed evidence',path)
expected={'baseline':True,'long-original':True,'long-reflow':True,'description-original':False,'description-reflow':True,'overload-reject':False}
views={(mode,(w,h)) for mode in ['scroll','slides'] for w,h in [(1600,950),(1440,810),(1366,768),(1280,720)]}
for path,key,n in [('evidence/validation.json','source_sha256',48),('review/audit.json','hashes',8),('review/variants.json','hashes',40)]:
 d=json.loads((HERE/path).read_text());assert d['pass'] and len(d['cases'])==n
 for name,h in d[key].items():assert hashlib.sha256((ROOT/'examples/rag-architecture'/name).read_bytes()).hexdigest()==h
 for row in d['cases']:
  assert row['pass'] and not row['errors']
  if 'fit' in row:assert row['fit']==expected[row['case']]==row['expectedFit']
 cases={x.get('case','baseline') for x in d['cases']}
 for case in cases:assert {(x['mode'],tuple(x['viewport'])) for x in d['cases'] if x.get('case','baseline')==case}==views
 if n==48:assert sum(x['fit'] for x in d['cases'])==32
print('PASS runtime/test/capture hashes; 32 accepted and 16 correctly rejected; independent baseline8 and variants40')
