// ¿Y si la Tierra girara al revés? (3204). Serie ¿QUÉ PASARÍA SI…? Parte 21. Fuentes en serie_reves.py.
// Reutilizable: GLOBO que frena y gira al revés (spinAngle), SALA DE SUPERORDENADOR con racks y LEDs (racks) y holograma,
// PLAZA AL AMANECER con el Sol saliendo por el OESTE y rosa de los vientos, nevada que llega, TERRENO DE VÓXELES que pasa de
// desierto a verde (o al revés) con una ola de color y árboles que brotan (makeLand).
import {THREE,J,mk,ss,V3,clamp,stage,sun,box,glow,capataz,segAt,mouthAt,label3d,stars,voxGlobe,puffs,snow} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x02030a,fog:null,exposure:1.1});cam.far=2500;cam.updateProjectionMatrix();const R=mk(3204);
const hemi=new THREE.HemisphereLight(0xdcefff,0xb8a080,.5);scene.add(hemi);
// ---------- GLOBO (h, cta) en z=-600
const GL=new THREE.Group();GL.position.set(0,0,-600);scene.add(GL);const ST=stars(scene,1500,{r0:300,r1:360,size:1.4});ST.position.copy(GL.position);
const tilt=new THREE.Group();tilt.rotation.z=23.5*Math.PI/180;GL.add(tilt);const glb=voxGlobe(9000,10);tilt.add(glb.group);
const ax=new THREE.Mesh(new THREE.CylinderGeometry(.2,.2,27,12),new THREE.MeshBasicMaterial({color:0xffd23a,toneMapped:false}));tilt.add(ax);
// flecha curva de giro (arco de cubos que recorre el ecuador)
const ARC=puffs(scene,26,.55,0xffd23a);const arcL=label3d(['*AL REVÉS'],{w:7,h:2.2,px:150,sprite:true,accent:'#ff5a4a'});GL.add(arcL);
const gS=new THREE.DirectionalLight(0xfff4e0,3.4);gS.position.set(560,60,-400);gS.target=GL;scene.add(gS);
// ángulo del globo: gira normal (oeste→este), frena, para y arranca al revés
const spinAngle=t=>{const t0=.6,t1=2.6;if(t<t0)return t*.9;if(t<t1){const u=(t-t0)/(t1-t0);return t0*.9+(t1-t0)*(.9*(u-u*u)-.9*u*u)}return t0*.9-(t-t1)*.9};
// ---------- SUPERORDENADOR (s1) en x=600
const SC=new THREE.Group();SC.position.set(600,0,0);scene.add(SC);
const sfl=new THREE.Mesh(new THREE.PlaneGeometry(80,80),new THREE.MeshStandardMaterial({color:0x1c2230,roughness:.5,metalness:.3}));sfl.rotation.x=-Math.PI/2;sfl.receiveShadow=true;SC.add(sfl);
for(let i=-10;i<=10;i++){const l=box(.05,.02,60,0x2a3346,.01);l.position.set(i*3,.01,0);SC.add(l)}
const LEDS=[];[-1,1].forEach(side=>{for(let j=0;j<7;j++){const rk=box(2.4,7,2.2,0x15181f,.06);rk.position.set(side*6,3.5,-4-j*3.2);SC.add(rk);
 for(let y=0;y<9;y++)for(let x=0;x<3;x++){const l=box(.22,.12,.06,0x103020,.01,{emissive:[0x2fd46b,0x4de3ff,0xffc23a][(x+y+j)%3],emissiveIntensity:0});l.position.set(side*6-side*1.22,1.1+y*.65,-4-j*3.2-.6+x*.6);l.rotation.y=side*Math.PI/2;SC.add(l);LEDS.push([l,R()*6,.5+R()*2])}}});
const holo=voxGlobe(2600,2.4,{cube:.32});holo.group.position.set(0,6.2,-9);SC.add(holo.group);const hg=glow(0x4de3ff,9,.5);hg.position.set(0,6.2,-9);SC.add(hg);
const ped=box(2.6,3.2,2.6,0x2a3346,.1);ped.position.set(0,1.6,-9);SC.add(ped);
const hero=capataz();hero.g.position.set(3.6,0,-2);hero.g.rotation.y=-.5;SC.add(hero.g);
const yrs=label3d(['*7.000','AÑOS SIMULADOS'],{w:5,h:2.2,px:130,sprite:true,accent:'#4de3ff'});yrs.position.set(-2.6,9.2,-9);SC.add(yrs);
const scL=new THREE.PointLight(0x4de3ff,40,30,1.6);scL.position.set(0,7,-6);SC.add(scL);
// ---------- PLAZA (s2) en x=-600: amanecer por el OESTE y luego nieve
const PZ=new THREE.Group();PZ.position.set(-600,0,0);scene.add(PZ);
const tiles=new THREE.Mesh(new THREE.PlaneGeometry(200,200),new THREE.MeshStandardMaterial({color:0xd9c8a8,roughness:.95}));tiles.rotation.x=-Math.PI/2;tiles.receiveShadow=true;PZ.add(tiles);
const snowG=new THREE.Mesh(new THREE.PlaneGeometry(200,200),new THREE.MeshStandardMaterial({color:0xeef4ff,roughness:.85,transparent:true,opacity:0}));snowG.rotation.x=-Math.PI/2;snowG.position.y=.05;PZ.add(snowG);
for(let i=0;i<8;i++){const h=8+R()*10,w=5+R()*3;const b=box(w,h,5,[0xe0b088,0xd8c0a0,0xc89878,0xe8d8c0][i%4],.1);b.position.set(-26+i*7.4,h/2,-20-R()*4);PZ.add(b)}
const roofs=[];for(let i=0;i<8;i++){const rf=box(6.6,.5,5.4,0xffffff,.05);rf.position.set(-26+i*7.4,0,-20);rf.visible=false;PZ.add(rf);roofs.push(rf)}
const hero2=capataz();hero2.g.position.set(1.5,0,-1);PZ.add(hero2.g);
const W1=label3d(['*OESTE'],{w:3.4,h:1.3,px:150,sprite:true,accent:'#ff9a3a'}),E1=label3d(['ESTE'],{w:2.8,h:1.1,px:130,sprite:true});PZ.add(W1,E1);W1.position.set(-3.6,8.5,-8);E1.position.set(2.6,8.5,-8);
const S2=sun(scene,{pos:[-640,8,-30],span:30,power:2.6,target:[-600,0,0]});
const sunD=new THREE.Mesh(new THREE.SphereGeometry(4,20,14),new THREE.MeshBasicMaterial({color:0xffd27a,toneMapped:false,fog:false}));scene.add(sunD);const sunDG=glow(0xff9a40,30,.85);scene.add(sunDG);
const WIND=puffs(scene,70,.11,0xffffff,{opacity:.7});
const SN=snow(scene,1600,[-630,-570,30,-25,22],{size:.28});
// ---------- TERRENOS (s3 Sáhara verde, s4 nuevos desiertos) en z=600
function makeLand(off,seed){const G=new THREE.Group();G.position.set(off,0,600);scene.add(G);const N=44,n=N*N;
 const im=new THREE.InstancedMesh(new THREE.BoxGeometry(1,1,1),new THREE.MeshStandardMaterial({roughness:.85}),n);im.receiveShadow=true;im.castShadow=true;G.add(im);
 const O=new THREE.Object3D(),C=new THREE.Color(),H=[];
 for(let i=0;i<N;i++)for(let j=0;j<N;j++){const x=(i-N/2),z=(j-N/2);const h=1+1.4*Math.max(0,Math.sin(x*.32+seed)+Math.sin(z*.21+x*.13+seed*2)*.8);H.push([x,z,h]);O.position.set(x,h/2,z);O.scale.set(1,h,1);O.updateMatrix();im.setMatrixAt(i*N+j,O.matrix)}
 const TR=[];for(let k=0;k<36;k++){const [x,z,h]=H[Math.floor(R()*n)];const g=new THREE.Group();const tr=box(.4,1.6,.4,0x6a4a2a,.04);tr.position.y=.8;g.add(tr);const lv=box(2.2,1.8,2.2,[0x3f9a3a,0x56b04a,0x2f8a3a][k%3],.25);lv.position.y=2.3;g.add(lv);g.position.set(x,h,z);G.add(g);TR.push([g,Math.hypot(x,z)])}
 const sandC=new THREE.Color(0xe8c07a),sandD=new THREE.Color(0xd4a45e),grnC=new THREE.Color(0x5aa84a),grnD=new THREE.Color(0x3f8a3a);
 return{G,set(f,toGreen){// f 0..1: ola de cambio desde el centro
  const R0=f*40;H.forEach(([x,z,h],i)=>{const d=Math.hypot(x,z);const w=clamp((R0-d)/4);const g=toGreen?w:1-w;const a=(i*7)%3?sandC:sandD,b=(i*5)%3?grnC:grnD;C.copy(a).lerp(b,g);C.multiplyScalar(.94+((i*13)%5)*.03);im.setColorAt(i,C)});im.instanceColor.needsUpdate=true;
  TR.forEach(([g,d])=>{const w=clamp((R0-d)/4);const s=toGreen?w:1-w;g.scale.setScalar(Math.max(.001,s));g.visible=s>.01})}}}
const SA=makeLand(0,1.3),AM=makeLand(200,4.1);
const sahL=label3d(['*SÁHARA'],{w:5.6,h:1.9,px:150,sprite:true,accent:'#4fd46b'});SA.G.add(sahL);sahL.visible=false;sahL.position.set(0,9,-6);
const amL=label3d(['*NUEVO','DESIERTO'],{w:5.6,h:2.4,px:140,sprite:true,accent:'#e8b86a'});AM.G.add(amL);amL.visible=false;amL.position.set(0,9.5,-6);
const SL=sun(scene,{pos:[30,40,630],span:40,power:2.8,target:[0,0,600]});
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],m=mouthAt(t),k=ss(0,d,lt);
 const set=(s==='h'||s==='cta')?'G':s==='s1'?'C':s==='s2'?'P':s==='s3'?'S':'A';
 GL.visible=ST.visible=set==='G';SC.visible=set==='C';PZ.visible=set==='P';SA.G.visible=set==='S';AM.G.visible=set==='A';
 sunD.visible=sunDG.visible=set==='P';SN.pts.visible=false;WIND.m.visible=set==='P';ARC.m.visible=set==='G';
 gS.intensity=set==='G'?3.4:0;S2.intensity=set==='P'?2.6:0;SL.intensity=(set==='S'||set==='A')?2.8:0;scL.intensity=set==='C'?40:0;
 let p,q;
 if(set==='G'){scene.background=new THREE.Color(0x02030a);hemi.intensity=.12;const tt=s==='h'?lt:3+lt;const a=spinAngle(tt);glb.group.rotation.y=a;
  // flecha: cubos en arco por delante del globo, avanzando en el sentido del giro
  const dir=tt<1.6?1:-1;for(let i=0;i<26;i++){const ph=((i/26)+(dir>0?1:-1)*tt*.18)%1;const ang=-.9+1.8*((ph+1)%1);const sc=Math.sin(Math.PI*((ph+1)%1));
   ARC.set(i,Math.sin(ang)*12.6,0,-600+Math.cos(ang)*12.6,sc*(tt>.4?1:0),0)}ARC.done();
  arcL.visible=tt>2.4;arcL.position.set(0,-11,4);
  p=V3(Math.sin(t*.3)*1.5,14,-534+k*4);q=V3(0,-1,-600)}
 else if(set==='C'){scene.background=new THREE.Color(0x05070d);hemi.intensity=.35;holo.group.rotation.y=-t*1.2;
  LEDS.forEach(([l,ph,sp])=>l.material.emissiveIntensity=Math.sin(t*sp*4+ph)>.2?2.2:.1);
  hero.pose(t,m*.4,{look:.3,point:lt>1?.7:0});yrs.visible=lt>1.2;
  p=V3(600+4-k*3,7.5,21-k*2.5);q=V3(600,5.5,-8)}
 else if(set==='P'){const u=ss(0,d*.45,lt),sn=ss(d*.45,d*.7,lt);// amanecer por el oeste y luego llega la nieve
  const el=-2+u*12;sunD.position.set(-611,14+u*30,-70);sunDG.position.copy(sunD.position);S2.position.set(-640,Math.max(2,el*3),-30);
  const sky=new THREE.Color(0xff9a5a).lerp(new THREE.Color(0x8ac8ff),u*.7).lerp(new THREE.Color(0x8a96aa),sn);scene.background=sky;hemi.intensity=.5+u*.4;
  snowG.material.opacity=sn;roofs.forEach(rf=>{rf.visible=sn>.2;rf.scale.y=sn});SN.pts.visible=sn>.05;if(sn>.05)SN.draw(t);
  for(let i=0;i<70;i++){const ph=(t*.6+i/70)%1;WIND.set(i,-600+26-ph*52,1.5+(i%7)*1.3+Math.sin(t*2+i)*.3,-12+(i%11)*2.2,1,0);}WIND.done();
  W1.visible=lt>.5;E1.visible=lt>.5;hero2.pose(t,m*.3,{look:-.3,point:lt>.8&&lt<d*.45?.7:0});hero2.g.rotation.y=-.9+sn*.9;
  p=V3(-600+3-k*2,5,26-k*3);q=V3(-600-2,9.5,-10)}
 else{const L=set==='S'?SA:AM;scene.background=new THREE.Color(set==='S'?0x9ad4ff:0xffd9a0);hemi.intensity=.8;
  const f=ss(.6,d-.8,lt);L.set(f,set==='S');const off=set==='S'?0:200;
  p=V3(off+Math.sin(t*.2)*6+18-k*6,22-k*4,600+30-k*4);q=V3(off,1.5,600-2)}
 cam.position.copy(p);cam.lookAt(q);r.render(scene,cam)};
window.ready=true;
