// Mito: 'un rayo nunca cae dos veces en el mismo sitio' (1803). Reutilizable: tormenta nocturna (lluvia determinista, relámpagos con rama y destello que ilumina
// toda la escena), torre de bloques con pararrayos, bosque de bloques y GUARDABOSQUES (personaje propio nº 2 de la cuenta: sombrero de ala, uniforme caqui).
import {THREE,J,mk,ss,V3,clamp,stage,sun,box,glow,rig,capataz,segAt,mouthAt,label3d,puffs} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x0b1226,fog:[0x0b1226,40,170],exposure:1.1});const R=mk(1803);
const hemi=new THREE.HemisphereLight(0x8aa0d8,0x1a1a2a,.55);scene.add(hemi);const S=sun(scene,{pos:[-20,40,25],span:40,color:0xbfd0ff,power:.5});
const flashL=new THREE.PointLight(0xdfe8ff,0,0,0);scene.add(flashL);
const NIGHT=new THREE.Color(0x0b1226),FLASH=new THREE.Color(0x8fa0d8);
// ---------- ciudad con torre
const city=new THREE.Group();scene.add(city);
const street=new THREE.Mesh(new THREE.PlaneGeometry(400,400),new THREE.MeshStandardMaterial({color:0x1c2030,roughness:.35,metalness:.2}));street.rotation.x=-Math.PI/2;street.receiveShadow=true;city.add(street);
function tower(){const g=new THREE.Group();const C=0x8a8f9e;[[8,10],[6.4,6],[4.8,4],[3.2,2.4]].reduce((y,[w,h])=>{const b=box(w,h,w,C,.1);b.position.y=y+h/2;g.add(b);for(let yy=y+.9;yy<y+h-.5;yy+=1.1)for(let x=-w/2+.7;x<w/2-.4;x+=.9){const on=R()<.35;const wi=box(.5,.6,.08,on?0xffe2a0:0x1a2236,.02,on?{emissive:0xffc060,emissiveIntensity:.7}:{});wi.position.set(x,yy,w/2+.05);g.add(wi)}return y+h},0);
 const ant=box(.35,5,.35,0xb8bcc8,.05,{metalness:.6});ant.position.y=22.4+2.5;g.add(ant);const tip=glow(0xff3b30,2.2,.9);tip.position.y=27.5;g.add(tip);g.userData.tip=V3(0,27.2,0);g.userData.beacon=tip;return g}
const TW=tower();city.add(TW);
for(let i=0;i<14;i++){const x=(i%7-3)*7+(R()-.5)*2,z=-6-Math.floor(i/7)*9-R()*4;if(Math.abs(x)<5&&z>-12)continue;const h=4+R()*9;const b=box(5,h,5,[0x3a4258,0x4a3e58,0x2e4a58][i%3],.1);b.position.set(x,h/2,z);city.add(b);for(let yy=1;yy<h-.5;yy+=1.3)for(let xx=-1.6;xx<=1.6;xx+=1.1){if(R()<.4){const w=box(.5,.6,.08,0xffd890,.02,{emissive:0xffb050,emissiveIntensity:.6});w.position.set(x+xx,yy,z+2.55);city.add(w)}}}
const counter=label3d(['RAYOS: 0'],{w:8,h:2.4,px:130,accent:'#4de3ff'});counter.position.set(0,9.5,6);city.add(counter);
// casa y capataz para el consejo (s4)
const house=new THREE.Group();{const b=box(7,5,5,0xc8b89a,.1);b.position.y=2.5;house.add(b);const roof=box(7.6,.6,5.6,0x5a3a3a,.08);roof.position.y=5.3;house.add(roof);const door=box(1.6,2.8,.12,0x6a4024,.04);door.position.set(-1.4,1.4,2.56);house.add(door);house.userData.door=door;const lamp=glow(0xffd070,2.4,.0);lamp.position.set(-1.4,3.1,2.8);house.add(lamp);house.userData.lamp=lamp;
 const w=box(1.8,1.4,.1,0xffe2a0,.03,{emissive:0xffc060,emissiveIntensity:.8});w.position.set(1.6,2.6,2.56);house.add(w)}house.position.set(-14,0,14);city.add(house);const lampL=new THREE.PointLight(0xffd090,90,36,1.4);lampL.position.set(-19,6.5,22);city.add(lampL);{const pl=box(.25,6.4,.25,0x2a2a30,.03);pl.position.set(-19,3.2,21.5);city.add(pl);const lg=glow(0xffd090,2.6,.9);lg.position.set(-19,6.5,21.5);city.add(lg)}
const car=new THREE.Group();{const a=box(3.6,1,1.8,0xd8343e,.15);a.position.y=.8;const b=box(2,.8,1.6,0x1a2030,.1);b.position.y=1.65;car.add(a,b);[[-1.2,.8],[1.2,.8],[-1.2,-.8],[1.2,-.8]].forEach(([x,z])=>{const w=box(.7,.7,.3,0x101014,.06);w.position.set(x,.35,z);car.add(w)})}car.position.set(-7,0,17);city.add(car);
const hero=capataz();hero.g.position.set(-8,0,20);city.add(hero.g);
const umb=new THREE.Group();{const c=new THREE.Mesh(new THREE.ConeGeometry(1.9,.9,10,1,true),new THREE.MeshStandardMaterial({color:0x2a6be0,side:THREE.DoubleSide,roughness:.6}));c.position.y=.45;const st=box(.1,2.4,.1,0x222222,.02);st.position.y=-.8;umb.add(c,st)}umb.position.set(1,4.5,0);hero.g.add(umb);
// ---------- bosque y guardabosques (s3)
const FO=new THREE.Group();FO.position.set(300,0,0);scene.add(FO);
const grass=new THREE.Mesh(new THREE.PlaneGeometry(200,200),new THREE.MeshStandardMaterial({color:0x24402a,roughness:1}));grass.rotation.x=-Math.PI/2;grass.receiveShadow=true;FO.add(grass);
const Q=mk(33);for(let i=0;i<46;i++){const x=(Q()-.5)*60,z=-4-Q()*40;if(Math.abs(x)<4&&z>-8)continue;const h=3+Q()*4;const tr=box(.7,h,.7,0x4a3020,.05);tr.position.set(x,h/2,z);FO.add(tr);for(let k=0;k<3;k++){const s=2.8-k*.8;const l=box(s,1.1,s,[0x2f6a34,0x3a7a3a,0x26582c][k],.1);l.position.set(x,h+k*.9,z);FO.add(l)}}
const ranger=rig({skin:0xd9a06a,body:0x8a7a4a,legC:0x5a4e30,shoe:0x2a1e14});{const h=ranger.head;const brim=new THREE.Mesh(new THREE.CylinderGeometry(1.35,1.35,.1,20),new THREE.MeshStandardMaterial({color:0x6a5230,roughness:.8}));brim.position.y=.72;const crown=box(1.1,.6,1.1,0x6a5230,.15);crown.position.y=1.05;const band=box(1.14,.14,1.14,0x2a1e14,.03);band.position.y=.84;h.add(brim,crown,band);const badge=box(.36,.36,.06,0xffd23a,.05,{metalness:.6,emissive:0x664400});badge.position.set(-.4,1.95,.5);ranger.g.add(badge)}
ranger.g.position.set(-1,0,2);FO.add(ranger.g);const smoke=puffs(scene,40,.28,0xc8c8d0,{opacity:.6,depthWrite:false});
const rec=label3d(['*7 RAYOS','1942 → 1977'],{w:3,h:1.7,px:110,accent:'#ffc23a'});rec.position.set(301.7,2.4,2.6);scene.add(rec);
// ---------- lluvia determinista
const NR=1400,rp=new Float32Array(NR*6),RG=new THREE.BufferGeometry();RG.setAttribute('position',new THREE.BufferAttribute(rp,3));const RD=[];for(let i=0;i<NR;i++)RD.push([(R()-.5)*60,R()*40,-20+R()*55,.8+R()*.4]);
const rain=new THREE.LineSegments(RG,new THREE.LineBasicMaterial({color:0x9fb4e8,transparent:true,opacity:.55}));rain.frustumCulled=false;scene.add(rain);
function drawRain(t,cx){for(let i=0;i<NR;i++){const[x,y0,z,v]=RD[i];const y=((y0-t*28*v)%40+40)%40;rp[i*6]=cx+x;rp[i*6+1]=y;rp[i*6+2]=z;rp[i*6+3]=cx+x-.12;rp[i*6+4]=y+1.1;rp[i*6+5]=z}RG.attributes.position.needsUpdate=true}
// ---------- relámpagos: camino quebrado con ramas, tubo emisivo + halo
const boltMat=new THREE.MeshBasicMaterial({color:0xeef4ff,toneMapped:false,transparent:true});const boltGlow=new THREE.MeshBasicMaterial({color:0x8fb0ff,toneMapped:false,transparent:true,opacity:.35,blending:THREE.AdditiveBlending,depthWrite:false});
function bolt(seed,from,to){const q=mk(seed),g=new THREE.Group();const path=(a,b,n,j)=>{const P=[];for(let i=0;i<=n;i++){const u=i/n;const p=a.clone().lerp(b,u);if(i>0&&i<n){p.x+=(q()-.5)*j;p.z+=(q()-.5)*j*.5}P.push(p)}return P};
 const main=path(from,to,18,4.5);const add=(P,rad)=>{const c=new THREE.CatmullRomCurve3(P,false,'catmullrom',0);g.add(new THREE.Mesh(new THREE.TubeGeometry(c,P.length*4,rad,5),boltMat));g.add(new THREE.Mesh(new THREE.TubeGeometry(c,P.length*4,rad*4,5),boltGlow))};add(main,.12);
 for(let k=0;k<3;k++){const i=3+Math.floor(q()*10);const a=main[i];const b=a.clone().add(V3((q()-.5)*12,-6-q()*8,(q()-.5)*4));add(path(a,b,7,2.5),.06)}const hg=glow(0xdfe8ff,9,.9);hg.position.copy(to);g.add(hg);g.visible=false;return g}
// golpes: [t, objetivo]  — torre (s1/s2/cta), guardabosques (s3, 7 golpes), casa lejos (s4)
const t1=TL.s1[0],t2=TL.s2[0],t3=TL.s3[0],t4=TL.s4[0],tC=TL.cta[0];
const tip=TW.userData.tip;const ST=[];
const addS=(t,to,src)=>{const b=bolt(ST.length*7+1,src||V3(to.x+(R()-.5)*14,48,to.z-6),to);(to.x>200?scene:city).add(b);ST.push({t,b,to})};
[0,2.2].forEach(x=>addS(x,tip));[t1+1.2,t1+3.4].forEach(x=>addS(x,tip));
{const d=TL.s2[1]-t2;for(let k=0;k<6;k++)addS(t2+.6+k*(d-1.2)/6,tip)}
const RT=V3(299,4.5,2);{const d=TL.s3[1]-t3;for(let k=0;k<7;k++)addS(t3+.5+k*(d-1)/7,RT)}
addS(t4+1,V3(8,0,-30).add(V3(0,0,0)));addS(tC+.8,tip);addS(tC+2.6,tip);
const towerStrikes=ST.filter(s=>s.to===tip);const rangerStrikes=ST.filter(s=>s.to===RT);
const flashAt=t=>{let f=0;for(const s of ST){const a=t-s.t;if(a>=0&&a<.45){const fl=a<.08?1:a<.16?.35:a<.24?.85:Math.max(0,1-(a-.24)/.2)*.5;if(fl>f)f=fl}}return f};
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],m=mouthAt(t);const forest=s==='s3';
 city.visible=!forest;FO.visible=rec.visible=forest;smoke.m.visible=forest;
 ST.forEach(o=>{const a=t-o.t;o.b.visible=a>=0&&a<.32&&(a<.08||a>.14);if(o.b.visible){o.b.children.forEach(c=>{if(c.material===boltMat)return})}});
 const f=flashAt(t);scene.background=NIGHT.clone().lerp(FLASH,f*.8);scene.fog.color.copy(scene.background);hemi.intensity=(s==='s4'?1.1:forest?1.0:.55)+(forest?.9:2.4)*f;
 const cur=ST.filter(o=>t>=o.t&&t<o.t+.45).pop();if(cur){flashL.position.copy(cur.to).add(V3(0,6,4)).add(cur.to.x>200?V3(0,0,0):V3(0,0,0));flashL.intensity=(forest?30:400)*f}else flashL.intensity=0;
 drawRain(t,forest?300:0);TW.userData.beacon.material.opacity=.5+.5*Math.sin(t*4);
 let p,q;
 if(!forest){const n=towerStrikes.filter(o=>t>=o.t+.05).length;counter.set([`RAYOS: ${n}`]);counter.visible=s!=='h'&&s!=='s4';
  hero.g.visible=s==='s4';house.userData.lamp.material.opacity=s==='s4'?ss(d*.65,d*.8,lt)*.9:0;
  if(s==='s4'){// el capataz deja el paraguas y entra en casa
   const k=ss(.3,d*.7,lt);hero.g.position.set(-8-7.2*k,0,20-2.8*k);hero.g.rotation.y=-1.2*ss(0,.4,k);hero.g.visible=k<.98;hero.pose(t,m,{walk:k>0&&k<.98?t*9:null,look:.2});umb.visible=true;
   house.userData.door.rotation.y=-1.2*ss(.5,.8,k);house.userData.door.position.x=-1.4-.6*ss(.5,.8,k);
   const kk=ss(0,d,lt);p=V3(-10.5+kk,5,38-kk*2);q=V3(-11.5,2.8,17)}
  else if(s==='h'){const kk=ss(0,d,lt);p=V3(6-kk*2,4,58-kk*6);q=V3(0,20,0)}
  else if(s==='s1'){const kk=ss(0,d,lt);p=V3(-14+kk*6,6,46);q=V3(0,20,0)}
  else if(s==='s2'){const kk=ss(0,d,lt);p=V3(12-kk*3,5,52-kk*4);q=V3(2,19,0)}
  else{const kk=ss(0,d,lt);p=V3(0,5,62+kk*4);q=V3(1,20,0)}
  if(f>.6){p.x+=(R()-.5)*.25;p.y+=(R()-.5)*.25}}
 else{const n=rangerStrikes.filter(o=>t>=o.t+.05).length;rec.set([`*${n} RAYO${n===1?'':'S'}`,'1942 → 1977']);
  ranger.pose(t,m,{look:-.3+Math.sin(t*.7)*.2,armsUp:n>0&&n<7?.15:0});
  const last=rangerStrikes.filter(o=>t>=o.t).pop();const age=last?t-last.t:9;for(let i=0;i<40;i++){const a=i*2.4,h=age*(.8+(i%5)*.3);smoke.set(i,299+Math.cos(a)*.5*(1+age),4.6+h,2+Math.sin(a)*.4,age<2.2?(1-age/2.2)*(.6+(i%3)*.2):0)}smoke.done();
  const kk=ss(0,d,lt);p=V3(300.3+kk*.3,3.3,18.5-kk*2);q=V3(300.3,4.1,0);if(f>.6){p.x+=(R()-.5)*.15}}
 cam.position.copy(p);cam.lookAt(q);r.render(scene,cam)};
window.ready=true;
