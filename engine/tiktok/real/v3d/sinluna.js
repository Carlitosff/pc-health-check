// Serie P23 '¿Y si la Tierra se quedara sin Luna?' (3404). Fuentes en serie_sinluna.py.
// Reutilizable: PUERTO DE NOCHE con mar de bloques, barcas que suben y bajan, regla de marea en el muelle (tideAt) y Luna que se apaga;
// PLAZA DE NOCHE (de doslunas.js) con luz de luna regulable; GLOBO con EJE que se bambolea (wob) frente al Sol y medidor de grados.
import {THREE,J,mk,ss,V3,clamp,stage,box,glow,capataz,segAt,mouthAt,puffs,stars,voxGlobe,voxMoon,ruler,label3d} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x0a1430,exposure:1.2});cam.far=2500;cam.updateProjectionMatrix();const R=mk(3404);
const hemi=new THREE.HemisphereLight(0x6f86c8,0x1a1420,.55);scene.add(hemi);
const moonL=new THREE.DirectionalLight(0xc8d8ff,.9);moonL.position.set(-20,60,-60);moonL.castShadow=true;moonL.shadow.mapSize.set(1024,1024);{const c=moonL.shadow.camera;c.left=-50;c.right=50;c.top=50;c.bottom=-50;c.far=220}scene.add(moonL);
const ST=stars(scene,1600,{r0:500,r1:700,size:1.5});
// ---------- PUERTO (origen)
const PT=new THREE.Group();scene.add(PT);
const sand=box(160,.6,40,0xb8a070,.02);sand.position.set(0,.2,30);sand.receiveShadow=true;PT.add(sand);
const SEA=new THREE.Mesh(new THREE.BoxGeometry(260,6,160),new THREE.MeshStandardMaterial({color:0x1a4a8a,roughness:.25,metalness:.2,emissive:0x0a2050,emissiveIntensity:.5}));SEA.position.set(0,-3,-70);PT.add(SEA);
const WV=puffs(scene,220,.45,0x9fd0ff,{opacity:.55});
const pier=box(5,.6,34,0x6a4a2a,.04);pier.position.set(22,3.6,-7);PT.add(pier);for(let i=0;i<8;i++)[-2.2,2.2].forEach(x=>{const p=box(.6,10,.6,0x4a3220,.05);p.position.set(22+x,-1.4,-22+i*4.4);PT.add(p)});const post=box(.8,9,.8,0x4a3220,.05);post.position.set(2.6,1,-4);PT.add(post);
const RUL=ruler(6,{step:.5,every:2,unit:50,label:'cm',col:0xffd23a,ls:1.2});RUL.position.set(3.1,-3,-3.5);PT.add(RUL);
const lamp=box(.4,4,.4,0x22252e,.05);lamp.position.set(22,5.9,8);PT.add(lamp);const lb=box(1,.6,1,0xfff0c0,.1,{emissive:0xffd890,emissiveIntensity:1.5});lb.position.set(22,8.1,8);PT.add(lb);const lg=glow(0xffd890,6,.55);lg.position.set(22,8.1,8);PT.add(lg);
const boats=[[-8,-14,0xd8342a],[-16,-26,0x2a7de1],[0,-30,0xf2c230]].map(([x,z,c],i)=>{const g=new THREE.Group();const h=box(5,1.2,2.2,c,.3);h.position.y=.4;g.add(h);const d=box(4.4,.2,1.8,0xf2efe8,.03);d.position.y=1.05;g.add(d);const m=box(.2,5,.2,0xe8e0d0,.02);m.position.set(.4,3.4,0);g.add(m);const s=box(.08,3.4,2.4,0xf4f2ec,.02);s.position.set(-.6,3.6,0);s.rotation.y=Math.PI/2;g.add(s);g.position.set(x,0,z);PT.add(g);return g});
const MO=voxMoon(4200,8,{cube:.55,seed:3,emissive:1.0});MO.group.position.set(-6,34,-150);PT.add(MO.group);const mh=glow(0xdfe8ff,60,.45);mh.position.copy(MO.group.position);PT.add(mh);
const refl=[];for(let i=0;i<10;i++){const g=glow(0xdfe8ff,6-i*.3,.35);g.position.set(-5+Math.sin(i)*.6,.25,-30-i*9);PT.add(g);refl.push(g)}
const flash=glow(0xffffff,10,0);flash.position.copy(MO.group.position);PT.add(flash);
const tideAt=(t,amp)=>amp*Math.sin(t*2.1);
const LVL=box(2.6,.22,.3,0x4de3ff,.05,{emissive:0x4de3ff,emissiveIntensity:2});LVL.position.set(3.4,0,-3.3);PT.add(LVL);const lvG=glow(0x4de3ff,4,.7);LVL.add(lvG);
const HI=box(2.6,.16,.3,0xff4a4a,.05,{emissive:0xff4a4a,emissiveIntensity:2});HI.position.set(3.4,1.6,-3.3);PT.add(HI);
// ---------- PLAZA DE NOCHE (x=-1000)
const PL=new THREE.Group();PL.position.set(-1000,0,0);scene.add(PL);
{const fl=box(90,.4,90,0x4a4e5e,.02);fl.position.y=-.2;fl.receiveShadow=true;PL.add(fl);for(let i=0;i<18;i++){const l=box(90,.03,.12,0x3a3e4c,.01);l.position.set(0,.02,-45+i*5);PL.add(l);const l2=box(.12,.03,90,0x3a3e4c,.01);l2.position.set(-45+i*5,.02,0);PL.add(l2)}
 const q=mk(9);for(let i=0;i<10;i++){const side=i%2?1:-1,h=10+q()*18,w=7+q()*4;const b=box(w,h,8,[0x2e3550,0x3a3248,0x283a48][i%3],.05);b.position.set(side*(20+q()*6),h/2,-40+i*7);b.castShadow=b.receiveShadow=true;PL.add(b);
  for(let f=1;f<h/3-1;f++)for(let k=0;k<2;k++)if(q()<.45){const wdw=box(1.2,1.4,.2,0xffd27a,.01,{emissive:0xffb84a,emissiveIntensity:1.1});wdw.position.set(b.position.x-w/4+k*w/2,f*3,-40+i*7+4.05);PL.add(wdw)}}
 [-9,9].forEach(x=>{const p=box(.4,6,.4,0x22252e,.05);p.position.set(x,3,8);PL.add(p);const l=box(1.1,.6,1.1,0xfff0c0,.1,{emissive:0xffd890,emissiveIntensity:1.4});l.position.set(x,6.2,8);PL.add(l);const g=glow(0xffd890,5,.5);g.position.set(x,6.2,8);PL.add(g)});
 const fnt=box(7,1.2,7,0x8a8e9e,.1);fnt.position.set(0,.6,-6);PL.add(fnt);const wat=box(6,.2,6,0x2a5a9a,.02,{emissive:0x0a2a5a,emissiveIntensity:.6});wat.position.set(0,1.15,-6);PL.add(wat)}
const PM=voxMoon(3500,9,{cube:.55,seed:1,emissive:.95});PM.group.position.set(-1000-4,32,-120);scene.add(PM.group);const ph=glow(0xdfe8ff,48,.4);ph.position.copy(PM.group.position);scene.add(ph);
const CAP=capataz();CAP.g.position.set(-1000+3.5,0,10);CAP.g.rotation.y=Math.PI*.1;scene.add(CAP.g);
// ---------- GLOBO (x=2000)
const GL=new THREE.Group();GL.position.set(2000,0,0);scene.add(GL);
const tilt=new THREE.Group();GL.add(tilt);const glb=voxGlobe(9000,10);tilt.add(glb.group);
const axis=new THREE.Mesh(new THREE.CylinderGeometry(.22,.22,30,12),new THREE.MeshBasicMaterial({color:0xffd23a,toneMapped:false}));tilt.add(axis);
const NP=new THREE.Mesh(new THREE.SphereGeometry(.7,12,8),new THREE.MeshBasicMaterial({color:0xff4a4a,toneMapped:false}));NP.position.y=15;tilt.add(NP);
const vert=new THREE.Mesh(new THREE.CylinderGeometry(.08,.08,32,8),new THREE.MeshBasicMaterial({color:0xffffff,transparent:true,opacity:.45,toneMapped:false}));GL.add(vert);
const ang=label3d(['*23°'],{w:7,h:2.8,px:170,sprite:true});ang.position.set(16,-9,0);GL.add(ang);
const gS=new THREE.DirectionalLight(0xfff4e0,3.4);gS.position.set(2000-560,0,0);gS.target=GL;scene.add(gS);
const sunB=new THREE.Mesh(new THREE.SphereGeometry(4,24,16),new THREE.MeshBasicMaterial({color:0xfff2b0,toneMapped:false}));sunB.position.set(2000-15,14,-30);scene.add(sunB);const sunG=glow(0xffd070,26,.9);sunG.position.copy(sunB.position);scene.add(sunG);
const ghostM=voxMoon(1500,2.7,{cube:.45,seed:5,emissive:.6});ghostM.group.position.set(2000+17,4,-6);scene.add(ghostM.group);
// bamboleo caótico determinista (deg): suma de senos, recortada a 0–88
const wob=t=>clamp(42+38*Math.sin(t*1.3)+14*Math.sin(t*2.9+1)+8*Math.sin(t*5.3+2),0,88);
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],k=ss(0,d,lt),m=mouthAt(t);let p,q;
 const port=s==='h'||s==='s1',plaza=s==='s2'||s==='cta',globe=s==='s3'||s==='s4';PT.visible=port;PL.visible=plaza;PM.group.visible=ph.visible=CAP.g.visible=plaza;GL.visible=sunB.visible=sunG.visible=globe;ghostM.group.visible=false;
 for(let i=0;i<220;i++)WV.set(i,0,-999,0,0);
 if(port){scene.background=new THREE.Color(0x0a1430);
  // Luna: en h se apaga a los ~2,4 s; en s1 vuelve como recuerdo en la primera mitad
  const gone=s==='h'?ss(2.2,2.9,lt):1;MO.group.scale.setScalar(Math.max(.001,1-gone));mh.material.opacity=.45*(1-gone);flash.material.opacity=s==='h'?Math.sin(clamp((lt-2.2)/.8)*Math.PI)*.9:0;flash.scale.setScalar(10+60*gone);
  refl.forEach(g=>g.material.opacity=.35*(1-gone));moonL.intensity=.3+.7*(1-gone);hemi.intensity=.35+.25*(1-gone);
  const amp=s==='h'?1.6:1.6-(1.6-.74)*ss(d*.45,d*.7,lt);const tide=tideAt(t,amp);SEA.position.y=-3+tide;LVL.position.y=tide;HI.position.y=s==='h'?1.6:1.6-(1.6-.74)*ss(d*.45,d*.9,lt);HI.visible=LVL.visible=s==='s1';if(s==='s1'){hemi.intensity=.75;moonL.intensity=.6}
  boats.forEach((b,i)=>{b.position.y=tide+Math.sin(t*1.7+i)*.12;b.rotation.z=Math.sin(t*1.3+i*2)*.06});
  for(let i=0;i<220;i++){const x=-60+(i*13.7)%120,z=-4-((i*7.3)%90);WV.set(i,x+Math.sin(t+i)*.6,tide+.08+Math.max(0,Math.sin(t*2+i*.7))*.18,z,.7+.5*Math.sin(t*1.5+i))}
  if(s==='h'){p=V3(-2+k*1.5,6.5,34-k*4);q=V3(-4,20-k*2,-90)}
  else{p=V3(-2+Math.sin(t*.4)*.6,4.2,24);q=V3(2,2.4,-8)}}
 else if(plaza){scene.background=new THREE.Color(0x07102a);
  const lit=s==='s2'?1-ss(d*.35,d*.6,lt):0;PM.group.scale.setScalar(Math.max(.001,lit));ph.material.opacity=.4*lit;moonL.intensity=.12+.9*lit;hemi.intensity=.18+.45*lit;ST.material.size=1.5+1.2*(1-lit);
  CAP.pose(t,s==='cta'?m:0,{wave:s==='cta'?1:0,look:.2});CAP.head.rotation.x=s==='cta'?-.1:-.45;
  if(s==='s2'){p=V3(-1000+3+Math.sin(t*.3),3.2+k*.8,30);q=V3(-1000+2.4,13,-40)}else{hemi.intensity=.55;moonL.intensity=.35;p=V3(-1000+3.5+k*1.2,7,34-k*2);q=V3(-1000+3.5,-.4,0)}}
 else{scene.background=new THREE.Color(0x02030a);moonL.intensity=0;hemi.intensity=.35;
  let a;if(s==='s3'){a=lt<d*.3?23+3*Math.sin(t*4)*(lt<d*.2?1:0):wob(t-TL.s3[0]-d*.3);ghostM.group.visible=lt<d*.25;ghostM.group.scale.setScalar(Math.max(.001,1-ss(d*.12,d*.25,lt)));
   ang.set([`*${Math.round(a)}°`]);p=V3(2000+Math.sin(t*.3)*3,4,112-k*6);q=V3(2000,4,0)}
  else{a=85;ang.set(['*85°']);p=V3(2000+20*Math.sin(.3+k*.5),6,106);q=V3(2000,4,0)}
  tilt.rotation.z=a*Math.PI/180;glb.group.rotation.y=t*.5}
 cam.position.copy(p);cam.lookAt(q);WV.done();r.render(scene,cam)};
window.ready=true;
