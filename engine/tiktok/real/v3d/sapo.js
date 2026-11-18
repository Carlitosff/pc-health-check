// Mito: '¿si tocas un sapo te salen verrugas?' (2603). Wonderopolis ('Do toads really give you warts?'): las verrugas las causa el VPH,
// pasan de persona a persona; los bultos del sapo son glándulas que sueltan toxinas para defenderse.
// Nuevo (v29): JARDÍN AL ATARDECER reutilizable (césped, estanque con ondas, juncos, piedras, luciérnagas, grifo de jardín con chorro de agua),
// SAPO de bloques (toad() en bloques.js) con bultos y PAROTOIDES que se iluminan, VIRUS de cubos que saltan de una mano a otra al saludar.
import {THREE,J,mk,ss,V3,clamp,stage,sun,box,glow,capataz,abuela,segAt,mouthAt,label3d,puffs,toad} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0xf6b98a,fog:[0xf6b98a,30,120],exposure:1.1});cam.far=600;cam.updateProjectionMatrix();const R=mk(2603);
scene.add(new THREE.HemisphereLight(0xffe2c4,0x3a5a2a,1.15));sun(scene,{pos:[-12,14,10],span:18,power:2.3,color:0xffd2a0});
// ---------- jardín
const gr=new THREE.Mesh(new THREE.PlaneGeometry(120,120),new THREE.MeshStandardMaterial({color:0x5d9a3e,roughness:.95}));gr.rotation.x=-Math.PI/2;gr.receiveShadow=true;scene.add(gr);
for(let i=0;i<260;i++){const h=.3+R()*.6;const bl=box(.12,h,.12,R()<.5?0x4f8a32:0x6aac46,.02);bl.position.set((R()-.5)*40,h/2,(R()-.5)*30-4);bl.rotation.z=(R()-.5)*.5;scene.add(bl)}
const pond=new THREE.Mesh(new THREE.CircleGeometry(4.2,48),new THREE.MeshStandardMaterial({color:0x3a7aa8,roughness:.15,metalness:.1,emissive:0x0a2a40,emissiveIntensity:.4}));pond.rotation.x=-Math.PI/2;pond.position.set(-5.5,.03,-3.5);scene.add(pond);
const rip=[0,1,2].map(i=>{const m=new THREE.Mesh(new THREE.RingGeometry(.9,1,40),new THREE.MeshBasicMaterial({color:0xcfe8ff,transparent:true,opacity:.5}));m.rotation.x=-Math.PI/2;m.position.set(-5.2,.05,-3.2);scene.add(m);return m});
for(let i=0;i<14;i++){const a=i/14*6.28;const st=box(.9+R()*.6,.5+R()*.4,.8+R()*.5,R()<.5?0x8a8a86:0x6e6e6a,.25);st.position.set(-5.5+Math.cos(a)*4.6,.25,-3.5+Math.sin(a)*4.3);st.rotation.y=R()*3;scene.add(st)}
for(let i=0;i<12;i++){const h=2+R()*1.8;const rd=box(.14,h,.14,0x4a7a2a,.03);rd.position.set(-9+R()*3,h/2,-6+R()*2.5);rd.rotation.z=(R()-.5)*.3;scene.add(rd);const tip=box(.26,.7,.26,0x7a4a2a,.08);tip.position.set(rd.position.x,h+.2,rd.position.z);scene.add(tip)}
const fence=new THREE.Group();for(let i=0;i<22;i++){const p=box(.5,2.4,.25,0xe8d6b4,.05);p.position.set(-22+i*2,1.2,-11);fence.add(p)}const rail=box(44,.25,.2,0xd8c6a4,.03);rail.position.set(0,1.7,-11);fence.add(rail);scene.add(fence);
const rock=box(2.4,1.0,1.9,0x8a8680,.35);rock.position.set(0,.5,1.2);scene.add(rock);
// grifo de jardín (s4)
const TAP=new THREE.Group();{const p=box(.35,3.4,.35,0x6a6a72,.05);p.position.y=1.7;TAP.add(p);const s=box(.9,.3,.3,0xb8b8c0,.08);s.position.set(.45,3,0);TAP.add(s);const k=box(.5,.2,.5,0xd03030,.08);k.position.set(0,3.4,0);TAP.add(k);const bs=box(1.8,.4,1.4,0x7a7a80,.1);bs.position.set(.8,.2,0);TAP.add(bs)}
TAP.position.set(6.2,0,-.4);scene.add(TAP);const NWt=140;const water=puffs(scene,NWt,.16,0x9ad8ff,{opacity:.85});const bub=puffs(scene,60,.22,0xffffff,{opacity:.9});
// luciérnagas
const NF=40;const flies=puffs(scene,NF,.12,0xfff27a,{opacity:.95});const FD=[];for(let i=0;i<NF;i++)FD.push([(R()-.5)*20,1+R()*4,(R()-.5)*10-3,R()*6.28]);
// personajes
const T=toad(1);T.g.position.set(0,1.0,1.3);T.g.rotation.y=.25;scene.add(T.g);
const hero=capataz();hero.g.position.set(2.6,0,2.6);hero.g.rotation.y=-.9;scene.add(hero.g);
const gran=abuela();gran.g.position.set(-2.4,0,2.4);gran.g.rotation.y=.9;scene.add(gran.g);
// virus de cubos (VPH) que saltan de mano a mano
const NV=7;const vir=[];for(let i=0;i<NV;i++){const v=new THREE.Group();const c=box(.34,.34,.34,0xff4a8a,.08,{emissive:0xff2a6a,emissiveIntensity:.8});v.add(c);for(let k=0;k<6;k++){const sp=box(.08,.08,.22,0xffe04a,.02,{emissive:0xffc020,emissiveIntensity:.8});const d=[[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]][k];sp.position.set(d[0]*.24,d[1]*.24,d[2]*.24);sp.lookAt(d[0]*2,d[1]*2,d[2]*2);v.add(sp)}scene.add(v);vir.push(v)}
const lVir=label3d(['VERRUGAS:','*UN VIRUS HUMANO','(VPH)'],{w:4.2,h:2.2,px:110,sprite:true,accent:'#ff5a9a'});scene.add(lVir);
const lNo=label3d(['*EL SAPO','NO LAS CONTAGIA'],{w:3.4,h:1.3,px:110,sprite:true,accent:'#4ade80'});scene.add(lNo);
const lGl=label3d(['NO SON VERRUGAS:','*SON GLÁNDULAS'],{w:3.2,h:1.15,px:110,sprite:true,accent:'#4de3ff'});scene.add(lGl);
const lTx=label3d(['GLÁNDULAS PAROTOIDES','*SUELTAN TÓXICOS'],{w:3.4,h:1.1,px:100,sprite:true,accent:'#ff8a3a'});scene.add(lTx);
const lWa=label3d(['*LÁVATE LAS MANOS','NI A LA BOCA NI A LOS OJOS'],{w:3.9,h:1.25,px:96,sprite:true,accent:'#4de3ff'});scene.add(lWa);
const drops=puffs(scene,24,.12,0xf4f0e0,{opacity:.95});
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],k=ss(0,d,lt),m=mouthAt(t);
 rip.forEach((q,i)=>{const u=((t*.45+i/3)%1);q.scale.setScalar(.5+u*3.2);q.material.opacity=.55*(1-u)});
 for(let i=0;i<NF;i++){const[x,y,z,p]=FD[i];flies.set(i,x+Math.sin(t*.7+p)*.8,y+Math.sin(t*1.3+p*2)*.4,z+Math.cos(t*.6+p)*.6,.6+.6*Math.max(0,Math.sin(t*3+p*5)),0)}flies.done();
 // sapo
 let hop=null;if(s==='cta'){const u=lt*.9;hop=u%1;T.g.position.set(0,1.0,1.3)}else T.g.position.set(0,1.0,1.3);
 T.pose(t,{hop,glow:s==='s2'?ss(.4,1.2,lt):0,paro:s==='s3'?ss(.3,1.0,lt):0});T.g.rotation.y=s==='cta'?.25+Math.sin(t*1.8)*.4:.25+Math.sin(t*.6)*.08;
 // personajes
 const hand=s==='s1';hero.pose(t,s==='h'||s==='s4'||s==='cta'?m*.3:0,{point:s==='h'?ss(.2,1,lt):0,wave:s==='cta'?1:0,look:s==='h'?-.3:0});
 gran.pose(t,0,{look:.2});gran.g.visible=hand;
 if(hand){hero.g.position.set(1.1,0,3.4);hero.g.rotation.y=-1.35;gran.g.position.set(-1.1,0,3.4);gran.g.rotation.y=1.35;const sh=Math.sin(lt*9)*.25*ss(.3,.8,lt);hero.armR.rotation.x=-1.25+sh;gran.armR.rotation.x=-1.25-sh;hero.armR.rotation.z=.6;gran.armR.rotation.z=.6}
 else if(s==='s4'){hero.g.position.set(5.4,0,.2);hero.g.rotation.y=.75;hero.armR.rotation.x=hero.armL.rotation.x=-1.0+.15*Math.sin(t*9);hero.armR.rotation.z=.35;hero.armL.rotation.z=-.35}
 else{hero.g.position.set(2.6,0,2.6);hero.g.rotation.y=-.9}
 // virus: saltan de la mano del capataz a la de la abuela
 vir.forEach((v,i)=>{v.visible=hand&&lt>.9;if(!v.visible)return;const u=((lt-.9)*.55+i/NV)%1;const a=V3(.55,2.55,4.2),b=V3(-.55,2.55,4.2);v.position.lerpVectors(a,b,u);v.position.y+=Math.sin(Math.PI*u)*1.3;v.rotation.set(t*2+i,t*3,0);v.scale.setScalar(.7+.3*Math.sin(t*6+i))});
 lVir.visible=hand;lVir.position.set(0,1.0,4.8);lVir.material.opacity=ss(.4,1,lt);
 lNo.visible=s==='h'&&lt>d*.55;lNo.position.set(-1.2,.5,3.0);lNo.material.opacity=1;
 lGl.visible=false;lGl.position.set(0,1.25,3.3);lGl.material.opacity=ss(.8,1.4,lt);
 lTx.visible=false;lTx.position.set(0,1.25,3.3);lTx.material.opacity=ss(.6,1.2,lt);
 // gotas lechosas de las parotoides (s3)
 drops.m.visible=s==='s3';if(s==='s3'){for(let i=0;i<24;i++){const side=i%2?1:-1;const u=((lt*.6+i/24)%1);drops.set(i,side*.5+side*u*.15,1.0+1.32-u*.9,1.3+.45+u*.1,(1-u)*ss(.8,1.2,lt),0)}drops.done()}
 // grifo (s4)
 const on=s==='s4'?ss(.2,.6,lt):0;water.m.visible=bub.m.visible=on>0;lWa.visible=on>0;lWa.position.set(6.4,.9,3.2);lWa.material.opacity=ss(.8,1.4,lt);
 if(on>0){for(let i=0;i<NWt;i++){const u=((t*1.6+i/NWt)%1);water.set(i,6.2+.9+Math.sin(i)*.05,3.0-u*2.6,-.4+Math.cos(i*1.7)*.05,on,0)}water.done();for(let i=0;i<60;i++){const a=i*2.4,u=((t*.5+i/60)%1);bub.set(i,7.0+Math.cos(a)*(.3+u*.5),1.9+u*1.2,-.2+Math.sin(a)*.4,on*(1-u)*(.6+.4*Math.sin(i)),0)}bub.done()}
 let p,q;
 if(s==='h'){p=V3(1.8-k*.6,3.4,13.5-k*1.2);q=V3(.6,2.1,1.3)}
 else if(s==='s1'){p=V3(.2,4.6,21-k*1.5);q=V3(0,3.9,3.4)}
 else if(s==='s2'){p=V3(.8+k*.4,4.4,8.2-k*.6);q=V3(0,2.0,1.2)}
 else if(s==='s3'){p=V3(1.6,3.6,7.6-k*.4);q=V3(0,2.1,1.4)}
 else if(s==='s4'){p=V3(5.6,4.6,15-k*1.0);q=V3(6.5,3.4,1)}
 else{p=V3(1.6-k,4.2,18);q=V3(1.2,1.9,2)}
 cam.position.copy(p);cam.lookAt(q);r.render(scene,cam)};
window.ready=true;
