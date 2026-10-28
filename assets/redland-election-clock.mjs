// Milestones stay inactive until an offset-bearing official timetable is verified.
export function milestoneState(item, now = Date.now()) {
  if (item.status === 'cancelled') return {text:'Cancelled — check the official ECQ notice.', active:false};
  if (item.status === 'completed') return {text:'Event completed — check the official ECQ status.', active:false};
  const valid = item.status === 'confirmed' && /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+10:00$/.test(item.target);
  const target = valid ? Date.parse(item.target) : NaN;
  if (!Number.isFinite(target)) return {text:'Awaiting confirmation to begin', active:false};
  if (now >= target) {
    if (item.kind === 'nominations') return {text:'Nominations closed. Check ECQ for accepted nominations and notices.', active:false};
    const end = Date.parse(item.ends || '');
    return {text:Number.isFinite(end) && now >= end ? 'Scheduled polling hours have ended. Check ECQ for the count and results.' : 'Scheduled polling time reached. Check ECQ for voting arrangements and election status.', active:false};
  }
  const total = Math.max(0, Math.floor((target - now) / 1000));
  return {text:item.kind === 'nominations' ? 'Time until the official nomination deadline:' : 'Time until the confirmed polling time:', active:true,
    values:[Math.floor(total / 86400), Math.floor(total / 3600) % 24, Math.floor(total / 60) % 60, total % 60]};
}

if (typeof document !== 'undefined') {
  for (const panel of document.querySelectorAll('[data-redland-milestone]')) {
    const item = {status:panel.dataset.timingStatus, target:panel.dataset.target, kind:panel.dataset.kind, ends:panel.dataset.ends};
    const status = panel.querySelector('[data-milestone-status]'), clock = panel.querySelector('[data-milestone-clock]');
    const tick = () => {
      const state = milestoneState(item);
      status.textContent = state.text; clock.hidden = !state.active;
      if (state.active) clock.querySelectorAll('strong').forEach((node, i) => { node.textContent = i ? String(state.values[i]).padStart(2,'0') : String(state.values[i]); });
    };
    tick();
    if (item.status === 'confirmed') setInterval(tick, 1000);
  }
}
