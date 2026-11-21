// Mito '¿despertarte a mitad de la noche es malo?' (2903): hace siglos se dormía en DOS turnos (Ekirch 2001; Wehr, años 90). Fuentes en mito_dossuenos.py.
// Reutiliza el DORMITORIO DE NOCHE de leer.js. Nuevo y reutilizable: VELA que parpadea (candle), RELOJ DE PARED que corre (wallClock),
// BARRA DE NOCHE 3D con dos bloques de sueño y el hueco despierto (sleepBar), pila de DOCUMENTOS antiguos que suben, apagón de 14 h.
import {THREE,J,mk,ss,V3,clamp,stage,sun,box,glow,capataz,abuela,segAt,mouthAt,label3d,bed,lieDown,puffs,candle,wallClock} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x0a0f26,fog:[0x0a0f26,40,120],exposure:1.25});cam.far=3000;cam.updateProjectionMatrix();const R=mk(2903);
const hemi=new THREE.HemisphereLight(0x7f94d8,0x2a2030,.75);scene.add(hemi);const MOONL=sun(scene,{pos:[-10,20,-14],span:16,color:0xb8c8ff,power:.7});
const ROOM=new THREE.Group();scene.add(ROOM);
const fl=new THREE.Mesh(new THREE.PlaneGeometry(30,30),new THREE.MeshStandardMaterial({color:0x5e4232,roughness:.9}));fl.rotation.x=-Math.PI/2;fl.receiveShadow=true;ROOM.add(fl);
for(let i=0;i<7;i++){const p=box(2.1,.04,30,i%2?0x6e4c36:0x5a3e2e,.01);p.position.set(-7+i*2.2,.02,0);ROOM.add(p)}
const rug=box(6,.06,4,0x2f6a8a,.02);rug.position.set(1,.06,3.2);ROOM.add(rug);
const back=box(30,12,.5,0x2c3462,.05);back.position.set(0,6,-8);ROOM.add(back);
const left=box(.5,12,30,0x323a6c,.05);left.position.set(-8,6,0);ROOM.add(left);
const win=new THREE.Group();{const f=box(5,4.4,.4,0x8a6a4a,.08);win.add(f);const g=box(4.3,3.7,.3,0x0a1030,.02,{emissive:0x14205a,emissiveIntensity:.7});g.position.z=.12;win.add(g);const mo=new THREE.Mesh(new THREE.SphereGeometry(.65,20,14),new THREE.MeshBasicMaterial({color:0xfff4c8,toneMapped:false}));mo.position.set(1,.9,.3);win.add(mo);const mg=glow(0xfff0c0,3,.6);mg.position.set(1,.9,.4);win.add(mg);for(let i=0;i<9;i++){const s=box(.09,.09,.05,0xffffff,.01,{emissive:0xffffff,emissiveIntensity:1});s.position.set((R()-.5)*3.8,(R()-.5)*3,.3);win.add(s)}const bar=box(.2,3.7,.35,0x8a6a4a,.02);bar.position.z=.2;win.add(bar)}
win.position.set(-3.6,6.6,-7.6);ROOM.add(win);
// estantería y mesilla con reloj
const sh=box(1.2,7,4,0x6a4a30,.06);sh.position.set(-7.2,3.5,1.5);ROOM.add(sh);
const BKC=[0xd84a3a,0x3a8ad8,0xf2c230,0x4ab06a,0x9a5cd6,0xff8a3a];for(let k=0;k<3;k++)for(let i=0;i<7;i++){const b=box(.8,1.2+R()*.4,.4,BKC[(i+k)%6],.03);b.position.set(-6.75,1.2+k*2.2+.6,-.2+i*.5);ROOM.add(b)}
const B=bed(0x3a6fd8);B.position.set(.8,0,-3.2);ROOM.add(B);
const nt=box(1.8,2,1.8,0x7a4e2e,.08);nt.position.set(-2.4,1,-6.2);ROOM.add(nt);
const clock=label3d(['03:00'],{w:2.4,h:1,px:170,bg:'#0b0d14',fg:'#ff4a4a',accent:'#2a2f40'});clock.position.set(-2.4,2.6,-5.25);ROOM.add(clock);
const cglow=glow(0xff3a3a,3.4,.55);cglow.position.set(-2.4,2.6,-5.1);ROOM.add(cglow);
const C=candle(scene);C.g.position.set(-2.4,2,-6.2);ROOM.add(C.g);
const WC=wallClock(1.3);WC.g.position.set(3.4,8.2,-7.7);ROOM.add(WC.g);
// puerta (s3: la vecina llega con su vela)
const door=box(3,6.6,.3,0xffd9a0,.02,{emissive:0xffb060,emissiveIntensity:.0});door.position.set(6.2,3.3,-7.7);ROOM.add(door);
const sleeper=capataz();sleeper.hat.forEach(h=>h.visible=false);const L=lieDown(sleeper,B,0x3a6fd8);const sitUp=a=>{sleeper.g.rotation.x=-a};
const book=new THREE.Group();{const cv=box(2.2,.12,1.6,0x7a3a1b,.03);book.add(cv);[-1,1].forEach(s=>{const pg=box(1.02,.1,1.48,0xf8f2e2,.02);pg.position.set(s*.53,.1,0);pg.rotation.z=-s*.12;book.add(pg)})}
book.position.set(0,3.75,1.05);book.rotation.x=-.9;book.scale.setScalar(.8);B.add(book);
const nb=abuela();nb.g.position.set(5.6,0,-5.2);nb.g.rotation.y=-2.3;ROOM.add(nb.g);const NC=candle(scene,{h:.6});NC.g.scale.setScalar(.7);nb.armR.add(NC.g);NC.g.position.set(0,-1.6,.5);
const ZZ=[0,1,2].map(()=>{const z=label3d(['*Z'],{w:1,h:1,px:140,sprite:true,bg:''});scene.add(z);return z});
// barra de la noche: 20:00 → 08:00, dos bloques de sueño y el hueco despierto
const BAR=new THREE.Group();scene.add(BAR);const BW=12;BAR.add((()=>{const b=box(BW+.4,1.3,.5,0x141a33,.2);return b})());
const blk=(c,emi)=>{const b=box(1,1,.6,c,.15,{emissive:emi,emissiveIntensity:.8});BAR.add(b);return b};
const b1=blk(0x3a6fd8,0x1a3a90),bw=blk(0xffc23a,0x9a6a10),b2=blk(0x3a6fd8,0x1a3a90);
const lb1=label3d(['*1er SUEÑO'],{w:4,h:1,px:120,sprite:true,accent:'#7fb0ff'}),lbw=label3d(['*DESPIERTOS'],{w:4,h:1,px:120,sprite:true}),lb2=label3d(['*2º SUEÑO'],{w:4,h:1,px:120,sprite:true,accent:'#7fb0ff'});BAR.add(lb1,lbw,lb2);
const moonI=new THREE.Mesh(new THREE.SphereGeometry(.45,16,12),new THREE.MeshBasicMaterial({color:0xfff4c8,toneMapped:false}));BAR.add(moonI);
const setBar=(fill,a4,aw,a42,labels)=>{// fracciones de la barra (12 h): bloque 1, despierto, bloque 2; fill 0..1 recorre la noche
 const x0=-BW/2;const segs=[[b1,a4],[bw,aw],[b2,a42]];let x=x0+BW*(2/12);const lab=[lb1,lbw,lb2];
 segs.forEach(([b,w],i)=>{const vis=clamp((fill*BW-(x-x0))/(w*BW));b.visible=vis>0;b.scale.set(Math.max(.01,w*BW*vis),1,1);b.position.set(x+w*BW*vis/2,0,.1);lab[i].visible=labels&&vis>.6;lab[i].position.set(x+w*BW/2,i===1?1.5:-1.5,.6);lab[i].scale.set(i===1?4.4:4,1.1,1);x+=w*BW});
 moonI.position.set(x0+fill*BW,1.1,.4)};
const BL=label3d(['20:00','08:00'],{w:1,h:1,px:10,bg:null});
// documentos antiguos que suben (s2) + contador
const DOC=new THREE.Group();scene.add(DOC);const docs=[];for(let i=0;i<34;i++){const d=box(1.1,1.4,.05,[0xe9dcb8,0xf2e8cc,0xd8c69a][i%3],.01);const ln=box(.8,.05,.06,0x5a4a30,.005);ln.position.set(0,.3,.03);d.add(ln);const ln2=ln.clone();ln2.position.y=0;d.add(ln2);DOC.add(d);docs.push([d,R(),R(),R()])}
const cnt=label3d(['*+500','MENCIONES'],{w:6.4,h:3,px:150,sprite:true});scene.add(cnt);
const dark=label3d(['*14 HORAS','A OSCURAS'],{w:6.4,h:3,px:140,sprite:true,accent:'#9fb4ff'});scene.add(dark);
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],k=ss(0,d,lt),m=mouthAt(t);
 const p0=V3(6.8-k*.8+Math.sin(t*.3)*.4,12.6,11.8-k*1.0);const q0=V3(.6,3.4,-4.4);
 const old=s==='s1'||s==='s2'||s==='s3';clock.visible=cglow.visible=!old&&s!=='s4';C.tick(t,old?1:0);C.g.visible=old;NC.tick(t+1.3,1);
 nb.g.visible=s==='s3';BAR.visible=false;DOC.visible=s==='s2';cnt.visible=false;dark.visible=false;ZZ.forEach(z=>z.visible=false);
 const br=Math.sin(t*1.6);L.blanket.scale.y=1+.06*br;sleeper.pose(t,s==='s3'?m*.5:0,{});sleeper.armL.rotation.set(-.3,0,.15);sleeper.armR.rotation.set(-.3,0,-.15);
 let sit=0,eyesClosed=false;book.visible=false;hemi.intensity=1.0;MOONL.intensity=.7;WC.g.visible=true;
 let p,q;
 if(s==='h'){// se despierta de golpe a las 03:00
  sit=1.0*ss(.5,1.0,lt);clock.set(['03:00']);cglow.material.opacity=.45+.2*Math.sin(t*6);eyesClosed=lt<.5;
  WC.set(3);p=p0;q=q0}
 else if(s==='s1'){// antiguo: barra de la noche que se rellena; el durmiente duerme, se despierta y vuelve a dormir
  const f=ss(.3,d-.4,lt);setBar(f,4/12,1.5/12,4/12,true);const inGap=f>6/12&&f<7.5/12;sit=inGap?1:0;eyesClosed=!inGap;WC.set(20+f*12);
  BAR.position.set(.4,1.6,2.2);BAR.scale.setScalar(.5);BAR.lookAt(p0);
  ZZ.forEach((zz,i)=>{if(!inGap){const ph=(t*.45+i/3)%1;zz.visible=true;zz.position.set(1.8+ph*1.4,3.8+ph*2.4,-5.4);zz.material.opacity=Math.sin(Math.PI*ph)}});
  p=p0;q=q0}
 else if(s==='s2'){// documentos que suben en espiral alrededor de la cama
  sit=0;eyesClosed=true;WC.set(1);const n=Math.round(500*ss(.2,d*.7,lt));cnt.set(['*+'+n,'MENCIONES']);cnt.position.set(.6,1.8,2.0);cnt.scale.set(3.6,1.7,1);
  docs.forEach(([dd,a,b,c],i)=>{const ph=(t*.12+a)%1;const ang=b*6.28+t*.5*(c>.5?1:-1);const rr=5.5+c*3;dd.position.set(.8+Math.cos(ang)*rr,ph*12,-4.2+Math.sin(ang)*rr*.5);if(Math.sin(ang)>.2&&ph*12>2&&ph*12<7)dd.visible=false;dd.rotation.set(t*.7+a*5,t*.5+b*5,0);if(!(Math.sin(ang)>.2&&ph*12>2&&ph*12<7))dd.visible=ph<.92});
  p=p0;q=q0}
 else if(s==='s3'){// despiertos a mitad de noche: lee a la luz de la vela y llega la vecina con su vela
  sit=1;book.visible=false;WC.set(1.5);nb.pose(t,m*.5,{look:.2});nb.armR.rotation.set(-1.2,0,.1);
  const wk=ss(0,d*.45,lt);nb.g.position.set(5.6-wk*1.9,0,-5.2+wk*4.0);nb.g.rotation.y=-.9;if(lt<d*.45)nb.pose(t,0,{walk:t*6,look:.2}),nb.armR.rotation.set(-1.2,0,.1);door.material.emissiveIntensity=.6;
  p=p0.clone().add(V3(1.2,0,1.5));q=q0.clone().add(V3(1.4,0,0))}
 else if(s==='s4'){// apagón: 14 horas a oscuras, el reloj de pared corre
  const off=ss(0,.6,lt);hemi.intensity=.95-.35*off;MOONL.intensity=.7*(1-.7*off);eyesClosed=true;WC.set(lt*3.2);
  dark.position.set(.6,1.8,2.0);dark.scale.set(3.6,1.7,1);
  p=p0;q=q0}
 else if(s==='s5'){// el experimento: 4 h, despiertos, 4 h
  hemi.intensity=.6;MOONL.intensity=.4;const f=ss(.2,d-.5,lt);setBar(f,4/12,1.5/12,4/12,true);const inGap=f>6/12&&f<7.5/12;sit=inGap?1:0;eyesClosed=!inGap;WC.set(20+f*12);
  BAR.position.set(.4,1.6,2.2);BAR.scale.setScalar(.5);BAR.lookAt(p0);
  p=p0;q=q0}
 else{// cta: moderno, 03:00, saluda
  sit=1.0;clock.set(['03:00']);WC.set(3);sleeper.armR.rotation.set(0,0,-(2.2+.3*Math.sin(t*7)));
  p=p0;q=q0}
 sitUp(Math.PI/2*(1-sit)+.3*sit);if(eyesClosed)sleeper.eyes.forEach(e=>e.scale.y=.1);
 if(s==='s1'||s==='s5'){ZZ.forEach((zz,i)=>{if(eyesClosed){const ph=(t*.45+i/3)%1;zz.visible=true;zz.position.set(1.8+ph*1.4,3.8+ph*2.4,-5.4);zz.material.opacity=Math.sin(Math.PI*ph)}})}
 cam.position.copy(p);cam.lookAt(q);r.render(scene,cam)};
window.ready=true;
