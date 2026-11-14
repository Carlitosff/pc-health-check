// ¿Y si la Tierra tuviera dos soles? (2204). Serie ¿QUÉ PASARÍA SI…? Parte 11. Kepler-16b (NASA Kepler, Science 15/09/2011).
// Reutilizable: PLAZA DE BLOQUES con DOS SOLES de verdad (dos luces direccionales con sombra: dos sombras por personaje; twoSuns.set(...) cambia
// altura, rumbo, color e intensidad de cada sol), mundo HELADO con doble atardecer, SISTEMA BINARIO (dos estrellas que giran alrededor del
// baricentro con masas reales y planeta circumbinario), órbitas con anillo de distancia (1 y √2) y contador de días.
import {THREE,J,mk,ss,V3,clamp,stage,box,glow,pixTex,capataz,segAt,mouthAt,label3d,puffs,snow,stars} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x8cc4f0,fog:[0x8cc4f0,60,260],exposure:1.1});cam.far=3000;cam.updateProjectionMatrix();const R=mk(2204);
const hemi=new THREE.HemisphereLight(0xcfe4ff,0x6a5a48,.75);scene.add(hemi);
// ---------- dos soles: luz + disco + halo
function mkSun(col){const L=new THREE.DirectionalLight(col,2);L.castShadow=true;L.shadow.mapSize.set(2048,2048);const c=L.shadow.camera;c.left=-22;c.right=22;c.top=22;c.bottom=-22;c.near=1;c.far=160;L.shadow.bias=-.0008;L.shadow.normalBias=.04;scene.add(L,L.target);
 const disc=new THREE.Mesh(new THREE.SphereGeometry(14,32,20),new THREE.MeshBasicMaterial({color:col,toneMapped:false,fog:false}));scene.add(disc);const h1=glow(col,90,.8),h2=glow(col,200,.35);[h1,h2].forEach(h=>{h.material.fog=false;scene.add(h)});
 return{L,disc,h1,h2,set(az,el,{col=null,power=2,size=1,vis=1}={}){const d=V3(Math.sin(az)*Math.cos(el),Math.sin(el),-Math.cos(az)*Math.cos(el));L.position.copy(d).multiplyScalar(60);L.target.position.set(0,0,0);L.intensity=power*vis;
  if(col!==null){L.color.setHex(col);disc.material.color.setHex(col);h1.material.color.setHex(col);h2.material.color.setHex(col)}
  disc.position.copy(d).multiplyScalar(420);h1.position.copy(disc.position);h2.position.copy(disc.position);disc.scale.setScalar(size);h1.scale.setScalar(90*size);h2.scale.setScalar(200*size);
  disc.visible=h1.visible=h2.visible=vis>.02;h1.material.opacity=.8*vis;h2.material.opacity=.35*vis;L.castShadow=vis>.15}}}
const SA=mkSun(0xfff1c8),SB=mkSun(0xfff1c8);
// ---------- plaza de bloques
const PL=new THREE.Group();scene.add(PL);
const tile=pixTex(64,64,(g)=>{for(let y=0;y<8;y++)for(let x=0;x<8;x++){g.fillStyle=(x+y)%2?'#d9cdb2':'#c7b996';g.fillRect(x*8,y*8,8,8)}},[60,60]);
const grMat=new THREE.MeshStandardMaterial({map:tile,roughness:.9});const gr=new THREE.Mesh(new THREE.PlaneGeometry(500,500),grMat);gr.rotation.x=-Math.PI/2;gr.receiveShadow=true;PL.add(gr);
const HC=[0xe8705a,0xf2c14e,0x6ab0de,0xf4efe6,0x8ad08a,0xd88ab8];
for(let i=0;i<16;i++){const side=i%2?1:-1,z=-8-Math.floor(i/2)*9-R()*3,w=5+R()*3,h=5+R()*9,x=side*(9+R()*6);const hb=box(w,h,6,HC[i%6],.12);hb.position.set(x,h/2,z);PL.add(hb);const rf=box(w+.6,.7,6.6,0x8a3a2e,.1);rf.position.set(x,h+.35,z);PL.add(rf);
 for(let k=0;k<Math.floor(h/2.6);k++){const wn=box(1,1.2,.1,0x2a3a5a,.03,{emissive:0x101828,emissiveIntensity:.3});wn.position.set(x+(side<0?1.4:-1.4),1.8+k*2.6,z+3.05);PL.add(wn)}}
const tree=(x,z)=>{const g=new THREE.Group();const tr=box(.6,2.4,.6,0x6a4a2e,.05);tr.position.y=1.2;g.add(tr);const lf=box(2.6,2.4,2.6,0x3f9a4a,.3);lf.position.y=3.4;g.add(lf);const lf2=box(1.6,1.4,1.6,0x4fb05a,.3);lf2.position.y=5;g.add(lf2);g.position.set(x,0,z);PL.add(g);return g};
[[-5,-4],[5.5,-6],[-6,6],[6,4]].forEach(([x,z])=>tree(x,z));
const hero=capataz();scene.add(hero.g);
// medidor de luz integrado (s3)
const meter=label3d(['LUZ DEL SOL','*100 %'],{w:6.4,h:2.8,px:130,sprite:true});scene.add(meter);
const venus=label3d(['VENUS RECIBE','*191 %'],{w:5.2,h:2.2,px:110,sprite:true,accent:'#ff8a3a'});scene.add(venus);
const sweat=puffs(scene,30,.22,0x9ad8ff,{opacity:.85});const heat=puffs(scene,60,.35,0xffd9a0,{opacity:.25});
// ---------- mundo helado (s2): mismo suelo, otro material y bloques de hielo
const ICE=new THREE.Group();scene.add(ICE);
const iceT=pixTex(64,64,(g)=>{for(let y=0;y<8;y++)for(let x=0;x<8;x++){const v=220+((x*7+y*13)%5)*7;g.fillStyle=`rgb(${v-30},${v-8},${v+20>255?255:v+20})`;g.fillRect(x*8,y*8,8,8)}},[60,60]);
const igr=new THREE.Mesh(new THREE.PlaneGeometry(500,500),new THREE.MeshStandardMaterial({map:iceT,roughness:.35,metalness:.1}));igr.rotation.x=-Math.PI/2;igr.position.y=.01;igr.receiveShadow=true;ICE.add(igr);
for(let i=0;i<26;i++){const s=1.5+R()*5;const b=box(s*(1+R()),s,s*(1+R()),0xbfe6ff,.15,{roughness:.2,metalness:.05,transparent:true,opacity:.92});const a=R()*6.28,d=10+R()*45;let bx=Math.cos(a)*d;if(Math.abs(bx)<9)bx+=bx<0?-9:9;b.position.set(bx,s/2-.3,-Math.abs(Math.sin(a))*d-6);b.rotation.y=R()*3;ICE.add(b)}
const SN=snow(scene,700,[-20,20,22,-30,16],{size:.18,speed:1.2});
const breath=puffs(scene,14,.28,0xffffff,{opacity:.6});
// ---------- espacio: sistema binario de Kepler-16 (s1) y órbitas de la Tierra (s4)
const SP=new THREE.Group();SP.position.set(5000,0,0);scene.add(SP);stars(SP,2000,{r0:500,r1:700,size:1.6});
const star=(rad,col,gs)=>{const g=new THREE.Group();g.add(new THREE.Mesh(new THREE.SphereGeometry(rad,32,20),new THREE.MeshBasicMaterial({color:col,toneMapped:false})));const h=glow(col,gs,.75);g.add(h);SP.add(g);return g};
const KA=star(2.4,0xffa040,16),KB=star(1.2,0xff4a2a,9);
const pc=document.createElement('canvas');pc.width=256;pc.height=128;{const g=pc.getContext('2d');for(let y=0;y<128;y++){const k=.5+.5*Math.sin(y*.18+Math.sin(y*.05)*3);g.fillStyle=`rgb(${200+30*k|0},${170+30*k|0},${120+30*k|0})`;g.fillRect(0,y,256,1)}}
const ptex=new THREE.CanvasTexture(pc);ptex.colorSpace=THREE.SRGBColorSpace;
const PLN=new THREE.Mesh(new THREE.SphereGeometry(1.6,32,20),new THREE.MeshStandardMaterial({map:ptex,roughness:.8}));SP.add(PLN);
const kL=new THREE.PointLight(0xffc080,40,0,0);SP.add(kL);
const ring=(rad,col,op=.7)=>{const m=new THREE.Mesh(new THREE.RingGeometry(rad-.12,rad+.12,160),new THREE.MeshBasicMaterial({color:col,transparent:true,opacity:op,side:THREE.DoubleSide,toneMapped:false}));m.rotation.x=-Math.PI/2;SP.add(m);return m};
const orbK=ring(15,0xffffff,.35);
const kLab=label3d(['*KEPLER-16b'],{w:11,h:2.5,px:130,sprite:true,bg:''});SP.add(kLab);
const sLab=label3d(['*2 ESTRELLAS','QUE GIRAN JUNTAS'],{w:13,h:4.2,px:110,sprite:true,bg:''});SP.add(sLab);
// s4: dos soles iguales, órbita de hoy (roja) y órbita √2 (verde)
const SS1=star(1.6,0xffd060,13),SS2=star(1.6,0xffd060,13);
const o1=ring(10,0xff4a3a,.8),o2=ring(10*Math.SQRT2,0x4ade80,.8);
const EA=new THREE.Mesh(new THREE.SphereGeometry(1.05,28,18),new THREE.MeshStandardMaterial({color:0x3a8ad8,roughness:.6,emissive:0x0a2a5a,emissiveIntensity:.5}));SP.add(EA);
const eg=glow(0x6ab8ff,4.5,.5);EA.add(eg);
const hot=label3d(['*¡DEMASIADO','CALOR!'],{w:9,h:3.3,px:110,sprite:true,bg:'',accent:'#ff4a3a'});SP.add(hot);
const days=label3d(['1 AÑO','*365 DÍAS'],{w:11,h:4.4,px:120,sprite:true});SP.add(days);
const p12=label3d(['*PARTE 12','LA TIERRA ×2'],{w:11,h:4.4,px:120,sprite:true});scene.add(p12);
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],k=ss(0,d,lt),m=mouthAt(t);
 const inSP=s==='s1'||s==='s4';PL.visible=s==='h'||s==='s3'||s==='cta';ICE.visible=s==='s2';SN.pts.visible=s==='s2';SP.visible=inSP;
 meter.visible=venus.visible=false;p12.visible=false;
 for(let i=0;i<30;i++)sweat.set(i,0,-999,0,.01);for(let i=0;i<60;i++)heat.set(i,0,-999,0,.01);for(let i=0;i<14;i++)breath.set(i,0,-999,0,.01);
 let fov=50,p,q,bg=0x8cc4f0;hero.g.position.set(0,0,0);hero.g.rotation.set(0,0,0);hemi.intensity=.75;
 if(s==='h'){SA.set(-.12,.16,{col:0xfff1c8,power:1.7});SB.set(.12,.15,{col:0xfff1c8,power:1.7});hero.pose(t,0,{look:Math.sin(t*1.2)*.6});hero.g.rotation.y=Math.PI*(1-ss(d*.25,d*.6,lt))+0;
  p=V3(Math.sin(t*.4)*.8,3.2,14.5-k*2);q=V3(0,6.5,-20)}
 else if(s==='s3'){// otro Sol igual aparece: la luz se duplica
  const a=ss(d*.08,d*.45,lt);SA.set(-.12,.3,{col:0xfff1c8,power:1.9});SB.set(.13,-.1+.4*a,{col:0xfff1c8,power:1.9,vis:a});
  const lux=Math.round(100+100*a);meter.visible=true;meter.set(['LUZ DEL SOL',`*${lux} %`]);meter.scale.set(5,2.2,1);meter.position.set(-2.5,6.4,-2);venus.visible=lt>d*.55;venus.scale.set(4.2,1.8,1);venus.position.set(2.7,6.2,-2);venus.material.opacity=ss(d*.55,d*.68,lt);
  grMat.color.setRGB(1,1-.18*a,1-.35*a);hemi.intensity=.75+.5*a;bg=a>.5?0xb8d4f0:0x8cc4f0;
  hero.pose(t,0,{wave:a,look:-.2});hero.g.rotation.y=0;
  for(let i=0;i<30;i++){const ph=(t*.7+i/30)%1;sweat.set(i,(i%2?.85:-.85),3.4-ph*2.4,.4,a>.4&&ph<.85&&i<8?.8:0)}
  for(let i=0;i<60;i++){const ph=(t*.25+i/60)%1;heat.set(i,-10+((i*37)%20),ph*6,-4-((i*13)%10),a*Math.sin(Math.PI*ph))}
  p=V3(0,4.6,15-k*2);q=V3(0,5.8,-10)}
 else if(s==='s2'){// Kepler-16b: dos atardeceres en un mundo helado
  SA.set(-.05,.1+.04*(1-k),{col:0xffa050,power:1.5,size:.9});SB.set(.14,.08+.03*(1-k),{col:0xff4a30,power:.9,size:.6});hemi.intensity=.45;bg=0x4a3a6e;
  hero.pose(t,0,{look:.3});hero.armL.rotation.set(-1.3,0,.9);hero.armR.rotation.set(-1.3,0,-.9);hero.g.position.x=-2.0+Math.sin(t*40)*.04;hero.g.rotation.y=Math.PI;
  SN.draw(t);for(let i=0;i<14;i++){const ph=((t*.8+i/14)%1);breath.set(i,-2+Math.sin(i*2)*.3*ph,3.1+ph*.8,-1.2-ph*1.6,ph<.9?1.2*(1-ph)+.3:0)}
  p=V3(.8+k*.6,3.4,15-k*1.5);q=V3(.6,6.8,-20)}
 else if(s==='s1'){bg=0x02030a;hemi.intensity=.15;SA.set(0,0,{vis:0});SB.set(0,0,{vis:0});
  const a=t*1.9,ap=t*.45;const sep=6,ma=.69,mb=.2;KA.position.set(Math.cos(a)*sep*mb/(ma+mb),0,Math.sin(a)*sep*mb/(ma+mb));KB.position.set(-Math.cos(a)*sep*ma/(ma+mb),0,-Math.sin(a)*sep*ma/(ma+mb));
  PLN.position.set(Math.cos(ap)*15,0,Math.sin(ap)*15);PLN.rotation.y=t;kL.position.set(0,0,0);kLab.position.copy(PLN.position).add(V3(0,3,0));sLab.position.set(0,0,19.5);sLab.material.opacity=ss(1.2,2,lt);
  [KA,KB,PLN,orbK,kLab,sLab].forEach(o=>o.visible=true);[SS1,SS2,o1,o2,EA,hot,days].forEach(o=>o.visible=false);
  p=V3(Math.sin(t*.2)*4,40-k*4,42-k*4).add(SP.position);q=V3(0,-6,0).add(SP.position)}
 else if(s==='s4'){bg=0x02030a;hemi.intensity=.15;SA.set(0,0,{vis:0});SB.set(0,0,{vis:0});
  [KA,KB,PLN,orbK,kLab,sLab].forEach(o=>o.visible=false);[SS1,SS2,o1,o2,EA,days].forEach(o=>o.visible=true);
  const a=t*2.2;SS1.position.set(Math.cos(a)*1.9,0,Math.sin(a)*1.9);SS2.position.set(-Math.cos(a)*1.9,0,-Math.sin(a)*1.9);kL.position.set(0,0,0);
  const mv=ss(d*.12,d*.5,lt);const rr=10+mv*(10*Math.SQRT2-10);const ae=t*.6;EA.position.set(Math.cos(ae)*rr,0,Math.sin(ae)*rr);
  hot.visible=lt<d*.4;hot.position.copy(EA.position).add(V3(0,2.6,0));hot.material.opacity=ss(0,.4,lt)*(1-ss(d*.3,d*.4,lt));
  const dd=Math.round(365+(434-365)*ss(d*.5,d*.85,lt));days.set(['1 AÑO',`*${dd} DÍAS`]);days.position.set(0,0,19.5);
  o1.material.opacity=.8-.5*mv;
  p=V3(Math.sin(t*.2)*3,34-k*3,36-k*3).add(SP.position);q=V3(0,-4.5,0).add(SP.position)}
 else{// cta: doble atardecer sobre la plaza
  SA.set(-.12,.06,{col:0xffb060,power:1.5});SB.set(.13,.035,{col:0xff8a50,power:1.3});bg=0xf0a070;hemi.intensity=.55;hero.g.position.set(0,0,-3);hero.pose(t,0,{wave:1});hero.g.rotation.y=0;
  p12.visible=true;p12.position.set(0,12.5,-30);p=V3(0,5.5,15+k);q=V3(0,10,-30)}
 if(!inSP){[KA,KB,PLN,orbK,kLab,sLab,SS1,SS2,o1,o2,EA,hot,days].forEach(o=>o.visible=false)}
 sweat.done();heat.done();breath.done();
 if(s!=='s3')grMat.color.setRGB(1,1,1);
 scene.background.setHex(bg);scene.fog.color.setHex(bg);scene.fog.near=inSP?2000:60;scene.fog.far=inSP?3000:260;
 if(cam.fov!==fov){cam.fov=fov;cam.updateProjectionMatrix()}cam.position.copy(p);cam.lookAt(q);r.render(scene,cam)};
window.ready=true;
