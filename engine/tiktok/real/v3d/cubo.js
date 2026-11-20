// ¿Y si la Tierra fuera un cubo? (2804). Serie ¿QUÉ PASARÍA SI…? Parte 17.
// Jesse Berezovsky (Case Western, Gizmodo 31/12/2013): la gravedad no es perpendicular a las caras → cuesta de hasta ~50° cerca de las esquinas;
// océanos en una lente en el centro de cada cara; casi toda la superficie fuera de la atmósfera; anillo habitable estrecho.
// Ask a Mathematician (09/05/2011): algo del tamaño de la Tierra acaba redondo. Cálculo propio (cubo de la misma masa y volumen, 48³ masas):
// inclinación por la diagonal 0→50,8° y peso 0,99→0,68 (tabla TILT).
// Reutilizable: PLANETA DE CUBOS que se transforma esfera ↔ cubo (morph), lentes de agua y cúpulas de aire en las caras, cara a escala
// humana con personaje que se INCLINA con la gravedad, flecha de gravedad 3D y bola que rueda cuesta abajo.
import {THREE,J,mk,ss,V3,clamp,stage,box,glow,capataz,segAt,mouthAt,label3d,stars,puffs} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x02040c,fog:null,exposure:1.1});cam.far=4000;cam.updateProjectionMatrix();const R=mk(2804);
const hemi=new THREE.HemisphereLight(0xdfe8ff,0x1a1a28,.55);scene.add(hemi);
const sunD=new THREE.DirectionalLight(0xfff2dc,2.4);sunD.position.set(-40,50,60);scene.add(sunD);
stars(scene,2600,{r0:1200,r1:1500,size:2.4});
// tabla de inclinación (grados) y peso relativo por la diagonal de una cara: f = 0 centro … 0,97 casi esquina (cálculo propio)
const TILT=[[0,0,.99],[.1,4.2,.99],[.2,8.7,.98],[.3,12.9,.97],[.4,17.4,.96],[.5,22,.93],[.6,26.7,.91],[.7,32.1,.87],[.8,37.8,.82],[.9,44.7,.76],[.97,50.8,.68]];
const tiltAt=f=>{f=clamp(f,0,.97);for(let i=1;i<TILT.length;i++)if(f<=TILT[i][0]){const[a,ta,wa]=TILT[i-1],[b,tb,wb]=TILT[i];const x=(f-a)/(b-a);return[ta+(tb-ta)*x,wa+(wb-wa)*x]}return[50.8,.68]};
// ---------- PLANETA DE CUBOS (esfera ↔ cubo)
const QI=new THREE.Quaternion();
export function cubePlanet(S=10,N=16,seed=3){const Q=mk(seed),cells=[],key=new Set();const st=2*S/N;
 const faces=[[0,1],[0,-1],[1,1],[1,-1],[2,1],[2,-1]];
 for(const[ax,sg]of faces)for(let i=0;i<N;i++)for(let j=0;j<N;j++){const u=-S+st*(i+.5),v=-S+st*(j+.5);const p=[0,0,0];const o=[0,1,2].filter(k=>k!==ax);p[ax]=sg*(S-st/2);p[o[0]]=u;p[o[1]]=v;const k=p.map(x=>x.toFixed(2)).join();if(key.has(k))continue;key.add(k);
  const uu=u/S,vv=v/S;cells.push({p:new THREE.Vector3(...p),ax,sg,rf:Math.sqrt(uu*uu+vv*vv)/Math.SQRT2,n:Q(),land:Q()})}
 const m=new THREE.InstancedMesh(new THREE.BoxGeometry(st*.96,st*.96,st*.96),new THREE.MeshStandardMaterial({roughness:.8}),cells.length);m.frustumCulled=false;m.castShadow=false;
 const O=new THREE.Object3D(),C=new THREE.Color(),Cb=new THREE.Color();const g=new THREE.Group();g.add(m);
 // morph: 0 = esfera, 1 = cubo ; fin: 0 = colores de la Tierra, 1 = cubo final (lago central, anillo verde, roca desnuda)
 g.set=(morph,fin)=>{cells.forEach((c,i)=>{const sp=c.p.clone().normalize().multiplyScalar(S*1.12);O.position.copy(sp).lerp(c.p,morph);O.lookAt(0,0,0);O.quaternion.slerp(QI,morph);O.scale.setScalar(1);O.updateMatrix();m.setMatrixAt(i,O.matrix);
   const earth=c.land<.38?C.setHex(c.n<.5?0x2fa84f:0x3c8a3a):C.setHex(c.n<.5?0x1d5fbf:0x2470d0);if(Math.abs(c.p.clone().normalize().y)>.86)C.setHex(0xf2f6ff);
   const r=c.rf;Cb.setHex(r<.27?0x1e6fd6:r<.36?0x34b35a:r<.6?0x8a6a4a:0x6b6670);C.lerp(Cb,fin);m.setColorAt(i,C)});m.instanceMatrix.needsUpdate=true;m.instanceColor.needsUpdate=true};
 g.cells=cells;g.S=S;return g}
const PL=cubePlanet(10,16);scene.add(PL);
// lentes de agua y cúpulas de aire en el centro de cada cara
const FN=[[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]].map(a=>V3(...a));
const lens=[],dome=[],ring=[];FN.forEach(n=>{const q=new THREE.Quaternion().setFromUnitVectors(V3(0,1,0),n);
 const l=new THREE.Mesh(new THREE.SphereGeometry(3.4,32,16,0,Math.PI*2,0,Math.PI/2),new THREE.MeshStandardMaterial({color:0x2f8cff,roughness:.15,metalness:.1,emissive:0x0a2a6a,emissiveIntensity:.5}));l.quaternion.copy(q);l.position.copy(n).multiplyScalar(10);PL.add(l);lens.push(l);
 const d=new THREE.Mesh(new THREE.SphereGeometry(6.2,32,16,0,Math.PI*2,0,Math.PI/2),new THREE.MeshBasicMaterial({color:0x7fd0ff,transparent:true,opacity:0,depthWrite:false,blending:THREE.AdditiveBlending}));d.quaternion.copy(q);d.position.copy(n).multiplyScalar(10);PL.add(d);dome.push(d);
 const rg=new THREE.Mesh(new THREE.TorusGeometry(4.1,.32,8,48),new THREE.MeshBasicMaterial({color:0x6dff8a,transparent:true,opacity:0,toneMapped:false}));rg.quaternion.copy(new THREE.Quaternion().setFromUnitVectors(V3(0,0,1),n));rg.position.copy(n).multiplyScalar(10.3);PL.add(rg);ring.push(rg)});
// gotas de agua que ruedan hacia el centro de las caras (s3)
const NW=360,drops=puffs(scene,NW,.55,0x3a9cff,{opacity:.95});const DW=[];for(let i=0;i<NW;i++){const f=i%6;DW.push([f,(R()-.5)*18,(R()-.5)*18,R()*.5])}
const lCorner=label3d(['ESQUINAS','*SIN AIRE'],{w:10,h:4.3,px:120,sprite:true,accent:'#ff5a6a'});scene.add(lCorner);
const lRing=label3d(['AQUÍ SÍ','*SE VIVE'],{w:12,h:5.5,px:120,sprite:true,accent:'#6dff8a'});scene.add(lRing);
const lSea=label3d(['6 CARAS','*6 MARES'],{w:15,h:6.9,px:120,sprite:true,accent:'#4db8ff'});scene.add(lSea);
// ---------- CARA A ESCALA HUMANA (s1–s2): suelo plano hasta el borde, capataz que se inclina con la gravedad
const FACE=new THREE.Group();FACE.position.set(0,0,0);scene.add(FACE);const FL=50;
{const t=new THREE.InstancedMesh(new THREE.BoxGeometry(1.95,1,1.95),new THREE.MeshStandardMaterial({roughness:.85}),50*50);let i=0;const O=new THREE.Object3D(),C=new THREE.Color();
 for(let a=0;a<50;a++)for(let b=0;b<50;b++){const x=-FL+1+a*2,z=-FL+1+b*2;const d=Math.max(Math.abs(x),Math.abs(z))/FL;O.position.set(x,-.5+(R()-.5)*.08,z);O.updateMatrix();t.setMatrixAt(i,O.matrix);
  C.setHex(d<.3?0x3aa85a:d<.55?0x6f9a48:d<.8?0x8a6a4a:0x6b6670).offsetHSL(0,0,(R()-.5)*.05);t.setColorAt(i,C);i++}t.receiveShadow=true;FACE.add(t)}
const fs=new THREE.DirectionalLight(0xfff2dc,2.2);fs.position.set(-20,40,30);fs.target.position.set(0,0,0);fs.castShadow=true;fs.shadow.mapSize.set(2048,2048);Object.assign(fs.shadow.camera,{left:-30,right:30,top:30,bottom:-30,near:1,far:120});FACE.add(fs,fs.target);
const hero=capataz();FACE.add(hero.g);hero.g.traverse(o=>{if(o.isMesh)o.castShadow=true});
// flecha de gravedad (cilindro + punta)
const ARR=new THREE.Group();{const sh=new THREE.Mesh(new THREE.CylinderGeometry(.22,.22,4,12),new THREE.MeshBasicMaterial({color:0xffc23a,toneMapped:false}));sh.position.y=-2;ARR.add(sh);const tp=new THREE.Mesh(new THREE.ConeGeometry(.6,1.2,14),new THREE.MeshBasicMaterial({color:0xffc23a,toneMapped:false}));tp.rotation.x=Math.PI;tp.position.y=-4.5;ARR.add(tp)}FACE.add(ARR);
const lAng=label3d(['CUESTA','*0°'],{w:3.6,h:1.75,px:120,sprite:true});lAng.visible=false; // v31: la cifra va en 2D (overlay de serie_cubo.py)
const lCen=label3d(['CENTRO','*DE LA CARA'],{w:5,h:2.2,px:110,sprite:true,accent:'#6dff8a'});lCen.position.set(-2.6,3.4,-2.6);FACE.add(lCen);
const ball=new THREE.Mesh(new THREE.SphereGeometry(.7,24,16),new THREE.MeshStandardMaterial({color:0xff4d5e,roughness:.4}));ball.castShadow=true;FACE.add(ball);
// polvo del colapso (s5)
const dust=puffs(scene,300,.7,0xb89a7a,{opacity:.8});const DD=[];for(let i=0;i<300;i++){const v=V3(R()-.5,R()-.5,R()-.5).normalize();DD.push([v,R()])}
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],k=ss(0,d,lt),m=mouthAt(t);
 const planetOn=!(s==='s1'||s==='s2');PL.visible=planetOn;FACE.visible=!planetOn;
 let morph=1,fin=0;if(s==='h')morph=ss(.3,2.6,lt);if(s==='s3')fin=ss(.4,d-.6,lt);if(s==='s4')fin=1;if(s==='s5'){fin=1;morph=1-ss(1.2,d-.3,lt)}if(s==='cta'){morph=0;fin=0}
 PL.set(morph,fin);PL.rotation.set(.42,t*.22,.08);
 const lensK=s==='s3'?ss(.8,d-.3,lt):s==='s4'?1:s==='s5'?1-ss(1.2,d-.3,lt):0;lens.forEach(l=>{l.visible=lensK>.01;l.scale.set(lensK,lensK*.35,lensK)});
 const domeK=s==='s4'?ss(.3,1.6,lt):s==='s5'?1-ss(.3,1.2,lt):0;dome.forEach(dm=>{dm.material.opacity=.32*domeK;dm.scale.setScalar(.6+.4*domeK)});
 const ringK=s==='s4'?ss(1.8,2.6,lt):0;ring.forEach(rg=>{rg.material.opacity=ringK*(.75+.25*Math.sin(t*6))});
 lCorner.visible=s==='s4'&&lt>1.0;lRing.visible=s==='s4'&&lt>2.4;lSea.visible=s==='s3'&&lt>d*.55;
 PL.updateMatrixWorld(true);const corner=V3(10,10,10).applyMatrix4(PL.matrixWorld);const fc=V3(0,0,10).applyMatrix4(PL.matrixWorld);
 lCorner.position.copy(corner).add(V3(0,-2,6));lRing.position.copy(fc).add(V3(0,-8.5,4));lSea.position.set(0,-20,6);
 // gotas: de puntos sueltos de cada cara al centro
 for(let i=0;i<NW;i++){const[f,u,v,dl]=DW[i];const n=FN[f];const kk=s==='s3'?ss(dl,dl+1.6,lt):(s==='s4'||s==='s5')?1:0;const vis=s==='s3'&&kk<.98;const o=[0,1,2].filter(a=>Math.abs(n.getComponent(a))<.5);
  const p=V3(0,0,0);p.setComponent(o[0],u*(1-kk));p.setComponent(o[1],v*(1-kk));p.add(n.clone().multiplyScalar(10.6));p.applyMatrix4(PL.matrixWorld);drops.set(i,p.x,p.y,p.z,vis?1:0,t+i)}drops.done();
 const dk=s==='s5'?ss(.8,d,lt):0;for(let i=0;i<300;i++){const[v,ph]=DD[i];const rr=11+dk*(8+ph*10);drops;dust.set(i,v.x*rr,v.y*rr,v.z*rr,dk>0&&dk<.98?1.2*(1-dk):0,ph*6+t)}dust.done();
 // cara a escala humana
 if(!planetOn){const f=s==='s1'?.0+.12*ss(.6,d,lt):.12+.83*ss(.2,d-.4,lt);const[ang,wgt]=tiltAt(f);const x=f*FL*.98;const a=ang*Math.PI/180;
  hero.g.position.set(x*.7071,0,x*.7071);hero.g.rotation.set(0,Math.PI/4,0);hero.pose(t,m*.5,{walk:s==='s2'&&lt<d-.4?t*6:null});hero.g.rotateX(-a);
  ARR.position.set(x*.7071+.0,6.2,x*.7071);ARR.rotation.set(0,Math.PI/4,0);ARR.rotateX(a);lAng.position.set(x*.7071+1.4,2.4,x*.7071+1.4);
  lCen.visible=false;const bf=s==='s2'?clamp(.85-1.1*ss(.4,d,lt)*(.6+.4*ss(.4,d,lt)),0,1):.0;const bx=bf*FL*.9;ball.position.set(bx*.7071+2.5,.7,bx*.7071-2.5);ball.rotation.z=-bf*40;ball.visible=s==='s2'}
 let p,q;
 if(s==='h'){const a=t*.15;p=V3(Math.sin(a)*12,8,96-k*14);q=V3(0,-7,0)}
 else if(s==='s1'){p=V3(-10+k*2,7.5,24);q=V3(2,3.5,0)}
 else if(s==='s2'){const f=.12+.83*ss(.2,d-.4,lt),x=f*FL*.98*.7071;p=V3(x-17,9,x+15);q=V3(x-1.6,3.0,x-1.6)}
 else if(s==='s3'){p=V3(0,6,100-k*6);q=V3(0,-7,0)}
 else if(s==='s4'){p=V3(Math.sin(t*.2)*10,10,98);q=V3(0,-7,0)}
 else if(s==='s5'){p=V3(0,6,98+k*6);q=V3(0,-7,0)}
 else{p=V3(Math.sin(t*.3)*8,4,108);q=V3(0,-9,0)}
 cam.position.copy(p);cam.lookAt(q);r.render(scene,cam)};
window.ready=true;
