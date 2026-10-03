/* VIC1: exact integer-microdegree deltas, zig-zag varints, gzip transport.
   Source GeoJSON is retained; encoder rejects any non-exact numeric round-trip. */
(function(root){
  'use strict';
  function decode(buffer){
    const bytes=new Uint8Array(buffer),view=new DataView(buffer);
    const magic=String.fromCharCode(...bytes.subarray(0,4));if(bytes.length<8||!['VIC1','VIC2'].includes(magic))throw new Error('Invalid Victoria geometry header');
    const length=view.getUint32(4,true);let cursor=8+length;
    if(cursor>bytes.length)throw new Error('Truncated Victoria geometry header');
    const meta=JSON.parse(new TextDecoder().decode(bytes.subarray(8,cursor)));
    const fullDouble=magic==='VIC2';if(fullDouble?meta.encoding!=='vic-float64-v1':meta.encoding!=='vic-delta-v1'||meta.scale!==1000000)throw new Error('Unsupported Victoria geometry encoding');
    const integer=()=>{let n=0,shift=0,b;do{if(cursor>=bytes.length||shift>28)throw new Error('Invalid geometry delta');b=bytes[cursor++];n|=(b&127)<<shift;shift+=7;}while(b&128);return(n>>>1)^-(n&1);};
    const features=meta.features.map(f=>{const polygons=f.rings.map(p=>p.map(count=>{const ring=new Array(count);let x=0,y=0;for(let i=0;i<count;i++){if(fullDouble){if(cursor+16>bytes.length)throw new Error('Truncated float64 coordinates');ring[i]=[view.getFloat64(cursor,true),view.getFloat64(cursor+8,true)];cursor+=16;}else{x+=integer();y+=integer();ring[i]=[x/meta.scale,y/meta.scale];}}return ring;}));return{type:'Feature',id:f.id,properties:f.properties,geometry:{type:f.type,coordinates:f.type==='Polygon'?polygons[0]:polygons}};});
    if(cursor!==bytes.length)throw new Error('Unexpected trailing geometry bytes');
    return{type:'FeatureCollection',features};
  }
  async function load(layer){
    const prefix='../../../assets/maps/vic-'+layer;
    // Classic local scripts are permitted under file://; fetch/XHR are not.
    // This contains the same lossless binary as HTTP delivery, without gzip.
    if(location.protocol==='file:'){
      if(!root.P4A_VIC_FILE_GEOMETRY?.[layer])await new Promise((resolve,reject)=>{const script=document.createElement('script');script.src=prefix+'.vic.js';script.onload=resolve;script.onerror=()=>reject(new Error('Local boundary script unavailable'));document.head.append(script);});
      const encoded=root.P4A_VIC_FILE_GEOMETRY?.[layer];if(!encoded)throw new Error('Local boundary data missing');
      const text=atob(encoded),bytes=new Uint8Array(text.length);for(let i=0;i<text.length;i++)bytes[i]=text.charCodeAt(i);
      return decode(bytes.buffer);
    }

    if(typeof DecompressionStream!=='undefined'){
      try{
        const response=await fetch(prefix+'.vic.gz');if(!response.ok)throw new Error('Compressed geometry unavailable');
        const compressed=await response.arrayBuffer();const b=new Uint8Array(compressed);
        // Some servers add Content-Encoding and the browser decompresses first.
        const binary=b[0]===31&&b[1]===139?await new Response(new Blob([compressed]).stream().pipeThrough(new DecompressionStream('gzip'))).arrayBuffer():compressed;
        return decode(binary);
      }catch(error){console.warn('Compressed map unavailable; loading original source geometry.',error.message);}
    }
    const response=await fetch(prefix+'.geojson');if(!response.ok)throw new Error('Boundary geometry unavailable');return response.json();
  }
  root.P4A_VIC_CODEC={decode,load};if(typeof module!=='undefined')module.exports={decode};
})(globalThis);
