// ¿Y si la Tierra tuviera la gravedad de Júpiter? (3004). Serie ¿QUÉ PASARÍA SI…? Parte 19. Cálculos en serie_jupiterg.py. Basada en lunag.js.
// Nuevo: gasGiant() (Júpiter con bandas que se mueven y Gran Mancha Roja), saltitos de 19 cm en tiempo real, capataz que se aplasta al pesar más, caída entre nubes sin suelo.
// Basada en crece.js (plaza, báscula, regla). Nuevo y reutilizable: SALTO A TIEMPO REAL con gravedad g (jumpY), CANASTA a escala (hoop),
// DOS VASOS que caen a la vez con g distinta (cronómetros), y ATMÓSFERA QUE SE ESCAPA del globo (cubos azules que salen y se apagan).
import {THREE,J,mk,ss,V3,clamp,stage,sun,box,glow,pixTex,capataz,segAt,mouthAt,puffs,label3d,ruler,stars,voxGlobe,hoop,glassCup,gasGiant} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x8ad4ff,fog:[0xc8e4ff,70,220],exposure:1.08});cam.far=3000;cam.updateProjectionMatrix();const R=mk(3004);
const hemi=new THREE.HemisphereLight(0xdcefff,0x8a9a6a,1.4);scene.add(hemi);const S=sun(scene,{pos:[-16,34,18],span:34});
const SKY=new THREE.Color(0x8ad4ff),SPACE=new THREE.Color(0x02030a);
const U=1.75/4.1, G0=9.82, G1=25.92;// metros por unidad (el capataz mide ~4,1 u = 1,75 m)
// ---------- plaza
const st=new THREE.Group();scene.add(st);
const grass=pixTex(128,128,(g,w,h)=>{const q=mk(8);g.fillStyle='#6fb24e';g.fillRect(0,0,w,h);for(let i=0;i<700;i++){g.fillStyle=['#62a544','#7dbd58','#568f3c'][Math.floor(q()*3)];g.fillRect(Math.floor(q()*w/4)*4,Math.floor(q()*h/4)*4,4,4)}},[40,40]);
const gnd=new THREE.Mesh(new THREE.PlaneGeometry(400,400),new THREE.MeshStandardMaterial({map:grass,roughness:1}));gnd.rotation.x=-Math.PI/2;gnd.receiveShadow=true;st.add(gnd);
const plaza=new THREE.Mesh(new THREE.PlaneGeometry(40,22),new THREE.MeshStandardMaterial({map:pixTex(64,64,(g,w,h)=>{g.fillStyle='#d8cdb6';g.fillRect(0,0,w,h);g.strokeStyle='#b9ad94';g.lineWidth=2;for(let i=0;i<=w;i+=16){g.strokeRect(i,0,16,h);g.strokeRect(0,i,w,16)}},[10,6]),roughness:.95}));plaza.rotation.x=-Math.PI/2;plaza.position.set(0,.01,0);plaza.receiveShadow=true;st.add(plaza);
const COLS=[0xd9c7a8,0xc2573f,0x8fa6b8,0xe8dfca,0xa86a48,0x6f86a8];
[[-15,-14,8,14],[-5,-16,9,18],[6,-15,8,12],[16,-13,8,16],[-26,-10,7,11],[27,-10,7,13]].forEach(([x,z,w,h],i)=>{const b=box(w,h,7,COLS[i%6],.15);b.position.set(x,h/2,z);st.add(b);for(let y=1.5;y<h-1;y+=2.2)for(let a=-w/2+1.3;a<w/2-.8;a+=1.8){const wi=box(.9,1.2,.1,R()<.3?0xffe9a8:0x2a3a58,.02);wi.position.set(x+a,y,z+3.52);st.add(wi)}});
[[-9,4],[9,5],[-12,-4],[12,-5]].forEach(([x,z])=>{const tr=box(.6,2.4,.6,0x7a5232,.05);tr.position.set(x,1.2,z);st.add(tr);const cr=box(2.6,2.4,2.6,0x3f9a46,.3);cr.position.set(x,3.4,z);st.add(cr)});
// Júpiter grande en el cielo de día (el que 'presta' su gravedad)
const skyJ=gasGiant(9,{seed:6});skyJ.mesh.position.set(20,30,-60);skyJ.mesh.rotation.z=.25;st.add(skyJ.mesh);
// báscula + pantalla
const scale=new THREE.Group();const base=box(3.2,.4,2.6,0xe8eaf0,.12);base.position.y=.2;scale.add(base);const top=box(2.8,.12,2.2,0x30343e,.05);top.position.y=.46;scale.add(top);scale.position.set(0,0,2);st.add(scale);
const disp=label3d(['80 kg'],{w:4.2,h:1.6,px:150,accent:'#ff4a4a'});disp.position.set(3.4,3.5,2.6);st.add(disp);const dpost=box(.25,2.4,.25,0x30343e,.03);dpost.position.set(3.4,1.2,2.5);st.add(dpost);
const hero=capataz();hero.g.position.set(0,.52,2);scene.add(hero.g);
// regla de 1 m junto al salto + marca fantasma de 'hoy' (50 cm) y pico de Júpiter (19 cm)
const RU=ruler(1.0/U,{step:.1/U,every:5,unit:10,label:'cm',ls:1.3});RU.position.set(-2.4,0,2.9);st.add(RU);RU.children.filter(ch=>ch.geometry&&ch.geometry.type==='PlaneGeometry').forEach(ch=>ch.visible=false);
const RUl=[0,50,100].map(m=>{const l=label3d([`${m} cm`],{w:2.4,h:.8,bg:null,px:200});l.position.set(-4.4,.52+m/100/U,3.1);st.add(l);return l});
const HP=hoop(U);HP.visible=false;
const ghostM=new THREE.MeshBasicMaterial({color:0x4de3ff,transparent:true,opacity:.7,toneMapped:false});const ghost=new THREE.Mesh(new THREE.BoxGeometry(3.2,.1,.1),ghostM);ghost.position.set(-.8,.52+.5/U,2.9);st.add(ghost);
const gLab=label3d(['HOY 50 cm'],{w:3,h:.8,px:110,bg:'#0d2a3a',accent:'#4de3ff'});gLab.position.set(2.6,.52+.5/U+.3,3.2);st.add(gLab);
const peakM=new THREE.Mesh(new THREE.BoxGeometry(3.2,.12,.12),new THREE.MeshBasicMaterial({color:0xffc23a,toneMapped:false}));peakM.position.set(-.8,.52+.19/U,2.9);st.add(peakM);
const jLab=label3d(['*19 cm'],{w:3.0,h:.95,px:130});jLab.position.set(2.6,.52+.19/U-.25,3.2);st.add(jLab);
const dust=puffs(scene,60,.3,0xcbbfa6,{opacity:.85,depthWrite:false});const dp=[];for(let i=0;i<60;i++)dp.push([R()*6.28,R()]);
// mesa con dos vasos (s3): uno cae con g de hoy y otro con g lunar
const TB=new THREE.Group();TB.position.set(0,0,-2);st.add(TB);const H15=1.5/U;
[-1.9,1.9].forEach(x=>{const t1=box(3.0,.3,2.4,0x8a5a3a,.06);t1.position.set(x,H15-.15,0);TB.add(t1);[[-1.2,-1],[1.2,-1],[-1.2,1],[1.2,1]].forEach(([a,b])=>{const l=box(.25,H15-.3,.25,0x6a4228,.03);l.position.set(x+a,(H15-.3)/2,b);TB.add(l)})});
const cupA=glassCup(),cupB=glassCup();cupA.scale.setScalar(1.6);cupB.scale.setScalar(1.6);TB.add(cupA,cupB);
const tA=label3d(['HOY','0,55 s'],{w:3.4,h:1.6,px:110,sprite:true,accent:'#4de3ff'});const tB=label3d(['JÚPITER','*0,34 s'],{w:3.4,h:1.6,px:110,sprite:true});TB.add(tA,tB);
const splash=puffs(scene,40,.18,0x9ad8ff,{opacity:.9,depthWrite:false});const sp=[];for(let i=0;i<40;i++)sp.push([R()*6.28,R()]);
// ---------- espacio: Tierra pequeña y Júpiter; en s4 la capataz cae entre las nubes (no hay suelo)
const GL=new THREE.Group();GL.position.set(600,0,0);scene.add(GL);const gE=voxGlobe(8000,6);GL.add(gE.group);
const JP=gasGiant(7,{seed:4});GL.add(JP.mesh);
const lE=label3d(['TIERRA','*9,8'],{w:4.4,h:2,px:120,sprite:true,accent:'#4de3ff'});const lMo=label3d(['JÚPITER','*25,9'],{w:4.4,h:2,px:120,sprite:true});GL.add(lE,lMo);
const lD=label3d(['*GRAVEDAD ×2,6'],{w:9,h:1.8,px:140,sprite:true,accent:'#ff4a4a'});GL.add(lD);
const lAir=label3d(['*SIN SUELO'],{w:7,h:1.5,px:130,sprite:true,accent:'#ffc23a'});GL.add(lAir);
const hero2=capataz();hero2.g.scale.setScalar(.42);GL.add(hero2.g);
const air=puffs(scene,220,.22,0xd9b98f,{opacity:.55,depthWrite:false});const ap=[];for(let i=0;i<220;i++)ap.push([R()*2-1,R(),R()*2-1,R()]);
const gS=new THREE.DirectionalLight(0xffffff,0);gS.position.set(560,30,60);gS.target.position.set(600,0,0);scene.add(gS,gS.target);
const ST=stars(scene,1400);ST.position.set(600,0,0);
const kgAt=(s,lt)=>s==='h'?80+131*ss(.8,2.6,lt):s==='cta'?null:211;
const JT=2*Math.sqrt(2*G1*.19)/G1;const jumpY=(lt,a)=>{const v=Math.sqrt(2*G1*.19);let u=lt-a;if(u<0)return 0;u=u%1.5;return u<JT?(v*u-.5*G1*u*u)/U:0};// saltitos reales con g de Júpiter (19 cm de pico), uno cada 1,5 s
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],k=ss(0,d,lt),m=mouthAt(t);let p,q,bg=SKY;
 const onP=s!=='s1'&&s!=='s4';st.visible=onP;hero.g.visible=onP&&s!=='s3';GL.visible=!onP;ST.visible=!onP;dust.m.visible=false;splash.m.visible=false;air.m.visible=false;skyJ.tick(t);
 const jumpOn=s==='s2';RU.visible=jumpOn;RUl.forEach(l=>l.visible=jumpOn);TB.visible=s==='s3';
 ghost.visible=gLab.visible=jumpOn&&lt>.3;peakM.visible=jumpOn&&lt>1.0;jLab.visible=jumpOn&&lt>1.2;disp.visible=dpost.visible=s==='h'||s==='cta';scale.visible=s==='h'||s==='cta';
 if(s==='h'||s==='cta'||s==='s2'){
  const kg=kgAt(s,lt);disp.set(kg==null?['¿Y TÚ?']:[`*${Math.round(kg)} kg`]);scale.position.x=s==='h'&&lt>.8&&lt<2.8?Math.sin(t*50)*.04:0;
  // al pesar más, la capataz se aplasta un poco (y el suelo suelta polvo al 'caer' el peso)
  const sq=s==='h'?ss(.8,2.6,lt):s==='s2'?1:0;hero.g.scale.set(1+.07*sq,1-.11*sq,1+.07*sq);
  let jy=0;if(s==='s2'){hero.g.position.x=-.2;jy=jumpY(lt,.6);const u=((lt-.6)%1.5-JT)/.6;if(lt>.6+JT&&u>=0&&u<1){dust.m.visible=true;for(let i=0;i<60;i++){const[a,b]=dp[i];const rr=.5+u*(1.0+b*1.5);dust.set(i,-.2+Math.cos(a)*rr,.6+u*b*.5,2+Math.sin(a)*rr*.6,(1-u)*(.6+b))}dust.done()}}
  else{hero.g.position.x=0;if(s==='h'&&lt>1.2&&lt<2.6){const u=(lt-1.2)/1.4;dust.m.visible=true;for(let i=0;i<60;i++){const[a,b]=dp[i];const rr=1.2+u*(1.2+b*2);dust.set(i,Math.cos(a)*rr,.5+u*b*.6,2+Math.sin(a)*rr*.6,(1-u)*(.6+b))}dust.done()}}
  hero.g.position.y=.52+jy;
  hero.pose(t,m,{wave:s==='cta'?1:0,armsUp:jy>0?.6:0,look:s==='h'?.55:s==='cta'?0:.25});
  if(s==='h'){p=V3(1.8,3.4,28-k*2);q=V3(1.8,5.6,1)}
  else if(s==='s2'){p=V3(-.6+Math.sin(t*.4)*.5,2.8,31-k*2);q=V3(-.6,2.9,1)}
  else{p=V3(1.6,2.1,31+k*1.5);q=V3(1.6,2.1+k*.2,0)}
  S.target.position.copy(q);S.position.set(q.x-16,34,q.z+18);S.target.updateMatrixWorld();S.intensity=2.6;gS.intensity=0;hemi.intensity=1.4}
 else if(s==='s3'){// dos vasos caen a la vez desde 1,5 m, en tiempo real, en bucle: el de Júpiter llega mucho antes
  const cyc=1.6,u=(lt-.4)%cyc,on=lt>.4;
  [[cupA,G0,-1.9,tA],[cupB,G1,1.9,tB]].forEach(([c,g,x,lb],i)=>{const tf=Math.sqrt(2*1.5/g);const uu=on?Math.min(u,tf):0;const y=(1.5-.5*g*uu*uu)/U;c.position.set(x,Math.max(0,y),1.4);c.rotation.z=on?(uu/tf)*(i?1.2:1.4)*(x<0?1:-1):0;
   if(on&&u>=tf){c.position.y=0;c.rotation.z=(x<0?1:-1)*1.57;splash.m.visible=true;const w=clamp((u-tf)/.5);for(let j=0;j<20;j++){const[a,b]=sp[j+i*20];splash.set(j+i*20,x+Math.cos(a)*w*(1+b)*1.4,.3+w*(1-w)*2*b,-.6+Math.sin(a)*w*.8,(1-w)*1.2)}}
   lb.position.set(x,H15+1.9,1.4);lb.scale.set(3.4,1.6,1)});splash.done();
  p=V3(Math.sin(t*.3)*.8,4.6,23-k*1.2);q=V3(0,5.2,-1);S.target.position.set(0,0,0);S.position.set(-16,34,18);S.target.updateMatrixWorld();S.intensity=2.6;hemi.intensity=1.4}
 else{bg=SPACE;S.intensity=0;hemi.intensity=.35;gS.intensity=3.2;gE.group.rotation.y=t*.3;JP.tick(t);
  if(s==='s1'){gE.group.visible=true;gE.group.scale.setScalar(.5);gE.group.position.set(-6,-6,0);JP.mesh.position.set(4.5,-9.5,0);hero2.g.visible=false;
   lE.position.set(-6,-10.6,6);lMo.position.set(4.5,-17.8,8);lE.scale.set(7,3.2,1);lMo.scale.set(7,3.2,1);lE.visible=lt>.6;lMo.visible=lt>1.2;
   lD.visible=lt>d*.45;lD.position.set(-5,-15.2,7);lD.scale.set(9.5,1.9,1);lAir.visible=false;
   p=V3(600.5+Math.sin(t*.2)*.8,-6+k*.8,72-k*4);q=V3(600.5,-5.5,0)}
  else{// s4: la capataz cae entre las nubes de Júpiter: no hay suelo donde ponerse de pie
   gE.group.visible=false;lE.visible=lMo.visible=lD.visible=false;JP.mesh.position.set(5,-9,0);
   const cx=604.5,cy=-9.5,cz=7.0;hero2.g.visible=true;const sink=ss(.3,d,lt);hero2.g.position.set(cx-600-.15,cy+.2-sink*1.3,cz+1.6-sink*.5);
   hero2.pose(t,m,{armsUp:.9,look:0});hero2.g.rotation.z=Math.sin(t*2.2)*.12;
   air.m.visible=true;for(let i=0;i<220;i++){const[x,y,z,ph]=ap[i];const f=((t*.12+ph)%1);air.set(i,cx+x*4.5+f*3-1.5,cy-1.6+y*1.6,cz+1.2+z*1.2,.6+ph*.8)}air.done();
   lAir.visible=lt>d*.4;lAir.position.set(cx-600,cy-2.7,cz+2.2);lAir.scale.set(3.6,.8,1);
   p=V3(cx+Math.sin(t*.25)*.6,cy+1.2-k*.6,cz+15-k*2);q=V3(cx,cy-.2,cz+1)}}
 scene.background=bg;const spc=bg===SPACE;scene.fog.near=spc?1e4:70;scene.fog.far=spc?2e4:220;
 cam.position.copy(p);cam.lookAt(q);r.render(scene,cam)};
window.ready=true;
