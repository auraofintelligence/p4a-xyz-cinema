/* Melbourne calendar-day countdown, independent of the visitor's timezone. */
(function (root) {
  'use strict';
  function status(now = new Date()) {
    const parts = new Intl.DateTimeFormat('en-AU', {timeZone:'Australia/Melbourne',year:'numeric',month:'2-digit',day:'2-digit'}).formatToParts(now);
    const date = Object.fromEntries(parts.map(p => [p.type,p.value]));
    const days = Math.round((Date.UTC(2026,10,28)-Date.UTC(+date.year,+date.month-1,+date.day))/86400000);
    if (days > 0) return {phase:'before',days,value:String(days),label:days===1?'day to election day':'days to election day',note:'Calendar days in Australia/Melbourne',action:'Explore the election guide'};
    if (days === 0) return {phase:'today',days:0,value:'Today',label:'Victoria election day',note:'Check VEC for voting locations and hours',action:'Election guide and voting information'};
    return {phase:'after',days:0,value:'28 Nov',label:'2026 polling date has passed',note:'Check official results and current representatives',action:'Explore the election record'};
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = {status};
  if (!root.document) return;
  root.P4A_VIC_HOME = {status};
  const card = document.querySelector('[data-vic-home-card]');
  if (!card) return;
  function render() {
    const state = status();
    for (const key of ['value','label','note','action']) {
      const node = card.querySelector('[data-vic-home-'+key+']');
      if (node && node.textContent !== state[key]) node.textContent = state[key];
    }
    card.dataset.electionPhase = state.phase;
  }
  render();
  setInterval(render,60000);
  document.addEventListener('visibilitychange',() => {if (!document.hidden) render();});
})(typeof window !== 'undefined' ? window : globalThis);
