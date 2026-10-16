// Execute the shipped countdown code against fixed times, without a browser.
import vm from 'node:vm';
import fs from 'node:fs';
import assert from 'node:assert/strict';
const code=fs.readFileSync(new URL('../assets/local-council.js',import.meta.url),'utf8');
function check(now,early=false){
  const values=[{},{},{},{}],status={};
  const clock={dataset:{electionCountdown:'2028-03-25T00:00:00+10:00'},parentElement:{querySelector:()=>status},querySelectorAll:()=>values};
  const window={dataset:{opens:'2028-03-13T08:00:00+10:00',closes:'2028-03-24T18:00:00+10:00'},querySelector:selector=>selector==='[data-voting-status]'?status:clock};
  class FixedDate extends Date{static now(){return Date.parse(now);}}
  const document={querySelector:()=>null,querySelectorAll:selector=>selector==='[data-election-countdown]'&&!early?[clock]:selector==='[data-voting-window]'&&early?[window]:[]};
  vm.runInNewContext(code,{document,Date:FixedDate,URLSearchParams,location:{search:''},setInterval:()=>0});
  return {clock,status,values:values.map(v=>v.textContent)};
}
assert.deepEqual(check('2028-03-24T00:00:00+10:00').values,['1','00','00','00']);
assert.deepEqual(check('2028-03-24T23:59:59+10:00').values,['0','00','00','01']);
assert.equal(check('2028-03-25T00:00:00+10:00').clock.hidden,true);
assert.match(check('2028-03-26T00:00:00+10:00').status.textContent,/Check ECQ/);
assert.match(check('2028-03-12T08:00:00+10:00',true).status.textContent,/window opens/);
assert.match(check('2028-03-13T08:00:00+10:00',true).status.textContent,/within its published/);
assert.equal(check('2028-03-24T18:00:00+10:00',true).clock.hidden,true);
console.log('PASS: AEST election countdown before/on/after date; sourced early-voting window before/during/after. Test dates are synthetic, not a published timetable.');
