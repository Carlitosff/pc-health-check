// ¿Y si la Tierra tuviera la gravedad de la Luna? (2904). Serie ¿QUÉ PASARÍA SI…? Parte 18. Cálculos en serie_lunag.py.
// Basada en crece.js (plaza, báscula, regla). Nuevo y reutilizable: SALTO A TIEMPO REAL con gravedad g (jumpY), CANASTA a escala (hoop),
// DOS VASOS que caen a la vez con g distinta (cronómetros), y ATMÓSFERA QUE SE ESCAPA del globo (cubos azules que salen y se apagan).
import {THREE,J,mk,ss,V3,clamp,stage,sun,box,glow,pixTex,capataz,segAt,mouthAt,puffs,label3d,ruler,stars,voxGlobe,hoop,glassCup} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x8ad4ff,fog:[0xc8e4ff,70,220],exposure:1.08});cam.far=3000;cam.updateProjectionMatrix();const R=mk(2904);
const hemi=new THREE.HemisphereLight(0xdcefff,0x8a9a6a,1.4);scene.add(hemi);const S=sun(scene,{pos:[-16,34,18],span:34});
const SKY=new THREE.Color(0x8ad4ff),SPACE=new THREE.Color(0x02030a);
const U=1.75/4.1, G0=9.81, G1=1.62;// metros por unidad (el capataz mide ~4,1 u = 1,75 m)
// ---------- plaza
const st=new THREE.Group();scene.add(st);
const grass=pixTex(128,128,(g,w,h)=>{const q=mk(8);g.fillStyle='#6fb24e';g.fillRect(0,0,w,h);for(let i=0;i<700;i++){g.fillStyle=['#62a544','#7dbd58','#568f3c'][Math.floor(q()*3)];g.fillRect(Math.floor(q()*w/4)*4,Math.floor(q()*h/4)*4,4,4)}},[40,40]);
const gnd=new THREE.Mesh(new THREE.PlaneGeometry(400,400),new THREE.MeshStandardMaterial({map:grass,roughness:1}));gnd.rotation.x=-Math.PI/2;gnd.receiveShadow=true;st.add(gnd);
const plaza=new THREE.Mesh(new THREE.PlaneGeometry(40,22),new THREE.MeshStandardMaterial({map:pixTex(64,64,(g,w,h)=>{g.fillStyle='#d8cdb6';g.fillRect(0,0,w,h);g.strokeStyle='#b9ad94';g.lineWidth=2;for(let i=0;i<=w;i+=16){g.strokeRect(i,0,16,h);g.strokeRect(0,i,w,16)}},[10,6]),roughness:.95}));plaza.rotation.x=-Math.PI/2;plaza.position.set(0,.01,0);plaza.receiveShadow=true;st.add(plaza);
const COLS=[0xd9c7a8,0xc2573f,0x8fa6b8,0xe8dfca,0xa86a48,0x6f86a8];
[[-15,-14,8,14],[-5,-16,9,18],[6,-15,8,12],[16,-13,8,16],[-26,-10,7,11],[27,-10,7,13]].forEach(([x,z,w,h],i)=>{const b=box(w,h,7,COLS[i%6],.15);b.position.set(x,h/2,z);st.add(b);for(let y=1.5;y<h-1;y+=2.2)for(let a=-w/2+1.3;a<w/2-.8;a+=1.8){const wi=box(.9,1.2,.1,R()<.3?0xffe9a8:0x2a3a58,.02);wi.position.set(x+a,y,z+3.52);st.add(wi)}});
[[-9,4],[9,5],[-12,-4],[12,-5]].forEach(([x,z])=>{const tr=box(.6,2.4,.6,0x7a5232,.05);tr.position.set(x,1.2,z);st.add(tr);const cr=box(2.6,2.4,2.6,0x3f9a46,.3);cr.position.set(x,3.4,z);st.add(cr)});
// Luna grande en el cielo de día (la que 'presta' su gravedad)
const skyMoon=new THREE.Mesh(new THREE.SphereGeometry(5,32,24),new THREE.MeshStandardMaterial({color:0xe8e6e0,roughness:1,emissive:0x6a6a70,emissiveIntensity:.5,map:pixTex(64,32,(g,w,h)=>{const q=mk(3);g.fillStyle='#ddd';g.fillRect(0,0,w,h);for(let i=0;i<40;i++){g.fillStyle=`rgba(90,90,100,${.15+q()*.25})`;g.beginPath();g.arc(q()*w,q()*h,1+q()*5,0,7);g.fill()}})}));skyMoon.position.set(22,34,-60);st.add(skyMoon);
// báscula + pantalla
const scale=new THREE.Group();const base=box(3.2,.4,2.6,0xe8eaf0,.12);base.position.y=.2;scale.add(base);const top=box(2.8,.12,2.2,0x30343e,.05);top.position.y=.46;scale.add(top);scale.position.set(0,0,2);st.add(scale);
const disp=label3d(['80 kg'],{w:4.2,h:1.6,px:150,accent:'#ff4a4a'});disp.position.set(3.4,3.5,2.6);st.add(disp);const dpost=box(.25,2.4,.25,0x30343e,.03);dpost.position.set(3.4,1.2,2.5);st.add(dpost);
const hero=capataz();hero.g.position.set(0,.52,2);scene.add(hero.g);
// regla de 3,5 m junto al salto + canasta + marca fantasma de 'hoy' (50 cm)
const RU=ruler(3.5/U,{step:.25/U,every:4,unit:100,label:'cm',ls:1.3});RU.children.forEach(ch=>{if(ch.isMesh&&ch.material.map&&ch.geometry.type==='PlaneGeometry'){}});RU.position.set(-2.4,0,2.9);st.add(RU);
// la regla rotula 0,100,200,300 cm → mejor en metros
const RUl=[0,1,2,3].map(m=>{const l=label3d([`${m} m`],{w:2.4,h:.8,bg:null,px:200});l.position.set(-4.4,m/U,3.1);st.add(l);return l});RU.children.filter(ch=>ch.geometry&&ch.geometry.type==='PlaneGeometry').forEach(ch=>ch.visible=false);
const HP=hoop(U);HP.position.set(4.6,0,0.6);st.add(HP);
const ghostM=new THREE.MeshBasicMaterial({color:0x4de3ff,transparent:true,opacity:.7,toneMapped:false});const ghost=new THREE.Mesh(new THREE.BoxGeometry(3.2,.1,.1),ghostM);ghost.position.set(-.8,.52+.5/U,2.9);st.add(ghost);
const gLab=label3d(['HOY 50 cm'],{w:3,h:.8,px:110,bg:'#0d2a3a',accent:'#4de3ff'});gLab.position.set(-5.3,.52+.5/U,3.2);st.add(gLab);
const peakM=new THREE.Mesh(new THREE.BoxGeometry(3.2,.12,.12),new THREE.MeshBasicMaterial({color:0xffc23a,toneMapped:false}));peakM.position.set(-.8,.52+3/U,2.9);st.add(peakM);
const jLab=label3d(['*3 METROS'],{w:3.2,h:.95,px:130});jLab.position.set(-5.3,.52+3/U,3.2);st.add(jLab);
const dust=puffs(scene,60,.3,0xcbbfa6,{opacity:.85,depthWrite:false});const dp=[];for(let i=0;i<60;i++)dp.push([R()*6.28,R()]);
// mesa con dos vasos (s3): uno cae con g de hoy y otro con g lunar
const TB=new THREE.Group();TB.position.set(0,0,-2);st.add(TB);const H15=1.5/U;
[-1.9,1.9].forEach(x=>{const t1=box(3.0,.3,2.4,0x8a5a3a,.06);t1.position.set(x,H15-.15,0);TB.add(t1);[[-1.2,-1],[1.2,-1],[-1.2,1],[1.2,1]].forEach(([a,b])=>{const l=box(.25,H15-.3,.25,0x6a4228,.03);l.position.set(x+a,(H15-.3)/2,b);TB.add(l)})});
const cupA=glassCup(),cupB=glassCup();cupA.scale.setScalar(1.6);cupB.scale.setScalar(1.6);TB.add(cupA,cupB);
const tA=label3d(['HOY','*0,55 s'],{w:3.4,h:1.6,px:110,sprite:true,accent:'#4de3ff'});const tB=label3d(['LUNA','*1,36 s'],{w:3.4,h:1.6,px:110,sprite:true});TB.add(tA,tB);
const splash=puffs(scene,40,.18,0x9ad8ff,{opacity:.9,depthWrite:false});const sp=[];for(let i=0;i<40;i++)sp.push([R()*6.28,R()]);
// ---------- espacio: Tierra y Luna, atmósfera que se escapa
const GL=new THREE.Group();GL.position.set(600,0,0);scene.add(GL);const gE=voxGlobe(8000,6);GL.add(gE.group);
const moonG=new THREE.Mesh(new THREE.SphereGeometry(2.2,32,24),new THREE.MeshStandardMaterial({color:0xcfcdc8,roughness:1,map:skyMoon.material.map}));GL.add(moonG);
const lE=label3d(['TIERRA','*9,81'],{w:4.4,h:2,px:120,sprite:true,accent:'#4de3ff'});const lMo=label3d(['LUNA','*1,62'],{w:4.4,h:2,px:120,sprite:true});GL.add(lE,lMo);
const lD=label3d(['*GRAVEDAD ÷6'],{w:9,h:1.8,px:140,sprite:true,accent:'#ff4a4a'});GL.add(lD);
const lAir=label3d(['*CASI SIN AIRE'],{w:7,h:1.5,px:130,sprite:true,accent:'#cfcdc8'});GL.add(lAir);
const air=puffs(scene,220,.32,0x7fc8ff,{opacity:.85,depthWrite:false,blending:THREE.AdditiveBlending});const ap=[];for(let i=0;i<220;i++){const y=1-2*R(),a=R()*6.28,rr=Math.sqrt(1-y*y);ap.push([Math.cos(a)*rr,y,Math.sin(a)*rr,R()])}
const gS=new THREE.DirectionalLight(0xffffff,0);gS.position.set(560,30,60);gS.target.position.set(600,0,0);scene.add(gS,gS.target);
const ST=stars(scene,1400);ST.position.set(600,0,0);
const kgAt=(s,lt)=>s==='h'?80-67*ss(.8,2.6,lt):s==='cta'?null:13;
const jumpY=(lt,a)=>{const v=Math.sqrt(2*G1*3.0),T=2*v/G1;const u=lt-a;return u>0&&u<T?(v*u-.5*G1*u*u)/U:0};// salto real con g lunar (3,0 m de pico)
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],k=ss(0,d,lt),m=mouthAt(t);let p,q,bg=SKY;
 const onP=s!=='s1'&&s!=='s4';st.visible=onP;hero.g.visible=onP&&s!=='s3';GL.visible=!onP;ST.visible=!onP;dust.m.visible=false;splash.m.visible=false;air.m.visible=false;
 const jumpOn=s==='s2';RU.visible=jumpOn;RUl.forEach(l=>l.visible=jumpOn);HP.visible=jumpOn||s==='cta';TB.visible=s==='s3';
 ghost.visible=gLab.visible=jumpOn&&lt>.3;peakM.visible=jumpOn&&lt>1.6;jLab.visible=jumpOn&&lt>2.0;disp.visible=dpost.visible=s==='h'||s==='cta';scale.visible=s==='h'||s==='cta';
 if(s==='h'||s==='cta'||s==='s2'){
  const kg=kgAt(s,lt);disp.set(kg==null?['¿Y TÚ?']:[`*${Math.round(kg)} kg`]);scale.position.x=s==='h'&&lt>.8&&lt<2.8?Math.sin(t*50)*.03:0;
  let jy=0;if(s==='s2'){hero.g.position.x=-.2;jy=jumpY(lt,.5);const T=2*Math.sqrt(2*G1*3)/G1;if(lt>.5+T){const u=clamp((lt-.5-T)/1.1);dust.m.visible=u<1;for(let i=0;i<60;i++){const[a,b]=dp[i];const rr=.6+u*(1.5+b*2);dust.set(i,-.2+Math.cos(a)*rr,.6+u*b*.8,2+Math.sin(a)*rr*.6,(1-u)*(.7+b))}dust.done()}}else hero.g.position.x=0;
  // en el gancho el capataz 'flota' un poco al quedarse ligero
  const fl=s==='h'?.35*ss(1.6,3,lt)*(.5+.5*Math.sin(t*3)):0;hero.g.position.y=.52+jy+fl;
  hero.pose(t,m,{wave:s==='cta'?1:0,armsUp:jy>0?.8:s==='h'&&lt>2?.4:0,look:s==='h'?.55:s==='cta'?0:.25});
  if(s==='h'){p=V3(1.8,3.4,28-k*2);q=V3(1.8,5.6,1)}
  else if(s==='s2'){p=V3(-.6+Math.sin(t*.4)*1.0,6,42-k*2);q=V3(-.6,9.2,1)}
  else{p=V3(1.6,2.1,31+k*1.5);q=V3(1.6,2.1+k*.2,0)}// en el CTA el capataz queda ENCIMA del botón de seguir
  S.target.position.copy(q);S.position.set(q.x-16,34,q.z+18);S.target.updateMatrixWorld();S.intensity=2.6;gS.intensity=0;hemi.intensity=1.4}
 else if(s==='s3'){// dos vasos caen a la vez desde 1,5 m, en tiempo real, en bucle
  const cyc=2.1,u=(lt-.4)%cyc,on=lt>.4;
  [[cupA,G0,-1.9,tA],[cupB,G1,1.9,tB]].forEach(([c,g,x,lb],i)=>{const tf=Math.sqrt(2*1.5/g);const uu=on?Math.min(u,tf):0;const y=(1.5-.5*g*uu*uu)/U;c.position.set(x,Math.max(0,y),1.4);c.rotation.z=on?(uu/tf)*(i?1.2:1.4)*(x<0?1:-1):0;
   if(on&&u>=tf){c.position.y=0;c.rotation.z=(x<0?1:-1)*1.57;if(i===0||u<cyc){splash.m.visible=true;const w=clamp((u-tf)/.5);for(let j=0;j<20;j++){const[a,b]=sp[j+i*20];splash.set(j+i*20,x+Math.cos(a)*w*(1+b)*1.4,.3+w*(1-w)*2*b,-.6+Math.sin(a)*w*.8,(1-w)*1.2)}}}
   lb.position.set(x,H15+1.9,1.4);lb.scale.set(3.4,1.6,1)});splash.done();
  p=V3(Math.sin(t*.3)*.8,4.6,23-k*1.2);q=V3(0,5.2,-1);S.target.position.set(0,0,0);S.position.set(-16,34,18);S.target.updateMatrixWorld();S.intensity=2.6;hemi.intensity=1.4}
 else{bg=SPACE;S.intensity=0;hemi.intensity=.3;gS.intensity=3.2;gE.group.rotation.y=t*.3;moonG.rotation.y=t*.2;
  if(s==='s1'){gE.group.position.set(-1.5,2.5,0);moonG.position.set(4.5,-7,2);lE.position.set(-2.2,-5.2,6);lMo.position.set(5.5,-11.6,6);lE.scale.set(9,4.1,1);lMo.scale.set(9,4.1,1);lE.visible=lt>.6;lMo.visible=lt>1.2;
   lD.visible=lt>d*.5;lD.position.set(0,-16.5,7);lD.scale.set(13,2.6,1);lAir.visible=false;
   p=V3(601+Math.sin(t*.2)*1.5,-5+k*1.5,62-k*5);q=V3(601,-4.5,0)}
  else{// s4: el aire sale del globo y se apaga; la Luna al lado, casi sin aire
   gE.group.position.set(-2,0,0);moonG.position.set(9,-9,2);lE.visible=lMo.visible=lD.visible=false;lAir.visible=lt>d*.45;lAir.position.set(9,-12.6,5);lAir.scale.set(10,2.1,1);
   air.m.visible=true;const rate=.25+.75*ss(0,d*.5,lt);for(let i=0;i<220;i++){const[x,y,z,ph]=ap[i];const f=((t*.22*rate+ph)%1);const rr=6.6+f*16;air.set(i,598+x*rr,y*rr,z*rr,(1-f)*1.4)}air.done();
   gE.group.children[gE.group.children.length-1].material.opacity=.35*(1-.6*ss(0,d,lt));
   p=V3(603+Math.sin(t*.25)*4,-4,70-k*5);q=V3(603,-3.5,0)}}
 scene.background=bg;const spc=bg===SPACE;scene.fog.near=spc?1e4:70;scene.fog.far=spc?2e4:220;
 cam.position.copy(p);cam.lookAt(q);r.render(scene,cam)};
window.ready=true;
