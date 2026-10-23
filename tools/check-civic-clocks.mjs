/* Verify the delivered clock code at Australian local-calendar boundaries. */
import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const context={window:{},document:{querySelectorAll:()=>[],querySelector:()=>null},Intl,Date,Number,String,JSON};
vm.runInNewContext(fs.readFileSync(new URL('../assets/civic-places.js',import.meta.url),'utf8'),context);
const label=context.window.P4A_CIVIC_CLOCK.clockLabel;
const cases=[
 [{date:'2026-11-28',timezone:'Australia/Melbourne'},'2026-11-27T12:59:59Z','1 day to polling day'],
 [{date:'2026-11-28',timezone:'Australia/Melbourne'},'2026-11-27T13:00:00Z','Polling day'],
 [{date:'2026-11-28',timezone:'Australia/Melbourne'},'2026-11-28T13:00:00Z','1 day since polling day'],
 [{date:'2026-10-18',timezone:'Australia/Brisbane'},'2026-10-17T13:59:59Z','1 day to polling day'],
 [{date:'2026-10-18',timezone:'Australia/Brisbane'},'2026-10-17T14:00:00Z','Polling day'],
 [{date:'2026-10-18',timezone:'Australia/Perth'},'2026-10-17T14:00:00Z','1 day to polling day'],
 [{date:'2026-10-04',timezone:'Australia/Sydney'},'2026-10-03T14:00:00Z','Polling day'],
 [{date:'2026-10-05',timezone:'Australia/Sydney'},'2026-10-04T13:00:00Z','Polling day'],
 [{date:'2028-03-01',timezone:'Australia/Adelaide'},'2028-02-28T14:00:00Z','1 day to polling day'],
 [{date:null,timezone:'Australia/Darwin'},'2026-10-17T00:00:00Z','Date not announced'],
 [{date:'2026-10-27',dateTime:'2026-10-27T14:00:00+11:00',timezone:'Australia/Hobart',milestoneLabel:'postal voting closes'},'2026-10-25T23:00:00Z','1 day until postal voting closes'],
 [{date:'2026-10-27',dateTime:'2026-10-27T14:00:00+11:00',timezone:'Australia/Hobart',milestoneLabel:'postal voting closes'},'2026-10-27T01:30:00Z','Voting closes today · 1 hour 30 minutes remaining'],
 [{date:'2026-10-27',dateTime:'2026-10-27T14:00:00+11:00',timezone:'Australia/Hobart',milestoneLabel:'postal voting closes'},'2026-10-27T03:00:00Z','Voting closed today'],
 [{date:'2027-04-07',dateTime:'2027-04-07T17:00:00+09:30',timezone:'Australia/Adelaide',milestoneLabel:'postal voting closes'},'2027-04-07T07:31:00Z','Voting closed today']
];
for(const [event,instant,expected] of cases)assert.ok(label(event,new Date(instant)).startsWith(expected),`${JSON.stringify(event)} at ${instant}: ${label(event,new Date(instant))}`);
console.log(`PASS: ${cases.length} delivered-clock cases: local before/on/after, postal deadlines, daylight saving, Perth/Brisbane, leap year and unknown date. Synthetic cases do not change source events.`);
