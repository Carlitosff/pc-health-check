// Mito: '¿crujirte los dedos te da artrosis?' (2803). Donald L. Unger se crujió solo la mano IZQUIERDA cada día durante más de 60 años
// (Improbable Research, 05/11/2009); Ig Nobel de Medicina 2009 ('Mother, you were wrong!', The Tech 02/10/2009); carta en Arthritis and
// Rheumatism (1998); el ruido: burbuja de gas que se forma y revienta (The Conversation, 'Monday's medical myth').
// Reutilizable: MANOS de bloques con nudillos que crujen (chispas + 'CRACK'), modo RAYOS X (hand().xray) y CORTE DE ARTICULACIÓN con burbuja.
import {THREE,J,mk,ss,V3,clamp,stage,sun,box,glow,capataz,abuela,segAt,mouthAt,label3d,hand,puffs} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x2a2440,fog:[0x2a2440,50,140],exposure:1.1});const R=mk(2803);
const hemi=new THREE.HemisphereLight(0xffe2c4,0x2a2030,.9);scene.add(hemi);sun(scene,{pos:[-10,24,18],span:22,color:0xffe8cc,power:1.6});
const key=new THREE.PointLight(0xffb070,70,40,1.4);key.position.set(6,12,10);scene.add(key);
// ---------- SALÓN (suelo, pared, cuadro, lámpara, mesa)
const fl=new THREE.Mesh(new THREE.PlaneGeometry(120,120),new THREE.MeshStandardMaterial({color:0x6a4a34,roughness:.9}));fl.rotation.x=-Math.PI/2;fl.receiveShadow=true;scene.add(fl);
for(let i=0;i<24;i++){const p=box(2.4,.05,120,i%2?0x7a5640:0x6e4c38,.01);p.position.set(-29+i*2.5,.02,0);scene.add(p)}
const wall=box(90,40,.6,0x3b4a6e,.05);wall.position.set(0,20,-12);scene.add(wall);
for(let i=0;i<12;i++){const s=box(.25,40,.1,0x34425f,.01);s.position.set(-33+i*6,20,-11.6);scene.add(s)}
const frame=box(6,4.4,.3,0x8a6a3a,.06);frame.position.set(-9,12,-11.5);scene.add(frame);const pic=box(5.2,3.6,.1,0xe8b04a,.02,{emissive:0x553300,emissiveIntensity:.3});pic.position.set(-9,12,-11.3);scene.add(pic);
const lamp=new THREE.Group();{const st=box(.3,9,.3,0x2a2a30,.02);st.position.y=4.5;lamp.add(st);const sh=box(2.6,1.8,2.6,0xf2d9a8,.2,{emissive:0xffc070,emissiveIntensity:.7});sh.position.y=9.6;lamp.add(sh);const gl=glow(0xffc070,9,.35);gl.position.y=9.6;lamp.add(gl)}lamp.position.set(10,0,-8);scene.add(lamp);
const table=new THREE.Group();{const top=box(16,.6,7,0x8a5a36,.08);top.position.y=3;table.add(top);[[-7,-2.8],[7,-2.8],[-7,2.8],[7,2.8]].forEach(([x,z])=>{const l=box(.6,3,.6,0x5e3c24,.04);l.position.set(x,1.5,z);table.add(l)})}scene.add(table);
// ---------- LAS DOS MANOS (izquierda cruje, derecha nunca)
const HL=hand(-1),HR=hand(1);const HANDS=new THREE.Group();scene.add(HANDS);HL.g.position.set(-3.5,6.6,0);HR.g.position.set(3.5,6.6,0);HANDS.add(HL.g,HR.g);
const lL=label3d(['IZQUIERDA','*CRUJE'],{w:4.6,h:2,px:120,accent:'#ff8a2e'});lL.position.set(-3.5,3.35+1.0,3.55);lL.rotation.x=-.05;HANDS.add(lL);
const lR=label3d(['DERECHA','*NUNCA'],{w:4.6,h:2,px:120,accent:'#4ade80'});lR.position.set(3.5,3.35+1.0,3.55);lR.rotation.x=-.05;HANDS.add(lR);
const okL=label3d(['*SIN ARTROSIS'],{w:4.8,h:1.2,px:110,accent:'#4ade80'}),okR=label3d(['*SIN ARTROSIS'],{w:4.8,h:1.2,px:110,accent:'#4ade80'});okL.position.set(-3.5,4.35,3.7);okR.position.set(3.5,4.35,3.7);HANDS.add(okL,okR);
const yr=label3d(['AÑO','*1'],{w:5,h:2.2,px:120});yr.position.set(0,1.6,3.62);scene.add(yr);
// chispas del crujido (destello + cubitos) en los 4 nudillos
const sparks=HL.knuckles.map(()=>{const s=glow(0xffd27a,2.2,0);scene.add(s);return s});const bits=puffs(scene,48,.14,0xffe2a0);
const crack=label3d(['CRACK!'],{w:4,h:1.5,px:150,bg:null,fg:'#ffd23a',sprite:true});scene.add(crack);
const W0=new THREE.Vector3();
function cracks(t,lt,period,on){ // curl cíclico de la izquierda y chispa al cerrar el puño del todo
 if(!on){HL.curl(0);sparks.forEach(s=>s.material.opacity=0);crack.visible=false;for(let i=0;i<48;i++)bits.set(i,0,-9,0,0);bits.done();return}
 const ph=(lt%period)/period;const k=ph<.45?ss(0,.45,ph):1-ss(.62,.95,ph);HL.curl(.95*k);HL.g.updateMatrixWorld(true);
 const e=ph>.45?Math.max(0,1-(ph-.45)/.22):0;
 HL.knuckles.forEach((kn,i)=>{kn.getWorldPosition(W0);const s=sparks[i];s.position.copy(W0).add(V3(0,0,.6));s.material.opacity=e*.95;s.scale.setScalar(1.2+2.4*(1-e))});
 for(let i=0;i<48;i++){const kn=HL.knuckles[i%4];kn.getWorldPosition(W0);const a=i*2.4,u=(1-e)*1.6;bits.set(i,W0.x+Math.cos(a)*u,W0.y+Math.sin(a)*u*.8+u*.3,W0.z+.7,e>0?.8+e:0,a)}bits.done();
 crack.visible=e>0;crack.position.set(-3.5+Math.sin(lt)*.2,13.2+(1-e)*.8,1.5);crack.material.opacity=e;crack.scale.set(4*(1+.25*(1-e)),1.5*(1+.25*(1-e)),1)}
// ---------- PERSONAJES: madre (abuela) y Donald de niño (capataz sin casco, pequeño)
const mom=abuela();mom.g.position.set(-2.3,0,1);mom.g.rotation.y=.45;scene.add(mom.g);
const kid=capataz();kid.hat.forEach(h=>h.visible=false);kid.g.scale.setScalar(.72);kid.g.position.set(2.4,0,1.5);kid.g.rotation.y=-.5;scene.add(kid.g);
const warn=label3d(['¡TE VA A DAR','*ARTROSIS!'],{w:6.4,h:2.6,px:118,sprite:true,accent:'#ff4d5e'});scene.add(warn);
const doc=capataz();doc.g.position.set(-11,0,3);doc.g.rotation.y=.5;scene.add(doc.g);
// trofeo dorado del Ig Nobel
const tro=new THREE.Group();{const gold={metalness:.8,roughness:.25,emissive:0x5a3c00,emissiveIntensity:.4};const b=box(1.6,.6,1.6,0x3a2a1e,.05);b.position.y=.3;tro.add(b);const st=box(.4,1.2,.4,0xffc23a,.05,gold);st.position.y=1.2;tro.add(st);const cup=box(1.5,1.4,1.5,0xffc23a,.3,gold);cup.position.y=2.4;tro.add(cup);[-1,1].forEach(s=>{const h=box(.25,.9,.25,0xffc23a,.05,gold);h.position.set(s*.95,2.5,0);tro.add(h)});const tg=glow(0xffd27a,5,.5);tg.position.y=2.4;tro.add(tg)}
tro.position.set(0,3.3,1.8);scene.add(tro);
// ---------- CORTE DE LA ARTICULACIÓN (s5): dos huesos, cápsula con líquido y burbuja que aparece y revienta
const JT=new THREE.Group();JT.position.set(0,7,0);scene.add(JT);
const bmat=new THREE.MeshStandardMaterial({color:0xd8ccb0,roughness:.6});
const b1=new THREE.Mesh(new THREE.CylinderGeometry(1.1,1.3,7,24),bmat);b1.rotation.z=Math.PI/2;b1.position.x=-4.25;JT.add(b1);const h1=new THREE.Mesh(new THREE.SphereGeometry(1.45,24,18),bmat);h1.position.x=-1.05;JT.add(h1);
const b2=new THREE.Mesh(new THREE.CylinderGeometry(1.3,1.1,7,24),bmat);b2.rotation.z=Math.PI/2;b2.position.x=4.25;JT.add(b2);const h2=new THREE.Mesh(new THREE.SphereGeometry(1.45,24,18),bmat);h2.position.x=1.05;JT.add(h2);
const cap=new THREE.Mesh(new THREE.SphereGeometry(2.9,32,24),new THREE.MeshStandardMaterial({color:0x7fd0ff,transparent:true,opacity:.18,roughness:.1,depthWrite:false}));cap.scale.set(1.25,.9,.9);JT.add(cap);
const bub=new THREE.Mesh(new THREE.SphereGeometry(1,24,18),new THREE.MeshStandardMaterial({color:0xffffff,emissive:0x4dc8ff,emissiveIntensity:1.1,transparent:true,opacity:.85,roughness:.05}));bub.position.set(0,0,.9);JT.add(bub);
const pop=glow(0xbfe8ff,3,0);pop.position.set(0,0,1.3);JT.add(pop);const lG=label3d(['BURBUJA','*DE GAS'],{w:5,h:2.1,px:120,sprite:true,accent:'#7fd0ff'});lG.position.set(0,-4.4,1.5);JT.add(lG);
const BG0=new THREE.Color(0x2a2440),BGX=new THREE.Color(0x06122e);
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],k=ss(0,d,lt),m=mouthAt(t);
 const handsOn=['h','s2','s3','s4'].includes(s);HANDS.visible=handsOn;yr.visible=s==='s3';
 HL.g.rotation.y=Math.sin(t*.7)*.08;HR.g.rotation.y=-Math.sin(t*.7)*.08;HR.curl(.08+.05*Math.sin(t*1.3));
 cracks(t,lt,s==='s3'?.9:1.35,['h','s2','s3'].includes(s));
 lL.visible=lR.visible=s==='s2'||s==='s3';const xr=s==='s4'?ss(.2,1.2,lt):0;HL.xray(xr);HR.xray(xr);okL.visible=okR.visible=s==='s4'&&lt>1.4;
 if(s==='s4'){const p=ss(1.4,1.9,lt);okL.scale.setScalar(.6+.4*p);okR.scale.setScalar(.6+.4*p);HL.curl(.15+.1*Math.sin(t*2))}
 scene.background=BG0.clone().lerp(BGX,xr);scene.fog.color.copy(scene.background);hemi.intensity=.9-.5*xr;
 if(s==='s3'){const y=Math.max(1,Math.min(60,Math.round(1+59*ss(.3,d-.8,lt))));yr.set(y>=60?['MÁS DE','*60 AÑOS']:['AÑO','*'+y])}
 tro.visible=s==='s4'&&lt>d*.55;if(tro.visible){const p=ss(d*.55,d*.55+.6,lt);tro.scale.setScalar(.01+.99*p);tro.rotation.y=t*1.2}
 const kidOn=s==='s1';table.visible=!(s==='s1'||s==='cta'||s==='s5');mom.g.visible=kid.g.visible=warn.visible=kidOn;
 if(kidOn){mom.pose(t,m,{});mom.armR.rotation.x=-1.3+Math.sin(t*6)*.25;mom.head.rotation.y=-.1;kid.pose(t,0,{look:.2});kid.armL.rotation.x=-1.1;kid.armR.rotation.x=-1.1;
  warn.position.set(-.3,5.45+Math.sin(t*3)*.15,1.5);warn.scale.set(5.0*(1+.05*Math.sin(t*8)),2.05*(1+.05*Math.sin(t*8)),1)}
 doc.g.visible=s==='cta';if(s==='cta'){doc.g.position.set(0,0,2);doc.g.rotation.y=Math.sin(t*.8)*.2;doc.pose(t,m,{wave:1})}
 JT.visible=s==='s5';if(s==='s5'){const g=ss(.4,d*.55,lt),popE=lt>d*.6?Math.max(0,1-(lt-d*.6)/.5):0;const gap=.1+.6*g;h1.position.x=-1.05-gap;h2.position.x=1.05+gap;b1.position.x=-4.25-gap;b2.position.x=4.25+gap;
  bub.visible=lt<d*.6;bub.scale.setScalar(.05+1.05*g*(1+.04*Math.sin(t*20)));pop.material.opacity=popE;pop.scale.setScalar(2.5+4*(1-popE));if(lt>d*.6){h1.position.x=-1.05;h2.position.x=1.05;b1.position.x=-4.25;b2.position.x=4.25}
  JT.rotation.y=Math.sin(t*.5)*.25;lG.material.opacity=ss(.8,1.4,lt)}
 let p,q;
 if(s==='h'){p=V3(-.8+Math.sin(t*.6)*.6,9.8,36-k*4);q=V3(-.4,8.6,0)}
 else if(s==='s1'){p=V3(Math.sin(t*.4)*.6,6.2,26-k*2.5);q=V3(0,4.4,1)}
 else if(s==='s2'){p=V3(-6+k*12,9.6,37);q=V3(0,7.6,0)}
 else if(s==='s3'){const a=-.5+k*1.0;p=V3(Math.sin(a)*37,10.5,Math.cos(a)*37);q=V3(0,7.6,0)}
 else if(s==='s4'){p=V3(Math.sin(t*.4)*1.5,9.6,38-k*3);q=V3(0,7.6,0)}
 else if(s==='s5'){p=V3(Math.sin(t*.5)*2,8.4,32-k*4);q=V3(0,6.2,0)}
 else{p=V3(Math.sin(t*.5)*1.5,4.6,24-k*2);q=V3(0,2.9,2)}
 cam.position.copy(p);cam.lookAt(q);r.render(scene,cam)};
window.ready=true;
