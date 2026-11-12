// Mito: 'te tragas 8 arañas al año mientras duermes' (2003). Rod Crawford (Museo Burke, Seattle) vía Scientific American y Mental Floss (06/06/2013).
// Reutilizable: dormitorio nocturno con la capataz DORMIDA (lieDown), respiración y latido visibles, ANILLOS DE VIBRACIÓN que salen del pecho y
// recorren la cama y el suelo, araña de bloques (spider) que baja del techo por su hilo, siente las vibraciones con las patas y huye; revista que se deshace.
import {THREE,J,mk,ss,V3,clamp,stage,sun,box,glow,capataz,segAt,mouthAt,label3d,puffs,spider,bed,lieDown} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x0d1430,fog:[0x0d1430,40,140],exposure:1.15});const R=mk(2003);
const hemi=new THREE.HemisphereLight(0x8fa4e0,0x241a2a,.8);scene.add(hemi);const S=sun(scene,{pos:[-12,26,16],span:26,color:0xb8c8ff,power:1.0});
const lampL=new THREE.PointLight(0xffc880,70,30,1.5);lampL.position.set(5.5,5,-3);scene.add(lampL);
// ---------- DORMITORIO
const fl=new THREE.Mesh(new THREE.PlaneGeometry(80,80),new THREE.MeshStandardMaterial({color:0x5a4030,roughness:.9}));fl.rotation.x=-Math.PI/2;fl.receiveShadow=true;scene.add(fl);
for(let i=0;i<16;i++){const p=box(2.4,.05,80,i%2?0x6a4a36:0x5e4232,.01);p.position.set(-19+i*2.5,.02,0);scene.add(p)}
const wall=box(60,22,.6,0x2a3360,.05);wall.position.set(0,11,-8);scene.add(wall);
const wall2=box(.6,22,40,0x242c54,.05);wall2.position.set(-12,11,10);scene.add(wall2);
const win=new THREE.Group();{const f=box(7,6,.5,0x8a6a4a,.08);win.add(f);const gl=box(6.2,5.2,.3,0x0a1030,.02,{emissive:0x101848,emissiveIntensity:.6});gl.position.z=.12;win.add(gl);const cx=box(.25,5.2,.35,0x8a6a4a,.02);cx.position.z=.2;const cy=box(6.2,.25,.35,0x8a6a4a,.02);cy.position.z=.2;win.add(cx,cy);const moon=new THREE.Mesh(new THREE.SphereGeometry(.9,20,14),new THREE.MeshBasicMaterial({color:0xfff4c8,toneMapped:false}));moon.position.set(1.5,1.3,.3);win.add(moon);
 for(let i=0;i<14;i++){const s=box(.12,.12,.05,0xffffff,.01,{emissive:0xffffff,emissiveIntensity:1});s.position.set((R()-.5)*5.6,(R()-.5)*4.6,.3);win.add(s)}}
win.position.set(-10.5,9,-7.6);scene.add(win);
const B=bed(0x3a6fd8);B.position.set(1,0,-3.5);scene.add(B);
const hero=capataz();hero.hat.forEach(h=>h.visible=false);const L=lieDown(hero,B,0x3a6fd8);
const nt=box(2.2,2.4,2.2,0x7a4e2e,.08);nt.position.set(5.6,1.2,-5.6);scene.add(nt);const lampS=box(.9,1.2,.9,0xffd890,.2,{emissive:0xffb050,emissiveIntensity:.9});lampS.position.set(5.6,3.1,-6.1);scene.add(lampS);const lg=glow(0xffc070,5,.5);lg.position.set(5.6,3.4,-5.9);scene.add(lg);
const clock=label3d(['03:12'],{w:2.4,h:1.0,px:170,bg:'#0b0d14',fg:'#ff4a4a',accent:'#2a2f40'});clock.position.set(5.6,2.9,-4.4);scene.add(clock);
// revista sobre la mesilla (s4): portada con '¿?' que se deshace en cubos
const magC=document.createElement('canvas');magC.width=256;magC.height=340;{const g=magC.getContext('2d');g.fillStyle='#f4ede0';g.fillRect(0,0,256,340);g.fillStyle='#c8202a';g.fillRect(0,0,256,70);g.fillStyle='#fff';g.font='bold 44px sans-serif';g.textAlign='center';g.fillText('REVISTA',128,50);g.fillStyle='#222';g.font='bold 150px sans-serif';g.fillText('¿?',128,240);g.font='bold 30px sans-serif';g.fillText('8 ARAÑAS/AÑO',128,310)}
const magT=new THREE.CanvasTexture(magC);magT.colorSpace=THREE.SRGBColorSpace;
const mag=new THREE.Mesh(new THREE.BoxGeometry(1.6,.08,2.1),[0,0,new THREE.MeshStandardMaterial({map:magT}),0,0,0].map(m=>m||new THREE.MeshStandardMaterial({color:0xe8e0d0})));mag.position.set(5.4,2.46,-5.2);mag.rotation.y=.25;scene.add(mag);
const magP=puffs(scene,60,.16,0xf4ede0);
// rótulo integrado en la pared (s1)
const panel=label3d(['TE TRAGAS AL AÑO…','*0 ARAÑAS'],{w:6,h:2.7,px:120});panel.position.set(-3.6,6.6,-7.6);scene.add(panel);
const who=label3d(['ROD CRAWFORD · MUSEO BURKE'],{w:6,h:.9,px:80,accent:'#ffc23a'});who.position.set(-3.6,4.75,-7.6);scene.add(who);
// latido y anillos de vibración
const heart=glow(0xff3a4a,1.6,.9);B.add(heart);heart.position.set(-.35,2.6,-.6);
const RINGS=[];for(let i=0;i<5;i++){const m=new THREE.Mesh(new THREE.TorusGeometry(1,.06,6,64),new THREE.MeshBasicMaterial({color:0xffc23a,transparent:true,opacity:0,toneMapped:false}));m.rotation.x=Math.PI/2;scene.add(m);RINGS.push(m)}
const zz=[0,1,2].map(i=>{const z=label3d(['*Z'],{w:1.2,h:1.2,px:140,sprite:true,bg:''});scene.add(z);return z});
// araña
const sp=spider(.85);scene.add(sp.g);const silk=new THREE.Mesh(new THREE.CylinderGeometry(.025,.025,1,6),new THREE.MeshBasicMaterial({color:0xe8eeff,transparent:true,opacity:.75}));scene.add(silk);
// telaraña en la esquina (cta)
const web=new THREE.Group();{const M=new THREE.LineBasicMaterial({color:0xdfe6ff,transparent:true,opacity:.55});for(let k=0;k<9;k++){const a=k/8*Math.PI/2;const g=new THREE.BufferGeometry().setFromPoints([V3(0,0,0),V3(Math.cos(a)*5,-Math.sin(a)*5,0)]);web.add(new THREE.Line(g,M))}
 for(let j=1;j<6;j++){const pts=[];for(let k=0;k<=8;k++){const a=k/8*Math.PI/2;pts.push(V3(Math.cos(a)*j*.9,-Math.sin(a)*j*.9,0))}web.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts),M))}}
web.position.set(7.6,10.2,-7.65);web.rotation.y=Math.PI;scene.add(web);
const HEAD=V3(1,2.6,-5.3);// cara de la capataz (mundo)
const beat=t=>{const p=(t*1.15)%1;return Math.exp(-p*9)+.6*Math.exp(-Math.max(0,p-.18)*9)*(p>.18?1:0)};
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],k=ss(0,d,lt);
 // respiración y latido
 const br=Math.sin(t*1.6);L.blanket.scale.y=1+.12*br;L.blanket.position.y=2.15+.04*br;hero.pose(t,0,{});hero.eyes.forEach(e=>e.scale.y=.1);hero.mouth.scale.y=1.6+.8*Math.max(0,br);
 const bt=beat(t);heart.material.opacity=(s==='s2'||s==='s3')?.4+.6*bt:0;heart.scale.setScalar(1.2+1.2*bt);
 // anillos: salen del pecho en cada latido (s2: sobre la cama; s3: por el suelo)
 RINGS.forEach((m,i)=>{const ph=((t*1.15)+i/RINGS.length)%1;const on=s==='s2'||s==='s3';const rad=s==='s3'?1+ph*16:.6+ph*5.5;m.scale.setScalar(rad);m.material.opacity=on?(1-ph)*.85:0;
  if(s==='s3')m.position.set(1,.08,-3.5+ph*2);else m.position.set(1,2.45,-4.1)});
 zz.forEach((z,i)=>{const ph=(t*.45+i/3)%1;z.position.set(1.4+ph*1.8,3.3+ph*3,-5.6);z.material.opacity=(s==='s2'||s==='h')?Math.sin(Math.PI*ph):0;z.visible=s==='s2'||s==='h'});
 panel.visible=who.visible=s==='s1'||s==='cta';clock.visible=s!=='s4';magP.m.visible=s==='s4';
 // araña
 silk.visible=false;sp.g.rotation.set(0,0,0);let p,q;
 if(s==='h'){// baja del techo hacia la cara
  const y=HEAD.y+3.7-1.9*ss(0,d*.85,lt);sp.g.position.set(HEAD.x,y,HEAD.z+.2);sp.g.rotation.x=Math.PI/2*.9;sp.walk(t*3);silk.visible=true;silk.position.set(HEAD.x,(y+16)/2+.6,HEAD.z+.2);silk.scale.y=16-y;
  p=V3(3.2-k*.6,10.2-k*.4,4.6-k*.8);q=V3(1,4.2,-5.0)}
 else if(s==='s1'){sp.g.position.set(-.3,6.0,-7.25);sp.g.rotation.x=Math.PI/2;sp.g.rotation.y=Math.sin(t*2)*.2;sp.walk(t*4);
  p=V3(-2.8+k*.6,5.2,16-k*1.2);q=V3(-3.0,7.2,-7)}
 else if(s==='s2'){sp.g.position.set(-14,0,0);p=V3(1+Math.sin(t*.3)*.5,12.5-k*.8,1.8);q=V3(1,1.2,-4.6)}
 else if(s==='s3'){// la araña camina hacia la cama, nota la vibración, se encoge y huye
  const a=ss(0,d*.38,lt),fz=ss(d*.38,d*.52,lt)-ss(d*.6,d*.66,lt),run=ss(d*.62,d,lt);
  const z=7-4.2*a+9*run;sp.g.position.set(-1.5+run*-3,0,z);sp.g.rotation.y=Math.PI+(run>0?Math.PI*ss(d*.6,d*.68,lt):0);
  if(fz>.01&&run<.02)sp.freeze(fz);else sp.walk(t*(run>0?16:6));sp.eyes.forEach(e=>e.scale.setScalar(1+fz*.6));
  p=V3(6.5,5.2,z+15+run*2);q=V3(-1.2,2.8,z-1.5)}
 else if(s==='s4'){sp.g.position.set(-14,0,0);const kk=ss(d*.3,d*.75,lt);mag.visible=kk<.98;mag.scale.setScalar(1-kk);
  for(let i=0;i<60;i++){const a=i*2.4,rr=(.3+(i%7)*.12)*kk*3;magP.set(i,5.4+Math.cos(a)*rr,2.6+kk*(i%5)*.35+Math.sin(i)*.2,-5.2+Math.sin(a)*rr,kk>0&&kk<.99?1:0,i+t)}magP.done();
  p=V3(7.2-k*.4,7.6,-.4-k*.6);q=V3(5.3,3.6,-5.3)}
 else{// cta: araña en su telaraña de la esquina, saludando
  sp.g.position.set(5.2,7.7,-7.25);sp.g.rotation.x=Math.PI/2;sp.g.rotation.y=.4;sp.walk(0);sp.wave(t);
  p=V3(4.6-k*1.0,5.5,14-k);q=V3(4.2,7.4,-7)}
 cam.position.copy(p);cam.lookAt(q);r.render(scene,cam)};
window.ready=true;
