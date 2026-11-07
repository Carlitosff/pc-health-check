// Mito de las zanahorias y la visión nocturna (1503). Reutilizable: cocina nocturna de la abuela, Londres de bloques con focos, caza nocturno con radar y ondas, ojo de vóxeles.
import {THREE,J,mk,ss,V3,clamp,stage,sun,box,glow,pixTex,capataz,abuela,segAt,mouthAt,puffs,label3d,plane,stars} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x0b1230,fog:[0x0b1230,40,160],exposure:1.15});const R=mk(1503);
const hemi=new THREE.HemisphereLight(0x6f86c8,0x1a1420,.9);scene.add(hemi);const S=sun(scene,{pos:[-14,26,14],color:0xbcd0ff,power:1.4,span:20});
const NIGHT=new THREE.Color(0x0b1230);
stars(scene,1400,{size:.6});
const carrot=(s=1)=>{const g=new THREE.Group();for(let i=0;i<6;i++){const b=box((1.1-i*.16)*s,.8*s,(1.1-i*.16)*s,i%2?0xff7a1a:0xf26a10,.12*s);b.position.y=-i*.75*s;g.add(b)}[-.25,0,.25].forEach((x,k)=>{const l=box(.18*s,1.2*s,.18*s,0x3fae3a,.05*s);l.position.set(x*s,.9*s,0);l.rotation.z=(k-1)*.35;g.add(l)});g.traverse(o=>{if(o.isMesh)o.castShadow=true});return g};
// ---------- cocina de la abuela (gancho y CTA)
const K0=new THREE.Group();scene.add(K0);
const fl=new THREE.Mesh(new THREE.PlaneGeometry(60,60),new THREE.MeshStandardMaterial({map:pixTex(64,64,(g,w,h)=>{for(let y=0;y<8;y++)for(let x=0;x<8;x++){g.fillStyle=(x+y)%2?'#e9e1cf':'#8a3a2e';g.fillRect(x*8,y*8,8,8)}},[12,12]),roughness:.85}));fl.rotation.x=-Math.PI/2;fl.receiveShadow=true;K0.add(fl);
const wall=box(40,16,1,0xe8cfa0,.05);wall.position.set(0,8,-7);K0.add(wall);const wnd=box(8,6,.2,0x0b1640,.04,{emissive:0x10205a,emissiveIntensity:.6});wnd.position.set(6,8.5,-6.4);K0.add(wnd);const moon=glow(0xfff2c0,3,.9);moon.position.set(7.5,10,-6.2);K0.add(moon);
[[-.1,0],[0,-.1]].forEach(([a,b],i)=>{const f=box(i?8.4:.3,i?.3:6.4,.3,0xf4f0e6,.02);f.position.set(6,8.5,-6.2);K0.add(f)});
const table=box(8,.4,4.6,0x8a5a32,.06);table.position.set(0,2.6,0);K0.add(table);[[-3.6,-2],[3.6,-2],[-3.6,2],[3.6,2]].forEach(([x,z])=>{const l=box(.4,2.6,.4,0x6b4426,.04);l.position.set(x,1.3,z);K0.add(l)});
const bowl=box(2.4,.8,2.4,0x3f6fd0,.3);bowl.position.set(-1.6,3.2,.2);K0.add(bowl);for(let i=0;i<5;i++){const c=carrot(.38);c.position.set(-2.2+i*.3,3.9+(i%2)*.2,0+(i%3)*.3);c.rotation.z=1.3+i*.2;K0.add(c)}
const lamp=new THREE.PointLight(0xffb060,40,30,1.6);lamp.position.set(0,9,2);K0.add(lamp);const lg=glow(0xffc070,4,.6);lg.position.set(0,9.3,2);K0.add(lg);const sh=box(1.6,.8,1.6,0xc8a040,.2,{emissive:0xffa030,emissiveIntensity:.8});sh.position.set(0,9.6,2);K0.add(sh);
const ab=abuela();ab.g.position.set(-2.5,0,2.8);ab.g.rotation.y=.6;scene.add(ab.g);const BC=carrot(.5);ab.armR.add(BC);BC.position.set(0,-1.7,.4);BC.rotation.x=1.4;
const cap=capataz();cap.g.position.set(2.4,0,2.8);cap.g.rotation.y=-.6;scene.add(cap.g);
const eyeG=[-.34,.34].map(x=>{const g=glow(0x7dff6a,1.1,.0);g.position.set(x,.14,.8);cap.head.add(g);return g});
const myth=label3d(['¿VISTA','*NOCTURNA?'],{w:4.2,h:2,px:150,accent:'#ff7a1a'});myth.position.set(3.6,8.6,0);K0.add(myth);
// ---------- Londres de noche con focos y bombarderos
const LON=new THREE.Group();LON.position.set(400,0,0);scene.add(LON);
const lg2=new THREE.Mesh(new THREE.PlaneGeometry(400,400),new THREE.MeshStandardMaterial({color:0x15182a,roughness:1}));lg2.rotation.x=-Math.PI/2;LON.add(lg2);
for(let i=0;i<70;i++){const w=3+R()*5,h=4+R()*16;const b=box(w,h,w,[0x2a2c3e,0x34323f,0x262838][i%3],.08);b.position.set((R()-.5)*120,h/2,-10-R()*80);LON.add(b);for(let y=1.5;y<h-1;y+=2.4)if(R()<.5){const wi=box(.7,.9,.1,0xffd070,.02,{emissive:0xffb040,emissiveIntensity:1.2});wi.position.set(b.position.x+(R()-.5)*(w-1),y,b.position.z+w/2+.06);LON.add(wi)}}
const lmoon=glow(0xfff2c0,30,.9);lmoon.position.set(-30,70,-120);LON.add(lmoon);const lamb=new THREE.PointLight(0x9fb4ff,300,200,1.2);lamb.position.set(0,40,20);LON.add(lamb);
const tower=new THREE.Group();{const b=box(4,30,4,0x6a5a3e,.1);b.position.y=15;tower.add(b);const cl=box(4.4,4.4,4.4,0x7a6a48,.1);cl.position.y=24;tower.add(cl);[1,-1].forEach(s=>{const f=box(3,3,.1,0xfff2c0,.2,{emissive:0xffe090,emissiveIntensity:1.4});f.position.set(0,24,s*2.25);tower.add(f)});const sp=box(2.4,6,2.4,0x5a4a30,.1);sp.position.y=29;tower.add(sp)}tower.position.set(14,0,-34);LON.add(tower);
const beams=[];for(let i=0;i<5;i++){const m=new THREE.Mesh(new THREE.CylinderGeometry(.3,3.6,110,16,1,true),new THREE.MeshBasicMaterial({color:0xdfeaff,transparent:true,opacity:.3,depthWrite:false,blending:THREE.AdditiveBlending,side:THREE.DoubleSide}));m.geometry.translate(0,45,0);m.position.set(-40+i*20,0,-40);LON.add(m);beams.push(m)}
const bombers=[];for(let i=0;i<4;i++){const p=plane({body:0x4a4a52,wing:0x3e3e46,accent:0x3e3e46});p.g.scale.setScalar(2.2);LON.add(p.g);bombers.push(p)}
// ---------- caza nocturno con radar
const AIR=new THREE.Group();AIR.position.set(800,0,0);scene.add(AIR);
const clouds=[];for(let i=0;i<26;i++){const g=new THREE.Group();for(let k=0;k<4;k++){const b=new THREE.Mesh(new THREE.BoxGeometry(4+R()*5,1.4+R()*1.6,3+R()*3),new THREE.MeshStandardMaterial({color:0x5a6688,roughness:1,transparent:true,opacity:.85}));b.position.set(k*3-6,R(),R()*2);g.add(b)}g.position.set((R()<.5?-1:1)*(12+R()*30),-6+R()*14,-20-R()*120);AIR.add(g);clouds.push(g)}
const ft=plane({body:0x1c1c22,wing:0x16161b,accent:0xd8d0b8});AIR.add(ft.g);
const pil=capataz();pil.hat.forEach(h=>h.visible=false);{const hl=box(1.6,.55,1.45,0x5a3a20,.2);hl.position.y=.62;pil.head.add(hl);[-.34,.34].forEach(x=>{const gg=box(.42,.3,.12,0x9fd8ff,.06,{metalness:.5,roughness:.2});gg.position.set(x,.2,.7);pil.head.add(gg)})}pil.g.scale.setScalar(.32);pil.g.position.set(0,.2,.6);ft.g.add(pil.g);
const ant=new THREE.Group();[[0,.5],[0,-.5],[.5,0],[-.5,0]].forEach(([x,y])=>{const a=box(.06,.06,1.4,0xd8d8e0,.01);a.position.set(x,y,4.2);ant.add(a)});ft.g.add(ant);
const waves=[];for(let i=0;i<5;i++){const m=new THREE.Mesh(new THREE.TorusGeometry(1,.06,6,48),new THREE.MeshBasicMaterial({color:0x6aff8a,transparent:true,opacity:.8,toneMapped:false}));AIR.add(m);waves.push(m)}
const enemy=plane({body:0x3a3a40,wing:0x2e2e34,accent:0x2e2e34});enemy.g.scale.setScalar(1.6);AIR.add(enemy.g);const eGlow=glow(0x6aff8a,7,.0);AIR.add(eGlow);
const crate=new THREE.Group();{const c=box(4,2,3,0x9a6a3a,.08);crate.add(c);for(let i=0;i<6;i++){const k=carrot(.3);k.position.set(-1.5+i*.6,1.4,0);k.rotation.z=1.57;crate.add(k)}}AIR.add(crate);
const vs=label3d(['ZANAHORIAS','*vs RADAR'],{w:5,h:2.2,px:150,sprite:true});AIR.add(vs);
// ---------- ojo de vóxeles (vitamina A)
const EYE=new THREE.Group();EYE.position.set(1200,0,0);scene.add(EYE);
const VO=[];const vs_=.32;for(let x=-4;x<=4;x+=vs_)for(let y=-4;y<=4;y+=vs_)for(let z=-4;z<=4;z+=vs_){const d=Math.hypot(x,y,z);if(d<4&&d>3.5)VO.push([x,y,z])}
const eim=new THREE.InstancedMesh(new THREE.BoxGeometry(vs_*.94,vs_*.94,vs_*.94),new THREE.MeshStandardMaterial({roughness:.5}),VO.length);eim.frustumCulled=false;EYE.add(eim);{const O=new THREE.Object3D(),C=new THREE.Color();VO.forEach(([x,y,z],i)=>{O.position.set(x,y,z);O.updateMatrix();eim.setMatrixAt(i,O.matrix);const rr=Math.hypot(x,y);C.setHex(z>3&&rr<.9?0x080808:z>2.7&&rr<2?0x2f8ad8:0xf4f0ea);if(z<=2.7&&rr<2.5&&z>0&&R()<.04)C.setHex(0xd84040);eim.setColorAt(i,C)})}
const meter=new THREE.Group();EYE.add(meter);meter.position.set(0,-6.2,0);const mb=box(10,1,1,0x20263a,.2);meter.add(mb);const mf=box(1,.8,1.05,0x6aff8a,.2,{emissive:0x2aa04a,emissiveIntensity:.6});meter.add(mf);
const vA=label3d(['VITAMINA A'],{w:6,h:1.4,px:150,accent:'#ff7a1a'});vA.position.set(0,6.2,0);vA.visible=false;EYE.add(vA);const mlab=label3d(['VITAMINA A','*VISIÓN NOCTURNA'],{w:7,h:2,px:110,bg:null});mlab.position.set(0,-4.6,1);EYE.add(mlab);
const eC=[];for(let i=0;i<8;i++){const c=carrot(.35);EYE.add(c);eC.push(c)}
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],m=mouthAt(t);let p,q;
 const onK=s==='h'||s==='cta';K0.visible=onK;ab.g.visible=onK;cap.g.visible=onK;LON.visible=s==='s1';AIR.visible=s==='s2'||s==='s3';EYE.visible=s==='s4';
 if(s==='h'){const k=ss(0,d,lt);ab.pose(t,m*.5,{point:.7,look:.5});cap.pose(t,0,{look:-.4});eyeG.forEach(g=>g.material.opacity=.55+.3*Math.sin(t*5));myth.visible=false;BC.visible=true;p=V3(-.4+k*.8,6.4,25-k*3);q=V3(0,3.3,1.5)}
 else if(s==='cta'){ab.pose(t,0,{wave:1,look:.5});cap.pose(t,m,{look:.2});cap.armL.rotation.x=-1.2;eyeG.forEach(g=>g.material.opacity=0);myth.visible=false;BC.visible=true;const k=ss(0,d,lt);p=V3(0,7.5+k,30+k*2);q=V3(0,3.4,1.5)}
 else if(s==='s1'){const k=ss(0,d,lt);beams.forEach((b,i)=>{b.rotation.z=Math.sin(t*.5+i*1.7)*.5;b.rotation.x=-.25+Math.cos(t*.4+i)*.2});bombers.forEach((b,i)=>{b.g.position.set(-40+((t*7+i*22)%80),17+i*3,-24-i*6);b.g.rotation.set(0,Math.PI/2,0);b.prop.rotation.z=t*40});p=V3(400+k*4,4,62-k*10);q=V3(405,15,-30)}
 else if(s==='s2'||s==='s3'){const sec=s==='s3';const k=ss(0,d,lt);ft.g.position.set(Math.sin(t*.6)*1.2,Math.sin(t*.9)*.6,0);ft.g.rotation.set(Math.sin(t*.7)*.04,0,Math.sin(t*.6)*.18);ft.prop.rotation.z=t*45;pil.pose(t,0,{look:.1});
  clouds.forEach((c,i)=>{c.position.z=((-20-((i*37)%120))+t*24)%140-130;});
  waves.forEach(w=>w.visible=sec);crate.visible=false;vs.visible=false;enemy.g.visible=sec;eGlow.visible=sec;
  if(sec){waves.forEach((w,i)=>{const u=((t*.8+i/5)%1);w.position.set(ft.g.position.x,ft.g.position.y,4.6+u*40);w.scale.setScalar(1+u*9);w.material.opacity=.85*(1-u)});enemy.g.position.set(4,3,-46+lt*3);enemy.g.position.z=48-lt*1.5;enemy.prop.rotation.z=t*40;enemy.g.rotation.y=Math.PI;eGlow.position.copy(enemy.g.position);eGlow.material.opacity=lt>d*.45?.7+.2*Math.sin(t*8):0;crate.position.set(-6,3.6,12);crate.rotation.y=t*.6;vs.position.set(-6,7,12)}
  if(!sec){p=V3(806-k*3,3.2,-14+k*3);q=V3(800,.4,1)}else{const u=ss(d*.4,d*.6,lt);p=V3(791+u*7,4.2+u*2,-12-u*4);q=V3(lerpN(796,802,u),1.5,lerpN(4,30,u))}}
 else if(s==='s4'){const k=ss(0,d,lt);EYE.rotation.y=Math.sin(t*.5)*.35-.2;const fill=lt<d*.45?ss(0,d*.4,lt)*.85:.85+.0*Math.sin(t);const extra=lt>d*.55;mf.scale.x=Math.max(.05,fill*10);mf.position.x=-5+fill*5;
  eC.forEach((c,i)=>{const u=extra?clamp((lt-d*.55-i*.12)/.8):0;c.visible=extra;c.position.set(-6+i*1.7,9-u*9.5,4.6);c.rotation.z=t*2+i});mlab.set(extra?['MÁS ZANAHORIA','*= IGUAL']:['VITAMINA A','*VISIÓN NOCTURNA']);p=V3(Math.sin(t*.3)*2,1.6,33-k*3);q=V3(0,1.6,0);p.add(EYE.position);q.add(EYE.position)}
 scene.background=NIGHT;
 if(q){S.target.position.copy(q);S.position.set(q.x-14,q.y+24,q.z+14);S.target.updateMatrixWorld()}
 cam.position.copy(p);cam.lookAt(q);r.render(scene,cam)};
function lerpN(a,b,u){return a+(b-a)*u}
window.ready=true;
