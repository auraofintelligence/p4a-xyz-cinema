(() => {
  const ticker=document.querySelector('[data-issue-ticker]');if(!ticker)return;
  const viewport=ticker.querySelector('[data-ticker-viewport]'),track=ticker.querySelector('[data-ticker-track]'),group=ticker.querySelector('[data-ticker-group]'),button=ticker.querySelector('[data-ticker-toggle]');
  const reduced=matchMedia('(prefers-reduced-motion: reduce)'),hoverDevice=matchMedia('(hover: hover)');
  let paused=false,hovered=false,pressed=false,linkFocused=false,previous=null;
  const clone=group.cloneNode(true);clone.removeAttribute('data-ticker-group');clone.dataset.tickerClone='';clone.setAttribute('aria-hidden','true');
  clone.querySelectorAll('a').forEach(a=>a.tabIndex=-1);track.append(clone);
  function stopped(){return paused||reduced.matches||hovered||pressed||linkFocused;}
  function update(){
    ticker.classList.toggle('is-paused',stopped());ticker.classList.toggle('is-running',!stopped());
    button.disabled=reduced.matches;button.setAttribute('aria-pressed',String(paused||reduced.matches));
    button.textContent=reduced.matches?'-':paused?'▶':'Ⅱ';
    button.setAttribute('aria-label',reduced.matches?'Ticker motion off to respect reduced-motion preference':paused?'Play ticker':'Pause ticker');
  }
  // Scroll the same two equal groups over the slightly slower 45-second cycle.
  // Pausing changes only state: no transform reset, clone removal or relayout.
  function frame(now){
    const elapsed=previous===null?0:Math.min(now-previous,64);previous=now;
    const width=group.getBoundingClientRect().width;
    if(!stopped()&&!document.hidden&&width>0){
      viewport.scrollLeft=(viewport.scrollLeft+elapsed*width/45000)%width;
    }
    requestAnimationFrame(frame);
  }
  button.hidden=false;button.addEventListener('click',()=>{paused=!paused;update();});
  ticker.addEventListener('pointerenter',e=>{hovered=e.pointerType!=='touch'&&hoverDevice.matches;update();});
  ticker.addEventListener('pointerleave',()=>{hovered=false;update();});
  viewport.addEventListener('pointerdown',()=>{pressed=true;update();},{passive:true});
  window.addEventListener('pointerup',()=>{pressed=false;update();},{passive:true});
  window.addEventListener('pointercancel',()=>{pressed=false;update();},{passive:true});
  viewport.addEventListener('focusin',()=>{linkFocused=true;update();});
  viewport.addEventListener('focusout',()=>queueMicrotask(()=>{linkFocused=viewport.contains(document.activeElement);update();}));
  // Native anchors handle mouse, touch, keyboard and new-tab navigation.
  reduced.addEventListener('change',update);document.addEventListener('visibilitychange',()=>{previous=null;});
  update();requestAnimationFrame(frame);
})();
