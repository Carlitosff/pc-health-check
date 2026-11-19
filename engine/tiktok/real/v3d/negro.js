// ¿Y si el Sol se convirtiera en un agujero negro? (2704). Serie ¿QUÉ PASARÍA SI…? Parte 16.
// Reutilizable: SOL de cubos que COLAPSA (los cubos caen en espiral hacia el centro), AGUJERO NEGRO con anillo de fotones y halo
// (blackHole()), Tierra que sigue en su órbita (misma masa → misma órbita), luz que se apaga con retraso y ESCARCHA que cubre el globo,
// regla de tamaños 700.000 km → 3 km con dos esferas a escala relativa, y el Sol que se recompone en s4.
import {THREE,J,mk,ss,V3,clamp,stage,box,glow,capataz,segAt,mouthAt,label3d,stars,voxGlobe} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x02030a,fog:null,exposure:1.05});cam.far=3000;cam.updateProjectionMatrix();const R=mk(2704);
const hemi=new THREE.HemisphereLight(0xcfe0ff,0x202030,.3);scene.add(hemi);
stars(scene,2400,{r0:900,r1:1100,size:2.2});
const ORB=42;
// ---------- SOL de cubos que colapsa
const SUN=new THREE.Group();scene.add(SUN);const SR=9;
const core=new THREE.Mesh(new THREE.SphereGeometry(SR*.97,48,32),new THREE.MeshBasicMaterial({color:0xffb030,toneMapped:false}));SUN.add(core);
const NG=1400;const gran=new THREE.InstancedMesh(new THREE.BoxGeometry(1,1,1),new THREE.MeshBasicMaterial({toneMapped:false}),NG);gran.frustumCulled=false;scene.add(gran);
const GD=[];for(let i=0;i<NG;i++){const y=1-2*(i+.5)/NG,rr=Math.sqrt(1-y*y),a=i*Math.PI*(3-Math.sqrt(5));GD.push([Math.cos(a)*rr,y,Math.sin(a)*rr,R()*6.28,.6+R()*.8])}
const gO=new THREE.Object3D(),gC=new THREE.Color();
// col = 0 sol entero, 1 colapsado (cada cubo con su retraso: los de fuera tardan más)
const updSun=(t,col)=>{for(let i=0;i<NG;i++){const[x,y,z,ph,dl]=GD[i];const b=.5+.5*Math.sin(t*1.7+ph*3);const kk=ss(0,1,clamp(col*1.6-(dl-.6)*.5));const rad=SR*(1-kk)+.2*kk;const sw=kk*kk*5*dl;
  const cx=x*Math.cos(sw)-z*Math.sin(sw),cz=x*Math.sin(sw)+z*Math.cos(sw);gO.position.set(cx*rad,y*rad,cz*rad);gO.lookAt(0,0,0);gO.scale.setScalar((.75+.55*b)*(1-.85*kk));gO.updateMatrix();gran.setMatrixAt(i,gO.matrix);
  gC.setRGB(1,(.62+.33*b)*(1-.5*kk),(.18+.3*b)*(1-.6*kk));gran.setColorAt(i,gC)}gran.instanceMatrix.needsUpdate=true;gran.instanceColor.needsUpdate=true};
const cor1=glow(0xffc050,55,.85),cor2=glow(0xff7a20,100,.45);scene.add(cor1,cor2);const sunL=new THREE.PointLight(0xfff0d8,9,0,0);scene.add(sunL);
// ---------- AGUJERO NEGRO (reutilizable)
export function blackHole(rad=2.2){const g=new THREE.Group();
 const ball=new THREE.Mesh(new THREE.SphereGeometry(rad,40,28),new THREE.MeshBasicMaterial({color:0x000000}));g.add(ball);
 const ring=new THREE.Mesh(new THREE.TorusGeometry(rad*1.5,rad*.09,12,160),new THREE.MeshBasicMaterial({color:0xffb050,transparent:true,opacity:.95,toneMapped:false,blending:THREE.AdditiveBlending}));g.add(ring);
 const ring2=new THREE.Mesh(new THREE.TorusGeometry(rad*1.62,rad*.04,8,160),new THREE.MeshBasicMaterial({color:0xfff0c8,transparent:true,opacity:.7,toneMapped:false,blending:THREE.AdditiveBlending}));g.add(ring2);
 const halo=glow(0xff8a30,rad*7,.5);g.add(halo);const occl=new THREE.Mesh(new THREE.CircleGeometry(rad*1.02,48),new THREE.MeshBasicMaterial({color:0x000000}));g.add(occl);
 g.userData={ring,ring2,halo,occl,ball};g.face=(c)=>{ring.lookAt(c);ring2.lookAt(c);occl.lookAt(c)};return g}
const BH=blackHole(2.2);scene.add(BH);
// ---------- órbita y Tierra
const orbit=new THREE.Mesh(new THREE.TorusGeometry(ORB,.22,8,300),new THREE.MeshBasicMaterial({color:0x4da8ff,transparent:true,opacity:.35,toneMapped:false}));orbit.rotation.x=Math.PI/2;scene.add(orbit);
const EG=new THREE.Group();scene.add(EG);const glb=voxGlobe(6000,4,{cube:.32});EG.add(glb.group);const atm=glow(0x6ab8ff,12,.35);EG.add(atm);
const frost=new THREE.Mesh(new THREE.IcosahedronGeometry(4.35,3),new THREE.MeshStandardMaterial({color:0xe8f4ff,roughness:.35,metalness:0,transparent:true,opacity:0,flatShading:true}));EG.add(frost);
const eL=new THREE.DirectionalLight(0xfff0d8,0);scene.add(eL);scene.add(eL.target);
// ---------- rótulos
const lSize=label3d(['EL SOL','*700.000 KM'],{w:12,h:4.6,px:120,sprite:true});scene.add(lSize);
const lOrb=label3d(['MISMA MASA','*MISMA ÓRBITA'],{w:13,h:4.6,px:120,sprite:true,accent:'#4da8ff'});scene.add(lOrb);
const lClock=label3d(['LA LUZ TARDA','*8 MIN 20 S'],{w:12,h:4.6,px:120,sprite:true,accent:'#9fd8ff'});scene.add(lClock);
const lNo=label3d(['EL SOL','*NO PUEDE'],{w:11,h:4.6,px:130,sprite:true,accent:'#4ade80'});scene.add(lNo);
// ---------- capataz en su isla (cta)
const ISL=new THREE.Group();scene.add(ISL);{const b=box(7,1.6,6,0x6a8a4a,.15);b.position.y=-.8;ISL.add(b);const b2=box(5,2,4.4,0x7a5a3a,.15);b2.position.y=-2.4;ISL.add(b2);const b3=box(2.6,1.6,2.4,0x6a4a2e,.15);b3.position.y=-4;ISL.add(b3)}
const hero=capataz();ISL.add(hero.g);const islL=new THREE.DirectionalLight(0xfff0d8,2.4);islL.position.set(30,60,40);islL.target=ISL;scene.add(islL);
const angAt=t=>-.6+t*.11;   // la Tierra sigue girando siempre a la misma velocidad (la órbita no cambia)
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],k=ss(0,d,lt),m=mouthAt(t);
 // colapso: h (1,0 s → final), queda colapsado s1-s3, se recompone en s4
 let col=0;if(s==='h')col=ss(.6,d+.4,lt);else if(s==='s1'||s==='s2'||s==='s3')col=1;else if(s==='s4')col=1-ss(.3,2.2,lt);else col=0;
 updSun(t,col);core.scale.setScalar(Math.max(.001,1-ss(0,.7,col)));core.visible=col<.95;
 cor1.material.opacity=.85*(1-col);cor2.material.opacity=.45*(1-col);
 const bh=ss(.7,1,col);BH.visible=bh>.01;BH.scale.setScalar(Math.max(.01,bh));BH.userData.ring.rotation.z=t*.4;BH.userData.halo.material.opacity=.5*bh*(.85+.15*Math.sin(t*3));BH.face(cam.position);
 // luz: tarda en apagarse (8 min 20 s), en el vídeo se apaga en s3
 let light=1;if(s==='s3')light=1-ss(.6,2.6,lt);else if(s==='s4')light=ss(.4,2.2,lt)*1;sunL.intensity=9*(1-col*.9);
 const fr=s==='s3'?ss(1.5,d,lt):s==='s4'?1-ss(.6,2.4,lt):0;frost.material.opacity=.62*fr;
 const a=angAt(t),ex=Math.cos(a)*ORB,ez=Math.sin(a)*ORB;EG.position.set(ex,0,ez);glb.group.rotation.y=t*.3;glb.group.rotation.z=.41;
 eL.position.set(0,0,0);eL.target.position.copy(EG.position);eL.intensity=2.6*light;atm.material.opacity=.35*light+.05;hemi.intensity=.12+.25*light;
 orbit.material.opacity=s==='s2'?.35+.45*ss(.5,1.5,lt):.3;
 lSize.visible=s==='s1';if(s==='s1'){lSize.set(lt<d*.45?['EL SOL MEDÍA','*700.000 KM']:['AHORA MIDE','*3 KM']);lSize.position.set(0,-6.2,0)}
 lOrb.visible=s==='s2'&&lt>1;lOrb.position.set(ex,-7.5,ez);
 lClock.visible=s==='s3'&&lt>.4;lClock.position.set(ex*.5,6,ez*.5);
 lNo.visible=s==='s4'&&lt>1.6;lNo.position.set(0,4.5,3);
 ISL.visible=s==='cta';ISL.position.set(ex*.55,-6,ez*.55+8);ISL.rotation.y=.4;hero.pose(t,m*.25,{wave:s==='cta'?1:0,look:.3});
 let p,q;
 if(s==='h'){p=V3(3,8-k*2,56-k*14);q=V3(0,5,0)}
 else if(s==='s1'){p=V3(2,1,34-k*4);q=V3(0,-1.2,0)}
 else if(s==='s2'){const E=EG.position,o=E.clone().normalize();p=E.clone().add(o.multiplyScalar(40)).add(V3(0,13-k*3,0));q=V3(0,-3,0).lerp(E,.42)}
 else if(s==='s3'){const E=EG.position;p=E.clone().add(V3(10-k*3,4,14-k*3));q=E.clone().add(V3(-3,3,-2))}
 else if(s==='s4'){p=V3(4,10,48-k*6);q=V3(0,7,0)}
 else{const I=ISL.position;p=I.clone().add(V3(2,4,34));q=I.clone().add(V3(0,1.8,0))}
 cam.position.copy(p);cam.lookAt(q);r.render(scene,cam)};
window.ready=true;
