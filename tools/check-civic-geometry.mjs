/* Exercise the actual Canvas controller with independent holes/island fixtures. */
import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const ring=(x,y,w,h)=>[[x,y],[x+w,y],[x+w,y+h],[x,y+h],[x,y]];
const fixture={type:'FeatureCollection',features:[
 {type:'Feature',properties:{code:'a'},geometry:{type:'Polygon',coordinates:[ring(0,0,10,10),ring(3,3,4,4)]}},
 {type:'Feature',properties:{code:'b'},geometry:{type:'MultiPolygon',coordinates:[[ring(20,0,2,2)],[ring(30,0,2,2)]]}},
 {type:'Feature',properties:{code:'c'},geometry:{type:'Polygon',coordinates:[ring(10,0,2,10)]}},
 {type:'Feature',properties:{code:'b-detached'},geometry:{type:'Polygon',coordinates:[ring(40,0,2,2)]}}
]};
class Element {
 constructor(){this.events={};this.children=[];this.dataset={};this.style={};this.attrs={};this.hidden=false;this.value='';}
 addEventListener(name,fn){this.events[name]=fn;}
 setAttribute(k,v){this.attrs[k]=v;}
 getAttribute(k){return this.attrs[k];}
 append(...values){this.children.push(...values);}
 replaceChildren(...values){this.children=values;}
 getBoundingClientRect(){return{width:1000,height:540,left:0,top:0};}
 getContext(){return new Proxy({},{get:()=>()=>{},set:()=>true});}
 querySelector(selector){return controls[selector]??=new Element();}
}
const controls={};const root=new Element();const canvas=new Element();controls.canvas=canvas;
const config={siteRoot:'http://localhost/',filterGeometry:true,layers:[{id:'fixture',name:'Synthetic geography fixture',geometryFile:'fixture.geojson',featureIdField:'code'}],places:['a','b','c'].map(id=>({id,name:id,kind:'fixture',layerId:'fixture',featureId:id,url:`${id}.html`,members:[]})),basemap:{},selectedId:'a'};
config.places[1].featureIds=['b','b-detached'];
const location={href:'http://localhost/a.html'};
const context={window:{devicePixelRatio:2},document:{querySelectorAll:()=>[],querySelector:()=>root,getElementById:()=>({textContent:JSON.stringify(config)}),createElement:()=>new Element()},URL,URLSearchParams,Map,Set,Intl,Date,JSON,Number,String,Math,console,location,history:{pushState:(_a,_b,url)=>{location.href=String(url);},replaceState:(_a,_b,url)=>{location.href=String(url);}},fetch:async()=>({ok:true,json:async()=>fixture}),Path2D:class{moveTo(){}lineTo(){}closePath(){}},ResizeObserver:class{constructor(fn){this.fn=fn;}observe(){this.fn();}},requestAnimationFrame:fn=>{queueMicrotask(fn);return 1;},addEventListener:()=>{},setTimeout,clearTimeout,setInterval:()=>{}};
vm.runInNewContext(fs.readFileSync(new URL('../assets/civic-places.js',import.meta.url),'utf8'),context);
await new Promise(resolve=>setTimeout(resolve,20));
const map=context.window.P4A_CIVIC_MAP;
assert.equal(map.getState().shapes,4);
assert.equal(map.getState().areas,3,'Several official features share one searchable page');
for(const [p,expected] of [[[1,1],'a'],[[5,5],null],[[20.5,1],'b'],[[31,1],'b'],[[41,1],'b'],[[11,5],'c'],[[15,15],null]])assert.equal(map.pickLonLat(p),expected,`hole/island/neighbour fixture ${p}`);
for(const p of [[153.25,-27.5],[115.86,-31.95],[147.33,-42.88]]){
 const actual=map.inverse(map.project(p));assert.ok(Math.abs(actual[0]-p[0])<1e-10&&Math.abs(actual[1]-p[1])<1e-10);
}
const before=map.getState().view.scale;
controls['[data-civic-zoom-in]'].events.click();assert.ok(map.getState().view.scale>before);
controls['[data-civic-reset]'].events.click();assert.equal(map.getState().selected,'a');
// A bare detail URL must restore its own initial edition on browser Back,
// even when a different edition appears first in the available-layer list.
const navigationEvents={};
context.addEventListener=(name,handler)=>{navigationEvents[name]=handler;};
context.window={devicePixelRatio:2};
config.layers.unshift({...config.layers[0],id:'alternate-edition'});
config.initialLayer='fixture';
location.href='http://localhost/a.html';
vm.runInNewContext(fs.readFileSync(new URL('../assets/civic-places.js',import.meta.url),'utf8'),context);
await new Promise(resolve=>setTimeout(resolve,20));
assert.equal(context.window.P4A_CIVIC_MAP.getState().layer,'fixture');
location.href='http://localhost/a.html?layer=alternate-edition';
navigationEvents.popstate();
await new Promise(resolve=>setTimeout(resolve,20));
assert.equal(context.window.P4A_CIVIC_MAP.getState().layer,'alternate-edition');
location.href='http://localhost/a.html';
navigationEvents.popstate();
await new Promise(resolve=>setTimeout(resolve,20));
assert.equal(context.window.P4A_CIVIC_MAP.getState().layer,'fixture');
assert.equal(context.window.P4A_CIVIC_MAP.getState().selected,'a');
console.log('PASS: delivered controller handles holes, multipart parts, shared place features, neighbour/water, projection, zoom/reset and Back to a bare detail URL with a different initial edition. Synthetic fixtures do not certify every real polygon.');
