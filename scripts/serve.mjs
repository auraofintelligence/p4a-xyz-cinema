// Local preview only. Added 17 October 2026. No dependencies or network writes.
import http from 'node:http';
import {createReadStream} from 'node:fs';
import {stat,realpath} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const port=Number(process.env.P4A_PREVIEW_PORT || 8768);
const types={'.mjs':'text/javascript; charset=utf-8','.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.json':'application/json; charset=utf-8','.md':'text/plain; charset=utf-8','.txt':'text/plain; charset=utf-8','.xml':'application/xml; charset=utf-8','.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.webp':'image/webp','.svg':'image/svg+xml','.pdf':'application/pdf','.woff2':'font/woff2','.xlsx':'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'};
http.createServer(async(req,res)=>{
  try {
    const pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
    if(pathname.split('/').some(piece=>piece.startsWith('.'))){res.writeHead(403).end('Private path');return;}
    let target=path.resolve(root,'.'+pathname);
    if(!target.startsWith(root+path.sep)&&target!==root){res.writeHead(403).end('Outside site');return;}
    if((await stat(target)).isDirectory())target=path.join(target,'index.html');
    const actual=await realpath(target);
    if(!actual.startsWith(root+path.sep)){res.writeHead(403).end('Outside site');return;}
    res.writeHead(200,{'Content-Type':types[path.extname(target)]||'application/octet-stream','Cache-Control':'no-store'});
    createReadStream(target).on('error',()=>res.destroy()).pipe(res);
  } catch {res.writeHead(404,{'Content-Type':'text/plain'}).end('Page not found');}
}).listen(port,'127.0.0.1',()=>console.log(`P4A local preview: http://127.0.0.1:${port}/pages/states.html`));
