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


class CandidateGroups(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.groups = {}
        self.active_group = None
        self.active_card = None
        self.in_name = False
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        group_id = attributes.get('id')
        if group_id in (
            'redland-current-candidates',
            'redland-unverified-candidate-announcements',
            'redland-earlier-candidate-records',
        ):
            self.active_group = group_id
            self.groups[group_id] = {'attributes': attributes, 'cards': [], 'text': ''}
        if 'data-candidate-status' in attributes:
            assert self.active_group, 'Candidate card has no presentation group'
            self.active_card = {'status': attributes['data-candidate-status'], 'name': ''}
            self.groups[self.active_group]['cards'].append(self.active_card)
        if tag == 'h3' and self.active_card is not None:
            self.in_name = True

    def handle_endtag(self, tag):
        if tag == 'h3':
            self.in_name = False
        if tag == 'article':
            self.active_card = None
        if tag in ('section', 'details'):
            self.active_group = None

    def handle_data(self, value):
        if self.active_group:
            self.groups[self.active_group]['text'] += value
        if self.in_name:
            self.active_card['name'] += value


def check_candidate_groups(text, candidates):
    groups = CandidateGroups(text).groups
    current = [candidate for candidate in candidates if candidate['status'] == 'accepted-nomination']
    awaiting = [candidate for candidate in candidates if candidate['status'] == 'announced-intention']
    earlier = [candidate for candidate in candidates if candidate['status'] in ('previously-certified', 'withdrawn')]
    expected_groups = (
        ('redland-current-candidates', current),
        ('redland-unverified-candidate-announcements', awaiting),
        ('redland-earlier-candidate-records', earlier),
    )
    for group_id, expected in expected_groups:
        if not expected and group_id != 'redland-current-candidates':
            assert group_id not in groups, ('Empty candidate group', group_id)
            continue
        group = groups[group_id]
        assert group['cards'] == [{'status': candidate['status'], 'name': candidate['name']} for candidate in expected], group_id
    label = 'candidate' if len(current) == 1 else 'candidates'
    assert f'{len(current)} ECQ-certified {label}' in groups['redland-current-candidates']['text']
    if earlier:
        group = groups['redland-earlier-candidate-records']
        assert 'open' not in group['attributes'], 'Earlier records must start collapsed'
        assert 'excluded from the current ECQ-certified candidate list' in group['text']


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
        check_candidate_groups(text, candidates)
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
            assert text.count(WAITING) == 3
        assert '28 December 2026' not in text, 'Do not turn a statutory interval into an announced polling date'
        assert 'Possible mayoral by-election:' not in text

# Synthetic fixtures stay offline and never enter published candidate data.
empty = deepcopy(data['byElection']); empty.pop('candidates', None)
assert candidate_announcements('fixture.html', empty, builder.link) == ''
if data['byElection'].get('candidates'):
    fixture = deepcopy(data['byElection'])
    fixture['candidateCoverage'] = 'Synthetic status-grouping fixture.'
    fixture['candidates'] = []
    for status, name in (
        ('withdrawn', 'Withdrawn fixture'),
        ('announced-intention', 'Awaiting fixture'),
        ('accepted-nomination', 'Certified fixture'),
        ('previously-certified', 'Earlier fixture'),
    ):
        candidate = deepcopy(data['byElection']['candidates'][0])
        candidate.update({'id': status + '-fixture', 'name': name, 'status': status, 'summary': name})
        candidate['statusLabel'] = status
        candidate['currentListingChecked'] = '2026-11-20'
        fixture['candidates'].append(candidate)
    check_candidate_groups(candidate_announcements('fixture.html', fixture, builder.link), fixture['candidates'])
    fixture['candidates'] = [candidate for candidate in fixture['candidates'] if candidate['status'] != 'accepted-nomination']
    check_candidate_groups(candidate_announcements('fixture.html', fixture, builder.link), fixture['candidates'])
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
