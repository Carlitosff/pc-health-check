// Mito '¿dormir con calcetines te ayuda a dormir?' (3203). Fuentes en mito_calcetines.py.
// Reutilizable: DORMITORIO FRESCO con DOS CAMAS (comparativa A/B de dormir), PIES que asoman de la manta (feet: descalzos o con calcetines),
// CALOR que sale de los pies (puffs naranjas), escarcha en la ventana, Z que suben y durmiente que se despierta a sacudidas.
import {THREE,J,mk,ss,V3,clamp,stage,sun,box,glow,capataz,abuela,segAt,mouthAt,label3d,bed,lieDown,puffs,wallClock} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x0a1230,fog:[0x0a1230,45,130],exposure:1.25});cam.far=600;cam.updateProjectionMatrix();const R=mk(3203);
const hemi=new THREE.HemisphereLight(0x8fb0ff,0x2a2030,.9);scene.add(hemi);const MOONL=sun(scene,{pos:[-12,22,-10],span:18,color:0xb8d0ff,power:.9});
const ROOM=new THREE.Group();scene.add(ROOM);
const fl=new THREE.Mesh(new THREE.PlaneGeometry(40,40),new THREE.MeshStandardMaterial({color:0x5e4232,roughness:.9}));fl.rotation.x=-Math.PI/2;fl.receiveShadow=true;ROOM.add(fl);
for(let i=0;i<11;i++){const p=box(2.1,.04,40,i%2?0x6e4c36:0x5a3e2e,.01);p.position.set(-11+i*2.2,.02,0);ROOM.add(p)}
const back=box(40,13,.5,0x2c3a6a,.05);back.position.set(0,6.5,-8);ROOM.add(back);
const left=box(.5,13,40,0x33407a,.05);left.position.set(-12,6.5,0);ROOM.add(left);
// ventana con escarcha (habitación fresca)
const win=new THREE.Group();{const f=box(5.4,4.4,.4,0xb8c8d8,.08);win.add(f);const g=box(4.7,3.7,.3,0x0a1438,.02,{emissive:0x1a2a6a,emissiveIntensity:.8});g.position.z=.12;win.add(g);
 for(let i=0;i<60;i++){const s=box(.18+R()*.3,.05,.05,0xffffff,.01,{emissive:0xdff0ff,emissiveIntensity:.9});const a=R()*6.28,d=1.3+R()*1.1;s.position.set(Math.cos(a)*d*1.1,Math.sin(a)*d*.8,.3);s.rotation.z=a;win.add(s)}
 const mo=new THREE.Mesh(new THREE.SphereGeometry(.6,20,14),new THREE.MeshBasicMaterial({color:0xfff4c8,toneMapped:false}));mo.position.set(.9,.8,.3);win.add(mo);const bar=box(.2,3.7,.35,0xb8c8d8,.02);bar.position.z=.2;win.add(bar)}
win.position.set(0,7,-7.6);ROOM.add(win);
const thermo=label3d(['HABITACIÓN','*FRESCA'],{w:4.2,h:1.9,px:110,accent:'#8fd0ff'});thermo.position.set(-6.5,8.6,-7.7);ROOM.add(thermo);
const WC=wallClock(1.2);WC.g.position.set(6.5,8.6,-7.7);ROOM.add(WC.g);
// dos camas: A (izquierda, abuela, descalza) y B (derecha, capataz, con calcetines)
const BA=bed(0x6a8ad8),BB=bed(0xd85a3a);BA.position.set(-4.2,0,-2.6);BB.position.set(4.2,0,-2.6);ROOM.add(BA,BB);
const sA=abuela(),sB=capataz();sB.hat.forEach(h=>h.visible=false);const LA=lieDown(sA,BA,0x6a8ad8),LB=lieDown(sB,BB,0xd85a3a);
const SKIN=0xe3b48c,SKINB=0xd9a06a;
function feet(B,sock,skin){const g=new THREE.Group();const parts=[];[-.5,.5].forEach(x=>{const f=new THREE.Group();const sole=box(.62,.95,.42,sock?0xd83a3a:skin,.12);sole.position.y=.47;f.add(sole);
  if(sock){const cuff=box(.66,.22,.46,0xffffff,.06);cuff.position.y=-.02;f.add(cuff);const st=box(.64,.14,.44,0xffffff,.04);st.position.y=.62;f.add(st);const toe=box(.64,.22,.44,0xffc23a,.08);toe.position.y=.9;f.add(toe)}
  else{for(let k=0;k<4;k++){const t=box(.12,.14,.14,skin,.04);t.position.set(-.21+k*.14,1.0,.08);f.add(t)}}
  f.position.set(x,2.2,3.55);f.rotation.x=-.15;g.add(f);parts.push(f)});B.add(g);return{g,parts}}
const FA=feet(BA,false,SKIN),FB=feet(BB,true,SKINB);
const coldA=glow(0x6ab8ff,2.6,.0);coldA.position.set(0,2.8,3.7);BA.add(coldA);
const warmB=glow(0xff8a3a,2.8,.0);warmB.position.set(0,2.8,3.7);BB.add(warmB);
const HEAT=puffs(scene,60,.16,0xffa040,{opacity:.85});
const lA=label3d(['*SIN','CALCETINES'],{w:3.4,h:1.5,px:110,sprite:true,accent:'#8fd0ff'}),lB=label3d(['*CON','CALCETINES'],{w:3.4,h:1.5,px:110,sprite:true,accent:'#ff6a4a'});scene.add(lA,lB);
const ZZ=[0,1,2].map(()=>{const z=label3d(['*Z'],{w:1,h:1,px:140,sprite:true,bg:''});scene.add(z);return z});
const big=label3d(['*TU CUERPO','SE ENFRÍA POR DENTRO'],{w:7.4,h:2.6,px:110,sprite:true,accent:'#ffc23a'});scene.add(big);
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],k=ss(0,d,lt),m=mouthAt(t);
 const br=Math.sin(t*1.6);LA.blanket.scale.y=1+.05*br;LB.blanket.scale.y=1+.05*Math.sin(t*1.6+1);
 [sA,sB].forEach(o=>{o.pose(t,0,{});o.armL.rotation.set(-.3,0,.15);o.armR.rotation.set(-.3,0,-.15)});
 sA.g.rotation.x=-Math.PI/2;sB.g.rotation.x=-Math.PI/2;
 FA.parts.forEach((f,i)=>f.rotation.z=Math.sin(t*2.2+i)*.05);FB.parts.forEach((f,i)=>f.rotation.z=Math.sin(t*.8+i)*.03);
 lA.visible=lB.visible=false;ZZ.forEach(z=>z.visible=false);big.visible=false;coldA.material.opacity=0;warmB.material.opacity=0;
 let heatOn=0;WC.set(23+t*.12);
 // la abuela (descalza) se despierta a sacudidas en s2/s3; el capataz duerme
 const wake=(s==='s2'||s==='s3')?Math.max(0,Math.sin(lt*(s==='s3'?3.2:1.6)-.6)):0;if(wake>0)sA.g.rotation.x=-Math.PI/2+.55*ss(0,.6,wake);
 const zzAt=c=>ZZ.forEach((zz,i)=>{const ph=(t*.45+i/3)%1;zz.visible=true;zz.position.set(c.x+.6+ph*1.4,c.y+ph*2.4,c.z);zz.material.opacity=Math.sin(Math.PI*ph)});
 let p,q;
 if(s==='h'){// primer plano de los pies con calcetines (el frame 0 ya enseña la pregunta)
  warmB.material.opacity=.35+.1*Math.sin(t*3);p=V3(4.2+3.4-k*1.2,7.2+Math.sin(t*.8)*.2,11.5-k*1.2);q=V3(4.2,2.6,-.8)}
 else if(s==='s1'){// las dos camas en la habitación fresca
  lA.visible=lB.visible=lt>.6;lA.position.set(-4.2,4.9,1.6);lB.position.set(4.2,4.9,1.6);coldA.material.opacity=.3;warmB.material.opacity=.3;
  p=V3(-1+k*2,13-k*1,33-k*2);q=V3(0,4.2,-2)}
 else if(s==='s2'){// el de los calcetines se duerme antes
  zzAt(V3(4.2,4.0,-1.8));warmB.material.opacity=.3;lB.visible=true;lB.position.set(4.2,4.9,1.6);
  p=V3(7.4+k*1.5,9.5,17-k*1.5);q=V3(4.2,3.0,-1.6)}
 else if(s==='s3'){// la descalza se despierta una y otra vez
  zzAt(V3(4.2,4.0,-1.8));coldA.material.opacity=.35+.15*Math.sin(t*4);lA.visible=true;lA.position.set(-4.2,4.9,1.6);
  p=V3(-7.6+k*1.5,9.5,17-k*1.5);q=V3(-4.2,3.0,-1.6)}
 else if(s==='s4'){// el calor sale por los pies y el cuerpo se enfría por dentro
  heatOn=1;warmB.material.opacity=.55+.15*Math.sin(t*5);big.visible=false;big.position.set(4.2,6.9,-1.2);
  p=V3(4.2-3.2+k*1.6,6.4+k*.5,12.5-k*.8);q=V3(4.2,3.8,-.2)}
 else{zzAt(V3(4.2,4.0,-1.8));coldA.material.opacity=.2;warmB.material.opacity=.3;p=V3(k*1.5,13,34-k*2);q=V3(0,4.2,-2)}
 for(let i=0;i<60;i++){const ph=(t*.55+i/60)%1,side=i%2?.5:-.5;const x=4.2+side+Math.sin(t*2+i*1.7)*.25*(1+ph),y=3.2+ph*3.2,z=1.0+Math.cos(t*1.6+i)*.2;HEAT.set(i,x,y,z,heatOn?(1-ph)*1.3:0,t+i)}
 HEAT.done();HEAT.m.material.opacity=.85;
 cam.position.copy(p);cam.lookAt(q);r.render(scene,cam)};
window.ready=true;
