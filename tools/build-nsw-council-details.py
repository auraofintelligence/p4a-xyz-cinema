#!/usr/bin/env python3
"""Normalize retained NSW Legislative Council facts; never acquire or infer office.

Result HTML is retained by acquire-nsw-state-details.py --fetch --only lc-.
The current roster JSON is a minimal browser extraction of the official current
directory with its Council checkbox selected and all 41 displayed results read.
Full pages, redirect tokens, photographs and contact details stay excluded.
"""
from pathlib import Path
import hashlib
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'content/places/raw'
CHECKED = '2026-10-17'
PREFIX = 'state-nsw-supp-'
ROSTER_URL = 'https://www.parliament.nsw.gov.au/members-and-electorates/members-and-ministers/all-members?sort=metalastName&f.House%7ChouseName=Legislative+Council'
RESULT_URL = 'https://pastvtr.elections.nsw.gov.au/SG2301/LC/state/fp_by_grp_and_candidate'
CHECK_URL = 'https://pastvtr.elections.nsw.gov.au/SG2301/LC/state/cc/fp_summary'


def read(name):
    return (RAW / (PREFIX + name)).read_text(encoding='utf-8-sig')


def clean(value):
    return ' '.join(html.unescape(re.sub('<[^>]*>', ' ', value)).split())


def source(name, title, url):
    p = RAW / (PREFIX + name)
    return {'id': PREFIX + name.rsplit('.', 1)[0], 'title': title, 'url': url,
            'checked': CHECKED, 'rawFile': p.relative_to(ROOT).as_posix(),
            'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}


def ballot(name, url, final):
    text = read(name)
    assert 'Check Count Complete' in text
    rows = [[clean(c) for c in re.findall(r'<td\b[^>]*>(.*?)</td>', row, re.S | re.I)]
            for row in re.findall(r'<tr\b[^>]*>(.*?)</tr>', text, re.S | re.I)]
    width = 6 if final else 5
    vote_col = 3 if final else 2
    candidates, groups = [], []
    group = party = ''
    formal = None
    for cells in rows:
        if len(cells) != width:
            continue
        code, label = cells[:2]
        votes = int(cells[vote_col].replace(',', '') or '0')
        if label in ('Total Formal Votes', 'Formal Votes'):
            formal = votes
            continue
        if label in ('Informal Ballot Papers', 'Informal', 'Total Votes / Ballot Papers'):
            continue
        if label == 'UNGROUPED CANDIDATES':
            group, party = 'ungrouped', ''
            continue
        if code:
            group, party = code, label
            groups.append({'group': group, 'ballotLabel': party, 'aboveLineVotes': votes})
            continue
        if label == 'Group Total':
            assert groups and groups[-1]['group'] == group
            groups[-1]['totalVotes'] = votes
            continue
        assert label and group, cells
        candidate = {'name': label, 'party': party, 'ballotGroup': group,
                     'ballotOrder': len(candidates) + 1, 'votes': votes,
                     'voteMeasure': 'below-the-line first-preference votes',
                     'status': 'contested', 'sourceUrl': url}
        if final and cells[2]:
            candidate['result'] = 'Elected in position ' + cells[2] + ' in this 2023 contest'
        candidates.append(candidate)
    assert formal is not None
    assert len({c['name'] for c in candidates}) == len(candidates)
    for g in groups:
        assert g['aboveLineVotes'] + sum(c['votes'] for c in candidates if c['ballotGroup'] == g['group']) == g['totalVotes'], g
    assert sum(g['totalVotes'] for g in groups) + sum(c['votes'] for c in candidates if c['ballotGroup'] == 'ungrouped') == formal
    return candidates, groups, formal


def main():
    roster = json.loads(read('lc-current-roster.json'))
    assert roster['displayedResults'] == len(roster['records']) == 41
    assert len({r['profileUrl'] for r in roster['records']}) == 41
    roster_source = source('lc-current-roster.json', 'NSW Parliament: current Legislative Council directory factual extraction', ROSTER_URL)
    roster_source['extractionMethod'] = 'Browser rendered current-member directory, Council filter selected; all 41 listed cards read through normal scroll loading. Names, current chamber, displayed affiliation and canonical public profile links only.'
    roster_source['rightsScope'] = 'Minimal public professional facts and links; no full directory, portraits, contacts or biographies republished.'
    result_source = source('lc-results-2023.html', 'NSWEC: 2023 Legislative Council final first-preference group and candidate report', RESULT_URL)
    check_source = source('lc-check-2023.html', 'NSWEC: 2023 Legislative Council completed check-count summary', CHECK_URL)
    candidates, groups, formal = ballot('lc-results-2023.html', RESULT_URL, True)
    checks, check_groups, check_formal = ballot('lc-check-2023.html', CHECK_URL, False)
    assert [(c['name'], c['party'], c['votes']) for c in candidates] == [(c['name'], c['party'], c['votes']) for c in checks]
    assert groups == check_groups and formal == check_formal
    elected = [c for c in candidates if c.get('result')]
    assert len(elected) == 21
    representatives = []
    for r in roster['records']:
        assert r['house'] == 'Legislative Council' and r['name'] and r['party']
        assert re.fullmatch(r'https://www\.parliament\.nsw\.gov\.au/members-and-electorates/members-and-ministers/members-details\?memberId=\d+', r['profileUrl'])
        representatives.append({'name': r['name'], 'role': 'Member of the Legislative Council', 'party': r['party'],
                                'profileUrl': r['profileUrl'], 'sourceId': roster_source['id'], 'checked': CHECKED})
    notes = ['41 current members are listed by the filtered official directory checked 17 October 2026. The difference from the 42-seat chamber is unresolved roster coverage, not an invented member, vacancy reason or party balance.',
             'The 2023 contest elects 21 members. Individual candidate votes are below-the-line first preferences; above-the-line votes belong to groups and are not assigned to individual candidates.',
             'Current affiliations come from the current directory; historical affiliations retain the 2023 ballot group labels. Current office is never inferred from that election result.']
    event = {'id': 'nsw-lc-2023-SG2301', 'label': '2023 NSW Legislative Council election', 'kind': 'periodic upper-house election',
             'status': 'completed; official check count complete', 'date': '2023-03-25',
             'dateBasis': 'Official NSW Electoral Commission 2023 final count reports.', 'timezone': 'Australia/Sydney',
             'sourceUrl': 'https://pastvtr.elections.nsw.gov.au/SG2301/LC/results', 'resultsUrl': RESULT_URL,
             'sourceId': result_source['id'], 'candidates': candidates, 'formalVotes': formal, 'groupVotes': groups}
    output = {'schemaVersion': 1, 'checked': CHECKED, 'scope': 'nsw-council-supplement',
              'sources': [roster_source, result_source, check_source],
              'places': [{'name': 'New South Wales Legislative Council', 'kind': 'statewide-upper-house',
                          'representatives': representatives, 'elections': [event], 'coverageNotes': notes}]}
    (ROOT / 'content/places/state-nsw-lc-details.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    report = {'status': 'pass', 'checked': CHECKED, 'scope': 'NSW Council retained roster extraction and completed 2023 ballot reconciliation',
              'counts': {'currentDirectoryListings': len(representatives), '2023Contestants': len(candidates),
                         '2023ElectedPositions': len(elected), 'ballotGroups': len(groups), 'formalVotes': formal},
              'checks': ['41 distinct official roster cards/profile URLs reconcile to the displayed current Council result count.',
                         'Final report and completed check-count summary agree on every candidate name, group label and vote.',
                         'Each group total equals above-the-line plus individual below-the-line votes; all groups plus ungrouped sum to published formal votes.',
                         'Current roster and historical elected positions remain independent.'],
              'limitations': notes + ['Profile URLs were read from the directory; this does not assert successful HTTP access or a full individual profile review.',
                                      'Full retained originals are local-only. No browser acceptance of generated place pages is claimed by this data adapter.']}
    (ROOT / 'content/places/sources/state-nsw-lc-verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report['counts'], indent=2))


if __name__ == '__main__':
    main()
