// Mito: 'si te pones bizco, te quedas así' (2503). AAO 'Five vision myths'; UT Austin Think Twice (Nathan Ngo, 29/04/2023).
// Nuevo (v28): ojos que CONVERGEN de verdad en los personajes (crossEyes: pupilas que siguen a un objetivo 3D), DEDO que se acerca a la nariz,
// PAR DE OJOS de vóxeles con MÚSCULO interno (recto medio) que se contrae y medidor de cansancio. Salón reutilizable (sofá, tele, lámpara, cuadro).
import {THREE,J,mk,ss,V3,clamp,stage,sun,box,glow,capataz,abuela,segAt,mouthAt,label3d,puffs} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0xf3e3c8,fog:[0xf3e3c8,40,140],exposure:1.1});cam.far=3000;cam.updateProjectionMatrix();const R=mk(2503);
const hemi=new THREE.HemisphereLight(0xfff2dc,0x6a5040,1.25);scene.add(hemi);const S=sun(scene,{pos:[-8,20,16],span:16,power:2.2});
// ---------- salón
const ROOM=new THREE.Group();scene.add(ROOM);
const fl=new THREE.Mesh(new THREE.PlaneGeometry(40,40),new THREE.MeshStandardMaterial({color:0xa8784e,roughness:.85}));fl.rotation.x=-Math.PI/2;fl.receiveShadow=true;ROOM.add(fl);
for(let i=0;i<12;i++){const p=box(2.1,.04,40,i%2?0xb4845a:0x9c6c44,.01);p.position.set(-12+i*2.2,.02,0);ROOM.add(p)}
const back=box(40,14,.5,0xe9d8b6,.05);back.position.set(0,7,-8);ROOM.add(back);
for(let i=0;i<14;i++){const s=box(.25,14,.1,0xdcc8a2,.01);s.position.set(-18+i*2.8,7,-7.7);ROOM.add(s)}
const rug=box(10,.06,6,0x2f6a8a,.02);rug.position.set(0,.06,1);ROOM.add(rug);const rug2=box(8.6,.07,4.6,0xd8a03a,.02);rug2.position.set(0,.07,1);ROOM.add(rug2);
const sofa=new THREE.Group();{const b=box(9,1.6,3,0xc0392b,.3);b.position.y=1.1;sofa.add(b);const bk=box(9,2.6,1,0xb03228,.3);bk.position.set(0,2.4,-1.2);sofa.add(bk);[-4.6,4.6].forEach(x=>{const a=box(1,2.2,3,0xb03228,.3);a.position.set(x,1.5,0);sofa.add(a)});[-2,2].forEach(x=>{const c=box(3.4,.6,2.2,0xd94a3a,.25);c.position.set(x,2.1,.2);sofa.add(c)})}
sofa.position.set(-1,0,-5.6);ROOM.add(sofa);
const pic=new THREE.Group();{const f=box(4.2,3,.2,0x7a5232,.05);pic.add(f);const im=box(3.7,2.5,.1,0x7fc8ff,.02);im.position.z=.08;pic.add(im);const hill=box(3.7,1,.12,0x58a84a,.02);hill.position.set(0,-.75,.1);pic.add(hill);const sn=box(.6,.6,.12,0xffd84a,.1);sn.position.set(1.1,.6,.12);pic.add(sn)}
pic.position.set(-1,7.6,-7.6);ROOM.add(pic);
const lamp=new THREE.Group();{const p=box(.2,6,.2,0x30343e,.03);p.position.y=3;lamp.add(p);const sh=box(1.8,1.2,1.8,0xfff0c8,.2,{emissive:0xffd890,emissiveIntensity:.8});sh.position.y=6.4;lamp.add(sh);const bs=box(1.2,.2,1.2,0x30343e,.05);bs.position.y=.1;lamp.add(bs)}
lamp.position.set(6.8,0,-5.8);ROOM.add(lamp);const lg=glow(0xffd890,5,.4);lg.position.set(6.8,6.4,-5.8);ROOM.add(lg);
const plant=new THREE.Group();{const pt=box(1.2,1.2,1.2,0xc86a3a,.1);pt.position.y=.6;plant.add(pt);for(let i=0;i<6;i++){const l=box(.4,1.8,.9,0x3f9a46,.15);l.position.set(Math.cos(i)*.4,1.9,Math.sin(i)*.4);l.rotation.set(Math.sin(i)*.4,i,Math.cos(i)*.4);plant.add(l)}}
plant.position.set(-8.4,0,-5.2);ROOM.add(plant);
// personajes: el capataz (hace el bizco) y la abuela (avisa)
const kid=capataz();kid.g.position.set(1.2,0,1.5);scene.add(kid.g);
const gran=abuela();gran.g.position.set(-3.6,0,.8);gran.g.rotation.y=.75;scene.add(gran.g);
const bubble=label3d(['¡QUE TE','*QUEDAS ASÍ!'],{w:6,h:2.4,px:130,sprite:true,bg:'#ffffff',fg:'#10131f',accent:'#ff4a4a'});scene.add(bubble);
const finger=new THREE.Group();{const body=new THREE.Mesh(new THREE.CylinderGeometry(.13,.13,1.9,6),new THREE.MeshStandardMaterial({color:0xffc42e,roughness:.6}));body.position.y=.95;finger.add(body);const ws=new THREE.Mesh(new THREE.CylinderGeometry(.13,.02,.38,6),new THREE.MeshStandardMaterial({color:0xf1d2a8,roughness:.8}));ws.position.y=2.09;finger.add(ws);const tip=new THREE.Mesh(new THREE.ConeGeometry(.05,.12,6),new THREE.MeshStandardMaterial({color:0x2a2a30}));tip.position.y=2.3;finger.add(tip);const er=new THREE.Mesh(new THREE.CylinderGeometry(.135,.135,.26,6),new THREE.MeshStandardMaterial({color:0xff7a9a,roughness:.7}));er.position.y=-.1;finger.add(er)}scene.add(finger);
const panel=label3d(['OFTALMÓLOGOS:','*NO SE QUEDAN ASÍ'],{w:8,h:2.6,px:110,accent:'#4ade80'});scene.add(panel);
const chk=new THREE.Group();[[-.55,-.2,.8,.7],[.5,.35,1.6,-.85]].forEach(([x,y,l,a])=>{const b=box(l,.38,.4,0x4ade80,.08,{emissive:0x22aa55,emissiveIntensity:1});b.position.set(x,y,0);b.rotation.z=a;chk.add(b)});scene.add(chk);
const causes=label3d(['ESTRABISMO DE VERDAD:','VISTA SIN CORREGIR','NERVIOS O MÚSCULOS','*→ AL OFTALMÓLOGO'],{w:8.4,h:4.6,px:90,accent:'#4de3ff'});scene.add(causes);
// v28 crossEyes: cada pupila se desplaza hacia la proyección del objetivo (cuanto más cerca, más bizco)
const tmp=V3();
function crossEyes(o,target,amt=1){o.eyes.forEach(e=>{const p=e.userData.p;const sx=Math.sign(e.position.x);p.position.x=-sx*.085*amt;p.position.y=-.05*amt;e.rotation.y=-sx*.3*amt})}
// ---------- par de ojos de vóxeles con recto medio (músculo) y medidor de cansancio
const EYES=new THREE.Group();EYES.position.set(1200,0,0);scene.add(EYES);
const eL=new THREE.PointLight(0xffffff,40,70,1.2);eL.position.set(4,8,16);EYES.add(eL);const eL2=new THREE.PointLight(0xffc8a0,16,60,1.2);eL2.position.set(-8,-4,10);EYES.add(eL2);
const vs=.36;const VO=[];for(let x=-3.4;x<=3.4;x+=vs)for(let y=-3.4;y<=3.4;y+=vs)for(let z=-3.4;z<=3.4;z+=vs){const d=Math.hypot(x,y,z);if(d<3.3&&d>2.85&&z>-1.2)VO.push([x,y,z])}
const mkEye=()=>{const g=new THREE.Group();const im=new THREE.InstancedMesh(new THREE.BoxGeometry(vs*.94,vs*.94,vs*.94),new THREE.MeshStandardMaterial({roughness:.45}),VO.length);im.frustumCulled=false;const O=new THREE.Object3D(),C=new THREE.Color();VO.forEach(([x,y,z],i)=>{O.position.set(x,y,z);O.updateMatrix();im.setMatrixAt(i,O.matrix);const rr=Math.hypot(x,y);im.setColorAt(i,C.setHex(z>2.4&&rr<.8?0x080808:z>2.0&&rr<1.7?(rr>1.3?0x6a3e1e:0x9a5a2a):0xf4f0ea))});g.add(im);const sh=box(.5,.5,.2,0xffffff,.1,{emissive:0xffffff,emissiveIntensity:1.5});sh.position.set(-.6,.75,3.35);g.add(sh);return g};
const EY=[mkEye(),mkEye()];EY[0].position.set(-4.4,0,0);EY[1].position.set(4.4,0,0);EYES.add(...EY);
const MUS=[0,1].map(i=>{const m=box(1,1,3.2,0xd84a4a,.3,{emissive:0x5a0a0a,emissiveIntensity:.4});EYES.add(m);return m});
const nose=box(1.6,2.6,1.6,0xd9a06a,.3);nose.position.set(0,-1.2,2.4);EYES.add(nose);
const meter=new THREE.Group();EYES.add(meter);meter.position.set(0,-6.4,0);meter.add(box(9,.9,.9,0x20263a,.2));const mf=box(1,.72,.95,0x4ade80,.2,{emissive:0x22aa55,emissiveIntensity:.7});meter.add(mf);
const mlab=label3d(['CANSANCIO','*0 %'],{w:6,h:1.6,px:120,bg:null});mlab.position.set(0,-4.7,1);EYES.add(mlab);
const mname=label3d(['*RECTO MEDIO'],{w:6,h:1.2,px:110,sprite:true,accent:'#ff7a7a'});EYES.add(mname);
const ZZ=[0,1,2].map(()=>{const z=label3d(['*?'],{w:1,h:1,px:140,sprite:true,bg:''});scene.add(z);return z});
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],k=ss(0,d,lt),m=mouthAt(t);
 const inE=s==='s3';ROOM.visible=kid.g.visible=gran.g.visible=!inE;EYES.visible=inE;scene.background.setHex(inE?0x1a1020:0xf3e3c8);scene.fog.near=inE?2000:40;scene.fog.far=inE?3000:140;
 bubble.visible=panel.visible=chk.visible=causes.visible=finger.visible=false;ZZ.forEach(z=>z.visible=false);let p,q;
 const hp=V3();kid.head.getWorldPosition(hp);
 if(!inE){kid.pose(t,s==='s1'||s==='s4'?0:m*.3,{wave:s==='cta'?1:0,look:0});gran.pose(t,s==='h'?m*.7:0,{point:s==='h'?1:0,look:.1,wave:s==='cta'?1:0});
  scene.updateMatrixWorld();kid.head.getWorldPosition(hp);const nosePt=hp.clone().add(V3(0,-.05,.9));
  let cross=0,tgt=null;
  if(s==='h'){cross=1;bubble.visible=true;bubble.position.set(-2.4,5.4,1.6);const b=.94+.06*Math.sin(t*6);bubble.scale.set(3.4*b,1.36*b,1)}
  if(s==='s1'){cross=1-ss(.2,1.2,lt);tgt=nosePt;panel.visible=true;panel.position.set(-1.6,3.3,1.6);panel.scale.setScalar(.46*ss(0,.6,lt));chk.visible=lt>1;chk.position.set(-1.6,4.7,1.8);chk.scale.setScalar(.7*ss(1,1.6,lt)*(1+.06*Math.sin(t*6)))}
  if(s==='s2'){// el dedo se acerca a la nariz y los ojos lo siguen hasta quedar bizcos; luego se aparta
   const a=ss(.6,d*.55,lt),b=ss(d*.75,d*.95,lt);const dist=3.6-2.75*a+2.75*b;finger.visible=true;finger.position.copy(hp).add(V3(0,-2.15,dist));tgt=null;cross=clamp((3.6-dist)/2.75)}
  if(s==='s4'){causes.visible=true;causes.position.set(-1.1,3.2,1.6);causes.scale.setScalar(.41*ss(0,.8,lt))}
  if(s==='cta'){cross=ss(d*.4,d*.6,lt);tgt=nosePt}
  crossEyes(kid,tgt,cross);gran.eyes.forEach(e=>{e.userData.p.position.set(0,0,0)});
  if(s==='h'){const e=ss(d*.35,d*.8,lt);p=V3(1.2-2.2*e,3.4+.9*e,8+10*e);q=V3(1.2-2.2*e,3.15+.5*e,1.5)}
  else if(s==='s1'){p=V3(0,4,20+k);q=V3(0,3.6,1)}
  else if(s==='s2'){p=V3(1.9-k*.4,3.5,7.6);q=V3(1.2,3.0,2.2)}
  else if(s==='s4'){p=V3(0,4,20+k);q=V3(0,3.6,1)}
  else{p=V3(-1,2.6,19+k);q=V3(-1,2.2,0)}// CTA: personajes por encima del botón de seguir
  S.target.position.set(q.x,0,q.z);S.target.updateMatrixWorld()}
 else{// s3: el par de ojos converge (los rectos medios se acortan), cansancio sube, descansan y vuelven
  const c=ss(.3,d*.4,lt)*(1-ss(d*.62,d*.85,lt));const ang=.42*c;EY[0].rotation.y=ang+Math.sin(t*2)*.01;EY[1].rotation.y=-ang;
  MUS.forEach((mm,i)=>{const sx=i?1:-1;const len=3.2-1.3*c;mm.scale.set(1+.45*c,1+.45*c,len/3.2);mm.position.set(sx*1.6,0,-1.2);mm.rotation.y=sx*-.35;mm.material.emissiveIntensity=.4+1.2*c});
  const tired=Math.min(1,ss(.3,d*.55,lt)*.8)*(1-ss(d*.65,d*.95,lt));mf.scale.x=Math.max(.05,tired*9);mf.position.x=-4.5+tired*4.5;const col=tired>.4?0xffa83a:0x4ade80;mf.material.color.setHex(col);mf.material.emissive.setHex(col);mlab.set(['CANSANCIO',`*${Math.round(tired*100)} %`]);
  mname.visible=lt>.8&&lt<d*.7;mname.position.set(0,4.6,-1);mname.scale.set(7,1.4,1);
  p=V3(Math.sin(t*.3)*1.5,1.5,34-k*2).add(EYES.position);q=V3(0,-1.2,0).add(EYES.position)}
 cam.position.copy(p);cam.lookAt(q);r.render(scene,cam)};
window.ready=true;
