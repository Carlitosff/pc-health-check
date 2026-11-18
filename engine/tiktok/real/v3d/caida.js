// ¿Y si la Tierra se parara en su órbita? (2604). Serie ¿QUÉ PASARÍA SI…? Parte 15.
// Reutilizable: CAÍDA LIBRE RADIAL real hacia el Sol (r(t) por la solución exacta de la cicloide radial, misma fórmula que el assert de Python),
// contador de DÍAS integrado que sigue a la Tierra, órbitas de Venus y Mercurio como aros de luz que se iluminan al cruzarlas, flecha de velocidad
// orbital que se encoge al frenar, estela de caída, Sol de cubos que crece al acercarnos y destello final. La capataz en su isla flotante (cta).
import {THREE,J,mk,ss,V3,clamp,stage,box,glow,capataz,segAt,mouthAt,label3d,stars,voxGlobe} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x02030a,fog:null,exposure:1.05});cam.far=3000;cam.updateProjectionMatrix();const R=mk(2604);
scene.add(new THREE.HemisphereLight(0xcfe0ff,0x202030,.25));
stars(scene,2200,{r0:900,r1:1100,size:2.2});
const AU=70,TFF=64.569;          // días de caída desde 1 UA (cálculo propio, igual que en serie_caida.py)
// r(día) en UA: r = cos²η, t = TFF·(2/π)(η + sinη·cosη)
const rOf=d=>{if(d<=0)return 1;if(d>=TFF)return 0;let lo=0,hi=Math.PI/2;for(let i=0;i<50;i++){const e=(lo+hi)/2;(TFF*2/Math.PI*(e+Math.sin(e)*Math.cos(e))<d)?lo=e:hi=e}const e=(lo+hi)/2;return Math.cos(e)**2};
// ---------- SOL de cubos (origen)
const SUN=new THREE.Group();scene.add(SUN);const SR=9;
SUN.add(new THREE.Mesh(new THREE.SphereGeometry(SR*.97,48,32),new THREE.MeshBasicMaterial({color:0xffb030,toneMapped:false})));
const NG=1100;const gran=new THREE.InstancedMesh(new THREE.BoxGeometry(1,1,1),new THREE.MeshBasicMaterial({toneMapped:false}),NG);gran.frustumCulled=false;SUN.add(gran);
const GD=[];for(let i=0;i<NG;i++){const y=1-2*(i+.5)/NG,rr=Math.sqrt(1-y*y),a=i*Math.PI*(3-Math.sqrt(5));GD.push([Math.cos(a)*rr,y,Math.sin(a)*rr,R()*6.28])}
const gO=new THREE.Object3D(),gC=new THREE.Color();
const updSun=t=>{for(let i=0;i<NG;i++){const[x,y,z,ph]=GD[i];const b=.5+.5*Math.sin(t*1.7+ph*3);gO.position.set(x*SR,y*SR,z*SR);gO.lookAt(0,0,0);gO.scale.setScalar(.75+.55*b);gO.updateMatrix();gran.setMatrixAt(i,gO.matrix);gC.setRGB(1,.62+.33*b,.18+.3*b);gran.setColorAt(i,gC)}gran.instanceMatrix.needsUpdate=true;gran.instanceColor.needsUpdate=true};
const cor1=glow(0xffc050,55,.85),cor2=glow(0xff7a20,100,.45);SUN.add(cor1,cor2);SUN.add(new THREE.PointLight(0xfff0d8,9,0,0));
// ---------- órbitas (aros verticales, en el plano de la cámara, centrados en el Sol)
const ring=(rad,col,op)=>{const m=new THREE.Mesh(new THREE.TorusGeometry(rad,.32,8,240),new THREE.MeshBasicMaterial({color:col,transparent:true,opacity:op,toneMapped:false}));scene.add(m);return m};
const oE=ring(AU,0x4da8ff,.35),oV=ring(AU*.723,0xffb35a,.3),oM=ring(AU*.387,0xc8c8c8,.3);
const lV=label3d(['ÓRBITA DE VENUS','*DÍA 41'],{w:13,h:4.4,px:110,sprite:true,accent:'#ffb35a'});scene.add(lV);
const lM=label3d(['ÓRBITA DE MERCURIO','*DÍA 57'],{w:14,h:4.4,px:110,sprite:true,accent:'#e0e0e0'});scene.add(lM);
// ---------- TIERRA
const EG=new THREE.Group();scene.add(EG);const glb=voxGlobe(6000,4,{cube:.32});EG.add(glb.group);const atm=glow(0x6ab8ff,12,.35);EG.add(atm);
const day=label3d(['DÍA','*0'],{w:9.5,h:6,px:150,sprite:true});scene.add(day);
// flecha de velocidad orbital (s1) y flecha de caída
const arrow=(col)=>{const g=new THREE.Group();const sh=box(1,1,1,col,.05,{emissive:col,emissiveIntensity:.7});const hd=new THREE.Mesh(new THREE.ConeGeometry(1.5,3,4),new THREE.MeshStandardMaterial({color:col,emissive:col,emissiveIntensity:.7}));g.add(sh,hd);g.userData={sh,hd};scene.add(g);return g};
const setArrow=(g,from,dir,len)=>{const{sh,hd}=g.userData;g.visible=len>.3;g.position.copy(from);g.lookAt(from.clone().add(dir));sh.scale.set(.7,.7,Math.max(.01,len));sh.position.set(0,0,len/2);hd.rotation.x=Math.PI/2;hd.position.set(0,0,len+1.4)};
const aV=arrow(0x4de3ff),aF=arrow(0xff5a3a);
const vlab=label3d(['*30 KM/S','DE LADO'],{w:8,h:3.6,px:110,sprite:true,accent:'#4de3ff'});scene.add(vlab);
// estela de caída
const NT=60;const trail=new THREE.InstancedMesh(new THREE.BoxGeometry(.8,.8,.8),new THREE.MeshBasicMaterial({color:0x8fd0ff,transparent:true,opacity:.6,toneMapped:false}),NT);trail.frustumCulled=false;scene.add(trail);
const flash=new THREE.Mesh(new THREE.PlaneGeometry(400,400),new THREE.MeshBasicMaterial({color:0xfff2d0,transparent:true,opacity:0,depthTest:false,toneMapped:false}));scene.add(flash);
// ---------- capataz en su isla (cta)
const ISL=new THREE.Group();scene.add(ISL);{const b=box(7,1.6,6,0x6a8a4a,.15);b.position.y=-.8;ISL.add(b);const b2=box(5,2,4.4,0x7a5a3a,.15);b2.position.y=-2.4;ISL.add(b2);const b3=box(2.6,1.6,2.4,0x6a4a2e,.15);b3.position.y=-4;ISL.add(b3)}
const hero=capataz();ISL.add(hero.g);const islL=new THREE.DirectionalLight(0xfff0d8,2.4);islL.position.set(0,60,20);islL.target=ISL;scene.add(islL);
// días en función del tiempo del vídeo: s2 0→30, s3 30→58, s4 58→65 (choque ~1 s antes del final de s4)
const dayAt=t=>{const[a2,b2]=TL.s2,[a3,b3]=TL.s3,[a4,b4]=TL.s4;if(t<a2)return 0;if(t<b2)return 30*ss(a2+.3,b2,t)**1.15;if(t<b3)return 30+28*ss(a3,b3,t);if(t<b4)return 58+(TFF-58)*Math.min(1,(t-a4)/Math.max(.5,b4-a4-1.2));return TFF};
const th0=-Math.PI/2;   // la Tierra abajo del Sol
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],k=ss(0,d,lt),m=mouthAt(t);
 updSun(t);SUN.rotation.y=t*.05;
 const D=dayAt(t),rr=rOf(D);
 // s1: la Tierra viene recorriendo su órbita y frena hasta quedarse quieta
 let ang=th0;if(s==='h')ang=th0-.22+lt*.035;else if(s==='s1')ang=th0-.22+.035*TL.h[1]+(.22-.035*TL.h[1])*ss(0,d*.75,lt);
 const ex=Math.cos(ang)*AU*rr,ey=Math.sin(ang)*AU*rr;EG.position.set(ex,ey,0);glb.group.rotation.y=t*.3;glb.group.rotation.z=.41;
 const big=1/Math.max(rr,.12);SUN.scale.setScalar(1);
 day.set(['DÍA',`*${Math.floor(D)}`]);day.visible=s==='s2'||s==='s3'||s==='s4';day.position.set(ex+(s==='s4'?4.6:6.8),ey+(s==='s4'?4.8:1.2),3);
 // flechas
 const vel=s==='h'?1:s==='s1'?1-ss(d*.1,d*.75,lt):0;const EP=EG.position.clone();
 setArrow(aV,EP.clone().add(V3(5,0,0)),V3(1,0,0),11*vel);vlab.visible=vel>.3;vlab.position.set(ex+7,ey+5,2);vlab.material.opacity=vel;
 const fall=s==='s1'?ss(d*.6,d*.9,lt):(s==='s2'?1:0);setArrow(aF,EP.clone().add(V3(0,5,0)),V3(0,1,0),7*fall);
 // estela
 for(let i=0;i<NT;i++){const dd=Math.max(0,D-i*.5);const r2=rOf(dd);gO.position.set(0,-AU*r2,0);gO.rotation.set(0,0,0);gO.scale.setScalar(D>0&&i*.5<D?(1-i/NT)*1.4:0.001);gO.updateMatrix();trail.setMatrixAt(i,gO.matrix)}trail.instanceMatrix.needsUpdate=true;trail.visible=D>.5&&s!=='cta';
 // órbitas: se encienden al cruzarlas
 const hitV=ss(40.5,41.5,D)*(1-ss(46,50,D)),hitM=ss(56.5,57.5,D)*(1-ss(61,63,D));
 oV.material.opacity=.3+.65*hitV;oM.material.opacity=.3+.65*hitM;oV.scale.z=oM.scale.z=1;
 lV.visible=hitV>.01;lV.position.set(-5.4,-AU*.723+2.5,3);lV.material.opacity=hitV;lM.visible=hitM>.01;lM.position.set(-6.5,-AU*.387+2.5,3);lM.material.opacity=hitM;
 // choque
 flash.position.copy(cam.position).add(cam.getWorldDirection(V3()).multiplyScalar(5));flash.lookAt(cam.position);
 const fl=s==='s4'?ss(d-1.25,d-.85,lt)*(1-ss(d-.4,d,lt)*.6):0;flash.material.opacity=fl;EG.visible=!(s==='s4'&&lt>d-1.0)&&s!=='cta';
 // isla
 ISL.visible=s==='cta';ISL.position.set(-3,-AU*.55,0);ISL.rotation.y=.5;hero.pose(t,m*.25,{wave:s==='cta'?1:0,look:.4});
 let p,q;
 if(s==='h'){p=V3(4-k*2,-AU*.6,165-k*15);q=V3(0,-AU*.5+1,0)}
 else if(s==='s1'){p=V3(ex+10,ey-6,62-k*8);q=V3(ex+3,ey+12,0)}
 else if(s==='s2'){p=V3(ex+14,ey-18,64);q=V3(ex+2,ey+14,0)}
 else if(s==='s3'){p=V3(ex+16,ey-20,70-k*6);q=V3(ex,ey+12,0)}
 else if(s==='s4'){p=V3(ex+10,ey-22,50);q=V3(ex*.4,ey*.4+6,0)}
 else{p=V3(-1-k*2,-AU*.55+2,34-k*3);q=V3(-3,-AU*.55+1.2,0)}
 cam.position.copy(p);cam.lookAt(q);r.render(scene,cam)};
window.ready=true;
