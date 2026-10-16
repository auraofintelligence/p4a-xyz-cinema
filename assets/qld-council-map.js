/* Self-similar place atlas. 17 Oct 2026. Canvas and official PNG map exports; no SVG.
 * All paths and picking use the same retained Qld Government source geometry.
 */
(() => {
  const normal=text=>String(text).normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,' ').trim();
  // EPSG:3857, matching the official geographic PNG base map exactly.
  const radius=6378137,rad=Math.PI/180;
  const project=([lon,lat])=>[radius*lon*rad,-radius*Math.log(Math.tan(Math.PI/4+Math.max(-85,Math.min(85,lat))*rad/2))];
  const invert=([x,y])=>[x/radius/rad,(2*Math.atan(Math.exp(-y/radius))-Math.PI/2)/rad];
  const polygons=geometry=>geometry.type==='Polygon'?[geometry.coordinates]:geometry.coordinates;
  // Stable colours distinguish places; they do not encode parties or rankings.
  const councilColours=['100,171,205','108,185,144','211,167,93','181,141,206','214,137,161','94,181,174','222,159,110','133,153,212'];
  const atlasHooks=[];
  document.querySelectorAll('[data-qld-council-map]').forEach(root=>{
  const divisions=root.dataset.mapLevel==='division';
  const bundle=divisions?window.P4A_REDLAND_DIVISIONS:window.P4A_QLD_COUNCILS;
  if(!bundle)return;
  const queryKey=divisions?'division':'council';
  const items=bundle.features.map(feature=>{
    const path=new Path2D(),bounds=[Infinity,Infinity,-Infinity,-Infinity];
    for(const polygon of polygons(feature.geometry))for(const ring of polygon){
      ring.forEach((point,i)=>{const [x,y]=project(point);i?path.lineTo(x,y):path.moveTo(x,y);bounds[0]=Math.min(bounds[0],x);bounds[1]=Math.min(bounds[1],y);bounds[2]=Math.max(bounds[2],x);bounds[3]=Math.max(bounds[3],y);});path.closePath();
    }
    const p=feature.properties;
    const id=String(p.lga_code);
    return {id,name:p.lga,path,bounds,colour:councilColours[(divisions?Number(id):Math.floor(Number(id)/10))%councilColours.length],kind:divisions?'Redland City council division':id==='7300'?'Town authority area':'Local government council',search:normal(p.lga+' '+p.abbrev_name+' '+id+(!divisions&&id==='6250'?' Redlands Minjerribah North Stradbroke Russell Macleay Coochiemudlo':'')),built:divisions||id==='6250'};
  }).sort((a,b)=>a.name.localeCompare(b.name,undefined,{numeric:true}));
  const allBounds=items.reduce((b,item)=>[Math.min(b[0],item.bounds[0]),Math.min(b[1],item.bounds[1]),Math.max(b[2],item.bounds[2]),Math.max(b[3],item.bounds[3])],[Infinity,Infinity,-Infinity,-Infinity]);
    const canvas=root.querySelector('canvas'),ctx=canvas.getContext('2d'),hit=document.createElement('canvas').getContext('2d');
    if(divisions)for(const item of items){
      const b=item.bounds,centre=[(b[0]+b[2])/2,(b[1]+b[3])/2];
      const candidates=[];
      for(let x=1;x<10;x++)for(let y=1;y<10;y++){
        const point=[b[0]+(b[2]-b[0])*x/10,b[1]+(b[3]-b[1])*y/10];
        if(hit.isPointInPath(item.path,...point,'evenodd'))candidates.push(point);
      }
      candidates.sort((a,c)=>Math.hypot(a[0]-centre[0],a[1]-centre[1])-Math.hypot(c[0]-centre[0],c[1]-centre[1]));
      item.labelPoint=candidates[0];
    }
    const input=root.querySelector('[data-council-search]'),results=root.querySelector('[data-council-results]'),counter=root.querySelector('[data-council-count]'),label=root.querySelector('[data-map-label]');
    const panel=root.querySelector('[data-council-selection]'),name=panel.querySelector('[data-selection-name]'),kind=panel.querySelector('[data-selection-kind]'),copy=panel.querySelector('[data-selection-copy]'),open=panel.querySelector('[data-open-council]');
    const load=root.querySelector('[data-map-loading]');
    const baseStatus=root.querySelector('[data-basemap-status]');
    const base=bundle.basemap,roadsButton=root.querySelector('[data-map-roads]');
    let showRoads=false;
    const currentBase=()=>showRoads&&base?.roads?base.roads:base;
    const baseImage=base?new Image():null;
    let detailImage=null,detailExtent=null,baseTimer=null,baseRequest=0,basemapController=null;
    let width=1,height=1,scale=1,offsetX=0,offsetY=0,selected=null,hover=null,drawQueued=false,resizeBounds=allBounds;
    let baseScale=1,gesture=null,dragged=false;
    const pointers=new Map();
    const screen=point=>[point[0]*scale+offsetX,point[1]*scale+offsetY];
    const world=point=>[(point[0]-offsetX)/scale,(point[1]-offsetY)/scale];
    const position=event=>{const box=canvas.getBoundingClientRect();return [event.clientX-box.left,event.clientY-box.top];};
    function paintRaster(image,extent){
      if(!image?.complete||!image.naturalWidth)return;
      const topLeft=screen([extent.xmin,-extent.ymax]),bottomRight=screen([extent.xmax,-extent.ymin]);
      ctx.drawImage(image,topLeft[0],topLeft[1],bottomRight[0]-topLeft[0],bottomRight[1]-topLeft[1]);
    }
    function refreshRaster(){
      if(!base)return;
      clearTimeout(baseTimer);
      baseTimer=setTimeout(async()=>{
        basemapController?.abort();basemapController=new AbortController();const request=++baseRequest;
        const lower=world([0,height]),upper=world([width,0]);
        const activeBase=currentBase();
        const endpoint=new URL(activeBase.serviceURL.replace(/\/$/,'')+'/export');
        const dpr=window.devicePixelRatio||1;
        endpoint.search=new URLSearchParams({bbox:[lower[0],-lower[1],upper[0],-upper[1]].join(','),bboxSR:'3857',imageSR:'3857',size:`${Math.min(3000,Math.round(width*dpr))},${Math.min(2000,Math.round(height*dpr))}`,format:'png32',transparent:'false',f:'json'}).toString();
        try{
          const response=await fetch(endpoint,{signal:basemapController.signal});if(!response.ok)throw Error('Map service unavailable');
          const result=await response.json();if(!result.href||!result.extent)throw Error('Map service returned no image');
          const image=new Image();
          image.onload=()=>{if(request!==baseRequest)return;detailImage=image;detailExtent=result.extent;queue();baseStatus.textContent=showRoads?'Detailed roads · official Queensland topographic map':'Quiet map · official Queensland geographic base';};
          image.onerror=()=>{if(request===baseRequest)baseStatus.textContent='Retained official base map shown; online detail could not load.';};
          image.src=result.href;
        }catch(error){if(error.name!=='AbortError')baseStatus.textContent='Retained official base map shown; online detail unavailable.';}
      },220);
    }
    function fit(bounds){
      const padding=30;
      scale=Math.min((width-padding*2)/Math.max(bounds[2]-bounds[0],.003),(height-padding*2)/Math.max(bounds[3]-bounds[1],.003));
      offsetX=width/2-(bounds[0]+bounds[2])/2*scale;offsetY=height/2-(bounds[1]+bounds[3])/2*scale;
      resizeBounds=bounds;queue();refreshRaster();
    }
    function queue(){if(!drawQueued){drawQueued=true;requestAnimationFrame(draw);}}
    function draw(){
      drawQueued=false;
      const dpr=window.devicePixelRatio||1;
      ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,canvas.width,canvas.height);
      ctx.setTransform(dpr,0,0,dpr,0,0);ctx.fillStyle='#d6eaf1';ctx.fillRect(0,0,width,height);
      if(base)paintRaster(baseImage,currentBase().extent);
      if(detailImage)paintRaster(detailImage,detailExtent);
      ctx.setTransform(dpr*scale,0,0,dpr*scale,dpr*offsetX,dpr*offsetY);
      const visible=[world([0,0]),world([width,height])];
      for(const item of items){
        const b=item.bounds;if(b[2]<visible[0][0]||b[0]>visible[1][0]||b[3]<visible[0][1]||b[1]>visible[1][1])continue;
        ctx.fillStyle=item===selected?'rgba(255,197,30,.25)':item===hover?`rgba(${item.colour},.34)`:`rgba(${item.colour},.18)`;
        ctx.fill(item.path,'evenodd');ctx.lineWidth=(item===selected?2.8:1.1)/scale;ctx.strokeStyle=item===selected?'#8b3e00':'#704278';ctx.stroke(item.path);
      }
      if(selected){ctx.lineWidth=2.5/scale;ctx.strokeStyle='#8b3e00';ctx.stroke(selected.path);}
      if(divisions){
        ctx.setTransform(dpr,0,0,dpr,0,0);ctx.font='bold 12px system-ui';ctx.textAlign='center';ctx.textBaseline='middle';
        for(const item of items){
          if(!item.labelPoint)continue;
          const [x,y]=screen(item.labelPoint);
          if(x<15||x>width-15||y<15||y>height-15)continue;
          ctx.beginPath();ctx.arc(x,y,12,0,Math.PI*2);ctx.fillStyle=item===selected?'#ffe18c':'#fffdf5eb';ctx.fill();
          ctx.lineWidth=1;ctx.strokeStyle='#704278';ctx.stroke();ctx.fillStyle='#40234d';ctx.fillText(item.id,x,y+.5);
        }
      }
      label.textContent=hover&&hover!==selected?hover.name:selected?selected.name+' · selected':divisions?'Redlands · click a division':'Queensland · click a council boundary';
    }
    function pick(point){
      const [x,y]=world(point);hit.setTransform(1,0,0,1,0,0);
      return items.find(item=>x>=item.bounds[0]&&x<=item.bounds[2]&&y>=item.bounds[1]&&y<=item.bounds[3]&&hit.isPointInPath(item.path,x,y,'evenodd'))||null;
    }
    function updateUrl(){
      const url=new URL(location.href);
      selected?url.searchParams.set(queryKey,selected.id):url.searchParams.delete(queryKey);
      history.replaceState(null,'',url);
    }
    function renderResults(){
      const terms=normal(input.value).split(' ').filter(Boolean);
      const matched=items.filter(item=>terms.every(term=>item.search.includes(term)));
      counter.textContent=terms.length?`${matched.length} matching ${matched.length===1?'area':'areas'}`:divisions?'10 council divisions':'77 councils + Weipa Town area';
      results.replaceChildren();
      for(const item of matched){
        const li=document.createElement('li'),button=document.createElement('button');button.type='button';button.className='atlas-result';button.dataset.councilId=item.id;button.setAttribute('aria-pressed',String(item===selected));
        button.append(document.createTextNode(item.name));
        if(item.built||(!divisions&&item.id==='7300')){const detail=document.createElement('small');detail.textContent=item.built?'Local journey available':'Town authority area';button.append(detail);}
        button.addEventListener('click',()=>select(item,true));li.append(button);results.append(li);
      }
      root.querySelector('[data-council-no-results]').hidden=matched.length!==0;
    }
    function select(item,zoom){
      selected=item;hover=null;panel.hidden=false;name.textContent=item.name;kind.textContent=item.kind;
      copy.textContent=divisions?'Follow this division into local questions, its current representative, source records and connected possibilities.':item.built?'Open the Redlands local journey: maps, statistics, questions, systems, people, participation and outcomes.':'Council selected. Its P4A local journey has not been built yet. The same place pattern can be extended here; use the official boundary and council references below.';
      if(!divisions&&item.id==='7300')copy.textContent='Weipa Town has a town authority rather than an elected local government council. It is retained as a separately labelled area in the official boundary layer.';
      open.hidden=!item.built;
      if(divisions){open.textContent='Open '+item.name;open.href=new URL(`states/qld/councils/redland/divisions/${item.id}/index.html`,new URL(root.dataset.siteRoot,location.href)).href;}
      if(zoom)fit(item.bounds);else queue();
      renderResults();updateUrl();
    }
    function zoom(factor,anchor=[width/2,height/2]){
      const before=world(anchor),next=Math.max(baseScale*.7,Math.min(scale*factor,baseScale*500));
      scale=next;offsetX=anchor[0]-before[0]*scale;offsetY=anchor[1]-before[1]*scale;resizeBounds=null;queue();refreshRaster();
    }
    function reset(){selected=null;hover=null;input.value='';panel.hidden=true;fit(allBounds);renderResults();updateUrl();}
    root.querySelector('[data-map-reset]').addEventListener('click',reset);
    root.querySelector('[data-map-zoom-in]').addEventListener('click',()=>zoom(1.6));
    root.querySelector('[data-map-zoom-out]').addEventListener('click',()=>zoom(1/1.6));
    root.querySelector('[data-map-seq]')?.addEventListener('click',()=>{const [x0,y0]=project([151.6,-25.9]),[x1,y1]=project([154,-28.5]);fit([x0,y0,x1,y1]);});
    root.querySelector('[data-map-redland]')?.addEventListener('click',()=>{input.value='Redland';select(items.find(item=>item.id==='6250'),true);});
    function loadBase(){
      if(!baseImage)return;
      baseImage.src=new URL(currentBase().image,new URL(root.dataset.siteRoot,location.href)).href;
    }
    if(roadsButton){
      roadsButton.disabled=!base?.roads;
      roadsButton.addEventListener('click',()=>{
        showRoads=!showRoads;roadsButton.setAttribute('aria-pressed',String(showRoads));
        basemapController?.abort();clearTimeout(baseTimer);baseRequest++;
        detailImage=null;detailExtent=null;loadBase();queue();refreshRaster();
        baseStatus.textContent=showRoads?'Detailed roads · loading official topographic map':'Quiet map · loading official geographic base';
      });
    }
    input.disabled=false;input.addEventListener('input',renderResults);input.addEventListener('keydown',event=>{if(event.key==='Enter'){const first=results.querySelector('button');if(first)first.click();event.preventDefault();}});
    canvas.addEventListener('wheel',event=>{event.preventDefault();zoom(Math.exp(-event.deltaY*.0015),position(event));},{passive:false});
    canvas.addEventListener('pointerdown',event=>{
      if(event.button!==0&&event.pointerType==='mouse')return;
      canvas.focus({preventScroll:true});canvas.setPointerCapture(event.pointerId);pointers.set(event.pointerId,position(event));
      if(pointers.size===1){gesture={start:position(event),last:position(event)};dragged=false;}
      else{gesture={points:[...pointers.values()],scale,offsetX,offsetY};dragged=true;}
    });
    canvas.addEventListener('pointermove',event=>{
      const point=position(event);
      if(!pointers.has(event.pointerId)){if(event.pointerType==='mouse'){const next=pick(point);if(next!==hover){hover=next;canvas.style.cursor=next?'pointer':'grab';queue();}}return;}
      const last=pointers.get(event.pointerId);pointers.set(event.pointerId,point);
      if(pointers.size===1&&gesture?.last){
        if(Math.hypot(point[0]-gesture.start[0],point[1]-gesture.start[1])>5)dragged=true;
        if(dragged){offsetX+=point[0]-last[0];offsetY+=point[1]-last[1];resizeBounds=null;queue();}
        gesture.last=point;
      }else if(pointers.size===2&&gesture?.points){
        const now=[...pointers.values()],old=gesture.points;
        const oldMid=[(old[0][0]+old[1][0])/2,(old[0][1]+old[1][1])/2],mid=[(now[0][0]+now[1][0])/2,(now[0][1]+now[1][1])/2];
        const distance=pair=>Math.max(1,Math.hypot(pair[1][0]-pair[0][0],pair[1][1]-pair[0][1]));
        scale=Math.max(baseScale*.7,Math.min(gesture.scale*distance(now)/distance(old),baseScale*500));
        offsetX=mid[0]-(oldMid[0]-gesture.offsetX)/gesture.scale*scale;offsetY=mid[1]-(oldMid[1]-gesture.offsetY)/gesture.scale*scale;resizeBounds=null;queue();
      }
    });
    function finish(event){
      const point=position(event),single=pointers.size===1;
      pointers.delete(event.pointerId);
      if(event.type==='pointerup'&&single&&!dragged){const item=pick(point);if(item)select(item,false);}
      if(pointers.size===1){const remaining=[...pointers.values()][0];gesture={start:remaining,last:remaining};dragged=true;}
      else if(pointers.size===0)gesture=null;
      if(pointers.size===0&&dragged)refreshRaster();
    }
    canvas.addEventListener('pointerup',finish);canvas.addEventListener('pointercancel',finish);
    canvas.addEventListener('pointerleave',()=>{if(!pointers.size){hover=null;queue();}});
    canvas.addEventListener('dblclick',event=>{const item=pick(position(event));if(item)select(item,true);else zoom(2,position(event));});
    canvas.addEventListener('keydown',event=>{
      const delta=55;
      if(event.key==='+'||event.key==='=')zoom(1.6);else if(event.key==='-')zoom(1/1.6);
      else if(event.key==='ArrowLeft')offsetX+=delta;else if(event.key==='ArrowRight')offsetX-=delta;else if(event.key==='ArrowUp')offsetY+=delta;else if(event.key==='ArrowDown')offsetY-=delta;
      else if(event.key.toLowerCase()==='r'){reset();event.preventDefault();return;}else return;
      event.preventDefault();resizeBounds=null;queue();refreshRaster();
    });
    function resize(){
      const box=canvas.getBoundingClientRect(),previous=[width/2,height/2],centre=world(previous);
      width=box.width;height=box.height;
      const dpr=window.devicePixelRatio||1;canvas.width=Math.round(width*dpr);canvas.height=Math.round(height*dpr);
      baseScale=Math.min((width-60)/(allBounds[2]-allBounds[0]),(height-60)/(allBounds[3]-allBounds[1]));
      if(resizeBounds)fit(resizeBounds);else{offsetX=width/2-centre[0]*scale;offsetY=height/2-centre[1]*scale;queue();refreshRaster();}
    }
    if(baseImage){baseImage.onload=()=>queue();baseImage.onerror=()=>{baseStatus.textContent='The retained geographic map could not load. Refresh or check the original source.';};loadBase();}
    new ResizeObserver(resize).observe(canvas);resize();renderResults();load.hidden=true;
    const requested=new URLSearchParams(location.search).get(queryKey);
    const initial=items.find(item=>item.id===requested||normal(item.name)===normal(requested||''));if(initial)select(initial,true);
    atlasHooks.push({level:divisions?'division':'council',getState:()=>({selected:selected?.id||null,name:selected?.name||null,scale,offsetX,offsetY,width,height,count:items.length,results:results.children.length,showRoads}),screenPoint:(lon,lat)=>screen(project([lon,lat])),pickLonLat:(lon,lat)=>{const p=screen(project([lon,lat]));return pick(p)?.id||null;}});
  });
  const hookFor=level=>{const hook=atlasHooks.find(item=>item.level===level);return hook?{getState:hook.getState,screenPoint:hook.screenPoint,pickLonLat:hook.pickLonLat}:null;};
  window.P4A_QLD_MAP=hookFor('council');window.P4A_REDLAND_MAP=hookFor('division');
})();
