// ¿Y si desaparece la Luna? (1304). Serie ¿QUÉ PASARÍA SI…? Parte 2. Reutilizable: muelle, mar con nivel, luna de cubos que estalla, globo con eje.
import {THREE,J,mk,ss,V3,clamp,stage,sun,box,glow,pixTex,capataz,camera,segAt,mouthAt} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x06102c,fog:[0x06102c,50,170],exposure:1.1});const R=mk(1304);
const hemi=new THREE.HemisphereLight(0xbcd0ff,0x1a2a4a,1.0);scene.add(hemi);const S=sun(scene,{pos:[-12,30,20],span:30,color:0xdfe8ff,power:1.5});
const NIGHT=new THREE.Color(0x06102c),BLACK=new THREE.Color(0x01020a),DAY=new THREE.Color(0x76c4ff),SPACE=new THREE.Color(0x02030c);
const CC=new THREE.Color();
// --- mar con nivel variable
const set=new THREE.Group();scene.add(set);const CS=1.5,SX=30,SZ=48,sea=new THREE.InstancedMesh(new THREE.BoxGeometry(CS,CS,CS),new THREE.MeshStandardMaterial({roughness:.32,metalness:.1}),SX*SZ);sea.frustumCulled=false;sea.receiveShadow=true;set.add(sea);
const far=new THREE.Mesh(new THREE.PlaneGeometry(600,400),new THREE.MeshStandardMaterial({color:0x0c4b9a,roughness:.5}));far.rotation.x=-Math.PI/2;far.position.set(0,-.4,-220);set.add(far);
const O=new THREE.Object3D();const waveY=(x,z,t)=>Math.sin(x*.32+t*1.5)*.2+Math.sin(z*.42-t*1.9)*.24+Math.sin((x+z)*.18+t*.9)*.16;
const A=new THREE.Color(0x18b6d8),B=new THREE.Color(0x0a5fb8),F=new THREE.Color(0xe8fbff);
function drawSea(t,lvl,lum){let i=0;for(let a=0;a<SX;a++)for(let b=0;b<SZ;b++){const x=(a-SX/2)*CS,z=42-b*CS,y=waveY(x,z,t)+lvl;O.position.set(x,y-CS/2-.1,z);O.updateMatrix();sea.setMatrixAt(i,O.matrix);CC.copy(A).lerp(B,clamp(Math.abs(z-6)/30));CC.lerp(F,clamp((waveY(x,z,t)-.34)*2.6));CC.multiplyScalar(lum*(.92+((a*7+b*13)%5)*.03));sea.setColorAt(i,CC);i++}sea.instanceMatrix.needsUpdate=true;sea.instanceColor.needsUpdate=true;far.position.y=-.4+lvl;far.material.color.setHex(0x0c4b9a).multiplyScalar(lum)}
// --- muelle
const PY=3.2;{const n=18;for(let i=0;i<n;i++){const p=box(5.2,.3,.92,i%2?0x8a6238:0x7a5430,.03);p.position.set(0,PY-.15,14-i);set.add(p)}[-2.3,2.3].forEach(x=>{for(let z=14;z>-4;z-=4){const q=box(.5,9,.5,0x4a3220,.05);q.position.set(x,PY-4.6,z);set.add(q)}})}
// regla de marea en el agua, con franjas
const ruler=new THREE.Group();ruler.position.set(3.0,0,3);set.add(ruler);for(let i=-5;i<7;i++){const q=box(.95,.98,.95,i%2?0xfff3e0:0xe5343f,.03);q.position.y=i+.5;ruler.add(q)}
const mk1=(col,y)=>{const m=new THREE.Mesh(new THREE.BoxGeometry(2.6,.2,1.3),new THREE.MeshBasicMaterial({color:col,toneMapped:false}));m.position.set(0,y,0);ruler.add(m);return m};
const AMP0=2.3,AMP1=AMP0/3;const old=[mk1(0xffc23a,AMP0),mk1(0xffc23a,-AMP0)],neu=[mk1(0x40ffe0,AMP1),mk1(0x40ffe0,-AMP1)];
// búho perdido
const owl=new THREE.Group();{const a=box(1.1,1.3,.95,0x8a6a42,.14);a.position.y=.65;owl.add(a);const hd=new THREE.Group();hd.position.y=1.5;const h=box(1.2,.9,1.0,0x9a784c,.12);hd.add(h);[-.28,.28].forEach(x=>{const e=box(.42,.42,.06,0xffd24a,.05);e.position.set(x,.08,.52);hd.add(e);const p=box(.16,.2,.05,0x101018,.02);p.position.set(x,.08,.56);hd.add(p)});const bk=box(.16,.2,.1,0xe08a2a,.02);bk.position.set(0,-.14,.54);hd.add(bk);owl.add(hd);owl.userData.h=hd;owl.position.set(1.7,PY,.4);set.add(owl)}
// cangrejos (día)
const crabs=[];for(let i=0;i<3;i++){const g=new THREE.Group();const a=box(.9,.34,.6,0xe0483a,.08);a.position.y=.3;g.add(a);[-.62,.62].forEach(x=>{const p=box(.3,.26,.26,0xc93a2e,.05);p.position.set(x,.36,.24);g.add(p)});g.userData.x=-1.6+i*1.1;g.userData.z=-1-i*.8;set.add(g);crabs.push(g)}
const hero=capataz();set.add(hero.g);const lantern=glow(0xffc070,5,.0);lantern.position.set(.6,PY+2.2,1.0);set.add(lantern);
// --- estrellas
const n=1800,pos=new Float32Array(n*3);for(let i=0;i<n;i++){pos[i*3]=(R()-.5)*260;pos[i*3+1]=-6+R()*120;pos[i*3+2]=-105-R()*30}
const sg=new THREE.BufferGeometry();sg.setAttribute('position',new THREE.BufferAttribute(pos,3));const stars=new THREE.Points(sg,new THREE.PointsMaterial({color:0xe4eaff,size:.55,fog:false,transparent:true}));scene.add(stars);
// sol del lapso de tiempo
const sunS=glow(0xfff2c0,28,.95);sunS.material.fog=false;scene.add(sunS);
// --- luna de cubos que estalla
const noise=(x,y,z)=>Math.sin(x*3.1+1.3)*Math.cos(y*3.7-.7)+Math.sin(y*2.9+z*4.3)*.8+Math.cos(z*3.3-x*2.7+2)*.7+Math.sin(x*6.7+z*5.1)*.3;
const MR=7,MN=7000,MP=V3(1.5,8.1,-34);const moonI=new THREE.InstancedMesh(new THREE.BoxGeometry(.6,.6,.6),new THREE.MeshStandardMaterial({roughness:1,emissive:0x707888,emissiveIntensity:.3}),MN);moonI.frustumCulled=false;scene.add(moonI);
const MC=[];for(let i=0;i<MN;i++){const y=1-2*(i+.5)/MN,rd=Math.sqrt(1-y*y),a=i*2.39996;const x=Math.cos(a)*rd,z=Math.sin(a)*rd;const c=noise(x*2,y*2,z*2)>.5?.56:.92;MC.push({x,y,z,v:1.5+R()*3.6,d:clamp((.2-x*.6+y*.35+1)/2)*.75,w:R()*9});moonI.setColorAt(i,new THREE.Color(c,c,c*1.03))}
const core=glow(0xffa040,20,0);core.material.fog=false;core.position.copy(MP);scene.add(core);
function drawMoon(tau){for(let i=0;i<MN;i++){const m=MC[i],a=Math.max(0,tau-m.d);const k=MR+m.v*a*(1+a*.35),sc=a>2.8?Math.max(0,1-(a-2.8)):1;O.position.set(MP.x+m.x*k,MP.y+m.y*k,MP.z+m.z*k);O.rotation.set(m.w*a,m.w*a*.7,0);O.scale.setScalar(sc*(a>0?1.1:1));O.updateMatrix();moonI.setMatrixAt(i,O.matrix)}O.scale.setScalar(1);O.rotation.set(0,0,0);moonI.instanceMatrix.needsUpdate=true;moonI.material.emissiveIntensity=.3+clamp(tau)*.25;core.material.opacity=clamp(tau*1.3)*(1-ss(1.6,2.8,tau))*.9}
// --- globo con eje
const globeG=new THREE.Group();scene.add(globeG);const spin=new THREE.Group();globeG.add(spin);const NG=9000,GR=10,gi=new THREE.InstancedMesh(new THREE.BoxGeometry(.56,.56,.56),new THREE.MeshStandardMaterial({roughness:.65}),NG);gi.frustumCulled=false;spin.add(gi);const GC=[];
for(let i=0;i<NG;i++){const y=1-2*(i+.5)/NG,rd=Math.sqrt(1-y*y),a=i*Math.PI*(3-Math.sqrt(5));const x=Math.cos(a)*rd,z=Math.sin(a)*rd;const land=noise(x,y,z)>.55;GC.push({y,land,sh:.92+((i*7)%5)*.03});O.position.set(x*(GR+(land?.2:0)),y*(GR+(land?.2:0)),z*(GR+(land?.2:0)));O.lookAt(0,0,0);O.updateMatrix();gi.setMatrixAt(i,O.matrix);O.rotation.set(0,0,0)}gi.instanceMatrix.needsUpdate=true;
const OC=new THREE.Color(0x1467c8),OC2=new THREE.Color(0x0c4fae),LC=new THREE.Color(0x58a84a),ICE=new THREE.Color(0xf2f8ff),DES=new THREE.Color(0xd0a860);
function globeCol(hotN,hotS){GC.forEach((g,i)=>{const lat=g.y;const cap=lat>0?.84-hotN*.5:.84-hotS*.5;const ice=Math.abs(lat)>clamp(cap,.25,.96);CC.copy(g.land?LC:(i%2?OC:OC2));if(g.land&&Math.abs(lat)<.5)CC.lerp(DES,Math.max(hotN*(lat>0),hotS*(lat<0))*.5);if(ice)CC.copy(ICE);CC.multiplyScalar(g.sh);gi.setColorAt(i,CC)});gi.instanceColor.needsUpdate=true}
const rod=new THREE.Mesh(new THREE.CylinderGeometry(.22,.22,27,10),new THREE.MeshStandardMaterial({color:0xffc23a,emissive:0x8a5a00,emissiveIntensity:.6}));globeG.add(rod);[13.6,-13.6].forEach(y=>{const c=box(.8,.8,.8,0xff3b4a,.1,{emissive:0x801018});c.position.y=y;globeG.add(c)});
const gSun=glow(0xfff2c0,40,.95);gSun.material.fog=false;gSun.position.set(-13,10,-30);scene.add(gSun);
const t1=TL.s1[0],t2=TL.s2[0],t3=TL.s3[0],t4=TL.s4[0],tC=TL.cta[0];
const shots={h:{p:V3(0,4.5,30),q:V3(0,7,0)},s1:{p:V3(-1.5,6,17),q:V3(0,7,-4)},s2:{p:V3(2.5,5.5,26),q:V3(2.5,5.5,3)},s3:{p:V3(0,0,66),q:V3(0,4.2,0)},s4:{p:V3(14,0,62),q:V3(0,4.2,0)},cta:{p:V3(0,6,34.6),q:V3(0,4.8,0)}};
const go=camera(cam,['h','s1','s2','s3','s4','cta'],shots,TL,.45);
window.tilt=23;
window.renderAt=t=>{const s=segAt(TL,t),m=mouthAt(t);const space=s==='s3'||s==='s4';
 set.visible=!space;stars.visible=!(s==='s2');globeG.visible=space;gSun.visible=space;sunS.visible=s==='s2';
 const tau=s==='h'?.28+t/TL.s1[0]*1.15:(s==='s1'?1.43+(t-t1)*1.2:9);moonI.visible=core.visible=(s==='h'||s==='s1')&&tau<5;if(moonI.visible)drawMoon(tau);
 let lum=.55,lvl=0;
 if(s==='h'){CC.copy(NIGHT);hemi.intensity=.95;S.intensity=1.5;stars.material.opacity=.55;stars.material.size=.5;lantern.material.opacity=0}
 if(s==='s1'){const k=ss(t1,t1+1.6,t);CC.copy(NIGHT).lerp(BLACK,k);hemi.intensity=.95-k*.45;S.intensity=1.5-k*1.25;lum=.55-.33*k;stars.material.opacity=.55+.45*k;stars.material.size=.5+k*.45;lantern.material.opacity=.75*k}
 if(s==='cta'){CC.copy(BLACK);hemi.intensity=.5;S.intensity=.5;lum=.3;stars.material.opacity=1;stars.material.size=.9;lantern.material.opacity=.7}
 if(s==='s2'){const k=ss(t2,t2+.6,t);CC.copy(BLACK).lerp(DAY,k);hemi.intensity=.3+k*1.25;S.intensity=.3+k*2.1;lum=.25+.75*k;lantern.material.opacity=0;const u=(t-t2)*1.8;sunS.position.set(Math.cos(u)*-50,26+Math.sin(u)*22,-110);const amp=AMP0+(AMP1-AMP0)*ss(t2+1.2,t2+3.2,t);lvl=amp*Math.sin((t-t2)*3.1);}
 if(space){CC.copy(SPACE);hemi.intensity=.5;S.intensity=2.9;S.position.set(-30,8,24);stars.material.opacity=1;stars.material.size=.7;S.castShadow=false}else{S.position.set(-12,30,20);S.castShadow=true}
 scene.background=CC.clone();scene.fog.color.copy(scene.background);scene.fog.far=space?3000:170;
 if(set.visible){drawSea(t,lvl,lum);old.forEach(o=>o.visible=s==='s2');neu.forEach(o=>o.visible=s==='s2'&&t>t2+2.4);owl.visible=s==='s1';ruler.visible=s==='s2';
  owl.userData.h.rotation.y=s==='s1'?Math.sin(t*2.7)*1.2:Math.sin(t)*.2;owl.rotation.z=Math.sin(t*1.7)*.05;
  crabs.forEach((g,i)=>{g.visible=false;g.position.set(g.userData.x+Math.sin(t*2+i)*.5,PY,g.userData.z+1.5);g.rotation.y=Math.sin(t*3+i)*.25});
  hero.g.position.set(s==='cta'?0:(s==='h'?-2.6:(s==='s2'?-.6:-1.25)),PY,2.4);hero.g.rotation.y=s==='h'?.25+Math.sin(t*.7)*.05:(s==='s1'?.1:-.05);hero.g.rotation.x=0;
  if(s==='h')hero.pose(t,m,{look:.5,armsUp:.25});else if(s==='s1')hero.pose(t,m,{look:Math.sin(t*1.3)*.6,point:.3});else if(s==='s2')hero.pose(t,m,{look:.5,point:ss(t2+.6,t2+1,t)});else hero.pose(t,m,{wave:1,look:.05})}
 if(space){const u=t-t3;const a=s==='s3'?(u<2.4?23+Math.sin(u*2.4)*1.3:23+(Math.sin((u-2.4)*1.05-.2)*.5+.5)*55*ss(2.4,3.6,u)+Math.sin(u*7)*1.5):70-ss(t4,tC-.2,t)*6+Math.sin(t*1.7)*2;window.tilt=a;globeG.rotation.z=-a*Math.PI/180*(s==='s4'?1:1);spin.rotation.y=t*.42;
  const hot=s==='s4'?ss(t4,t4+1.2,t):(s==='s3'?ss(t3+3.6,t3+6,t)*.5:0);globeCol(hot,0);globeG.position.y=0}
 go(t,(p,q)=>{if(s==='h'){p.z-=t*.32}if(s==='s1')p.y+=(t-t1)*.1;if(s==='h'&&tau>.6&&tau<1.3){const a=.04;p.x+=Math.sin(t*60)*a;p.y+=Math.cos(t*67)*a}});
 r.render(scene,cam);return true};
window.ready=true;
