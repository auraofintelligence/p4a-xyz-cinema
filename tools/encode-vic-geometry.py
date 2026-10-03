"""Lossless microdegree delta/varint encoding; fails if a source value cannot
round-trip exactly. Original source files remain untouched for provenance."""
import pathlib,json,gzip,struct,hashlib,base64
ROOT=pathlib.Path(__file__).resolve().parents[1]
def encode_float64(source):
 meta={'encoding':'vic-float64-v1','features':[]};body=bytearray();count=0
 for f in source['features']:
  geo=f['geometry'];polys=[geo['coordinates']] if geo['type']=='Polygon' else geo['coordinates']
  meta['features'].append({'id':f.get('id'),'properties':f['properties'],'type':geo['type'],'rings':[[len(r) for r in p] for p in polys]})
  for polygon in polys:
   for ring in polygon:
    for point in ring:
     assert len(point)==2
     body.extend(struct.pack('<dd',*point));count+=1
 header=json.dumps(meta,separators=(',',':'),ensure_ascii=False).encode('utf-8')
 return b'VIC2'+struct.pack('<I',len(header))+header+body,count

def encode(source):
 meta={'encoding':'vic-delta-v1','scale':1000000,'features':[]};body=bytearray();count=0
 def varint(n):
  u=2*n if n>=0 else -2*n-1
  while u>=128:body.append((u&127)|128);u>>=7
  body.append(u)
 for f in source['features']:
  geo=f['geometry'];polys=[geo['coordinates']] if geo['type']=='Polygon' else geo['coordinates']
  meta['features'].append({'id':f.get('id'),'properties':f['properties'],'type':geo['type'],'rings':[[len(r) for r in p] for p in polys]})
  for polygon in polys:
   for ring in polygon:
    last=[0,0]
    for point in ring:
     assert len(point)==2
     for axis,v in enumerate(point):
      n=round(v*1000000);assert n/1000000==v,('Cannot encode without rounding',v)
      varint(n-last[axis]);last[axis]=n
     count+=1
 header=json.dumps(meta,separators=(',',':'),ensure_ascii=False).encode('utf-8')
 return b'VIC1'+struct.pack('<I',len(header))+header+body,count
def main():
 report={}
 for layer in ['assembly','council','lga','ward','rap','rsa']:
  p=ROOT/f'assets/maps/vic-{layer}.geojson';raw=p.read_bytes();binary,count=(encode_float64 if layer in ['rap','rsa'] else encode)(json.loads(raw));compressed=gzip.compress(binary,compresslevel=9,mtime=0)
  dest=ROOT/f'assets/maps/vic-{layer}.vic.gz';dest.write_bytes(compressed)
  local_script='window.P4A_VIC_FILE_GEOMETRY = window.P4A_VIC_FILE_GEOMETRY || {}; window.P4A_VIC_FILE_GEOMETRY.'+layer+' = '+json.dumps(base64.b64encode(binary).decode('ascii'))+';\n'
  (ROOT/f'assets/maps/vic-{layer}.vic.js').write_bytes(local_script.encode('ascii'))
  report[layer]={'encoding':'vic-float64-v1' if layer in ['rap','rsa'] else 'vic-delta-v1','file':dest.name,'sourceSha256':hashlib.sha256(raw).hexdigest(),'encodedSha256':hashlib.sha256(compressed).hexdigest(),'sourceBytes':len(raw),'binaryBytes':len(binary),'gzipBytes':len(compressed),'vertices':count,'fileScriptBytes':len(local_script.encode('ascii')),'reductionPercent':round(100*(1-len(compressed)/len(raw)),2)}
 (ROOT/'assets/maps/vic-delivery.json').write_text(json.dumps({'format':'VIC1 microdegree deltas or VIC2 original float64 values','lossless':True,'sourceCoordinateRoundTrip':'VIC1 requires exact integer-microdegree round-trip; VIC2 stores original IEEE754 float64 values. Neither format rounds or simplifies any coordinate.','layers':report},indent=2)+'\n',encoding='utf-8')
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()
