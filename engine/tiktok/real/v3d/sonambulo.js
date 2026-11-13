// Mito: 'nunca despiertes a un sonámbulo, le da un infarto' (2103). UAMS Health 08/03/2019 (Raghu Reddy), BrainFacts 11/10/2019, Sleep Foundation 2025.
// Reutilizable: CASA DE NOCHE (dormitorio con ventana y luna + pasillo con cuadros y lámpara + escalera que baja con barandilla y aviso rojo),
// pose de SONÁMBULO (sleepwalk: brazos al frente, ojos cerrados, paso lento), DESPERTAR CONFUSO (ojos que se abren, '?' que giran, respingo),
// la abuela acompaña de la mano de vuelta a la cama; capataz dormida en la cama (lieDown) para el CTA.
import {THREE,J,mk,ss,V3,clamp,stage,sun,box,glow,capataz,abuela,segAt,mouthAt,label3d,bed,lieDown} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x0b1028,fog:[0x0b1028,30,90],exposure:1.2});const R=mk(2103);
scene.add(new THREE.HemisphereLight(0x8fa4e0,0x2a2030,.85));sun(scene,{pos:[-14,24,-6],span:30,color:0xb8c8ff,power:.9});
const lamp=new THREE.PointLight(0xffc880,60,26,1.6);lamp.position.set(-2.5,7.6,-3);scene.add(lamp);
// ---------- suelo, paredes
const fl=new THREE.Mesh(new THREE.PlaneGeometry(9,32),new THREE.MeshStandardMaterial({color:0x6a4a34,roughness:.9}));fl.rotation.x=-Math.PI/2;fl.position.set(0,0,-6);fl.receiveShadow=true;scene.add(fl);
for(let i=0;i<4;i++){const p=box(2.1,.05,32,i%2?0x6e4c36:0x5e4232,.01);p.position.set(-3.4+i*2.25,.02,-6);scene.add(p)}
const rug=box(3,.06,9,0x8a2a3a,.02);rug.position.set(0,.06,-3);scene.add(rug);
const wallL=box(.6,10,32,0x2e3866,.05);wallL.position.set(-4.8,5,-6);scene.add(wallL);
const back=box(20,10,.6,0x283058,.05);back.position.set(0,5,-22.3);scene.add(back);
// pared con puerta entre dormitorio y pasillo (z=-10)
const dw1=box(4,10,.5,0x2e3866,.05);dw1.position.set(-2.8,5,-10);scene.add(dw1);const dw2=box(4,10,.5,0x2e3866,.05);dw2.position.set(3.6,5,-10);scene.add(dw2);const dw3=box(2.4,3.2,.5,0x2e3866,.05);dw3.position.set(.4,8.4,-10);scene.add(dw3);
const frame=box(2.8,7,.6,0x8a6a4a,.05);frame.position.set(.4,3.4,-10);frame.material.transparent=true;frame.material.opacity=0;scene.add(frame);
// cuadros y lámpara de pared
[[-6,0xd86a3a],[-1,0x3ab08a],[3,0xd8b03a]].forEach(([z,c])=>{const f=box(.2,2.2,2.8,0x8a6a4a,.04);f.position.set(-4.45,6,z);scene.add(f);const a=box(.1,1.7,2.3,c,.02,{emissive:c,emissiveIntensity:.15});a.position.set(-4.33,6,z);scene.add(a)});
const wl=box(.5,.9,.9,0xffd890,.2,{emissive:0xffb050,emissiveIntensity:1});wl.position.set(-4.3,7.6,-3);scene.add(wl);const wlg=glow(0xffc070,5,.45);wlg.position.set(-3.9,7.6,-3);scene.add(wlg);
// ---------- escalera (baja desde z=6 hacia +z)
const STEP=[];for(let i=0;i<9;i++){const s=box(9,.6,1,0x7a5638,.03);s.position.set(0,-.3-i*.62,6.5+i*.95);scene.add(s);STEP.push(s)}
const stairFl=box(9,.6,10,0x3a2a22,.03);stairFl.position.set(0,-5.9,19);scene.add(stairFl);
const rail=new THREE.Group();for(let i=0;i<9;i++){const p=box(.22,2.4,.22,0xe8e0d0,.03);p.position.set(4.2,-.3-i*.62+1.2,6.5+i*.95);rail.add(p)}{const top=box(.3,.3,9.6,0xc8a070,.05);top.position.set(4.2,-1.4,10.3);top.rotation.x=Math.atan2(.62,.95);rail.add(top)}scene.add(rail);
const edge=box(9,.08,.25,0xff3a3a,.01,{emissive:0xff2020,emissiveIntensity:1.4});edge.position.set(0,.04,6.1);scene.add(edge);const edgeG=glow(0xff3030,12,.0);edgeG.position.set(0,.6,6.2);scene.add(edgeG);
const warn=label3d(['*¡ESCALERA!'],{w:5.4,h:1.6,px:150,accent:'#ff4a4a',fg:'#ffffff'});warn.position.set(-4.4,4.4,6.2);warn.rotation.y=Math.PI/2;scene.add(warn);
// ---------- dormitorio
const win=new THREE.Group();{const f=box(6,5,.4,0x8a6a4a,.08);win.add(f);const gl=box(5.2,4.2,.3,0x0a1030,.02,{emissive:0x101848,emissiveIntensity:.6});gl.position.z=.12;win.add(gl);const moon=new THREE.Mesh(new THREE.SphereGeometry(.8,20,14),new THREE.MeshBasicMaterial({color:0xfff4c8,toneMapped:false}));moon.position.set(1.2,1.1,.3);win.add(moon);for(let i=0;i<10;i++){const s=box(.1,.1,.05,0xffffff,.01,{emissive:0xffffff,emissiveIntensity:1});s.position.set((R()-.5)*4.6,(R()-.5)*3.6,.3);win.add(s)}}
win.position.set(-4,6.5,-22);scene.add(win);
const B=bed(0x3a6fd8);B.position.set(1.2,0,-17.5);scene.add(B);
const sleeper=capataz();sleeper.hat.forEach(h=>h.visible=false);const L=lieDown(sleeper,B,0x3a6fd8);
const nt=box(2,2.2,2,0x7a4e2e,.08);nt.position.set(4.6,1.1,-20);scene.add(nt);const nl=box(.8,1.1,.8,0xffd890,.2,{emissive:0xffb050,emissiveIntensity:.9});nl.position.set(4.6,2.75,-20.3);scene.add(nl);const nlg=glow(0xffc070,5,.5);nlg.position.set(4.6,3,-20);scene.add(nlg);
const clock=label3d(['03:47'],{w:2.2,h:.9,px:170,bg:'#0b0d14',fg:'#ff4a4a',accent:'#2a2f40'});clock.position.set(4.6,2.6,-19);scene.add(clock);
// ---------- personajes
const hero=capataz();hero.hat.forEach(h=>h.visible=false);scene.add(hero.g);
const gran=abuela();scene.add(gran.g);
const Q=[0,1,2].map(i=>{const q=label3d(['*?'],{w:2,h:2,px:200,sprite:true,bg:''});scene.add(q);return q});
const ZZ=[0,1,2].map(i=>{const z=label3d(['*Z'],{w:1.1,h:1.1,px:140,sprite:true,bg:''});scene.add(z);return z});
const ask=label3d(['¿LA DESPIERTO?'],{w:4.6,h:1.1,px:110,sprite:true});scene.add(ask);
// rótulo integrado en la pared (s1)
const panel=label3d(['¿LE DA UN INFARTO?','*NO'],{w:5.4,h:2.4,px:120});panel.position.set(-3.95,7.0,-1.9);panel.rotation.y=Math.PI/2;scene.add(panel);
const who=label3d(['DR. RAGHU REDDY · ARKANSAS'],{w:7,h:.9,px:80,accent:'#ffc23a'});who.position.set(-3.95,5.3,-1.9);who.rotation.y=Math.PI/2;scene.add(who);
const heart=new THREE.Group();{const C=0xe8304a;[[0,0],[-1,1],[1,1],[-1,0],[1,0],[0,-1],[-2,1],[2,1],[-2,2],[-1,2],[1,2],[2,2],[0,1]].forEach(([x,y])=>{const b=box(.55,.55,.55,C,.06,{emissive:0x801020,emissiveIntensity:.5});b.position.set(0,y*.56,x*.56);heart.add(b)})}
heart.position.set(-4.0,7.0,-5.6);heart.scale.setScalar(.7);scene.add(heart);
const xMark=new THREE.Group();[1,-1].forEach(sg=>{const b=box(.25,3.4,.35,0x4ade80,.05,{emissive:0x22aa55,emissiveIntensity:1});b.rotation.x=sg*.78;xMark.add(b)});xMark.position.set(-3.6,7.0,-5.6);scene.add(xMark);
const hand=box(.5,.5,.5,0xe3b48c,.1);scene.add(hand);
const sleepwalk=(o,t,ph)=>{o.pose(t,0,{walk:ph});o.armL.rotation.set(-1.45+Math.sin(t*1.3)*.05,0,-.08);o.armR.rotation.set(-1.45+Math.sin(t*1.1+1)*.05,0,.08);o.eyes.forEach(e=>e.scale.y=.1);o.head.rotation.x=.12;o.g.position.y=Math.abs(Math.sin(ph))*.06};
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],k=ss(0,d,lt),m=mouthAt(t);
 const br=Math.sin(t*1.6);L.blanket.scale.y=1+.1*br;sleeper.pose(t,0,{});sleeper.eyes.forEach(e=>e.scale.y=.1);
 Q.forEach(q=>q.visible=false);ZZ.forEach(z=>z.visible=false);ask.visible=false;panel.visible=who.visible=heart.visible=xMark.visible=s==='s1';wl.visible=wlg.visible=s!=='s1';hand.visible=false;
 warn.visible=s==='s3';edgeG.material.opacity=s==='s3'?.35+.3*Math.abs(Math.sin(t*5)):.0;edge.material.emissiveIntensity=s==='s3'?1.2+Math.sin(t*8)*.6:.5;
 hero.g.rotation.set(0,0,0);gran.g.rotation.set(0,0,0);let p,q;
 if(s==='h'||s==='s1'){// la capataz avanza dormida por el pasillo; la abuela la sigue desde la puerta
  const T=t;const z=-7.5+Math.min(T,TL.s2[0])*.55;hero.g.position.set(.2,0,z);sleepwalk(hero,t,t*2.2);
  ZZ.forEach((zz,i)=>{const ph=(t*.45+i/3)%1;zz.visible=true;zz.position.set(.8+ph*1.4,4.4+ph*2.6,z);zz.material.opacity=Math.sin(Math.PI*ph)});
  gran.g.position.set(-2.4,0,z-4.2);gran.pose(t,0,{walk:t*2.2,look:.15});gran.armR.rotation.x=-.9;
  if(s==='h'){ask.visible=lt>d*.35;ask.position.set(-1.6,5.7,z-4.2);ask.material.opacity=ss(d*.35,d*.5,lt);
   p=V3(4.6-k*1.4,5.2,z+15-k*2.5);q=V3(-.6,4.2,z-2.5)}
  else{p=V3(10.5-k*1,6.6,-2.9);q=V3(-4,6.6,-2.9);heart.rotation.y=t*.8;heart.scale.setScalar(.7+.06*Math.sin(t*7));xMark.scale.setScalar(ss(1.0,1.6,lt))}}
 else if(s==='s2'){// la abuela le toca el hombro: se despierta confusa
  const z=-7.5+TL.s2[0]*.55;hero.g.position.set(.2,0,z);gran.g.position.set(-2.5,0,z-.9);gran.g.rotation.y=.6;
  const wake=ss(d*.18,d*.3,lt);hero.pose(t,wake*.5,{armsUp:wake*(1-ss(d*.45,d*.8,lt))*.55,look:Math.sin(t*2.4)*.5*wake});
  if(wake<.05){sleepwalk(hero,t,0);}else{hero.eyes.forEach(e=>e.scale.set(1+.35*wake,1+.35*wake,1));hero.g.position.x=.2+Math.sin(lt*40)*.06*(1-ss(d*.3,d*.45,lt))}
  gran.pose(t,0,{point:1-ss(d*.3,d*.5,lt)});
  Q.forEach((qq,i)=>{qq.visible=wake>.5;const a=t*1.6+i*2.09;qq.position.set(.2+Math.cos(a)*1.7,5.2+Math.sin(t*3+i)*.3,z+Math.sin(a)*1.7);qq.material.opacity=ss(.5,1,wake)});
  p=V3(3.4-k*.8,5.0,z+16-k*1.5);q=V3(-.9,4.4,z-.8)}
 else if(s==='s3'){// lo peligroso: dormida hacia la escalera; se para en el borde
  const z=1.8+3.6*ss(0,d*.75,lt);hero.g.position.set(.2,0,z);sleepwalk(hero,t,lt<d*.75?t*2.2:0);hero.g.rotation.x=lt>d*.75?Math.sin(t*5)*.05:0;
  gran.g.position.set(-14,0,0);
  p=V3(13-k*1.5,9.5,z+8);q=V3(0,.2,z+2.2)}
 else if(s==='s4'){// de vuelta a la cama, de la mano, con calma
  const z=2-10*ss(0,d,lt);hero.g.rotation.y=gran.g.rotation.y=Math.PI;hero.g.position.set(.9,0,z);gran.g.position.set(-1.0,0,z);
  sleepwalk(hero,t,t*2);hero.armL.rotation.set(-.5,0,-.4);gran.pose(t,m*.3,{walk:t*2,look:-.5});gran.armR.rotation.set(-.6,0,.5);
  hand.visible=true;hand.position.set(-.05,1.5,z+.35);
  p=V3(3.4,7.0,z+15-k*1.5);q=V3(-.2,3.8,z-2.5)}
 else{// cta: dormida en su cama; la abuela saluda
  hero.g.position.set(-30,0,0);gran.g.position.set(-2.1,0,-15.2);gran.g.rotation.y=.35;gran.pose(t,0,{wave:1});
  ZZ.forEach((zz,i)=>{const ph=(t*.45+i/3)%1;zz.visible=true;zz.position.set(1.8+ph*1.4,3.4+ph*2.6,-20.1);zz.material.opacity=Math.sin(Math.PI*ph)});
  p=V3(.4,9.6,-6.5+k*-1.2);q=V3(.6,2.2,-17)}
 const fv=s==='cta'?62:s==='s1'?54:35;if(cam.fov!==fv){cam.fov=fv;cam.updateProjectionMatrix()}cam.position.copy(p);cam.lookAt(q);r.render(scene,cam)};
window.ready=true;
