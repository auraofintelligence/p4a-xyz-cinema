#!/usr/bin/env python3
"""Read-only local HTTP browser acceptance. A PASS is never visual/source approval."""
import argparse
from datetime import datetime, timezone
import hashlib
import html
import importlib.metadata
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]
VERSION = '1.64.1'
BASE = 'http://127.0.0.1:8768'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def site_file(root, value):
    require(isinstance(value, str) and value, 'Expected nonempty relative file path')
    require('\\' not in value and '%' not in value, 'Encoded/backslash paths are forbidden')
    parts = urlsplit(value)
    require(not parts.scheme and not parts.netloc and not parts.query and not parts.fragment,
            'Paths cannot contain origins, queries or fragments')
    require(not value.startswith('/') and all(p not in ('', '.', '..') for p in value.split('/')),
            'Paths must be normalized and relative')
    target = (root / value).resolve()
    require(target.is_relative_to(root.resolve()) and target.is_file(), f'Not a repository file: {value}')
    return target


def served_repository_file(root, url):
    """Map a local request to the preview server's repository file, not response bytes."""
    parsed = urlsplit(url)
    require(f'{parsed.scheme}://{parsed.netloc}' == BASE and not parsed.fragment,
            'Only local preview request URLs are valid')
    path = unquote(parsed.path, errors='strict')
    require(path.startswith('/') and not path.startswith('//') and '\\' not in path,
            'Invalid served path')
    require(not any(part.startswith('.') for part in path.split('/')),
            'Private or traversal paths are forbidden')
    target = (root / path.lstrip('/')).resolve()
    require(target.is_relative_to(root.resolve()), 'Served path escapes repository')
    if target.is_dir():
        target = (target / 'index.html').resolve()
    require(target.is_relative_to(root.resolve()) and target.is_file(), 'Served repository file missing')
    return target


def strings(values, label):
    require(isinstance(values, list) and all(isinstance(x, str) and x.strip() for x in values), label)


def load_scope(root, path):
    path = path.resolve()
    require(path.is_relative_to(root.resolve()) and path.is_file(), 'Scope must be an existing file inside the repository')
    scope = json.loads(path.read_text())
    require(isinstance(scope, dict), 'Scope must be an object')
    require(not set(scope) - {'schema_version', 'name', 'viewports', 'pages', 'map_journeys', 'redland_clock_pages', 'provenance_files'}, 'Unknown scope field')
    require(scope.get('schema_version') == 1, 'Unsupported scope schema')
    require(re.fullmatch(r'[a-zA-Z0-9_-]{1,100}', scope.get('name', '')), 'Invalid scope name')
    require(isinstance(scope.get('pages'), list) and scope['pages'], 'Scope needs pages')
    seen = set()
    for page in scope['pages']:
        require(isinstance(page, dict) and not set(page) - {'path', 'expected_text', 'absent_text', 'visible'}, 'Unknown page field')
        site_file(root, page['path'])
        require(page['path'].endswith('.html'), 'Page must be HTML')
        require(page['path'] not in seen, 'Duplicate page')
        seen.add(page['path'])
        for key in ('expected_text', 'absent_text', 'visible'):
            strings(page.get(key, []), f'Invalid {key}')
    views = scope.get('viewports')
    require(isinstance(views, list) and views, 'Scope needs viewports')
    for v in views:
        require(set(v) == {'width', 'height'} and all(type(n) is int and 200 <= n <= 3000 for n in v.values()), 'Invalid viewport')
    require(len({v['width'] for v in views}) == len(views), 'Duplicate viewport widths')
    for journey in scope.get('map_journeys', []):
        require(isinstance(journey, dict) and not set(journey) - {'start', 'entry_selector', 'map_path', 'layer', 'search', 'area', 'destination'}, 'Unknown journey field')
        for key in ('start', 'map_path', 'destination'):
            site_file(root, journey[key])
            require(journey[key] in seen, f'Journey {key} must be declared in pages')
        for key in ('entry_selector', 'layer', 'search', 'area'):
            require(isinstance(journey.get(key), str) and journey[key].strip(), f'Missing journey {key}')
    for p in scope.get('redland_clock_pages', []):
        require(p in seen, 'Clock page must be declared in pages')
    for p in scope.get('provenance_files', []):
        site_file(root, p)
    return scope


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def provenance(root, scope_path, scope):
    def git(*args):
        return subprocess.check_output(['git', '-C', str(root), *args], text=True).strip()
    files = {p['path'] for p in scope['pages']} | set(scope.get('provenance_files', []))
    return {'tested_commit': git('rev-parse', 'HEAD'),
            'working_tree_status': git('status', '--porcelain', '--untracked-files=all'),
            'scope_sha256': digest(scope_path), 'runner_sha256': digest(Path(__file__)),
            'requirements_sha256': digest(Path(__file__).with_name('requirements.txt')),
            'files_sha256': {p: digest(site_file(root, p)) for p in sorted(files)},
            'github': {k: os.environ.get(k) for k in ('GITHUB_REPOSITORY', 'GITHUB_SHA', 'GITHUB_RUN_ID', 'GITHUB_RUN_ATTEMPT', 'GITHUB_WORKFLOW', 'GITHUB_REF')},
            'python': sys.version, 'playwright_required': VERSION}


def output_directory(root, output):
    output = output.resolve()
    # Artifacts may only go outside the checkout, or in its dedicated ignored folder.
    require(output != root and (not output.is_relative_to(root) or output.is_relative_to(root / 'browser-qa-results')),
            'Output must be outside repository or inside browser-qa-results')
    require(not output.exists() or not any(output.iterdir()), 'Output directory must be empty (no evidence overwrite)')
    output.mkdir(parents=True, exist_ok=True)
    return output


def finish(report, output):
    report['automated_status'] = 'PASS' if report['checks'] and all(c['status'] == 'PASS' for c in report['checks']) else 'FAIL'
    report['visual_review'] = {'status': 'PENDING', 'note': 'Screenshots need explicit human visual review; automation does not establish source accuracy, editorial approval or publication.'}
    report['artifact_sha256'] = {p.name: digest(p) for p in sorted(output.iterdir()) if p.is_file() and p.suffix in ('.png', '.zip')}
    report['finished_utc'] = datetime.now(timezone.utc).isoformat()
    (output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    links = ''.join(f'<li><a href="{html.escape(p)}">{html.escape(p)}</a></li>' for p in report['screenshots'])
    (output / 'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Browser acceptance</title>'
        f'<h1>Automated {report["automated_status"]}</h1><p>Visual review PENDING. Source/editorial/publication approval not established.</p>'
        f'<a href="report.json">Exact provenance and assertion results</a><ul>{links}</ul>')
    return 0 if report['automated_status'] == 'PASS' else 1


def observe_clock_panels(page):
    """Snapshot delivered state before importing any potentially initializing module."""
    return page.evaluate('''() => ({now: Date.now(), module_declared:
        [...document.scripts].some(script => script.type === 'module' &&
            new URL(script.src, location.href).pathname === '/assets/redland-election-clock.mjs'), panels:
        [...document.querySelectorAll('[data-redland-milestone]')].map(panel => {
            const item = {status:panel.dataset.timingStatus, target:panel.dataset.target,
                kind:panel.dataset.kind, ends:panel.dataset.ends};
            const clock = panel.querySelector('[data-milestone-clock]');
            return {item, actual:panel.querySelector('[data-milestone-status]').textContent,
                hidden:clock.hidden, values:[...clock.querySelectorAll('strong')].map(n=>n.textContent)};
        })})''')


def compare_clock_observation(page, observed):
    require(observed['module_declared'], 'Delivered page is missing the Redland clock module script')
    # The oracle receives a serialized snapshot and never re-reads the repaired DOM.
    expected = page.evaluate('''async observed => {
        const {milestoneState} = await import('/assets/redland-election-clock.mjs');
        return observed.panels.map(panel => milestoneState(panel.item, observed.now));
    }''', observed)
    require(observed['panels'], 'No delivered Redland milestone panels')
    require(len(observed['panels']) == len(expected), 'Clock oracle count mismatch')
    result = []
    for actual, state in zip(observed['panels'], expected):
        r = {**actual, 'expected': state}
        require(r['actual'] == state['text'], f'Clock status mismatch: {r}')
        require(r['hidden'] == (not state['active']), f'Clock visibility mismatch: {r}')
        if r['item']['status'] != 'confirmed':
            require(r['hidden'], 'Unconfirmed milestone must not run countdown')
        if not r['hidden']:
            require(len(r['values']) == 4 and all(v.isdigit() for v in r['values']), 'Invalid countdown digits')
        result.append(r)
    return result


def settle_page(page):
    """Wait for delivered fonts and navigation transitions, without masking failures."""
    page.evaluate('''async () => {
        await document.fonts.ready;
        await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
        if (document.activeViewTransition) await document.activeViewTransition.finished;
    }''')
    page.wait_for_timeout(750)


def run(scope, report, output):
    from playwright.sync_api import sync_playwright, expect
    require(importlib.metadata.version('playwright') == VERSION, f'Install pinned Playwright {VERSION}')
    report['playwright_version'] = importlib.metadata.version('playwright')
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel="chromium")
        report['browser_version'] = browser.version
        report['browser_channel'] = 'chromium'
        report['browser_mode'] = 'full-chromium-new-headless'
        try:
            for viewport in scope['viewports']:
                width = viewport['width']
                context = browser.new_context(viewport=viewport, device_scale_factor=1, locale='en-AU', timezone_id='Australia/Brisbane', service_workers='block')
                context.set_default_timeout(30000)
                context.set_default_navigation_timeout(60000)
                blocked, network_errors, page_errors = [], [], []
                responses = []
                def route(request_route):
                    request = request_route.request
                    u = urlsplit(request.url)
                    if f'{u.scheme}://{u.netloc}' != BASE or request.method not in ('GET', 'HEAD'):
                        blocked.append({'url': request.url, 'method': request.method})
                        request_route.abort()
                    else:
                        request_route.continue_()
                context.route('**/*', route)
                context.tracing.start(screenshots=True, snapshots=True, sources=False)
                page = context.new_page()
                page.on('pageerror', lambda e: page_errors.append(str(e)))
                page.on('response', lambda r: responses.append({'url': r.url, 'status': r.status}) if r.url.startswith(BASE + '/') else None)
                def hash_finished(request):
                    if not request.url.startswith(BASE + '/'):
                        return
                    try:
                        response = request.response()
                        if response is None or not 200 <= response.status < 300:
                            return
                        source = served_repository_file(ROOT, request.url)
                        key = source.relative_to(ROOT).as_posix()
                        if key not in report['loaded_repository_files_sha256']:
                            report['loaded_repository_files_sha256'][key] = digest(source)
                    except Exception as exc:
                        page_errors.append(f'Loaded repository file hash failed: {request.url}: {exc}')
                page.on('requestfinished', hash_finished)
                page.on('requestfailed', lambda r: network_errors.append(r.url) if r.url.startswith(BASE + '/') else None)
                def check(name, fn):
                    entry = {'name': name, 'viewport': viewport, 'status': 'PASS'}
                    try:
                        fn()
                    except Exception as exc:
                        entry.update(status='FAIL', error=str(exc))
                    report['checks'].append(entry)
                    print(f"[{width}px] {entry['status']}: {name}" + (f" | {entry['error']}" if 'error' in entry else ''), flush=True)
                def settle():
                    settle_page(page)
                def screenshot(label):
                    settle()
                    name = f'{width}-{label}.png'
                    page.evaluate('() => window.scrollTo({top: 0, left: 0, behavior: \"instant\"})')
                    page.wait_for_timeout(150)
                    page.screenshot(path=str(output / name), full_page=True)
                    report['screenshots'].append(name)
                def layout():
                    dimensions = page.evaluate('''() => ({viewport: document.documentElement.clientWidth,
                        scroll: Math.max(document.documentElement.scrollWidth, document.body.scrollWidth)})''')
                    require(dimensions['scroll'] <= dimensions['viewport'] + 1, f'Horizontal page overflow: {dimensions}')
                def goto(path):
                    response = page.goto(BASE + '/' + path, wait_until='load')
                    require(response is not None and response.status == 200, f'Page not HTTP 200: {path}')
                    settle()
                def map_ready():
                    page.wait_for_function('''() => window.P4A_CIVIC_MAP?.getState().shapes > 0 &&
                        document.querySelector('[data-civic-map]').getAttribute('aria-busy') === 'false' ''')
                    expect(page.locator('[data-civic-map] canvas')).to_be_visible()
                for i, entry in enumerate(scope['pages']):
                    def inspect(entry=entry, i=i):
                        goto(entry['path'])
                        if page.locator('[data-civic-map]').count():
                            map_ready()
                        for text in entry.get('expected_text', []):
                            expect(page.locator('body')).to_contain_text(text)
                        for text in entry.get('absent_text', []):
                            expect(page.locator('body')).not_to_contain_text(text)
                        for selector in entry.get('visible', []):
                            nodes = page.locator(selector)
                            require(nodes.count() > 0, f'No nodes: {selector}')
                            for node in nodes.all():
                                expect(node).to_be_visible()
                        screenshot(f'page-{i}')
                        layout()
                    check('page: ' + entry['path'], inspect)
                for i, journey in enumerate(scope.get('map_journeys', [])):
                    def navigate(j=journey, i=i):
                        goto(j['start'])
                        page.locator(j['entry_selector']).click()
                        page.wait_for_url(BASE + '/' + j['map_path'] + '**')
                        map_ready()
                        page.locator('[data-civic-layer]').select_option(j['layer'])
                        map_ready()
                        page.locator('[data-civic-search]').fill(j['search'])
                        button = page.locator('[data-civic-results] button').filter(has_text=j['search'])
                        expect(button).to_have_count(1)
                        button.click()
                        expect(button).to_have_attribute('aria-pressed', 'true')
                        page.wait_for_function('(area) => window.P4A_CIVIC_MAP.getState().selected === area', arg=j['area'])
                        expect(page.locator('[data-civic-selection-name]')).to_have_text(j['search'])
                        settle(); screenshot(f'journey-{i}-selected'); layout()
                        selected_url = page.url
                        page.locator('[data-civic-open]').click()
                        page.wait_for_url(BASE + '/' + j['destination'] + '**')
                        settle(); screenshot(f'journey-{i}-open'); layout()
                        destination_url = page.url
                        page.go_back(wait_until='load')
                        settle()
                        require(page.url == selected_url, 'Back did not return to selected map URL')
                        map_ready()
                        page.wait_for_function('(area) => window.P4A_CIVIC_MAP.getState().selected === area', arg=j['area'])
                        screenshot(f'journey-{i}-back'); layout()
                        page.go_forward(wait_until='load')
                        settle()
                        require(page.url == destination_url, 'Forward did not restore destination')
                    check(f'map search/select/Open/Back/Forward: {i}', navigate)
                for clock_index, path in enumerate(scope.get('redland_clock_pages', [])):
                    def clocks(path=path, clock_index=clock_index):
                        goto(path)
                        observed = observe_clock_panels(page)
                        # Capture visual evidence before the oracle import can initialize panels.
                        screenshot(f'redland-clock-{clock_index}'); layout()
                        result = compare_clock_observation(page, observed)
                        report.setdefault('delivered_clocks', []).append({'viewport': viewport, 'path': path, 'panels': result})
                    check('Redland delivered clock: ' + path, clocks)
                def network_check():
                    bad = [r for r in responses if r['status'] >= 400]
                    require(not bad, f'Local HTTP failures: {bad}')
                    require(not network_errors, f'Local request failures: {network_errors}')
                    require(not page_errors, f'Browser JavaScript errors: {page_errors}')
                    require(not any(b['method'] not in ('GET', 'HEAD') for b in blocked), 'Attempted non-read request')
                check('local HTTP, JavaScript and read-only safety', network_check)
                report.setdefault('observed_http_responses', []).append({'viewport': viewport, 'responses': responses})
                report.setdefault('blocked_external_requests', []).append({'viewport': viewport, 'requests': blocked})
                if any(c['status'] == 'FAIL' and c.get('viewport') == viewport for c in report['checks']):
                    context.tracing.stop(path=str(output / f'{width}-trace.zip'))
                else:
                    context.tracing.stop()
                context.close()
        finally:
            browser.close()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scope', type=Path, default=ROOT / 'tools/browser-qa/smoke-scope.json')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--validate-only', action='store_true')
    args = parser.parse_args(argv)
    scope = load_scope(ROOT, args.scope)
    if args.validate_only:
        print('Scope valid (browser not launched)')
        return 0
    output = output_directory(ROOT, args.output)
    report = {'schema_version': 1, 'scope': scope, 'started_utc': datetime.now(timezone.utc).isoformat(),
              'base_url': BASE, 'checks': [], 'screenshots': [], 'loaded_repository_files_sha256': {},
              'loaded_file_hash_basis': 'Repository files mapped from successful local HTTP requests. These are not transport response-body hashes. The clean unchanged checkout and recorded preview-server script bind the source files to this run.'}
    try:
        report['provenance'] = provenance(ROOT, args.scope, scope)
        require(not report['provenance']['working_tree_status'], 'Refusing exact-commit acceptance from a dirty working tree')
        run(scope, report, output)
        after = provenance(ROOT, args.scope, scope)
        require(after == report['provenance'], 'Checkout or provenance inputs changed during browser run')
    except Exception as exc:
        report['checks'].append({'name': 'runner', 'status': 'FAIL', 'error': str(exc)})
    return finish(report, output)


if __name__ == '__main__':
    sys.exit(main())
