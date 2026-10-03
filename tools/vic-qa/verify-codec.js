const fs=require('fs'),path=require('path'),zlib=require('zlib'),assert=require('assert');
const root=process.argv[2],codec=require(path.join(root,'assets/vic-geometry-codec.js'));
let vertices=0;
for(const layer of ['assembly','council','lga','ward','rap','rsa']){
 const raw=JSON.parse(fs.readFileSync(path.join(root,`assets/maps/vic-${layer}.geojson`),'utf8'));
 const binary=zlib.gunzipSync(fs.readFileSync(path.join(root,`assets/maps/vic-${layer}.vic.gz`)));
 const decoded=codec.decode(binary.buffer.slice(binary.byteOffset,binary.byteOffset+binary.byteLength));
 assert.equal(raw.features.length,decoded.features.length);
 raw.features.forEach((f,i)=>{assert.deepStrictEqual(decoded.features[i].geometry,f.geometry);assert.deepStrictEqual(decoded.features[i].properties,f.properties);for(const p of (f.geometry.type==='Polygon'?[f.geometry.coordinates]:f.geometry.coordinates))for(const r of p)vertices+=r.length;});
 const sandbox={window:{}};require('vm').runInNewContext(fs.readFileSync(path.join(root,`assets/maps/vic-${layer}.vic.js`),'utf8'),sandbox);assert.deepStrictEqual(Buffer.from(sandbox.window.P4A_VIC_FILE_GEOMETRY[layer],'base64'),binary);
 console.log(layer+': every coordinate, ring, polygon and property round-trips exactly.');
}
console.log('Verified vertices:',vertices);
