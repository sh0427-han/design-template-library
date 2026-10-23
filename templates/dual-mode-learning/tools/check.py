"""Check that both modes reuse the eight editable originals and only two outputs."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
assert sorted(p.name for p in ROOT.glob('*.html'))==['scroll.html','slides.html']
for name in ('scroll','slides'):
    text=(ROOT/f'{name}.html').read_text()
    for part in ('tokens.css','components.css',f'{name}.css',f'{name}.js'):assert part in text,(name,part)
files=re.findall(r"file:'([^']+)'",(ROOT/'assets/js/lesson.js').read_text())
assert len(files)==len(set(files))==8,files
assert all((ROOT/'../html'/name).is_file() for name in files)
assert not (ROOT/'assets/js/lab.js').exists(),'Use original Interactive logic, no duplicate lab engine'
assert 'iframe' in (ROOT/'assets/js/render.js').read_text()
assert 'renderReferences' in (ROOT/'assets/js/scroll.js').read_text()
assert 'renderReferences' in (ROOT/'assets/js/slides.js').read_text()
print('PASS two entrypoints, eight existing HTML sources and one shared renderer')
