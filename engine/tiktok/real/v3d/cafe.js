// ¿El café te deshidrata? (3003, mito 3D). Killer, Blannin y Jeukendrup, Universidad de Birmingham, PLOS ONE 09/01/2014.
// Nuevo y reutilizable: COCINA de bloques (encimera, cafetera, ventana), mug()+steam() (taza con vapor), DEPÓSITO de agua del cuerpo con nivel animado (tank),
// LABORATORIO con 50 voluntarios (crowd) y dos depósitos que se llenan igual. La capataz bebe con la taza en la mano.
import {THREE,J,mk,ss,V3,clamp,stage,sun,box,pixTex,capataz,segAt,mouthAt,puffs,label3d,crowd,glassCup,mug,steam} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x2a2230,exposure:1.1});const R=mk(3003);
const hemi=new THREE.HemisphereLight(0xfff1dc,0x6a5a4a,1.25);scene.add(hemi);const S=sun(scene,{pos:[-10,22,16],span:22});
const warm=new THREE.PointLight(0xffc98a,30,40,1.6);warm.position.set(2,8,6);scene.add(warm);
// ---------- cocina
const K=new THREE.Group();scene.add(K);
const tiles=pixTex(64,64,(g,w,h)=>{g.fillStyle='#e9e1d2';g.fillRect(0,0,w,h);g.fillStyle='#c9bba3';for(let y=0;y<h;y+=16)for(let x=(y/16%2)*8;x<w;x+=16)g.fillRect(x,y,8,8)},[18,18]);
const floor=new THREE.Mesh(new THREE.PlaneGeometry(140,140),new THREE.MeshStandardMaterial({map:tiles,roughness:.8}));floor.rotation.x=-Math.PI/2;floor.receiveShadow=true;K.add(floor);
const wallT=pixTex(64,64,(g,w,h)=>{g.fillStyle='#f4efe6';g.fillRect(0,0,w,h);g.strokeStyle='#d8cfc0';g.lineWidth=2;for(let y=0;y<h;y+=8)for(let x=0;x<w;x+=16)g.strokeRect(x+(y/8%2)*8,y,16,8)},[10,4]);
const wall=new THREE.Mesh(new THREE.PlaneGeometry(60,24),new THREE.MeshStandardMaterial({map:wallT,roughness:.9}));wall.position.set(0,12,-6);wall.receiveShadow=true;K.add(wall);
const counter=box(16,3.4,3,0x8a5a3a,.05);counter.position.set(-1,1.7,-4.4);K.add(counter);const ctop=box(16.4,.3,3.3,0x2f3238,.03);ctop.position.set(-1,3.55,-4.4);K.add(ctop);
[-7,-3,1,5].forEach(x=>{const d=box(3.6,2.8,.1,0x9d6a46,.03);d.position.set(x,1.7,-2.88);K.add(d);const kn=box(.5,.14,.14,0xd8d8d8,.02);kn.position.set(x,2.6,-2.8);K.add(kn)});
// cafetera
const CM=new THREE.Group();CM.position.set(-5.5,3.7,-4.6);K.add(CM);const cb=box(2.4,3.0,2,0x2c2f36,.12);cb.position.y=1.5;CM.add(cb);const ch=box(2.4,.6,2.4,0x3a3e47,.08);ch.position.set(0,3.1,.2);CM.add(ch);const cp=box(.5,.4,.5,0xc0c4cc,.03);cp.position.set(0,2.4,1.1);CM.add(cp);
const led=box(.3,.18,.05,0x40ff8a,.01);led.material.emissive=new THREE.Color(0x40ff8a);led.material.emissiveIntensity=2;led.position.set(.7,2.4,1.02);CM.add(led);
// ventana con luz de mañana
const win=new THREE.Mesh(new THREE.PlaneGeometry(6,4.5),new THREE.MeshBasicMaterial({color:0xbfe6ff,toneMapped:false}));win.position.set(5,8.5,-5.95);K.add(win);
[[5,10.85,6.6,.3],[5,6.15,6.6,.3],[1.85,8.5,.3,4.9],[8.15,8.5,.3,4.9],[5,8.5,.2,4.6],[5,8.5,6.2,.2]].forEach(([x,y,w,h])=>{const f=box(w,h,.2,0xffffff,.02);f.position.set(x,y,-5.85);K.add(f)});
// plantas y tarros
[[2.5,'#3f9a46'],[6.5,'#5fb24e']].forEach(([x,c])=>{const p=box(.9,.9,.9,0xb8643a,.05);p.position.set(x,4.15,-4.6);K.add(p);const l=box(1.2,1.1,1.2,parseInt(c.slice(1),16),.3);l.position.set(x,5.1,-4.6);K.add(l)});
// depósito: 'agua de tu cuerpo'
function tank(col=0x4aa8ff){const g=new THREE.Group();const gl=new THREE.Mesh(new THREE.CylinderGeometry(1.4,1.4,6,28,1,true),new THREE.MeshStandardMaterial({color:0xcfefff,transparent:true,opacity:.28,roughness:.05,side:THREE.DoubleSide,depthWrite:false}));gl.position.y=3;g.add(gl);
 const base=box(3.3,.3,3.3,0x50545e,.05);base.position.y=.15;g.add(base);const lid=box(3.3,.25,3.3,0x50545e,.05);lid.position.y=6.1;g.add(lid);
 const w=new THREE.Mesh(new THREE.CylinderGeometry(1.32,1.32,1,28),new THREE.MeshStandardMaterial({color:col,transparent:true,opacity:.82,roughness:.1,emissive:col,emissiveIntensity:.15}));g.add(w);
 for(let i=1;i<6;i++){const m=box(.5,.06,.06,0xffffff,.01);m.position.set(-1.38,i,1.0);g.add(m)}
 g.level=f=>{w.scale.y=Math.max(.02,f*5.7);w.position.y=.3+f*5.7/2};return g}
const T1=tank();T1.position.set(3.8,0,-.6);K.add(T1);
const tLab=label3d(['AGUA DE','*TU CUERPO'],{w:3.6,h:1.6,px:110,accent:'#4de3ff'});tLab.position.set(3.8,7.0,-.6);K.add(tLab);
const q1=label3d(['*¿?'],{w:1.6,h:1.2,px:160,accent:'#ff4a4a'});q1.position.set(6.2,4.6,-.4);K.add(q1);
const hero=capataz();hero.g.position.set(-1.6,0,0);hero.g.rotation.y=.25;K.add(hero.g);
const hm=mug(0xe84a3a);hm.scale.setScalar(.7);hm.position.set(0,-1.75,.25);hm.rotation.x=0;hero.armR.add(hm);
const ST=puffs(scene,80,.5,0xffffff,{opacity:.35,depthWrite:false});
// mesas del experimento (s2): 4 tazas de café frente a 4 vasos de agua, 3 días
const TB=new THREE.Group();K.add(TB);
const tab=(x)=>{const t=box(6.2,.3,2.6,0xb98a5a,.05);t.position.set(x,3.0,1.2);TB.add(t);[[-2.8,-1],[2.8,-1],[-2.8,1],[2.8,1]].forEach(([a,b])=>{const l=box(.25,2.9,.25,0x7a5232,.03);l.position.set(x+a,1.45,1.2+b);TB.add(l)})};tab(-3.6);tab(3.6);
const mugs=[0,1,2,3].map(i=>{const m=mug(0xf2efe8);m.position.set(-5.7+i*1.4,3.15,1.2);m.scale.setScalar(.8);TB.add(m);return m});
const cups=[0,1,2,3].map(i=>{const c=glassCup();c.position.set(1.5+i*1.4,3.15,1.2);c.scale.setScalar(.9);TB.add(c);return c});
const lC=label3d(['*CAFÉ','4 tazas'],{w:3.6,h:1.6,px:110,accent:'#c8874a'});lC.position.set(-3.6,6.2,1.2);TB.add(lC);
const lW=label3d(['*AGUA','4 vasos'],{w:3.6,h:1.6,px:110,accent:'#4de3ff'});lW.position.set(3.6,6.2,1.2);TB.add(lW);
const day=label3d(['DÍA 1'],{w:3.4,h:1.1,px:120,accent:'#ffc23a'});day.position.set(0,8.4,0);TB.add(day);
// ---------- laboratorio (s1, s3) a x=200
const L=new THREE.Group();L.position.set(200,0,0);scene.add(L);
const lf=new THREE.Mesh(new THREE.PlaneGeometry(80,60),new THREE.MeshStandardMaterial({map:pixTex(32,32,(g,w,h)=>{g.fillStyle='#dfe6ec';g.fillRect(0,0,w,h);g.strokeStyle='#c4cdd6';g.strokeRect(0,0,w,h)},[20,15]),roughness:.7}));lf.rotation.x=-Math.PI/2;lf.receiveShadow=true;L.add(lf);
const lw=new THREE.Mesh(new THREE.PlaneGeometry(80,30),new THREE.MeshStandardMaterial({color:0xeef3f6,roughness:.9}));lw.position.set(0,15,-14);L.add(lw);
const banner=label3d(['UNIVERSIDAD DE BIRMINGHAM','*2014'],{w:12,h:2.6,px:90,accent:'#ffc23a'});banner.position.set(0,11.5,-13.8);L.add(banner);
const CR=crowd(scene,50,{s:1,seed:14});const crowdP=[];for(let i=0;i<50;i++){const row=Math.floor(i/10),col=i%10;crowdP.push([200-11.25+col*2.5,0,-9+row*2.6])}
const n50=label3d(['*50 HOMBRES'],{w:8,h:1.8,px:140,sprite:true,accent:'#ffc23a'});n50.position.set(200,7.5,0);scene.add(n50);
const T2=tank(0x7b4a2a),T3=tank();T2.position.set(-3.2,0,2);T3.position.set(3.2,0,2);L.add(T2,T3);
const lT2=label3d(['*CAFÉ'],{w:3.4,h:1,px:120,accent:'#c8874a'});lT2.position.set(-3.2,7.1,2);L.add(lT2);
const lT3=label3d(['*AGUA'],{w:3.4,h:1,px:120,accent:'#4de3ff'});lT3.position.set(3.2,7.1,2);L.add(lT3);
const eq=label3d(['*='],{w:1.8,h:1.6,px:200,sprite:true,accent:'#4ade80',bg:null});eq.position.set(200,3.4,3);scene.add(eq);
const meas=label3d(['SANGRE · ORINA · AGUA'],{w:8,h:1.0,px:80,accent:'#9ad8ff'});meas.position.set(0,8.4,-1);L.add(meas);
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],k=ss(0,d,lt),m=mouthAt(t);let p,q;
 const inLab=s==='s1'||s==='s3';K.visible=!inLab;L.visible=inLab;CR.body.visible=CR.head.visible=s==='s1';n50.visible=s==='s1'&&lt>1.2;eq.visible=s==='s3'&&lt>d*.55;
 T2.visible=T3.visible=lT2.visible=lT3.visible=meas.visible=s==='s3';TB.visible=s==='s2';T1.visible=s!=='s2';tLab.visible=s!=='s2'&&s!=='cta';banner.visible=s==='s1';hero.g.visible=s!=='s2';q1.visible=s==='h'&&lt>1.0;ST.m.visible=false;led.visible=(t%1)<.6;
 if(!inLab){scene.background=new THREE.Color(0x2a2230);
  if(s==='s2'){// 3 días: tazas y vasos que aparecen uno a uno y se vacían
   const dd=Math.min(3,1+Math.floor(lt/(d/3)));day.set([`*DÍA ${dd} de 3`]);const ph=(lt%(d/3))/(d/3);
   mugs.forEach((mm,i)=>{const a=ss(i*.12,i*.12+.1,ph);mm.scale.setScalar(.8*a+.001);mm.userData.coffee.position.y=.86-.8*ss(.55+i*.08,.65+i*.08,ph)});
   cups.forEach((c,i)=>{const a=ss(i*.12,i*.12+.1,ph);c.scale.setScalar(.9*a+.001);c.children[2].scale.y=Math.max(.02,1-ss(.55+i*.08,.65+i*.08,ph))});
   ST.m.visible=true;mugs.forEach((mm,i)=>steam(ST,i*20,20,mm.position.x,4.1,1.2,t+i,.8));ST.done();
   p=V3(Math.sin(t*.3)*.8,7.0,40-k*2);q=V3(0,4.8,0)}
  else{const drink=s==='s4'?ss(.3,1.3,lt)*(1-ss(d-1.2,d-.4,lt)):s==='cta'?0:s==='h'?ss(.4,1.2,lt)*(1-ss(2.2,2.8,lt)):0;
   hero.pose(t,drink>.5?0:m,{wave:s==='cta'?1:0,look:s==='cta'?.1:.2});hero.armR.rotation.x=-drink*2.1;hero.armR.rotation.z=.14+drink*.35;hm.rotation.x=drink*1.7;
   ST.m.visible=true;const mp=new THREE.Vector3();hm.getWorldPosition(mp);steam(ST,0,20,mp.x,mp.y+.7,mp.z,t,.7);for(let i=20;i<80;i++)ST.set(i,0,-50,0,0);ST.done();
   const lev=s==='h'?.85-.45*ss(1.4,3.4,lt):s==='s4'?.4+.48*ss(.6,2.6,lt):.88;T1.level(lev);T1.children[3].material.color.setHex(s==='h'&&lt>1.4?0xff6a5a:0x4aa8ff);
   if(s==='h'){p=V3(1.3+Math.sin(t*.4)*.4,5.2,28-k*2.5);q=V3(1.3,4.4,-.5)}
   else if(s==='s4'){p=V3(1.3+Math.sin(t*.4)*.4,5.2,28-k*2);q=V3(1.3,4.4,-.5)}
   else{p=V3(.8,2.6,31+k);q=V3(.8,1.8,-.5)}}
  S.intensity=1.6;hemi.intensity=1.25;warm.intensity=30}
 else{scene.background=new THREE.Color(0xdfe6ec);warm.intensity=0;hemi.intensity=1.5;S.intensity=1.8;
  if(s==='s1'){for(let i=0;i<50;i++){const[x,y,z]=crowdP[i];const a=ss(i*.03,i*.03+.4,lt);CR.set(i,x,y+(1-a)*6,z,a+.001,Math.sin(t+i)*.2)}CR.done();
   p=V3(200+Math.sin(t*.25)*2,18-k*2,50-k*4);q=V3(200,3.2,-3)}
  else{const f=.25+.6*ss(.4,d*.6,lt);T2.level(f+.01*Math.sin(t*3));T3.level(f+.01*Math.sin(t*3+1));
   p=V3(200+Math.sin(t*.3)*.8,6.4,36-k*2);q=V3(200,5.0,1)}}
 cam.position.copy(p);cam.lookAt(q);r.render(scene,cam)};
window.ready=true;
