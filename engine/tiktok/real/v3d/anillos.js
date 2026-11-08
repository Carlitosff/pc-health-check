// ¿Y si la Tierra tuviera anillos? (1604). Serie ¿QUÉ PASARÍA SI…? Parte 5. Reutilizable: ringSystem() (bloques.js v19) en el globo y arco de anillos en el cielo de la plaza.
import {THREE,J,mk,ss,V3,clamp,stage,sun,box,glow,pixTex,capataz,segAt,mouthAt,label3d,stars,voxGlobe,snow,ringSystem,skyArch} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x7fb8ff,fog:[0xb8d4ff,80,260],exposure:1.08});const R=mk(1604);
const hemi=new THREE.HemisphereLight(0xdcefff,0x6a7a5a,1.3);scene.add(hemi);const S=sun(scene,{pos:[-14,30,18],span:30});
// ---------------- PLAZA (vista hacia el sur)
const st=new THREE.Group();scene.add(st);
const grass=pixTex(128,128,(g,w,h)=>{const q=mk(8);g.fillStyle='#6fb24e';g.fillRect(0,0,w,h);for(let i=0;i<700;i++){g.fillStyle=['#62a544','#7dbd58','#568f3c'][Math.floor(q()*3)];g.fillRect(Math.floor(q()*w/4)*4,Math.floor(q()*h/4)*4,4,4)}},[50,50]);
const gmat=new THREE.MeshStandardMaterial({map:grass,roughness:1});const gnd=new THREE.Mesh(new THREE.PlaneGeometry(500,500),gmat);gnd.rotation.x=-Math.PI/2;gnd.receiveShadow=true;st.add(gnd);
const COLS=[0xd9c7a8,0xc2573f,0x8fa6b8,0xe8dfca,0xa86a48,0x6f86a8];const wins=[];
[[-17,-26,8,10],[-7,-30,9,14],[5,-28,8,9],[16,-27,9,12],[-28,-22,7,8],[28,-22,7,10]].forEach(([x,z,w,h],i)=>{const b=box(w,h,7,COLS[i%6],.15);b.position.set(x,h/2,z);st.add(b);for(let y=1.5;y<h-1;y+=2.2)for(let a=-w/2+1.3;a<w/2-.8;a+=1.8){const lit=R()<.55;const wi=box(.9,1.2,.1,0x2a3a58,.02,{emissive:0xffc050,emissiveIntensity:0});wi.position.set(x+a,y,z+3.52);wi.userData.lit=lit;st.add(wi);wins.push(wi)}});
const hero=capataz();hero.g.position.set(-1.6,0,-4);hero.g.scale.setScalar(.85);scene.add(hero.g);
const lamp=new THREE.Group();{const p=box(.3,6,.3,0x2a2a33,.05);p.position.y=3;const h=box(1.1,.5,1.1,0xfff2c0,.1,{emissive:0xffd070,emissiveIntensity:0});h.position.y=6.1;lamp.add(p,h);lamp.userData.h=h}lamp.position.set(-5,0,-3);st.add(lamp);
// el arco de anillos en el cielo del sur
const ARC=skyArch({r:560,w:120,center:[40,-210,-520],tilt:-.38});scene.add(ARC.g);
const SN=snow(scene,700,[-30,30,26,-30,12],{size:.3,speed:2});SN.pts.visible=false;
const STARS=stars(scene,1400,{r0:300,r1:380,size:1.4});STARS.material.fog=false;
// ---------------- ESPACIO
const SP=new THREE.Group();SP.position.set(0,0,-2000);scene.add(SP);
const G1=voxGlobe(9000,10);SP.add(G1.group);G1.group.rotation.z=-.41;// eje inclinado 23,4°
const RS=ringSystem({r0:13,r1:23});G1.group.add(RS.g);
const LAT=40.4*Math.PI/180;const pin=new THREE.Group();const pinB=box(.6,.6,.6,0xffd23a,.1,{emissive:0xffa000,emissiveIntensity:1});pinB.position.y=10.6;pin.add(pinB);const pg=glow(0xffd23a,3.5,.9);pg.position.y=10.7;pin.add(pg);pin.rotation.z=-(Math.PI/2-LAT);pin.rotation.y=.4;G1.group.add(pin);
// sombra de los anillos en el hemisferio de invierno (banda oscura que se desliza)
const SH=new THREE.Mesh(new THREE.SphereGeometry(10.6,64,32,0,Math.PI*2,.3,.65),new THREE.MeshBasicMaterial({color:0x000006,transparent:true,opacity:0,depthWrite:false}));G1.group.add(SH);
const SUNG=glow(0xfff1c0,60,1);SUNG.position.set(-70,-38,-30);SP.add(SUNG);
const spL=new THREE.DirectionalLight(0xfff4e0,0);spL.position.set(-70,-38,-30);spL.target=G1.group;SP.add(spL);
const eqL=label3d(['*ECUADOR'],{w:7,h:2,px:140,sprite:true});SP.add(eqL);
// Tierra antigua (hace 466 M años) con el anillo y los 21 cráteres en ±30°
const G2=voxGlobe(9000,10,{seed:2.7});const AN=new THREE.Group();AN.position.set(0,0,-3000);scene.add(AN);AN.add(G2.group);
const RS2=ringSystem({r0:12.5,r1:17,op:.6,seed:9});G2.group.add(RS2.g);
const bandM=new THREE.MeshBasicMaterial({color:0xff4d6d,transparent:true,opacity:.75,side:THREE.DoubleSide,toneMapped:false});[-1,1].forEach(s=>{const b=new THREE.Mesh(new THREE.TorusGeometry(10.55*Math.cos(Math.PI/6),.09,6,96),bandM);b.rotation.x=Math.PI/2;b.position.y=s*10.55*Math.sin(Math.PI/6);G2.group.add(b)});
const CR=[];const q=mk(466);for(let i=0;i<21;i++){const la=(q()*2-1)*.5,lo=q()*6.283;const c=new THREE.Group();const dir=V3(Math.cos(la)*Math.cos(lo),Math.sin(la),Math.cos(la)*Math.sin(lo));const m=box(.8,.8,.35,0xff2d3f,.08,{emissive:0xff2020,emissiveIntensity:1.2});m.position.copy(dir).multiplyScalar(10.35);m.lookAt(0,0,0);const gw=glow(0xff4040,2.6,.85);gw.position.copy(dir).multiplyScalar(10.8);c.add(m,gw);G2.group.add(c);CR.push(c)}
stars(SP,1500,{r0:150,r1:220,size:1.1});stars(AN,1500,{r0:150,r1:220,size:1.1,seed:4});
cam.far=3000;cam.updateProjectionMatrix();
const crL=label3d(['*21 CRÁTERES','CERCA DEL ECUADOR'],{w:9,h:3.2,px:120,sprite:true});AN.add(crL);
const p6=label3d(['PARTE 6','*LA LUNA'],{w:5,h:2.2,px:150,sprite:true});scene.add(p6);
const moon=new THREE.Mesh(new THREE.SphereGeometry(40,48,32),new THREE.MeshStandardMaterial({color:0xcfcfd6,roughness:1,emissive:0x50505a,emissiveIntensity:.6,fog:false}));moon.position.set(140,160,-700);scene.add(moon);
const DAY=new THREE.Color(0x7fb8ff),NIGHT=new THREE.Color(0x070b22),WINTER=new THREE.Color(0xa9b4c4),SPACE=new THREE.Color(0x02030a),DUSK=new THREE.Color(0x6f8fd8);
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],m=mouthAt(t);let p,q,bg;
 const inSpace=s==='s1'||s==='s3';const inOld=s==='s4';const onPlaza=!inSpace&&!inOld;
 st.visible=ARC.g.visible=onPlaza;hero.g.visible=onPlaza&&s!=='cta';SP.visible=inSpace;AN.visible=inOld;STARS.visible=!onPlaza||s==='s2';
 const night=s==='s2'?ss(0,.8,lt):0;
 moon.visible=s==='cta';p6.visible=s==='cta'&&lt>.6;SN.pts.visible=false;
 if(onPlaza){bg=s==='s2'?DUSK.clone().lerp(NIGHT,night):s==='cta'?DAY:DAY.clone().lerp(DUSK,.25+.1*Math.sin(t*.3));
  ARC.draw(t,{night,gap:s==='s2'?ss(.6,1.6,lt):0});
  wins.forEach(w=>{w.material.emissiveIntensity=w.userData.lit?night*1.4:0});lamp.userData.h.material.emissiveIntensity=night*2;
  hemi.intensity=1.3-night*.9;S.intensity=2.6-night*2.2;
  hero.pose(t,m,{look:s==='cta'?0:Math.sin(t*.5)*.25,wave:s==='cta'?1:0,point:s==='h'||s==='s2'?.8:0});hero.g.rotation.y=Math.PI*.85;
  hero.head.rotation.x=-.45;
  if(s==='h'){const e=ss(0,d,lt);p=V3(2.5-e*1,1.6+e*.4,17-e*1.5);q=V3(0,13+e*3,-30)}
  else if(s==='s2'){const e=ss(0,d,lt);p=V3(1+e*2,1.6,17);q=V3(2,13+e*3,-30)}
  else{const e=ss(0,d,lt);p=V3(2.5+Math.sin(t*.5)*.4,1.6,17.5-e*1);q=V3(0,15+e*2,-30);p6.position.set(4,15,-14);moon.position.set(-60+e*10,120-e*10,-420+e*90)}
  S.target.position.set(q.x,0,q.z*0);S.target.updateMatrixWorld();S.position.set(-14,30,18)}
 else if(inSpace){bg=SPACE;hemi.intensity=.12;S.intensity=0;G1.group.rotation.y=t*.18;
  if(s==='s1'){spL.intensity=2.4;spL.position.set(-50,20,40);SH.material.opacity=0;eqL.visible=lt>1;eqL.position.set(0,-17,10);const e=ss(0,d,lt);p=V3(-24+e*12,40-e*8,48-e*4);q=V3(0,-2,0)}
  else{spL.intensity=2.8;spL.position.set(-60,-36,26);SH.material.opacity=.62*ss(.6,1.8,lt);eqL.visible=false;const e=ss(0,d,lt);p=V3(-18+e*8,6-e*2,50-e*6);q=V3(-4,-3,0);SUNG.position.set(-40,-30,-20)}
  p.add(SP.position);q.add(SP.position)}
 else{bg=SPACE;hemi.intensity=.35;S.intensity=0;spL.intensity=0;G2.group.rotation.y=t*.22;G2.group.rotation.z=-.15;
  const shown=Math.floor(clamp((lt-.6)/(d*.6))*21);CR.forEach((c,i)=>{c.visible=i<shown;const age=(lt-.6)-i*(d*.6/21);c.children[1].scale.setScalar(2.6*(age>0&&age<.4?1+1.6*(1-age/.4):1))});
  crL.visible=false;crL.position.set(0,-15,8);const e=ss(0,d,lt);p=V3(20-e*8,8,40-e*6);q=V3(0,-1.5,0);p.add(AN.position);q.add(AN.position);crL.position.add(AN.position)}
 scene.background=bg;scene.fog.near=onPlaza?80:1e5;scene.fog.far=onPlaza?260:2e5;scene.fog.color.copy(bg);
 cam.position.copy(p);cam.lookAt(q);r.render(scene,cam)};
window.ready=true;
