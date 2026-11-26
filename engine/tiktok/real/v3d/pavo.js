// ¿El pavo te da sueño por el triptófano? (3403, mito 3D, Acción de Gracias 26/11/2026). Fuentes en mito_pavo.py.
// Reutilizable: COMEDOR de noche con ventana, guirnalda y mesa de fiesta (feast), PAVO ASADO (turkey), SOFÁ con la abuela dormida y Z que suben (zzz),
// BÁSCULA DE PLATOS (balance) pavo frente a pollo, TORRE de raciones que crece una a una junto a un bote de pastillas.
import {THREE,J,mk,ss,V3,clamp,stage,sun,box,glow,pixTex,capataz,abuela,segAt,mouthAt,puffs,label3d,crowd,steam,turkey,sofa,balance,zzz,feast} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x1a1426,exposure:1.12});const R=mk(3403);
const hemi=new THREE.HemisphereLight(0xffe8cc,0x4a3a3a,1.05);scene.add(hemi);const S=sun(scene,{pos:[-8,22,14],span:24,power:1.6});
const warm=new THREE.PointLight(0xffb060,60,60,1.4);warm.position.set(0,10,4);scene.add(warm);
// ---------- comedor
const D=new THREE.Group();scene.add(D);
const wood=pixTex(64,64,(g,w,h)=>{g.fillStyle='#8a5a36';g.fillRect(0,0,w,h);g.fillStyle='#7a4c2c';for(let y=0;y<h;y+=8)g.fillRect(0,y,w,2);g.fillStyle='#9a6a42';for(let i=0;i<40;i++)g.fillRect((i*37)%w,(i*23)%h,6,1)},[14,14]);
const fl=new THREE.Mesh(new THREE.PlaneGeometry(120,120),new THREE.MeshStandardMaterial({map:wood,roughness:.75}));fl.rotation.x=-Math.PI/2;fl.receiveShadow=true;D.add(fl);
const wp=pixTex(64,64,(g,w,h)=>{g.fillStyle='#6a3a3a';g.fillRect(0,0,w,h);g.fillStyle='#7a4646';for(let x=0;x<w;x+=16)g.fillRect(x,0,6,h);g.fillStyle='#d8b05a';for(let y=8;y<h;y+=32)for(let x=3;x<w;x+=16)g.fillRect(x,y,2,2)},[12,5]);
const wall=new THREE.Mesh(new THREE.PlaneGeometry(80,30),new THREE.MeshStandardMaterial({map:wp,roughness:.9}));wall.position.set(0,15,-9);wall.receiveShadow=true;D.add(wall);
// ventana de noche con nieve
const win=new THREE.Mesh(new THREE.PlaneGeometry(7,5.5),new THREE.MeshBasicMaterial({color:0x1a2a5a,toneMapped:false}));win.position.set(8,9.5,-8.95);D.add(win);
[[8,12.35,7.6,.35],[8,6.65,7.6,.35],[4.35,9.5,.35,6],[11.65,9.5,.35,6],[8,9.5,.25,5.6],[8,9.5,7.2,.25]].forEach(([x,y,w,h])=>{const f=box(w,h,.25,0xf4efe6,.03);f.position.set(x,y,-8.85);D.add(f)});
const flakes=puffs(scene,60,.12,0xffffff,{opacity:.9});
// guirnalda de luces
const bulbs=[];for(let i=0;i<26;i++){const x=-20+i*1.6,y=14.5-Math.sin(i/25*Math.PI*3)**2*1.2;const c=[0xffc23a,0xff5a4a,0x4ade80,0x4de3ff][i%4];const b=box(.32,.42,.32,c,.1,{emissive:c,emissiveIntensity:1.6});b.position.set(x,y,-8.7);D.add(b);bulbs.push(b)}
// cuadro y aparador
const pic=box(5,3.4,.2,0xc8a050,.05);pic.position.set(-9,10,-8.85);D.add(pic);const pin=new THREE.Mesh(new THREE.PlaneGeometry(4.2,2.6),new THREE.MeshStandardMaterial({map:pixTex(32,20,(g,w,h)=>{g.fillStyle='#e89a4a';g.fillRect(0,0,w,h);g.fillStyle='#7a4a2a';g.fillRect(0,13,w,7);g.fillStyle='#ffd27a';g.fillRect(20,3,5,5)})}));pin.position.set(-9,10,-8.7);D.add(pin);
const F=feast(16);D.add(F.g);
const TK=turkey(1.05);TK.position.set(0,3.24,0);D.add(TK);
const ST=puffs(scene,40,.35,0xffffff,{opacity:.3,depthWrite:false});
// familia detrás de la mesa
const FAM=crowd(scene,6,{s:1.75,seed:26});const famP=[[-6.4,-3.4],[-3.8,-3.4],[-1.3,-3.6],[5.6,-3.4],[7.6,-3.0],[-8.4,-2.4]];
const hero=capataz();hero.g.position.set(2.6,0,-3.3);hero.g.scale.setScalar(1.25);hero.g.rotation.y=-.15;D.add(hero.g);
// sofá con la abuela
const SF=sofa(0x5a4a8a);SF.position.set(-12.5,0,-4.5);SF.rotation.y=.35;D.add(SF);
const ab=abuela();ab.g.position.set(-.6,1.2,.15);ab.g.rotation.x=-.32;SF.add(ab.g);
const Z1=zzz(scene,3,{w:1.6}),Z2=zzz(scene,3,{w:1.4}),Z3=zzz(scene,3,{w:1.4});
// ---------- laboratorio (x=300): báscula y torre de raciones
const LB=new THREE.Group();LB.position.set(300,0,0);scene.add(LB);
const lf=new THREE.Mesh(new THREE.PlaneGeometry(90,60),new THREE.MeshStandardMaterial({map:pixTex(32,32,(g,w,h)=>{g.fillStyle='#2a2f48';g.fillRect(0,0,w,h);g.strokeStyle='#3a4060';g.strokeRect(0,0,w,h)},[22,15]),roughness:.7}));lf.rotation.x=-Math.PI/2;lf.receiveShadow=true;LB.add(lf);
const lw=new THREE.Mesh(new THREE.PlaneGeometry(90,40),new THREE.MeshStandardMaterial({color:0x232842,roughness:.9}));lw.position.set(0,20,-12);LB.add(lw);
const BAL=balance();BAL.g.position.set(0,0,0);LB.add(BAL.g);
const tP=turkey(.42);tP.position.y=-2.55;BAL.pans[0].add(tP);
const tC=turkey(.42);tC.traverse(o=>{if(o.isMesh&&o.material.color&&o.material.color.getHex()===0xb8642a)o.material=o.material.clone(),o.material.color.setHex(0xe0a868)});tC.position.y=-2.55;BAL.pans[1].add(tC);
const lPv=label3d(['*PAVO','≈250 mg'],{w:3.8,h:1.8,px:110,accent:'#ffc23a'});lPv.position.set(-5.2,1.6,1.2);LB.add(lPv);
const lPo=label3d(['*POLLO','≈250 mg'],{w:3.8,h:1.8,px:110,accent:'#4ade80'});lPo.position.set(5.2,1.6,1.2);LB.add(lPo);
// torre de 12 raciones (x=330 local 30)
const TW=new THREE.Group();TW.position.set(30,0,0);LB.add(TW);const port=[];for(let i=0;i<12;i++){const tk=turkey(.32);tk.position.y=i*.78;TW.add(tk);port.push(tk)}
const ped=box(2.4,.5,2.4,0x4a5070,.05);ped.position.y=-.25;TW.add(ped);
const bot=new THREE.Group();bot.position.set(-4.2,0,0);TW.add(bot);{const b=new THREE.Mesh(new THREE.CylinderGeometry(1.1,1.1,3,24),new THREE.MeshStandardMaterial({color:0xf4f6ff,roughness:.3}));b.position.y=1.5;bot.add(b);const cap=new THREE.Mesh(new THREE.CylinderGeometry(1.15,1.15,.7,24),new THREE.MeshStandardMaterial({color:0xff6a4a,roughness:.4}));cap.position.y=3.35;bot.add(cap);
 const lab=label3d(['*TRIPTÓFANO','1.000–3.000 mg'],{w:2.2,h:1.3,px:100,accent:'#ff6a4a'});lab.position.set(0,1.6,1.12);bot.add(lab);
 for(let i=0;i<5;i++){const p=box(.5,.22,.28,0xffffff,.1);p.position.set(1.6+i*.15,.11,.9-i*.4);p.rotation.y=i;bot.add(p)}}
const cnt=label3d(['×1'],{w:3.2,h:1.6,px:190,sprite:true,bg:null,accent:'#ffc23a',fg:'#ffc23a'});TW.add(cnt);
const four=glow(0xffc23a,5,.0);TW.add(four);
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],k=ss(0,d,lt),m=mouthAt(t);let p,q;
 const lab=s==='s2'||s==='s3';D.visible=!lab;LB.visible=lab;FAM.body.visible=FAM.head.visible=!lab;
 bulbs.forEach((b,i)=>b.material.emissiveIntensity=1.0+.9*Math.sin(t*3+i*1.7));
 for(let i=0;i<60;i++){const x=4.8+((i*.53)%6.4),y=12-((t*.8+i*.37)%5.4);flakes.set(i,lab?-999:x,y,-8.8,1)}flakes.done();
 Z1.at(0,0,0,t,0);Z2.at(0,0,0,t,0);Z3.at(0,0,0,t,0);
 if(!lab){scene.background=new THREE.Color(0x1a1426);S.intensity=1.6;warm.intensity=60;
  // sueño de la familia: 0 despiertos, 1 cabeceando
  const sleepy=s==='h'?0:s==='s1'?ss(1.5,d,lt)*.6:s==='s4'?.6+.4*ss(.5,d*.6,lt):.5;
  famP.forEach(([x,z],i)=>{const nod=sleepy*(.35+.25*Math.sin(t*1.3+i*1.9));FAM.set(i,x,-nod*.6,z,1.75,i===5?.6:0)});FAM.done();
  hero.pose(t,s==='h'||s==='s1'||s==='s4'||s==='cta'?m:0,{wave:s==='cta'?1:0,point:s==='h'?.7*ss(.3,.9,lt):0,look:-.2});
  hero.head.rotation.x=s==='s4'?.25*Math.sin(t*1.2)**2:hero.head.rotation.x;
  ST.m.visible=true;steam(ST,0,40,0,5.6,0,t,1.3);ST.done();
  ab.head.rotation.x=.35+.12*Math.sin(t*1.1);ab.head.rotation.z=.2;
  const abp=new THREE.Vector3();ab.head.getWorldPosition(abp);Z1.at(abp.x+.4,abp.y+.9,abp.z,t,s==='h'?ss(1.2,2,lt):1);
  if(s==='s4'){Z2.at(-6.4,5.4,-3.4,t+.4,ss(1,2,lt));Z3.at(5.6,5.4,-3.4,t+.9,ss(1.8,2.8,lt))}
  if(s==='h'){p=V3(1+Math.sin(t*.4)*.5,8.6-k*.6,22-k*3);q=V3(1,4.9,-1.2)}
  else if(s==='s1'){const a=ss(.4,d,lt);p=V3(-1-a*10,9.5,38-a*4);q=V3(-1-a*10.5,4.6,-3)}
  else if(s==='s4'){p=V3(.5+Math.sin(t*.3)*2,9.5,36-k*4);q=V3(0,5.0,-2)}
  else{p=V3(3.4+k*.6,8.0,24-k*1.5);q=V3(2.6,3.6,-3)}}
 else{scene.background=new THREE.Color(0x232842);warm.intensity=0;S.intensity=2.0;hemi.intensity=1.2;
  if(s==='s2'){const a=Math.sin(lt*3.2)*.22*Math.exp(-lt*.75)*(lt>.3?1:0);BAL.set(a);
   p=V3(300+Math.sin(t*.3)*1.2,5.4,46-k*3);q=V3(300,3.4,0)}
  else{const n=Math.min(12,Math.floor(ss(.3,d*.82,lt)*12+1e-6)+1);port.forEach((pp,i)=>{const a=clamp((ss(.3,d*.82,lt)*12-i)*1.0);pp.visible=i<n;pp.position.y=i*.78+(1-a)*3;pp.scale.setScalar(.32*(i<n?Math.max(.05,a):.001))});
   cnt.set([`×${n}`]);cnt.position.set(3.6,Math.min(n,12)*.78*.5+1,0);four.material.opacity=n>=4&&n<6?.6:0;four.position.set(0,1.6,0);
   p=V3(300+28.5+Math.sin(t*.3),4.4+k*1.8,24+k*17);q=V3(300+28.5,2.6+k*4.6,0)}}
 cam.position.copy(p);cam.lookAt(q);r.render(scene,cam)};
window.ready=true;
