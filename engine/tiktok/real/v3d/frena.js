// ¿Y si la Tierra frena de golpe? (1204). Serie ¿QUÉ PASARÍA SI…?
import {THREE,J,mk,ss,V3,clamp,stage,sun,box,glow,pixTex,capataz,camera,segAt,mouthAt} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x8ad4ff,fog:[0xc8e4ff,60,190],exposure:1.08});const R=mk(1204);
const hemi=new THREE.HemisphereLight(0xdcefff,0x8a9a6a,1.5);scene.add(hemi);const S=sun(scene,{pos:[-16,34,18],span:40});
const sky=new THREE.Color(0x8ad4ff),dust=new THREE.Color(0xb0562a),dark=new THREE.Color(0x03040c);
const street=new THREE.Group();scene.add(street);
// suelo
const grass=pixTex(128,128,(g,w,h)=>{const q=mk(8);g.fillStyle='#6fb24e';g.fillRect(0,0,w,h);for(let i=0;i<700;i++){g.fillStyle=['#62a544','#7dbd58','#568f3c'][Math.floor(q()*3)];g.fillRect(Math.floor(q()*w/4)*4,Math.floor(q()*h/4)*4,4,4)}},[40,40]);
const gnd=new THREE.Mesh(new THREE.PlaneGeometry(400,400),new THREE.MeshStandardMaterial({map:grass,roughness:1}));gnd.rotation.x=-Math.PI/2;gnd.position.y=-.02;gnd.receiveShadow=true;street.add(gnd);
const road=new THREE.Mesh(new THREE.PlaneGeometry(400,9),new THREE.MeshStandardMaterial({color:0x34363f,roughness:.95}));road.rotation.x=-Math.PI/2;road.position.set(0,.01,9);road.receiveShadow=true;street.add(road);
for(let i=-40;i<40;i++){const d=new THREE.Mesh(new THREE.BoxGeometry(2,.03,.22),new THREE.MeshBasicMaterial({color:0xf2e9b8}));d.position.set(i*5,.03,9);street.add(d)}
// montes lejanos
for(let i=0;i<26;i++){const h=8+R()*22,w=14+R()*22;const m=new THREE.Mesh(new THREE.BoxGeometry(w,h,w),new THREE.MeshStandardMaterial({color:i%2?0x5f8f6a:0x6e9c74,roughness:1}));m.position.set((i-13)*18+R()*6,h/2,-120-R()*30);street.add(m)}
// nubes
const clouds=[];for(let i=0;i<10;i++){const g=new THREE.Group();const n=3+Math.floor(R()*3);for(let k=0;k<n;k++){const b=new THREE.Mesh(new THREE.BoxGeometry(5+R()*6,1.6+R()*2,3+R()*3),new THREE.MeshStandardMaterial({color:0xffffff,roughness:1,emissive:0xffffff,emissiveIntensity:.25}));b.position.set(k*3-n,R(),R()*2);g.add(b)}g.position.set((R()-.5)*160,28+R()*16,-70-R()*50);g.userData.x=g.position.x;scene.add(g);clouds.push(g);street.add(g)}
// ciudad de cubos que se suelta: cada cubo tiene su velocidad
const bl=[];const COLS=[0xd9c7a8,0xc2573f,0x8fa6b8,0xe8dfca,0xa86a48,0x6f86a8];
const B=[[-12,-4,6,10,0],[-4.5,-9,5,14,1],[3,-6,6,8,2],[11,-3,5,12,3],[18,-10,7,16,4],[-20,-9,7,13,5],[27,-5,5,9,0],[-29,-4,6,10,2]];
for(const[x0,z0,w,h,c]of B)for(let y=0;y<h;y++)for(let a=0;a<w;a++)for(let b=0;b<w;b++){if(a>0&&a<w-1&&b>0&&b<w-1)continue;const win=(y%2===1&&(a+b)%2===1);bl.push({p:[x0+a-w/2,y+.5,z0+b-w/2],c:win?0x25324e:COLS[c],v:[34+R()*38+y*1.8,3+R()*9+y*.4,(R()-.5)*10],w:[R()*8,R()*8,R()*8],d:y*.012+R()*.12})}
const inst=new THREE.InstancedMesh(new THREE.BoxGeometry(1,1,1),new THREE.MeshStandardMaterial({roughness:.8}),bl.length);inst.castShadow=true;inst.receiveShadow=true;inst.frustumCulled=false;street.add(inst);bl.forEach((b,i)=>inst.setColorAt(i,new THREE.Color(b.c)));
// coches y árboles
const props=[];const carC=[0xe0344a,0x2d6be0,0xf0a020,0x18b89a];for(let i=0;i<5;i++){if(i===2)continue;const g=new THREE.Group();const a=box(3.4,.8,1.6,carC[i%4],.1);a.position.y=.75;const b=box(1.8,.7,1.4,0x18202e,.08);b.position.y=1.45;g.add(a,b);[[-1.1,.7],[1.1,.7],[-1.1,-.7],[1.1,-.7]].forEach(([x,z])=>{const w=box(.6,.6,.25,0x15151a,.05);w.position.set(x,.32,z);g.add(w)});g.position.set(-38+i*15,0,6);g.userData={o:g.position.clone(),v:[52+R()*25,5+R()*7,(R()-.5)*6],w:[R()*5,R()*5,R()*5]};street.add(g);props.push(g)}
for(let i=0;i<9;i++){const g=new THREE.Group();const a=box(.6,2.4,.6,0x6b4a2e,.04);a.position.y=1.2;const b=box(2.6,2.6,2.6,0x3f9a48,.12);b.position.y=3.4;g.add(a,b);g.position.set(-30+i*7.3+R(),0,3+R()*1.2);g.userData={o:g.position.clone(),v:[40+R()*22,6+R()*8,(R()-.5)*7],w:[R()*5,R()*5,R()*5]};street.add(g);props.push(g)}
// estelas de velocidad
const streaks=[];for(let i=0;i<80;i++){const m=new THREE.Mesh(new THREE.BoxGeometry(5+R()*9,.05,.05),new THREE.MeshBasicMaterial({color:0xffffff,transparent:true,opacity:.55}));m.position.set((R()-.5)*90,.8+R()*22,-8+R()*26);m.userData.v=70+R()*70;street.add(m);streaks.push(m)}
const hero=capataz();scene.add(hero.g);
// globo de cubos: k=0 hoy; k=1 océanos en los polos
const globe=new THREE.Group();scene.add(globe);globe.visible=false;const NG=11000,GR=10;const GC=[];
const noise=(x,y,z)=>Math.sin(x*3.1+1.3)*Math.cos(y*3.7-.7)+Math.sin(y*2.9+z*4.3)*.8+Math.cos(z*3.3-x*2.7+2)*.7+Math.sin(x*6.7+z*5.1)*.3;
const gi=new THREE.InstancedMesh(new THREE.BoxGeometry(.5,.5,.5),new THREE.MeshStandardMaterial({roughness:.6}),NG);gi.frustumCulled=false;globe.add(gi);const O=new THREE.Object3D(),Y=V3(0,0,1);
for(let i=0;i<NG;i++){const y=1-2*(i+.5)/NG,rad=Math.sqrt(1-y*y),a=i*Math.PI*(3-Math.sqrt(5));const x=Math.cos(a)*rad,z=Math.sin(a)*rad;GC.push({x,y,z,lat:Math.abs(y),land:noise(x,y,z)>.55,sh:.92+((i*7)%5)*.03})}
const C=new THREE.Color(),OC=new THREE.Color(0x1467c8),OC2=new THREE.Color(0x0c4fae),LC=new THREE.Color(0x58a84a),DC=new THREE.Color(0xc9a868),ICEC=new THREE.Color(0xeef6ff);
function drawGlobe(k){GC.forEach((g,i)=>{const p=g.lat;// el agua abandona el ecuador primero y se apila en los polos
 const dry=1-ss(k*.58-.06,k*.58+.02,p);const wet=k*ss(.56,.74,p);let w=g.land?0:1;let h=GR+(g.land?.22:0);
 if(p>.92&&!g.land)C.copy(ICEC);else if(w)C.copy(i%2?OC:OC2);else C.copy(LC);
 if(!g.land&&k>0&&dry>0){C.lerp(DC,dry);}
 if(wet>.05){C.copy(i%2?OC:OC2);h=GR+wet*1.5}
 if(g.land&&p<.62)C.lerp(DC,.25*k);
 C.multiplyScalar(g.sh);gi.setColorAt(i,C);O.position.set(g.x*h,g.y*h,g.z*h);O.lookAt(0,0,0);O.updateMatrix();gi.setMatrixAt(i,O.matrix)});gi.instanceColor.needsUpdate=true;gi.instanceMatrix.needsUpdate=true}
// estrellas
{const n=900,p=new Float32Array(n*3);for(let i=0;i<n;i++){const a=R()*6.28,b=Math.acos(2*R()-1),d=130+R()*40;p[i*3]=d*Math.sin(b)*Math.cos(a);p[i*3+1]=d*Math.cos(b);p[i*3+2]=d*Math.sin(b)*Math.sin(a)}const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.BufferAttribute(p,3));var stars=new THREE.Points(g,new THREE.PointsMaterial({color:0xdfe6ff,size:.55,fog:false}));stars.visible=false;scene.add(stars)}
// CTA: isla y luna de cubos
const isle=new THREE.Group();isle.visible=false;scene.add(isle);{const a=box(9,2.4,9,0x4a3a2c,.08);a.position.y=-1.2;const b=box(9.3,.5,9.3,0x6fb24e,.08);b.position.y=-.1;isle.add(a,b)}
const moon=new THREE.Group();moon.visible=false;scene.add(moon);{const n=4200,I=new THREE.InstancedMesh(new THREE.BoxGeometry(.62,.62,.62),new THREE.MeshStandardMaterial({roughness:1}),n);const o=new THREE.Object3D();for(let i=0;i<n;i++){const y=1-2*(i+.5)/n,rd=Math.sqrt(1-y*y),a=i*2.39996;const x=Math.cos(a)*rd,z=Math.sin(a)*rd;const c=noise(x*2,y*2,z*2)>.5?.62:.9;o.position.set(x*6,y*6,z*6);o.lookAt(0,0,0);o.updateMatrix();I.setMatrixAt(i,o.matrix);I.setColorAt(i,new THREE.Color(c,c,c*1.02))}moon.add(I)}
const t1=TL.s1[0],t2=TL.s2[0],t3=TL.s3[0],t4=TL.s4[0],tC=TL.cta[0],stopT=t2+1.15;
const order=['h','s1','s2','s3','s4','cta'];
const shots={h:{p:V3(-6,4,22),q:V3(9,7.2,0)},s1:{p:V3(2,4.6,27),q:V3(1,5.4,2)},s2:{p:V3(-10,5.5,30),q:V3(8,8,0)},s3:{p:V3(0,10,70),q:V3(0,6,0)},s4:{p:V3(30,8,62),q:V3(0,6,0)},cta:{p:V3(0,5,30),q:V3(0,1,0)}};
const go=camera(cam,order,shots,TL,.45);
function launch(tau,shake){const o=new THREE.Object3D();bl.forEach((b,i)=>{const a=Math.max(0,tau-b.d);const x=b.p[0]+b.v[0]*a,y=Math.max(.5,b.p[1]+b.v[1]*a-9.8*a*a*.5),z=b.p[2]+b.v[2]*a;o.position.set(x,y,z);o.rotation.set(b.w[0]*a,b.w[1]*a,b.w[2]*a);o.updateMatrix();inst.setMatrixAt(i,o.matrix)});inst.instanceMatrix.needsUpdate=true;
 props.forEach(g=>{g.visible=!window._hideProps;const u=g.userData,a=Math.max(0,tau);g.position.set(u.o.x+u.v[0]*a,Math.max(0,u.o.y+u.v[1]*a-4.9*a*a),u.o.z+u.v[2]*a);g.rotation.set(u.w[0]*a,u.w[1]*a,u.w[2]*a)})}
window.renderAt=t=>{const s=segAt(TL,t),m=mouthAt(t);
 // tau: tiempo desde que se suelta. En el gancho, cámara lenta del desastre (bucle abierto); en s1 volvemos atrás.
 const inGlobe=s==='s3'||s==='s4';const inCta=s==='cta';
 let tau=0,slow=false;if(s==='h'){tau=.3+t*.05;slow=true}else if(s==='s1')tau=0;else if(s==='s2')tau=Math.max(0,t-stopT);
 street.visible=!inGlobe&&!inCta;globe.visible=inGlobe;stars.visible=inGlobe||inCta;isle.visible=inCta;moon.visible=inCta;hero.g.visible=!inGlobe;
 if(street.visible){window._hideProps=s==='h';launch(s==='h'?tau:tau*.42);const K=s==='h'?.75:clamp(tau*1.2);scene.background=C.copy(sky).lerp(dust,K*.75).clone();scene.fog.color.copy(scene.background);scene.fog.far=190-K*90;
  streaks.forEach(m_=>{m_.visible=tau>.05;if(m_.visible){const x=m_.userData.v*tau*(slow?1:1);m_.position.x=((m_.position.x+0)+0);m_.scale.x=1;const base=m_.userData.b??(m_.userData.b=m_.position.x);m_.position.x=((base+x+50)%100+100)%100-50}});
  clouds.forEach(g=>{g.position.x=g.userData.x+tau*14});hemi.intensity=1.5;S.intensity=2.6*(1-K*.3)}
 else{scene.background=dark;scene.fog.far=2000;hemi.intensity=inCta?.5:(s==='s3'?1.0:.05);hemi.color.set(0xdfe6ff);S.intensity=s==='s4'?3.8:(s==='s3'?1.9:1.5);S.position.set(s==='s4'?70:-30,s==='s4'?10:30,s==='s4'?-6:40);S.castShadow=false}
 if(street.visible)S.castShadow=true;
 // personaje
 if(street.visible){if(tau>0){const a=tau;if(s==='h'){hero.g.position.set(.2+a*1.2,3.4+Math.sin(t*2)*.15,9.5);hero.g.rotation.order='YXZ';hero.g.rotation.set(0,-.6,-1.25+Math.sin(t*1.6)*.1)}else{{const e=ss(0,.5,a);hero.g.position.set(1-e*3.2+a*.25,Math.min(4.5,.1+e*3)+Math.sin(t*3)*.2,7+e*6.5);hero.g.rotation.order='YXZ';hero.g.rotation.set(0,-.56*e,-1.2*e+Math.sin(a*3)*.2*e)}};hero.pose(t,.9,{armsUp:.7})}else{const a=clamp((t-t1)/2);hero.g.position.set(1,0,7);hero.g.rotation.order='XYZ';hero.g.rotation.set(0,-.15,0);hero.pose(t,m,{look:-.1,wave:s==='s1'?clamp(1-Math.abs(t-t1-1.2)):0})}}
 if(inCta){hero.g.position.set(0,.15,1);hero.g.rotation.order='XYZ';hero.g.rotation.set(0,-.1,0);hero.pose(t,m,{wave:1,look:.05})}
 // globo
 if(inGlobe){const k=s==='s3'?ss(t3+1.4,t4-.6,t):1;drawGlobe(k);globe.rotation.y=s==='s3'?t*.2:(t3*.2+(t4-t3)*.2);globe.rotation.x=.22}
 if(inCta){moon.position.set(5,9.6,-14);moon.rotation.y=t*.2;const f=(t-tC)>1.6?(Math.sin(t*18)>.3?1:.18):1;moon.scale.setScalar(1.3*(f>.5?1:.96));moon.traverse(o=>{if(o.isInstancedMesh)o.material.opacity=f});const u=moon.children[0];u.material.transparent=true}
 go(t,(p,q)=>{if(s==='h'){p.x+=t*.45}if(s==='s2'&&tau>0&&tau<1.3){const a=(1.3-tau)*.32;p.x+=Math.sin(t*63)*a;p.y+=Math.cos(t*71)*a}if(s==='s4'){const u=clamp((t-t4)/(tC-t4));p.x=Math.sin(u*1.6+.45)*70;p.z=Math.cos(u*1.6+.45)*70;p.y=10;q.set(0,6,0)}});
 r.render(scene,cam);return true};
window.ready=true;
