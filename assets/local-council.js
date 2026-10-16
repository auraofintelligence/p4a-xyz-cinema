/* Browser-local enhancement only. Reviewed 2026-10-16. No submissions/network writes. */
(() => {
  const params = new URLSearchParams(location.search);
  const search = document.querySelector('[data-local-search]');
  if (search) {
    const input = search.querySelector('input');
    const select = search.querySelector('select');
    const cards = [...document.querySelectorAll('[data-local-record]')];
    const count = document.querySelector('[data-result-count]');
    const empty = document.querySelector('[data-no-results]');
    input.value = params.get('q') || '';
    if ([...select.options].some(o => o.value === params.get('type'))) select.value = params.get('type');
    function filter(update) {
      const terms = input.value.toLowerCase().trim().split(/\s+/).filter(Boolean);
      let shown = 0;
      cards.forEach(card => {
        const match = (!select.value || card.dataset.type === select.value) && terms.every(term => card.dataset.search.includes(term));
        card.hidden = !match;
        if (match) shown++;
      });
      count.textContent = `${shown} of ${cards.length} connections`;
      empty.hidden = shown > 0;
      if (update) {
        const next = new URL(location.href);
        input.value.trim() ? next.searchParams.set('q', input.value.trim()) : next.searchParams.delete('q');
        select.value ? next.searchParams.set('type', select.value) : next.searchParams.delete('type');
        history.replaceState(null, '', next);
      }
    }
    search.addEventListener('submit', e => {e.preventDefault(); filter(true);});
    input.addEventListener('input', () => filter(true));
    select.addEventListener('change', () => filter(true));
    search.querySelector('[data-clear-search]').addEventListener('click', () => {input.value='';select.value='';filter(true);input.focus();});
    function openHash() {
      let id;
      try {id = decodeURIComponent(location.hash.slice(1));} catch {return;}
      const card = cards.find(item => item.id === id);
      if (!card) return;
      // A direct related-item link must remain visible even after a previous filter.
      if (card.hidden) {input.value='';select.value='';filter(true);}
      card.open = true;
      requestAnimationFrame(() => card.scrollIntoView({block:'start'}));
    }
    filter(false); openHash(); window.addEventListener('hashchange', openHash);
  }
  document.querySelectorAll('[data-map-gallery]').forEach(gallery => {
    const buttons = [...gallery.querySelectorAll('[data-map-choice]')];
    buttons.forEach(button => button.addEventListener('click', () => {
      buttons.forEach(other => other.setAttribute('aria-pressed', String(other === button)));
      gallery.querySelectorAll('[data-map-panel]').forEach(panel => {panel.hidden = panel.dataset.mapPanel !== button.dataset.mapChoice;});
    }));
  });
  document.querySelectorAll('[data-election-countdown]').forEach(clock => {
    const target = Date.parse(clock.dataset.electionCountdown);
    const status = clock.parentElement.querySelector('[data-election-status]');
    function tick() {
      const remaining = target - Date.now();
      if (remaining <= 0) {clock.hidden = true;status.textContent = 'Scheduled date reached. Check ECQ for the election status and results; this clock does not verify that polling occurred.';return;}
      const total = Math.floor(remaining/1000);
      const units = [Math.floor(total/86400), Math.floor(total/3600)%24, Math.floor(total/60)%60, total%60];
      clock.querySelectorAll('strong').forEach((value,i) => {value.textContent = i ? String(units[i]).padStart(2,'0') : String(units[i]);});
    }
    tick(); setInterval(tick,1000);
  });
  document.querySelectorAll('[data-voting-window]').forEach(window => {
    const opens=Date.parse(window.dataset.opens), closes=Date.parse(window.dataset.closes);
    const clock=window.querySelector('[data-voting-countdown]'), status=window.querySelector('[data-voting-status]');
    function tick() {
      const now=Date.now();
      if (now>=closes) {clock.hidden=true;status.textContent='The published early-voting window has ended. Check ECQ for remaining voting options.';return;}
      const open=now>=opens, total=Math.max(0,Math.floor(((open?closes:opens)-now)/1000));
      status.textContent=open?'Early voting is within its published date window. Check the centre\'s actual opening hours. Time until this window closes:':'Time until the published early-voting window opens:';
      const units=[Math.floor(total/86400),Math.floor(total/3600)%24,Math.floor(total/60)%60,total%60];
      clock.querySelectorAll('strong').forEach((value,i)=>{value.textContent=i?String(units[i]).padStart(2,'0'):String(units[i]);});
    }
    tick();setInterval(tick,1000);
  });
  const form = document.querySelector('[data-journey-note]');
  if (form && params.has('topic')) form.elements.namedItem('Place or thread').value=params.get('topic');
  if (form) form.addEventListener('submit', event => {
    event.preventDefault();
    const fields = new FormData(form);
    const rows = ['# My Redlands journey','',`Written: ${new Date().toISOString()}`, 'Place: Redland City, Queensland', `Page: ${location.href}`, '', 'Private draft; not submitted to P4A or council.'];
    fields.forEach((value,key) => rows.push('',`## ${key}`,String(value).trim() || 'Not yet recorded'));
    rows.push('', 'Agent handover: preserve my wording and purpose. Check source dates and geography. Ask before sharing or taking action outside my existing authorisation. Distinguish proposed work, authorised work and observed outcomes.');
    const url = URL.createObjectURL(new Blob([rows.join('\n')+'\n'],{type:'text/markdown;charset=utf-8'}));
    const link = document.createElement('a');link.href=url;link.download='my-redlands-journey.md';link.click();setTimeout(() => URL.revokeObjectURL(url),10000);
    document.querySelector('[data-note-status]').textContent = 'Your draft was prepared for download. It has not been submitted or saved by this site.';
  });
  // The shipped HTML is disabled: without this listener private notes cannot
  // fall back to a browser GET submission and enter a URL or request log.
  if (form) form.querySelector('[data-note-fields]').disabled=false;
})();
