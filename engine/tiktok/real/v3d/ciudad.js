// LA CIUDAD DE LA COMUNIDAD en 3D (Three.js). 1 seguidor = 1 ventana. Datos en job.json (ver ciudad3d.py).
import * as THREE from 'three';
import {RoundedBoxGeometry} from '/node_modules/three/examples/jsm/geometries/RoundedBoxGeometry.js';
const J=await (await fetch('/job.json')).json();
const W=1080,H=1920,TL=J.tl;
const r=new THREE.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});r.setSize(W,H,false);r.setPixelRatio(1);
r.toneMapping=THREE.ACESFilmicToneMapping;r.toneMappingExposure=1.25;document.body.prepend(r.domElement);
const scene=new THREE.Scene();scene.background=new THREE.Color(0x060a22);scene.fog=new THREE.Fog(0x0b1030,34,120);
const cam=new THREE.PerspectiveCamera(35,W/H,.1,300);
const mk=s=>()=>{s=(s+0x6D2B79F5)|0;let t=Math.imul(s^s>>>15,1|s);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296};
const R=mk(2018);
const ss=(a,b,x)=>{x=Math.min(1,Math.max(0,(x-a)/(b-a)));return x*x*(3-2*x)};
const V3=(...a)=>new THREE.Vector3(...a);
// --- texturas
function concrete(base,dark){const c=document.createElement('canvas');c.width=c.height=256;const g=c.getContext('2d');g.fillStyle=base;g.fillRect(0,0,256,256);const q=mk(9);g.fillStyle=dark;for(let i=0;i<220;i++){g.globalAlpha=.05+q()*.18;g.fillRect(q()*256,q()*256,4+q()*26,2+q()*5)}const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;t.wrapS=t.wrapT=THREE.RepeatWrapping;t.magFilter=THREE.NearestFilter;return t}
const glowTex=(()=>{const c=document.createElement('canvas');c.width=c.height=128;const g=c.getContext('2d');const d=g.createRadialGradient(64,64,0,64,64,64);d.addColorStop(0,'rgba(255,255,255,1)');d.addColorStop(.25,'rgba(255,255,255,.45)');d.addColorStop(1,'rgba(255,255,255,0)');g.fillStyle=d;g.fillRect(0,0,128,128);return new THREE.CanvasTexture(c)})();
// --- luces
scene.add(new THREE.HemisphereLight(0x5f78e0,0x0a0a18,1.15));
const moon=new THREE.DirectionalLight(0xbfd0ff,1.8);moon.position.set(-12,24,18);scene.add(moon);
const warm=new THREE.PointLight(0xffb060,38,40,1.6);warm.position.set(-3,5,9);scene.add(warm);
const rim=new THREE.DirectionalLight(0xff4fb0,1.0);rim.position.set(14,6,-10);scene.add(rim);
// --- cielo
{const n=500,p=new Float32Array(n*3);for(let i=0;i<n;i++){p[i*3]=(R()-.5)*240;p[i*3+1]=8+R()*110;p[i*3+2]=-70-R()*20}const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.BufferAttribute(p,3));scene.add(new THREE.Points(g,new THREE.PointsMaterial({color:0xcfd8ff,size:.32,fog:false,transparent:true,opacity:.85})))
 const m=new THREE.Mesh(new THREE.CircleGeometry(4.2,48),new THREE.MeshBasicMaterial({color:0xfff2d8,fog:false}));m.position.set(-13,54,-68);scene.add(m);
 const h=new THREE.Sprite(new THREE.SpriteMaterial({map:glowTex,color:0xffe9c0,opacity:.4,transparent:true,blending:THREE.AdditiveBlending,fog:false,depthWrite:false}));h.scale.set(34,34,1);h.position.copy(m.position);scene.add(h)}
// --- skyline lejano
{const c=document.createElement('canvas');c.width=64;c.height=128;const g=c.getContext('2d');g.fillStyle='#0c1236';g.fillRect(0,0,64,128);const q=mk(3);for(let y=4;y<124;y+=8)for(let x=4;x<60;x+=8)if(q()<.3){g.fillStyle=q()<.8?'#caa35e':'#6a7fd0';g.globalAlpha=.75;g.fillRect(x,y,4,5);g.globalAlpha=1}
 const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;t.magFilter=THREE.NearestFilter;const mat=new THREE.MeshBasicMaterial({map:t});
 for(let i=0;i<80;i++){const w=3+R()*5,h=8+R()*30,z=-30-R()*26,x=(R()-.5)*110;if(Math.abs(x)<5&&z>-38)continue;const gm=new THREE.BoxGeometry(w,h,w),uv=gm.attributes.uv;for(let k=0;k<uv.count;k++)uv.setXY(k,uv.getX(k)*Math.max(1,Math.round(w/4)),uv.getY(k)*Math.max(1,Math.round(h/8)));t.wrapS=t.wrapT=THREE.RepeatWrapping;const b=new THREE.Mesh(gm,mat);b.position.set(x,h/2-.5,z);scene.add(b)}}
// --- suelo y calle
const gnd=new THREE.Mesh(new THREE.PlaneGeometry(260,200),new THREE.MeshStandardMaterial({color:0x10142a,roughness:.55,metalness:.3}));gnd.rotation.x=-Math.PI/2;gnd.position.set(0,-.02,-40);scene.add(gnd);
const road=new THREE.Mesh(new THREE.PlaneGeometry(200,6.5),new THREE.MeshStandardMaterial({color:0x080a14,roughness:.3,metalness:.5}));road.rotation.x=-Math.PI/2;road.position.set(0,0,7.5);scene.add(road);
for(let i=-30;i<30;i++){const d=new THREE.Mesh(new THREE.BoxGeometry(1.6,.02,.14),new THREE.MeshBasicMaterial({color:0xc9b77a}));d.position.set(i*3.4,.02,7.5);scene.add(d)}
for(let i=-6;i<=6;i++){const x=i*5+1.2;const p=new THREE.Mesh(new THREE.BoxGeometry(.14,3.4,.14),new THREE.MeshStandardMaterial({color:0x2a2f46}));p.position.set(x,1.7,3.9);scene.add(p);const b=new THREE.Mesh(new THREE.BoxGeometry(.5,.16,.3),new THREE.MeshBasicMaterial({color:0xffdca0}));b.position.set(x,3.45,3.9);scene.add(b);const s=new THREE.Sprite(new THREE.SpriteMaterial({map:glowTex,color:0xffc070,opacity:.55,transparent:true,blending:THREE.AdditiveBlending,depthWrite:false}));s.scale.set(4,4,1);s.position.copy(b.position);scene.add(s)}
const cars=[];const carCols=[0xd8344a,0x2d6be0,0xe8e8f0,0xf0a020,0x18b89a];for(let i=0;i<9;i++){const g=new THREE.Group(),d=i%2?1:-1,col=carCols[i%5];const m=new THREE.MeshStandardMaterial({color:col,roughness:.35,metalness:.4});const a=new THREE.Mesh(new THREE.BoxGeometry(1.9,.42,.9),m);a.position.y=.34;const b=new THREE.Mesh(new THREE.BoxGeometry(1,.36,.82),new THREE.MeshStandardMaterial({color:0x11142a,roughness:.2}));b.position.y=.72;g.add(a,b);const hl=new THREE.Sprite(new THREE.SpriteMaterial({map:glowTex,color:0xfff0c0,transparent:true,opacity:.9,blending:THREE.AdditiveBlending,depthWrite:false}));hl.scale.set(1.6,1.6,1);hl.position.set(1.0*d,.36,.3);g.add(hl);const tl=new THREE.Sprite(new THREE.SpriteMaterial({map:glowTex,color:0xff2030,transparent:true,opacity:.9,blending:THREE.AdditiveBlending,depthWrite:false}));tl.scale.set(1,1,1);tl.position.set(-1.0*d,.36,.3);g.add(tl);g.userData={d,o:i*17,v:7+i*.9,z:d>0?6.0:9.0};scene.add(g);cars.push(g)}
// --- edificios: la capacidad total es exactamente la META (cada ventana existe ya, a oscuras)
const FH=.98,CW=.92;
const SPECS=[[4,13,-4.5,-7,0x2a3358],[3,16,.1,-11,0x303a66],[4,11,4.7,-6,0x262c50],[4,9,-3.0,-.8,0x38324f],[4,J.goal>212?8:99,2.7,-.2,0x3b3f5c],
 [2,19,-3.4,-13,0x34406e],[4,20,9.2,-14,0x2c2a55],[5,15,-14,-16,0x262c52],[5,22,14,-18,0x2c345c],[6,24,0,-22,0x262a50]];
const blds=[],WIN=[];let cap=0;const crown=[0,1,2];
for(let i=0;i<SPECS.length*4&&cap<J.goal;i++){const sp=SPECS[i%SPECS.length];const ring=Math.floor(i/SPECS.length);let [cols,floors,x,z,hue]=sp;x*=1+ring*.9;z-=ring*16;floors+=ring*4;
 const left=J.goal-cap,fin=(cols*floors>=left);if(fin)floors=Math.ceil(left/cols);const b={i,cols,floors,x,z,hue,fin,w:cols*CW+.7,h:floors*FH+.8};blds.push(b);
 for(let f=0;f<floors;f++)for(let c=0;c<cols;c++){if(WIN.length>=J.goal)break;WIN.push({b,f,c,x:x+(c-(cols-1)/2)*CW,y:.75+f*FH+.32,z:z+b.w/2+.02,k:i*7+f*3+c});cap++}}
const LAST=WIN[Math.min(J.n,WIN.length-1)].b;
for(const b of blds){const m=new THREE.MeshStandardMaterial({map:concrete('#'+b.hue.toString(16).padStart(6,'0'),'#0a0c1c'),roughness:.82});m.map.repeat.set(b.w/3,b.h/3);
 const body=new THREE.Mesh(new THREE.BoxGeometry(b.w,b.h,b.w),m);body.position.set(b.x,b.h/2,b.z);scene.add(body);
 const trim=new THREE.MeshStandardMaterial({color:0x4a5478,roughness:.6});
 for(let f=0;f<=b.floors;f+=3){const l=new THREE.Mesh(new THREE.BoxGeometry(b.w+.14,.09,b.w+.14),trim);l.position.set(b.x,.42+f*FH,b.z);scene.add(l)}
 const pil=new THREE.Mesh(new THREE.BoxGeometry(b.w+.26,.4,b.w+.26),new THREE.MeshStandardMaterial({color:0x1a1f38,roughness:.8}));pil.position.set(b.x,.2,b.z);scene.add(pil);
 if(b!==LAST&&!(J.n>=250&&b.i===5)){const par=new THREE.Mesh(new THREE.BoxGeometry(b.w+.2,.22,b.w+.2),trim);par.position.set(b.x,b.h+.1,b.z);scene.add(par);
  const v=b.i%3;if(v===0){const a=new THREE.Mesh(new THREE.BoxGeometry(.1,3.4,.1),new THREE.MeshStandardMaterial({color:0x8088a8}));a.position.set(b.x,b.h+1.8,b.z);scene.add(a);const s=new THREE.Sprite(new THREE.SpriteMaterial({map:glowTex,color:0xff2028,transparent:true,blending:THREE.AdditiveBlending,depthWrite:false}));s.scale.set(1.7,1.7,1);s.position.set(b.x,b.h+3.55,b.z);scene.add(s);b.beacon=s}
  else if(v===1){const t=new THREE.Mesh(new THREE.CylinderGeometry(.7,.7,1.2,10),new THREE.MeshStandardMaterial({color:0x5a4238,roughness:.9}));t.position.set(b.x-.3,b.h+1.1,b.z);scene.add(t);const u=new THREE.Mesh(new THREE.ConeGeometry(.82,.5,10),new THREE.MeshStandardMaterial({color:0x3a2a28}));u.position.set(b.x-.3,b.h+1.95,b.z);scene.add(u)}
  else{const n=new THREE.Mesh(new THREE.BoxGeometry(b.w*.62,.8,b.w*.62),m);n.position.set(b.x,b.h+.6,b.z);scene.add(n)}
  const ac=new THREE.Mesh(new THREE.BoxGeometry(.6,.4,.5),new THREE.MeshStandardMaterial({color:0x6a7088}));ac.position.set(b.x+b.w*.28,b.h+.4,b.z+.3);scene.add(ac);
  if(b.i%2===0){const neon=new THREE.Mesh(new THREE.BoxGeometry(.08,b.h*.55,.08),new THREE.MeshBasicMaterial({color:b.i%4?0x20e8d8:0xff3fb0}));neon.position.set(b.x-b.w/2-.05,b.h*.55,b.z+b.w/2+.02);scene.add(neon);const s=new THREE.Sprite(new THREE.SpriteMaterial({map:glowTex,color:b.i%4?0x20e8d8:0xff3fb0,opacity:.3,transparent:true,blending:THREE.AdditiveBlending,depthWrite:false}));s.scale.set(3.4,b.h*.8,1);s.position.copy(neon.position);scene.add(s)}}
}
// --- v16 (05/11): el primer rascacielos: la torre que termina en la ventana 250 lleva corona escalonada, aristas LED y antena con baliza dorada
let skyB=null,skyG=[];if(J.n>=250){skyB=blds.find(b=>b.i===5);if(skyB){const b=skyB,gold=new THREE.MeshStandardMaterial({color:0xffc23a,emissive:0xb07810,emissiveIntensity:.9,roughness:.35});[[1.0,.8],[.72,.8],[.44,1.0]].reduce((y,[k,h])=>{const q=new THREE.Mesh(new THREE.BoxGeometry(b.w*k,h,b.w*k),gold);q.position.set(b.x,y+h/2,b.z);scene.add(q);return y+h},b.h+.2);const top=b.h+2.8;const an=new THREE.Mesh(new THREE.BoxGeometry(.14,4.2,.14),new THREE.MeshStandardMaterial({color:0xe8ecf8,emissive:0x8088a8}));an.position.set(b.x,top+2.1,b.z);scene.add(an);const be=new THREE.Sprite(new THREE.SpriteMaterial({map:glowTex,color:0xffd040,transparent:true,blending:THREE.AdditiveBlending,depthWrite:false}));be.scale.set(3,3,1);be.position.set(b.x,top+4.3,b.z);scene.add(be);skyG.push(be);[[-1,1],[1,1]].forEach(([u,v])=>{const l=new THREE.Mesh(new THREE.BoxGeometry(.09,b.h,.09),new THREE.MeshBasicMaterial({color:0xffd86a,toneMapped:false}));l.position.set(b.x+u*(b.w/2+.04),b.h/2,b.z+v*(b.w/2+.04));scene.add(l);skyG.push(l)})}}
// --- ventanas
const wg=new THREE.BoxGeometry(CW*.64,FH*.62,.07);const wm=new THREE.MeshBasicMaterial({toneMapped:false});const wins=new THREE.InstancedMesh(wg,wm,WIN.length);{const o=new THREE.Object3D();WIN.forEach((w,i)=>{o.position.set(w.x,w.y,w.z);o.updateMatrix();wins.setMatrixAt(i,o.matrix);wins.setColorAt(i,new THREE.Color(0))})}scene.add(wins);
const gp=new Float32Array(WIN.length*3),gc=new Float32Array(WIN.length*3);WIN.forEach((w,i)=>{gp[i*3]=w.x;gp[i*3+1]=w.y;gp[i*3+2]=w.z+.1});const gg=new THREE.BufferGeometry();gg.setAttribute('position',new THREE.BufferAttribute(gp,3));gg.setAttribute('color',new THREE.BufferAttribute(gc,3));
scene.add(new THREE.Points(gg,new THREE.PointsMaterial({map:glowTex,size:2.1,vertexColors:true,transparent:true,blending:THREE.AdditiveBlending,depthWrite:false,sizeAttenuation:true})));
const WARM=[0xffcf78,0xffb95a,0xffe3a4,0xffa848].map(h=>new THREE.Color(h));const SPECIAL=new Map(J.special.map(s=>[s.idx,s]));
// --- grúa sobre el edificio en obras
const yel=new THREE.MeshStandardMaterial({color:0xf0b030,roughness:.5,emissive:0x2a1a00,emissiveIntensity:.4});
const crane=new THREE.Group();{const ht=LAST.h+7;const m=new THREE.Mesh(new THREE.BoxGeometry(.5,ht,.5),yel);m.position.y=ht/2;crane.add(m);const J2=new THREE.Group();J2.position.y=ht;const a=new THREE.Mesh(new THREE.BoxGeometry(8.5,.34,.34),yel);a.position.x=-2.6;J2.add(a);const cw=new THREE.Mesh(new THREE.BoxGeometry(1.1,.8,.7),new THREE.MeshStandardMaterial({color:0x60647a}));cw.position.set(1.4,-.3,0);J2.add(cw);const cab=new THREE.Mesh(new THREE.BoxGeometry(.8,.8,.8),new THREE.MeshStandardMaterial({color:0xe8e8f0}));cab.position.set(-.1,-.6,0);J2.add(cab);const c=new THREE.Mesh(new THREE.BoxGeometry(.05,1,.05),new THREE.MeshBasicMaterial({color:0xcccccc}));J2.add(c);const beam=new THREE.Mesh(new THREE.BoxGeometry(1.6,.22,.3),new THREE.MeshStandardMaterial({color:0xb07a2a}));J2.add(beam);crane.add(J2);crane.userData={J2,c,beam};const s=new THREE.Sprite(new THREE.SpriteMaterial({map:glowTex,color:0xff3028,transparent:true,blending:THREE.AdditiveBlending,depthWrite:false}));s.scale.set(1.5,1.5,1);s.position.set(-6.8,0,0);J2.add(s);crane.userData.lamp=s}crane.position.set(LAST.x+LAST.w/2+.5,0,LAST.z-.2);scene.add(crane);
// vigas de la planta en obras
for(let c=0;c<=LAST.cols;c++){const v=new THREE.Mesh(new THREE.BoxGeometry(.13,FH*1.1,.13),yel);v.position.set(LAST.x+(c-LAST.cols/2)*CW,LAST.h+FH*.55,LAST.z+LAST.w/2-.08);scene.add(v)}{const v=new THREE.Mesh(new THREE.BoxGeometry(LAST.w,.13,.13),yel);v.position.set(LAST.x,LAST.h+FH*1.1,LAST.z+LAST.w/2-.08);scene.add(v)}
// --- personaje: la obrera/capataz de la ciudad (propio de la cuenta)
const box=(w,h,d,col,rad=.05,opt={})=>new THREE.Mesh(new RoundedBoxGeometry(w,h,d,2,rad),new THREE.MeshStandardMaterial({color:col,roughness:.7,...opt}));
const hero=new THREE.Group();const SK=0xd9a06a,OV=0x1f7a8c,HAT=0xffc42e;const headG=new THREE.Group();headG.position.y=3.05;hero.add(headG);
const headB=box(1.5,1.3,1.3,SK,.12);headG.add(headB);
const brim=box(1.9,.14,1.65,HAT,.04);brim.position.set(0,.72,.1);const dome=box(1.5,.5,1.3,HAT,.14);dome.position.y=.98;const ridge=box(.3,.16,1.1,0xf2a800,.05);ridge.position.y=1.28;headG.add(brim,dome,ridge);
const hair=box(1.54,.22,.3,0x3a2416,.04);hair.position.set(0,.5,-.55);headG.add(hair);
const eyes=[-.34,.34].map(x=>{const g=new THREE.Group();const w=box(.34,.4,.05,0xfdf8f0,.02);const p=box(.17,.25,.04,0x15101c,.02);p.position.z=.04;g.add(w,p);g.position.set(x,.14,.66);g.userData.p=p;headG.add(g);return g});
[-.34,.34].forEach(x=>{const b=box(.42,.09,.05,0x3a2416,.02);b.position.set(x,.42,.67);headG.add(b)});
const nose=box(.2,.24,.14,0xc98c58,.05);nose.position.set(0,-.08,.69);headG.add(nose);
const mouth=box(.46,.1,.05,0x4a1a14,.02);mouth.position.set(0,-.38,.66);headG.add(mouth);
const torso=box(1.5,1.5,.95,OV,.1);torso.position.y=1.65;hero.add(torso);
const shirt=box(1.0,.5,.05,0xf4efe6,.02);shirt.position.set(0,2.15,.47);hero.add(shirt);const stripe=box(1.54,.14,.99,0xffe25a,.02);stripe.position.y=1.5;hero.add(stripe);
const armL=new THREE.Group(),armR=new THREE.Group();armL.position.set(-1.0,2.3,0);armR.position.set(1.0,2.3,0);for(const a of[armL,armR]){const s=box(.44,1.3,.48,OV,.08);s.position.y=-.58;const h=box(.46,.4,.5,SK,.08);h.position.y=-1.34;a.add(s,h);hero.add(a)}
[-.42,.42].forEach(x=>{const l=box(.6,.9,.72,0x154f5c,.06);l.position.set(x,.55,0);const f=box(.66,.28,.92,0x20161c,.06);f.position.set(x,.14,.1);hero.add(l,f)});
hero.position.set(.1,0,4.6);scene.add(hero);
const lift=new THREE.Mesh(new THREE.CylinderGeometry(1.5,1.6,.14,20),new THREE.MeshStandardMaterial({color:0x20243c,roughness:.9}));lift.position.set(.1,.05,4.6);scene.add(lift);

// --- v15 (04/11): panel LED del reto con cuenta atrás real y fuegos artificiales de hito
let panel=null,pc=null,pg=null,pT=null;const PX=3.1,PZ=2.6,PY=3.5;
if(J.clock){pc=document.createElement('canvas');pc.width=640;pc.height=400;pg=pc.getContext('2d');pT=new THREE.CanvasTexture(pc);pT.colorSpace=THREE.SRGBColorSpace;panel=new THREE.Group();const sc=new THREE.Mesh(new THREE.BoxGeometry(3.6,2.25,.14),new THREE.MeshBasicMaterial({map:pT,toneMapped:false}));panel.add(sc);const fr=box(3.85,2.5,.1,0x20243c,.05);fr.position.z=-.1;panel.add(fr);[-1.2,1.2].forEach(x=>{const l=box(.18,3.4,.18,0x30354e,.03);l.position.set(x,-2.2,-.12);panel.add(l)});const gl=new THREE.Sprite(new THREE.SpriteMaterial({map:glowTex,color:0xff5040,opacity:.35,transparent:true,blending:THREE.AdditiveBlending,depthWrite:false}));gl.scale.set(8,6,1);gl.position.z=.2;panel.add(gl);panel.position.set(PX,PY,PZ);panel.rotation.y=-.18;scene.add(panel)}
function drawPanel(t){if(J.clock.secs==null){if(drawPanel.done)return;drawPanel.done=1;pg.fillStyle='#07060f';pg.fillRect(0,0,640,400);pg.textAlign='center';pg.textBaseline='middle';pg.fillStyle='#ff3b30';pg.font='900 56px sans-serif';pg.fillText('FALTAN',320,60);pg.fillStyle='#fff';pg.font='900 170px sans-serif';pg.fillText(String(J.clock.falta),320,190);pg.fillStyle='#ffc23a';pg.font='900 62px sans-serif';pg.fillText('SIN RELOJ',320,332);pT.needsUpdate=true;return}const rem=Math.max(0,J.clock.secs-t);const h=Math.floor(rem/3600),m=Math.floor(rem%3600/60),s_=Math.floor(rem%60);pg.fillStyle='#07060f';pg.fillRect(0,0,640,400);pg.fillStyle='#ff3b30';pg.textAlign='center';pg.textBaseline='middle';pg.font='900 56px sans-serif';pg.fillText('FALTAN',320,52);pg.fillStyle='#fff';pg.font='900 150px sans-serif';pg.fillText(String(J.clock.falta),320,160);pg.fillStyle='#ffc23a';pg.font='900 76px monospace';pg.fillText(`${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(s_).padStart(2,'0')}`,320,300);pg.fillStyle='#8890b8';pg.font='700 34px sans-serif';pg.fillText('HASTA LAS 02:00',320,368);pT.needsUpdate=true}
const FW=[];if(J.hito){const cols=[0xffc23a,0xff3fb0,0x20e8d8,0xff5040,0xffffff,0x7dff6a,0xffc23a,0xff3fb0,0x20e8d8];const q=mk(200);for(let b=0;b<9;b++){const n=110,p=new Float32Array(n*3),dirs=[];for(let i=0;i<n;i++){const u=q()*6.283,v=Math.acos(2*q()-1);dirs.push([Math.sin(v)*Math.cos(u),Math.sin(v)*Math.sin(u),Math.cos(v)])}const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.BufferAttribute(p,3));const m=new THREE.Points(g,new THREE.PointsMaterial({map:glowTex,color:cols[b],size:2.0,transparent:true,blending:THREE.AdditiveBlending,depthWrite:false}));m.frustumCulled=false;scene.add(m);FW.push({m,g,dirs,c:[(q()-.5)*13,5+q()*8,-2-q()*9],t0:b*.6})}}
let halo=null;function drawFW(t){if(!halo){halo=new THREE.Sprite(new THREE.SpriteMaterial({map:glowTex,color:0xffd040,transparent:true,blending:THREE.AdditiveBlending,depthWrite:false}));halo.position.set(focus.x,focus.y,focus.z+.3);scene.add(halo)}const on=ss(TL.s2[0]+1.2,TL.s2[0]+1.6,t);halo.visible=on>0;const pu=.65+.35*Math.sin(t*5);halo.scale.setScalar(5.5*pu*on);halo.material.opacity=on*pu*.8;if(!halo.userData.f){const m=new THREE.MeshBasicMaterial({color:0xffe27a,toneMapped:false});const fr=new THREE.Group();[[CW*.86,.08,0,FH*.42],[CW*.86,.08,0,-FH*.42],[.08,FH*.9,CW*.4,0],[.08,FH*.9,-CW*.4,0]].forEach(([w,h,x,y])=>{const b=new THREE.Mesh(new THREE.BoxGeometry(w,h,.1),m);b.position.set(x,y,0);fr.add(b)});fr.position.set(focus.x,focus.y,focus.z+.1);scene.add(fr);halo.userData.f=fr}halo.userData.f.visible=on>0;const a0=TL.s2[0]+.9;FW.forEach(f=>{const a=t-a0-f.t0;f.m.visible=a>0&&a<1.9;if(!f.m.visible)return;const P=f.g.attributes.position;f.dirs.forEach((d,i)=>{const r=9*(1-Math.exp(-a*2.6));P.setXYZ(i,focus.x+f.c[0]+d[0]*r,focus.y+f.c[1]+d[1]*r-1.4*a*a,focus.z+f.c[2]+d[2]*r)});P.needsUpdate=true;f.m.material.opacity=Math.max(0,1-a/1.9)})}
// --- animación
const seg=t=>Object.entries(TL).find(([k,[a,b]])=>t>=a&&t<b)?.[0]||'cta';
const fr=J.special.filter(s=>s.fresh);const focus=fr.length?WIN[fr[Math.floor(fr.length/2)].idx]:WIN[Math.floor(WIN.length/2)];
const lastIdx=J.goal-1,LW=WIN[J.vote?lastIdx:Math.min(J.n+3,WIN.length-1)],faceY=3.15;
const wideZ=Math.max(33,23+blds.length*1.7);
const shots={
 h:{p:V3(.25,3.9,13.2),q:V3(.25,3.55,4.6)},
 s1:{p:V3(-1.6,7.5,wideZ),q:V3(0,8.0,-5)},
 s2:{p:V3(focus.x+.6,focus.y+7.5,focus.z+15),q:V3(focus.x,focus.y+1.2,focus.z)},
 s3:J.goal>=500?{p:V3(0,13,wideZ+8),q:V3(0,17,-20)}:{p:V3(LW.x+1.2,LW.y+.3,LW.z+16),q:V3(LW.x-.4,LW.y+2,LW.z)},
 cta:J.clock?(J.clock.secs==null?{p:V3(.1,3,34.6),q:V3(.1,1.43,0)}:{p:V3(1.2,5.2,20),q:V3(1,2.6,0)}):{p:V3(.6,4.6,17.5),q:V3(.5,6.6,0)}};
if(J.clock){shots.h={p:V3(1.4,4.4,25),q:V3(1.4,5.4,3)};if(J.hito)shots.s2={p:V3(focus.x+.6,focus.y-2,focus.z+19),q:V3(focus.x,focus.y+2.6,focus.z)};shots.s3={p:V3(PX-.4,PY+.35,PZ+9),q:V3(PX-.1,PY+1.5,PZ)}}
if(J.noria){const[nx,nz]=J.noria.at||[-7.5,5.5];shots.h={p:V3(-3.4,4.4,34),q:V3(-3.4,6.4,2)};shots.s2={p:V3(nx+.8,3.6,nz+22),q:V3(nx,6.3,nz)};shots.s3={p:V3(nx-1,3.8,nz+21),q:V3(nx+.1,6.2,nz)}}
function camAt(t){const ord=['h','s1','s2','s3','cta'];let p=shots.h.p.clone(),q=shots.h.q.clone();for(const k of ord.slice(1)){const a=TL[k][0],e=ss(a,a+.85,t);p.lerp(shots[k].p,e);q.lerp(shots[k].q,e)}p.x+=Math.sin(t*.55)*.35;p.y+=Math.sin(t*.8)*.12;const s=seg(t);if(s==='s1'||s==='s2')p.z-=(t-TL[s][0])*.32;return{p,q}}
// --- v17 (06/11): LA NORIA DE LA CIUDAD: de la ventana 250 a la 300, cada seguidor pone 1 pieza de 50. En 300 se enciende y gira.
let NOR=null;if(J.noria){const[nx,nz]=J.noria.at||[-7.5,5.5],RAD=3.4,HUB=4.5,g=new THREE.Group();g.position.set(nx,0,nz);scene.add(g);const wheel=new THREE.Group();wheel.position.y=HUB;g.add(wheel);
 const steel=new THREE.MeshStandardMaterial({color:0x8a94b8,roughness:.45,metalness:.3});[-1,1].forEach(sx=>[-1,1].forEach(sz=>{const L=Math.hypot(HUB,1.9),leg=new THREE.Mesh(new THREE.BoxGeometry(.2,L,.2),steel);leg.position.set(sx*.95,HUB/2,sz*.55);leg.rotation.z=sx*Math.atan2(1.9,HUB);g.add(leg)}));const axle=new THREE.Mesh(new THREE.BoxGeometry(.4,.4,1.5),steel);axle.position.y=HUB;g.add(axle);const base=new THREE.Mesh(new THREE.BoxGeometry(5,.3,2.2),new THREE.MeshStandardMaterial({color:0x2a3050,roughness:.8}));base.position.y=.15;g.add(base);
 const NP=50,ghost=new THREE.MeshBasicMaterial({color:0xa8b8ff,transparent:true,opacity:.5,toneMapped:false}),gold=0xffc23a,pieces=[];for(let i=0;i<NP;i++){const a=i/NP*6.2832+1.57,p=new THREE.Mesh(new THREE.BoxGeometry(.5,.2,.38),ghost);p.position.set(Math.cos(a)*RAD,Math.sin(a)*RAD,0);p.rotation.z=a+1.57;wheel.add(p);pieces.push(p)}
 const spokes=[];for(let i=0;i<8;i++){const a=i/8*6.2832+1.57,sp=new THREE.Mesh(new THREE.BoxGeometry(RAD,.07,.07),ghost);sp.position.set(Math.cos(a)*RAD/2,Math.sin(a)*RAD/2,0);sp.rotation.z=a;wheel.add(sp);spokes.push(sp)}
 const COLS=[0xff4d6d,0x20e8d8,0xffc23a,0x7dff6a,0xff7a2e,0x8a7dff,0xff3fb0,0x4dc3ff];const gond=COLS.map((c,i)=>{const a=i/8*6.2832+1.57,q=box(.62,.56,.56,c,.08,{emissive:c,emissiveIntensity:.25});q.position.set(Math.cos(a)*RAD,Math.sin(a)*RAD-.42,0);wheel.add(q);return q});
 const on=new THREE.MeshStandardMaterial({color:gold,emissive:gold,emissiveIntensity:.9,roughness:.4});const hot=new THREE.MeshBasicMaterial({color:0xffffff,toneMapped:false});const sprk=new THREE.Sprite(new THREE.SpriteMaterial({map:glowTex,color:0xffd040,transparent:true,blending:THREE.AdditiveBlending,depthWrite:false}));scene.add(sprk);
 // v18 (07/11): rótulo integrado en la base con las piezas (n/50) y cabinas que caen colgando con muelle + destello al aparecer
 const sc=document.createElement('canvas');sc.width=512;sc.height=160;const sg=sc.getContext('2d');const stex=new THREE.CanvasTexture(sc);stex.colorSpace=THREE.SRGBColorSpace;let slast='';const sign=new THREE.Mesh(new THREE.PlaneGeometry(3.2,1),new THREE.MeshBasicMaterial({map:stex,transparent:true,toneMapped:false}));sign.position.set(0,1.05,1.2);g.add(sign);
 const setSign=n=>{const k=String(n);if(k===slast)return;slast=k;sg.clearRect(0,0,512,160);sg.fillStyle='#10131f';sg.beginPath();sg.roundRect(6,6,500,148,30);sg.fill();sg.lineWidth=10;sg.strokeStyle='#ffc23a';sg.stroke();sg.textAlign='center';sg.textBaseline='middle';sg.font='900 96px sans-serif';sg.fillStyle='#ffc23a';sg.fillText(n+' / 50',256,84);stex.needsUpdate=true};
 const cntAt=t=>{const a=TL.s2[0];const n0=Math.max(0,J.old-250),n1=Math.max(0,J.n-250);return n0+(n1-n0)*ss(a+.6,a+(TL.s2[1]-a)*.9,t)};
 const tCross=v=>{let lo=0,hi=J.total;if(cntAt(hi)<v)return 1e9;if(cntAt(0)>=v)return -1e9;for(let i=0;i<40;i++){const m=(lo+hi)/2;if(cntAt(m)>=v)hi=m;else lo=m}return hi};
 const gT=gond.map((q,i)=>tCross((i+1)*50/8-1));const gF=gond.map((q,i)=>{const f=new THREE.Sprite(new THREE.SpriteMaterial({map:glowTex,color:0xfff0c0,transparent:true,opacity:0,blending:THREE.AdditiveBlending,depthWrite:false}));f.scale.set(2.6,2.6,1);f.position.copy(q.position);wheel.add(f);return f});
 NOR={x:nx,z:nz,HUB,RAD,draw(t,s){const a=TL.s2[0],b=TL.s3[1];const n0=Math.max(0,J.old-250),n1=Math.max(0,J.n-250);const cnt=cntAt(t);const k=Math.floor(cnt+1e-6);setSign(Math.min(50,k));pieces.forEach((p,i)=>{p.material=i<k?on:ghost;p.scale.setScalar(i<k?1.25:1);if(i<k&&i===k-1&&cnt<n1)p.material=hot});gond.forEach((q,i)=>{const need=(i+1)*50/8;q.visible=cnt>=need-1;const age=t-gT[i];if(q.visible&&age>=0&&age<1.6){const sp=1-Math.exp(-age*5)*Math.cos(age*14);q.scale.setScalar(Math.max(.01,sp));q.rotation.z=Math.exp(-age*3)*Math.sin(age*9)*.5;gF[i].material.opacity=.9*Math.exp(-age*2.2)}else{q.scale.setScalar(1);q.rotation.z=Math.sin(t*1.3+i)*.04;gF[i].material.opacity=0}});spokes.forEach((sp,i)=>{sp.material=cnt>=(i+1)*50/8-1?on:ghost});
  if(J.n>=300)wheel.rotation.z=t*.5;else wheel.rotation.z=Math.sin(t*.8)*.012;
  const ang=k/50*6.2832+1.57;const wp=new THREE.Vector3(nx+Math.cos(ang)*RAD,HUB+Math.sin(ang)*RAD,nz+.3);sprk.position.copy(wp);const go=cnt<n1&&cnt>n0;const pul=.5+.5*Math.sin(t*30);sprk.visible=(s==='s2'||s==='s3')&&(go||s==='s3');sprk.scale.setScalar(go?2+pul*1.5:1.2+.5*Math.sin(t*4));sprk.material.opacity=go?.9:.65}}}
// --- v19 (08/11): GUIRNALDAS DE BOMBILLAS de la noria: dos cadenas con catenaria del eje a dos farolas; se encienden en cascada al pasar la mitad (pieza 25)
const glowS=(col,size,op)=>{const g=new THREE.Sprite(new THREE.SpriteMaterial({map:glowTex,color:col,opacity:op,transparent:true,blending:THREE.AdditiveBlending,depthWrite:false}));g.scale.set(size,size,1);return g};
if(NOR&&J.n-250>=25){const GB=[];const cols=[0xff4d6d,0xffc23a,0x20e8d8,0x7dff6a,0xff7a2e,0x8a7dff];const top=V3(NOR.x,NOR.HUB+.15,NOR.z+.85);
 [-1,1].forEach(sd=>{const pole=new THREE.Group();const pb=new THREE.Mesh(new THREE.BoxGeometry(.18,4,.18),new THREE.MeshStandardMaterial({color:0x2a2a38}));pb.position.y=2;const lp=new THREE.Mesh(new THREE.BoxGeometry(.5,.35,.5),new THREE.MeshStandardMaterial({color:0xfff0c0,emissive:0xffd070,emissiveIntensity:.8}));lp.position.y=4.1;pole.add(pb,lp);pole.position.set(NOR.x+sd*5.2,0,NOR.z+1.4);scene.add(pole);
  const end=V3(NOR.x+sd*5.2,4,NOR.z+1.4);const n=16;for(let i=1;i<=n;i++){const u=i/(n+1);const pp=top.clone().lerp(end,u);pp.y-=Math.sin(u*Math.PI)*1.1;const c=cols[(i+(sd>0?3:0))%cols.length];const b=new THREE.Mesh(new THREE.SphereGeometry(.13,10,8),new THREE.MeshStandardMaterial({color:0x333344,emissive:c,emissiveIntensity:0}));b.position.copy(pp);scene.add(b);const g=glowS(c,.9,0);g.position.copy(pp);scene.add(g);GB.push({b,g,u:sd>0?u:u,c})}
  const wire=new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(Array.from({length:12},(_,k)=>{const u=k/11;const pp=top.clone().lerp(end,u);pp.y-=Math.sin(u*Math.PI)*1.1;return pp})),40,.025,4),new THREE.MeshStandardMaterial({color:0x1a1a22}));scene.add(wire)});
 const t0=Math.max(TL.s3?TL.s3[0]+.35:0,0);const _d=NOR.draw;NOR.draw=(t,s)=>{_d(t,s);GB.forEach((o,i)=>{const on=ss(t0+o.u*1.3,t0+o.u*1.3+.12,t);const tw=.75+.25*Math.sin(t*6+i*1.7);o.b.material.emissiveIntensity=on*2.2*tw;o.g.material.opacity=on*.85*tw})}}
const tmp=new THREE.Color(),black=new THREE.Color(0x0a0e22),amber=new THREE.Color(0xffc23a);
// --- v20 (09/11): FOCO BUSCADOR (J.spot): un cañón de luz barre la ciudad en s2 y se clava en la ventana nueva (J.n-1). Para días de pocas ventanas: se ve CUÁL es.
let SPOT=null;if(J.spot){const W0=WIN[Math.min(J.n-1,WIN.length-1)],src=V3(W0.x+4.2,.2,W0.z+8);const L=1;const geo=new THREE.ConeGeometry(.55,1,32,1,true);geo.translate(0,-.5,0);geo.rotateX(-Math.PI/2);
 const mat=new THREE.MeshBasicMaterial({color:0xfff0c0,transparent:true,opacity:.0,blending:THREE.AdditiveBlending,depthWrite:false,side:THREE.DoubleSide,toneMapped:false});const beam=new THREE.Mesh(geo,mat);beam.position.copy(src);scene.add(beam);
 const base=new THREE.Mesh(new THREE.CylinderGeometry(.45,.6,.5,16),new THREE.MeshStandardMaterial({color:0x30343c,roughness:.6}));base.position.set(src.x,.25,src.z);scene.add(base);
 const lens=new THREE.Sprite(new THREE.SpriteMaterial({map:glowTex,color:0xfff2c0,transparent:true,blending:THREE.AdditiveBlending,depthWrite:false}));lens.position.copy(src).add(V3(0,.3,0));lens.scale.setScalar(1.6);scene.add(lens);
 const hal=new THREE.Sprite(new THREE.SpriteMaterial({map:glowTex,color:0xffe080,transparent:true,blending:THREE.AdditiveBlending,depthWrite:false,opacity:0}));hal.position.set(W0.x,W0.y,W0.z+.25);scene.add(hal);
 const a=TL.s2[0],lock=a+Math.min(2.2,(TL.s2[1]-a)*.55);const tgt=V3();
 SPOT={lock,idx:Math.min(J.n-1,WIN.length-1),draw(t,s){const on=s==='s2'||s==='s3'||(s==='s1'&&t>TL.s1[1]-.6);beam.visible=base.visible=lens.visible=on;hal.visible=on||s==='cta';
  const k=ss(a-.2,lock,t);const sw=(1-k);tgt.set(W0.x+Math.sin(t*2.3)*7*sw,W0.y+Math.cos(t*1.7)*4*sw,W0.z);
  const d=src.distanceTo(tgt);beam.scale.set(1+d*.04,1+d*.04,d);beam.lookAt(tgt);beam.position.copy(src);mat.opacity=.10+.08*Math.sin(t*9)*(1-k)+.12*k;
  const lk=ss(lock,lock+.25,t);hal.material.opacity=lk*(.85+.15*Math.sin(t*6));hal.scale.setScalar(1.2+2.2*lk+1.5*Math.exp(-Math.max(0,t-lock)*3)*lk)}};
 shots.s2={p:V3(W0.x+1.3,W0.y+1.1,W0.z+13.5),q:V3(W0.x+.2,W0.y-.4,W0.z)}}
window.renderAt=t=>{const s=seg(t);const{p,q}=camAt(t);if(panel){drawPanel(t);panel.visible=s!=='s2'}if(NOR)NOR.draw(t,s);if(SPOT)SPOT.draw(t,s);if(FW.length)drawFW(t);cam.position.copy(p);cam.lookAt(q);
 // cuántas encendidas
 const a1=TL.s1[0],b1=TL.s1[1];const lit=J.old+(J.n-J.old)*ss(a1+.5,b1-.25,t);
 const red_a=TL.s2?TL.s2[0]+1.4:1e9;
 const col=wins.instanceColor;WIN.forEach((w,i)=>{let c;let g=0;
  if(i<lit){const age=lit-i;c=tmp.copy(WARM[w.k%4]);g=.32;const flick=.92+.08*Math.sin(t*(1.5+(w.k%7)*.3)+w.k);c.multiplyScalar(flick);
   if(i>=J.old&&age<3.5){const e=Math.exp(-age*.9);c.lerp(new THREE.Color(0xffffff),e);g+=e*1.6}
   const sp=SPECIAL.get(i);if(sp){const on=sp.fresh?ss(red_a+sp.seq*.42,red_a+sp.seq*.42+.12,t):1;if(on>0){c.lerp(new THREE.Color(sp.color),on);g=.32+on*(.95+.3*Math.sin(t*3+i));if(sp.fresh){const pop=Math.exp(-Math.max(0,t-red_a-sp.seq*.42)*2.4)*on;g+=pop*3}}}
  }else{c=tmp.copy(black);
   const lead=s==='s3'||s==='cta';if(lead){const pu=.5+.5*Math.sin(t*4+i*.8);const k=J.goal>=500?.5:1;c.lerp(amber,(.1+.24*pu)*k);g=(.05+.08*pu)*k}
   if(J.vote&&i===lastIdx&&s==='cta'){const pu=.5+.5*Math.sin(t*7);c.set(0xffffff).multiplyScalar(.45+.55*pu);g=.7+.9*pu}}
  if(J.hito&&i!==J.hito-1){const d=1-.68*ss(TL.s2[0]+.9,TL.s2[0]+1.5,t)*(1-ss(TL.s2[1]-.5,TL.s2[1],t));c.multiplyScalar(d);g*=d}else if(J.hito&&t>TL.s2[0]+1.2){c.set(0xffa800);g=1.6+.5*Math.sin(t*5)}if(J.noria){const dk=1-.72*ss(TL.s2[0]+.2,TL.s2[0]+.9,t)*(1-ss(TL.s3[1]-.6,TL.s3[1],t));c.multiplyScalar(dk);g*=dk}if(SPOT&&i===SPOT.idx){const on=ss(SPOT.lock,SPOT.lock+.2,t);if(on>0){c.lerp(new THREE.Color(0xfff2b0),on);g=Math.max(g,(1.8+.6*Math.sin(t*6))*on)}}wins.setColorAt(i,c);gc[i*3]=c.r*g;gc[i*3+1]=c.g*g;gc[i*3+2]=c.b*g});
 col.needsUpdate=true;gg.attributes.color.needsUpdate=true;
 // grúa, balizas, coches
 crane.visible=s!=='s2';const U=crane.userData;U.J2.rotation.y=Math.sin(t*.32)*.4-.2;const tx=-3-1.7*Math.sin(t*.7),ln=2.2+1.1*Math.sin(t*.9);U.c.position.set(tx,-ln/2,0);U.c.scale.y=ln;U.beam.position.set(tx,-ln-.1,0);U.beam.rotation.y=Math.sin(t*.8)*.5;U.lamp.material.opacity=Math.floor(t*2)%2?1:.1;
 if(skyG[0])skyG[0].material.opacity=.55+.45*Math.sin(t*4);blds.forEach(b=>{if(b.beacon)b.beacon.material.opacity=.55+.45*Math.sin(t*3+b.i)});
 cars.forEach(g=>{const u=g.userData;g.position.set(((t*u.v*u.d+u.o+60)%120+120)%120-60,0,u.z)});
 // personaje
 const m=J.mouth[Math.min(J.mouth.length-1,Math.floor(t*30))]||0;mouth.scale.y=1+m*2.4;mouth.position.y=-.38-m*.07;
 const bl=(t%3.1)>2.96;eyes.forEach(e=>{e.scale.y=bl?.1:1;const pp=e.userData.p;pp.position.x=Math.sin(t*.7)*.03;pp.position.y=s==='h'?-.01:.03});
 headG.rotation.y=Math.sin(t*.9)*.12+(s==='h'?0:-.2);headG.rotation.x=Math.sin(t*2.6)*.035-m*.05;headG.position.y=3.05+Math.sin(t*2.2)*.02;
 const c0=s==='cta'||s==='h';const wave=c0?(.5+.5*Math.sin(t*6)):0;armR.rotation.z=c0?2.55+wave*.35:.16+Math.sin(t*1.7)*.05;armR.rotation.x=0;armL.rotation.z=-.16-Math.sin(t*1.5)*.05-m*.25;armL.rotation.x=-m*.5;
 hero.visible=lift.visible=!(J.hito&&s==='s2');hero.rotation.y=-.1+Math.sin(t*.6)*.05;hero.position.y=Math.abs(Math.sin(t*2.1))*.03;
 r.render(scene,cam);return true};
window.layout={w283:J.spot?[WIN[J.n-1].x,WIN[J.n-1].y,WIN[J.n-1].z,wideZ]:0,wins:WIN.length,blds:blds.length,lastBuilt:LAST.floors};if(J.spot&&J.debug)console.error("LAYOUT",JSON.stringify(window.layout),JSON.stringify(blds.map(b=>[b.x,b.z,b.w,b.d,b.h].map(v=>v==null?null:+(+v).toFixed(2)))));window.ready=true;
