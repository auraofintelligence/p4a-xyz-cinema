// Exercise the actual delivered loader, including gzip-only large layers.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {gzipSync} from 'node:zlib';
const source=fs.readFileSync(new URL('../assets/civic-places.js',import.meta.url),'utf8');
const body=source.match(/  async function fetchGeometry\(entry\) \{([\s\S]*?)\n  \}\n  async function loadLayer/);
assert.ok(body,'Delivered geometry loader must be discoverable for these checks');
const AsyncFunction=Object.getPrototypeOf(async function(){}).constructor;
const loader=new AsyncFunction('entry','siteRoot','fetch','DecompressionStream',body[1]);
const fixture={type:'FeatureCollection',features:[{type:'Feature',properties:{code:'island'},geometry:{type:'Polygon',coordinates:[[[150,-30],[151,-30],[150,-29],[150,-30]]]}}]};
const plain=JSON.stringify(fixture),compressed=gzipSync(plain),base=new URL('https://fixture.invalid/');
async function run(entry,responses,support=DecompressionStream){
 const calls=[];
 const fetch=async url=>{calls.push(String(url));const value=responses[new URL(url).pathname];return value===undefined?new Response('',{status:404}):new Response(value);};
 return {value:await loader(entry,base,fetch,support),calls};
}
for(const bytes of [compressed,plain]){
 const result=await run({geometryFile:'exact.geojson.gz',compressedFile:'exact.geojson.gz'},{'/exact.geojson.gz':bytes});
 assert.deepEqual(result.value,fixture);assert.equal(result.calls.length,1);
}
const fallback=await run({geometryFile:'exact.geojson',compressedFile:'exact.geojson.gz'},{'/exact.geojson.gz':'bad gzip source', '/exact.geojson':plain});
assert.deepEqual(fallback.value,fixture);assert.equal(fallback.calls.length,2);
const calls=[];
await assert.rejects(loader({geometryFile:'exact.geojson.gz',compressedFile:'exact.geojson.gz'},base,async url=>{calls.push(String(url));return new Response('bad data');},DecompressionStream));
assert.equal(calls.length,1,'A gzip-only failure must not download the same large asset twice');
await assert.rejects(loader({geometryFile:'exact.geojson.gz',compressedFile:'exact.geojson.gz'},base,()=>{throw Error('No fetch expected');},undefined),/linked text directory/);
const plainOnly=await run({geometryFile:'exact.geojson'},{'/exact.geojson':plain},null);
assert.deepEqual(plainOnly.value,fixture);
console.log('PASS: actual geometry loader handles gzip-only, server-decoded JSON, plain fallback, single-request failure and unsupported-browser text guidance.');
