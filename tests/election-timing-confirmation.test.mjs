import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const root = new URL('../', import.meta.url);
const read = path => fs.readFileSync(new URL(path, root), 'utf8');
const calendarContext = {Intl, Date, Number, String, JSON};
vm.runInNewContext(read('assets/state-election-calendar.js'), calendarContext);
const calendar = calendarContext.P4A_ELECTION_CALENDAR;
for (const slug of ['qld','wa','sa','nt']) {
  const row = calendar.data.elections.find(row => row.slug === slug);
  assert.equal(row.date, null);
  assert.match(row.indicativeDate, /^\d{4}-\d{2}-\d{2}$/);
  assert.equal(calendar.status(row, new Date('2026-11-02T00:00:00Z')).text, 'Awaiting confirmation to begin');
}
for (const slug of ['vic','nsw','act']) {
  const row = calendar.data.elections.find(row => row.slug === slug);
  assert.equal(calendar.status(row, new Date('2026-11-02T00:00:00Z')).phase, 'future');
}
const civicContext = {window:{},document:{querySelectorAll:()=>[],querySelector:()=>null},Intl,Date,Number,String,JSON};
vm.runInNewContext(read('assets/civic-places.js'), civicContext);
assert.equal(civicContext.window.P4A_CIVIC_CLOCK.clockLabel({date:'2028-03-25',timingStatus:'awaiting-confirmation'}), 'Awaiting confirmation to begin');
assert.equal(civicContext.window.P4A_CIVIC_CLOCK.clockLabel({date:null}), 'Awaiting confirmation to begin');
// Exercise the actual delivered state-card date arithmetic with controlled time.
const source = read('script.js');
const start = source.indexOf('  const dayMs = 86400000;', source.indexOf('const countdowns'));
const end = source.indexOf('  const updateCardState', start);
function cardTime(instant, values) {
  class FixedDate extends Date { static now() { return Date.parse(instant); } }
  const context = {Date:FixedDate,Intl,Number,Math};
  vm.runInNewContext(source.slice(start,end)+'\nthis.cardTime = getCardTime;', context);
  return context.cardTime({getAttribute:name=>values[name]||null,querySelector:()=>null});
}
const act = {'data-election-date':'2028-10-21','data-state':'act','data-election-timezone':'Australia/Sydney','data-election-precision':'day'};
assert.equal(cardTime('2028-10-20T12:59:59Z',act).calendarDays,1);
assert.equal(cardTime('2028-10-20T13:00:00Z',act).calendarDays,0);
assert.equal(cardTime('2028-10-21T13:00:00Z',act).calendarDays,-1);
assert.equal(cardTime('2028-10-20T13:00:00Z',act).dateOnly,true);
assert.equal(cardTime('2026-11-02T00:00:00Z',{...act,'data-timing-status':'awaiting-confirmation'}).state,'waiting');
const instant = cardTime('2026-12-03T09:59:00Z',{'data-election-date':'2026-12-03T18:00:00+08:00','data-state':'wa'});
assert.equal(instant.diff,60000);
assert.equal(cardTime('2026-12-03T10:01:00Z',{'data-election-date':'2026-12-03T18:00:00+08:00','data-state':'wa'}).state,'past');
let pending = 0;
for (const scope of ['councils','state']) {
 for (const place of JSON.parse(read(`content/places/${scope}.json`)).places) {
  for (const event of place.elections || []) {
   if (event.indicativeDate) {
    pending++;
    assert.equal(event.date,null,event.id);
    assert.equal(event.timingStatus,'awaiting-confirmation',event.id);
    assert.equal(event.waitingLabel,'Awaiting confirmation to begin',event.id);
   }
  }
 }
}
assert.equal(pending,489);
const redland=JSON.parse(read('content/local/redland-election.json'));
assert.equal(redland.general.countdownTarget,null);
assert.equal(redland.general.date,'2028-03-25');
assert.equal(redland.general.timingStatus,'awaiting-confirmation');
console.log('PASS: 489 indicative national events, four state-calendar waiting dates, confirmed dates, date-only DST boundaries, exact deadline expiry and Redland ordinary waiting.');
const vicTemplate = read('tools/templates/vic-election.html');
assert.ok(vicTemplate.includes('<strong data-election-days>28 Nov</strong>'));
const vicSource = read('assets/vic-election.js');
const vicStart = vicSource.indexOf(' function updateElectionDays()');
const vicEnd = vicSource.indexOf('\n updateElectionDays();',vicStart);
for (const [now,number,label] of [['2026-11-27T12:59:59Z',1,'calendar days to polling day'],['2026-11-27T13:00:00Z',0,'Election day today'],['2026-11-28T13:00:00Z',1,'calendar days since polling day']]) {
 class FixedDate extends Date {constructor(...args){super(...(args.length?args:[now]));}}
 const nodes = {'[data-election-days]':{},'[data-election-day-label]':{}};
 const ctx = {Date:FixedDate,Intl,Math,Object,data:{pollingDate:'2026-11-28'},document:{querySelector:q=>nodes[q]}};
 vm.runInNewContext(vicSource.slice(vicStart,vicEnd)+'\nupdateElectionDays();',ctx);
 assert.equal(nodes['[data-election-days]'].textContent,number);
 assert.equal(nodes['[data-election-day-label]'].textContent,label);
}
console.log('PASS: Victoria neutral no-JavaScript fallback and before/on/after polling-day labels.');
const qldSupplement = JSON.parse(read('content/places/state-qld-details.json'));
let qldRuleCount = 0;
for (const place of qldSupplement.places) for (const event of place.elections) {
  if (event.indicativeDate === '2028-10-28') {
    qldRuleCount++;
    assert.equal(event.date, null);
    assert.equal(event.timingStatus, 'awaiting-confirmation');
    assert.equal(event.waitingLabel, 'Awaiting confirmation to begin');
  }
}
assert.equal(qldRuleCount, 93);
assert.ok(!read('tools/acquire-council-places.py').includes("date='2028-03-25',status='scheduled'"));
assert.ok(!read('tools/acquire-qld-state-details.py').includes("'date': '2028-10-28'"));
console.log('PASS: QLD supplementary records and acquisition paths preserve waiting clocks.');
// Null dates without explicit timingStatus must initialize their metric labels too.
assert.ok(source.includes("querySelectorAll('[data-countdown], [data-election-card] .countdown-value')"));
const metricsStart=source.indexOf('  const renderDayMetrics =');
const metricsEnd=source.indexOf('\n  const renderCountdown',metricsStart);
for (const [historical,expectedSince] of [['','Awaiting confirmation to begin'],['2026-11-01T08:00:00+10:00','1']]) {
 class FixedDate extends Date {static now(){return Date.parse('2026-11-02T00:00:00Z');}}
 const nodes=Object.fromEntries(['[data-days-until-wrap]','[data-days-since-wrap]','[data-days-until]','[data-days-since]'].map(k=>[k,{}]));
 const ctx={Date:FixedDate,Intl,Number,Math};
 vm.runInNewContext(source.slice(start,end)+source.slice(metricsStart,metricsEnd)+'\nthis.renderMetrics=renderDayMetrics;',ctx);
 ctx.renderMetrics({querySelector:q=>nodes[q],getAttribute:k=>({'data-days-since-date':historical,'data-election-timezone':'Australia/Brisbane'}[k]||null)},{invalid:true});
 assert.equal(nodes['[data-days-until]'].textContent,'Awaiting confirmation to begin');
 assert.equal(nodes['[data-days-since]'].textContent,expectedSince);
}
assert.equal(cardTime('2026-11-02T00:00:00Z',{'data-state':'tas'}).state,'waiting');
console.log('PASS: all null-date cards initialize waiting labels while retaining real historical days-since.');
