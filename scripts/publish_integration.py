"""Publish the validated integration normally, then merge and retire old PRs.

Run from a clean integration checkout with a GitHub identity that can push:
  python scripts/publish_integration.py --check-only
  python scripts/publish_integration.py --merge
Never changes credentials, forces a push, or bypasses repository protections.
"""
from argparse import ArgumentParser
from datetime import datetime, timezone
from pathlib import Path
import json
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / 'docs/integration-sources.json').read_text())
REPO = MANIFEST['repo']


def run(*args, capture=True):
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=capture)
    if result.returncode:
        detail = (result.stderr or result.stdout or '').strip()
        raise RuntimeError(f'{args[0]} {args[1]} failed ({result.returncode}): {detail}')
    return result.stdout.strip() if capture else ''


def gh_json(*args):
    return json.loads(run('gh', *args))


def ancestor(older, newer):
    result = subprocess.run(['git', 'merge-base', '--is-ancestor', older, newer], cwd=ROOT)
    if result.returncode not in (0, 1):
        raise RuntimeError('Cannot inspect commit ancestry')
    return result.returncode == 0


def preflight():
    branch = run('git', 'branch', '--show-current')
    if branch != MANIFEST['integration_branch']:
        raise RuntimeError(f'Checkout {MANIFEST["integration_branch"]} first')
    if run('git', 'status', '--porcelain'):
        raise RuntimeError('Commit or preserve local changes first; checkout must be clean')
    remote = run('git', 'remote', 'get-url', 'origin').removesuffix('.git')
    if remote not in (f'https://github.com/{REPO}', f'git@github.com:{REPO}'):
        raise RuntimeError(f'origin must be the canonical repository {REPO}')
    for source in MANIFEST['sources'].values():
        run('git', 'cat-file', '-e', source['head'] + '^{commit}')
    # These checks use the final committed files and detect stale render evidence.
    run(sys.executable, 'scripts/check_sources.py', capture=False)
    run(sys.executable, 'scripts/check_documentation.py', capture=False)
    for name in ('interactive-validation.json', 'dual-mode-validation.json'):
        evidence = json.loads((ROOT / 'previews/review' / name).read_text())
        if evidence.get('status') != 'passed':
            raise RuntimeError(f'{name} has not passed')
    account = gh_json('api', 'user')['login']
    permissions = gh_json('api', f'repos/{REPO}')['permissions']
    print(f'GitHub identity: {account}; permissions: {json.dumps(permissions)}', flush=True)
    if not permissions.get('push'):
        raise RuntimeError(f'{account} has no push permission for {REPO}. '
                           'Connect an authorized GitHub identity or grant repository access. '
                           'No push, PR, merge or PR cleanup was attempted.')
    run('git', 'fetch', 'origin', 'main')
    head = run('git', 'rev-parse', 'HEAD')
    main = run('git', 'rev-parse', 'origin/main')
    if not ancestor(main, head) and not ancestor(head, main):
        raise RuntimeError('main advanced independently. Integrate it and rerun all validation first.')
    for key in ('pr9', 'pr10', 'pr11'):
        source = MANIFEST['sources'][key]
        pr = gh_json('pr', 'view', str(source['pr']), '--repo', REPO,
                     '--json', 'headRefOid,state')
        if pr['headRefOid'] != source['head']:
            raise RuntimeError(f'PR #{source["pr"]} advanced. Review its new commits before publication.')
    return head, account


def find_or_create_pr():
    prs = gh_json('pr', 'list', '--repo', REPO, '--head', MANIFEST['integration_branch'],
                  '--base', 'main', '--state', 'all', '--json', 'number,url,state,headRefOid')
    candidates = [p for p in prs if p['state'] in ('OPEN', 'MERGED')]
    if candidates:
        return candidates[0]
    run('gh', 'pr', 'create', '--repo', REPO, '--base', 'main',
        '--head', MANIFEST['integration_branch'],
        '--title', 'Integrate eight HTML references, verified Pretendard previews and figure standards',
        '--body-file', str(ROOT / 'docs/INTEGRATION_PR.md'), capture=False)
    return gh_json('pr', 'view', MANIFEST['integration_branch'], '--repo', REPO,
                   '--json', 'number,url,state,headRefOid')


def await_checks(number, head):
    deadline = time.monotonic() + 1800
    while time.monotonic() < deadline:
        pr = gh_json('pr', 'view', str(number), '--repo', REPO,
                     '--json', 'headRefOid,statusCheckRollup')
        if pr['headRefOid'] != head:
            raise RuntimeError('Integration PR head changed; refusing to merge unreviewed commits')
        checks = pr['statusCheckRollup']
        if checks:
            run('gh', 'pr', 'checks', str(number), '--repo', REPO,
                '--watch', '--interval', '10', '--fail-fast', capture=False)
            final = gh_json('pr', 'view', str(number), '--repo', REPO,
                            '--json', 'headRefOid,statusCheckRollup')
            if final['headRefOid'] != head:
                raise RuntimeError('PR head changed while waiting for CI')
            validate = [c for c in final['statusCheckRollup'] if c.get('name') == 'validate']
            if not validate or any(c.get('conclusion') != 'SUCCESS' for c in validate):
                raise RuntimeError('The final HTML validation CI job must succeed before merging')
            return
        print('Waiting for PR validation checks to appear...', flush=True)
        time.sleep(10)
    raise RuntimeError('CI checks did not appear; no merge was attempted')


def publish(head, account, output):
    # Immutable source commits work from a bundle clone even without local branch names.
    for key in ('interactive', 'experiment'):
        source = MANIFEST['sources'][key]
        run('git', 'push', 'origin', f'{source["head"]}:refs/heads/{source["branch"]}', capture=False)
    run('git', 'push', '-u', 'origin', MANIFEST['integration_branch'], capture=False)
    pr = find_or_create_pr()
    if pr['headRefOid'] != head:
        raise RuntimeError('Remote integration head differs from the validated local commit')
    if pr['state'] == 'OPEN':
        await_checks(pr['number'], head)
        run('gh', 'pr', 'merge', str(pr['number']), '--repo', REPO,
            '--merge', '--match-head-commit', head, capture=False)
    final = gh_json('pr', 'view', str(pr['number']), '--repo', REPO,
                    '--json', 'url,state,mergeCommit,headRefOid')
    if final['state'] != 'MERGED' or not final.get('mergeCommit'):
        raise RuntimeError('GitHub has not completed the merge. Old PRs remain untouched.')
    run('git', 'fetch', 'origin', 'main')
    main = run('git', 'rev-parse', 'origin/main')
    if not ancestor(head, main):
        raise RuntimeError('Integration commit is not present in fetched main')
    # Verify actual final files, not just commit ancestry (no squash merge is used).
    paths = run('git', 'diff', '--name-only', MANIFEST['main_base'], head).splitlines()
    if paths:
        if run('git', 'diff', '--name-only', head, main, '--', *paths):
            raise RuntimeError('main contains further changes to integration files; inspect before retiring PRs')
    result = {'status': 'merged', 'time_utc': datetime.now(timezone.utc).isoformat(),
              'account': account, 'pr': final['url'], 'integration_head': head,
              'merge_commit': final['mergeCommit']['oid'], 'main': main, 'retired_prs': []}
    # Keep a durable result even if a later PR comment/close is rejected.
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    for key in ('pr9', 'pr10', 'pr11'):
        source = MANIFEST['sources'][key]
        old = gh_json('pr', 'view', str(source['pr']), '--repo', REPO,
                      '--json', 'headRefOid,state')
        item = {'number': source['pr'], 'previous_state': old['state']}
        if old['state'] == 'OPEN' and old['headRefOid'] == source['head']:
            message = (f'최종 구현을 {final["url"]}에서 검증 후 main에 통합했습니다. '
                       '각 페이지의 최신 버전을 선택했고, Architecture는 #10, '
                       'Step-by-Step은 #11 기준입니다. 이 PR은 통합 PR로 대체되어 정리합니다.')
            run('gh', 'pr', 'close', str(source['pr']), '--repo', REPO,
                '--comment', message, capture=False)
            item['result'] = 'closed with integration link'
        else:
            item['result'] = 'left unchanged (already closed/merged or head advanced)'
        result['retired_prs'].append(item)
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


def main():
    parser = ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check-only', action='store_true', help='Read-only preflight')
    mode.add_argument('--merge', action='store_true', help='Push, create PR, require CI, merge, retire old PRs')
    parser.add_argument('--result', type=Path, default=Path('/tmp/design-template-integration-publish.json'))
    args = parser.parse_args()
    try:
        head, account = preflight()
        print(f'Preflight passed for {head}', flush=True)
        if args.merge:
            publish(head, account, args.result)
    except (RuntimeError, FileNotFoundError) as exc:
        print(f'BLOCKED: {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
