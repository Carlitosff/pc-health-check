// Mito: 'leer con poca luz te estropea la vista' (2203). Vreeman y Carroll, BMJ dic-2007.
// Reutilizable: DORMITORIO DE NOCHE con lectura bajo la LINTERNA (libro abierto, haz de luz volumétrico, puerta con luz de pasillo),
// OJO de vóxeles con PÁRPADO que se cierra de cansancio y MEDIDOR DE VISTA integrado (eyeRig), bocadillo de la abuela.
import {THREE,J,mk,ss,V3,clamp,stage,sun,box,glow,capataz,abuela,segAt,mouthAt,label3d,bed,lieDown,puffs} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x0a0f26,fog:[0x0a0f26,40,120],exposure:1.25});cam.far=3000;cam.updateProjectionMatrix();const R=mk(2203);
const hemi=new THREE.HemisphereLight(0x7f94d8,0x2a2030,.75);scene.add(hemi);sun(scene,{pos:[-10,20,-14],span:16,color:0xb8c8ff,power:.7});
// ---------- dormitorio
const ROOM=new THREE.Group();scene.add(ROOM);
const fl=new THREE.Mesh(new THREE.PlaneGeometry(30,30),new THREE.MeshStandardMaterial({color:0x5e4232,roughness:.9}));fl.rotation.x=-Math.PI/2;fl.receiveShadow=true;ROOM.add(fl);
for(let i=0;i<7;i++){const p=box(2.1,.04,30,i%2?0x6e4c36:0x5a3e2e,.01);p.position.set(-7+i*2.2,.02,0);ROOM.add(p)}
const rug=box(6,.06,4,0x2f6a8a,.02);rug.position.set(1,.06,3.2);ROOM.add(rug);
const back=box(30,12,.5,0x2c3462,.05);back.position.set(0,6,-8);ROOM.add(back);
const left=box(.5,12,30,0x323a6c,.05);left.position.set(-8,6,0);ROOM.add(left);
const win=new THREE.Group();{const f=box(5,4.4,.4,0x8a6a4a,.08);win.add(f);const g=box(4.3,3.7,.3,0x0a1030,.02,{emissive:0x14205a,emissiveIntensity:.7});g.position.z=.12;win.add(g);const mo=new THREE.Mesh(new THREE.SphereGeometry(.65,20,14),new THREE.MeshBasicMaterial({color:0xfff4c8,toneMapped:false}));mo.position.set(1,.9,.3);win.add(mo);const mg=glow(0xfff0c0,3,.6);mg.position.set(1,.9,.4);win.add(mg);for(let i=0;i<9;i++){const s=box(.09,.09,.05,0xffffff,.01,{emissive:0xffffff,emissiveIntensity:1});s.position.set((R()-.5)*3.8,(R()-.5)*3,.3);win.add(s)}const bar=box(.2,3.7,.35,0x8a6a4a,.02);bar.position.z=.2;win.add(bar)}
win.position.set(-3.6,6.6,-7.6);ROOM.add(win);
// puerta abierta con luz de pasillo (derecha)
const door=box(3,6.6,.3,0xffd9a0,.02,{emissive:0xffb060,emissiveIntensity:1.1});door.position.set(6.2,3.3,-7.7);ROOM.add(door);
const dgl=glow(0xffc070,9,.35);dgl.position.set(6.2,3.4,-7.2);ROOM.add(dgl);
const hall=new THREE.PointLight(0xffb870,40,22,1.6);hall.position.set(6.2,5,-5.5);ROOM.add(hall);
// estantería y mesilla con reloj
const sh=box(1.2,7,4,0x6a4a30,.06);sh.position.set(-7.2,3.5,1.5);ROOM.add(sh);
const BKC=[0xd84a3a,0x3a8ad8,0xf2c230,0x4ab06a,0x9a5cd6,0xff8a3a];for(let k=0;k<3;k++)for(let i=0;i<7;i++){const b=box(.8,1.2+R()*.4,.4,BKC[(i+k)%6],.03);b.position.set(-6.75,1.2+k*2.2+.6,-.2+i*.5);ROOM.add(b)}
const B=bed(0x3a6fd8);B.position.set(.8,0,-3.2);ROOM.add(B);
const nt=box(1.8,2,1.8,0x7a4e2e,.08);nt.position.set(-2.4,1,-6.2);ROOM.add(nt);
const clock=label3d(['23:30'],{w:1.9,h:.8,px:170,bg:'#0b0d14',fg:'#ff4a4a',accent:'#2a2f40'});clock.position.set(-2.4,2.45,-5.25);ROOM.add(clock);
// lectora en la cama con libro y linterna
const reader=capataz();reader.hat.forEach(h=>h.visible=false);const L=lieDown(reader,B,0x3a6fd8);const sitUp=a=>{reader.g.rotation.x=-a};sitUp(1.0);
const book=new THREE.Group();{const cv=box(2.2,.12,1.6,0xc0392b,.03);book.add(cv);[-1,1].forEach(s=>{const pg=box(1.02,.1,1.48,0xf8f2e2,.02);pg.position.set(s*.53,.1,0);pg.rotation.z=-s*.12;book.add(pg);for(let i=0;i<5;i++){const ln=box(.8,.02,.08,0x2a2a2a,.005);ln.position.set(s*.53,.17+(-s*.06),-.5+i*.25);ln.rotation.z=-s*.12;book.add(ln)}})}
book.position.set(0,4.35,.55);B.add(book);
const fla=new THREE.Group();/*linterna*/{const b=box(.35,.35,1.1,0x30343e,.06);fla.add(b);const lens=box(.42,.42,.12,0xfff6c8,.04,{emissive:0xfff0b0,emissiveIntensity:2});lens.position.z=.58;fla.add(lens)}
fla.position.set(1.35,3.9,-.4);fla.scale.setScalar(.75);B.add(fla);
const beamM=new THREE.MeshBasicMaterial({color:0xfff0b0,transparent:true,opacity:.16,blending:THREE.AdditiveBlending,depthWrite:false,side:THREE.DoubleSide});
const beam=new THREE.Mesh(new THREE.ConeGeometry(1.2,2.6,24,1,true),beamM);scene.add(beam);
const spot=new THREE.SpotLight(0xfff0c0,60,14,.55,.5,1.5);scene.add(spot,spot.target);
const fglow=glow(0xfff0b0,2.4,.8);scene.add(fglow);
// abuela en la puerta, con bocadillo
const gran=abuela();gran.g.position.set(5.6,0,-5.4);gran.g.rotation.y=-2.2;ROOM.add(gran.g);
const bubble=label3d(['¡TE VAS A','*QUEDAR CIEGA!'],{w:6.2,h:2.4,px:130,sprite:true,bg:'#ffffff',fg:'#10131f',accent:'#ff4a4a'});scene.add(bubble);
const ZZ=[0,1,2].map(()=>{const z=label3d(['*Z'],{w:1,h:1,px:140,sprite:true,bg:''});scene.add(z);return z});
const late=label3d(['*03:12','SIN DORMIR'],{w:5,h:2.2,px:120,sprite:true,accent:'#ff4a4a'});scene.add(late);
// ---------- ojo de vóxeles con párpado y medidor de vista
const EYE=new THREE.Group();EYE.position.set(1200,0,0);scene.add(EYE);
const eL=new THREE.PointLight(0xffffff,30,60,1.2);eL.position.set(4,6,14);EYE.add(eL);const eL2=new THREE.PointLight(0x8fb0ff,14,60,1.2);eL2.position.set(-8,-4,10);EYE.add(eL2);
const VO=[];const vs=.32;for(let x=-4;x<=4;x+=vs)for(let y=-4;y<=4;y+=vs)for(let z=-4;z<=4;z+=vs){const d=Math.hypot(x,y,z);if(d<4&&d>3.5&&z>-1)VO.push([x,y,z])}
const eim=new THREE.InstancedMesh(new THREE.BoxGeometry(vs*.94,vs*.94,vs*.94),new THREE.MeshStandardMaterial({roughness:.45}),VO.length);eim.frustumCulled=false;EYE.add(eim);
const red=new Set();{const O=new THREE.Object3D(),C=new THREE.Color();VO.forEach(([x,y,z],i)=>{O.position.set(x,y,z);O.updateMatrix();eim.setMatrixAt(i,O.matrix);const rr=Math.hypot(x,y);let c=z>3&&rr<.95?0x080808:z>2.6&&rr<2.05?(rr>1.6?0x1f6a5a:0x3aa88a):0xf4f0ea;if(c===0xf4f0ea&&R()<.07)red.add(i);eim.setColorAt(i,C.setHex(c))})}
const setRed=k=>{const C=new THREE.Color();red.forEach(i=>{eim.setColorAt(i,C.setHex(0xf4f0ea).lerp(new THREE.Color(0xd84040),k))});eim.instanceColor.needsUpdate=true};
const shine=box(.6,.6,.2,0xffffff,.1,{emissive:0xffffff,emissiveIntensity:1.5});shine.position.set(-.8,.9,4.05);EYE.add(shine);
const LID=new THREE.Group();EYE.add(LID);{const lid=box(9.4,8,1.2,0xd9a06a,.4);lid.position.set(0,4,0);LID.add(lid);for(let i=0;i<9;i++){const la=box(.14,.9,.14,0x20141a,.03);la.position.set(-3.6+i*.9,-.25,.3);la.rotation.x=.5;LID.add(la)}}
LID.position.set(0,6,4.0);
const meter=new THREE.Group();EYE.add(meter);meter.position.set(0,-7.2,0);const mb=box(9,.9,.9,0x20263a,.2);meter.add(mb);const mf=box(1,.72,.95,0x4ade80,.2,{emissive:0x22aa55,emissiveIntensity:.7});meter.add(mf);
const mlab=label3d(['VISTA','*100 %'],{w:6,h:1.6,px:120,bg:null});mlab.position.set(0,-5.4,1);EYE.add(mlab);
const panel=label3d(['¿DAÑO PERMANENTE?','*NO'],{w:9,h:3,px:120,accent:'#4ade80'});panel.position.set(0,-6.6,1.5);EYE.add(panel);
const chk=new THREE.Group();[[-.55,-.2,.8,.7],[.5,.35,1.6,-.85]].forEach(([x,y,l,a])=>{const b=box(l,.38,.4,0x4ade80,.08,{emissive:0x22aa55,emissiveIntensity:1});b.position.set(x,y,0);b.rotation.z=a;chk.add(b)});chk.position.set(3.4,3.4,4.6);EYE.add(chk);
const tears=puffs(scene,24,.28,0x9ad8ff,{opacity:.8});
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],k=ss(0,d,lt),m=mouthAt(t);
 const inEye=s==='s1'||s==='s2'||s==='s3';ROOM.visible=!inEye;EYE.visible=inEye;beam.visible=spot.visible=fglow.visible=!inEye&&s!=='cta';
 scene.background.setHex(inEye?0x0d1330:0x0a0f26);scene.fog.near=inEye?2000:40;scene.fog.far=inEye?3000:120;
 bubble.visible=false;late.visible=false;ZZ.forEach(z=>z.visible=false);panel.visible=s==='s1';chk.visible=s==='s1';mlab.visible=meter.visible=s!=='s1';
 for(let i=0;i<24;i++)tears.set(i,0,-999,0,.01);
 // lectora: respira, mira el libro; la linterna tiembla un poco
 const br=Math.sin(t*1.6);L.blanket.scale.y=1+.08*br;sitUp(s==='cta'?Math.PI/2:1.0);reader.pose(t,0,{});reader.head.rotation.x=.25;reader.armL.rotation.set(-1.35,0,.25);reader.armR.rotation.set(-1.35,0,-.25);
 scene.updateMatrixWorld();{const hp=V3();reader.head.getWorldPosition(hp);book.position.set(0,s==='cta'?2.9:3.75,s==='cta'?.2:1.05);book.scale.setScalar(.8);book.lookAt(hp);book.rotateX(Math.PI/2);if(s==='cta'){book.rotation.set(0,0,0)}}
 scene.updateMatrixWorld();const fp=V3(),bp=V3();fla.getWorldPosition(fp);book.getWorldPosition(bp);bp.y+=Math.sin(t*1.3)*.08;fla.lookAt(bp);
 beam.position.copy(fp).lerp(bp,.5);beam.lookAt(bp);beam.rotateX(-Math.PI/2);beam.scale.set(1,fp.distanceTo(bp)/2.6,1);
 spot.position.copy(fp);spot.target.position.copy(bp);fglow.position.copy(fp);
 gran.g.visible=s==='h'||s==='cta';let p,q;
 if(s==='h'){gran.pose(t,m*.6,{point:1,look:.2});bubble.visible=true;bubble.position.set(4.6,6.1,-4.6);bubble.scale.set(5*(.94+.06*Math.sin(t*6)),1.94*(.94+.06*Math.sin(t*6)),1);
  clock.set(['23:30']);p=V3(11.5-k*1.2,11.5,17.5-k*1.6);q=V3(3.1,5.4,-4.4)}
 else if(inEye){EYE.rotation.y=Math.sin(t*.45)*.25;EYE.rotation.x=Math.sin(t*.37)*.08;
  let lid=0,vis=1,col=0x4ade80;
  if(s==='s1'){chk.scale.setScalar(ss(1.2,1.8,lt)*(1+.06*Math.sin(t*6)));setRed(0)}
  if(s==='s2'){lid=ss(.3,d*.6,lt)*.55+.04*Math.sin(t*3);vis=1-.3*ss(.3,d*.7,lt);col=vis<.85?0xffa83a:0x4ade80;setRed(ss(.3,d*.7,lt));
   for(let i=0;i<24;i++){const ph=(t*.6+i/24)%1;tears.set(i,-2.8+(i%3)*.25,-1-ph*6,4.2,ph<.9?1:0)}}
  if(s==='s3'){const o=ss(d*.15,d*.55,lt);lid=.55*(1-o);vis=.7+.3*o;col=o>.6?0x4ade80:0xffa83a;setRed(1-o)}
  LID.position.y=6-lid*9.2;LID.visible=lid>.02;tears.done();mf.scale.x=Math.max(.05,vis*9);mf.position.x=-4.5+vis*4.5;mf.material.color.setHex(col);mf.material.emissive.setHex(col);mlab.set(['VISTA',`*${Math.round(vis*100)} %`]);
  p=V3(Math.sin(t*.3)*1.5,-.6,31-k*2.5).add(EYE.position);q=V3(0,-1.6,0).add(EYE.position)}
 else if(s==='s4'){const hh=Math.floor(ss(0,d*.7,lt)*3.7);clock.set([['23:30','00:45','02:05','03:12'][Math.min(3,hh)]]);
  late.visible=lt>d*.55;late.position.set(4.6,5.8,-6.5);late.material.opacity=ss(d*.55,d*.7,lt);
  if(lt>d*.6){reader.mouth.scale.y=1+2.4*Math.abs(Math.sin(lt*2));}
  p=V3(8.5-k*1.2,9.5,11-k*1.5);q=V3(.4,3.4,-3.6)}
 else{// cta: dormida con el libro en el pecho; la abuela apaga y saluda
  gran.pose(t,0,{wave:1,look:-.3});reader.eyes.forEach(e=>e.scale.y=.1);clock.set(['03:13']);
  ZZ.forEach((zz,i)=>{const ph=(t*.45+i/3)%1;zz.visible=true;zz.position.set(1.8+ph*1.4,3.8+ph*2.4,-5.4);zz.material.opacity=Math.sin(Math.PI*ph)});
  p=V3(3,8.5,16+k*.8);q=V3(3,7.4,-6)}
 cam.position.copy(p);cam.lookAt(q);r.render(scene,cam)};
window.ready=true;
