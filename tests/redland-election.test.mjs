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
