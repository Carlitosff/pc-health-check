// ¿Y si se apaga la gravedad 5 segundos? (1504). Serie ¿QUÉ PASARÍA SI…? Parte 4. Reutilizable: calle que flota con regla integrada, globo con tangente, estación espacial que se sale de la órbita.
import {THREE,J,mk,ss,V3,clamp,stage,sun,box,glow,pixTex,capataz,segAt,mouthAt,puffs,label3d,ruler,stars,voxGlobe} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x8ad4ff,fog:[0xc8e4ff,60,190],exposure:1.08});const R=mk(1504);
scene.add(new THREE.HemisphereLight(0xdcefff,0x8a9a6a,1.4));const S=sun(scene,{pos:[-16,34,18],span:34});
const SKY=new THREE.Color(0x8ad4ff),SPACE=new THREE.Color(0x02030a);
// ---------- calle
const st=new THREE.Group();scene.add(st);
const grass=pixTex(128,128,(g,w,h)=>{const q=mk(8);g.fillStyle='#6fb24e';g.fillRect(0,0,w,h);for(let i=0;i<700;i++){g.fillStyle=['#62a544','#7dbd58','#568f3c'][Math.floor(q()*3)];g.fillRect(Math.floor(q()*w/4)*4,Math.floor(q()*h/4)*4,4,4)}},[40,40]);
const gnd=new THREE.Mesh(new THREE.PlaneGeometry(400,400),new THREE.MeshStandardMaterial({map:grass,roughness:1}));gnd.rotation.x=-Math.PI/2;gnd.receiveShadow=true;st.add(gnd);
const plaza=new THREE.Mesh(new THREE.PlaneGeometry(40,22),new THREE.MeshStandardMaterial({map:pixTex(64,64,(g,w,h)=>{g.fillStyle='#d8cdb6';g.fillRect(0,0,w,h);g.strokeStyle='#b9ad94';g.lineWidth=2;for(let i=0;i<=w;i+=16){g.strokeRect(i,0,16,h);g.strokeRect(0,i,w,16)}},[10,6]),roughness:.95}));plaza.rotation.x=-Math.PI/2;plaza.position.set(0,.01,0);plaza.receiveShadow=true;st.add(plaza);
const COLS=[0xd9c7a8,0xc2573f,0x8fa6b8,0xe8dfca,0xa86a48,0x6f86a8];
[[-15,-14,8,14],[-5,-16,9,18],[6,-15,8,12],[16,-13,8,16],[-26,-10,7,11],[27,-10,7,13]].forEach(([x,z,w,h],i)=>{const b=box(w,h,7,COLS[i%6],.15);b.position.set(x,h/2,z);st.add(b);for(let y=1.5;y<h-1;y+=2.2)for(let a=-w/2+1.3;a<w/2-.8;a+=1.8){const wi=box(.9,1.2,.1,R()<.3?0xffe9a8:0x2a3a58,.02,R()<.3?{emissive:0xffc050,emissiveIntensity:.4}:{});wi.position.set(x+a,y,z+3.52);st.add(wi)}});
// cosas que flotan: cada una con su fase (sube despacio y gira un poco)
const fl=[];const add=(o,x,z,y0=0)=>{o.position.set(x,y0,z);o.userData={x,z,y0,ph:R()*6,rot:(R()-.5)*.6};st.add(o);fl.push(o);return o};
const car=(c)=>{const g=new THREE.Group();const a=box(3.4,.8,1.6,c,.1);a.position.y=.75;const b=box(1.8,.7,1.4,0x18202e,.08);b.position.y=1.45;g.add(a,b);[[-1.1,.7],[1.1,.7],[-1.1,-.7],[1.1,-.7]].forEach(([x,z])=>{const w=box(.6,.6,.25,0x15151a,.05);w.position.set(x,.32,z);g.add(w)});return g};
add(car(0xe0344a),-9,5);add(car(0x2d6be0),9.5,6.5);
const bench=()=>{const g=new THREE.Group();const s=box(3,.2,.9,0x8a5a32,.04);s.position.y=.8;const bk=box(3,.8,.15,0x8a5a32,.04);bk.position.set(0,1.3,-.4);g.add(s,bk);[-1.3,1.3].forEach(x=>{const l=box(.15,.8,.8,0x2a2a30,.02);l.position.set(x,.4,0);g.add(l)});return g};add(bench(),-5,-3);
const balls=[0xff5a3a,0x3ad1ff,0xffd23a,0x7ce06a].map((c,i)=>add(new THREE.Mesh(new THREE.SphereGeometry(.45,16,12),new THREE.MeshStandardMaterial({color:c,roughness:.5})),-7.5+i*1.4,1+(i%2)*1.2));balls.forEach(b=>b.castShadow=true);
const cups=[0,1,2].map(i=>add(box(.5,.6,.5,0xffffff,.1),5.3+i*.8,1.2,1.05));const tbl=box(3,.15,1.6,0xa86a48,.04);tbl.position.set(6.1,.95,1.2);st.add(tbl);[[-1.3,-.6],[1.3,-.6],[-1.3,.6],[1.3,.6]].forEach(([x,z])=>{const l=box(.12,.95,.12,0x2a2a30,.02);l.position.set(6.1+x,.47,1.2+z);st.add(l)});
const hero=capataz();hero.g.position.set(0,0,2);scene.add(hero.g);fl.push(hero.g);hero.g.userData={x:0,z:2,y0:0,ph:0,rot:0};
// regla integrada (1 unidad de escena = 10 cm) y rótulo con la altura
const U=1.75/4.1;// 1 unidad de escena = 43 cm (el capataz mide ~4,1 = 1,75 m)
const RU=ruler(.05/U*7,{step:.05/U,every:2,unit:5,ls:.5});RU.position.set(1.25,0,2.9);st.add(RU);
const HL=label3d(['¿ cm ?'],{w:2.6,h:1,px:150});HL.position.set(3.6,4.4,2.4);st.add(HL);
const ring=new THREE.Mesh(new THREE.RingGeometry(1.1,1.35,40),new THREE.MeshBasicMaterial({color:0xffd23a,transparent:true,opacity:.8,side:THREE.DoubleSide}));ring.rotation.x=-Math.PI/2;ring.position.set(0,.03,2);st.add(ring);
// anillos de Saturno en el cielo (teaser de la parte 5)
const SR=new THREE.Group();{for(let i=0;i<5;i++){const m=new THREE.Mesh(new THREE.RingGeometry(60+i*7,65+i*7,96),new THREE.MeshBasicMaterial({color:[0xf2e2b8,0xd9c294,0xf6ecd0,0xc8ae7c,0xe8d8b0][i],transparent:true,opacity:.75,side:THREE.DoubleSide,fog:false}));SR.add(m)}SR.rotation.set(1.25,0,.35);SR.position.set(0,30,-120);scene.add(SR)}
const dust=puffs(scene,140,.35,0xcbbfa6,{opacity:.85,depthWrite:false});const dp=[];for(let i=0;i<140;i++)dp.push([R()*6.28,R(),R()]);
// ---------- globo con la tangente
const GL=new THREE.Group();GL.position.set(500,0,0);scene.add(GL);const glb=voxGlobe(9000,10);GL.add(glb.group);
const LAT=40.4*Math.PI/180;const pin=new THREE.Group();const pinB=box(.5,.5,.5,0xffd23a,.1,{emissive:0xffa000,emissiveIntensity:.8});pinB.position.y=10.5;pin.add(pinB);const pg=glow(0xffd23a,3,.9);pg.position.y=10.6;pin.add(pg);pin.rotation.z=-(Math.PI/2-LAT);glb.group.add(pin);
const tang=new THREE.Mesh(new THREE.BoxGeometry(.14,.14,1),new THREE.MeshBasicMaterial({color:0xff3a4a,toneMapped:false}));GL.add(tang);const arrow=new THREE.Mesh(new THREE.ConeGeometry(.5,1.2,12),new THREE.MeshBasicMaterial({color:0xff3a4a,toneMapped:false}));GL.add(arrow);
const sp1=label3d(['*1.270 km/h','EN MADRID'],{w:7,h:3,px:130,sprite:true});GL.add(sp1);
stars(scene,1200);
// ---------- estación espacial que se sale de la órbita
const SPc=new THREE.Group();SPc.position.set(1000,0,0);scene.add(SPc);
const planet=new THREE.Mesh(new THREE.SphereGeometry(129,96,64),new THREE.MeshStandardMaterial({color:0x2d6fd0,roughness:.7,map:pixTex(256,128,(g,w,h)=>{const q=mk(5);g.fillStyle='#2a68c8';g.fillRect(0,0,w,h);for(let i=0;i<90;i++){g.fillStyle=q()<.6?'#4f9a48':'#f2f6ff';g.fillRect(q()*w,q()*h,8+q()*30,5+q()*16)}})}));planet.position.set(0,-128,0);SPc.add(planet);const atm=glow(0x7fc8ff,300,.4);atm.position.copy(planet.position);SPc.add(atm);
const orbit=new THREE.Group();SPc.add(orbit);for(let i=0;i<400;i++){const a=i/400*Math.PI*2;const d=box(1.5,.35,.35,0xffd23a,.05,{emissive:0xffb000,emissiveIntensity:1.2});d.position.set(Math.sin(a)*136,-128+Math.cos(a)*136,0);d.rotation.z=-a;if(i%2)orbit.add(d)}
const iss=new THREE.Group();{const m=box(4,1,1,0xd8dce4,.2,{metalness:.4});iss.add(m);const tr=box(13,.25,.25,0xb8bcc8,.04);iss.add(tr);[-5.2,-3.4,3.4,5.2].forEach(x=>[-1,1].forEach(s=>{const p=box(1.5,.06,3.2,0x2a3e8a,.02,{emissive:0x10205a,emissiveIntensity:.5});p.position.set(x,0,s*1.9);iss.add(p)}));const mod=box(1,1,2.4,0xe8e8ee,.2);mod.position.set(0,0,1.2);iss.add(mod)}SPc.add(iss);
const issL=label3d(['*+108 m','FUERA DE ÓRBITA'],{w:7,h:3,px:130,sprite:true});SPc.add(issL);
const suns=sun(scene,{pos:[1040,40,40],power:0,span:10});
const MXs=.25/U;
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],m=mouthAt(t);let p,q,bg=SKY;
 const onS=['h','s2','s4','cta'].includes(s);st.visible=onS;hero.g.visible=onS;GL.visible=s==='s1';SPc.visible=s==='s3';dust.m.visible=s==='s4';
 // altura de flote: 0 a 25 cm (2,5 unidades) en los 5 s de s2 / s4 ; en h ya flota un poco (gancho) ; 1 unidad = 10 cm
 let lift=0,fall=0;
 const MX=.25/U;if(s==='h')lift=MX*(.55+.15*Math.sin(t*1.6));
 else if(s==='s2')lift=MX*clamp(lt/Math.max(1,d))**2;
 else if(s==='s4'){lift=MX*clamp(lt/1.5)**2;fall=ss(d*.62,d*.62+.35,lt)}
 const L=lift*(1-fall);
 if(onS){fl.forEach((o,i)=>{const u=o.userData;const LL=L/MXs;const wob=L>0?Math.sin(t*1.3+u.ph)*.05*LL:0;o.position.y=u.y0+L*(o===hero.g?1:.8+.4*((i*37)%10)/10)+wob;o.rotation.z=u.rot*LL*Math.sin(t*.7+u.ph);o.rotation.x=u.rot*.5*LL});
  hero.pose(t,m,{armsUp:s==='h'?.4:s==='s2'?.6*clamp(lt/1.5):s==='s4'?(fall>0?0:.7):0,wave:s==='cta'?1:0,look:s==='cta'?0:Math.sin(t*.6)*.3,walk:L>0&&fall===0?t*3:null});
  const cm=Math.round(L*U*100);HL.set(s==='h'?['¿ CUÁNTO','SUBES ?']:s==='cta'?['PARTE 5','*ANILLOS']:[`*${cm} cm`]);ring.material.opacity=.5+.4*Math.sin(t*4);
  SR.visible=s==='cta';HL.visible=s!=='h';
  if(s==='s4'&&fall>0){const k=clamp((lt-d*.62-.3)/1.2);for(let i=0;i<140;i++){const[a,b,c]=dp[i];const rr=1+k*(3+b*5);dust.set(i,Math.cos(a)*rr*(c<.5?1:2.5)+(c<.5?0:-4),.3+k*b*1.6,2+Math.sin(a)*rr,(1-k)*(.6+b))}dust.done()}}
 if(s==='h'){const k=ss(0,d,lt);p=V3(2+k,3,21-k*3);q=V3(1.4,2.5,2)}
 else if(s==='s2'){const k=ss(0,d,lt);p=V3(3.4-k*1.2,1.3+k*.4,8.5-k*1.5);q=V3(1.4,1.1,2)}
 else if(s==='s4'){const k=ss(0,d,lt);p=V3(3.6-k*1.2,1.3+k*.8,8.2+k*3);q=V3(1.3,1.1+k*.6,2);if(fall>0&&fall<1){p.y+=Math.sin(t*60)*.12*(1-fall)}}
 else if(s==='cta'){const k=ss(0,d,lt);p=V3(0,3+k*2,19+k*2);q=V3(0,2.6+k*9,0)}
 else if(s==='s1'){bg=SPACE;const k=ss(0,d,lt);glb.group.rotation.y=-1.2+t*.35;glb.group.rotation.x=.25;
  // posición del pin en mundo, tangente en la dirección de giro
  pinB.updateMatrixWorld();const P0=new THREE.Vector3();pinB.getWorldPosition(P0);const ax=new THREE.Vector3(0,1,0).applyEuler(glb.group.rotation);const rel=P0.clone().sub(GL.position);const dir=new THREE.Vector3().crossVectors(ax,rel).normalize();const len=2+6*ss(.6,2.6,lt);
  tang.position.copy(rel).addScaledVector(dir,len/2);tang.scale.set(1,1,len);tang.lookAt(tang.position.clone().add(dir).add(GL.position));tang.position.add(GL.position).sub(GL.position);
  arrow.position.copy(rel).addScaledVector(dir,len);arrow.quaternion.setFromUnitVectors(V3(0,1,0),dir);
  sp1.position.copy(rel).add(V3(0,4.5,2));sp1.visible=false;
  p=V3(500+rel.x*4.2,rel.y*4.2+2,rel.z*4.2+16-k*4);q=V3(500+rel.x*.5,rel.y*.5-5,rel.z*.5)}
 else if(s==='s3'){bg=SPACE;const k=clamp(lt/Math.max(1,d));const a=-.08+k*.16;const off=12*ss(.1,1,k);// la estación sale recta (tangente) y la órbita se curva
  iss.position.set(Math.sin(a)*136,-128+Math.cos(a)*136+off,0);iss.rotation.set(t*.15,0,-a);issL.position.copy(iss.position).add(V3(0,-5,0));issL.material.opacity=ss(.45,.6,k);
  const by=-128+Math.cos(a)*136;p=V3(1000+iss.position.x+5,by-1+off*.4,36-k*3);q=V3(1000+iss.position.x,by+2+off*.4,0)}
 scene.background=bg;scene.fog.near=bg===SPACE?1e4:60;scene.fog.far=bg===SPACE?2e4:190;
 if(onS){S.target.position.copy(q);S.position.set(q.x-16,34,q.z+18);S.target.updateMatrixWorld();S.intensity=2.6}else{S.intensity=0}
 suns.intensity=s==='s3'?3.6:0;if(s==='s1'){S.intensity=2.2;S.position.set(480,30,40);S.target.position.set(500,0,0);S.target.updateMatrixWorld()}
 cam.position.copy(p);cam.lookAt(q);r.render(scene,cam)};
window.ready=true;
