"""Verify documentation-only role migration without rewriting historical approvals."""
from pathlib import Path
import json
import subprocess
import re
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
BASELINE = 'bfeb7c6cb19a0373f6d4d1a8d54647988c79eebc'


def preserved_body(path, content):
    manifest = json.loads((ROOT / 'docs/document-role-migration.json').read_text())
    assert manifest['baseline'] == BASELINE
    entries = {entry['path']: entry['inserted'] for entry in manifest['entries']}
    assert len(entries) == len(manifest['entries']), 'duplicate migration path'
    if path not in entries:
        return content
    insertion = entries[path].encode()
    assert content.count(insertion) == 1, ('role banner changed/missing', path)
    return content.replace(insertion, b'', 1)


def main():
    manifest = json.loads((ROOT / 'docs/document-role-migration.json').read_text())
    for entry in manifest['entries']:
        path = entry['path']
        original = subprocess.check_output(['git', 'show', f'{BASELINE}:{path}'], cwd=ROOT)
        actual = preserved_body(path, (ROOT / path).read_bytes())
        if path == 'docs/USAGE.md':
            old = original.decode()
            commands = '\n'.join(f'python scripts/{name}.py' for name in (
                'check_sources', 'verify_character_spacing', 'validate_references',
                'check_interactive', 'verify_pretendard', 'check_documentation')) + '\n'
            assert commands in old
            expected = old.replace(commands, '', 1).replace('대표 프리뷰는',
                '공통 검증 명령은 [검토 가이드의 필수 PC 화면 절](REFERENCE_REVIEW_GUIDE.md#필수-pc-화면)에 한 곳에서 관리합니다. 위 설치 후 해당 명령을 저장소 루트에서 실행합니다.\n\n대표 프리뷰는', 1)
            assert actual.decode() == expected, ('unmapped content change', path)
            review = (ROOT / 'docs/REFERENCE_REVIEW_GUIDE.md').read_text()
            assert commands in review, 'canonical commands lost'
        else:
            assert actual == original, ('original rules changed', path)
    fragments = 0
    for name in ('docs/DOCUMENTATION_MAP.md', 'docs/DOCUMENTATION_AUDIT.md',
                 'docs/USAGE.md', 'docs/reviews/document-contracts-review.md'):
        doc = ROOT / name
        for target in re.findall(r'\]\(([^\s)]+)\)', doc.read_text()):
            if '://' in target or '#' not in target:
                continue
            file, fragment = target.split('#', 1)
            destination = doc.parent / file if file else doc
            headings = [re.sub(r'[^\w\- ]', '', h.lower()).replace(' ', '-')
                        for h in re.findall(r'^#+ (.+)$', destination.read_text(), re.M)]
            assert unquote(fragment) in headings, ('navigation anchor missing', name, target)
            fragments += 1
    print(f"PASS {len(manifest['entries'])} role mappings; original bodies preserved, USAGE commands retained at canonical target; {fragments} navigation fragments")


if __name__ == '__main__':
    main()
