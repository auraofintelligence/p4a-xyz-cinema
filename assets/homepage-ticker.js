(() => {
  const ticker=document.querySelector('[data-issue-ticker]');if(!ticker)return;
  const viewport=ticker.querySelector('[data-ticker-viewport]'),track=ticker.querySelector('[data-ticker-track]'),group=ticker.querySelector('[data-ticker-group]'),button=ticker.querySelector('[data-ticker-toggle]');
  const reduced=matchMedia('(prefers-reduced-motion: reduce)');let paused=false;
  const clone=group.cloneNode(true);clone.removeAttribute('data-ticker-group');clone.dataset.tickerClone='';clone.setAttribute('aria-hidden','true');
  clone.querySelectorAll('a').forEach(a=>{a.tabIndex=-1;a.addEventListener('mousedown',e=>e.preventDefault());});track.append(clone);
  function update(){const stopped=paused||reduced.matches;ticker.classList.toggle('is-paused',stopped);ticker.classList.toggle('is-running',!stopped);button.disabled=reduced.matches;button.setAttribute('aria-pressed',String(stopped));button.textContent=reduced.matches?'Motion off':paused?'Play ticker':'Pause ticker';button.setAttribute('aria-label',reduced.matches?'Ticker motion off to respect reduced-motion preference':paused?'Play ticker':'Pause ticker and browse the topics');if(!stopped)viewport.scrollLeft=0;}
  button.hidden=false;button.addEventListener('click',()=>{paused=!paused;update();});
  group.addEventListener('focusin',e=>{ticker.classList.add('has-link-focus');requestAnimationFrame(()=>e.target.scrollIntoView({block:'nearest',inline:'nearest',behavior:'instant'}));});
  ticker.addEventListener('focusout',()=>queueMicrotask(()=>{if(!group.contains(document.activeElement)){ticker.classList.remove('has-link-focus');if(!paused&&!reduced.matches)viewport.scrollLeft=0;}}));
  reduced.addEventListener('change',update);update();
})();
