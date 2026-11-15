// ¿Y si la Tierra fuera el doble de grande? (2304). Serie ¿QUÉ PASARÍA SI…? Parte 12. Cálculos en serie_crece.py.
// Reutilizable: báscula con lectura que se dispara (kgAt), SALTO medido con regla y marca fantasma de 'hoy', dos globos HOY/×2 que crecen,
// COHETE de bloques con plataforma, llama y humo que despega (rocket()), y un cielo de supertierras (globos de colores).
import {THREE,J,mk,ss,V3,clamp,stage,sun,box,glow,pixTex,capataz,segAt,mouthAt,puffs,label3d,ruler,stars,voxGlobe} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x8ad4ff,fog:[0xc8e4ff,60,190],exposure:1.08});cam.far=3000;cam.updateProjectionMatrix();const R=mk(2304);
const hemi=new THREE.HemisphereLight(0xdcefff,0x8a9a6a,1.4);scene.add(hemi);const S=sun(scene,{pos:[-16,34,18],span:34});
const SKY=new THREE.Color(0x8ad4ff),SPACE=new THREE.Color(0x02030a);
// ---------- plaza
const st=new THREE.Group();scene.add(st);
const grass=pixTex(128,128,(g,w,h)=>{const q=mk(8);g.fillStyle='#6fb24e';g.fillRect(0,0,w,h);for(let i=0;i<700;i++){g.fillStyle=['#62a544','#7dbd58','#568f3c'][Math.floor(q()*3)];g.fillRect(Math.floor(q()*w/4)*4,Math.floor(q()*h/4)*4,4,4)}},[40,40]);
const gnd=new THREE.Mesh(new THREE.PlaneGeometry(400,400),new THREE.MeshStandardMaterial({map:grass,roughness:1}));gnd.rotation.x=-Math.PI/2;gnd.receiveShadow=true;st.add(gnd);
const plaza=new THREE.Mesh(new THREE.PlaneGeometry(40,22),new THREE.MeshStandardMaterial({map:pixTex(64,64,(g,w,h)=>{g.fillStyle='#d8cdb6';g.fillRect(0,0,w,h);g.strokeStyle='#b9ad94';g.lineWidth=2;for(let i=0;i<=w;i+=16){g.strokeRect(i,0,16,h);g.strokeRect(0,i,w,16)}},[10,6]),roughness:.95}));plaza.rotation.x=-Math.PI/2;plaza.position.set(0,.01,0);plaza.receiveShadow=true;st.add(plaza);
const COLS=[0xd9c7a8,0xc2573f,0x8fa6b8,0xe8dfca,0xa86a48,0x6f86a8];
[[-15,-14,8,14],[-5,-16,9,18],[6,-15,8,12],[16,-13,8,16],[-26,-10,7,11],[27,-10,7,13]].forEach(([x,z,w,h],i)=>{const b=box(w,h,7,COLS[i%6],.15);b.position.set(x,h/2,z);st.add(b);for(let y=1.5;y<h-1;y+=2.2)for(let a=-w/2+1.3;a<w/2-.8;a+=1.8){const wi=box(.9,1.2,.1,R()<.3?0xffe9a8:0x2a3a58,.02);wi.position.set(x+a,y,z+3.52);st.add(wi)}});
[[-9,4],[9,5],[-12,-4],[12,-5]].forEach(([x,z])=>{const tr=box(.6,2.4,.6,0x7a5232,.05);tr.position.set(x,1.2,z);st.add(tr);const cr=box(2.6,2.4,2.6,0x3f9a46,.3);cr.position.set(x,3.4,z);st.add(cr)});
// báscula + lectura (pantalla en un poste)
const scale=new THREE.Group();const base=box(3.2,.4,2.6,0xe8eaf0,.12);base.position.y=.2;scale.add(base);const top=box(2.8,.12,2.2,0x30343e,.05);top.position.y=.46;scale.add(top);scale.position.set(0,0,2);st.add(scale);
const disp=label3d(['80 kg'],{w:4.2,h:1.6,px:150,accent:'#ff4a4a'});disp.position.set(3.4,3.5,2.6);st.add(disp);const dpost=box(.25,2.4,.25,0x30343e,.03);dpost.position.set(3.4,1.2,2.5);st.add(dpost);
const hero=capataz();hero.g.position.set(0,.52,2);scene.add(hero.g);
// regla de salto (1 u = 43 cm: el capataz mide ~4,1 u = 1,75 m) y marca fantasma de 'hoy' (50 cm)
const U=1.75/4.1;const RU=ruler(.6/U,{step:.05/U,every:2,unit:5,ls:.5});RU.position.set(-1.9,.52,2.9);st.add(RU);
const ghostM=new THREE.MeshBasicMaterial({color:0x4de3ff,transparent:true,opacity:.6,toneMapped:false});const ghost=new THREE.Mesh(new THREE.BoxGeometry(2.6,.08,.08),ghostM);ghost.position.set(-.6,.52+.5/U,2.9);st.add(ghost);
const gLab=label3d(['HOY 50 cm'],{w:3,h:.8,px:110,bg:'#0d2a3a',accent:'#4de3ff'});gLab.position.set(-4.1,.52+.5/U+.35,3);st.add(gLab);
const jLab=label3d(['*25 cm'],{w:2.4,h:.9,px:130});jLab.position.set(-4.1,.52+.25/U-.35,3);st.add(jLab);
const dust=puffs(scene,60,.3,0xcbbfa6,{opacity:.85,depthWrite:false});const dp=[];for(let i=0;i<60;i++)dp.push([R()*6.28,R()]);
// ---------- espacio: dos globos HOY / ×2
const GL=new THREE.Group();GL.position.set(600,0,0);scene.add(GL);const gA=voxGlobe(5000,5);const gB=voxGlobe(9000,5,{seed:.4});GL.add(gA.group,gB.group);
gA.group.position.set(-6,0,0);
const lA=label3d(['HOY'],{w:3.4,h:1.2,px:130,sprite:true});GL.add(lA);const lB=label3d(['*×2'],{w:3.4,h:1.4,px:150,sprite:true});GL.add(lB);
const lM=label3d(['*MASA ×8'],{w:7,h:1.6,px:130,sprite:true});GL.add(lM);const lG=label3d(['*GRAVEDAD ×2'],{w:8,h:1.6,px:130,sprite:true,accent:'#ff4a4a'});GL.add(lG);
const lS=label3d(['*SUPERTIERRA','HASTA 2× TAMAÑO · NASA'],{w:10,h:2.6,px:120,sprite:true,accent:'#4ade80'});GL.add(lS);
const lH=label3d(['HORIZONTE','*4,7 → 6,6 km'],{w:10,h:2.6,px:120,sprite:true});GL.add(lH);
const others=[];[[0xd9824a,3.2,[-26,14,-40]],[0x9a6ad8,4,[24,-12,-50]],[0x4ac0b0,2.6,[30,18,-60]],[0xe0c060,3.6,[-30,-16,-55]]].forEach(([c,rad,p])=>{const m=new THREE.Mesh(new THREE.SphereGeometry(rad,28,20),new THREE.MeshStandardMaterial({color:c,roughness:.8,map:pixTex(64,32,(g,w,h)=>{const q=mk(rad*10|0);g.fillStyle='#fff';g.fillRect(0,0,w,h);for(let i=0;i<60;i++){g.fillStyle=`rgba(0,0,0,${.08+q()*.15})`;g.fillRect(q()*w,q()*h,4+q()*12,2+q()*4)}})}));m.position.set(...p);GL.add(m);const gl=glow(c,rad*3,.35);gl.position.set(...p);GL.add(gl);others.push(m)});
const gS=new THREE.DirectionalLight(0xffffff,0);gS.position.set(560,30,60);gS.target.position.set(600,0,0);scene.add(gS,gS.target);
const ST=stars(scene,1400);
// ---------- cohete (rocket): plataforma, torre, llama y humo
const RK=new THREE.Group();RK.position.set(1200,0,0);scene.add(RK);
const pad=box(14,1,14,0x5a5e66,.1);pad.position.y=.5;RK.add(pad);const twr=box(1.4,22,1.4,0xc8462e,.06);twr.position.set(-4.2,11,0);RK.add(twr);for(let y=2;y<21;y+=2.4){const a=box(3,.25,.25,0xc8462e,.02);a.position.set(-2.7,y,0);RK.add(a)}
const rocket=new THREE.Group();{const b=box(2.4,12,2.4,0xf2f2f4,.3);b.position.y=7;rocket.add(b);[3,9].forEach(y=>{const s=box(2.5,.6,2.5,0x2a2f3e,.1);s.position.y=y;rocket.add(s)});const n=new THREE.Mesh(new THREE.ConeGeometry(1.7,4,4),new THREE.MeshStandardMaterial({color:0xe0343a,roughness:.5}));n.rotation.y=Math.PI/4;n.position.y=15;rocket.add(n);
 [[1.6,0],[-1.6,0],[0,1.6],[0,-1.6]].forEach(([x,z])=>{const f=box(x?.3:1.6,3,z?.3:1.6,0xe0343a,.05);f.position.set(x*1.05,2.2,z*1.05);rocket.add(f)});const w=box(1,1,.2,0x2a6fe0,.1,{emissive:0x123a80,emissiveIntensity:.6});w.position.set(0,10.8,1.25);rocket.add(w)}
rocket.position.y=1;RK.add(rocket);
const flame=new THREE.Mesh(new THREE.ConeGeometry(1.2,5,16,1,true),new THREE.MeshBasicMaterial({color:0xffb030,transparent:true,opacity:.9,blending:THREE.AdditiveBlending,depthWrite:false,toneMapped:false}));flame.rotation.x=Math.PI;rocket.add(flame);
const fg=glow(0xffa030,9,.9);rocket.add(fg);const smoke=puffs(scene,140,1.2,0xe8e4dc,{opacity:.85,depthWrite:false});const sm=[];for(let i=0;i<140;i++)sm.push([R()*6.28,R(),R()]);
const vLab=label3d(['*22,4 km/s'],{w:7,h:1.8,px:150,sprite:true});RK.add(vLab);const vHoy=label3d(['HOY: 11,2 km/s'],{w:6.4,h:1.3,px:120,sprite:true,accent:'#4de3ff'});RK.add(vHoy);
const LOW=new THREE.Color(0x8ad4ff),HIGH=new THREE.Color(0x0a1030);
// ---------- lectura de la báscula
const kgAt=(s,lt,d)=>s==='h'?80+80*ss(.6,2.2,lt):s==='s2'?80+80*ss(.3,1.4,lt):s==='cta'?null:160;
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],k=ss(0,d,lt),m=mouthAt(t);let p,q,bg=SKY;
 const onP=s==='h'||s==='s2'||s==='cta';st.visible=hero.g.visible=onP;GL.visible=s==='s1'||s==='s4';RK.visible=s==='s3';dust.m.visible=smoke.m.visible=false;
 ST.visible=!onP;ST.position.set(s==='s3'?1200:600,0,0);
 if(onP){// báscula y salto
  const kg=kgAt(s,lt,d);disp.visible=dpost.visible=!(s==='s2'&&lt>=d*.5-.6);disp.set(kg==null?['¿Y TÚ?']:[`*${Math.round(kg)} kg`]);
  const shake=s==='h'&&lt>.6&&lt<2.4?Math.sin(t*50)*.03:0;scale.position.x=shake;
  // salto en la 2ª mitad de s2: sube 25 cm (en vez de 50, marca fantasma)
  let jy=0;const ja=d*.5,jb=d*.5+1.0;const show=s==='s2'&&lt>ja-.4;ghost.visible=gLab.visible=show;jLab.visible=s==='s2'&&lt>jb-.3;RU.visible=s==='s2';
  if(s==='s2'&&lt>ja&&lt<jb){const u=(lt-ja)/(jb-ja);jy=4*u*(1-u)*(.25/U)}
  if(s==='s2'&&lt>=jb){const u=clamp((lt-jb)/1.1);dust.m.visible=u<1;for(let i=0;i<60;i++){const[a,b]=dp[i];const rr=.6+u*(1.5+b*2);dust.set(i,Math.cos(a)*rr,.6+u*b*.8,2+Math.sin(a)*rr*.6,(1-u)*(.7+b))}dust.done()}
  hero.g.position.y=.52+jy;const sq=s==='h'||s==='s2'?ss(.6,1.6,s==='h'?lt:lt+1):0;hero.g.scale.set(1+.05*sq,1-.06*sq,1+.05*sq);
  hero.pose(t,m,{wave:s==='cta'?1:0,armsUp:jy>0?.6:0,look:s==='h'?.55:s==='cta'?0:.25,point:s==='h'&&lt>1.2?.5:0});
  if(s==='h'){p=V3(1.8,3.4,28-k*2);q=V3(1.8,5.6,1)}
  else if(s==='s2'){if(lt<ja-.6){p=V3(2,3.4,27-k);q=V3(1.8,5.4,1)}else{p=V3(-1.5,3,23);q=V3(-1.5,4.4,2)}}
  else{p=V3(1.6,2.1,31+k*1.5);q=V3(1.6,2.1+k*.2,0)}// v26: en el CTA el capataz queda ENCIMA del botón de seguir (y<1120)
  S.target.position.copy(q);S.position.set(q.x-16,34,q.z+18);S.target.updateMatrixWorld();S.intensity=2.6;gS.intensity=0;hemi.intensity=1.4}
 else if(s==='s1'||s==='s4'){bg=SPACE;S.intensity=0;hemi.intensity=.3;gS.intensity=3.2;
  gA.group.rotation.y=t*.3;gB.group.rotation.y=t*.3+1;
  const g2=s==='s1'?1+ss(.4,d*.55,lt):2;gB.group.scale.setScalar(g2);const gx=s==='s1'?1+(g2-1)*5:6;gB.group.position.set(gx,0,0);gA.group.position.set(s==='s1'?-10:-14,s==='s1'?-5:-6,0);
  lA.position.set(gA.group.position.x,gA.group.position.y-7.4,6);lB.position.set(gx,-5*g2-2.8,6);lA.scale.set(9,3.2,1);lB.scale.set(9,3.7,1);lB.visible=lA.visible=s==='s1';
  lM.visible=s==='s1'&&lt>d*.45;lG.visible=s==='s1'&&lt>d*.65;lM.position.set(-2,-17,8);lG.position.set(-2,-20.5,8);lM.scale.set(12,2.7,1);lG.scale.set(13,2.6,1);
  lS.visible=s==='s4'&&lt>.8;lH.visible=false;lS.scale.set(16,4.2,1);lS.position.set(5,-11.5,10);lH.position.set(6,14,6);
  others.forEach((o,i)=>{o.visible=s==='s4';o.rotation.y=t*.2*(i+1)});
  if(s==='s1'){p=V3(600.5+Math.sin(t*.2)*1.5,-6+k*2,100-k*6);q=V3(600.5,1,0)}else{p=V3(604+Math.sin(t*.25)*8,-4,74-k*6);q=V3(604,3,0)}}
 else{// s3: despegue
  const ta=Math.max(0,lt-.8);const y=1+1.6*ta*ta;rocket.position.y=y;rocket.rotation.y=t*.15;
  const fl=lt>.5?1:lt/.5;flame.visible=fg.visible=fl>0;flame.scale.set(1,(.8+.3*Math.sin(t*40))*fl*(1+ta*.3),1);flame.position.y=-2.4;fg.position.y=-1.5;fg.material.opacity=.9*fl;
  smoke.m.visible=true;for(let i=0;i<140;i++){const[a,b,c]=sm[i];const ph=((lt*.5+c)%1);const rr=1.5+ph*(5+b*7);smoke.set(i,1200+Math.cos(a)*rr,.8+ph*(1+b*2)+ (c<.3?y*ph*.6:0),Math.sin(a)*rr,fl*(.5+ph*1.4)*(1-ph*.5))}smoke.done();
  const hk=ss(1.5,d,lt);bg=LOW.clone().lerp(HIGH,hk);ST.visible=hk>.4;
  vHoy.visible=lt>d*.3;vLab.visible=lt>d*.55;vHoy.position.set(6.5,y+5,3);vLab.position.set(6.5,y+8.6,3);
  p=V3(1203,3+y*.85,54);q=V3(1202,13+y*.98,0);if(lt<1.2){p.x+=Math.sin(t*55)*.12}
  S.intensity=2.4;S.position.set(1180,40,40);S.target.position.set(1200,y,0);S.target.updateMatrixWorld();gS.intensity=0;hemi.intensity=1.2-.8*hk}
 scene.background=bg;const sp=bg===SPACE||(s==='s3');scene.fog.near=sp?1e4:60;scene.fog.far=sp?2e4:190;
 cam.position.copy(p);cam.lookAt(q);r.render(scene,cam)};
window.ready=true;
