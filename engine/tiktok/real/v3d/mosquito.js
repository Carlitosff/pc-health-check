// Mito: '¿te pican más porque tienes la sangre dulce?' (2403). Rockefeller University 18/10/2022 (De Obaldia y Vosshall, Cell):
// 8 personas, medias de nailon, olfatómetro de dos tubos, 3 años; la nº 33, 100× más atractiva que la nº 19 y 4× que la siguiente; ácidos carboxílicos del sebo.
// Reutilizable: TERRAZA DE NOCHE con farolillo, MOSQUITOS de bloques (mosquito/swarmPos en bloques.js) con enjambre y picaduras que salen,
// GOTA DE SANGRE con terrones que se tachan, OLFATÓMETRO en Y con dos cajas y medias, BARRAS HORIZONTALES 3D, PIEL DE VÓXELES con penacho de olor.
import {THREE,J,mk,ss,V3,clamp,stage,sun,box,glow,pixTex,capataz,abuela,segAt,mouthAt,label3d,puffs,stars,mosquito,swarmPos} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x0b1230,fog:[0x0b1230,45,160],exposure:1.15});cam.far=2000;cam.updateProjectionMatrix();const R=mk(2403);
const hemi=new THREE.HemisphereLight(0x8fa4e0,0x2a2030,.9);scene.add(hemi);const S=sun(scene,{pos:[-12,24,16],span:24,color:0xb8c8ff,power:1.1});
const warm=new THREE.PointLight(0xffc070,90,40,1.4);warm.position.set(4.5,7,3);scene.add(warm);
const ST=stars(scene,900);
// ---------- TERRAZA (x=0)
const T=new THREE.Group();scene.add(T);
const tiles=pixTex(64,64,(g,w,h)=>{g.fillStyle='#b9775a';g.fillRect(0,0,w,h);g.strokeStyle='#8a5440';g.lineWidth=3;for(let i=0;i<=w;i+=16){g.strokeRect(i,0,16,h);g.strokeRect(0,i,w,16)}},[16,16]);
const fl=new THREE.Mesh(new THREE.PlaneGeometry(60,60),new THREE.MeshStandardMaterial({map:tiles,roughness:.95}));fl.rotation.x=-Math.PI/2;fl.receiveShadow=true;T.add(fl);
const wall=box(40,14,.6,0xe8dcc0,.05);wall.position.set(0,7,-6);T.add(wall);
const door=box(3.2,6,.3,0x5a3a26,.05);door.position.set(-6.5,3,-5.6);T.add(door);
const win=box(4,3.2,.3,0x2a3a68,.04,{emissive:0xffb050,emissiveIntensity:.5});win.position.set(6.5,6,-5.6);T.add(win);
[[-11,1],[11,1]].forEach(([x])=>{const p=box(2.2,2,2.2,0xc0603a,.1);p.position.set(x,1,-4);T.add(p);const pl=box(2.6,3,2.6,0x2f8a46,.3);pl.position.set(x,3.4,-4);T.add(pl)});
// farolillo y guirnalda
const post=box(.3,7,.3,0x2a2a30,.03);post.position.set(4.5,3.5,-3.5);T.add(post);const lamp=box(.9,1.1,.9,0xffd890,.2,{emissive:0xffb050,emissiveIntensity:1.2});lamp.position.set(4.5,7.3,-3.5);T.add(lamp);const lg=glow(0xffc070,6,.6);lg.position.set(4.5,7.3,-3.3);T.add(lg);
for(let i=0;i<9;i++){const x=-8+i*2,y=10.3-Math.sin(i/8*Math.PI)*1.2;const b=box(.3,.4,.3,[0xffd060,0xff7a50,0x8ae070][i%3],.1,{emissive:[0xffb030,0xff5030,0x50c050][i%3],emissiveIntensity:1.1});b.position.set(x,y,-5.4);T.add(b)}
const hero=capataz();hero.g.position.set(-2.3,0,0);T.add(hero.g);
const nana=abuela();nana.g.position.set(2.3,0,0);T.add(nana.g);
// picaduras: bultos rojos que aparecen en brazos y cara de la capataz
const bites=[];[[hero.armL,0,-1.0,.26],[hero.armR,0,-.7,.26],[hero.armL,0,-.45,.26],[hero.head,-.45,-.3,.66],[hero.armR,0,-1.15,.26],[hero.head,.5,.25,.66]].forEach(([par,x,y,z])=>{const b=box(.2,.2,.1,0xe0303a,.05,{emissive:0x801010,emissiveIntensity:.5});b.position.set(x,y,z);b.scale.setScalar(.001);par.add(b);bites.push(b)});
// enjambre
const NM=14,MS=[];for(let i=0;i<NM;i++){const m=mosquito(.42);scene.add(m.g);MS.push(m)}
const flyTo=(m,pos,t,i)=>{const nx=swarmPos(i,t+.04,{x:0,y:0,z:0});m.g.position.copy(pos);m.g.lookAt(pos.clone().add(V3(Math.cos(t*1.3+i),Math.sin(t*.7+i)*.3,Math.sin(t*1.3+i))));m.buzz(t+i)};
// ---------- s1: GOTA DE SANGRE con terrones (x=300)
const G1=new THREE.Group();G1.position.set(300,0,0);scene.add(G1);
const dropM=new THREE.MeshStandardMaterial({color:0xb0101c,roughness:.25,metalness:.1,emissive:0x300004});
const drop=new THREE.Group();const ds=new THREE.Mesh(new THREE.SphereGeometry(2,40,30),dropM);const dc=new THREE.Mesh(new THREE.ConeGeometry(1.72,2.6,40,1,true),dropM);dc.position.y=2.2;drop.add(ds,dc);drop.position.y=-.6;G1.add(drop);
const shine=glow(0xffffff,1.3,.6);shine.position.set(-.7,.4,1.9);drop.add(shine);
const cubes=[];for(let i=0;i<6;i++){const c=box(.9,.9,.9,0xfbfbf6,.08);G1.add(c);cubes.push(c)}
const xA=box(6.4,.5,.5,0xff2d3f,.1,{emissive:0xff1020,emissiveIntensity:.8});const xB=xA.clone();xA.rotation.z=.8;xB.rotation.z=-.8;xA.position.set(0,-.4,3);xB.position.set(0,-.4,3);G1.add(xA,xB);
const l1=label3d(['¿SANGRE DULCE?'],{w:7,h:1.5,px:120,accent:'#ff4a5a'});l1.position.set(0,-3.3,1);G1.add(l1);
const l1b=label3d(['*SIN PRUEBAS SERIAS'],{w:7,h:1.4,px:110,accent:'#ff2d3f'});l1b.position.set(0,-4.75,1);G1.add(l1b);
// ---------- s2: OLFATÓMETRO en Y (x=600)
const G2=new THREE.Group();G2.position.set(600,0,0);scene.add(G2);
const lab=new THREE.Mesh(new THREE.PlaneGeometry(80,60),new THREE.MeshStandardMaterial({color:0x1d2a44,roughness:1}));lab.position.z=-4;G2.add(lab);
const glassM=new THREE.MeshStandardMaterial({color:0xbfe8ff,transparent:true,opacity:.22,roughness:.05,depthWrite:false});
const edgeM=new THREE.LineBasicMaterial({color:0x9fd8ff,transparent:true,opacity:.8});
const ch=new THREE.Mesh(new THREE.BoxGeometry(3.4,2.4,2.4),glassM);ch.position.set(0,-1.9,0);G2.add(ch);const che=new THREE.LineSegments(new THREE.EdgesGeometry(ch.geometry),edgeM);che.position.copy(ch.position);G2.add(che);
const BX=[];[-1,1].forEach(sd=>{const tb=new THREE.Mesh(new THREE.CylinderGeometry(.55,.55,6.2,24,1,true),glassM);tb.position.set(sd*2.3,-5.3,0);tb.rotation.z=sd*.62;G2.add(tb);
 const bx=box(3,2.6,2.6,0xe8e8f0,.12);bx.position.set(sd*4.4,-8.6,0);G2.add(bx);
 const sock=new THREE.Group();const s1=box(1,1.8,.5,0xd8b48a,.18);s1.position.y=.3;const s2=box(1.3,.6,.5,0xd8b48a,.18);s2.position.set(sd*.2,-.7,0);sock.add(s1,s2);sock.position.set(sd*4.4,-8.3,1.35);sock.rotation.z=sd*.1;G2.add(sock);
 const lb=label3d([sd<0?'MEDIA A':'MEDIA B'],{w:3,h:.9,px:110,accent:'#ffc23a'});lb.position.set(sd*4.4,-10.5,1.4);G2.add(lb);BX.push({bx,lb})});
const l2=label3d(['*8 PERSONAS · 3 AÑOS','ROCKEFELLER · CELL · 2022'],{w:9,h:2.2,px:100});l2.position.set(0,-13.3,1);G2.add(l2);
// ---------- s3: BARRAS HORIZONTALES (x=900)
const G3=new THREE.Group();G3.position.set(900,0,0);scene.add(G3);
const back3=new THREE.Mesh(new THREE.PlaneGeometry(80,60),new THREE.MeshStandardMaterial({color:0x141a30,roughness:1}));back3.position.z=-3;G3.add(back3);
const BARS=[{v:100,y:-1.4,col:0xff3a4a,lab:'Nº 33',big:true},{v:25,y:-4.4,col:0xffc23a,lab:'LA SEGUNDA'},{v:1,y:-7.4,col:0x6aa8ff,lab:'Nº 19'}].map(b=>{const m=box(1,1.7,1.4,b.col,.12,{emissive:b.col,emissiveIntensity:.25});m.position.set(-4.6,b.y,0);G3.add(m);
 const nm=label3d([b.lab],{w:3.4,h:.9,px:110,accent:'#ffffff'});nm.position.set(-3.2,b.y+1.45,.8);G3.add(nm);const val=label3d(['×1'],{w:3.6,h:1.5,px:130,bg:''});G3.add(val);return{...b,m,nm,val}});
const l3=label3d(['*×100','QUE LA QUE MENOS'],{w:6,h:2.4,px:120,accent:'#ff3a4a'});l3.position.set(1.5,-10.6,1);G3.add(l3);
// ---------- s4: PIEL DE VÓXELES con penacho de olor (x=1200)
const G4=new THREE.Group();G4.position.set(1200,0,0);scene.add(G4);
const skinN=26*16,SK=new THREE.InstancedMesh(new THREE.BoxGeometry(.6,.6,.6),new THREE.MeshStandardMaterial({roughness:.8}),skinN);const O=new THREE.Object3D();const col=new THREE.Color();let si=0;
for(let i=0;i<26;i++)for(let j=0;j<16;j++){const x=-7.5+i*.6,z=-4.5+j*.6;const h=Math.sin(i*.7)*.12+Math.cos(j*.9+i*.3)*.1+(R()*.08);O.position.set(x,h,z);O.updateMatrix();SK.setMatrixAt(si,O.matrix);col.setHex([0xd9a06a,0xd29760,0xe0aa76,0xcb905a][(i*7+j*3)%4]);SK.setColorAt(si,col);si++}
SK.receiveShadow=true;G4.add(SK);
const PORES=[];for(let k=0;k<7;k++){const x=-6+R()*12,z=-3.4+R()*5;const p=box(.36,.1,.36,0x7a4a2a,.02);p.position.set(x,.32,z);G4.add(p);PORES.push(V3(x,.4,z))}
const mol=puffs(scene,140,.26,0xffa030,{opacity:.95,depthWrite:false});const mp=[];for(let i=0;i<140;i++)mp.push([i%7,R(),R()*6.28,R()]);
const l4=label3d(['*ÁCIDOS DE LA PIEL','EN LA GRASA NATURAL (SEBO)'],{w:5.4,h:1.4,px:100,accent:'#ffa030'});l4.position.set(0,1.3,1.2);l4.rotation.x=-.6;G4.add(l4);
const l4b=label3d(['AÑO 1 → AÑO 3:','*SIGUE SIENDO IMÁN'],{w:5.4,h:1.4,px:100,accent:'#ff3a4a'});l4b.position.set(0,1.3,1.2);l4b.rotation.x=-.6;G4.add(l4b);
// ---------- render
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],k=ss(0,d,lt),m=mouthAt(t);let p,q;
 const onT=s==='h'||s==='cta';T.visible=onT;G1.visible=s==='s1';G2.visible=s==='s2';G3.visible=s==='s3';G4.visible=s==='s4';mol.m.visible=s==='s4';ST.visible=onT;
 MS.forEach(o=>o.g.visible=false);
 if(onT){const scr=s==='h'?ss(.3,d,lt):1;
  hero.pose(t,s==='cta'?m:0,{wave:s==='cta'?1:0,look:s==='h'?Math.sin(t*3)*.35:.15});
  if(s==='h'){hero.armL.rotation.z=-.14-1.9*Math.max(0,Math.sin(t*4.2));hero.armL.rotation.x=-.8*Math.max(0,Math.sin(t*4.2))}// se rasca y espanta
  nana.pose(t,s==='cta'?.3+.3*Math.sin(t*9):0,{look:-.45});
  bites.forEach((b,i)=>{const a=s==='cta'?1:ss(.4+i*.45,.7+i*.45,lt);b.scale.setScalar(Math.max(.001,a*(1+.15*Math.sin(t*6+i))))});
  // 13 alrededor de la capataz, 1 que prueba con la abuela y se va
  const HC=V3(-2.3,3.1,.3);MS.forEach((o,i)=>{o.g.visible=true;let pos;
   if(i===NM-1){const u=(t*.25)%1;const A=V3(2.3,3.2,.8),B2=V3(-1.4,3.5,.6);pos=A.clone().lerp(B2,ss(.35,.75,u));pos.y+=Math.sin(t*5)*.25;pos.x+=Math.sin(t*7)*.2}
   else pos=swarmPos(i,t,HC,1.7,1.25,1.2);flyTo(o,pos,t,i)});
  if(s==='h'){p=V3(Math.sin(t*.4)*.6,4.3,24.5-k*1.8);q=V3(-.3,3.2,0)}else{p=V3(0,2.6,30-k*1.2);q=V3(0,.4,0)}
  S.intensity=1.1;hemi.intensity=.9}
 else if(s==='s1'){drop.rotation.y=t*.4;drop.scale.setScalar(1+.03*Math.sin(t*3));
  cubes.forEach((c,i)=>{const a=t*.6+i*1.047;c.position.set(Math.cos(a)*3.4,-.4+Math.sin(t*1.3+i)*.6,Math.sin(a)*2.2+.8);c.rotation.set(t+i,t*.7,0);c.visible=lt<d*.55||((lt*6|0)%2===0&&lt<d*.65)});
  const xk=ss(d*.42,d*.5,lt);xA.scale.set(xk,1,1);xB.scale.set(xk,1,1);xA.visible=xB.visible=xk>0;l1b.visible=lt>d*.45;
  // un mosquito da vueltas a la gota
  const mo=MS[0];mo.g.visible=true;const mp0=V3(300+Math.cos(t*1.4)*3.2,1.6+Math.sin(t*2)*.4,Math.sin(t*1.4)*2.4);flyTo(mo,mp0,t,0);
  p=V3(300+Math.sin(t*.3)*1.5,3,26-k*1.5);q=V3(300,1.6,0);S.intensity=1.6;hemi.intensity=1.1}
 else if(s==='s2'){// los mosquitos salen de la cámara central y casi todos bajan por el tubo de la derecha (media B)
  MS.forEach((o,i)=>{o.g.visible=true;const u=clamp((lt-.8-i*.18)/2.4);const goR=i%5!==0;const sd=goR?1:-1;const c0=V3(600,-1.9,0),c1=V3(600+sd*2.3,-5.3,0),c2=V3(600+sd*4.4,-7.2,.6);
   let pos=u<.5?c0.clone().lerp(c1,u*2):c1.clone().lerp(c2,(u-.5)*2);if(u>=1)pos=swarmPos(i,t,c2,1.1,.6,.6);else pos.add(V3(Math.sin(t*9+i)*.35,Math.sin(t*7+i)*.3,Math.cos(t*8+i)*.3));flyTo(o,pos,t,i)});
  BX[1].bx.material.emissive=new THREE.Color(0xff3a4a);BX[1].bx.material.emissiveIntensity=.35*ss(d*.55,d*.8,lt);
  p=V3(600+Math.sin(t*.3)*1,-2,36-k*1.5);q=V3(600,-3.3,0);S.intensity=1.4;hemi.intensity=1.2}
 else if(s==='s3'){BARS.forEach((b,i)=>{const g=ss(.4+i*.25,d*.55,lt);const L=Math.max(.06,8.4*b.v/100*g);b.m.scale.x=L;b.m.position.x=-4.6+L/2;
   b.val.set([`*×${Math.max(1,Math.round(b.v*g))}`]);b.val.position.set(-4.6+L+1.5,b.y,.9);if(b.big)b.val.position.set(-4.6+L-1.4,b.y,.9);b.val.visible=g>.05});
  l3.visible=lt>d*.6;
  const end=V3(900-4.6+8.4*ss(.4,d*.55,lt),-1.4,.6);MS.forEach((o,i)=>{if(i>9)return;o.g.visible=true;flyTo(o,swarmPos(i,t,end,1.1,.9,.8),t,i)});
  p=V3(900+Math.sin(t*.3)*.8,-3.6,33-k*1.5);q=V3(900,-1.8,0);S.intensity=1.5;hemi.intensity=1.1}
 else{// s4: piel, penacho de olor y mosquitos que siguen el rastro
  for(let i=0;i<140;i++){const[pi,o,a,w]=mp[i];const ph=(lt*.32+o)%1;const P0=PORES[pi];mol.set(i,1200+P0.x+Math.sin(a+t*.8+ph*4)*ph*1.8,P0.y+ph*9,P0.z+Math.cos(a+ph*3)*ph*1.2,(1-ph*.7)*(.7+w*.6),t+i)}mol.done();
  MS.forEach((o,i)=>{if(i>7)return;o.g.visible=true;const P0=PORES[i%7];const u=((lt*.18+i*.13)%1);const pos=V3(1200+P0.x+Math.sin(t*2+i)*.6,P0.y+8-7*u,P0.z+Math.cos(t*2+i)*.5);flyTo(o,pos,t,i)});
  l4.visible=lt<d*.55;l4b.visible=!l4.visible;
  p=V3(1200+Math.sin(t*.25)*1.5,9.5-k*.6,15.5-k*.8);q=V3(1200,1.2,-1.4);S.intensity=1.8;hemi.intensity=1.3}
 cam.position.copy(p);cam.lookAt(q);r.render(scene,cam)};
window.ready=true;
