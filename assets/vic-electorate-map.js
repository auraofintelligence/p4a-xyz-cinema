(() => {
  'use strict';
  const G = window.P4A_VIC_GEOMETRY, data = window.P4A_VIC_ELECTORATES;
  const stage = document.querySelector('.vic-map-stage');
  if (!stage || !G || !data) return;
  const base = stage.querySelector('[data-map-base]'), canvas = stage.querySelector('[data-map-interaction]');
  const ctx = base.getContext('2d'), overlay = canvas.getContext('2d');
  const list = document.querySelector('[data-electorate-list]'), search = document.querySelector('[data-electorate-search]');
  const message = document.querySelector('[data-map-message]'), label = document.querySelector('[data-map-label]');
  const profile = document.querySelector('[data-electorate-profile]');
  const colours = ['#604e86','#58698c','#756185','#486e79','#706e91','#696087','#486779','#7b637a'];
  let colourMode='geographic',localScope=null,pickedMatches=[],hoverMatches=[];
  const recognitionEnabled=()=>[...document.querySelectorAll('[data-recognition-layer]:checked')].map(x=>x.dataset.recognitionLayer);
  const representation=window.P4A_VIC_REPRESENTATION;
  const patterns={};
  for(const party of ['Independent','Vacant']){const tile=document.createElement('canvas');tile.width=tile.height=10;const t=tile.getContext('2d');t.fillStyle=representation.style(party)[1];t.fillRect(0,0,10,10);t.strokeStyle=party==='Vacant'?'#eee5fa':'#645a6d';t.lineWidth=1.3;t.beginPath();t.moveTo(0,0);t.lineTo(10,10);if(party==='Vacant'){t.moveTo(10,0);t.lineTo(0,10);}t.stroke();patterns[party]=ctx.createPattern(tile,'repeat');}
  let layer = 'assembly', selected = null, hovered = null, shapes = [], bounds, size = [0,0], ratio = 1;
  let transform = {scale:1,x:0,y:0}, baseScale = 1, loadingToken = 0, drag = null, pinch = null;
  const pointers = new Map(), cache = new Map();
  let layerReady=false,pendingReset=false,viewMode='state',alignmentRequest=0;
  const extentPoints=[G.project(data.victoriaBoundsLonLat.slice(0,2)),G.project(data.victoriaBoundsLonLat.slice(2))];
  const stateBounds=[Math.min(...extentPoints.map(p=>p[0])),Math.min(...extentPoints.map(p=>p[1])),Math.max(...extentPoints.map(p=>p[0])),Math.max(...extentPoints.map(p=>p[1]))];
  history.scrollRestoration='manual';
  async function alignMap(token=loadingToken){
    const request=++alignmentRequest;await document.fonts.ready;let stable=0,last='';
    for(let frame=0;frame<120;frame++){
      await new Promise(resolve=>requestAnimationFrame(resolve));if(token!==loadingToken||request!==alignmentRequest)return;
      let obstruction=0,animating=false;for(const node of document.querySelectorAll('.site-header,.site-layer-strip')){const style=getComputedStyle(node),rect=node.getBoundingClientRect();if(['sticky','fixed'].includes(style.position)&&rect.top<150&&rect.bottom>0)obstruction=Math.max(obstruction,rect.bottom);animating ||= node.getAnimations({subtree:true}).some(a=>a.playState==='running');}
      const rect=stage.getBoundingClientRect(),documentTop=rect.top+scrollY,target=Math.max(0,documentTop-obstruction-12),stamp=[documentTop,obstruction,rect.width,rect.height].map(v=>Math.round(v*10)/10).join(':');
      window.scrollTo({top:target,behavior:'instant'});stable=!animating&&stamp===last&&Math.abs(scrollY-target)<1.5?stable+1:0;last=stamp;
      if(stable>=3){canvas.focus({preventScroll:true});return;}
    }
  }
  for(const type of ['wheel','touchstart','pointerdown'])window.addEventListener(type,()=>{alignmentRequest++;},{passive:true});
  function resetToVictoria(){search.value='';localScope=null;viewMode='state';pendingReset=!layerReady;if(layerReady&&layer==='ward')shapes=cache.get('ward')||shapes;renderList();fit(stateBounds);updateNavigation(selected,true);alignMap();}

  const escape = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const records = () => data[layer].filter(r=>layer==='firstpeoples'?recognitionEnabled().includes(r.kind):layer!=='ward'||!localScope||r.parentId===localScope);
  const record = id => data[layer].find(r => r.id === id);
  const isLocal=()=>['lga','ward'].includes(layer);
  const sortField=document.querySelector('[data-electorate-sort]'),sortOrder=document.querySelector('[data-electorate-order]');
  const sortMeta={populationGrowth:{label:'Population growth',note:'ABS ERP change 2024-25 · %'},populationDensity:{label:'Population density',note:'ABS ERP 2025 · people/km²'},name:{label:'Electorate name',note:'Alphabetical'},population:{label:'Population',note:'2021 Census · people'},areaKm2:{label:'Electorate area',note:'Published workbook area on 2022 boundaries · km²; not a verified land-only measure'},medianAge:{label:'Median age',note:'2021 Census · years'},medianWeeklyRent:{label:'Median weekly rent',note:'2021 Census · AUD/week'},medianWeeklyHouseholdIncome:{label:'Median weekly household income',note:'2021 Census · AUD/week'}};
  const metricValue=(r,key)=>Number.isFinite(r.sortMetrics?.[key])?r.sortMetrics[key]:null;
  const metricText=(r,key)=>{const v=metricValue(r,key);if(v===null)return 'Not available';const f=(n,d=0)=>n.toLocaleString('en-AU',{maximumFractionDigits:d});if(layer==='lga')return key==='population'?`${f(v)} people · 30 June 2025`:key==='areaKm2'?`${f(v,2)} km² · ABS LGA 2025`:key==='populationGrowth'?`${f(v,2)}% · 2024-25`:`${f(v,2)} people/km² · 2025`;return key==='population'?`${f(v)} people · ${layer==='council'?'2021 district sum':'2021 Census'}`:key==='areaKm2'?`${f(v,2)} km² · ${layer==='council'?'district area sum, 2022 boundaries':'published area, 2022 boundaries'}`:key==='medianAge'?`${f(v)} years · 2021 Census`:['medianWeeklyRent','medianWeeklyHouseholdIncome'].includes(key)?`$${f(v,2)}/week · 2021 Census`:`${f(v)} · 2021 Census`;};
  const compareRecords=(a,b,key,direction)=>{const tie=a.name.localeCompare(b.name,'en-AU',{sensitivity:'base'});if(key==='name')return(direction==='desc'?-1:1)*tie;const av=metricValue(a,key),bv=metricValue(b,key);if(av===null||bv===null)return av===bv?tie:av===null?1:-1;return av===bv?tie:(direction==='desc'?-1:1)*(av-bv);};

  const mapPoint = (x,y) => [(x-transform.x)/transform.scale,(y-transform.y)/transform.scale];
  const localPoint = event => {const b=canvas.getBoundingClientRect();return [event.clientX-b.left,event.clientY-b.top];};
  const shapeVisible = s => s.bounds[2]*transform.scale+transform.x>=0 && s.bounds[0]*transform.scale+transform.x<=size[0] && s.bounds[3]*transform.scale+transform.y>=0 && s.bounds[1]*transform.scale+transform.y<=size[1];
  function setupContext(context) {context.setTransform(ratio,0,0,ratio,0,0);context.clearRect(0,0,size[0],size[1]);context.translate(transform.x,transform.y);context.scale(transform.scale,transform.scale);}
  function drawOverlay() {
    setupContext(overlay);
    for (const [id,colour,width] of [[selected,'#f6ce73',2.1],...(layer==='firstpeoples'?hoverMatches:[hovered]).map(id=>[id,'#eee1ff',1.7])]) {
      if (!id) continue;
      const s=shapes.find(s=>s.id===id);if(!s)continue;
      overlay.fillStyle=id===selected?'rgba(246,206,115,.22)':'rgba(224,193,255,.23)';
      overlay.fill(s.path,'evenodd');overlay.strokeStyle=colour;overlay.lineWidth=width/transform.scale;overlay.stroke(s.path);
    }
    overlay.setTransform(1,0,0,1,0,0);
  }
  let frame = 0, needsBase = false;
  function schedule(full=false) {
    needsBase ||= full;
    if (frame) return;
    frame=requestAnimationFrame(()=>{frame=0;if(needsBase){needsBase=false;setupContext(ctx);for(const s of shapes){if(!shapeVisible(s))continue;const party=record(s.id)?.members[0]?.party||'Vacant';ctx.fillStyle=layer==='firstpeoples'?(record(s.id).kind==='rap'?'rgba(88,183,173,.46)':'rgba(214,167,68,.35)'):isLocal()&&record(s.id)?.kind==='unincorporated'?'#514a5a':colourMode==='party'&&layer==='assembly'?(patterns[party]||representation.style(party)[1]):colours[(s.region-1)%colours.length];if(patterns[party]&&colourMode==='party'&&layer==='assembly')patterns[party].setTransform(new DOMMatrix().scale(1/transform.scale));ctx.fill(s.path,'evenodd');ctx.strokeStyle=layer==='firstpeoples'?(record(s.id).kind==='rap'?'#74ded0':'#f0c568'):'#b8a6d0';ctx.lineWidth=(layer==='firstpeoples'?1.1:.65)/transform.scale;ctx.setLineDash(layer==='firstpeoples'&&record(s.id).kind==='rsa'?[5/transform.scale,3/transform.scale]:[]);ctx.stroke(s.path);ctx.setLineDash([]);}
      ctx.setTransform(ratio,0,0,ratio,0,0);ctx.font='12px "Archivo Var", sans-serif';ctx.textAlign='center';ctx.textBaseline='middle';
      const labelBoxes=[];
      for(const s of shapes){const r=record(s.id);if(!r.labelPoint)continue;const p=G.project(r.labelPoint),x=p[0]*transform.scale+transform.x,y=p[1]*transform.scale+transform.y,w=ctx.measureText(r.name).width+10;
        if((s.bounds[2]-s.bounds[0])*transform.scale<w+20||(s.bounds[3]-s.bounds[1])*transform.scale<45||x<w/2+8||x>size[0]-w/2-8||y<100||y>size[1]-48)continue;
        const box=[x-w/2,y-10,x+w/2,y+10];if(labelBoxes.some(b=>box[0]<b[2]&&box[2]>b[0]&&box[1]<b[3]&&box[3]>b[1]))continue;labelBoxes.push(box);
        ctx.lineWidth=3;ctx.strokeStyle='#24172bdd';ctx.strokeText(r.name,x,y);ctx.fillStyle='#f6efff';ctx.fillText(r.name,x,y);
      }
      ctx.setTransform(1,0,0,1,0,0);}drawOverlay();});
  }
  function fit(box=bounds) {
    if(!box)return;
    const scale=Math.min((size[0]-60)/(box[2]-box[0]),(size[1]-85)/(box[3]-box[1]));
    transform={scale:Math.min(baseScale*1200,scale),x:0,y:0};
    transform.x=size[0]/2-(box[0]+box[2])/2*transform.scale;
    transform.y=size[1]/2-(box[1]+box[3])/2*transform.scale;
    schedule(true);
  }
  function zoom(factor,anchor=[size[0]/2,size[1]/2]) {
    const p=mapPoint(...anchor), scale=Math.max(baseScale*.65,Math.min(baseScale*1200,transform.scale*factor));
    transform={scale,x:anchor[0]-p[0]*scale,y:anchor[1]-p[1]*scale};schedule(true);
  }
  function pickAll(x,y) {
    const p=mapPoint(x,y);overlay.setTransform(1,0,0,1,0,0);const matches=[];
    for(let i=shapes.length-1;i>=0;i--){const s=shapes[i],b=s.bounds;if(p[0]>=b[0]&&p[0]<=b[2]&&p[1]>=b[1]&&p[1]<=b[3]&&overlay.isPointInPath(s.path,p[0],p[1],'evenodd'))matches.push(s.id);}return matches;
  }
  function pick(x,y){return pickAll(x,y)[0]||null;}
  function setHover(id,matches=[]) {if(id===hovered&&matches.join()===hoverMatches.join())return;hovered=id;hoverMatches=matches;
    label.textContent=layer==='firstpeoples'?(matches.length?`${matches.length} statutory record${matches.length===1?'':'s'}: ${matches.map(x=>record(x).name).join(' / ')}`:'No record here in the selected statutory layers; this does not define Country.'):(id?record(id).name:(selected?`${record(selected).name} selected`:'Hover or tap a boundary to explore'));schedule();
  }
  function recognitionChooser(ids,navMode=true){pickedMatches=ids;selected=null;profile.innerHTML='<span class="vic-kicker">Records at this map point</span><h2>'+ids.length+' statutory record'+(ids.length===1?'':'s')+'</h2><p>These are separate legal records. Choose each to inspect its meaning, authority and dates. Their overlap does not make them interchangeable.</p>';if(!ids.length)profile.innerHTML='<h2>No record in the selected layer(s)</h2><p>This does not mean no Country, language, cultural connection or Traditional Owners. Explore the community-led resources above and check the official sources.</p>';for(const id of ids){const b=document.createElement('button');b.type='button';b.textContent=record(id).name+' - '+record(id).body;b.addEventListener('click',()=>select(id,false));profile.append(b);}updateNavigation(null,navMode);schedule();}
  function renderRecognitionProfile(r){profile.replaceChildren(document.querySelector(`#${r.id} [data-first-peoples-facts]`).cloneNode(true));if(pickedMatches.length>1){const p=document.createElement('p');p.textContent='Other records at the same point: ';for(const id of pickedMatches.filter(id=>id!==r.id)){const b=document.createElement('button');b.type='button';b.textContent=record(id).name;b.addEventListener('click',()=>select(id,false));p.append(b);}profile.prepend(p);}const u=new URL(location.href);u.searchParams.set('chamber',layer);u.searchParams.set('electorate',r.id);u.searchParams.set('recognition',recognitionEnabled().join(','));u.searchParams.delete('council');if(pickedMatches.length>1)u.searchParams.set('matches',pickedMatches.join(','));const a=document.createElement('a');a.href=u.href;a.textContent='Permanent link to this statutory record';profile.append(a);const b=document.createElement('button');b.type='button';b.textContent='Zoom to this record';b.addEventListener('click',()=>fit(shapes.find(s=>s.id===r.id)?.bounds));profile.append(b);}
  function renderList() {
    const focusId=list.contains(document.activeElement)?document.activeElement.dataset.electorate:null;
    const q=search.value.trim().toLocaleLowerCase('en-AU');
    sortField.querySelectorAll('option').forEach(o=>{o.disabled=['ward','firstpeoples'].includes(layer)?o.value!=='name':layer==='lga'?!['name','population','areaKm2','populationGrowth','populationDensity'].includes(o.value):layer==='council'?!['name','population','areaKm2'].includes(o.value):['populationGrowth','populationDensity'].includes(o.value);});
    if(sortField.selectedOptions[0].disabled)sortField.value='name';
    const sortKey=sortField.value, direction=sortOrder.value;
    document.querySelector('[data-sort-note]').textContent=(layer==='lga'&&['population','areaKm2'].includes(sortKey)?(sortKey==='population'?'ABS ERP · 30 June 2025 · people':'ABS LGA 2025 statistical area · km²; differs from legal map geometry'):sortMeta[sortKey].note)+(layer==='council'&&sortKey!=='name'?'. Region value is the sum of 11 district values; no medians or rates are averaged.':'')+'. Missing values always appear last.';

    const filtered=records().filter(r=>[r.name,r.regionName,r.parentName,...r.members.map(m=>`${m.name} ${m.party}`)].join(' ').toLocaleLowerCase('en-AU').includes(q));
    filtered.sort((a,b)=>compareRecords(a,b,sortKey,direction));
    list.replaceChildren(...filtered.map(r=>{const b=document.createElement('button');b.type='button';b.dataset.electorate=r.id;b.setAttribute('aria-pressed',String(selected===r.id));b.append(document.createTextNode(r.name));const sub=document.createElement('small');sub.textContent=layer==='firstpeoples'?r.body:layer==='assembly'?r.regionName:layer==='council'?`${r.districts.length} districts · 5 seats`:layer==='ward'?`${r.parentName} · ${r.kind}`:r.kind==='unincorporated'?'Unincorporated area · not a council':r.governance==='administration'?'Municipality · administrators':'Municipality · local government';b.append(sub);if(sortKey!=='name'){const metric=document.createElement('small');metric.className='vic-list-metric';metric.textContent=metricText(r,sortKey);b.append(metric);}b.addEventListener('click',()=>select(r.id,true));return b;}));
    document.querySelector('[data-electorate-count]').textContent=`${filtered.length} of ${records().length} ${layer==='assembly'?'districts':layer==='council'?'regions':layer==='ward'?'electoral areas':layer==='firstpeoples'?'statutory records':'local areas (79 councils + 8 unincorporated)'}`;
    if(!filtered.length)list.textContent='No matches. Try an electorate, member or party name.';
    if(focusId)list.querySelector(`[data-electorate="${focusId}"]`)?.focus({preventScroll:true});
  }
  function renderLocalProfile(r){
    profile.replaceChildren(document.querySelector(`#${r.id} [data-local-facts]`).cloneNode(true));
    const zoomButton=document.createElement('button');zoomButton.type='button';zoomButton.textContent=`Zoom to ${r.name}`;zoomButton.addEventListener('click',()=>fit(shapes.find(s=>s.id===r.id)?.bounds));profile.append(zoomButton);
    const u=new URL(location.href);u.searchParams.set('chamber',layer);u.searchParams.set('electorate',r.id);if(layer==='ward')u.searchParams.set('council',localScope||'all');else u.searchParams.delete('council');u.hash='';for(const key of ['recognition','matches','person','view'])u.searchParams.delete(key);const link=document.createElement('a');link.href=u.href;link.textContent='Permanent link to this place';const p=document.createElement('p');p.append(link);profile.append(p);
    profile.querySelectorAll('a[href^="?"]').forEach(a=>a.addEventListener('click',event=>{event.preventDefault();const url=new URL(a.href);changeLayer(url.searchParams.get('chamber'),url.searchParams.get('electorate'),true,url.searchParams.get('council'));}));
    profile.querySelector('[data-local-wards]')?.addEventListener('click',e=>changeLayer('ward',null,true,e.currentTarget.dataset.localWards));
  }
  function renderProfile(r) {
    if(layer==='firstpeoples'){renderRecognitionProfile(r);return;}
    if(isLocal()){renderLocalProfile(r);return;}
    const members=r.members.map(m=>`<p class="vic-member"><strong>${escape(m.name)}</strong><small>${escape(m.party)}</small></p>`).join('');
    const memberText=r.vacancy?'<p><strong>Vacant seat</strong></p><p class="vic-quiet">No sitting Assembly member is listed for this district in the Parliament directory checked 2 October 2026.</p>':members;
    const related=layer==='assembly'?`<p>Legislative Council: <button type="button" data-related-region="${escape(r.regionId)}">${escape(r.regionName)}</button></p>`:`<p>${r.districts.map(d=>`<button type="button" data-related-district="${escape(d.id)}">${escape(d.name)}</button>`).join(' ')}</p>`;
    profile.innerHTML=`<span class="vic-kicker">${layer==='assembly'?'Legislative Assembly · one seat':'Legislative Council · five seats'}</span><h2>${escape(r.name)}</h2><p class="vic-quiet">${escape(r.regionName||'Victoria')} · Boundary edition 2022 · Official code ${escape(r.code)}</p><div class="vic-profile-grid"><section><h3>Current representation</h3>${memberText}<p class="vic-quiet">Parliament member directory · checked 2 October 2026. Sitting members are not a final 2026 candidate list.</p><a href="${escape(data.memberSource)}">Official member directory</a></section><section><h3>Place and evidence</h3>${related}<ul><li><a href="${escape(r.vecUrl)}">VEC electorate information</a></li><li><a href="${escape(r.resultsUrl)}">${escape(r.resultsLabel)}</a></li><li><a href="https://www.parliament.vic.gov.au/teach-and-learn/Resources/electorate-data-cards/">Census data cards: 2021 Census, 2022 boundaries</a></li></ul><p class="vic-quiet">Historical election results and Census observations are dated evidence, separate from current representation.</p></section><section><h3>Work on this place</h3><ul><li><a href="../../../pages/noticeboard-contract-builder.html">Draft a public noticeboard</a></li><li><a href="../../../pages/p4a-builder.html?tool=project-readiness">Draft a local project</a></li><li><a href="../../../pages/c-hour-receipt-builder.html">Record a contribution</a></li><li><a href="../architecture/index.html">Council-first civic architecture</a></li></ul><p class="vic-quiet">These tools create drafts to review and export. They do not publish submissions.</p><button type="button" data-zoom-selected>Zoom to ${escape(r.name)}</button></section></div>`;
    const sourceFacts=document.querySelector(`#${r.id} [data-facts]`);
    if(sourceFacts)profile.append(sourceFacts.cloneNode(true));
    const permalink=new URL(location.href);permalink.searchParams.set('chamber',layer);permalink.searchParams.set('electorate',r.id);for(const key of ['council','recognition','matches','person','view'])permalink.searchParams.delete(key);permalink.hash='';
    const share=document.createElement('p');share.className='vic-quiet';const link=document.createElement('a');link.href=permalink.href;link.textContent='Permanent link to this electorate';share.append(link);profile.append(share);
    profile.querySelectorAll('[data-census-district]').forEach(a=>a.addEventListener('click',event=>{event.preventDefault();changeLayer('assembly',a.dataset.censusDistrict);}));
    profile.querySelector('[data-related-region]')?.addEventListener('click',e=>changeLayer('council',e.currentTarget.dataset.relatedRegion));
    profile.querySelectorAll('[data-related-district]').forEach(b=>b.addEventListener('click',()=>changeLayer('assembly',b.dataset.relatedDistrict)));
    profile.querySelector('[data-zoom-selected]').addEventListener('click',()=>fit(shapes.find(s=>s.id===selected)?.bounds));
  }
  function updateNavigation(id,mode=true) {
    if(!mode)return;
    const u=new URL(location.href);u.searchParams.set('chamber',layer);u.hash='';if(viewMode==='state')u.searchParams.set('view','state');else u.searchParams.delete('view');if(layer==='firstpeoples'){u.searchParams.set('recognition',recognitionEnabled().join(','));if(pickedMatches.length>1)u.searchParams.set('matches',pickedMatches.join(','));else u.searchParams.delete('matches');}else{u.searchParams.delete('recognition');u.searchParams.delete('matches');}if(layer==='ward')u.searchParams.set('council',localScope||'all');else u.searchParams.delete('council');
    if(id)u.searchParams.set('electorate',id);else u.searchParams.delete('electorate');
    if(u.href!==location.href)history[mode==='replace'?'replaceState':'pushState'](null,'',u);currentRoute=mapRoute();
  }
  function select(id,zoomTo=false,updateURL=true,align=zoomTo) {
    if(zoomTo)viewMode='selection';
    const r=record(id);if(!r)return;
    selected=id;renderProfile(r);window.P4A_VIC_DETAILS?.enhance(profile,r,layer);renderList();label.textContent=`${r.name} selected`;
    document.querySelector('[data-selection-status]').textContent=`Selected ${r.name}. Details below the map.`;
    updateNavigation(id,updateURL);
    if(zoomTo)fit(shapes.find(s=>s.id===id)?.bounds);else schedule();if(align)alignMap();
  }
  async function changeLayer(next,id=null,navMode=true,scope=null,align=true,requestedView=null) {
    layerReady=false;pendingReset=false;viewMode=requestedView||(id?'selection':'state');
    if(!['assembly','council','lga','ward','firstpeoples'].includes(next))next='assembly';localScope=next==='ward'?(scope==='all'?null:scope||data.ward.find(r=>r.id===id)?.parentId||null):null;
    const colourControl=document.querySelector('[data-map-colours]');colourControl.disabled=['lga','ward','firstpeoples'].includes(next);document.querySelector('[data-first-peoples-controls]').hidden=next!=='firstpeoples';hoverMatches=[];if(next!=='firstpeoples')pickedMatches=[];if(colourControl.disabled){colourMode='geographic';colourControl.value='geographic';}
    const token=++loadingToken;layer=next;selected=null;hovered=null;shapes=[];search.value='';renderList();representation.legend(colourMode,layer);
    document.querySelectorAll('[data-map-layer]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.mapLayer===layer)));
    profile.innerHTML='<h2>Explore a place</h2><p>Select a boundary or a name to see its representatives, evidence and civic tools.</p>';
    message.hidden=false;message.textContent=`Loading official ${layer==='assembly'?'district':'region'} boundaries…`;schedule(true);
    try {
      const cacheKey=next==='firstpeoples'?next+':'+recognitionEnabled().join(','):next;
      if(!cache.has(cacheKey)){
        const geo=next==='firstpeoples'?{features:(await Promise.all(recognitionEnabled().map(async key=>(await window.P4A_VIC_CODEC.load(key)).features.map(f=>({...f,_sourceLayer:key}))))).flat()}:await window.P4A_VIC_CODEC.load(next);if(geo.features.length!==(next==='firstpeoples'?records().length:data[next].length))throw new Error('Boundary coverage does not match the directory');
        const built=[];
        for(let i=0;i<geo.features.length;i++){
          const f=geo.features[i],p=f.properties,path=new Path2D(),b=[Infinity,Infinity,-Infinity,-Infinity];
          for(const polygon of G.polygons(f.geometry))for(const ring of polygon){ring.forEach((coord,j)=>{const [x,y]=G.project(coord);b[0]=Math.min(b[0],x);b[1]=Math.min(b[1],y);b[2]=Math.max(b[2],x);b[3]=Math.max(b[3],y);if(j===0)path.moveTo(x,y);else path.lineTo(x,y);});path.closePath();}
          built.push({id:next==='firstpeoples'?`vic-${f._sourceLayer}-${p.OBJECTID}`:`vic-${next}-${next==='lga'?p.lga_code:next==='ward'?p.pfi:p.district_code??p.region_code}`,region:p.region_code??(Number(p.lga_code)%8+1),path,bounds:b});
          if(i%8===0)await new Promise(resolve=>setTimeout(resolve,0));
        }
        cache.set(cacheKey,built);
      }
      if(token!==loadingToken)return;
      shapes=cache.get(cacheKey).filter(s=>next!=='ward'||!localScope||record(s.id).parentId===localScope);bounds=shapes.reduce((b,s)=>[Math.min(b[0],s.bounds[0]),Math.min(b[1],s.bounds[1]),Math.max(b[2],s.bounds[2]),Math.max(b[3],s.bounds[3])],[Infinity,Infinity,-Infinity,-Infinity]);
      if(!shapes.length){bounds=null;layerReady=true;pendingReset=false;message.hidden=false;message.textContent='No statutory layer selected. Choose a layer above; this is not a statement about Country or Traditional Owners.';recognitionChooser([],navMode);if(align)alignMap(token);return;}
      baseScale=Math.min((size[0]-60)/(stateBounds[2]-stateBounds[0]),(size[1]-85)/(stateBounds[3]-stateBounds[1]));fit();message.hidden=true;layerReady=true;
      const desired=pendingReset?selected:id||selected;if(desired&&records().some(r=>r.id===desired))select(desired,viewMode!=='state',navMode,false);else if(next==='firstpeoples'&&pickedMatches.length){recognitionChooser(pickedMatches.filter(id=>records().some(r=>r.id===id)),navMode);}else{label.textContent='Hover or tap a boundary to explore';updateNavigation(null,navMode);}
      if(viewMode==='state')fit(stateBounds);pendingReset=false;if(align)alignMap(token);
    }catch(error){if(token!==loadingToken)return;message.textContent='The map could not load. The searchable directory and full text records remain available below. Reload to retry.';console.error('Victoria map:',error);}
  }
  new ResizeObserver(()=>{const old=size;size=[stage.clientWidth,stage.clientHeight];ratio=Math.min(window.devicePixelRatio||1,3);for(const c of [base,canvas]){c.width=Math.round(size[0]*ratio);c.height=Math.round(size[1]*ratio);}if(old[0]){transform.x+=(size[0]-old[0])/2;transform.y+=(size[1]-old[1])/2;}if(bounds)baseScale=Math.min((size[0]-60)/(stateBounds[2]-stateBounds[0]),(size[1]-85)/(stateBounds[3]-stateBounds[1]));schedule(true);}).observe(stage);
  document.querySelectorAll('[data-recognition-layer]').forEach(box=>box.addEventListener('change',()=>{pickedMatches=[];changeLayer('firstpeoples');}));
  document.querySelector('[data-map-colours]').addEventListener('change',e=>{colourMode=e.target.value;representation.legend(colourMode,layer);schedule(true);});
  search.addEventListener('input',renderList);sortField.addEventListener('change',renderList);sortOrder.addEventListener('change',renderList);
  document.querySelectorAll('[data-map-layer]').forEach(b=>b.addEventListener('click',()=>changeLayer(b.dataset.mapLayer)));
  document.querySelector('[data-map-zoom-in]').addEventListener('click',()=>zoom(1.6));document.querySelector('[data-map-zoom-out]').addEventListener('click',()=>zoom(1/1.6));
  document.querySelector('[data-map-reset]').addEventListener('click',resetToVictoria);
  canvas.addEventListener('wheel',e=>{e.preventDefault();zoom(Math.exp(-e.deltaY*.0015),localPoint(e));},{passive:false});
  canvas.addEventListener('pointerdown',e=>{canvas.setPointerCapture(e.pointerId);pointers.set(e.pointerId,localPoint(e));drag={start:localPoint(e),last:localPoint(e),moved:false};if(pointers.size===2){const [a,b]=[...pointers.values()];pinch={distance:Math.hypot(a[0]-b[0],a[1]-b[1]),mid:[(a[0]+b[0])/2,(a[1]+b[1])/2]};}canvas.classList.add('is-dragging');});
  canvas.addEventListener('pointermove',e=>{const p=localPoint(e);if(pointers.has(e.pointerId)){pointers.set(e.pointerId,p);if(pointers.size===2){const[a,b]=[...pointers.values()],distance=Math.hypot(a[0]-b[0],a[1]-b[1]),mid=[(a[0]+b[0])/2,(a[1]+b[1])/2];if(pinch){transform.x+=mid[0]-pinch.mid[0];transform.y+=mid[1]-pinch.mid[1];zoom(distance/Math.max(1,pinch.distance),mid);}pinch={distance,mid};drag.moved=true;}else if(drag){if(Math.hypot(p[0]-drag.start[0],p[1]-drag.start[1])>4)drag.moved=true;if(drag.moved){transform.x+=p[0]-drag.last[0];transform.y+=p[1]-drag.last[1];schedule(true);}drag.last=p;}return;}const matches=pickAll(...p);setHover(matches[0]||null,layer==='firstpeoples'?matches:[]);});
  const release=(e,cancel=false)=>{const p=localPoint(e);if(!cancel&&drag&&!drag.moved&&!pinch){const ids=pickAll(...p);if(layer==='firstpeoples'){pickedMatches=ids;if(ids.length===1)select(ids[0]);else recognitionChooser(ids);}else if(ids[0])select(ids[0]);}pointers.delete(e.pointerId);pinch=null;drag=null;canvas.classList.remove('is-dragging');};
  canvas.addEventListener('pointerup',e=>release(e));canvas.addEventListener('pointercancel',e=>release(e,true));canvas.addEventListener('pointerleave',()=>{if(!drag)setHover(null);});
  canvas.addEventListener('keydown',e=>{const pan={ArrowLeft:[50,0],ArrowRight:[-50,0],ArrowUp:[0,50],ArrowDown:[0,-50]}[e.key];if(pan){e.preventDefault();transform.x+=pan[0];transform.y+=pan[1];schedule(true);}else if(['+','=','-','Home'].includes(e.key)){e.preventDefault();if(e.key==='Home')resetToVictoria();else zoom(e.key==='-'?1/1.6:1.6);}else if(e.key==='Escape'){changeLayer(layer,null,true);}});
  const updateDays=()=>{document.querySelector('[data-vic-days]').textContent=G.daysUntil('2026-11-28T08:00:00+11:00');};updateDays();setInterval(updateDays,60000);
  const restoreNavigation=(mode=false,initial=false)=>{const query=new URLSearchParams(location.search);if(query.get('chamber')==='firstpeoples'){const enabled=(query.get('recognition')??'rap').split(',');document.querySelectorAll('[data-recognition-layer]').forEach(b=>b.checked=enabled.includes(b.dataset.recognitionLayer));pickedMatches=(query.get('matches')||'').split(',').filter(id=>data.firstpeoples.some(r=>r.id===id));}changeLayer(['council','lga','ward','firstpeoples'].includes(query.get('chamber'))?query.get('chamber'):'assembly',query.get('electorate'),mode,query.get('council'),!initial||(!location.hash&&(query.has('electorate')||query.has('chamber'))),query.get('view')==='state'?'state':null);};
  const mapRoute=()=>{const q=new URLSearchParams(location.search);return ['chamber','electorate','council','view','recognition','matches'].map(k=>q.get(k)||'').join('|');};let currentRoute=mapRoute();window.addEventListener('popstate',()=>{const route=mapRoute();if(route!==currentRoute){currentRoute=route;restoreNavigation(false);}});restoreNavigation('replace',true);
  // Read-only test hook: reports the same picker used by pointer events.
  window.P4A_VIC_MAP={compareRecords,pickAllLonLat:(lon,lat)=>{const p=G.project([lon,lat]);return pickAll(p[0]*transform.scale+transform.x,p[1]*transform.scale+transform.y);},pickLonLat:(lon,lat)=>{const p=G.project([lon,lat]);return pick(p[0]*transform.scale+transform.x,p[1]*transform.scale+transform.y);},screenPoint:(lon,lat)=>{const p=G.project([lon,lat]);return[p[0]*transform.scale+transform.x,p[1]*transform.scale+transform.y];},getState:()=>({layer,localScope,colourMode,viewMode,layerReady,stateBounds:[...stateBounds],pickedMatches:[...pickedMatches],enabledRecognition:recognitionEnabled(),selected,hovered,count:shapes.length,transform:{...transform}})};
})();
