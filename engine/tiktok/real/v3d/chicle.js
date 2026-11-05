// Mito del chicle (1303): dentro de tu estómago. Reutilizable: túnel de cubos con peristalsis (tripa), balsa, panel LED integrado, salón de la abuela.
import {THREE,J,mk,ss,V3,clamp,stage,sun,box,glow,pixTex,capataz,abuela,camera,segAt,mouthAt} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x2a0710,fog:[0x3a0a14,24,92],exposure:1.2});const R=mk(1303);
const hemi=new THREE.HemisphereLight(0xffc0c8,0x401020,1.25);scene.add(hemi);const S=sun(scene,{pos:[-8,16,16],span:14,color:0xfff0e0,power:2.4});
const fill2=new THREE.PointLight(0xff5a78,60,40,1.6);fill2.position.set(5,6,6);scene.add(fill2);
const gut=new THREE.Group();scene.add(gut);
// túnel: anillos de cubos que respiran
const NR=72,NA=44,RS=1.5,RL=NR*RS;const tun=new THREE.InstancedMesh(new THREE.BoxGeometry(1.2,1.2,1.42),new THREE.MeshStandardMaterial({roughness:.42,metalness:.02}),NR*NA);tun.frustumCulled=false;gut.add(tun);
const O=new THREE.Object3D(),C=new THREE.Color(),P1=new THREE.Color(0xd8354f),P2=new THREE.Color(0xa81f3c),P3=new THREE.Color(0xff7a8c);
function drawTun(t,zoff){let i=0;for(let a=0;a<NR;a++){const z=((a*RS+zoff)%RL+RL)%RL-RL+48;for(let b=0;b<NA;b++){const th=b/NA*6.2832;const fold=Math.sin(th*6+z*.45);const rad=8.2+Math.sin(z*.34-t*2.2)*.75+fold*.28;O.position.set(Math.cos(th)*rad,Math.sin(th)*rad+2.2,z);O.rotation.set(0,0,th);O.updateMatrix();tun.setMatrixAt(i,O.matrix);C.copy(fold>.3?P3:(fold>-.3?P1:P2));C.multiplyScalar(.9+((a*5+b*3)%5)*.05);tun.setColorAt(i,C);i++}}O.rotation.set(0,0,0);tun.instanceMatrix.needsUpdate=true;tun.instanceColor.needsUpdate=true}
// ácido: cubos verdes con olas
const AX=20,AZ=66,acid=new THREE.InstancedMesh(new THREE.BoxGeometry(1,1,1),new THREE.MeshStandardMaterial({roughness:.6,emissive:0x2a6a10,emissiveIntensity:.55}),AX*AZ);acid.frustumCulled=false;acid.receiveShadow=true;gut.add(acid);
const G1=new THREE.Color(0x9ff23a),G2=new THREE.Color(0x63c524),G3=new THREE.Color(0xe6ff8a);
function drawAcid(t,zoff){let i=0;for(let a=0;a<AX;a++)for(let b=0;b<AZ;b++){const x=a-AX/2+.5;const z=((b+zoff)%AZ+AZ)%AZ-AZ+44;const y=Math.sin(x*.7+t*1.7)*.12+Math.sin(z*.6-t*2.2)*.14;O.position.set(x,y-.62,z);O.updateMatrix();acid.setMatrixAt(i,O.matrix);C.copy(G1).lerp(G2,.5+.5*Math.sin(a*2.1+b*1.3));C.lerp(G3,clamp((y-.1)*4));acid.setColorAt(i,C);i++}acid.instanceMatrix.needsUpdate=true;acid.instanceColor.needsUpdate=true}
// balsa
const raft=new THREE.Group();gut.add(raft);for(let i=0;i<6;i++){const b=box(1.02,.42,4.2,i%2?0x9a6a3a:0x87592f,.05);b.position.set(-2.55+i*1.02,.15,0);raft.add(b)}
const hero=capataz();raft.add(hero.g);
const lamp=glow(0xfff0b0,3.2,.8);lamp.position.set(0,4.6,.9);hero.head.add(lamp);lamp.position.set(0,.9,.9);
// chicle: bloque rosa mordisqueado
const gumMat=()=>new THREE.MeshStandardMaterial({color:0xff6fb8,roughness:.3,metalness:.02,emissive:0x5a1036,emissiveIntensity:.35});
function makeGum(s=1,col){const g=new THREE.Group();const lumps=[[0,0,0,2.2],[-.7,.3,.3,1.5],[.7,.45,-.2,1.6],[.1,.85,.2,1.4],[-.3,-.35,-.5,1.5],[.55,-.3,.55,1.2]];lumps.forEach(([x,y,z,w])=>{const m=box(w,w*.86,w,col||0xff6fb8,.32,{roughness:.28,emissive:0x5a1036,emissiveIntensity:.35});m.position.set(x,y,z);m.castShadow=true;g.add(m)});g.scale.setScalar(s);return g}
const gum=makeGum(1);gum.position.set(1.42,2.0,.2);raft.add(gum);
// enzimas: cubitos verdes que rebotan sin poder con él
const enz=[];for(let i=0;i<14;i++){const g=box(.42,.42,.42,0x7dff5a,.08,{emissive:0x2f8a1a,emissiveIntensity:.6});const eye=box(.2,.14,.03,0x101808,.01);eye.position.z=.22;g.add(eye);g.userData={a:R()*6.28,b:(R()-.5)*1.6,p:R()*2,sp:.9+R()*.8};raft.add(g);enz.push(g)}
// gotas de ácido desde el techo
const drops=[];for(let i=0;i<26;i++){const d=box(.2,.42,.2,0xc4ff5a,.05,{emissive:0x4a9a10,emissiveIntensity:.8});d.userData={x:(R()-.5)*9,z:(R()-.5)*9,p:R(),v:.5+R()*.6};gut.add(d);drops.push(d)}
// panel LED colgado: los datos viven en la escena
const pc=document.createElement('canvas');pc.width=512;pc.height=320;const pg=pc.getContext('2d');const pT=new THREE.CanvasTexture(pc);pT.colorSpace=THREE.SRGBColorSpace;const panel=new THREE.Group();{const sc=new THREE.Mesh(new THREE.BoxGeometry(3.6,2.25,.12),new THREE.MeshBasicMaterial({map:pT,toneMapped:false}));panel.add(sc);const f=box(3.85,2.5,.1,0x20161c,.05);f.position.z=-.1;panel.add(f);[-1.4,1.4].forEach(x=>{const w=box(.07,8,.07,0x303038,.01);w.position.set(x,5.2,-.1);panel.add(w)});const g=glow(0xff5040,8,.3);g.position.z=.2;panel.add(g)}gut.add(panel);
function pan(big,small,col,strike){pg.fillStyle='#08060c';pg.fillRect(0,0,512,320);pg.textAlign='center';pg.textBaseline='middle';pg.fillStyle=col;pg.font='900 112px sans-serif';pg.fillText(big,256,134);pg.fillStyle='#fff';pg.font='800 54px sans-serif';pg.fillText(small,256,264);if(strike){pg.strokeStyle='#ff2d3f';pg.lineWidth=20;pg.beginPath();pg.moveTo(30,40);pg.lineTo(482,230);pg.stroke()}pT.needsUpdate=true}
let lastP='';function setP(k,...a){if(k!==lastP){pan(...a);lastP=k}}
// atasco
const pile=[];for(let i=0;i<20;i++){const g=makeGum(.62+R()*.4,[0xff6fb8,0xff93cb,0xf0529f,0x7ae6d8,0xffd34a][i%5]);g.userData={x:(i%5-2)*1.85+(R()-.5)*.5,y:.9+Math.floor(i/5)*1.45,z:-5.2-(i%3)*1.4,d:i*.09,rx:R()*3,ry:R()*3};g.visible=false;gut.add(g);pile.push(g)}
const warn=new THREE.PointLight(0xff2020,0,46,1.4);warn.position.set(0,7,-2);gut.add(warn);
// salón de la abuela
const room=new THREE.Group();scene.add(room);{const fl=pixTex(128,128,(g,w,h)=>{const q=mk(4);for(let y=0;y<h;y+=16)for(let x=0;x<w;x+=32){g.fillStyle=['#9a6a3e','#8b5e36','#a87548'][Math.floor(q()*3)];g.fillRect(x+(y%32?16:0),y,31,15)}},[6,6]);const f=new THREE.Mesh(new THREE.PlaneGeometry(40,30),new THREE.MeshStandardMaterial({map:fl,roughness:.8}));f.rotation.x=-Math.PI/2;f.receiveShadow=true;f.position.z=4;room.add(f);
 const wp=pixTex(64,64,(g,w,h)=>{g.fillStyle='#e7d6b6';g.fillRect(0,0,w,h);g.fillStyle='#d8c29a';for(let x=0;x<w;x+=16)g.fillRect(x,0,6,h)},[8,4]);const w=new THREE.Mesh(new THREE.PlaneGeometry(40,18),new THREE.MeshStandardMaterial({map:wp,roughness:.95}));w.position.set(0,9,-5);w.receiveShadow=true;room.add(w);
 const zc=box(40,.8,.2,0xf4efe6,.02);zc.position.set(0,.4,-4.9);room.add(zc);
 [[-3.4,6.3,0xc98a4a],[3.2,6.6,0x5a8ab0]].forEach(([x,y,c])=>{const a=box(2.2,2.8,.14,0x5a3a20,.04);a.position.set(x,y,-4.8);room.add(a);const b=box(1.7,2.3,.06,c,.02);b.position.set(x,y,-4.7);room.add(b)});
 const sof=box(6,1.6,1.9,0x7a2f4a,.2);sof.position.set(0,.9,-3.6);room.add(sof);const bk=box(6,2.6,.7,0x8a3858,.2);bk.position.set(0,2.2,-4.3);room.add(bk);
 const rug=box(9,.06,5,0xc7433a,.02);rug.position.set(0,.03,1.6);room.add(rug)}
const gran=abuela();room.add(gran.g);const kid=capataz();room.add(kid.g);const bubble=new THREE.Mesh(new THREE.SphereGeometry(1,24,18),new THREE.MeshStandardMaterial({color:0xff85c4,roughness:.18,emissive:0x5a1036,emissiveIntensity:.3}));room.add(bubble);
const t1=TL.s1[0],t2=TL.s2[0],t3=TL.s3[0],t4=TL.s4[0],tC=TL.cta[0];
const shots={h:{p:V3(-.4,3.2,20),q:V3(0,5.2,0)},s1:{p:V3(0,3.1,18),q:V3(0,4.9,0)},s2:{p:V3(3,2.8,17),q:V3(.3,4.6,0)},s3:{p:V3(-3,3,20),q:V3(0,5,0)},s4:{p:V3(0,3.5,23),q:V3(0,5.3,-2)},cta:{p:V3(0,3,34.6),q:V3(0,2,0)}};
const go=camera(cam,['h','s1','s2','s3','s4','cta'],shots,TL,.45);
const speedAt=t=>t<t3?t*1.2:(t<t4?t3*1.2+(t-t3)*(1.2+16*ss(t3,t3+1.1,t)*(1-ss(t4-1.1,t4,t))):t3*1.2+(t4-t3)*9+(t-t4)*.5);
window.renderAt=t=>{const s=segAt(TL,t),m=mouthAt(t);const inRoom=s==='s1';gut.visible=!inRoom;room.visible=inRoom;
 scene.background=new THREE.Color(inRoom?0xe7d6b6:0x2a0710);scene.fog.color.copy(scene.background);scene.fog.far=inRoom?300:92;hemi.intensity=inRoom?1.5:1.25;fill2.intensity=inRoom?0:60;
 if(!inRoom){const zo=speedAt(t);drawTun(t,zo);drawAcid(t,zo);const b=Math.sin(t*1.5)*.08;raft.position.set(0,b+.15,s==='s4'?-ss(t4,t4+.6,t)*1.1+1.1:1.1);raft.rotation.z=Math.sin(t*1.1)*.016;
  // personaje
  hero.g.position.set(-1.3,.38,.2);hero.g.rotation.y=.15;
  if(s==='h')hero.pose(t,m,{look:.5,point:.0,wave:0});else if(s==='s2')hero.pose(t,m,{look:.55,point:.75});else if(s==='s3')hero.pose(t,m,{armsUp:.55+.2*Math.sin(t*4)});else if(s==='s4')hero.pose(t,m,{armsUp:ss(t4,t4+.4,t)});else hero.pose(t,m,{wave:1});
  gum.rotation.y=Math.sin(t*.6)*.1;gum.scale.setScalar(1+Math.sin(t*2.2)*.02);gum.visible=s!=='cta';
  panel.position.set(s==='s3'?1.5:(s==='s2'?1.7:1.0),s==='s2'?5.2:5.9,-.7+1.1);panel.rotation.y=-.1;panel.rotation.z=Math.sin(t*1.1)*.018;panel.visible=(s==='h'||s==='s2'||s==='s3');
  if(s==='h')setP('h','7 AÑOS','¿AHÍ DENTRO?','#ff3b30');if(s==='s2')setP('s2','7 AÑOS','FALSO','#ff3b30',true);if(s==='s3'){const hrs=Math.round(40*ss(t3+.4,t4-.7,t));setP('c'+hrs,hrs+' H','UNAS 40 HORAS','#ffc23a')}
  enz.forEach((e,i)=>{const u=e.userData;e.visible=s==='s2';if(e.visible){const ph=((t*u.sp+u.p)%1.6)/1.6;const d=1.65+Math.abs(Math.sin(ph*3.14*2))*2.4;e.position.set(1.42+Math.cos(u.a+t*.4)*d,2.1+u.b+Math.abs(Math.sin(ph*6.28))*.4,.2+Math.sin(u.a+t*.4)*d);e.rotation.set(t*2+i,t*3,0);const lookG=Math.atan2(1.42-e.position.x,.2-e.position.z);e.rotation.y=lookG}});
  drops.forEach(d=>{const u=d.userData;d.visible=s==='s2'||s==='h';const f=(t*u.v+u.p)%1;d.position.set(u.x,9.2-f*9.6,-2-Math.abs(u.z)*.7);});
  pile.forEach(g=>{const u=g.userData;g.visible=s==='s4';if(g.visible){const a=t-t4-.5-u.d;const f=ss(0,.45,a);const by=a>.45?Math.abs(Math.sin((a-.45)*9))*Math.exp(-(a-.45)*4)*.5:0;g.position.set(u.x,14-(14-u.y)*f+by,u.z);g.rotation.set(u.rx*(1-f),u.ry,0)}});
  warn.intensity=s==='s4'?(.5+.5*Math.sin(t*9))*110*ss(t4+.8,t4+1.2,t):0;
 }else{const u=(t-t1)/(t2-t1);gran.g.position.set(-1.75,0,.6);gran.g.rotation.y=.55;gran.pose(t,m,{point:.85,look:.2});
  kid.g.position.set(1.75,0,.6);kid.g.rotation.y=-.45;const gulp=ss(.72,.8,u);kid.pose(t,0,{look:-.2,armsUp:gulp*.15});
  const rb=.1+1.15*ss(.12,.72,u)*(1-gulp);bubble.scale.setScalar(rb);bubble.visible=rb>.12;const hd=kid.head.getWorldPosition(V3());bubble.position.set(hd.x-.2-rb*.55,hd.y-.38,hd.z+.75+rb*.6);kid.g.scale.y=1-(gulp>0&&gulp<1?.05:0);if(u>.8){kid.g.position.y=Math.abs(Math.sin((u-.8)*28))*.28*(1-(u-.8)/.2)}}
 go(t,(p,q)=>{if(s==='s3'){p.x+=Math.sin(t*23)*.06*ss(t3+.6,t3+1.2,t);p.y+=Math.cos(t*29)*.05*ss(t3+.6,t3+1.2,t)}if(s==='s4'&&t>t4+.5&&t<t4+2.2){const a=.07;p.x+=Math.sin(t*61)*a;p.y+=Math.cos(t*67)*a}if(s==='h')p.z-=t*.5});
 r.render(scene,cam);return true};
window.ready=true;
