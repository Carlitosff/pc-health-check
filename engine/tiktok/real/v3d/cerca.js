// ¿Y si la Tierra se acerca al Sol? (2004). Serie ¿QUÉ PASARÍA SI…? Parte 9.
// Reutilizable: SOL de cubos que hierve (granulación por instancias + corona), Tierra que se desliza por un EJE VERTICAL hacia el Sol (sol arriba, al
// fondo de la franja de subtítulos; la Tierra queda abajo, libre), regla de distancia en UA con rótulo vivo, MEDIDOR DE LUZ integrado (∝ 1/d²),
// océanos que se escapan al espacio en cubitos, VENUS con nubes que giran. La capataz en su isla flotante de bloques (h, cta).
import {THREE,J,mk,ss,V3,clamp,stage,box,glow,capataz,segAt,mouthAt,label3d,puffs,stars,voxGlobe} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x02030a,fog:null,exposure:1.05});cam.far=3000;cam.updateProjectionMatrix();const R=mk(2004);
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
// agua que se escapa (s3)
const NW=220;const water=puffs(scene,NW,.9,0x7ad0ff,{opacity:.85});const WD=[];for(let i=0;i<NW;i++)WD.push([R()*6.28,R()*2-1,R(),R()]);
const wl=label3d(['*1 % MÁS CERCA','EL AGUA SE ESCAPA'],{w:11,h:3.4,px:110,sprite:true,accent:'#4de3ff'});scene.add(wl);
// ---------- VENUS (s4)
const vc=document.createElement('canvas');vc.width=512;vc.height=256;{const g=vc.getContext('2d');for(let y=0;y<256;y++){const k=.5+.5*Math.sin(y*.07+Math.sin(y*.21)*2);g.fillStyle=`rgb(${230+18*k|0},${190+30*k|0},${110+40*k|0})`;g.fillRect(0,y,512,1)}for(let i=0;i<300;i++){g.fillStyle=`rgba(255,240,200,${.08+R()*.1})`;g.beginPath();g.ellipse(R()*512,R()*256,20+R()*60,4+R()*8,0,0,6.3);g.fill()}}
const vt=new THREE.CanvasTexture(vc);vt.colorSpace=THREE.SRGBColorSpace;vt.wrapS=THREE.RepeatWrapping;
const VEN=new THREE.Mesh(new THREE.SphereGeometry(7.6,48,32),new THREE.MeshStandardMaterial({map:vt,roughness:.9,emissive:0x3a2208,emissiveIntensity:.25}));scene.add(VEN);
const vatm=glow(0xffd890,22,.4);VEN.add(vatm);
const vlab=label3d(['VENUS','*CASI 2× LUZ','MÁS DE 450 °C'],{w:11,h:5.6,px:110,sprite:true,accent:'#ff8a3a'});scene.add(vlab);
// ---------- capataz en su isla flotante
const ISL=new THREE.Group();scene.add(ISL);{const b=box(7,1.6,6,0x6a8a4a,.15);b.position.y=-.8;ISL.add(b);const b2=box(5,2,4.4,0x7a5a3a,.15);b2.position.y=-2.4;ISL.add(b2);const b3=box(2.6,1.6,2.4,0x6a4a2e,.15);b3.position.y=-4;ISL.add(b3)}
const hero=capataz();ISL.add(hero.g);const islL=new THREE.DirectionalLight(0xfff0d8,2.4);islL.position.set(0,60,20);islL.target=ISL;scene.add(islL);
const t1=TL.s1[0],t2=TL.s2[0],t3=TL.s3[0],t4=TL.s4[0],tC=TL.cta[0];
const Ed=(s,lt,d)=>{if(s==='h')return 1-.06*ss(d*.2,d,lt);if(s==='s2')return 1-.1*ss(d*.15,d*.7,lt);if(s==='s3')return .99;return 1};
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],k=ss(0,d,lt),m=mouthAt(t);
 updSun(t);SUN.rotation.y=t*.05;cor1.material.opacity=.8+.08*Math.sin(t*3);
 const D=Ed(s,lt,d);EG.position.set(0,-AU*D,0);glb.group.rotation.y=t*.3;glb.group.rotation.z=.41;
 const light=1/(D*D);meter.set(['LUZ DEL SOL',`*${Math.round(light*100)} %`]);meter.position.set(9.5,-AU*D+17,2);
 meter.visible=s==='s2'||s==='h';
 // regla de distancia entre Sol y Tierra (s1)
 const ruler=s==='s1';bar.scale.x=2.4;bar.visible=ruler;ticks.forEach(tk=>tk.visible=ruler);dlab.visible=ruler;
 if(ruler){const g=ss(.2,d*.6,lt);const top=-25,bot=-AU*D+9;const yy=top+(bot-top)*g;bar.scale.y=Math.max(.01,top-yy);bar.position.set(-14,(top+yy)/2,0);
  ticks.forEach((tk,i)=>{const y=top+(bot-top)*i/10;tk.position.set(-14,y,0);tk.visible=y>=yy-.1});dlab.position.set(8,(top+bot)/2,3);dlab.material.opacity=ss(d*.4,d*.7,lt)}
 // agua que se escapa (s3): cubitos que salen del lado de noche y se alejan del Sol
 water.m.visible=s==='s3';wl.visible=false;
 if(s==='s3'){for(let i=0;i<NW;i++){const[a,h,sp,o]=WD[i];const ph=(lt*.35*(.5+sp)+o)%1;const rr=8.2+ph*30;const x=Math.cos(a)*Math.sqrt(1-h*h)*(8.2+ph*6),z=Math.sin(a)*Math.sqrt(1-h*h)*(8.2+ph*6);
   water.set(i,x,-AU*D+h*8.2*.6-ph*30*(.4+sp*.6),z,(1-ph)*(.6+o*.6)*ss(0,.6,lt),ph*6)}water.done();wl.position.set(0,-AU*D-22,4);wl.material.opacity=ss(.8,1.6,lt)}
 // Venus
 const vOn=s==='s4';VEN.visible=vlab.visible=vOn;
 if(vOn){VEN.position.set(5.5,-AU*.72,-2);VEN.rotation.y=-t*.25;vt.offset.x=t*.02;vlab.position.set(5.5,-AU*.72-11,2);vlab.material.opacity=ss(.6,1.4,lt);EG.position.set(-6,-AU,0)}
 // isla con la capataz (h, cta)
 ISL.visible=s==='cta';ISL.position.set(12,-AU*D-5,6);ISL.rotation.y=-.5;
 hero.pose(t,m*.25,{wave:s==='cta'?1:0,look:.4,point:s==='h'&&lt>d*.4?.6:0});
 let p,q;
 if(s==='h'){p=V3(16-k*4,-AU*D+18,128-k*10);q=V3(0,-AU*D+27,0)}
 else if(s==='s1'){p=V3(24,-42,175-k*10);q=V3(0,-36,0)}
 else if(s==='s2'){p=V3(10,-AU*D+16,118-k*14);q=V3(1,-AU*D+25,0)}
 else if(s==='s3'){p=V3(-14+k*8,-AU*D-12,62);q=V3(0,-AU*D-6,0)}
 else if(s==='s4'){p=V3(3,-60,74-k*6);q=V3(0,-55,0)}
 else{p=V3(9-k*2,-AU+1,64-k*4);q=V3(6,-AU+7,0)}
 cam.position.copy(p);cam.lookAt(q);r.render(scene,cam)};
window.ready=true;
