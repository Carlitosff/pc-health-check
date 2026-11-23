// Mito: '¿el queso antes de dormir da pesadillas?' (3103). British Cheese Board, 2005: 200 voluntarios, 20 g de queso 30 min antes de dormir, una semana;
// ninguno tuvo pesadillas; 72 % durmió muy bien; con Stilton, 75 % de hombres y 85 % de mujeres con sueños raros (Scotsman; Live Science: sin grupo de control).
// Reutilizable: DORMITORIO de noche con mesilla y queso en plato (cheese), LABORATORIO con 200 voluntarios y su cubito de queso, barras 3D,
// ISLA DE SUEÑO RARO con gatitos guerreros (kitten) y cocodrilo vegetariano (croc) y quesos azules que orbitan.
import {THREE,J,mk,ss,V3,clamp,stage,sun,box,glow,capataz,segAt,mouthAt,label3d,bed,lieDown,crowd,pixTex,cheese,kitten,croc,dreamIsle,stars} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x0d1430,fog:[0x0d1430,70,190],exposure:1.12});const R=mk(3103);
const hemi=new THREE.HemisphereLight(0x8fa4e0,0x241a2a,.85);scene.add(hemi);const S=sun(scene,{pos:[-12,26,16],span:26,color:0xb8c8ff,power:1.0});
const lamp=new THREE.PointLight(0xffc880,70,30,1.5);lamp.position.set(5.2,6,-1);scene.add(lamp);
// ---------- DORMITORIO
const BR=new THREE.Group();scene.add(BR);
const fl=new THREE.Mesh(new THREE.PlaneGeometry(90,90),new THREE.MeshStandardMaterial({color:0x5a4030,roughness:.9}));fl.rotation.x=-Math.PI/2;fl.receiveShadow=true;BR.add(fl);
for(let i=0;i<18;i++){const p=box(2.4,.05,90,i%2?0x6a4a36:0x5e4232,.01);p.position.set(-21+i*2.5,.02,0);BR.add(p)}
const wall=box(70,34,.6,0x27315a,.05);wall.position.set(0,17,-9);BR.add(wall);
const win=new THREE.Group();{const f=box(6,5,.5,0x8a6a4a,.08);win.add(f);const gl=box(5.2,4.2,.3,0x0a1030,.02,{emissive:0x101848,emissiveIntensity:.6});gl.position.z=.12;win.add(gl);const moon=new THREE.Mesh(new THREE.SphereGeometry(.8,20,14),new THREE.MeshBasicMaterial({color:0xfff4c8,toneMapped:false}));moon.position.set(1.2,1.1,.3);win.add(moon);const mg=glow(0xfff0b0,4,.6);mg.position.set(1.2,1.1,.4);win.add(mg)}
win.position.set(-6,8,-8.6);BR.add(win);
const B=bed(0x3a6fd8);B.position.set(0,0,-4);BR.add(B);const sleeper=capataz();sleeper.hat.forEach(h=>h.visible=false);const bl=lieDown(sleeper,B,0x3a6fd8);
// mesilla con lámpara y plato de queso
const NS=new THREE.Group();NS.position.set(4.4,0,-6);BR.add(NS);{const t=box(2.4,2.4,2.2,0x8a5a3a,.06);t.position.y=1.2;NS.add(t);const dr=box(1.8,.7,.1,0x9d6a46,.03);dr.position.set(0,1.4,1.12);NS.add(dr);
 const lb=box(.6,1.6,.6,0xd8d0c0,.05);lb.position.set(-.6,3.2,-.4);NS.add(lb);const sh=new THREE.Mesh(new THREE.CylinderGeometry(.5,.9,1,16),new THREE.MeshStandardMaterial({color:0xffe0a0,emissive:0xffc060,emissiveIntensity:.8}));sh.position.set(-.6,4.3,-.4);NS.add(sh)}
const plate=new THREE.Mesh(new THREE.CylinderGeometry(.85,.85,.08,28),new THREE.MeshStandardMaterial({color:0xf4f4f0,roughness:.3}));plate.position.set(.4,2.45,.3);NS.add(plate);
const CH=cheese(.42);CH.position.set(.4,2.5,.3);CH.rotation.y=-.5;NS.add(CH);
const qmark=label3d(['*?'],{w:2.2,h:2.2,px:300,sprite:true,bg:null,accent:'#ff4a6a'});BR.add(qmark);
// barras 3D (s2)
const BARS=new THREE.Group();BR.add(BARS);BARS.position.set(0,0,4);
const barN=box(2.4,1,2.4,0xff4a6a,.08,{emissive:0x5a0a1a,emissiveIntensity:.4});const barG=box(2.4,1,2.4,0x4ade80,.08,{emissive:0x0a5a2a,emissiveIntensity:.35});barN.position.x=-2.2;barG.position.x=2.2;BARS.add(barN,barG);
const lN=label3d(['PESADILLAS','*0'],{w:4.0,h:2.6,px:130,sprite:true,accent:'#ff4a6a'});const lG=label3d(['DURMIERON BIEN','*72 %'],{w:4.4,h:2.6,px:120,sprite:true,accent:'#4ade80'});BARS.add(lN,lG);
const zz=[0,1,2].map(i=>{const z=label3d(['Z'],{w:1.2,h:1.2,px:260,sprite:true,bg:null,accent:'#9ad8ff',fg:'#9ad8ff'});BR.add(z);return z});
// isla de sueño raro (s3) sobre la cama
const ISL=dreamIsle(false,8);ISL.userData.y=13.5;ISL.position.set(0,13.5,-4);ISL.scale.setScalar(1.05);BR.add(ISL);
const cats=[0xff9a3a,0xf2f2f2,0x6a6a72].map((c,i)=>{const k=kitten(c);k.scale.setScalar(.75);k.userData.y0=.5;k.position.set(-2.4+i*1.4,.5,1.2-i*.2);k.rotation.y=-.2;ISL.add(k);return k});
const CR=croc();CR.scale.setScalar(.6);CR.position.set(.6,.62,-1.4);CR.rotation.y=Math.PI*.85;ISL.add(CR);
const blues=[0,1,2,3].map(i=>{const c=cheese(.5,{blue:true});ISL.add(c);return c});
const bub=[0,1,2].map(i=>{const m=new THREE.Mesh(new THREE.SphereGeometry(.25+i*.2,14,10),new THREE.MeshStandardMaterial({color:0xffffff,emissive:0xffffff,emissiveIntensity:.35,transparent:true,opacity:.85}));BR.add(m);return m});
const lBlue=label3d(['QUESO AZUL','*SUEÑOS RARÍSIMOS'],{w:7.5,h:2.6,px:110,sprite:true,accent:'#6aa8ff'});BR.add(lBlue);
const hero=capataz();hero.g.position.set(-5.6,0,1);hero.g.rotation.y=.35;BR.add(hero.g);
const handCh=cheese(.22);handCh.position.set(0,-1.5,.35);hero.armR.add(handCh);
// ---------- LABORATORIO a x=300 (s1, s4)
const L=new THREE.Group();L.position.set(300,0,0);scene.add(L);
const lf=new THREE.Mesh(new THREE.PlaneGeometry(120,80),new THREE.MeshStandardMaterial({map:pixTex(32,32,(g,w,h)=>{g.fillStyle='#dfe6ec';g.fillRect(0,0,w,h);g.strokeStyle='#c4cdd6';g.strokeRect(0,0,w,h)},[30,20]),roughness:.7}));lf.rotation.x=-Math.PI/2;lf.receiveShadow=true;L.add(lf);
const lw=new THREE.Mesh(new THREE.PlaneGeometry(120,40),new THREE.MeshStandardMaterial({color:0xeef3f6,roughness:.9}));lw.position.set(0,20,-22);L.add(lw);
const N=200,CW=crowd(scene,N,{s:1,seed:31});const cP=[];for(let i=0;i<N;i++){const row=Math.floor(i/20),col=i%20;cP.push([300-23.75+col*2.5,0,-19+row*2.7])}
const cubes=new THREE.InstancedMesh(new THREE.BoxGeometry(.5,.4,.5),new THREE.MeshStandardMaterial({color:0xffc83a,roughness:.5}),N);cubes.frustumCulled=false;scene.add(cubes);const O=new THREE.Object3D();
const banner=label3d(['CONSEJO BRITÁNICO DEL QUESO','*2005'],{w:15,h:3,px:86,accent:'#ffc23a'});banner.position.set(0,15.5,-21.8);L.add(banner);
const n200=label3d(['*200 PERSONAS','20 g · 30 MIN ANTES · 1 SEMANA'],{w:12,h:3,px:100,sprite:true,accent:'#ffc23a'});scene.add(n200);
const pay=label3d(['LO PAGARON','*LOS QUESEROS'],{w:5.6,h:3,px:120,sprite:true,accent:'#ffc23a'});scene.add(pay);
const ctl=label3d(['GRUPO SIN QUESO','*NO HUBO'],{w:5.6,h:3,px:110,sprite:true,accent:'#ff4a6a'});scene.add(ctl);
const BIG=cheese(2.2);BIG.position.set(0,0,-6);BIG.rotation.y=.4;L.add(BIG);
const coins=[];for(let i=0;i<14;i++){const c=new THREE.Mesh(new THREE.CylinderGeometry(.45,.45,.1,20),new THREE.MeshStandardMaterial({color:0xffd23a,emissive:0xb88a10,emissiveIntensity:.6,metalness:.2,roughness:.4}));c.rotation.x=Math.PI/2;scene.add(c);coins.push(c)}
const ST=stars(scene,600,{r0:120,r1:150,size:.8});ST.position.set(0,0,-4);
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],k=ss(0,d,lt),m=mouthAt(t);let p,q;
 const inLab=s==='s1'||s==='s4';BR.visible=!inLab;L.visible=inLab;ST.visible=!inLab;
 CW.body.visible=CW.head.visible=cubes.visible=s==='s1';banner.visible=false;n200.visible=s==='s1'&&lt>1.0;pay.visible=s==='s4'&&lt>.6;ctl.visible=s==='s4'&&lt>d*.5;coins.forEach(c=>c.visible=s==='s4');
 if(!inLab){scene.background=new THREE.Color(0x0d1430);hemi.intensity=.85;S.intensity=1.0;lamp.intensity=70;
  ISL.visible=s==='s3';ISL.tick(t);cats.forEach((c,i)=>{c.tick(t,i*1.3);c.position.x=-2.4+i*1.4+Math.sin(t*.8)*.8});CR.tick(t);
  blues.forEach((c,i)=>{const a=t*.9+i*Math.PI/2;c.position.set(Math.cos(a)*5.2,3.2+Math.sin(t*1.4+i)*.6,Math.sin(a)*3.4);c.rotation.set(t*.7+i,t*.5,0)});
  bub.forEach((b,i)=>{b.visible=s==='s3';b.position.set(Math.sin(t*1.3+i)*.2,4.4+i*2.6,-5.2)});lBlue.visible=s==='s3'&&lt>.7;lBlue.position.set(0,9.2,0);
  bl.blanket.scale.y=1+.06*Math.sin(t*1.6);sleeper.eyes.forEach(e=>e.scale.y=.1);
  qmark.visible=s==='h';qmark.position.set(3.2,4.6+Math.sin(t*2)*.2,-5.0);qmark.material.opacity=ss(.3,.9,lt);
  const bh=s==='s2'?ss(.8,2.4,lt):0;barN.scale.y=.06;barN.position.y=.03;barG.scale.y=Math.max(.01,4.6*bh);barG.position.y=barG.scale.y/2;BARS.visible=s==='s2';
  lN.position.set(-2.2,2.4,0);lG.position.set(2.2,barG.scale.y+1.8,0);lN.material.opacity=ss(.4,1.0,lt);lG.material.opacity=ss(1.6,2.4,lt);
  zz.forEach((z,i)=>{z.visible=s==='s2'||s==='h';const f=(t*.45+i/3)%1;z.position.set(-.6+f*1.6,3.6+f*4,-6.5);z.material.opacity=Math.sin(f*Math.PI)});
  hero.g.visible=s==='cta';const eat=s==='cta'?ss(.5,1.2,lt)*(1-ss(2.0,2.6,lt)):0;hero.pose(t,eat>.5?0:m,{wave:s==='cta'&&lt>2.6?1:0,look:.15});if(eat>0){hero.armR.rotation.x=-eat*2.1;hero.armR.rotation.z=.14+eat*.35}
  CH.visible=s!=='cta';
  if(s==='h'){p=V3(7.5-k*1.2,6.4,8-k*1.5);q=V3(3.0,2.8,-5.2)}
  else if(s==='s2'){p=V3(Math.sin(t*.3)*.8,8.5,38-k*3);q=V3(0,6.4,0)}
  else if(s==='s3'){p=V3(Math.sin(t*.25)*1.5,13+k,25-k*3);q=V3(0,15.2,-4)}
  else{p=V3(-2.5,6,22);q=V3(-2.5,3.4,-2)}}
 else{scene.background=new THREE.Color(0xdfe6ec);hemi.intensity=1.5;S.intensity=1.8;lamp.intensity=0;
  for(let i=0;i<N;i++){const[x,y,z]=cP[i];const a=s==='s1'?ss(i*.006,i*.006+.4,lt):1;CW.set(i,x,y+(1-a)*7,z,a+.001,Math.sin(t+i)*.2);
   O.position.set(x+.75,y+1.75+Math.sin(t*2+i)*.05,z+.55);O.rotation.set(0,t+i,0);O.scale.setScalar(a+.001);O.updateMatrix();cubes.setMatrixAt(i,O.matrix)}CW.done();cubes.instanceMatrix.needsUpdate=true;
  n200.position.set(300,10,4);BIG.visible=s==='s4';BIG.rotation.y=.4+t*.3;
  coins.forEach((c,i)=>{const f=((lt*.6+i/14)%1);c.position.set(300+Math.sin(i*2.3)*5,16-f*16,-4+Math.cos(i*1.7)*2);c.rotation.z=t*3+i});
  pay.position.set(300,7.6,2);ctl.position.set(300,4.4,2);
  if(s==='s1'){p=V3(300+Math.sin(t*.25)*2,22-k*3,58-k*6);q=V3(300,3,-8)}
  else{p=V3(300+Math.sin(t*.3)*1.5,7,30-k*3);q=V3(300,6.5,-4)}}
 cam.position.copy(p);cam.lookAt(q);r.render(scene,cam)};
window.ready=true;
