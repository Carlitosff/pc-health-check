// Mito: '¿salir con el pelo mojado te resfría?' (2303). Johnson y Eccles, Family Practice 2005 (pies en agua helada: 29 % frente a 9 %).
// Reutilizable: CALLE DE INVIERNO de noche (portal con luz, farola, nieve, vaho), PELO MOJADO que gotea (wetHair), VIRUS de vóxeles con espículas (virus()),
// LABORATORIO con barreños de agua helada / vacíos, reloj de 20 min y GRÁFICA DE BARRAS 3D que crece (bars), y la NARIZ por dentro: vasos que se estrechan,
// glóbulos blancos que dejan de llegar y virus que se multiplican.
import {THREE,J,mk,ss,V3,clamp,stage,sun,box,glow,pixTex,capataz,abuela,segAt,mouthAt,puffs,label3d,snow} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x0b1230,fog:[0x0b1230,40,130],exposure:1.2});cam.far=3000;cam.updateProjectionMatrix();const R=mk(2303);
const hemi=new THREE.HemisphereLight(0x8fa6e8,0x2a2a38,.8);scene.add(hemi);const S=sun(scene,{pos:[-12,22,14],span:26,color:0xb8c8ff,power:.9});
// ---------- calle de invierno
const ST=new THREE.Group();scene.add(ST);
const road=new THREE.Mesh(new THREE.PlaneGeometry(200,200),new THREE.MeshStandardMaterial({color:0x2a2e3a,roughness:.85}));road.rotation.x=-Math.PI/2;road.receiveShadow=true;ST.add(road);
const walk=box(60,.25,8,0xbfc4cc,.03);walk.position.set(0,.12,-1);ST.add(walk);
for(let i=0;i<14;i++){const sn=box(1.2+R()*2,.2,1+R(),0xf4f8ff,.1);sn.position.set(-18+R()*36,.3,-4.4+R()*.8);ST.add(sn)}
const facade=box(40,14,1,0x8a4a3a,.05);facade.position.set(0,7,-6);ST.add(facade);
for(let x=-16;x<=16;x+=4)for(let y of [5.5,10]){if(Math.abs(x)<3&&y<7)continue;const w=box(1.6,2,.2,R()<.5?0xffd890:0x1a2240,.02,R()<.5?{emissive:0xffb050,emissiveIntensity:.7}:{});w.position.set(x,y,-5.45);ST.add(w)}
const door=box(3,5,.3,0xffd9a0,.02,{emissive:0xffb060,emissiveIntensity:1.1});door.position.set(0,2.6,-5.4);ST.add(door);const dl=new THREE.PointLight(0xffb870,30,18,1.6);dl.position.set(0,3.5,-3.5);ST.add(dl);
const lamp=new THREE.Group();{const p=box(.3,7,.3,0x23262e,.03);p.position.y=3.5;lamp.add(p);const h=box(1.2,.5,1.2,0x23262e,.05);h.position.y=7.1;lamp.add(h);const b=box(.8,.3,.8,0xfff0c0,.05,{emissive:0xffe0a0,emissiveIntensity:2});b.position.y=6.8;lamp.add(b);const g=glow(0xffe0a0,6,.6);g.position.y=6.6;lamp.add(g);const L=new THREE.PointLight(0xffe0a0,40,20,1.5);L.position.y=6.4;lamp.add(L)}lamp.position.set(6.5,0,0);ST.add(lamp);
const SN=snow(scene,700,[-20,20,20,-6,16],{size:.2,speed:1.6});
const hero=capataz();hero.hat.forEach(h=>h.visible=false);hero.g.position.set(1.3,.25,1.5);ST.add(hero.g);
const hair=box(1.6,.5,1.42,0x2a1a10,.14,{roughness:.15,metalness:.2});hair.position.y=.72;hero.head.add(hair);const fringe=box(1.56,.24,.3,0x2a1a10,.06,{roughness:.15});fringe.position.set(0,.5,.58);hero.head.add(fringe);
const scarf=box(1.7,.42,1.14,0xd8343a,.12);scarf.position.y=2.45;hero.g.add(scarf);scarf.visible=false;const towel=box(1.8,.7,1.6,0xf4f0e8,.25);towel.position.y=.95;hero.head.add(towel);towel.visible=false;
const gran=abuela();gran.g.position.set(-2.2,.25,-.2);gran.g.rotation.y=.45;ST.add(gran.g);
const bubble=label3d(['¡QUE TE VAS','*A RESFRIAR!'],{w:6.4,h:2.4,px:130,sprite:true,bg:'#ffffff',fg:'#10131f',accent:'#ff4a4a'});scene.add(bubble);
const drops=puffs(scene,30,.16,0x8ad8ff,{opacity:.9});const breath=puffs(scene,24,.35,0xe8f0ff,{opacity:.5,depthWrite:false});
// ---------- virus de vóxeles (x=600)
function virus(rad=3,{seed=3,col=0x6ad04a,tip=0xff4a6a,vs=.32}={}){const g=new THREE.Group();const P=[];for(let x=-rad;x<=rad;x+=vs)for(let y=-rad;y<=rad;y+=vs)for(let z=-rad;z<=rad;z+=vs){const d=Math.hypot(x,y,z);if(d<rad&&d>rad-vs*1.6)P.push([x,y,z])}
 const im=new THREE.InstancedMesh(new THREE.BoxGeometry(vs*.95,vs*.95,vs*.95),new THREE.MeshStandardMaterial({roughness:.5}),P.length);const O=new THREE.Object3D(),C=new THREE.Color(),q=mk(seed);P.forEach(([x,y,z],i)=>{O.position.set(x,y,z);O.updateMatrix();im.setMatrixAt(i,O.matrix);im.setColorAt(i,C.setHex(col).multiplyScalar(.8+q()*.35))});g.add(im);
 const n=26;for(let i=0;i<n;i++){const yy=1-2*(i+.5)/n,rr=Math.sqrt(1-yy*yy),a=i*2.39996;const d=V3(Math.cos(a)*rr,yy,Math.sin(a)*rr);const st=box(.22,rad*.42,.22,0x9ad870,.03);st.position.copy(d.clone().multiplyScalar(rad+rad*.18));st.quaternion.setFromUnitVectors(V3(0,1,0),d);g.add(st);const tp=box(.55,.3,.55,tip,.06,{emissive:tip,emissiveIntensity:.5});tp.position.copy(d.clone().multiplyScalar(rad*1.42));tp.quaternion.copy(st.quaternion);g.add(tp)}return g}
const VX=new THREE.Group();VX.position.set(600,0,0);scene.add(VX);const VL=new THREE.PointLight(0xffffff,30,60,1.2);VL.position.set(6,8,14);VX.add(VL);
const big=virus(3.4);VX.add(big);const vLab=label3d(['*VIRUS'],{w:5,h:1.6,px:140,sprite:true,accent:'#6ad04a'});vLab.position.set(0,-6.4,2);VX.add(vLab);
const flake=new THREE.Group();for(let i=0;i<6;i++){const a=box(.25,3.2,.25,0xcfeaff,.03,{emissive:0x5aa0ff,emissiveIntensity:.4});a.position.set(Math.sin(i*1.047)*1.6,Math.cos(i*1.047)*1.6,0);a.rotation.z=-i*1.047;flake.add(a)}flake.position.set(-3.6,6.6,0);VX.add(flake);
const fLab=label3d(['SOLO FRÍO','*= 0'],{w:4.2,h:2,px:110,sprite:true,accent:'#4de3ff'});fLab.position.set(-3.6,3.6,1);VX.add(fLab);
// ---------- laboratorio (x=300): barreños, reloj de 20 min y barras
const LAB=new THREE.Group();LAB.position.set(300,0,0);scene.add(LAB);
const lf=new THREE.Mesh(new THREE.PlaneGeometry(80,60),new THREE.MeshStandardMaterial({map:pixTex(64,64,(g,w,h)=>{g.fillStyle='#e8ecf2';g.fillRect(0,0,w,h);g.strokeStyle='#c4cad4';g.lineWidth=2;for(let i=0;i<=w;i+=16){g.strokeRect(i,0,16,h);g.strokeRect(0,i,w,16)}},[20,15]),roughness:.8}));lf.rotation.x=-Math.PI/2;lf.receiveShadow=true;LAB.add(lf);
const lw=box(80,16,.5,0xdfe8f0,.02);lw.position.set(0,8,-8);LAB.add(lw);const LL=new THREE.PointLight(0xffffff,60,60,1.2);LL.position.set(0,12,6);LAB.add(LL);
const tub=(cold)=>{const g=new THREE.Group();const b=box(2.6,1,2,0x2a7ad8,.15);b.position.y=.5;g.add(b);const w=box(2.3,.1,1.7,cold?0x8ad8ff:0x2a7ad8,.02,cold?{emissive:0x3a8ad8,emissiveIntensity:.5,transparent:true,opacity:.85}:{});w.position.y=.95;g.add(w);if(cold)for(let i=0;i<5;i++){const ic=box(.45,.45,.45,0xf2fbff,.08,{transparent:true,opacity:.9});ic.position.set(-.8+i*.4,1.05,(i%2-.5)*.6);ic.rotation.set(i,i*.7,0);g.add(ic)}return g};
const pC=capataz();pC.hat.forEach(h=>h.visible=false);const pA=abuela();const tC=tub(true),tA=tub(false);
tC.position.set(-2.8,0,0);tA.position.set(2.8,0,0);LAB.add(tC,tA);pC.g.position.set(-2.8,.35,0);pA.g.position.set(2.8,.35,0);LAB.add(pC.g,pA.g);
const lC=label3d(['AGUA HELADA'],{w:4.4,h:1,px:110,bg:'#0d2a3a',accent:'#4de3ff'});lC.position.set(-2.8,.9,1.4);lC.rotation.x=-.3;LAB.add(lC);const lA2=label3d(['VACÍO'],{w:3,h:1,px:110});lA2.position.set(2.8,.9,1.4);lA2.rotation.x=-.3;LAB.add(lA2);
const clk=label3d(['20:00'],{w:4,h:1.6,px:150,bg:'#0b0d14',fg:'#ff4a4a',accent:'#2a2f40'});clk.position.set(0,8.4,-7.6);LAB.add(clk);
const bars=[[10,29,0x4de3ff],[15,9,0x9aa0aa]].map(([x,v,c])=>{const b=box(2.4,1,2,c,.1,{emissive:c,emissiveIntensity:.25});b.position.set(x,0,0);LAB.add(b);const l=label3d([`*${v} %`],{w:3.6,h:1.5,px:150,sprite:true,accent:c===0x4de3ff?'#4de3ff':'#ffffff'});LAB.add(l);return{b,l,v}});
const bl1=label3d(['AGUA HELADA'],{w:4.4,h:1,px:110,bg:'#0d2a3a',accent:'#4de3ff'});bl1.position.set(10,.6,1.6);bl1.rotation.x=-.3;LAB.add(bl1);const bl2=label3d(['SIN AGUA'],{w:3.6,h:1,px:110});bl2.position.set(15,.6,1.6);bl2.rotation.x=-.3;LAB.add(bl2);
const shiv=puffs(scene,20,.3,0xe8f0ff,{opacity:.5,depthWrite:false});
// ---------- nariz por dentro (x=900): vasos que se estrechan, glóbulos blancos y virus
const NO=new THREE.Group();NO.position.set(900,0,0);scene.add(NO);const NL=new THREE.PointLight(0xffb0a0,50,80,1.1);NL.position.set(0,6,16);NO.add(NL);
const wall=new THREE.Mesh(new THREE.PlaneGeometry(80,60),new THREE.MeshStandardMaterial({color:0xd8737a,roughness:.6,map:pixTex(64,64,(g,w,h)=>{const q=mk(4);g.fillStyle='#d8737a';g.fillRect(0,0,w,h);for(let i=0;i<300;i++){g.fillStyle=['#c8636a','#e4868c','#bf5a62'][Math.floor(q()*3)];g.fillRect(Math.floor(q()*w/4)*4,Math.floor(q()*h/4)*4,4,4)}},[8,6])}));wall.position.z=-4;NO.add(wall);
const VES=[];[-5,0,5].forEach((y,i)=>{const m=new THREE.Mesh(new THREE.CylinderGeometry(1,1,40,20,1,true),new THREE.MeshStandardMaterial({color:0xb81e2a,roughness:.4,transparent:true,opacity:.75,side:THREE.DoubleSide,emissive:0x5a0a10,emissiveIntensity:.4}));m.rotation.z=Math.PI/2;m.position.set(0,y,-1);NO.add(m);VES.push(m)});
const wbc=puffs(scene,45,.7,0xffffff,{opacity:.95});const vir=[];for(let i=0;i<12;i++){const v=virus(.9,{seed:i,vs:.3});v.scale.setScalar(0);NO.add(v);vir.push([v,(R()-.5)*16,(R()-.5)*12+1,1.5+R()*2,R()])}
const nLab=label3d(['VASOS DE LA NARIZ'],{w:8,h:1.4,px:110,sprite:true});nLab.position.set(0,-5.2,4);NO.add(nLab);const nLab2=label3d(['*SE CIERRAN'],{w:6,h:1.5,px:130,sprite:true,accent:'#ff4a4a'});nLab2.position.set(0,-7.2,4);NO.add(nLab2);
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],k=ss(0,d,lt),m=mouthAt(t);let p,q;
 const onS=s==='h'||s==='cta';ST.visible=onS;SN.pts.visible=onS;LAB.visible=s==='s2'||s==='s3';VX.visible=s==='s1';NO.visible=s==='s4';bubble.visible=false;
 drops.m.visible=breath.m.visible=onS;shiv.m.visible=LAB.visible;
 scene.background.setHex(onS?0x0b1230:s==='s4'?0x3a0a14:s==='s1'?0x081a12:0x1a2230);scene.fog.near=onS?40:1e4;scene.fog.far=onS?130:2e4;S.intensity=onS?.9:0;
 if(onS){SN.draw(t);
  hero.pose(t,s==='cta'?m:0,{look:s==='h'?-.5:0,wave:s==='cta'&&lt>d*.4?1:0});hero.g.position.x=1.3+Math.sin(t*25)*.02;// tirita
  gran.pose(t,s==='h'?m*.7:0,{point:s==='h'?1:0,look:.3});towel.visible=scarf.visible=s==='cta';hair.visible=fringe.visible=s!=='cta';
  for(let i=0;i<30;i++){const ph=(t*.9+i/30)%1;const a=i*2.4;drops.set(i,1.3+Math.cos(a)*.7,4.2-ph*4,1.5+Math.sin(a)*.6,s==='h'&&ph<.95?1:0)}drops.done();
  for(let i=0;i<24;i++){const ph=(t*.5+i/24)%1;breath.set(i,1.3+.2+ph*.8,3.1+ph*.9+Math.sin(i)*.1,2.3+ph*1.2,(ph<.5?ph*2:1)*(1-ph)*1.6*(Math.sin(t*1.2)>-.2?1:0))}breath.done();
  if(s==='h'){bubble.visible=true;bubble.position.set(-3.6,7.6,0);const pu=.94+.06*Math.sin(t*6);bubble.scale.set(5.6*pu,2.1*pu,1);p=V3(-1.4-k*.4,4.4,29-k*2);q=V3(-1.4,5.8,0)}
  else{p=V3(-.45,2.2,32+k);q=V3(-.45,2.1,0)}/* v26: en el CTA los dos quedan ENCIMA del botón de seguir (y<1120) */}
 else if(s==='s1'){big.rotation.set(t*.3,t*.45,0);big.scale.setScalar(.6+.4*ss(0,1,lt));flake.rotation.z=t*.4;fLab.visible=flake.visible=lt>d*.35;
  p=V3(599.5+Math.sin(t*.3)*1.5,-3,34-k*3);q=V3(599.5,-.5,0)}
 else if(s==='s2'||s==='s3'){
  pC.pose(t,0,{look:.2});pA.pose(t,0,{look:-.2});pC.g.position.x=-2.8+Math.sin(t*28)*.03;// el del agua helada tirita
  for(let i=0;i<20;i++){const ph=(t*.6+i/20)%1;shiv.set(i,300-2.8+(i%5-2)*.4,1.1+ph*1.6,(i%3-1)*.5,(1-ph)*.9)}shiv.done();
  const mins=s==='s2'?Math.max(0,20-Math.floor(ss(.4,d*.9,lt)*20)):0;clk.set([`${String(mins).padStart(2,'0')}:00`]);
  bars.forEach((b,i)=>{const g=s==='s3'?ss(.3+i*.25,d*.55+i*.25,lt):0;const hgt=Math.max(.01,b.v/29*7*g);b.b.scale.y=hgt;b.b.position.y=hgt/2;b.b.visible=s==='s3';b.l.visible=s==='s3'&&g>.15;b.l.position.set(i?15:10,hgt+1.4,0);b.l.set([`*${Math.round(b.v*g)} %`])});
  if(s==='s2'){p=V3(300+Math.sin(t*.3),5.5,29-k*2);q=V3(300,4.2,-1)}else{const u=ss(0,1.2,lt);p=V3(300+12.5*u,6.5,29+k);q=V3(300+12.5*u,5.2,0)}}
 else{// s4: los vasos se estrechan, menos glóbulos blancos, más virus
  const c=ss(.4,d*.55,lt);VES.forEach((v,i)=>{const sc=1-.68*c;v.scale.set(sc,1,sc)});nLab2.visible=c>.3;
  for(let i=0;i<45;i++){const lane=i%3,ph=((t*.35+i/45*3)%1);const keep=(i/45)<1-.8*c;wbc.set(i,900-18+ph*36,[-5,0,5][lane],-1,keep?(1-.6*c)*.9:0)}wbc.done();
  vir.forEach(([v,x,y,z,o],i)=>{const g=ss(d*.35+o*d*.4,d*.35+o*d*.4+.4,lt);v.scale.setScalar(g);v.position.set(x,y+Math.sin(t+i)*.3,z);v.rotation.set(t*.6+i,t*.4,0)});
  p=V3(900+Math.sin(t*.25)*2,-1,30-k*4);q=V3(900,-2,0)}
 cam.position.copy(p);cam.lookAt(q);r.render(scene,cam)};
window.ready=true;
