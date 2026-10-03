(() => {
  'use strict';
  const data=window.P4A_VIC_ELECTORATES;
  const parties={
    'Australian Labor Party':['ALP','#e05268'],
    'Liberal Party':['LIB','#498fea'],
    'The Nationals':['NAT','#59a177'],
    'The Australian Greens - Victoria':['GRN','#9ac94c'],
    'Independent':['IND','#c3bccb'],
    'Animal Justice Party':['AJP','#bd7dea'],
    'One Nation Victoria':['ON','#f9a458'],
    'Libertarian Party':['LDP','#edd66b'],
    'Legalise Cannabis Victoria':['LCV','#43baad'],
    'Shooters, Fishers and Farmers Party Victoria':['SFF','#ae8865'],
    'Family First Victoria':['FF','#e493c3'],
    'Vacant':['VAC','#30253c']
  };
  const geographic=['#604e86','#58698c','#756185','#486e79','#706e91','#696087','#486779','#7b637a'];
  const style=party=>parties[party]||['OTHER','#b6b6b6'];
  function swatch(party){const el=document.createElement('span');el.className='vic-party-swatch'+(party==='Vacant'?' is-vacant':party==='Independent'?' is-independent':'');el.style.setProperty('--party',style(party)[1]);el.textContent=style(party)[0];return el;}
  const seats=chamber=>data[chamber].flatMap(r=>r.members.length?r.members.map(m=>({...m,electorate:r.name,id:r.id})): [{name:'Vacant seat',party:'Vacant',electorate:r.name,id:r.id}]);
  function regionCards(){const target=document.querySelector('[data-region-composition]');for(const r of data.council){const card=document.createElement('div');card.className='vic-region-composition';const a=document.createElement('a');a.href=`?chamber=council&electorate=${r.id}`;a.textContent=r.name;card.append(a);const group=document.createElement('div');for(const m of r.members){const chip=swatch(m.party);chip.title=`${m.name} — ${m.party}`;chip.setAttribute('aria-label',chip.title);group.append(chip);}card.append(group);target.append(card);}}
  const chamberControl=document.querySelector('[data-parliament-chamber]');
  function renderChamber(){
    const chamber=chamberControl.value,room=window.P4A_VIC_SEATING[chamber],people=new Map(window.P4A_VIC_PEOPLE.people.map(p=>[p.id,p])),total=room.seats.length,majority=total/2+1;
    const all=room.seats.map(s=>{const p=people.get(s.personId),area=data[chamber].find(r=>r.id===s.areaId);return {...s,name:p?.name||'Vacant seat',party:p?.party||'Vacant',electorate:area.name};});
    const counts=new Map();all.forEach(s=>counts.set(s.party,(counts.get(s.party)||0)+1));
    document.querySelector('[data-chamber-summary]').textContent=`${total} seats · ${all.filter(s=>!s.vacancy).length} current members · ${all.filter(s=>s.vacancy).length} vacant. Occupancy snapshot: 2 October 2026.`;
    const source=document.querySelector('[data-seating-source]');source.replaceChildren(document.createTextNode(room.note+' '));const a=document.createElement('a');a.href=room.source;a.textContent=`Official ${chamber==='assembly'?'Assembly':'Council'} seating source · ${room.sourceDate}`;source.append(a);
    const board=document.querySelector('[data-chamber-seats]');board.replaceChildren();board.className='vic-physical-room';board.dataset.chamber=chamber;board.setAttribute('aria-label',`${chamber==='assembly'?'Legislative Assembly':'Legislative Council'} source-derived physical seating, gallery perspective`);
    const [ox,oy,w,h]=room.viewBox;board.style.aspectRatio=`${w} / ${h}`;
    const background=document.createElement('canvas');background.width=w*2;background.height=h*2;background.setAttribute('aria-hidden','true');board.append(background);const c=background.getContext('2d');c.scale(2,2);c.translate(-ox,-oy);c.strokeStyle='#80705c';c.lineWidth=1.5;c.fillStyle='#2f2832';
    const table=(x,y,width,height,label)=>{c.fillRect(x,y,width,height);c.strokeRect(x,y,width,height);c.fillStyle='#edca79';c.font=`${chamber==='assembly'?9:18}px sans-serif`;c.textAlign='center';c.fillText(label,x+width/2,y+height/2+4);c.fillStyle='#2f2832';};
    if(chamber==='assembly'){table(253,275,108,54,'Clerks');table(268,333,76,142,'Table');c.strokeStyle='#67564c';for(const [x,y,r] of [[70,445,234],[130,445,174],[185,445,119]]){c.beginPath();c.moveTo(x,150);c.lineTo(x,y);c.ellipse(304,y,r,r,0,Math.PI,Math.PI/2,true);c.stroke();c.beginPath();c.moveTo(608-x,210);c.lineTo(608-x,y);c.ellipse(304,y,r,r,0,0,Math.PI/2);c.stroke();}}
    else{table(490,535,180,100,'Clerks');table(525,639,110,320,'Table');table(510,379,140,64,'President');c.strokeStyle='#67564c';for(const x of [160,285,410]){c.beginPath();c.moveTo(x,490);c.lineTo(x,1040);c.quadraticCurveTo(x,1250,500,1330);c.stroke();c.beginPath();c.moveTo(1160-x,490);c.lineTo(1160-x,1040);c.quadraticCurveTo(1160-x,1250,660,1330);c.stroke();}}
    const detail=document.querySelector('[data-seat-detail]');detail.textContent='Hover or focus for a name. Click for the representative’s details. Arrow keys move through the physical positions; Tab leaves the chamber.';
    const buttons=[];
    all.forEach((s,i)=>{const b=document.createElement('button');b.type='button';b.className='vic-physical-seat'+(s.vacancy?' is-vacant':'');b.style.left=`${(s.x-ox)/w*100}%`;b.style.top=`${(s.y-oy)/h*100}%`;b.style.setProperty('--seat-colour',style(s.party)[1]);b.dataset.seat=s.id;b.dataset.person=s.personId||'';b.setAttribute('aria-label',`${s.name}; ${s.party}; ${s.electorate}${s.presiding?'; presiding officer':''}`);b.title=b.getAttribute('aria-label');b.tabIndex=i===0?0:-1;b.textContent=s.vacancy?'Vacant':s.sourceLabel==='SPEAKER'?'Speaker':s.name.split(' ').slice(1).join(' ');
      const show=()=>{detail.textContent=b.getAttribute('aria-label')+'. Click to open details.';};b.addEventListener('pointerenter',show);b.addEventListener('focus',show);b.addEventListener('click',()=>{if(s.personId)window.P4A_VIC_DETAILS.openPerson(s.personId);else location.href=`?chamber=${chamber}&electorate=${s.areaId}&section=representatives`;});
      b.addEventListener('keydown',e=>{let next;if(e.key==='Home')next=0;else if(e.key==='End')next=all.length-1;else if(['ArrowLeft','ArrowRight','ArrowUp','ArrowDown'].includes(e.key)){const [dx,dy]=({ArrowLeft:[-1,0],ArrowRight:[1,0],ArrowUp:[0,-1],ArrowDown:[0,1]})[e.key];const options=all.map((p,j)=>({j,along:(p.x-s.x)*dx+(p.y-s.y)*dy,across:Math.abs((p.x-s.x)*dy-(p.y-s.y)*dx)})).filter(p=>p.along>1);options.sort((a,b)=>(a.along+2*a.across)-(b.along+2*b.across));next=options[0]?.j;}if(next!==undefined){e.preventDefault();buttons.forEach(x=>x.tabIndex=-1);buttons[next].tabIndex=0;buttons[next].focus();}});buttons.push(b);board.append(b);
    });
    const totals=document.querySelector('[data-chamber-totals]');totals.replaceChildren();for(const [party,count] of counts){const li=document.createElement('li');li.append(swatch(party),document.createTextNode(` ${party}: ${count} ${count===1?'seat':'seats'}`));totals.append(li);}
    const bar=document.querySelector('[data-chamber-bar]');bar.replaceChildren();bar.style.setProperty('--majority',`${majority/total*100}%`);bar.setAttribute('aria-label',`Party seat totals; full-house majority marker at ${majority} of ${total} seats. Party order is not a coalition.`);
    for(const [party,count] of counts){const s=document.createElement('span');s.style.width=`${count/total*100}%`;s.style.background=style(party)[1];s.title=`${party}: ${count}`;bar.append(s);}
    document.querySelector('[data-majority-label]').textContent=`Full-house majority marker: ${majority} of ${total} seats. Parties are displayed separately; their order does not imply a coalition.`;
  }
  function legend(mode,layer){
    const target=document.querySelector('[data-colour-legend]');target.replaceChildren();
    if(layer==='firstpeoples'){
      document.querySelector('[data-region-composition-wrap]').hidden=true;
      document.querySelector('[data-colour-caption]').textContent='Statutory records, not a comprehensive Country map. Overlapping matches are retained.';
      document.querySelector('[data-colour-explanation]').textContent='Teal: RAP appointment areas. Amber with dashed boundaries: settlement-agreement extents. These colours distinguish legal record types; they do not represent party support, cultural ownership or exclusive authority.';
      for(const [label,colour] of [['RAP appointment area','#58b7ad'],['Settlement-agreement extent','#d6a744']]){const li=document.createElement('li'),s=document.createElement('span');s.className='vic-geo-swatch';s.style.background=colour;li.append(s,document.createTextNode(label));target.append(li);}return;
    }
    if(['lga','ward'].includes(layer)){
      document.querySelector('[data-region-composition-wrap]').hidden=true;
      document.querySelector('[data-colour-caption]').textContent=layer==='lga'?'Municipalities: geographic colours. Grey: unincorporated areas.':'Electoral areas: geographic colours; no party affiliation is inferred.';
      document.querySelector('[data-colour-explanation]').textContent='Local colours only distinguish geographic areas. They do not represent parties, population, vote share or ownership. Eight unincorporated areas are separate from the 79 councils. Ward and unsubdivided area labels follow the source.';
      for(const [label,colour] of [['Municipal / ward geography','#58698c'],['Unincorporated area','#514a5a']]){const li=document.createElement('li'),swatch=document.createElement('span');swatch.className='vic-geo-swatch';swatch.style.background=colour;li.append(swatch,document.createTextNode(label));target.append(li);}return;
    }

    const caption=document.querySelector('[data-colour-caption]');caption.textContent=mode==='geographic'?'Geographic colours identify Legislative Council regions.':'Assembly: sitting member party. Council: geographic base + five-member party compositions below.';
    const explanatory=document.querySelector('[data-colour-explanation]');explanatory.textContent=mode==='geographic'?'Each muted colour identifies one Legislative Council region and its 11 Assembly districts. Colours are geographic grouping aids, not party support, population, vote share, land ownership or election results.':'Assembly districts use their current representative’s party colour, not a predicted winner or a past result. Independent seats have stripes; vacancies have a cross pattern. Council regions keep their geographic base because five members can represent different parties; the badges show every member separately.';
    if(mode==='geographic'){for(const r of data.council){const li=document.createElement('li'),s=document.createElement('span');s.className='vic-geo-swatch';s.style.background=geographic[r.code-1];li.append(s,document.createTextNode(r.name));target.append(li);}}
    else {for(const party of Object.keys(parties).filter(p=>seats(layer).some(s=>s.party===p))){const li=document.createElement('li');li.append(swatch(party),document.createTextNode(party));target.append(li);}}
    document.querySelector('[data-region-composition-wrap]').hidden=!(mode==='party'&&layer==='council');
  }
  window.P4A_VIC_REPRESENTATION={style,legend};regionCards();renderChamber();chamberControl.addEventListener('change',renderChamber);
})();
