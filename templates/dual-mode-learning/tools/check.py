"""Check static template consistency without third-party packages."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    'DESIGN.md', 'MODES.md', 'index.html', 'scroll.html', 'slides.html',
    'assets/css/tokens.css', 'assets/css/components.css',
    'assets/css/scroll.css', 'assets/css/slides.css',
    'assets/js/lesson.js', 'assets/js/lab.js', 'assets/js/render.js',
    'assets/js/scroll.js', 'assets/js/slides.js',
]
missing = [str(path) for name in REQUIRED if not (path := ROOT / name).is_file()]
assert not missing, f'Missing files: {missing}'
for name in ('scroll.html', 'slides.html'):
    html = (ROOT / name).read_text(encoding='utf-8')
    for required_css in ('tokens.css', 'components.css'):
        assert required_css in html, f'{name} does not include {required_css}'
assert 'renderLessons' in (ROOT / 'assets/js/scroll.js').read_text(encoding='utf-8')
assert 'renderLessons' in (ROOT / 'assets/js/slides.js').read_text(encoding='utf-8')
assert 'mountLab' in (ROOT / 'assets/js/render.js').read_text(encoding='utf-8')
ids = re.findall(r"id: '([^']+)'", (ROOT / 'assets/js/lesson.js').read_text(encoding='utf-8'))
assert len(ids) == len(set(ids)) == 5, f'Unexpected duplicate/missing sections: {ids}'
print('PASS: files, common styles, shared content, shared lab and section IDs')
