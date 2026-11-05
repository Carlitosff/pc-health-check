// Render determinista: abre <page>.html?job=... y guarda JPEG por frame. Uso: node render.mjs job.json [t1 t2 ...]
import {createRequire} from 'module';import http from 'http';import fs from 'fs';import path from 'path';
const require=createRequire(process.env.NODE_PATH+'/x.js');const pw=require('playwright');
const root=path.dirname(new URL(import.meta.url).pathname);const job=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
const stills=process.argv.slice(3).map(Number);
const MIME={'.html':'text/html','.js':'text/javascript','.json':'application/json'};
const srv=http.createServer((q,s)=>{const u=q.url.split('?')[0];if(u==='/job.json'){s.writeHead(200,{'content-type':'application/json'});s.end(JSON.stringify(job));return}
 const f=path.join(root,u==='/'?'index.html':u);fs.readFile(f,(e,d)=>{if(e){s.writeHead(404);s.end();return}s.writeHead(200,{'content-type':MIME[path.extname(f)]||'application/octet-stream'});s.end(d)})}).listen(0);
await new Promise(r=>srv.once('listening',r));
const b=await pw.chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
p.on('pageerror',e=>{console.error('ERR',e.message);process.exitCode=1});p.on('console',m=>{if(m.type()==='error')console.error(m.text())});
await p.goto(`http://localhost:${srv.address().port}/`);await p.waitForFunction('window.ready===true',{timeout:90000});
fs.mkdirSync(job.frames,{recursive:true});const t0=Date.now();
// v16 (05/11): desenfoque de movimiento REAL en los cambios de plano: en los 0,4 s tras cada corte se promedian 4 subframes (coste +~20 %). job.blur=false lo quita.
const CUTS=job.blur===false?[]:Object.entries(job.tl||{}).filter(([k])=>k!=='h').map(([,v])=>v[0]);
const inCut=t=>CUTS.some(a=>t>=a&&t<a+.4);
await p.evaluate(()=>{const c=document.createElement('canvas');c.width=1080;c.height=1920;c.id='mb';c.style.cssText='position:fixed;left:0;top:0;width:1080px;height:1920px;display:none;z-index:9';document.body.appendChild(c)});
const shot=async(t,name)=>{if(inCut(t)){await p.evaluate(x=>{const c=document.getElementById('mb'),g=c.getContext('2d'),src=document.querySelector('canvas');for(let k=0;k<4;k++){window.renderAt(x+k/120);g.globalAlpha=1/(k+1);g.drawImage(src,0,0,1080,1920)}g.globalAlpha=1;c.style.display='block'},t)}else{await p.evaluate(x=>{document.getElementById('mb').style.display='none';window.renderAt(x)},t)}await p.screenshot({path:path.join(job.frames,name),type:'jpeg',quality:95})};
if(stills.length){for(const t of stills)await shot(t,`still_${t}.jpg`)}
else{const n=Math.ceil(job.total*30)+1;for(let i=0;i<n;i++){const f=path.join(job.frames,`f${String(i).padStart(5,'0')}.jpg`);const fz=(process.env.FORCE||'').split('-').map(Number);if(fs.existsSync(f)&&!(fz.length===2&&i>=fz[0]&&i<=fz[1]))continue;await shot(i/30,path.basename(f));if(i%60===0)console.log(i,n,Math.round((Date.now()-t0)/1000)+'s')}}
await b.close();srv.close();console.log('ok',Math.round((Date.now()-t0)/1000)+'s');
