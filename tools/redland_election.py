"""Render only sourced Redland election news, process and confirmed milestones."""
from datetime import date, datetime, timedelta
from html import escape
import re

WAITING = 'Awaiting confirmation to begin'
START = '<!-- redland-election:start -->'
END = '<!-- redland-election:end -->'


def validate(election):
    assert election['timezone'] == 'Australia/Brisbane'
    bye = election['byElection']
    for item in (bye, bye['nominationDeadline']):
        date.fromisoformat(item['checked'])
        assert item['timingStatus'] in ('awaiting-confirmation', 'confirmed', 'cancelled', 'completed')
        if item['timingStatus'] == 'confirmed':
            day = date.fromisoformat(item['date'])
            target = datetime.fromisoformat(item['countdownTarget'])
            assert re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+10:00', item['countdownTarget'])
            assert target.date() == day and target.utcoffset() == timedelta(hours=10)
            assert item['source'].startswith('https://www.ecq.qld.gov.au/')
            assert item['dateBasis'].strip()
            if item.get('timePrecision') == 'calendar-day':
                assert target.hour == target.minute == target.second == 0
        elif item['timingStatus'] == 'awaiting-confirmation':
            assert item['date'] is None and item['countdownTarget'] is None
    candidates = bye.get('candidates', [])
    assert len({c['id'] for c in candidates}) == len(candidates)
    for candidate in candidates:
        assert candidate['status'] in ('announced-intention', 'accepted-nomination', 'withdrawn')
        assert candidate['source'].startswith('https://')
        date.fromisoformat(candidate['checked'])
        if candidate.get('announced'):
            date.fromisoformat(candidate['announced'])
        else:
            assert candidate.get('sourceType') == 'media-report'
            date.fromisoformat(candidate['reported'])
        if candidate['status'] == 'accepted-nomination':
            assert (candidate.get('nominationSource') or '').startswith('https://www.ecq.qld.gov.au/')
        elif candidate['status'] == 'announced-intention':
            assert candidate['nominationStatus'] == 'not-verified'
    if bye.get('pollEndsAt'):
        end = datetime.fromisoformat(bye['pollEndsAt'])
        start = datetime.fromisoformat(bye['countdownTarget'])
        assert end > start and end.utcoffset() == timedelta(hours=10)


def milestone(item, title, kind):
    e = lambda value: escape(str(value), quote=True)
    state = item['timingStatus']
    target = item.get('countdownTarget') or ''
    waiting = WAITING if state == 'awaiting-confirmation' else (
        'Cancelled — check the official ECQ notice.' if state == 'cancelled' else
        'Event completed — check the official ECQ status.' if state == 'completed' else
        'Official date confirmed. Live countdown requires JavaScript.')
    confirmed = state == 'confirmed'
    calendar_day = item.get('timePrecision') == 'calendar-day'
    date_html = ''
    if confirmed:
        readable = datetime.fromisoformat(target).strftime('%d %B %Y' if calendar_day else '%d %B %Y, %H:%M').lstrip('0')
        date_html = f'<p><time datetime="{e(item["date"] if calendar_day else target)}" style="white-space:normal">{e(readable)} AEST (Brisbane, UTC+10)</time></p>'
        if calendar_day:
            date_html += '<p>Countdown to the start of this Brisbane calendar date, not a polling opening time or postal deadline.</p>'
    units = ''.join(f'<span><strong>--</strong>{unit}</span>' for unit in ['days', 'hours', 'minutes', 'seconds'])
    return f'''<article class="local-card" data-redland-milestone data-kind="{e(kind)}" data-time-precision="{e(item.get('timePrecision', 'instant'))}" data-timing-status="{e(state)}" data-target="{e(target)}" data-ends="{e(item.get('pollEndsAt') or '')}">
<h3>{e(title)}</h3>{date_html}<p data-milestone-status role="status">{e(waiting)}</p>
<div class="local-clock" data-milestone-clock role="timer" aria-label="{e(title)} countdown" hidden>{units}</div>
<p class="local-source"><a href="{e(item['source'])}" target="_blank" rel="noopener noreferrer">Official ECQ timetable and updates</a></p></article>'''



def candidate_announcements(page, bye, link):
    candidates = bye.get('candidates', [])
    if not candidates:
        return ''
    rows = ''.join(f'<article class="local-card" data-candidate-status="{escape(c["status"])}"><h3>{escape(c["name"])}</h3><p><strong>{escape(c["statusLabel"])}</strong></p><p>{escape(c["summary"])}</p><p class="local-source">{escape(('Announced ' + c['announced']) if c.get('announced') else ('Reported ' + c['reported']))} · Checked {escape(c["checked"])} · AEST (Brisbane, UTC+10). {link(page,c["source"],c.get("sourceLabel", "Read the primary announcement"))}</p></article>' for c in candidates)
    return '<div id="redland-candidate-announcements"><h3>Candidate announcements and nominations</h3><p>' + escape(bye['candidateCoverage']) + '</p><div class="local-grid">' + rows + '</div><p>Announcing an intention to run is separate from lodging a formal nomination and ECQ accepting it. No formal nomination status is inferred from social media or news reporting.</p></div>'


def render(page, election, link):
    validate(election)
    bye = election['byElection']; vacancy = bye['vacancy']
    sources = {s['id']: s['url'] for s in bye['sources']}
    l = lambda key, label: link(page, sources[key], label)
    proposal = bye.get('postalVoting') or bye.get('postalVotingProposal')
    proposal_html = (f"<p>{escape(proposal['summary'])} {link(page, proposal['source'], 'Read the official postal-ballot update')}.</p>" if proposal else '')
    general = election['general']
    units = ''.join(f'<span><strong>--</strong>{unit}</span>' for unit in ['days', 'hours', 'minutes', 'seconds'])
    checked = date.fromisoformat(bye['checked']).strftime('%d %B %Y').lstrip('0')
    timing_copy = (f'At the {checked} check, ECQ’s election-events page did not list a Redland polling date or nomination deadline.'
                   if all(item['timingStatus'] == 'awaiting-confirmation' for item in (bye, bye['nominationDeadline']))
                   else f'Timetable checked {checked}. The panels show the separately verified status of each milestone.')
    return START + f'''
<section class="local-panel accent" id="redland-mayoral-update" aria-labelledby="election-title">
<p class="local-kicker">Redlands mayoral update · Checked {escape(bye['checked'])} · Australia/Brisbane</p>
<h2 id="election-title">Mayoral by-election: 12 December 2026, full postal ballot.</h2>
<p>Redland City Council confirms it received Jos Mitchell’s resignation on <time datetime="{escape(vacancy['date'])}">28 October 2026</time>. The mayoral office is vacant. Julie Talty continues as Acting Mayor during the election period. {l('rcc-mayoral-vacancy-20261028', 'Read Council’s announcement')}.</p>
{proposal_html}
<p>ECQ says the notice of election will be issued and candidate nominations will open on <time datetime="2026-11-10">10 November 2026</time>. The nomination closing date and postal deadlines have not been verified. {link(page, bye["source"], "Read ECQ’s 5 November announcement")}.</p>
<p>{escape(timing_copy)} Check {l('ecq-events-20261028', 'ECQ’s election-events page')}. Each panel uses its own verified milestone. The election-day countdown is to the start of the calendar date; the nomination-deadline panel remains inactive.</p>
<div class="local-grid two">{milestone(bye, 'Election day: full postal ballot', 'poll')}{milestone(bye['nominationDeadline'], 'Candidate nomination deadline', 'nominations')}</div>
<p class="local-source">All times are Brisbane time (AEST, UTC+10). Check ECQ for enrolment, ballot packs, postal deadlines and any changed notice. A full postal ballot does not imply ordinary in-person polling hours.</p>
{candidate_announcements(page, bye, link)}
<details><summary>How the replacement process works</summary>
<ol class="local-list"><li><strong>A vacancy, then an election.</strong> A mayoral vacancy in the beginning or middle of a council term is filled by a by-election. In the final part it is filled by appointing a sitting councillor. The final part of this term begins on 16 March 2027, the third anniversary of the 2024 election; the 28 October 2026 vacancy is earlier. The deputy mayor acts during the vacancy. {l('qld-local-government-act', 'Local Government Act 2009, ss 161, 164–165')}.</li>
<li><strong>Wait for the official notice.</strong> The returning officer fixes the by-election day. The ordinary rule is within two months of the vacancy; this is not a confirmed event date. The notice sets a nomination day 8–18 calendar days after publication and 18–42 days before polling. {l('qld-local-government-electoral-act', 'Local Government Electoral Act 2011, ss 24–25')}.</li>
<li><strong>Nominations come before voting.</strong> Nominations must reach the returning officer before noon on the official nomination day (s 27). Eligibility, required training, nomination, campaign accounts and disclosure obligations are explained in the {l('ecq-candidate-guidance', 'ECQ candidate guide')}. Considering standing, announcing an intention and an accepted nomination are different stages.</li>
<li><strong>Check the result.</strong> Follow ECQ’s nomination, voting, count and declaration notices. A countdown reaching its target does not establish that polling occurred or somebody was elected. Council says the elected mayor will serve until the next local elections in 2028.</li></ol></details>
<details><summary>Ordinary 2028 election and earlier records</summary><p>The separate ordinary council cycle remains {escape(general['date'])}, derived from ECQ’s calendar rule and subject to regulation and the official timetable. Its original check date is {escape(general['checked'])}; it is not this by-election’s polling date.</p><p class="local-clock" data-ordinary-election-status>{WAITING}</p><p>The ordinary-cycle date is indicative only. No countdown begins until an official election date is confirmed.</p><p>{link(page, 'content/local/redland-election.json', 'Current election data and source checks')} · {link(page, 'content/local/history/redland-election-2026-10-16.json', 'Earlier conditional snapshot, 16 October 2026')}</p></details>
</section>
''' + END


def apply_block(text, page, election, link, overview=False):
    block = render(page, election, link)
    if START in text:
        match = re.search(re.escape(START) + r'[\s\S]*?' + re.escape(END), text)
    else:
        legacy = r'<section class="local-panel accent" aria-labelledby="election-title">[\s\S]*?</noscript></section>'
        match = re.search(legacy, text)
    if not match:
        raise ValueError('Existing election section not found: ' + page)
    if overview:
        text = text[:match.start()] + text[match.end():]
        nav = re.search(r'<nav class="local-nav"[\s\S]*?</nav>', text)
        if not nav: raise ValueError('Local navigation missing')
        return text[:nav.end()] + block + text[nav.end():]
    return text[:match.start()] + block + text[match.end():]


def sources_section(page, election, link):
    bye = election['byElection']
    rows = ''.join('<li>' + link(page, s['url'], s['title']) + ' — checked ' + escape(s['checked']) + '</li>' for s in bye['sources'])
    return f'<section class="local-panel" id="redland-election-sources"><h2>Mayoral by-election: dates, announcements and sources</h2><p>Council confirms the vacancy and acting arrangement. ECQ’s 5 November announcement confirms the 12 December full postal by-election and 10 November nominations opening. Candidate intentions are labelled by source; they are not accepted nominations.</p><ul class="local-list">{rows}</ul><p>{link(page, "states/qld/councils/redland/index.html#redland-mayoral-update", "Current news and countdown status")} · {link(page, "content/local/redland-election.json", "Canonical timing data")} · {link(page, "content/local/history/redland-election-2026-10-16.json", "Earlier conditional snapshot")}</p></section>'


def apply_page(page, text, election, link):
    base = 'states/qld/councils/redland/'
    if page in (base + 'index.html', base + 'candidates/index.html'):
        text = apply_block(text, page, election, link, overview=page == base + 'index.html')
        if 'assets/redland-election-clock.mjs' not in text:
            # Existing link helper gives the correct relative path at either depth.
            from pathlib import PurePosixPath
            prefix = '../' * (len(PurePosixPath(page).parts) - 1)
            text = text.replace('</body>', f'<script type="module" src="{prefix}assets/redland-election-clock.mjs?v=20261108"></script></body>')
    elif page == base + 'sources/index.html':
        section = sources_section(page, election, link)
        if 'id="redland-election-sources"' in text:
            text = re.sub(r'<section class="local-panel" id="redland-election-sources">[\s\S]*?</section>', lambda _: section, text, count=1)
        else:
            anchor = '<section id="statistics">'
            if anchor not in text: raise ValueError('Source page statistics anchor missing')
            text = text.replace(anchor, section + anchor, 1)
    else:
        return text
    text = text.replace('redland-election-clock.mjs?v=20261028', 'redland-election-clock.mjs?v=20261108')
    if page == base + 'candidates/index.html':
        text = text.replace('If a mayoral by-election is called.', 'Following the confirmed mayoral vacancy.')
        text = text.replace('Begin with an official vacancy and election notice, then use the current ECQ candidate guidance. A possible by-election is a branch in this journey; it does not need to happen for local work to continue.', 'Council has confirmed the vacancy and a by-election is required. Follow the official ECQ notice and current candidate guidance. Community work can also continue outside office.')
    from page_review_register import reviewed_page_entries
    stamp = max(election['changed'], next((row['lastUpdated'] for row in reviewed_page_entries() if row['path'] == page), election['changed']))
    readable = date.fromisoformat(stamp).strftime('%d %B %Y').lstrip('0')
    text = re.sub(r'(<div class="local-stamp"><span>Started 16 October[^<]*Updated )<time[^>]*>[^<]*</time>', lambda m: m[1] + f'<time datetime="{stamp}">{readable}</time>', text, count=1)
    return text

