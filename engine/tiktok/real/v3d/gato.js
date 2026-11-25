// Mito '¿tu gato siempre cae de pie y no se hace daño?' (3303). Fuentes en mito_gato.py.
// Reutilizable: CALLE CON EDIFICIO DE PISOS (fachada con ventanas, balcón con barandilla y RED de seguridad), GATO de bloques (cat(): sentado,
// cola que se mueve, caída con giro de enderezamiento), SALA DE VETERINARIO con un REBAÑO INSTANCIADO de gatos (catHerd: n gatos, vendas,
// colores) y franjas de pisos que se iluminan en la fachada.
import {THREE,J,mk,ss,V3,clamp,stage,sun,box,glow,capataz,segAt,mouthAt,puffs} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x9fd4ff,fog:[0x9fd4ff,90,260],exposure:1.18});cam.far=700;cam.updateProjectionMatrix();const R=mk(3303);
const hemi=new THREE.HemisphereLight(0xcfe8ff,0x5a4a3a,.85);scene.add(hemi);sun(scene,{pos:[-30,60,40],span:40,power:2.2});
const FH=6; // altura de un piso
// ---------- calle
const STREET=new THREE.Group();scene.add(STREET);
const road=box(160,.4,40,0x3a3d44,.02);road.position.set(0,-.2,24);road.receiveShadow=true;STREET.add(road);
const walk=box(160,.6,12,0xc8c2b6,.03);walk.position.set(0,.3,4);walk.receiveShadow=true;STREET.add(walk);
for(let i=0;i<16;i++){const l=box(4,.05,.5,0xf2f2f2,.01);l.position.set(-75+i*10,.02,24);STREET.add(l)}
function tree(x,z){const g=new THREE.Group();const tr=box(.9,4,.9,0x6a4a2e,.05);tr.position.y=2;g.add(tr);[[0,5.2,0,3.6],[1,6.4,.4,2.6],[-.8,6.2,-.3,2.4]].forEach(([a,b,c,s])=>{const f=box(s,s,s,0x4f9a3e,.3);f.position.set(a,b,c);g.add(f)});g.position.set(x,.6,z);STREET.add(g)}
tree(-16,6);tree(17,6);tree(40,6);tree(-40,6);
// ---------- edificio: 20 pisos (la mayoría solo se ve en s4)
const NF=20,BW=34;const BLD=new THREE.Group();scene.add(BLD);
const facade=box(BW,NF*FH,10,0xe8d6b8,.05);facade.position.set(0,NF*FH/2,-7);facade.castShadow=facade.receiveShadow=true;BLD.add(facade);
const WIN=new THREE.InstancedMesh(new THREE.BoxGeometry(3.2,3.6,.3),new THREE.MeshStandardMaterial({color:0x6a9ccc,roughness:.15,metalness:.3,emissive:0x1a2a3a,emissiveIntensity:.4}),NF*5);
{const O=new THREE.Object3D();let k=0;for(let f=0;f<NF;f++)for(let i=0;i<5;i++){O.position.set(-13.2+i*6.6,f*FH+3.4,-1.9);O.updateMatrix();WIN.setMatrixAt(k++,O.matrix)}}BLD.add(WIN);
for(let f=1;f<NF;f++){const c=box(BW+.6,.35,10.6,0xcdb896,.02);c.position.set(0,f*FH,-7);BLD.add(c)}
// franjas de pisos que llegan / no llegan al hospital (s4)
const bandLow=box(BW+1.2,FH*4.6,.4,0x4ade80,.02,{emissive:0x2ad060,emissiveIntensity:1,transparent:true,opacity:0});bandLow.position.set(0,FH*1+FH*4.6/2,-1.5);BLD.add(bandLow);
const bandHi=box(BW+1.2,FH*13.6,.4,0xff4a4a,.02,{emissive:0xd02a2a,emissiveIntensity:.8,transparent:true,opacity:0});bandHi.position.set(0,FH*6.2+FH*13.6/2,-1.5);BLD.add(bandHi);
// balcón del 5º (suelo en y=5*FH)
const BAL=new THREE.Group();BAL.position.set(0,5*FH,0);BLD.add(BAL);
const slab=box(12,.6,4.2,0xd8cbb4,.04);slab.position.set(0,-.3,0);slab.castShadow=true;BAL.add(slab);
const rail=box(12,.35,.35,0x2a2a30,.05,{metalness:.5,roughness:.4});rail.position.set(0,2.6,1.9);BAL.add(rail);
for(let i=0;i<13;i++){const b=box(.14,2.6,.14,0x2a2a30,.02);b.position.set(-6+i,1.3,1.9);BAL.add(b)}
[-6,6].forEach(x=>{const s=box(.35,2.6,4,0x2a2a30,.04);s.position.set(x,1.3,0);BAL.add(s)});
const plant=box(1.2,1.2,1.2,0xb0603a,.1);plant.position.set(-4.2,.6,-.8);BAL.add(plant);const pl2=box(1.6,1.4,1.6,0x4f9a3e,.4);pl2.position.set(-4.2,1.9,-.8);BAL.add(pl2);
// red de seguridad (CTA)
const NET=new THREE.Group();BAL.add(NET);{const m={color:0xffffff,transparent:true,opacity:.75,emissive:0xffffff,emissiveIntensity:.25};
 for(let i=0;i<=24;i++){const v=box(.05,5.4,.05,0xffffff,.01,m);v.position.set(-6+i*.5,2.7,2.05);NET.add(v)}
 for(let j=0;j<=10;j++){const h=box(12,.05,.05,0xffffff,.01,m);h.position.set(0,j*.54,2.05);NET.add(h)}}
NET.visible=false;
// ---------- gato de bloques
function cat(col=0xf08a2e,stripe=0xc8641a){const g=new THREE.Group();const B=new THREE.Group();g.add(B);
 const body=box(1.0,1.0,1.7,col,.25);body.position.set(0,.95,0);B.add(body);
 for(let i=0;i<3;i++){const s=box(1.04,.16,.3,stripe,.03);s.position.set(0,1.42,-.4+i*.45);B.add(s)}
 const chest=box(.7,.6,.2,0xfff2e2,.08);chest.position.set(0,.85,.86);B.add(chest);
 const hd=new THREE.Group();hd.position.set(0,1.75,.85);B.add(hd);hd.add(box(1.1,.95,.95,col,.25));
 [-.32,.32].forEach(x=>{const e=new THREE.Mesh(new THREE.ConeGeometry(.2,.42,4),new THREE.MeshStandardMaterial({color:col,roughness:.6}));e.position.set(x,.62,-.05);e.rotation.y=Math.PI/4;hd.add(e);
  const ey=box(.2,.24,.06,0x2ad060,.04,{emissive:0x1a8a3a,emissiveIntensity:.4});ey.position.set(x*.85,.1,.48);hd.add(ey);const pu=box(.07,.2,.04,0x10131a,.01);pu.position.set(x*.85,.1,.52);hd.add(pu)});
 const ns=box(.16,.12,.08,0xff7aa8,.03);ns.position.set(0,-.12,.5);hd.add(ns);
 [-1,1].forEach(sg=>{for(let k=0;k<2;k++){const w=box(.7,.03,.03,0xffffff,.005);w.position.set(sg*.55,-.16-k*.1,.48);w.rotation.z=sg*(.12-k*.22);hd.add(w)}});
 const legs=[[-.32,.62],[.32,.62],[-.32,-.62],[.32,-.62]].map(([x,z])=>{const l=new THREE.Group();l.position.set(x,.55,z);const m=box(.32,.6,.32,col,.08);m.position.y=-.3;const p=box(.36,.16,.4,0xfff2e2,.05);p.position.set(0,-.55,.04);l.add(m,p);B.add(l);return l});
 const tail=new THREE.Group();tail.position.set(0,1.2,-.85);B.add(tail);const tl=[];let par=tail;for(let i=0;i<4;i++){const s=new THREE.Group();s.position.y=i?.38:0;const m=box(.22,.42,.22,i===3?stripe:col,.06);m.position.y=.2;s.add(m);par.add(s);tl.push(s);par=s}
 return{g,B,hd,legs,tail,tl,tick(t,{sway=1,curl=.25}={}){tail.rotation.x=-.9;tl.forEach((s,i)=>{s.rotation.x=curl+Math.sin(t*2.2-i*.7)*.18*sway;s.rotation.z=Math.sin(t*1.6-i*.6)*.25*sway})}}}
const C=cat();C.g.scale.setScalar(1.25);scene.add(C.g);
// ---------- sala del veterinario con 132 gatos (en otra zona del mundo)
const VET=new THREE.Group();VET.position.set(400,0,0);scene.add(VET);
{const fl=box(70,.4,60,0xdfe8ee,.02);fl.position.y=-.2;fl.receiveShadow=true;VET.add(fl);for(let i=0;i<14;i++){const l=box(70,.03,.12,0xc8d4dc,.01);l.position.set(0,.02,-28+i*4.3);VET.add(l)}
 const wall=box(70,30,.6,0xbfe0e8,.03);wall.position.set(0,15,-24);VET.add(wall);
 const cross=new THREE.Group();const a=box(6,1.8,.4,0x2ad060,.05,{emissive:0x18a048,emissiveIntensity:.7}),b=box(1.8,6,.4,0x2ad060,.05,{emissive:0x18a048,emissiveIntensity:.7});cross.add(a,b);cross.position.set(-22,21,-23.5);VET.add(cross)}
const NC=132,COLS=[0xf08a2e,0x3a3a42,0xf2f2ee,0x9a9aa6,0xd8b088,0x6a4a32];
const hb=new THREE.InstancedMesh(new THREE.BoxGeometry(1,1,1.7),new THREE.MeshStandardMaterial({roughness:.6}),NC),hh=new THREE.InstancedMesh(new THREE.BoxGeometry(1.1,.95,.95),new THREE.MeshStandardMaterial({roughness:.6}),NC),
 he=new THREE.InstancedMesh(new THREE.ConeGeometry(.2,.42,4),new THREE.MeshStandardMaterial({roughness:.6}),NC*2),bnd=new THREE.InstancedMesh(new THREE.BoxGeometry(1.16,1.1,.55),new THREE.MeshStandardMaterial({color:0xffffff,roughness:.5,emissive:0xffffff,emissiveIntensity:.15}),NC),
 tk=new THREE.InstancedMesh(new THREE.BoxGeometry(.5,.5,.12),new THREE.MeshBasicMaterial({color:0x4ade80,toneMapped:false}),NC);
[hb,hh,he,bnd,tk].forEach(m=>{m.frustumCulled=false;m.castShadow=true;VET.add(m)});
const CAT=[];for(let i=0;i<NC;i++){const cx=i%12,cz=Math.floor(i/12);CAT.push({x:-24.2+cx*4.4+(R()-.5)*.6,z:-19+cz*3.6+(R()-.5)*.5,col:COLS[Math.floor(R()*COLS.length)],ry:(R()-.5)*.5,ph:R()*6,band:R()<.55,lost:false})}
{const idx=[...Array(NC).keys()].sort((a,b)=>((a*37)%NC)-((b*37)%NC));idx.slice(0,13).forEach(i=>CAT[i].lost=true)} // 13 de 132 ≈ 1 de cada 10
console.assert(CAT.filter(c=>c.lost).length===13);
const O=new THREE.Object3D(),CC=new THREE.Color();
function herd(t,{show=1,bandOn=0,tickOn=0,gray=0}){CAT.forEach((c,i)=>{const s=ss(i/NC*.8,i/NC*.8+.2,show)*1.2;const bob=Math.abs(Math.sin(t*3+c.ph))*.06;
  O.position.set(c.x,.95*s+bob,c.z);O.rotation.set(0,c.ry,0);O.scale.setScalar(s);O.updateMatrix();hb.setMatrixAt(i,O.matrix);
  O.position.set(c.x+Math.sin(c.ry)*1.0*s,1.75*s+bob,c.z+Math.cos(c.ry)*1.0*s);O.rotation.set(Math.sin(t*1.3+c.ph)*.1,c.ry+Math.sin(t*.9+c.ph)*.3,0);O.updateMatrix();hh.setMatrixAt(i,O.matrix);
  for(let k=0;k<2;k++){const ex=new THREE.Vector3(k?.32:-.32,.62,-.05).multiplyScalar(s).applyEuler(O.rotation);O.position.set(c.x+Math.sin(c.ry)*1.0*s+ex.x,1.75*s+bob+ex.y,c.z+Math.cos(c.ry)*1.0*s+ex.z);O.updateMatrix();he.setMatrixAt(i*2+k,O.matrix)}
  const bs=c.band&&!c.lost?ss(i/NC*.6,i/NC*.6+.4,bandOn)*s:0;O.position.set(c.x+Math.sin(c.ry)*.35*s,.95*s+bob,c.z+Math.cos(c.ry)*.35*s);O.rotation.set(0,c.ry,0);O.scale.set(bs,bs,bs);O.updateMatrix();bnd.setMatrixAt(i,O.matrix);
  const ts=!c.lost?ss(i/NC*.6,i/NC*.6+.4,tickOn)*s:0;O.position.set(c.x,3.2*s+bob,c.z);O.rotation.set(0,0,Math.PI/4);O.scale.set(ts,ts*.35,ts);O.updateMatrix();tk.setMatrixAt(i,O.matrix);O.scale.setScalar(1);
  CC.setHex(c.col);if(c.lost&&gray>0)CC.lerp(new THREE.Color(0x30333c),gray*.85);hb.setColorAt(i,CC);hh.setColorAt(i,CC);he.setColorAt(i*2,CC);he.setColorAt(i*2+1,CC)});
 [hb,hh,he,bnd,tk].forEach(m=>{m.instanceMatrix.needsUpdate=true;if(m.instanceColor)m.instanceColor.needsUpdate=true})}
const VETC=capataz();VETC.g.scale.setScalar(1.3);VETC.g.position.set(400+22,0,-10);scene.add(VETC.g);
const coat=box(1.6,1.6,1.0,0xffffff,.1);coat.position.y=1.6;VETC.g.add(coat);
// ---------- partículas: viento de la caída y polvo al aterrizar
const WIND=puffs(scene,40,.12,0xffffff,{opacity:.8}),DUST=puffs(scene,30,.35,0xd8cbb4,{opacity:.85});
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],k=ss(0,d,lt),m=mouthAt(t);
 C.tick(t);C.B.rotation.set(0,0,0);C.hd.rotation.set(Math.sin(t*1.1)*.08,Math.sin(t*.7)*.3,0);C.legs.forEach(l=>l.rotation.set(0,0,0));
 scene.fog.far=260;NET.visible=false;bandLow.material.opacity=0;bandHi.material.opacity=0;for(let i=0;i<40;i++)WIND.set(i,0,-99,0,0);for(let i=0;i<30;i++)DUST.set(i,0,-99,0,0);
 VETC.pose(t,0,{});let p,q;const yB=5*FH;
 if(s==='h'||s==='cta'){// gato sentado en la barandilla del 5º, mirando abajo
  NET.visible=s==='cta';C.g.position.set(1.2,yB+(s==='cta'?.05:2.78),s==='cta'?.4:1.9);C.g.rotation.set(0,s==='cta'?.5:-.25,0);C.hd.rotation.x=s==='cta'?0:.45;
  if(s==='cta'){C.g.position.y=yB;C.tick(t,{sway:1.6,curl:.4})}
  p=V3(9-k*2,yB+(s==='cta'?4.2:5.6),22-k*3);q=V3(.6,yB+(s==='cta'?.7:4.3),.6)}
 else if(s==='s1'){// resbala y cae boca arriba; se endereza en el aire; aterriza
  const fall=ss(.15,d-.9,lt),y=yB+2.78-(yB+2.78-.6)*fall*fall*(3-2*fall)*.0+(-(yB+2.18))*fall;const yy=Math.max(.6,yB+2.78-(yB+2.18)*fall);
  const roll=Math.PI*(1-ss(.25,.7,fall));C.g.position.set(1.2,yy,1.9+fall*2.2);C.g.rotation.set(0,-.25,0);C.B.rotation.z=roll;C.hd.rotation.x=-.4*(1-ss(.1,.4,fall));
  C.legs.forEach((l,i)=>l.rotation.x=(i<2?-1:1)*(.6*(1-fall)+.25*Math.sin(t*9+i)));C.tick(t,{sway:2.5,curl:.6});
  if(fall>0&&fall<.98)for(let i=0;i<40;i++){const ph=(t*2.2+i/40)%1;WIND.set(i,1.2+Math.sin(i*2.3)*1.6,yy-1+ph*6,1.9+fall*2.2+Math.cos(i*1.7)*1.4,(1-ph)*1.2)}
  const land=ss(d-.9,d-.5,lt);if(land>0){C.g.scale.set(1.25*(1+.18*Math.sin(land*Math.PI)),1.25*(1-.25*Math.sin(land*Math.PI)),1.25);for(let i=0;i<30;i++){const a=i*.21,rr=land*3.2*(.6+(i%5)*.12);DUST.set(i,1.2+Math.cos(a)*rr,.7+Math.sin(land*3.14)*(.4+(i%3)*.3),4.1+Math.sin(a)*rr,(1-land)*1.3+.2)}}else C.g.scale.setScalar(1.25);
  p=V3(10,yy+4.5+ (1-fall)*1.5,24);q=V3(1.2,yy+.6,2)}
 else if(s==='s2'||s==='s3'){// sala del veterinario: aparecen los 132; en s3, vendas, ✓ verdes y 13 en gris
  C.g.position.set(0,-99,0);herd(t,{show:s==='s2'?ss(.3,d*.7,lt):1,bandOn:s==='s3'?ss(.5,2.8,lt):0,tickOn:s==='s3'?ss(1.0,3.2,lt):0,gray:s==='s3'?ss(1.0,3.2,lt):0});
  VETC.g.position.set(400+22-k*6,0,-10+k*4);VETC.pose(t,m,{walk:t*5,look:-.6});
  if(s==='s2'){p=V3(400+4-k*4,19-k*3,44-k*6);q=V3(400,2.5,-8)}else{p=V3(400-8+k*10,13,26-k*4);q=V3(400-2+k*6,1.6,-8)}}
 else if(s==='s4'){// edificio de 20 pisos: los pisos bajos (verde) llegan al hospital; los de arriba (rojo) casi nunca
  C.g.position.set(0,-99,0);scene.fog.far=900;bandLow.material.opacity=.62*ss(.6,1.6,lt);bandHi.material.opacity=.62*ss(2.6,3.6,lt);
  p=V3(30-k*10,22+k*58,150+k*40);q=V3(0,30+k*34,-5)}
 cam.position.copy(p);cam.lookAt(q);WIND.done();DUST.done();r.render(scene,cam)};
window.ready=true;
