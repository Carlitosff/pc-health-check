// MUNDO DE BLOQUES (motor v15, 04/11): piezas comunes para las escenas 3D. Personajes propios de la cuenta: capataz (casco amarillo) y abuela.
import * as THREE from 'three';
import {RoundedBoxGeometry} from '/node_modules/three/examples/jsm/geometries/RoundedBoxGeometry.js';
export {THREE};
export const W=1080,H=1920;
export const J=await (await fetch('/job.json')).json();
export const mk=s=>()=>{s=(s+0x6D2B79F5)|0;let t=Math.imul(s^s>>>15,1|s);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296};
export const ss=(a,b,x)=>{x=Math.min(1,Math.max(0,(x-a)/(b-a)));return x*x*(3-2*x)};
export const V3=(...a)=>new THREE.Vector3(...a);
export const clamp=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
export function stage({bg=0x7fc8ff,fog=null,fov=35,exposure=1.15,shadow=[0,0,0]}={}){
 const r=new THREE.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});r.setSize(W,H,false);r.setPixelRatio(1);
 r.toneMapping=THREE.ACESFilmicToneMapping;r.toneMappingExposure=exposure;r.shadowMap.enabled=true;r.shadowMap.type=THREE.PCFSoftShadowMap;document.body.prepend(r.domElement);
 const scene=new THREE.Scene();scene.background=new THREE.Color(bg);if(fog)scene.fog=new THREE.Fog(fog[0],fog[1],fog[2]);
 const cam=new THREE.PerspectiveCamera(fov,W/H,.1,500);return{r,scene,cam}}
// sol con sombra suave: la sombra de contacto es lo que más "pega" los personajes al suelo
export function sun(scene,{pos=[-14,26,14],color=0xfff0d8,power=2.6,span=26,target=[0,0,0]}={}){const d=new THREE.DirectionalLight(color,power);d.position.set(...pos);d.target.position.set(...target);scene.add(d.target);d.castShadow=true;d.shadow.mapSize.set(1024,1024);const c=d.shadow.camera;c.left=-span;c.right=span;c.top=span;c.bottom=-span;c.near=1;c.far=120;d.shadow.bias=-.0006;d.shadow.normalBias=.03;scene.add(d);return d}
export const box=(w,h,d,col,rad=.05,opt={})=>{const m=new THREE.Mesh(new RoundedBoxGeometry(w,h,d,2,rad),new THREE.MeshStandardMaterial({color:col,roughness:.72,...opt}));m.castShadow=true;m.receiveShadow=true;return m};
export const glowTex=(()=>{const c=document.createElement('canvas');c.width=c.height=128;const g=c.getContext('2d');const d=g.createRadialGradient(64,64,0,64,64,64);d.addColorStop(0,'rgba(255,255,255,1)');d.addColorStop(.25,'rgba(255,255,255,.45)');d.addColorStop(1,'rgba(255,255,255,0)');g.fillStyle=d;g.fillRect(0,0,128,128);return new THREE.CanvasTexture(c)})();
export const glow=(col,size,op=.8)=>{const s=new THREE.Sprite(new THREE.SpriteMaterial({map:glowTex,color:col,opacity:op,transparent:true,blending:THREE.AdditiveBlending,depthWrite:false}));s.scale.set(size,size,1);return s};
export function pixTex(w,h,draw,rep=[1,1]){const c=document.createElement('canvas');c.width=w;c.height=h;draw(c.getContext('2d'),w,h);const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;t.magFilter=THREE.NearestFilter;t.wrapS=t.wrapT=THREE.RepeatWrapping;t.repeat.set(...rep);return t}
// personaje genérico con piernas y brazos articulados
export function rig({skin,body,legC,shoe}){const g=new THREE.Group(),head=new THREE.Group();head.position.y=3.05;g.add(head);head.add(box(1.5,1.3,1.3,skin,.12));
 const eyes=[-.34,.34].map(x=>{const e=new THREE.Group();const w=box(.34,.4,.05,0xfdf8f0,.02);const p=box(.17,.25,.04,0x15101c,.02);p.position.z=.04;e.add(w,p);e.position.set(x,.14,.66);e.userData.p=p;head.add(e);return e});
 const nose=box(.2,.24,.14,0xc98c58,.05);nose.position.set(0,-.08,.69);head.add(nose);
 const mouth=box(.46,.1,.05,0x4a1a14,.02);mouth.position.set(0,-.38,.66);head.add(mouth);
 const torso=box(1.5,1.5,.95,body,.1);torso.position.y=1.65;g.add(torso);
 const arm=x=>{const a=new THREE.Group();a.position.set(x,2.3,0);const s=box(.44,1.3,.48,body,.08);s.position.y=-.58;const h=box(.46,.4,.5,skin,.08);h.position.y=-1.34;a.add(s,h);g.add(a);return a};
 const leg=x=>{const a=new THREE.Group();a.position.set(x,.95,0);const l=box(.6,.72,.72,legC,.06);l.position.y=-.4;const f=box(.66,.26,.92,shoe,.06);f.position.set(0,-.82,.1);a.add(l,f);g.add(a);return a};
 const o={g,head,eyes,mouth,armL:arm(-1.0),armR:arm(1.0),legL:leg(-.42),legR:leg(.42)};
 // pose: m=boca (0-1), wave, walk (fase o null), look (giro cabeza)
 o.pose=(t,m=0,{wave=0,walk=null,look=0,armsUp=0,point=0}={})=>{mouth.scale.y=1+m*2.4;mouth.position.y=-.38-m*.07;const bl=(t%3.1)>2.96;eyes.forEach(e=>{e.scale.y=bl?.1:1});head.rotation.y=look+Math.sin(t*.9)*.1;head.rotation.x=Math.sin(t*2.6)*.035-m*.05;
  const w=walk===null?0:Math.sin(walk)*.7;o.legL.rotation.x=w;o.legR.rotation.x=-w;
  o.armR.rotation.set(-w*.7,0,.14+Math.sin(t*1.7)*.05);o.armL.rotation.set(w*.7-m*.4,0,-.14-Math.sin(t*1.5)*.05);
  if(wave>0){o.armR.rotation.z=.14+wave*(2.45+.35*Math.sin(t*7))}
  if(armsUp>0){o.armR.rotation.z=.14+armsUp*2.7+Math.sin(t*5)*.12*armsUp;o.armL.rotation.z=-.14-armsUp*2.7-Math.sin(t*5)*.12*armsUp}
  if(point>0){o.armR.rotation.x=-point*1.6;o.armR.rotation.z=.14;o.armR.rotation.x+=Math.sin(t*6)*.12*point}};
 return o}
export function capataz(){const o=rig({skin:0xd9a06a,body:0x1f7a8c,legC:0x154f5c,shoe:0x20161c});const h=o.head;const brim=box(1.9,.14,1.65,0xffc42e,.04);brim.position.set(0,.72,.1);const dome=box(1.5,.5,1.3,0xffc42e,.14);dome.position.y=.98;const ridge=box(.3,.16,1.1,0xf2a800,.05);ridge.position.y=1.28;h.add(brim,dome,ridge);o.hat=[brim,dome,ridge];const hair=box(1.54,.22,.3,0x3a2416,.04);hair.position.set(0,.5,-.55);h.add(hair);[-.34,.34].forEach(x=>{const b=box(.42,.09,.05,0x3a2416,.02);b.position.set(x,.42,.67);h.add(b)});const shirt=box(1,.5,.05,0xf4efe6,.02);shirt.position.set(0,2.15,.47);o.g.add(shirt);const stripe=box(1.54,.14,.99,0xffe25a,.02);stripe.position.y=1.5;o.g.add(stripe);return o}
export function abuela(){const o=rig({skin:0xe3b48c,body:0xb0487f,legC:0x4a4258,shoe:0x2a2230});const h=o.head;const hair=box(1.56,.46,1.36,0xd8d8de,.12);hair.position.y=.56;h.add(hair);const bun=box(.7,.56,.6,0xcfcfd6,.14);bun.position.set(0,.98,-.2);h.add(bun);[-.34,.34].forEach(x=>{const r=new THREE.Mesh(new THREE.TorusGeometry(.26,.04,6,14),new THREE.MeshStandardMaterial({color:0x2a2a38}));r.position.set(x,.14,.71);h.add(r)});const shawl=box(1.56,.42,1.02,0xf2e2c8,.08);shawl.position.y=2.2;o.g.add(shawl);return o}
// cámara por planos: {seg:{p,q}} se encadenan con un fundido corto
export function camera(cam,order,shots,TL,fade=.7){return(t,extra)=>{let p=shots[order[0]].p.clone(),q=shots[order[0]].q.clone();for(const k of order.slice(1)){if(!TL[k])continue;const a=TL[k][0],e=ss(a,a+fade,t);p.lerp(shots[k].p,e);q.lerp(shots[k].q,e)}p.x+=Math.sin(t*.55)*.3;p.y+=Math.sin(t*.8)*.1;if(extra)extra(p,q);cam.position.copy(p);cam.lookAt(q)}}
export const segAt=(TL,t)=>{let s=Object.keys(TL)[0];for(const[k,[a]]of Object.entries(TL))if(t>=a)s=k;return s};
export const mouthAt=t=>J.mouth[Math.min(J.mouth.length-1,Math.floor(t*30))]||0;

// --- v17 (06/11): piezas nuevas reutilizables
// multitud barata: 2 mallas instanciadas (cuerpo+cabeza). set(i,x,y,z,s,ry) y luego done()
export function crowd(scene,n,{s=1,seed=7,pal=[0xe5343f,0x2a7de1,0xf2c230,0x34b56a,0xf2f2f2,0x8a5cd6,0xff7a2e,0x20c4c4,0xd94f9a,0x39424e],skins=[0xe3b48c,0xd9a06a,0xa8724a,0x7a4e2e,0xf0cba8]}={}){
 const R=mk(seed),bm=new THREE.MeshStandardMaterial({roughness:.8}),hm=new THREE.MeshStandardMaterial({roughness:.8});
 const body=new THREE.InstancedMesh(new THREE.BoxGeometry(1.1,1.9,.8),bm,n),head=new THREE.InstancedMesh(new THREE.BoxGeometry(.9,.85,.85),hm,n);body.frustumCulled=head.frustumCulled=false;body.castShadow=true;
 const C=new THREE.Color();for(let i=0;i<n;i++){C.setHex(pal[Math.floor(R()*pal.length)]);body.setColorAt(i,C);C.setHex(skins[Math.floor(R()*skins.length)]);head.setColorAt(i,C)}
 scene.add(body,head);const O=new THREE.Object3D();
 return{body,head,set(i,x,y,z,k=s,ry=0){O.position.set(x,y+.95*k,z);O.rotation.set(0,ry,0);O.scale.setScalar(k);O.updateMatrix();body.setMatrixAt(i,O.matrix);O.position.y=y+2.3*k;O.updateMatrix();head.setMatrixAt(i,O.matrix)},done(){body.instanceMatrix.needsUpdate=true;head.instanceMatrix.needsUpdate=true}}}
// partículas de cubos sin sombra: set(i,x,y,z,s) ; color por instancia opcional
export function puffs(scene,n,size,col,opt={}){const m=new THREE.InstancedMesh(new THREE.BoxGeometry(size,size,size),new THREE.MeshBasicMaterial({color:col,toneMapped:false,transparent:true,...opt}),n);m.frustumCulled=false;scene.add(m);const O=new THREE.Object3D();return{m,set(i,x,y,z,s=1,w=0){O.position.set(x,y,z);O.rotation.set(w,w*.7,0);O.scale.setScalar(s);O.updateMatrix();m.setMatrixAt(i,O.matrix)},done(){m.instanceMatrix.needsUpdate=true}}}
// nieve que cae determinista en una caja
export function snow(scene,n,[x0,x1,y1,z0,z1],{size=.22,seed=3,col=0xffffff,speed=2.2}={}){const R=mk(seed),P=[];for(let i=0;i<n;i++)P.push([x0+R()*(x1-x0),R()*y1,z0+R()*(z1-z0),.7+R()*.6,R()*9]);const g=new THREE.BufferGeometry(),a=new Float32Array(n*3);g.setAttribute('position',new THREE.BufferAttribute(a,3));const pts=new THREE.Points(g,new THREE.PointsMaterial({color:col,size,transparent:true,opacity:.9}));pts.frustumCulled=false;scene.add(pts);return{pts,draw(t){P.forEach((p,i)=>{a[i*3]=p[0]+Math.sin(t*.7+p[4])*.7;a[i*3+1]=y1-((p[1]+t*speed*p[3])%y1);a[i*3+2]=p[2]});g.attributes.position.needsUpdate=true}}}
