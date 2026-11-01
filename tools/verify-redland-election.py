"""Read-only checks for the sourced Redlands news/timing update; no live source claim."""
from pathlib import Path
from html.parser import HTMLParser
import importlib.util
import json
from copy import deepcopy
from html import escape
from redland_election import apply_page, candidate_announcements, validate, WAITING

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('redland_builder', ROOT / 'tools/build-redland.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)
data = builder.read('content/local/redland-election.json')
validate(data)
assert builder.read('content/local/history/redland-election-2026-10-16.json')['byElection']['date'] is None
assert data['byElection']['vacancy']['date'] == '2026-10-28'
assert data['general']['date'] == '2028-03-25'

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.ids=[]; self.panels=[]; self.feed(text)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'): self.ids.append(a['id'])
        if 'data-redland-milestone' in a: self.panels.append(a)

for suffix in ['index.html', 'candidates/index.html', 'sources/index.html']:
    page = builder.BASE + suffix
    text = (ROOT / page).read_text(encoding='utf-8'); parsed = Page(text)
    assert len(parsed.ids) == len(set(parsed.ids)), page
    assert apply_page(page, text, data, builder.link) == text, ('non-idempotent section build', page)
    assert 'Council confirms' in text or 'Council confirms mayoral' in text or 'Council confirms the vacancy' in text
    assert '2026-10-28' in text
    if suffix != 'sources/index.html':
        candidates = data['byElection'].get('candidates', [])
        assert text.count('data-candidate-status=') == len(candidates), page
        for candidate in candidates:
            assert f'data-candidate-status="{candidate["status"]}"' in text
            assert escape(candidate['name']) in text
            assert escape(candidate['statusLabel']) in text
            assert escape(candidate['source'], quote=True) in text
            assert candidate['sourceId'] in {s['id'] for s in data['byElection']['sources']}
        assert len(parsed.panels) == 2
        assert 'Jos Mitchell' in text and 'Julie Talty' in text
        assert text.count('assets/redland-election-clock.mjs') == 1
        for panel in parsed.panels:
            if panel['data-timing-status'] == 'awaiting-confirmation':
                assert not panel['data-target']
        if all(p['data-timing-status'] == 'awaiting-confirmation' for p in parsed.panels):
            assert text.count(WAITING) == 2
        assert '28 December 2026' not in text, 'Do not turn a statutory interval into an announced polling date'
        assert 'Possible mayoral by-election:' not in text

# Synthetic fixtures stay offline and never enter published candidate data.
empty = deepcopy(data['byElection']); empty.pop('candidates', None)
assert candidate_announcements('fixture.html', empty, builder.link) == ''
if data['byElection'].get('candidates'):
    fixture = deepcopy(data)
    fixture['byElection']['candidates'][0]['name'] = '<script>alert("fixture")</script>'
    rendered = candidate_announcements('fixture.html', fixture['byElection'], builder.link)
    assert '<script>alert' not in rendered and '&lt;script&gt;' in rendered
    fixture['byElection']['candidates'].append(deepcopy(fixture['byElection']['candidates'][0]))
    try:
        validate(fixture)
    except AssertionError:
        pass
    else:
        raise AssertionError('Duplicate candidate IDs were accepted')
    fixture = deepcopy(data)
    fixture['byElection']['candidates'][0]['status'] = 'accepted-nomination'
    fixture['byElection']['candidates'][0]['nominationSource'] = 'https://www.facebook.com/example'
    try:
        validate(fixture)
    except AssertionError:
        pass
    else:
        raise AssertionError('Accepted nomination without ECQ evidence was accepted')
print(json.dumps({'result':'PASS','pages':3,'milestonePanels':4,'checks':'Canonical status, source links, unique IDs, scoped-render parity/idempotence and inactive unconfirmed targets. Browser layout and live source verification remain separate.'},indent=2))
