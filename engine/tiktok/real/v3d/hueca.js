// ¿Y si la Tierra estuviera hueca? (2504). Serie ¿QUÉ PASARÍA SI…? Parte 14. Cálculos en serie_hueca.py. Basada en encoge.js.
// Nuevo (v28): voxShell (bloques.js): planeta de cubos CORTADO en cuña, con corteza de varias capas, cara interior de roca y esferas dentro (Halley 1692);
// interior hueco con luz central y capataz que FLOTA girando sin arriba ni abajo.
import {THREE,J,mk,ss,V3,clamp,stage,sun,box,glow,pixTex,capataz,segAt,mouthAt,puffs,label3d,stars,voxShell} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x8ad4ff,fog:[0xc8e4ff,60,190],exposure:1.08});cam.far=3000;cam.updateProjectionMatrix();const R=mk(2504);
const hemi=new THREE.HemisphereLight(0xdcefff,0x8a9a6a,1.4);scene.add(hemi);const S=sun(scene,{pos:[-16,34,18],span:34});
const SKY=new THREE.Color(0x8ad4ff),SPACE=new THREE.Color(0x02030a),CAVE=new THREE.Color(0x1a0f08);
// ---------- plaza (igual que crece/encoge)
const st=new THREE.Group();scene.add(st);
const grass=pixTex(128,128,(g,w,h)=>{const q=mk(8);g.fillStyle='#6fb24e';g.fillRect(0,0,w,h);for(let i=0;i<700;i++){g.fillStyle=['#62a544','#7dbd58','#568f3c'][Math.floor(q()*3)];g.fillRect(Math.floor(q()*w/4)*4,Math.floor(q()*h/4)*4,4,4)}},[40,40]);
const gnd=new THREE.Mesh(new THREE.PlaneGeometry(400,400),new THREE.MeshStandardMaterial({map:grass,roughness:1}));gnd.rotation.x=-Math.PI/2;gnd.receiveShadow=true;st.add(gnd);
const plaza=new THREE.Mesh(new THREE.PlaneGeometry(40,22),new THREE.MeshStandardMaterial({map:pixTex(64,64,(g,w,h)=>{g.fillStyle='#d8cdb6';g.fillRect(0,0,w,h);g.strokeStyle='#b9ad94';g.lineWidth=2;for(let i=0;i<=w;i+=16){g.strokeRect(i,0,16,h);g.strokeRect(0,i,w,16)}},[10,6]),roughness:.95}));plaza.rotation.x=-Math.PI/2;plaza.position.set(0,.01,0);plaza.receiveShadow=true;st.add(plaza);
const COLS=[0xd9c7a8,0xc2573f,0x8fa6b8,0xe8dfca,0xa86a48,0x6f86a8];
[[-15,-14,8,14],[-5,-16,9,18],[6,-15,8,12],[16,-13,8,16],[-26,-10,7,11],[27,-10,7,13]].forEach(([x,z,w,h],i)=>{const b=box(w,h,7,COLS[i%6],.15);b.position.set(x,h/2,z);st.add(b);for(let y=1.5;y<h-1;y+=2.2)for(let a=-w/2+1.3;a<w/2-.8;a+=1.8){const wi=box(.9,1.2,.1,R()<.3?0xffe9a8:0x2a3a58,.02);wi.position.set(x+a,y,z+3.52);st.add(wi)}});
[[-9,4],[9,5],[-12,-4],[12,-5]].forEach(([x,z])=>{const tr=box(.6,2.4,.6,0x7a5232,.05);tr.position.set(x,1.2,z);st.add(tr);const cr=box(2.6,2.4,2.6,0x3f9a46,.3);cr.position.set(x,3.4,z);st.add(cr)});
// agujero en la plaza (se abre en el h): pozo oscuro con borde de roca
const hole=new THREE.Group();const pit=new THREE.Mesh(new THREE.CircleGeometry(2.6,40),new THREE.MeshBasicMaterial({color:0x050302}));pit.rotation.x=-Math.PI/2;pit.position.y=.03;hole.add(pit);
for(let i=0;i<22;i++){const a=i/22*6.283;const rk=box(.8,.35+R()*.3,.8,i%2?0x7a5a3e:0x5e4430,.08);rk.position.set(Math.cos(a)*2.8,.15,Math.sin(a)*2.8);rk.rotation.y=a;hole.add(rk)}hole.position.set(-4.6,0,4.5);st.add(hole);
const holeGlow=glow(0xff9a40,5,.0);holeGlow.position.set(-4.6,.4,4.5);st.add(holeGlow);
// báscula + pantalla
const scale=new THREE.Group();const base=box(3.2,.4,2.6,0xe8eaf0,.12);base.position.y=.2;scale.add(base);const top=box(2.8,.12,2.2,0x30343e,.05);top.position.y=.46;scale.add(top);scale.position.set(0,0,2);st.add(scale);
const disp=label3d(['80 kg'],{w:4.2,h:1.6,px:150,accent:'#ff4a4a'});disp.position.set(3.4,3.5,2.6);st.add(disp);const dpost=box(.25,2.4,.25,0x30343e,.03);dpost.position.set(3.4,1.2,2.5);st.add(dpost);
const corteza=label3d(['*SOLO CORTEZA','0,4 % DE LA MASA'],{w:6.4,h:2.2,px:120,accent:'#ff9a40'});corteza.position.set(-1.9,2.4,3.6);corteza.scale.setScalar(.6);st.add(corteza);
const hero=capataz();hero.g.position.set(0,.52,2);scene.add(hero.g);
// ---------- espacio: planeta hueco cortado (Halley 1692)
const SP=new THREE.Group();SP.position.set(600,0,0);scene.add(SP);
const shell=voxShell({n:5200,rad:10,layers:3,cut:[0,Math.PI/2]});SP.add(shell.group);
const in1=voxShell({n:2200,rad:6.4,layers:2,cut:[0,Math.PI/2],cols:[0xc9783a,0xa85e2c],land:false});SP.add(in1.group);
const in2=voxShell({n:900,rad:3.6,layers:2,cut:[0,Math.PI/2],cols:[0xd9a548,0xb88a36],land:false});SP.add(in2.group);
const core=new THREE.Mesh(new THREE.IcosahedronGeometry(1.4,1),new THREE.MeshBasicMaterial({color:0xffe08a,toneMapped:false}));SP.add(core);const cg=glow(0xffb040,7,.9);SP.add(cg);
const lHal=label3d(['*HALLEY · 1692'],{w:7,h:1.5,px:120,sprite:true});SP.add(lHal);
const lMas=label3d(['TODA LA MASA','*EN LA CORTEZA'],{w:9,h:2.6,px:110,sprite:true,accent:'#4de3ff'});SP.add(lMas);
const gS=new THREE.DirectionalLight(0xffffff,0);gS.position.set(570,20,60);gS.target.position.set(600,0,0);scene.add(gS,gS.target);const gFill=new THREE.PointLight(0xffb060,0,40,1.2);gFill.position.set(600,0,0);scene.add(gFill);
const ST=stars(scene,1400);
// ---------- interior hueco: cueva esférica, sol interior y capataz flotando
const IN=new THREE.Group();IN.position.set(1200,0,0);scene.add(IN);
const caveTex=pixTex(256,128,(g,w,h)=>{const q=mk(31);g.fillStyle='#3e2a1c';g.fillRect(0,0,w,h);for(let i=0;i<1600;i++){g.fillStyle=['#352418','#4d3626','#2a1c12','#5a4030'][Math.floor(q()*4)];g.fillRect(Math.floor(q()*w/4)*4,Math.floor(q()*h/4)*4,4,4)}},[6,3]);
const cave=new THREE.Mesh(new THREE.SphereGeometry(40,48,32),new THREE.MeshStandardMaterial({map:caveTex,side:THREE.BackSide,roughness:1}));IN.add(cave);
const isun=new THREE.Mesh(new THREE.IcosahedronGeometry(3,1),new THREE.MeshBasicMaterial({color:0xffd27a,toneMapped:false}));isun.position.set(0,0,-14);IN.add(isun);const ig=glow(0xffa040,22,.8);ig.position.copy(isun.position);IN.add(ig);
const iL=new THREE.PointLight(0xffd8a0,0,140,1);iL.position.set(1200,0,-14);scene.add(iL);const iA=new THREE.AmbientLight(0x6a5040,0);scene.add(iA);
const rocks=puffs(scene,70,.6,0x9a7454,{opacity:1});const rp=[];for(let i=0;i<70;i++)rp.push([(R()<.5?-1:1)*(6+R()*12),(R()-.5)*40,(R()-.5)*20-8,R()*6.28,.4+R()*.9]);
const lFlo=label3d(['*SIN ARRIBA','NI ABAJO'],{w:7,h:2.4,px:130,sprite:true,accent:'#4de3ff'});IN.add(lFlo);
const lNew=label3d(['NEWTON · 1687'],{w:6,h:1.3,px:110,sprite:true});IN.add(lNew);
const kgAt=(s,lt,d)=>s==='h'?80:s==='s2'?80:s==='s4'?80-79.68*ss(d*.35,d*.7,lt):null;
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],k=ss(0,d,lt),m=mouthAt(t);let p,q,bg=SKY;
 const onP=s==='h'||s==='s2'||s==='s4'||s==='cta';st.visible=onP;hero.g.visible=onP||s==='s3';SP.visible=s==='s1';IN.visible=s==='s3';rocks.m.visible=s==='s3';
 ST.visible=s==='s1';ST.position.set(600,0,0);iL.intensity=s==='s3'?260:0;iA.intensity=s==='s3'?1.2:0;gFill.intensity=s==='s1'?60:0;
 if(onP){const kg=kgAt(s,lt,d);disp.set(kg==null?['¿Y TÚ?']:kg<1?[`*${Math.round(kg*1000)} g`]:[`*${Math.round(kg)} kg`]);corteza.visible=s==='s4'&&lt>d*.2;
  const op=s==='h'?ss(.8,2.2,lt):1;hole.scale.setScalar(.01+.99*op);holeGlow.material.opacity=.7*op*(.8+.2*Math.sin(t*6));
  // en s4 pesa casi nada: rebota muy alto al final
  let jy=0;if(s==='s4'&&lt>d*.72){const u=((lt-d*.72)/2.4)%1;jy=4*u*(1-u)*6}
  hero.g.position.set(0,.52+jy,2);hero.g.rotation.set(0,0,0);hero.g.scale.setScalar(1);
  hero.pose(t,m,{wave:s==='cta'?1:0,armsUp:jy>0?.7:s==='s2'?.25:0,look:s==='h'?-.5:s==='cta'?0:.25,point:s==='h'&&lt>1.2?.6:0});
  if(s==='h'){p=V3(.2,6.2-k*1.0,29-k*3);q=V3(-.4,3.5,1.8)}
  else if(s==='s2'){p=V3(2.2,3.6,25-k*1.5);q=V3(1.8,4.6,1)}
  else if(s==='s4'){p=V3(0,4.2+jy*.5,30);q=V3(0,6+jy*.6,1)}
  else{p=V3(1.6,2.1,31+k*1.5);q=V3(1.6,2.1+k*.2,0)}// CTA: el capataz por encima del botón de seguir
  S.target.position.copy(q);S.position.set(q.x-16,34,q.z+18);S.target.updateMatrixWorld();S.intensity=2.6;gS.intensity=0;hemi.intensity=1.4}
 else if(s==='s1'){bg=SPACE;S.intensity=0;hemi.intensity=.35;gS.intensity=3.0;
  const rot=-Math.PI/4+.55+Math.sin(t*.25)*.2;[shell,in1,in2].forEach((o,i)=>o.group.rotation.y=rot*(1+i*.15));
  const op2=ss(d*.35,d*.6,lt);in1.group.visible=in2.group.visible=lt>d*.3;in1.group.scale.setScalar(.2+.8*op2);in2.group.scale.setScalar(.2+.8*ss(d*.45,d*.7,lt));
  lHal.position.set(0,-12.2,6);lHal.scale.set(10,2.2,1);lHal.visible=lt>.6;lMas.visible=false;core.rotation.y=t;
  p=V3(600+Math.sin(t*.2)*3,6+k*2,68-k*9);q=V3(600,2,0)}
 else{// s3: dentro del hueco, el capataz flota y gira
  bg=CAVE;S.intensity=0;hemi.intensity=.2;
  const fx=1200+Math.sin(t*.7)*.8,fy=-1.5+Math.sin(t*1.1)*.6;hero.g.position.set(fx,fy,0);hero.g.rotation.set(t*.45,t*.3,t*.2+.4);hero.pose(t,m,{armsUp:.6+.3*Math.sin(t*2),look:.2});
  for(let i=0;i<70;i++){const[x,y,z,a,sz]=rp[i];rocks.set(i,1200+x+Math.sin(t*.3+a)*.6,y+Math.cos(t*.25+a)*.8,z,sz,t*.4+a)}rocks.done();
  lFlo.visible=lt>d*.35;lFlo.position.set(0,-7,4);lFlo.scale.set(8,2.7,1);lNew.visible=lt>d*.6;lNew.position.set(0,-9.6,4);lNew.scale.set(6.5,1.4,1);
  isun.rotation.y=t;ig.material.opacity=.7+.1*Math.sin(t*3);
  p=V3(1200+Math.sin(t*.3)*1.5,-.5+k*1.5,34-k*4);q=V3(1200,-1.8,0)}
 scene.background=bg;const sp=s==='s1'||s==='s3';scene.fog.near=sp?1e4:60;scene.fog.far=sp?2e4:190;
 cam.position.copy(p);cam.lookAt(q);r.render(scene,cam)};
window.ready=true;
