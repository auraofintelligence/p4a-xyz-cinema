/* VEC dates checked 9 October 2026; Melbourne calendar days. */
(function(root){'use strict';
const OPEN='2026-11-18T09:00:00+11:00',CLOSE='2026-11-27T18:00:00+11:00';
function status(now=new Date()){
 const parts=Object.fromEntries(new Intl.DateTimeFormat('en-AU',{timeZone:'Australia/Melbourne',year:'numeric',month:'2-digit',day:'2-digit'}).formatToParts(now).map(p=>[p.type,p.value]));
 const days=Math.round((Date.UTC(2026,10,18)-Date.UTC(+parts.year,+parts.month-1,+parts.day))/86400000);
 if(now<new Date(OPEN))return {phase:'before',days:Math.max(0,days),value:days>0?String(days):'Today',label:days>0?(days===1?'day to early voting':'days to early voting'):'Early voting opens at 9 am',note:'Opens 18 November · Australia/Melbourne'};
 if(now<new Date(CLOSE))return {phase:'open',days:0,value:'Open',label:'Early voting is open',note:'18–27 November · 9 am–6 pm; closed Sunday 22 November'};
 return {phase:'closed',days:0,value:'Closed',label:'Early voting has ended',note:'Election day: Saturday 28 November · check VEC voting options'};
}
if(typeof module!=='undefined')module.exports={status,open:OPEN,close:CLOSE};
if(!root.document)return;
const nodes=[...document.querySelectorAll('[data-vic-early-clock]')];
// State cards and the site tree use the same component as the main countdowns.
document.querySelectorAll('[data-election-state="vic"], [data-election-card][data-state="vic"][data-election-scope="general"]').forEach(card=>{
 if(card.querySelector('[data-vic-early-clock]'))return;
 const p=document.createElement('p');p.className='vic-early-clock';p.dataset.vicEarlyClock='';
 p.innerHTML='<strong data-vic-early-value>18 Nov</strong> <span data-vic-early-label>Early voting opens</span><br><small data-vic-early-note>18–27 November · Australia/Melbourne</small>';
 card.append(p);nodes.push(p);
});
function render(){const s=status();nodes.forEach(node=>{node.dataset.earlyPhase=s.phase;for(const k of ['value','label','note'])node.querySelector('[data-vic-early-'+k+']').textContent=s[k];});}
render();setInterval(render,60000);document.addEventListener('visibilitychange',()=>{if(!document.hidden)render();});
})(typeof window!=='undefined'?window:globalThis);
