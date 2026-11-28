// Mito '¿tu pez de colores lo olvida todo a los 3 segundos?' (3603). Fuentes en mito_pez.py (Universidad de Plymouth 2003; Discover Wildlife; Mental Floss).
// Reutilizable: SALÓN con mesa y PECERA (fishbowl), PEZ DE COLORES (goldfish), LABORATORIO con acuario, PALANCA que suelta bolitas de comida,
// reloj de pared que corre y luz verde/roja de 'funciona / no funciona', calendario de pared, FONDO MARINO con altavoz que emite ondas y banco de peces.
import {THREE,J,mk,ss,V3,clamp,stage,sun,box,glow,pixTex,capataz,segAt,mouthAt,puffs,label3d,wallClock,goldfish,fishbowl} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0xf0e2cc,exposure:1.12});const R=mk(3603);
const hemi=new THREE.HemisphereLight(0xfff4e4,0x8a7060,1.05);scene.add(hemi);const S=sun(scene,{pos:[8,22,16],span:22,power:2.0});
const lerp=(a,b,x)=>a+(b-a)*x;
// ---------- SALÓN (origen)
const HOME=new THREE.Group();scene.add(HOME);
const wood=pixTex(64,64,(g,w,h)=>{g.fillStyle='#b88452';g.fillRect(0,0,w,h);g.fillStyle='#a8743f';for(let y=0;y<h;y+=8)g.fillRect(0,y,w,2)},[14,14]);
const fl=new THREE.Mesh(new THREE.PlaneGeometry(120,120),new THREE.MeshStandardMaterial({map:wood,roughness:.75}));fl.rotation.x=-Math.PI/2;fl.receiveShadow=true;HOME.add(fl);
const wp=pixTex(64,64,(g,w,h)=>{g.fillStyle='#e6c79a';g.fillRect(0,0,w,h);g.fillStyle='#dcb886';for(let x=0;x<w;x+=16)g.fillRect(x,0,6,h)},[12,5]);
const wall=new THREE.Mesh(new THREE.PlaneGeometry(80,30),new THREE.MeshStandardMaterial({map:wp,roughness:.9}));wall.position.set(0,15,-7);wall.receiveShadow=true;HOME.add(wall);
const win=new THREE.Mesh(new THREE.PlaneGeometry(5,4.4),new THREE.MeshBasicMaterial({color:0x9fd8ff,toneMapped:false}));win.position.set(-6.5,8.4,-6.95);HOME.add(win);
[[-6.5,10.7,5.6,.3],[-6.5,6.1,5.6,.3],[-9.2,8.4,.3,4.9],[-3.8,8.4,.3,4.9],[-6.5,8.4,.2,4.4]].forEach(([x,y,w,h])=>{const f=box(w,h,.25,0xf4efe6,.03);f.position.set(x,y,-6.85);HOME.add(f)});
const tab=box(7,.35,4,0x7a4a2a,.05);tab.position.set(0,3.0,0);HOME.add(tab);[[-3.1,-1.6],[3.1,-1.6],[-3.1,1.6],[3.1,1.6]].forEach(([x,z])=>{const l=box(.35,2.9,.35,0x5a3218,.04);l.position.set(x,1.45,z);HOME.add(l)});
const BW=fishbowl(2.3);BW.g.position.set(0,3.18,0);HOME.add(BW.g);
const FH=goldfish();FH.g.scale.setScalar(1.25);HOME.add(FH.g);
const can=box(.7,1.0,.7,0xe5343f,.08);can.position.set(2.6,3.68,.9);HOME.add(can);const canL=box(.72,.4,.72,0xffd23a,.04);canL.position.set(2.6,3.7,.9);HOME.add(canL);
const OW=capataz();OW.g.position.set(4.4,0,1.2);HOME.add(OW.g);
const BUB=puffs(scene,24,.16,0xe8f8ff,{opacity:.75});const bub=[...Array(24)].map(()=>[R()*6.28,R(),R()]);
// ---------- LABORATORIO (x=300)
const LAB=new THREE.Group();LAB.position.set(300,0,0);scene.add(LAB);
const lfl=new THREE.Mesh(new THREE.PlaneGeometry(120,120),new THREE.MeshStandardMaterial({color:0xd8dee8,roughness:.6}));lfl.rotation.x=-Math.PI/2;lfl.receiveShadow=true;LAB.add(lfl);
const tiles=pixTex(64,64,(g,w,h)=>{g.fillStyle='#f2f5fa';g.fillRect(0,0,w,h);g.fillStyle='#d6dde8';for(let i=0;i<w;i+=16){g.fillRect(i,0,1,h);g.fillRect(0,i,w,1)}},[16,6]);
const lw=new THREE.Mesh(new THREE.PlaneGeometry(80,30),new THREE.MeshStandardMaterial({map:tiles,roughness:.8}));lw.position.set(0,15,-7);LAB.add(lw);
const bench=box(11,.4,4.6,0x3a4252,.05);bench.position.set(0,3.0,0);LAB.add(bench);[[-5,-2],[5,-2],[-5,2],[5,2]].forEach(([x,z])=>{const l=box(.35,2.9,.35,0x2a303c,.03);l.position.set(x,1.45,z);LAB.add(l)});
const TW=8,TH=4.6,TD=3.4;const tank=new THREE.Mesh(new THREE.BoxGeometry(TW,TH,TD),new THREE.MeshStandardMaterial({color:0xcfefff,transparent:true,opacity:.18,roughness:.05,depthWrite:false}));tank.position.set(0,3.2+TH/2,0);LAB.add(tank);
const twat=new THREE.Mesh(new THREE.BoxGeometry(TW-.1,TH*.86,TD-.1),new THREE.MeshStandardMaterial({color:0x3fa8f0,transparent:true,opacity:.26,depthWrite:false}));twat.position.set(0,3.2+TH*.43,0);LAB.add(twat);
[[0,3.25,TW,.12,TD],[0,3.2+TH,TW,.14,TD]].forEach(([x,y,w,h,d])=>{const b=box(w+.1,h,d+.1,0x20242e,.03);b.position.set(x,y,0);LAB.add(b)});
for(let i=0;i<60;i++){const s=box(.3,.2,.3,[0xd8c49a,0x8a7a64,0xf2e8d0][i%3],.05);s.position.set((R()-.5)*(TW-.6),3.38+R()*.1,(R()-.5)*(TD-.6));LAB.add(s)}
// palanca: cuelga del borde superior y entra en el agua (eje en lo alto)
const LEV=new THREE.Group();LEV.position.set(2.6,3.2+TH+.2,0);LAB.add(LEV);const rod=box(.14,2.6,.14,0xc8ccd8,.03,{metalness:.6,roughness:.3});rod.position.y=-1.3;LEV.add(rod);
const pad=box(.7,.7,.16,0xe5343f,.08);pad.position.y=-2.6;LEV.add(pad);const lamp=new THREE.Mesh(new THREE.SphereGeometry(.34,16,12),new THREE.MeshBasicMaterial({color:0x40ff70,toneMapped:false}));lamp.position.set(2.6,3.2+TH+.75,0);LAB.add(lamp);const lampG=glow(0x40ff70,2.6,.8);lamp.add(lampG);
const feeder=box(1.1,.9,1.1,0x6a7286,.06);feeder.position.set(1.0,3.2+TH+.6,0);LAB.add(feeder);
const PEL=puffs(scene,30,.15,0x8a4a1a,{opacity:1});const pel=[...Array(30)].map(()=>[R()-.5,R(),R()-.5]);
const FL=goldfish();FL.g.scale.setScalar(.9);LAB.add(FL.g);
const CK=wallClock(1.3);CK.g.position.set(-4.2,9.0,-6.8);LAB.add(CK.g);
const cal=label3d(['DÍA 1'],{w:3.2,h:2.4,px:130,bg:'#ffffff',fg:'#1a1a22',accent:'#e5343f'});cal.position.set(-.9,9.2,-6.85);LAB.add(cal);
const calRing=box(3.3,.3,.2,0xe5343f,.04);calRing.position.set(-.9,10.5,-6.8);LAB.add(calRing);
const lS=new THREE.DirectionalLight(0xffffff,0);lS.position.set(310,20,14);lS.target=LAB;scene.add(lS);
// ---------- MAR (x=-300)
const SEA=new THREE.Group();SEA.position.set(-300,0,0);scene.add(SEA);
const sfl=new THREE.Mesh(new THREE.PlaneGeometry(200,200),new THREE.MeshStandardMaterial({color:0xc8b88a,roughness:1}));sfl.rotation.x=-Math.PI/2;SEA.add(sfl);
for(let i=0;i<26;i++){const rk=box(1+R()*2.4,.6+R()*1.8,1+R()*2,[0x5a6a72,0x6a7a6a,0x4a5a64][i%3],.3);rk.position.set((R()-.5)*60,.4,-6-R()*40);SEA.add(rk)}
const weeds=[];for(let i=0;i<14;i++){const w=new THREE.Group();for(let k=0;k<6;k++){const l=box(.25,.9,.2,0x2f8a4a,.05);l.position.y=.45+k*.85;w.add(l)}w.position.set((R()-.5)*40,0,-4-R()*20);SEA.add(w);weeds.push(w)}
const spk=box(1.6,1.6,1.2,0x22262e,.12);spk.position.set(0,.8,0);SEA.add(spk);const cone=new THREE.Mesh(new THREE.CylinderGeometry(.55,.3,.2,20),new THREE.MeshStandardMaterial({color:0xffc23a,metalness:.4,roughness:.4}));cone.rotation.x=Math.PI/2;cone.position.set(0,.85,.65);SEA.add(cone);
const rings=[0,1,2].map(()=>{const m=new THREE.Mesh(new THREE.TorusGeometry(1,.06,8,48),new THREE.MeshBasicMaterial({color:0xfff2a0,transparent:true,opacity:.7,toneMapped:false}));m.position.set(0,.85,.8);SEA.add(m);return m});
const school=[...Array(14)].map((_,i)=>{const f=goldfish(0x9aa8b8,0xe6ecf2);f.g.scale.setScalar(.7);SEA.add(f.g);f.u=[R()*6.28,R(),R()];return f});
const RAYS=puffs(scene,40,.12,0xeaffff,{opacity:.6});
const BG_HOME=new THREE.Color(0xf0e2cc),BG_LAB=new THREE.Color(0xe8eef6),BG_SEA=new THREE.Color(0x1a6aa0);
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],k=ss(0,d,lt),m=mouthAt(t);let p,q;
 const home=(s==='h'||s==='cta'),lab=(s==='s1'||s==='s2'||s==='s3'),sea=s==='s4';HOME.visible=home;LAB.visible=lab;SEA.visible=sea;
 for(let i=0;i<24;i++)BUB.set(i,0,-99,0,0);for(let i=0;i<30;i++)PEL.set(i,0,-99,0,0);for(let i=0;i<40;i++)RAYS.set(i,0,-99,0,0);
 scene.fog=null;S.intensity=2.0;hemi.intensity=1.05;lS.intensity=0;
 if(home){scene.background=BG_HOME;
  const cy=3.18+BW.cy;// el pez da vueltas dentro de la pecera; en el CTA se queda mirando al cristal (hacia la cámara)
  let fx,fz,fy,turn;if(s==='h'){const a=t*1.1+Math.PI/2;fx=Math.cos(a)*.6;fz=Math.sin(a)*.45;fy=cy-.1+Math.sin(t*1.3)*.25;turn=-a-Math.PI/2}
  else{fx=lerp(Math.cos(t)*.8,.0,ss(0,1.2,lt));fz=lerp(.2,1.0,ss(0,1.2,lt));fy=cy;turn=lerp(0,-Math.PI/2,ss(0,1.2,lt))+Math.sin(t*2)*.15}
  FH.g.position.set(fx,fy,fz);FH.g.rotation.y=turn;FH.pose(t,{swim:s==='h'?1:.5});
  bub.forEach(([a,b,c],i)=>{const f=(t*.35+b)%1;BUB.set(i,fx+Math.cos(a)*.2+.5,fy+f*1.6,fz+Math.sin(a)*.2,(1-f)*.9)});
  BW.g.userData.plant.children.forEach((l,i)=>l.rotation.z=Math.sin(t*1.5+i)*.25);
  OW.g.visible=false;OW.g.position.set(3.7,0,1.6);OW.g.rotation.y=-.5;OW.pose(t,m,{wave:s==='cta'?1:0,look:-.2});
  if(s==='h'){p=V3(1.0+Math.sin(t*.5)*.6,cy+1.8-k*.4,18-k*2.5);q=V3(0,cy+.9,0)}
  else{p=V3(1.6+k*.4,cy+2.0,27);q=V3(1.4,cy-1.0,0)}}
 else if(lab){scene.background=BG_LAB;lS.intensity=1.2;
  const top=3.2+TH;let hours=9.2,on=1,push=0,fx=-1.5,fy=5.6,fz=0,turn=0,pellets=0,day=1;
  if(s==='s1'){// aprende: nada hacia la palanca, la empuja, cae comida
   const c=(lt%3.4)/3.4;fx=lerp(-2.6,2.0,ss(0,.45,c));fy=5.2+Math.sin(t*1.6)*.25;turn=0;push=ss(.45,.55,c)*(1-ss(.62,.8,c));pellets=c>.5?(c-.5)/.5:0;hours=9+lt*.05}
  else if(s==='s2'){// el reloj corre: la palanca solo funciona 1 hora al día (luz verde); el pez espera y empuja a la hora justa
   hours=6+lt*(18/d)*1.0;const hh=hours%24;on=(hh>=10&&hh<11)?1:0;
   const wait=hh>=9.3&&hh<11;fx=wait?lerp(-1,2.0,ss(9.3,9.9,hh)):-2.4+Math.sin(t*.9)*1.4;fy=5.0+Math.sin(t*1.2)*.3;turn=wait?0:Math.sin(t*.9)>0?Math.PI:0;
   push=on?Math.max(0,Math.sin((hh-10)*Math.PI*6)):0;pellets=on?((hh-10)%1):0}
  else{// semanas después: el calendario pasa páginas y el pez SIGUE yendo a la palanca a su hora
   day=1+Math.floor(ss(.2,d*.8,lt)*89);hours=10.3;on=1;const c=(lt%2.6)/2.6;fx=lerp(-1.2,2.0,ss(0,.4,c));fy=5.1;push=ss(.4,.5,c)*(1-ss(.6,.75,c));pellets=c>.45?(c-.45)/.55:0}
  CK.set(hours);cal.set([day===1?'DÍA 1':`DÍA ${day}`]);
  lamp.material.color.setHex(on?0x40ff70:0xff3a3a);lampG.material.color.setHex(on?0x40ff70:0xff3a3a);
  LEV.rotation.z=push*.35;FL.g.position.set(fx,fy,fz);FL.g.rotation.y=turn;FL.pose(t,{swim:1});
  if(pellets>0)pel.forEach(([a,b,c],i)=>{const y=top-.2-pellets*(1+b*3.2);PEL.set(i,300+1.0+a*.9,Math.max(3.5,y),c*.9,1)});
  if(s==='s1'){p=V3(-.6+k*1.2,8.4,27-k*1.5);q=V3(.4,7.2,0)}
  else if(s==='s2'){p=V3(-1.6+k*1.0,8.6,29);q=V3(-.4,7.4,-2)}
  else{p=V3(1.6-k*.8,8.6,29-k*1.5);q=V3(.8,7.4,-2)}
  p.x+=300;q.x+=300}
 else{scene.background=BG_SEA;scene.fog=new THREE.Fog(0x1a6aa0,14,90);S.intensity=1.3;hemi.intensity=.9;
  weeds.forEach((w,i)=>w.children.forEach((l,j)=>l.rotation.z=Math.sin(t*1.2+i+j*.5)*.12*j));
  rings.forEach((rg,i)=>{const f=((t*.7+i/3)%1);rg.scale.setScalar(.6+f*6);rg.material.opacity=.7*(1-f)});
  const call=ss(.6,d*.85,lt);
  school.forEach((f,i)=>{const [a,b,c]=f.u;const far=V3(Math.cos(a)*(22+b*10),2+c*5,-14-b*14+Math.sin(a)*6);const near=V3(Math.cos(a)*(2.2+b*1.6),1.4+c*2.4,2.4+Math.sin(a)*1.6);
   const P=far.clone().lerp(near,call);P.x+=Math.sin(t*1.3+i)*.4;P.y+=Math.sin(t*1.7+i*2)*.3;f.g.position.copy(P);
   const dir=near.clone().sub(far);f.g.rotation.y=Math.atan2(-dir.z,dir.x)*(1-call*.6)+Math.sin(t+i)*.3*call;f.pose(t+i,{swim:1})});
  for(let i=0;i<40;i++){const f=((t*.05+i*.13)%1);RAYS.set(i,-300+(i%10-5)*4,18-f*16,-10-(i%4)*5,.8)}
  p=V3(-300+Math.sin(t*.3)*1.5,6.2-k*1.0,17-k*2);q=V3(-300,3.2,-2)}
 RAYS.done();BUB.done();PEL.done();
 cam.position.copy(p);cam.lookAt(q);r.render(scene,cam)};
window.ready=true;
