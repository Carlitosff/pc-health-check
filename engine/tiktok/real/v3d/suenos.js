// Mito: '¿soñamos en blanco y negro?' (2703). Eva Murzyn, Universidad de Dundee, Consciousness and Cognition 17(4), dic-2008.
// Reutilizable: ISLA DE SUEÑO flotante (dreamIsle: césped, árboles, casa, globo, nubes) en COLOR o en GRIS (misma isla, paleta pasada a luminancia),
// burbujas que suben de la cabeza, dormitorio doble con dos camas, TELE ANTIGUA de bloques con nieve en la pantalla y barras 3D de porcentaje.
// La gradación de toda la imagen (blanco y negro ↔ color) la hace v3d_run con V['grade'] (motor v30).
import {THREE,J,mk,ss,V3,clamp,stage,sun,box,glow,capataz,abuela,segAt,mouthAt,label3d,bed,lieDown,pixTex} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x0d1430,fog:[0x0d1430,60,160],exposure:1.12});const R=mk(2703);
const hemi=new THREE.HemisphereLight(0x8fa4e0,0x241a2a,.8);scene.add(hemi);sun(scene,{pos:[-12,26,16],span:26,color:0xb8c8ff,power:1.0});
const lampL=new THREE.PointLight(0xffc880,60,30,1.5);lampL.position.set(0,5,0);scene.add(lampL);
const gray=c=>{const C=new THREE.Color(c);const l=.2126*C.r+.7152*C.g+.0722*C.b;return new THREE.Color(l,l,l)};
// ---------- ISLA DE SUEÑO (exportable)
export function dreamIsle(isGray=false,seed=5){const g=new THREE.Group();const Q=mk(seed);const col=c=>isGray?gray(c).getHex():c;
 const top=box(7,1,5.2,col(0x58c25a),.2);g.add(top);const dirt=box(6,1.6,4.4,col(0x8a5a36),.2);dirt.position.y=-1.2;g.add(dirt);const tip=box(3.4,1.4,2.6,col(0x6e4528),.2);tip.position.y=-2.5;g.add(tip);
 [[-2.2,-1.2],[2.4,-1.4],[-2.6,1.4]].forEach(([x,z],i)=>{const tr=box(.5,1.6,.5,col(0x7a4e2e),.05);tr.position.set(x,1.3,z);g.add(tr);const lf=box(1.8,1.6,1.8,col([0x2fa84f,0x3cc46a,0x24944a][i]),.3);lf.position.set(x,2.7,z);g.add(lf)});
 const house=box(2.2,1.8,1.8,col(0xf2e6c8),.08);house.position.set(.6,1.4,.2);g.add(house);const roof=box(2.6,.7,2.1,col(0xe5343f),.08);roof.position.set(.6,2.6,.2);g.add(roof);
 const door=box(.6,1,.06,col(0x6a4a2e),.02);door.position.set(.6,1,1.12);g.add(door);
 const balloon=new THREE.Group();const bb=new THREE.Mesh(new THREE.SphereGeometry(.9,18,14),new THREE.MeshStandardMaterial({color:col(0xff5fa8),roughness:.4}));balloon.add(bb);const bk=box(.5,.4,.5,col(0xc8a070),.05);bk.position.y=-1.6;balloon.add(bk);balloon.position.set(-1,5.4,0);g.add(balloon);
 const clouds=[];for(let i=0;i<5;i++){const c=box(1.6+Q(),.7,1.1,0xffffff,.3,{emissive:0xffffff,emissiveIntensity:.15});c.position.set((Q()-.5)*10,2+Q()*4,(Q()-.5)*3-1);g.add(c);clouds.push(c)}
 const L=new THREE.PointLight(0xfff0e0,40,22,1.2);L.position.set(0,7,5);g.add(L);
 g.tick=t=>{g.position.y=g.userData.y+Math.sin(t*1.1+seed)*.25;g.rotation.y=Math.sin(t*.4+seed)*.25;balloon.position.y=5.4+Math.sin(t*1.7)*.3;clouds.forEach((c,i)=>{c.position.x+=0;c.position.x=((c.position.x+5+.006*(i+1))%10)-5})};return g}
// ---------- DORMITORIO DOBLE
const fl=new THREE.Mesh(new THREE.PlaneGeometry(90,90),new THREE.MeshStandardMaterial({color:0x5a4030,roughness:.9}));fl.rotation.x=-Math.PI/2;fl.receiveShadow=true;scene.add(fl);
for(let i=0;i<18;i++){const p=box(2.4,.05,90,i%2?0x6a4a36:0x5e4232,.01);p.position.set(-21+i*2.5,.02,0);scene.add(p)}
const wall=box(70,30,.6,0x27315a,.05);wall.position.set(0,15,-9);scene.add(wall);
const win=new THREE.Group();{const f=box(6,5,.5,0x8a6a4a,.08);win.add(f);const gl=box(5.2,4.2,.3,0x0a1030,.02,{emissive:0x101848,emissiveIntensity:.6});gl.position.z=.12;win.add(gl);const moon=new THREE.Mesh(new THREE.SphereGeometry(.8,20,14),new THREE.MeshBasicMaterial({color:0xfff4c8,toneMapped:false}));moon.position.set(1.2,1.1,.3);win.add(moon);const mg=glow(0xfff0b0,4,.6);mg.position.set(1.2,1.1,.4);win.add(mg)}
win.position.set(0,7.5,-8.6);scene.add(win);
const BA=bed(0x8a5cd6);BA.position.set(-4.6,0,-4);scene.add(BA);const gran=abuela();const blA=lieDown(gran,BA,0x8a5cd6);
const BC=bed(0x3a6fd8);BC.position.set(4.6,0,-4);scene.add(BC);const hero=capataz();hero.hat.forEach(h=>h.visible=false);const blC=lieDown(hero,BC,0x3a6fd8);
// TELE ANTIGUA de bloques con nieve (junto a la abuela)
const TV=new THREE.Group();{const cab=box(3.4,2.8,2.6,0x6a4a2e,.15);cab.position.y=1.4;TV.add(cab);const legs=[[-1.3,-.9],[1.3,-.9],[-1.3,.9],[1.3,.9]].forEach(([x,z])=>{const l=box(.2,.9,.2,0x3a2a1e,.02);l.position.set(x,-.45,z);TV.add(l)});
 const ant1=box(.08,2,.08,0x9a9aa8,.01);ant1.position.set(-.5,3.6,0);ant1.rotation.z=.5;TV.add(ant1);const ant2=box(.08,2,.08,0x9a9aa8,.01);ant2.position.set(.5,3.6,0);ant2.rotation.z=-.5;TV.add(ant2)}
const noise=pixTex(64,48,(g,w,h)=>{});const scr=new THREE.Mesh(new THREE.PlaneGeometry(2.6,2),new THREE.MeshBasicMaterial({map:noise,toneMapped:false}));scr.position.set(-.2,1.45,1.31);TV.add(scr);
const tvg=glow(0xc8d8ff,6,.35);tvg.position.set(-.2,1.45,1.6);TV.add(tvg);
TV.position.set(-10.5,.9,-3);TV.rotation.y=.5;scene.add(TV);
const NC=noise.image.getContext('2d');const tvNoise=t=>{const f=Math.floor(t*15);const Q=mk(f);const im=NC.createImageData(64,48);for(let i=0;i<64*48;i++){const v=(Q()*200+40)|0;im.data[i*4]=im.data[i*4+1]=im.data[i*4+2]=v;im.data[i*4+3]=255}NC.putImageData(im,0,0);noise.needsUpdate=true};
// islas de sueño: gris sobre la abuela, color sobre la capataz
const IA=dreamIsle(true,3);IA.userData.y=12;IA.position.set(-5,12,-3);IA.scale.setScalar(.85);scene.add(IA);
const IC=dreamIsle(false,8);IC.userData.y=12;IC.position.set(5,12,-3);IC.scale.setScalar(.85);scene.add(IC);
// burbujas que suben de cada cabeza
const bub=(x)=>{const a=[];for(let i=0;i<3;i++){const m=new THREE.Mesh(new THREE.SphereGeometry(.25+i*.18,14,10),new THREE.MeshStandardMaterial({color:0xffffff,emissive:0xffffff,emissiveIntensity:.35,transparent:true,opacity:.85}));scene.add(m);a.push(m)}return(t)=>a.forEach((m,i)=>{m.position.set(x+Math.sin(t*1.3+i)*.2,4.2+i*2.2+Math.sin(t*2+i)*.15,-4.6)})};
const bA=bub(-4.6),bC=bub(4.6);
// barras 3D de porcentaje (s3)
const BARS=new THREE.Group();scene.add(BARS);const barA=box(2.2,1,2.2,0xc8c8d0,.08,{emissive:0x505058,emissiveIntensity:.6});const barC=box(2.2,1,2.2,0x4de3ff,.08,{emissive:0x0a5a6a,emissiveIntensity:.3});BARS.add(barA,barC);barA.position.x=-2.2;barC.position.x=2.2;
const lA=label3d(['MAYORES','*22 %'],{w:5,h:2.6,px:130,sprite:true,accent:'#c8c8d0'});const lC=label3d(['JÓVENES','*4 %'],{w:5,h:2.6,px:130,sprite:true,accent:'#4de3ff'});BARS.add(lA,lC);
const lT=label3d(['SUEÑOS EN','*BLANCO Y NEGRO'],{w:8,h:2.8,px:120,sprite:true});BARS.add(lT);BARS.position.set(0,0,2);
const lD=label3d(['60 PERSONAS','*DIARIO DE SUEÑOS'],{w:8.5,h:2.9,px:120,sprite:true});scene.add(lD);
const lY=label3d(['HACE','*100 AÑOS'],{w:6,h:2.8,px:120,sprite:true,accent:'#e8d2a0'});scene.add(lY);
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],k=ss(0,d,lt),m=mouthAt(t);
 IA.tick(t);IC.tick(t);bA(t);bC(t);tvNoise(t);
 blA.blanket.scale.y=1+.06*Math.sin(t*1.6);blC.blanket.scale.y=1+.06*Math.sin(t*1.8+1);
 gran.eyes.forEach(e=>e.scale.y=.1);hero.eyes.forEach(e=>e.scale.y=.1);
 const bh=s==='s3'?ss(.6,2.2,lt):0;barA.scale.y=Math.max(.01,22*.22*bh);barA.position.y=barA.scale.y/2;barC.scale.y=Math.max(.01,4*.22*bh);barC.position.y=barC.scale.y/2;
 BARS.visible=s==='s3';lA.position.set(-2.2,barA.scale.y+1.7,0);lC.position.set(2.2,barC.scale.y+1.7,0);lA.material.opacity=lC.material.opacity=ss(1.6,2.4,lt);lT.position.set(0,-.3,2.5);
 lD.visible=s==='s2'&&lt>.8;lD.position.set(0,1.2,5);lY.visible=s==='s1'&&lt>.5;lY.position.set(-6.3,1.6,3);
 tvg.material.opacity=.3+.1*Math.sin(t*20);
 let p,q;
 if(s==='h'){p=V3(5.6+Math.sin(t*.5)*.4,12.6,19-k*2.5);q=V3(5,14.2,-3)}
 else if(s==='s1'){p=V3(-6.5+k*1.5,7,22-k*2);q=V3(-7,4.6,-3)}
 else if(s==='s2'){p=V3(0,10,44-k*4);q=V3(0,7.5,-3)}
 else if(s==='s3'){p=V3(Math.sin(t*.3)*1.5,7,31-k*2);q=V3(0,6,0)}
 else if(s==='s4'){p=V3(5+Math.sin(t*.6)*.6,12.8,19-k*5);q=V3(5,13.8,-3)}
 else{p=V3(0,8,34);q=V3(0,2.5,-3)}
 cam.position.copy(p);cam.lookAt(q);r.render(scene,cam)};
window.ready=true;
