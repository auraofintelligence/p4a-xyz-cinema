import {test} from 'node:test';
import assert from 'node:assert/strict';
import {milestoneState} from '../assets/redland-election-clock.mjs';

test('unconfirmed, missing, date-only and wrong-offset dates never start a timer', () => {
  for (const item of [{status:'awaiting-confirmation'}, {status:'confirmed'}, {status:'confirmed',target:'2026-11-01'}, {status:'confirmed',target:'2026-11-01T08:00:00+11:00'}]) {
    assert.deepEqual(milestoneState(item), {text:'Awaiting confirmation to begin', active:false});
  }
});
test('synthetic nomination cutoff uses Brisbane time and closes at the exact instant', () => {
  const item = {status:'confirmed',kind:'nominations',target:'2026-11-02T12:00:00+10:00'};
  assert.deepEqual(milestoneState(item, Date.parse('2026-11-01T12:00:00+10:00')).values, [1,0,0,0]);
  assert.deepEqual(milestoneState(item, Date.parse('2026-11-02T01:59:59Z')).values, [0,0,0,1]);
  for (const now of ['2026-11-02T02:00:00Z','2026-11-03T00:00:00Z']) {
    const state = milestoneState(item, Date.parse(now)); assert.equal(state.active,false); assert.match(state.text,/Nominations closed/);
  }
});
test('synthetic poll changes status at opening/close and never declares a result', () => {
  const item = {status:'confirmed',kind:'poll',target:'2026-11-14T08:00:00+10:00',ends:'2026-11-14T18:00:00+10:00'};
  assert.equal(milestoneState(item, Date.parse('2026-11-13T21:59:59Z')).active,true);
  assert.match(milestoneState(item, Date.parse('2026-11-13T22:00:00Z')).text,/Check ECQ/);
  assert.match(milestoneState(item, Date.parse('2026-11-14T08:00:00Z')).text,/hours have ended/);
  assert.equal(milestoneState({...item,status:'cancelled'}).active,false);
  assert.equal(milestoneState({...item,status:'completed'}).active,false);
});

test('candidate presentation keeps requested order and public links separate from nomination status', async () => {
  const {readFile} = await import('node:fs/promises');
  const data = JSON.parse(await readFile(new URL('../content/local/redland-election.json', import.meta.url), 'utf8'));
  const {candidates, officialCandidateSearch} = data.byElection;
  const originalOrder = ['jasmine-person','julie-talty','rowanne-mckenzie','don-brown','gary-williamson'];
  assert.deepEqual(candidates.filter(c => originalOrder.includes(c.id)).map(c => c.id), originalOrder);
  for (const c of candidates) {
    if (c.status === 'announced-intention') assert.equal(c.nominationStatus, 'not-verified');
    if (c.status === 'accepted-nomination') {
      assert.equal(c.nominationStatus, 'accepted');
      assert.equal(c.nominationSource, officialCandidateSearch.url);
      assert.match(c.nominationChecked, /^\d{4}-\d{2}-\d{2}$/);
    }
  }
  const publicLinks = id => candidates.find(c => c.id === id).publicLinks;
  assert.equal(publicLinks('jasmine-person')[0].url, 'https://jasmineformayor.au/');
  assert.equal(publicLinks('julie-talty')[1].url, 'https://julietalty.au/');
  assert.match(publicLinks('julie-talty')[0].url, /redland\.qld\.gov\.au\/.+Division-6/);
  assert.match(publicLinks('rowanne-mckenzie')[0].url, /redland\.qld\.gov\.au\/.+Division-7/);
  for (const route of ['index.html','candidates/index.html']) {
    const html = await readFile(new URL('../states/qld/councils/redland/' + route, import.meta.url), 'utf8');
    let previous = -1;
    for (const c of candidates) { const i=html.indexOf('<h3>'+c.name+'</h3>'); assert.ok(i>previous); previous=i; }
    for (const c of candidates) for (const item of c.publicLinks || []) assert.ok(html.includes(item.url));
  }
});

test('official deadline, exact AEST expiry and certified-candidate link stay distinct from announcements', async () => {
  const {readFile} = await import('node:fs/promises');
  const data = JSON.parse(await readFile(new URL('../content/local/redland-election.json', import.meta.url), 'utf8'));
  const d = data.byElection.nominationDeadline;
  assert.equal(d.countdownTarget, '2026-11-19T12:00:00+10:00');
  assert.equal(d.timingStatus, 'confirmed');
  assert.equal(data.byElection.nominationsOpen.countdownTarget, undefined);
  const item = {status:d.timingStatus,kind:'nominations',target:d.countdownTarget};
  assert.deepEqual(milestoneState(item, Date.parse('2026-11-19T01:59:59Z')).values, [0,0,0,1]);
  for (const now of ['2026-11-19T02:00:00Z', '2026-11-20T00:00:00Z']) {
    const state = milestoneState(item, Date.parse(now)); assert.equal(state.active, false); assert.match(state.text, /Nominations closed/);
  }
  assert.equal(data.byElection.officialCandidateSearch.url, 'https://event.elections.qld.gov.au/Events/VoteCardsView?EventID=653&EventType=8');
  for (const route of ['index.html', 'candidates/index.html']) {
    const html = await readFile(new URL('../states/qld/councils/redland/' + route, import.meta.url), 'utf8');
    assert.match(html, /data-kind="nominations"[^>]*data-timing-status="confirmed"[^>]*data-target="2026-11-19T12:00:00\+10:00"/);
    assert.ok(html.includes('12 noon AEST on Thursday 19 November 2026'));
    assert.ok(html.includes('No opening clock time is stated.'));
    assert.ok(html.includes('Check ECQ’s certified candidates'));
    assert.ok(html.includes('certification by the Returning Officer'));
    assert.ok(!html.includes('nomination-deadline panel remains inactive'));
  }
});
