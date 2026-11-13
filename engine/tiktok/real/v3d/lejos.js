// ¿Y si la Tierra se aleja del Sol? (2104). Serie ¿QUÉ PASARÍA SI…? Parte 10. Basado en cerca.js (parte 9).
// Nuevo: CASQUETE DE HIELO que avanza de los polos al ecuador (instancias sobre el globo), LÍNEA DEL LÍMITE (Kopparapu 2013, 1,70 UA) y
// FRANJA DE ZONA HABITABLE (0,99–1,70 UA) con el borde caliente que late; medidor de luz y temperatura ∝ 1/d² y 1/√d.
import {THREE,J,mk,ss,V3,clamp,stage,box,glow,capataz,segAt,mouthAt,label3d,puffs,stars,voxGlobe} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x02030a,fog:null,exposure:1.05});cam.far=3000;cam.updateProjectionMatrix();const R=mk(2104);
const hemi=new THREE.HemisphereLight(0xcfe0ff,0x202030,.22);scene.add(hemi);
const ST=stars(scene,2200,{r0:900,r1:1100,size:2.2});
const AU=70;
// ---------- SOL (arriba, en el origen)
const SUN=new THREE.Group();scene.add(SUN);
const sunCore=new THREE.Mesh(new THREE.SphereGeometry(23.5,48,32),new THREE.MeshBasicMaterial({color:0xffb030,toneMapped:false}));SUN.add(sunCore);
const NG=1400;const gran=new THREE.InstancedMesh(new THREE.BoxGeometry(2.2,2.2,2.2),new THREE.MeshBasicMaterial({toneMapped:false}),NG);gran.frustumCulled=false;SUN.add(gran);
const GD=[];for(let i=0;i<NG;i++){const y=1-2*(i+.5)/NG,rr=Math.sqrt(1-y*y),a=i*Math.PI*(3-Math.sqrt(5));GD.push([Math.cos(a)*rr,y,Math.sin(a)*rr,R()*6.28])}
const gO=new THREE.Object3D(),gC=new THREE.Color();
const updSun=t=>{for(let i=0;i<NG;i++){const[x,y,z,ph]=GD[i];const b=.5+.5*Math.sin(t*1.7+ph*3);gO.position.set(x*24.2,y*24.2,z*24.2);gO.lookAt(0,0,0);gO.scale.setScalar(.7+.5*b);gO.updateMatrix();gran.setMatrixAt(i,gO.matrix);gC.setRGB(1,.62+.33*b,.18+.3*b);gran.setColorAt(i,gC)}gran.instanceMatrix.needsUpdate=true;gran.instanceColor.needsUpdate=true};
const cor1=glow(0xffc050,130,.85),cor2=glow(0xff7a20,220,.45);SUN.add(cor1,cor2);
const SL=new THREE.PointLight(0xfff0d8,9,0,0);SUN.add(SL);
// ---------- TIERRA
const EG=new THREE.Group();scene.add(EG);const glb=voxGlobe(9000,8);EG.add(glb.group);
const atm=glow(0x6ab8ff,24,.35);EG.add(atm);
const meter=label3d(['LUZ DEL SOL','*100 %'],{w:15,h:6,px:140,sprite:true});scene.add(meter);
const dlab=label3d(['*150 MILLONES','DE KILÓMETROS'],{w:26,h:8,px:150,sprite:true});scene.add(dlab);
const bar=box(.6,1,.6,0xffd23a,.05,{emissive:0xffb020,emissiveIntensity:.8});scene.add(bar);
const ticks=[];for(let i=0;i<=10;i++){const tk=box(i%5?2.4:4.2,.5,.5,0xffd23a,.05,{emissive:0xffb020,emissiveIntensity:.8});scene.add(tk);ticks.push(tk)}
// ---------- HIELO: cubos blancos sobre el globo que tapan desde los polos (ice 0..1)
const NI=2600;const ICE=new THREE.InstancedMesh(new THREE.BoxGeometry(.62,.62,.62),new THREE.MeshStandardMaterial({color:0xf2f8ff,roughness:.35,emissive:0x9fc8ff,emissiveIntensity:.18}),NI);ICE.frustumCulled=false;glb.group.add(ICE);
const ID=[];for(let i=0;i<NI;i++){const y=1-2*(i+.5)/NI,rr=Math.sqrt(1-y*y),a=i*Math.PI*(3-Math.sqrt(5));ID.push([Math.cos(a)*rr,y,Math.sin(a)*rr,R()])}
const iO=new THREE.Object3D();let lastIce=-1;
const setIce=ice=>{if(Math.abs(ice-lastIce)<.004)return;lastIce=ice;for(let i=0;i<NI;i++){const[x,y,z,n]=ID[i];const th=1-ice*(1.02)+n*.06;const on=Math.abs(y)>th;const g=on?clamp((Math.abs(y)-th)*14):0;iO.position.set(x*8.25,y*8.25,z*8.25);iO.lookAt(0,0,0);iO.scale.setScalar(g);iO.updateMatrix();ICE.setMatrixAt(i,iO.matrix)}ICE.instanceMatrix.needsUpdate=true};
// ---------- límite exterior (1,70 UA) y franja habitable (0,99–1,70)
const LIM=new THREE.Group();scene.add(LIM);{const b=box(60,.8,.8,0x4de3ff,.1,{emissive:0x2ab8ff,emissiveIntensity:1.6});LIM.add(b);const g=glow(0x4de3ff,40,.35);g.scale.set(70,8,1);LIM.add(g)}LIM.position.set(0,-AU*1.7,0);
const limLab=label3d(['*LÍMITE: 1,7×','ESTUDIO DE 2013'],{w:16,h:5,px:120,sprite:true,accent:'#4de3ff'});scene.add(limLab);
const ZONE=new THREE.Mesh(new THREE.BoxGeometry(30,AU*(1.70-.99),4),new THREE.MeshBasicMaterial({color:0x3ad07a,transparent:true,opacity:.18,depthWrite:false}));ZONE.position.set(0,-AU*(1.70+.99)/2,-6);scene.add(ZONE);
const hot=box(34,.9,.9,0xff4a3a,.1,{emissive:0xff2a1a,emissiveIntensity:1.6});hot.position.set(0,-AU*.99,-4);scene.add(hot);const hotG=glow(0xff4a3a,40,.4);hotG.scale.set(60,10,1);hot.add(hotG);
const zLab=label3d(['ZONA','*HABITABLE'],{w:14,h:5,px:130,sprite:true,accent:'#4ade80'});scene.add(zLab);
const hLab=label3d(['*BORDE CALIENTE','AQUÍ ESTAMOS'],{w:19,h:6,px:120,sprite:true,accent:'#ff6a4a'});scene.add(hLab);
const mars=label3d(['*DISTANCIA DE MARTE'],{w:16,h:2.6,px:110,sprite:true,accent:'#ff8a3a'});scene.add(mars);
// ---------- capataz en su isla flotante
const ISL=new THREE.Group();scene.add(ISL);{const b=box(7,1.6,6,0x6a8a4a,.15);b.position.y=-.8;ISL.add(b);const b2=box(5,2,4.4,0x7a5a3a,.15);b2.position.y=-2.4;ISL.add(b2);const b3=box(2.6,1.6,2.4,0x6a4a2e,.15);b3.position.y=-4;ISL.add(b3)}
const hero=capataz();ISL.add(hero.g);const islL=new THREE.DirectionalLight(0xfff0d8,2.4);islL.position.set(0,60,20);islL.target=ISL;scene.add(islL);
const Ed=(s,lt,d)=>{if(s==='h')return 1+.03*ss(d*.3,d,lt);if(s==='s1')return 1.03+.07*ss(d*.1,d*.6,lt);if(s==='s2')return 1.1+.424*ss(d*.05,d*.6,lt);if(s==='s3')return 1.524+.176*ss(d*.05,d*.7,lt);return 1};
const Ic=(s,lt,d)=>{if(s==='h'||s==='s4'||s==='cta')return .1;if(s==='s1')return .1+.08*ss(d*.2,d,lt);if(s==='s2')return .18+.62*ss(d*.2,d*.9,lt);if(s==='s3')return .8+.2*ss(0,d*.8,lt);return .1};
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],k=ss(0,d,lt),m=mouthAt(t);
 updSun(t);SUN.rotation.y=t*.05;cor1.material.opacity=.8+.08*Math.sin(t*3);
 const D=Ed(s,lt,d);EG.position.set(0,-AU*D,0);glb.group.rotation.y=t*.3;glb.group.rotation.z=.41;setIce(Ic(s,lt,d));
 const light=1/(D*D),temp=Math.round(255/Math.sqrt(D)-255);
 meter.set(s==='s2'&&lt>d*.45?['DISTANCIA DE MARTE',`*${Math.round(light*100)} % DE LUZ`]:['LUZ DEL SOL',`*${Math.round(light*100)} %`]);if(s==='s2'){meter.position.set(0,-AU*D-11.5,4)}else{meter.position.set(10,-AU*D+17,2)}meter.visible=s==='h'||s==='s1'||s==='s2';
 atm.material.color.setHex(Ic(s,lt,d)>.5?0xcfe8ff:0x6ab8ff);
 // regla Sol–Tierra (s1)
 const ruler=s==='s1';bar.scale.x=2.4;bar.visible=ruler;ticks.forEach(tk=>tk.visible=ruler);dlab.visible=ruler;
 if(ruler){const top=-25,bot=-AU*D+9;bar.scale.y=Math.max(.01,top-bot);bar.position.set(-14,(top+bot)/2,0);ticks.forEach((tk,i)=>{tk.position.set(-14,top+(bot-top)*i/10,0)});dlab.set(['*+10 %','MÁS LEJOS']);dlab.position.set(-1,-AU*D+30,3);dlab.scale.set(18,5.5,1);dlab.material.opacity=ss(d*.2,d*.5,lt)}
 mars.visible=false;mars.position.set(0,-AU*D+12,4);mars.material.opacity=ss(d*.45,d*.65,lt);
 LIM.visible=s==='s3'||s==='s4';limLab.visible=s==='s3';limLab.position.set(0,-AU*1.7-8,4);limLab.material.opacity=ss(d*.3,d*.55,lt);
 ZONE.visible=hot.visible=hLab.visible=s==='s4';zLab.visible=false;
 if(s==='s4'){ZONE.material.opacity=.22*ss(0,d*.3,lt);zLab.position.set(0,-AU*1.38,4);hot.material.emissiveIntensity=1.2+.9*Math.abs(Math.sin(t*4));hLab.position.set(0,-AU*.99-14,6);hLab.material.opacity=ss(d*.35,d*.55,lt)}
 ISL.visible=s==='cta';ISL.position.set(12,-AU*D-5,6);ISL.rotation.y=-.5;
 hero.pose(t,m*.25,{wave:s==='cta'?1:0,look:.4});
 let p,q;
 if(s==='h'){p=V3(16-k*4,-AU*D+18,128-k*10);q=V3(0,-AU*D+27,0)}
 else if(s==='s1'){p=V3(22,-AU*D+18,150-k*10);q=V3(0,-AU*D+30,0)}
 else if(s==='s2'){p=V3(12,-AU*D+6,74-k*8);q=V3(0,-AU*D+1.5,0)}
 else if(s==='s3'){p=V3(-10+k*6,-AU*D+4,64-k*4);q=V3(0,-AU*D-1,0)}
 else if(s==='s4'){p=V3(10-k*3,-AU*.94,92-k*8);q=V3(0,-AU*.95,0)}
 else{p=V3(9-k*2,-AU+1,64-k*4);q=V3(6,-AU+7,0)}
 cam.position.copy(p);cam.lookAt(q);r.render(scene,cam)};
window.ready=true;
