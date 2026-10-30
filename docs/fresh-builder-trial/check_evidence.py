"""Check this trial's frozen first result and final evidence; not a render substitute."""
from pathlib import Path
import hashlib,json,subprocess
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
first=json.loads((HERE/'FIRST_SNAPSHOT.json').read_text())
for path,expected in first['first_result_source_sha256'].items():
    raw=subprocess.check_output(['git','show',f"{first['first_result_commit']}:{path}"],cwd=ROOT)
    assert hashlib.sha256(raw).hexdigest()==expected,('first result altered',path)
assert hashlib.sha256((HERE/first['original_builder_history_bundle']).read_bytes()).hexdigest()==first['bundle_sha256']
final=json.loads((HERE/'FINAL_SNAPSHOT.json').read_text())
for path,expected in final['sha256'].items():
    assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==expected,('final evidence altered',path)
expected={(m,(w,h)) for m in ('scroll','slides') for w,h in ((1600,950),(1440,810),(1366,768),(1280,720))}
for path in [ROOT/'examples/rag-architecture/verification.json',HERE/'review-first/audit.json',HERE/'review-final/audit.json']:
    result=json.loads(path.read_text());assert result['pass']
    assert len(result['cases'])==8 and {(c['mode'],tuple(c['viewport'])) for c in result['cases']}==expected
    assert all(c['pass'] and not c['errors'] for c in result['cases'])
for path,key in [(ROOT/'examples/rag-architecture/verification.json','source_sha256'),(HERE/'review-final/audit.json','hashes')]:
    result=json.loads(path.read_text())
    for file,sha in result[key].items():assert hashlib.sha256((ROOT/'examples/rag-architecture'/file).read_bytes()).hexdigest()==sha
print('PASS preserved first-result files/history; final artifact hashes; 8 unique viewport/mode cases per execution; current source matches final evidence')
