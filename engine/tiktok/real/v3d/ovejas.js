// Mito: 'contar ovejas te ayuda a dormir' (1903). Harvey y Payne, Oxford, Behaviour Research and Therapy 2002.
// Reutilizable: OVEJA de bloques (personaje propio nº 3 de la cuenta: lana de cubos, cara gris, salta con arco y se tumba a dormir), cama con manta,
// dormitorio nocturno con ventana y luna, reloj digital integrado (label3d), sala del laboratorio con 3 camas y 'burbujas de pensamiento' (mini-dioramas).
import {THREE,J,mk,ss,V3,clamp,stage,sun,box,glow,rig,capataz,abuela,segAt,mouthAt,label3d,puffs,stars} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x0d1430,fog:[0x0d1430,40,140],exposure:1.12});const R=mk(1903);
const hemi=new THREE.HemisphereLight(0x8fa4e0,0x241a2a,.75);scene.add(hemi);const S=sun(scene,{pos:[-12,26,16],span:26,color:0xb8c8ff,power:1.1});
const lampL=new THREE.PointLight(0xffc880,60,30,1.5);lampL.position.set(5.5,5,3);scene.add(lampL);
// ---------- OVEJA (exportable por copia): o.g, o.jump(k) 0..1 arco, o.sleep(k)
export function oveja(s=1){const g=new THREE.Group();const body=new THREE.Group();g.add(body);const W_=0xf4f1ea,W2=0xe6e1d6;
 const Q=mk(77);for(let i=0;i<14;i++){const b=box(.9+Q()*.4,.8+Q()*.3,.9+Q()*.4,i%3?W_:W2,.3);b.position.set((Q()-.5)*1.6,1.35+(Q()-.3)*.55,(Q()-.5)*.9);body.add(b)}
 const core=box(2.1,1.15,1.3,W_,.35);core.position.y=1.35;body.add(core);
 const head=new THREE.Group();head.position.set(1.25,1.75,0);body.add(head);const hd=box(.85,.8,.75,0x3a3a42,.14);head.add(hd);const tuft=box(.7,.35,.7,W_,.15);tuft.position.set(-.05,.5,0);head.add(tuft);
 const eyes=[-.2,.2].map(z=>{const e=box(.06,.16,.14,0xffffff,.02);e.position.set(.43,.08,z);head.add(e);const p=box(.05,.1,.07,0x101014,.01);p.position.set(.46,.07,z);head.add(p);return[e,p]});
 [-1,1].forEach(z=>{const ear=box(.15,.18,.45,0x2c2c34,.05);ear.position.set(-.1,.18,z*.48);ear.rotation.x=z*.5;head.add(ear)});
 const legs=[[.65,.4],[.65,-.4],[-.65,.4],[-.65,-.4]].map(([x,z])=>{const l=new THREE.Group();l.position.set(x,.8,z);const m=box(.28,.8,.28,0x2c2c34,.05);m.position.y=-.4;l.add(m);body.add(l);return l});
 g.scale.setScalar(s);
 const o={g,body,head,eyes,legs,jump(k){// k 0..1: carrera, salto con arco y aterrizaje
   const y=Math.sin(Math.PI*clamp(k))*2.2;body.position.y=y;body.rotation.z=Math.cos(Math.PI*clamp(k))*.35*(k>0&&k<1?1:0);
   const tuck=k>0&&k<1?Math.sin(Math.PI*k):0;legs.forEach((l,i)=>{l.rotation.z=(i<2?-1:1)*tuck*.9})},
  sleep(k){body.position.y=-.55*k;legs.forEach(l=>{l.rotation.x=0;l.scale.y=1-.6*k});head.rotation.z=-.35*k;head.position.y=1.75-.25*k;eyes.forEach(([e,p])=>{e.scale.y=1-.9*k;p.visible=k<.5})}};
 return o}
// ---------- cama
function bed(col=0x3a6fd8){const g=new THREE.Group();const fr=box(4.4,.8,7,0x7a4e2e,.08);fr.position.y=.6;g.add(fr);const mat=box(4.1,.5,6.6,0xf2efe8,.15);mat.position.y=1.2;g.add(mat);
 const hb=box(4.6,3,.4,0x7a4e2e,.1);hb.position.set(0,1.6,-3.4);g.add(hb);const pil=box(2.6,.5,1.3,0xffffff,.22);pil.position.set(0,1.65,-2.4);g.add(pil);
 const bl=box(4.3,.5,4.4,col,.18);bl.position.set(0,1.62,1.0);g.add(bl);const fold=box(4.32,.52,.6,0xf4f4f4,.15);fold.position.set(0,1.64,-1.1);g.add(fold);return g}
// persona sentada en la cama (piernas bajo la manta)
function inBed(o,y=1.25){o.legL.visible=o.legR.visible=false;o.g.position.y=y;o.g.position.z=-1.6;return o}
// ---------- DORMITORIO (h, s3, s4, cta)
const room=new THREE.Group();scene.add(room);
const fl=new THREE.Mesh(new THREE.PlaneGeometry(80,80),new THREE.MeshStandardMaterial({color:0x5a4030,roughness:.9}));fl.rotation.x=-Math.PI/2;fl.receiveShadow=true;room.add(fl);
const planks=new THREE.Group();room.add(planks);for(let i=0;i<16;i++){const p=box(2.4,.05,80,i%2?0x6a4a36:0x5e4232,.01);p.position.set(-19+i*2.5,.02,0);planks.add(p)}
const wall=box(60,22,.6,0x27315a,.05);wall.position.set(0,11,-8);room.add(wall);
const win=new THREE.Group();{const f=box(7,6,.5,0x8a6a4a,.08);win.add(f);const gl=box(6.2,5.2,.3,0x0a1030,.02,{emissive:0x101848,emissiveIntensity:.6});gl.position.z=.12;win.add(gl);const cx=box(.25,5.2,.35,0x8a6a4a,.02);cx.position.z=.2;const cy=box(6.2,.25,.35,0x8a6a4a,.02);cy.position.z=.2;win.add(cx,cy);const moon=new THREE.Mesh(new THREE.SphereGeometry(.9,20,14),new THREE.MeshBasicMaterial({color:0xfff4c8,toneMapped:false}));moon.position.set(1.5,1.3,.3);win.add(moon);const mg=glow(0xfff0b0,5,.6);mg.position.set(1.5,1.3,.4);win.add(mg);
 for(let i=0;i<14;i++){const s=box(.12,.12,.05,0xffffff,.01,{emissive:0xffffff,emissiveIntensity:1});s.position.set((R()-.5)*5.6,(R()-.5)*4.6,.3);win.add(s)}}
win.position.set(-7,9,-7.6);room.add(win);
const B1=bed(0x3a6fd8);B1.position.set(1,0,-3.5);room.add(B1);
const hero=inBed(capataz());hero.hat.forEach(h=>h.visible=false);B1.add(hero.g);
const nt=box(2.2,2.4,2.2,0x7a4e2e,.08);nt.position.set(5.2,1.2,-5.5);room.add(nt);const lampS=box(.9,1.2,.9,0xffd890,.2,{emissive:0xffb050,emissiveIntensity:.9});lampS.position.set(5.2,3.1,-5.5);room.add(lampS);const lg=glow(0xffc070,5,.5);lg.position.set(5.2,3.4,-5.3);room.add(lg);
const clock=label3d(['03:12'],{w:3,h:1.25,px:170,bg:'#0b0d14',fg:'#ff4a4a',accent:'#2a2f40'});clock.position.set(-3.3,4.8,-7.6);room.add(clock);
// valla y ovejas que saltan por el dormitorio
const fence=new THREE.Group();[-1.6,0,1.6].forEach(z=>{const p=box(.35,2,.35,0xc8a070,.05);p.position.set(0,1,z);fence.add(p)});[.7,1.5].forEach(y=>{const b=box(.22,.3,3.8,0xd8b080,.05);b.position.set(0,y,0);fence.add(b)});fence.position.set(1,0,4.5);room.add(fence);
const flock=[];for(let i=0;i<6;i++){const o=oveja(.85);o.g.rotation.y=0;room.add(o.g);flock.push(o)}
const cnt=label3d(['OVEJA 1'],{w:3.6,h:1.1,px:130,accent:'#ffc23a'});cnt.position.set(3.9,5.8,-1);room.add(cnt);
const zz=[];for(let i=0;i<4;i++){const z=label3d(['Z'],{w:1.4,h:1.4,bg:null,fg:'#cfe0ff',px:400,sprite:true});room.add(z);zz.push(z)}
const pile=[];for(let i=0;i<10;i++){const o=oveja(.7);o.g.visible=false;room.add(o.g);pile.push(o)}
// ---------- LABORATORIO (s1, s2): 3 camas, rótulo de Oxford y burbujas de pensamiento
const LAB=new THREE.Group();LAB.position.set(300,0,0);scene.add(LAB);
const lf=new THREE.Mesh(new THREE.PlaneGeometry(120,80),new THREE.MeshStandardMaterial({color:0xd8dbe2,roughness:.6}));lf.rotation.x=-Math.PI/2;lf.receiveShadow=true;LAB.add(lf);
for(let i=0;i<12;i++)for(let j=0;j<8;j++){if((i+j)%2)continue;const t=box(2.8,.03,2.8,0xc2c6d0,.01);t.position.set(-16.5+i*3,.02,-9+j*3);LAB.add(t)}
const lw=box(80,24,.6,0x3a4a6a,.05);lw.position.set(0,12,-11);LAB.add(lw);
const sign=label3d(['UNIVERSIDAD DE OXFORD','*2002 · INSOMNIO'],{w:13,h:3.4,px:100,accent:'#ffc23a'});sign.position.set(0,12.2,-10.6);LAB.add(sign);
const beds=[[-4.9,0xd85a3a],[0,0x3aa86a],[4.9,0x7a7a8a]].map(([x,c],i)=>{const b=bed(c);b.position.set(x,0,-4);b.scale.setScalar(.85);LAB.add(b);const p=inBed(i===1?abuela():capataz());if(p.hat)p.hat.forEach(h=>h.visible=false);b.add(p.g);return{b,p}});
const tags=['OVEJAS','PLAYA','NADA'].map((s,i)=>{const l=label3d([s],{w:4.4,h:1.3,px:120,accent:['#ff7a5a','#4ade80','#9aa0b0'][i]});l.position.set(-4.9+i*4.9,1.3,1.2);LAB.add(l);return l});
// burbujas: mini valla+oveja / mini playa / vacía
const bub=[];for(let i=0;i<3;i++){const g=new THREE.Group();g.position.set(-4.9+i*4.9,7.6,-4);const disc=new THREE.Mesh(new THREE.CircleGeometry(2.2,40),new THREE.MeshBasicMaterial({color:0xffffff,transparent:true,opacity:.92}));g.add(disc);[[-.9,-2.8,.4],[-.5,-3.4,.25]].forEach(([x,y,s])=>{const d=new THREE.Mesh(new THREE.CircleGeometry(s,20),disc.material);d.position.set(x,y,0);g.add(d)});LAB.add(g);bub.push(g)}
const miniS=oveja(.55);miniS.g.position.set(-.3,-1.3,.3);bub[0].add(miniS.g);const mf=box(.15,1.1,.15,0xc8a070,.03);mf.position.set(.3,-1.1,.4);bub[0].add(mf);
{const g=bub[1];const sea=box(5,1.2,.2,0x2a9ad8,.05);sea.position.set(0,-.3,.1);g.add(sea);const sand=box(5,1,.25,0xf0d890,.05);sand.position.set(0,-1.5,.15);g.add(sand);const sunM=new THREE.Mesh(new THREE.CircleGeometry(.6,20),new THREE.MeshBasicMaterial({color:0xffd23a}));sunM.position.set(1.4,1.2,.15);g.add(sunM);const tr=box(.22,1.6,.2,0x7a5430,.03);tr.position.set(-1.4,-.4,.3);g.add(tr);for(let k=0;k<4;k++){const lf_=box(1.1,.2,.1,0x3fa04a,.03);lf_.position.set(-1.4+Math.cos(k*1.6)*.5,.45,.35);lf_.rotation.z=k*1.6;g.add(lf_)}g.userData.wave=sea}
const q3=label3d(['…'],{w:2.4,h:1.2,bg:null,fg:'#9aa0b0',px:300});q3.position.set(0,0,.2);bub[2].add(q3);
const lsun=sun(scene,{pos:[290,30,20],target:[300,0,-4],span:24,color:0xffffff,power:2.2});
const minus=label3d(['*−20 MIN'],{w:4,h:1.45,px:170,accent:'#4ade80',sprite:true});room.add(minus);
// ---------- PLAYA imaginada (s4): se abre alrededor de la cama
const BE=new THREE.Group();room.add(BE);const bs=new THREE.Mesh(new THREE.PlaneGeometry(80,40),new THREE.MeshStandardMaterial({color:0xf0d890,roughness:1}));bs.rotation.x=-Math.PI/2;bs.position.set(0,.06,8);BE.add(bs);
const bsea=new THREE.Mesh(new THREE.PlaneGeometry(120,60),new THREE.MeshStandardMaterial({color:0x2a9ad8,roughness:.3}));bsea.rotation.x=-Math.PI/2;bsea.position.set(0,.08,-40);BE.add(bsea);
const T1=label3d(['TARDABAN MÁS'],{w:4.6,h:1.25,px:140,accent:'#ff4a4a',sprite:true});room.add(T1);
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],m=mouthAt(t);
 const inLab=s==='s1'||s==='s2';room.visible=!inLab;LAB.visible=inLab;
 let p,q;
 if(!inLab){
  // reloj: avanza; en s3 corre deprisa (tardan más); en s4 se para
  const base=3*60+12;let mins=base+Math.floor(t/4);if(s==='s3')mins+=Math.floor(lt*9);if(s==='s4'||s==='cta')mins=base+Math.floor(TL.s4[0]/4)+3;
  clock.set([`0${Math.floor(mins/60)%10}:${String(mins%60).padStart(2,'0')}`]);
  const beach=s==='s4'||s==='cta';const bk=s==='s4'?ss(.3,2.2,lt):s==='cta'?1:0;BE.visible=bk>0;bs.material.opacity=bk;
  BE.position.y=-3+3*bk;planks.visible=bk<.6;fence.visible=!beach;
  const night=new THREE.Color(0x0d1430),day=new THREE.Color(0x8fd0ff);const bg=night.clone().lerp(day,bk*.85);scene.background=bg;scene.fog.color.copy(bg);wall.visible=win.visible=clock.visible=bk<.5;
  S.intensity=1.1+1.6*bk;hemi.intensity=.75+.6*bk;
  // ovejas que saltan la valla (en bucle; en s4 se tumban)
  const nS=s==='s3'?Math.min(10,Math.floor(lt*2.2)):0;
  flock.forEach((o,i)=>{const per=2.4,ph=(t/per+i/flock.length+.411)%1;const x=-14+ph*28;o.g.position.set(x,0,4.5+(i%2)*.4);o.g.rotation.y=0;o.sleep(0);
   const jk=clamp((x-(1-2.2))/4.4);o.jump(x>-1.2&&x<3.2?jk:0);o.legs.forEach((l,k)=>{l.rotation.x=Math.sin(t*14+k*1.6)*.5});
   o.g.visible=!beach});
  // s3: se amontonan ovejas (no se duerme)
  pile.forEach((o,i)=>{o.g.visible=s==='s3'&&i<nS;o.g.position.set(-5+(i%5)*2.4,0,9.5+Math.floor(i/5)*2.3);o.g.rotation.y=.6+i;o.sleep(0)});
  let cn=1+Math.floor(t*1.6);if(s==='s3')cn+=Math.floor(lt*6);cnt.set([`OVEJA ${cn}`]);cnt.visible=!beach;
  T1.visible=s==='s3'&&lt>1.5;T1.position.set(-1.4,6.7,-1);
  // personaje: ojos abiertos (h, s3) / se duerme (s4, cta)
  const sl=s==='s4'?ss(d*.35,d*.75,lt):s==='cta'?1:0;
  hero.pose(t,s==='cta'?0:m*.15,{look:s==='h'?.6+Math.sin(t*1.4)*.25:s==='s3'?Math.sin(t*2.2)*.35:0});
  hero.eyes.forEach(e=>{e.scale.y=Math.max(.08,1-sl)});hero.head.rotation.z=.25*sl;hero.g.rotation.x=-.5*sl;
  hero.armL.rotation.z=-.14-(s==='s3'?.5+.2*Math.sin(t*6):0);
  zz.forEach((z,i)=>{const k=((t*.45+i/4)%1);z.visible=sl>.4;z.position.set(2+k*2+Math.sin(t+i)*.3,4.6+k*2.6,-4.5);z.material.opacity=Math.sin(Math.PI*k);const sc=.8+k*1.4;z.scale.set(sc,sc,1)});
  minus.visible=s==='s4'&&lt>d*.45||s==='cta';minus.position.set(-.8,6.9,-1);
  // cámara
  if(s==='h'){const k=ss(0,d,lt);p=V3(6-k*2,8.5,25-k*3);q=V3(1,3.6,0)}
  else if(s==='s3'){const k=ss(0,d,lt);p=V3(-6+k*3,8,26-k*2);q=V3(.5,4.6,1)}
  else if(s==='s4'){const k=ss(0,d,lt);p=V3(4,7+k*1.5,20+k*3);q=V3(1,4.6,-3)}
  else{const k=ss(0,d,lt);p=V3(2-k*3,8+k,25+k*2);q=V3(1,4.8,-2)}
  if(lt<.5&&s==='s3'){p.x+=Math.sin(t*60)*.06}
 }else{scene.background=new THREE.Color(0x26304a);scene.fog.color.set(0x26304a);S.intensity=0;hemi.intensity=1.0;lsun.intensity=2.2;
  beds.forEach(({p:pp},i)=>{pp.pose(t,0,{look:Math.sin(t*.8+i)*.3});});
  const k2=s==='s2'?ss(.2,1.6,lt):0;bub.forEach((g,i)=>{const kk=s==='s2'?ss(.2+i*.9,1.2+i*.9,lt):0;g.scale.setScalar(Math.max(.001,kk*(1+.04*Math.sin(t*3+i))));g.visible=kk>0;g.lookAt(LAB.position.clone().add(V3(0,9,30)))});
  tags.forEach((l,i)=>{l.visible=s==='s2'&&lt>.4+i*.9});
  const mk2=(t*.5)%1;miniS.jump(mk2);miniS.g.position.x=-1.6+mk2*2.6;bub[1].userData.wave.position.y=-.3+Math.sin(t*2)*.08;
  if(s==='s1'){const k=ss(0,d,lt);p=V3(300+4-k*4,7,40-k*4);q=V3(300,7.5,-4)}
  else{const k=ss(0,d,lt);p=V3(300,6+k,38);q=V3(300,6.2,-4)}
  sign.visible=s==='s1'
 }
 if(inLab)lsun.intensity=2.2;else lsun.intensity=0;
 cam.position.copy(p);cam.lookAt(q);r.render(scene,cam)};
window.ready=true;
