// Serie P24 '¿Y si la Luna estuviera el doble de cerca?' (3504). Fuentes en serie_luna2x.py. Basada en sinluna.js.
// Nuevo y reutilizable: Luna que CRECE a escala (moonScale), marea con amplitud regulable, ESPACIO con Tierra, Luna y RAYO LÁSER que rebota en un espejo (lunar laser ranging).
// Reutilizable: PUERTO DE NOCHE con mar de bloques, barcas que suben y bajan, regla de marea en el muelle (tideAt) y Luna que se apaga;
// PLAZA DE NOCHE (de doslunas.js) con luz de luna regulable; GLOBO con EJE que se bambolea (wob) frente al Sol y medidor de grados.
import {THREE,J,mk,ss,V3,clamp,stage,box,glow,capataz,segAt,mouthAt,puffs,stars,voxGlobe,voxMoon,ruler,label3d} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x0a1430,exposure:1.2});cam.far=2500;cam.updateProjectionMatrix();const R=mk(3504);
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

// ---------- ESPACIO (x=2000): Tierra, Luna y láser
const SP=new THREE.Group();SP.position.set(2000,0,0);scene.add(SP);
const EA=voxGlobe(9000,8);EA.group.position.set(-14,0,0);SP.add(EA.group);
const LM=voxMoon(2600,2.6,{cube:.4,seed:4,emissive:.55});SP.add(LM.group);
const gS=new THREE.DirectionalLight(0xfff4e0,3.0);gS.position.set(2000-200,60,120);gS.target=SP;scene.add(gS);
const LZ=new THREE.Mesh(new THREE.CylinderGeometry(.09,.09,1,8),new THREE.MeshBasicMaterial({color:0x4aff6a,toneMapped:false,transparent:true,opacity:.95}));SP.add(LZ);
const LZg=glow(0x4aff6a,3,.9);SP.add(LZg);const MIR=box(.8,.5,.8,0xdfe6ee,.05,{metalness:.9,roughness:.15,emissive:0x4aff6a,emissiveIntensity:0});SP.add(MIR);
const BUL=new THREE.Mesh(new THREE.SphereGeometry(.28,12,8),new THREE.MeshBasicMaterial({color:0xb8ffc8,toneMapped:false}));SP.add(BUL);
const sky=new THREE.Color(0x0a1430);
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],k=ss(0,d,lt),m=mouthAt(t);let p,q;
 const port=s==='h'||s==='s2',plaza=s==='s1'||s==='cta',space=s==='s3'||s==='s4';PT.visible=port;PL.visible=plaza;PM.group.visible=ph.visible=CAP.g.visible=plaza;SP.visible=space;gS.intensity=space?3:0;
 for(let i=0;i<220;i++)WV.set(i,0,-999,0,0);flash.material.opacity=0;
 if(port){scene.background=sky;
  // Luna al DOBLE de tamaño aparente (×2) desde el primer frame; en h sube por encima del puerto
  MO.group.scale.setScalar(2);mh.scale.setScalar(120);mh.material.opacity=.55;MO.group.position.set(-6,s==='h'?14+k*16:30,-150);mh.position.copy(MO.group.position);
  refl.forEach(g=>g.material.opacity=.55);moonL.intensity=1.6;hemi.intensity=.8;
  const amp=s==='h'?1.6:1.6+(4.2-1.6)*ss(d*.25,d*.6,lt);const tide=tideAt(t,amp);SEA.position.y=-3+tide;LVL.position.y=tide;HI.position.y=s==='h'?1.6:1.6+(4.2-1.6)*ss(d*.25,d*.6,lt);HI.visible=LVL.visible=s==='s2';
  boats.forEach((b,i)=>{b.position.y=tide+Math.sin(t*1.7+i)*.12;b.rotation.z=Math.sin(t*1.3+i*2)*.08});
  for(let i=0;i<220;i++){const x=-60+(i*13.7)%120,z=-4-((i*7.3)%90);WV.set(i,x+Math.sin(t+i)*.6,tide+.08+Math.max(0,Math.sin(t*2+i*.7))*.18,z,.7+.5*Math.sin(t*1.5+i))}
  if(s==='h'){p=V3(-2+k*1.5,5.5,34-k*4);q=V3(-4,16+k*8,-90)}
  else{p=V3(-2+Math.sin(t*.4)*.6,5.2,25);q=V3(2,2.8,-8)}}
 else if(plaza){scene.background=new THREE.Color(0x0b1638);
  // s1: la Luna crece de ×1 a ×2 (ancho) y la plaza se ilumina ×4
  const g=s==='s1'?1+ss(d*.3,d*.7,lt):2;PM.group.scale.setScalar(g);ph.scale.setScalar(48*g);ph.material.opacity=.4+.1*g;
  moonL.intensity=.25*g*g;hemi.intensity=.12+.12*g*g;ST.material.size=1.5;
  CAP.pose(t,s==='cta'?m:0,{wave:s==='cta'?1:0,look:.2});CAP.head.rotation.x=s==='cta'?-.1:-.45;
  if(s==='s1'){p=V3(-1000+3+Math.sin(t*.3),3.0+k*.8,30);q=V3(-1000+2.4,13,-40)}else{hemi.intensity=1.0;moonL.intensity=1.2;p=V3(-1000+3.5+k*1.2,6,32-k*2);q=V3(-1000+3.5,-1.2,0)}}
 else{scene.background=new THREE.Color(0x02030a);moonL.intensity=0;hemi.intensity=.3;EA.group.rotation.y=t*.4;
  // distancia en el plano: s3 la Luna se aleja poco a poco; s4 vuelve atrás en el tiempo y se acerca
  const D=s==='s3'?22+2*k:24-10*ss(.1,.8,lt/d);LM.group.position.set(-14+D,0,0);LM.group.rotation.y=t*.2;
  MIR.position.set(-14+D-2.75,0,0);const on=s==='s3';LZ.visible=LZg.visible=BUL.visible=on;MIR.material.emissiveIntensity=on?1.2*(.5+.5*Math.sin(t*8)):0;
  if(on){const L=D-8-2.75;LZ.scale.set(1,L,1);LZ.rotation.z=Math.PI/2;LZ.position.set(-14+8+L/2,0,0);const f=(t*1.1)%1;const u=f<.5?f*2:2-f*2;BUL.position.set(-14+8+u*L,0,0);LZg.position.copy(BUL.position)}
  if(s==='s3'){p=V3(2000-5+Math.sin(t*.3)*2,1,114-k*5);q=V3(2000-5,0,0)}else{p=V3(2000-5,1,112-k*8);q=V3(2000-5,0,0)}
  // los mares de la Tierra se 'abultan' más cuanto más cerca (marea exagerada a ojo, sin cifra)
  EA.group.scale.set(1,1,1)}
 cam.position.copy(p);cam.lookAt(q);WV.done();r.render(scene,cam)};
window.ready=true;
