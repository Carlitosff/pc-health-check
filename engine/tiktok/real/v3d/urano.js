// ¿Y si la Tierra estuviera tumbada como Urano? (3104). Serie ¿QUÉ PASARÍA SI…? Parte 20.
// Reutilizable: globo de vóxeles con EJE que se tumba (23,5° → 98°) y se orienta hacia el Sol; URANO (gasGiant con paleta cian, anillos verticales);
// PLAZA DE MADRID A MEDIANOCHE con el Sol alto y reloj de pared 00:00 (wallClock); misma plaza en la NOCHE POLAR con nieve, farolas y estrellas.
import {THREE,J,mk,ss,V3,clamp,stage,sun,box,glow,capataz,segAt,mouthAt,label3d,stars,voxGlobe,gasGiant,wallClock,snow} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x02030a,fog:null,exposure:1.1});cam.far=2500;cam.updateProjectionMatrix();const R=mk(3104);
const hemi=new THREE.HemisphereLight(0xdcefff,0xb8a080,.5);scene.add(hemi);
const D2R=Math.PI/180;const MID=J.mid||32.4;
// ---------- GLOBO (h, s2, cta) en z=-600
const GL=new THREE.Group();GL.position.set(0,0,-600);scene.add(GL);const ST=stars(scene,1500,{r0:300,r1:360,size:1.4});ST.position.copy(GL.position);
const tilt=new THREE.Group();GL.add(tilt);const glb=voxGlobe(9000,10);tilt.add(glb.group);
const axis=new THREE.Mesh(new THREE.CylinderGeometry(.22,.22,30,12),new THREE.MeshBasicMaterial({color:0xffd23a,toneMapped:false}));tilt.add(axis);
const NP=new THREE.Mesh(new THREE.SphereGeometry(.7,12,8),new THREE.MeshBasicMaterial({color:0xff4a4a,toneMapped:false}));NP.position.y=15;tilt.add(NP);
const SP=new THREE.Mesh(new THREE.SphereGeometry(.55,12,8),new THREE.MeshBasicMaterial({color:0xffd23a,toneMapped:false}));SP.position.y=-15;tilt.add(SP);
const npL=label3d(['*NORTE'],{w:3.6,h:1.3,px:120,sprite:true,accent:'#ff4a4a'});NP.add(npL);npL.position.set(0,2.2,0);
const vert=new THREE.Mesh(new THREE.CylinderGeometry(.08,.08,32,8),new THREE.MeshBasicMaterial({color:0xffffff,transparent:true,opacity:.45,toneMapped:false}));GL.add(vert);
const ang=label3d(['*23,5°'],{w:7.5,h:3,px:170,sprite:true});GL.add(ang);
const gS=new THREE.DirectionalLight(0xfff4e0,3.4);gS.position.set(-560,0,-600);gS.target=GL;scene.add(gS);
const sunB=new THREE.Mesh(new THREE.SphereGeometry(5,24,16),new THREE.MeshBasicMaterial({color:0xfff2b0,toneMapped:false}));sunB.position.set(-27,0,-600);scene.add(sunB);const sunBG=glow(0xffd070,30,.9);sunBG.position.copy(sunB.position);scene.add(sunBG);
const jun=label3d(['JUNIO','*EL NORTE MIRA AL SOL'],{w:12,h:3.2,px:110,sprite:true,accent:'#ffc23a'});GL.add(jun);
// ---------- URANO (s1) en x=-500
const UR=new THREE.Group();UR.position.set(-500,0,-600);scene.add(UR);const ST2=stars(scene,900,{r0:300,r1:360,size:1.3,seed:5});ST2.position.copy(UR.position);
const ut=new THREE.Group();UR.add(ut);const U=gasGiant(10,{seed:9,spot:false,pal:['#bfeff2','#a6e3ea','#c9f4f5','#9bdbe4','#b4ebef','#8fd2dc']});ut.add(U.mesh);
const ring=new THREE.Mesh(new THREE.RingGeometry(14,15.2,120),new THREE.MeshBasicMaterial({color:0xcfe8f0,transparent:true,opacity:.55,side:THREE.DoubleSide,toneMapped:false}));ring.rotation.x=Math.PI/2;ut.add(ring);
const ring2=new THREE.Mesh(new THREE.RingGeometry(16,16.4,120),new THREE.MeshBasicMaterial({color:0xcfe8f0,transparent:true,opacity:.35,side:THREE.DoubleSide,toneMapped:false}));ring2.rotation.x=Math.PI/2;ut.add(ring2);
const uax=new THREE.Mesh(new THREE.CylinderGeometry(.22,.22,32,12),new THREE.MeshBasicMaterial({color:0xffd23a,toneMapped:false}));ut.add(uax);
const uL=label3d(['URANO','*98°'],{w:6,h:3,px:150,sprite:true,accent:'#4de3ff'});UR.add(uL);uL.position.set(0,-15.5,4);
const uS=new THREE.DirectionalLight(0xfff4e0,3.0);uS.position.set(-560-500,0,-600);uS.target=UR;scene.add(uS);
const sunU=new THREE.Mesh(new THREE.SphereGeometry(1.2,16,12),new THREE.MeshBasicMaterial({color:0xfff2b0,toneMapped:false}));sunU.position.set(-530,6,-640);scene.add(sunU);const sunUG=glow(0xffd070,10,.9);sunUG.position.copy(sunU.position);scene.add(sunUG);
// ---------- PLAZA DE MADRID (s3 medianoche al sol · s4 noche polar)
const PZ=new THREE.Group();scene.add(PZ);
const tiles=new THREE.Mesh(new THREE.PlaneGeometry(200,200),new THREE.MeshStandardMaterial({color:0xd9c8a8,roughness:.95}));tiles.rotation.x=-Math.PI/2;tiles.receiveShadow=true;PZ.add(tiles);
for(let i=-6;i<=6;i++){const l=box(.08,.02,40,0xc4b292,.01);l.position.set(i*3,.01,0);PZ.add(l);const m=box(40,.02,.08,0xc4b292,.01);m.position.set(0,.01,i*3);PZ.add(m)}
const snowG=new THREE.Mesh(new THREE.PlaneGeometry(200,200),new THREE.MeshStandardMaterial({color:0xeef4ff,roughness:.85}));snowG.rotation.x=-Math.PI/2;snowG.position.y=.05;snowG.receiveShadow=true;PZ.add(snowG);
const WINS=[];const B=[];for(let i=0;i<7;i++){const h=8+R()*10,w=5+R()*3;const b=box(w,h,5,[0xe0b088,0xd8c0a0,0xc89878,0xe8d8c0][i%4],.1);b.position.set(-21+i*7,h/2,-16-R()*4);PZ.add(b);
 for(let y=2;y<h-1;y+=2.2)for(let x=-w/2+1;x<w/2-.6;x+=1.6){const wn=box(.8,1.2,.1,0x3a4a6a,.02,{emissive:0xffc860,emissiveIntensity:0});wn.position.set(b.position.x+x,y,b.position.z+2.55);PZ.add(wn);WINS.push(wn)}}
// reloj de la Puerta del Sol (inventado: torre de bloques con reloj)
const TW=new THREE.Group();TW.position.set(-8,0,-10);PZ.add(TW);{const t=box(4,13,4,0xe8dcc8,.06);t.position.y=6.5;TW.add(t);const tp=box(4.6,.6,4.6,0xb8a888,.04);tp.position.y=13.3;TW.add(tp);const cu=box(2,2,2,0x6a7a8a,.1);cu.position.y=14.6;TW.add(cu)}
const CK=wallClock(1.5);CK.g.position.set(0,10.5,2.05);TW.add(CK.g);
const clk=label3d(['*00:00'],{w:5.6,h:2.2,px:200,sprite:true});PZ.add(clk);
const panel=label3d(['MADRID · MEDIANOCHE','*SOL A 32°'],{w:4.8,h:2.1,px:110});panel.position.set(-.6,4.2,8);PZ.add(panel);const pp=box(.25,3.2,.25,0x30343e,.03);pp.position.set(-.6,1.6,7.9);PZ.add(pp);
const lamps=[];[[-4,6],[8,5],[-12,2]].forEach(([x,z])=>{const g=new THREE.Group();const p=box(.3,5,.3,0x2a2e38,.03);p.position.y=2.5;g.add(p);const h=box(.9,.6,.9,0xfff0c0,.05,{emissive:0xffd890,emissiveIntensity:0});h.position.y=5.2;g.add(h);g.userData.h=h;const L=new THREE.PointLight(0xffc870,0,18,1.6);L.position.y=4.8;g.add(L);g.userData.L=L;g.position.set(x,0,z);PZ.add(g);lamps.push(g)});
const trees=[];[[-9,6],[11,-7],[12,4]].forEach(([x,z])=>{const g=new THREE.Group();const tr=box(.7,3,.7,0x6a4a2a,.05);tr.position.y=1.5;g.add(tr);const lv=box(3.4,2.8,3.4,0x4fa84a,.3);lv.position.y=4;g.add(lv);g.userData.lv=lv;g.position.set(x,0,z);PZ.add(g);trees.push(g)});
const hero=capataz();hero.g.position.set(0,0,6);PZ.add(hero.g);
const S=sun(scene,{pos:[0,30,-30],span:30,power:2.8});
const skyDisc=new THREE.Mesh(new THREE.SphereGeometry(4,20,14),new THREE.MeshBasicMaterial({color:0xfff2b0,toneMapped:false,fog:false}));scene.add(skyDisc);const skyG=glow(0xffd070,26,.8);scene.add(skyG);
const ST3=stars(scene,900,{r0:150,r1:190,size:1.2,seed:8});
const SN=snow(scene,1400,[-30,30,30,-20,25],{size:.25});
const polar=label3d(['*80 DÍAS','SIN AMANECER'],{w:7,h:3,px:150,sprite:true,accent:'#9ad8ff'});PZ.add(polar);
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],m=mouthAt(t),k=ss(0,d,lt);
 const set=(s==='h'||s==='s2'||s==='cta')?'G':s==='s1'?'U':'Z';const night=s==='s4';
 GL.visible=ST.visible=sunB.visible=sunBG.visible=set==='G';UR.visible=ST2.visible=sunU.visible=sunUG.visible=set==='U';PZ.visible=set==='Z';
 skyDisc.visible=skyG.visible=set==='Z'&&!night;ST3.visible=set==='Z'&&night;SN.pts.visible=set==='Z'&&night;snowG.visible=night;
 S.intensity=set==='Z'&&!night?2.8:0;gS.intensity=set==='G'?3.4:0;uS.intensity=set==='U'?3.2:0;
 let p,q;
 if(set==='G'){scene.background=new THREE.Color(0x02030a);hemi.intensity=.12;
  let tl=23.5;if(s==='h')tl=23.5+(98-23.5)*ss(.9,3.0,lt);else tl=98;
  // eje en el plano x-y; con 98° el polo norte queda casi horizontal: lo giramos hacia el Sol (−x) en s2
  tilt.rotation.z=tl*D2R;tilt.rotation.y=0;glb.group.rotation.y=t*.35;
  ang.set([`*${Math.round(tl)}°`]);ang.position.set(8,12.5,4);ang.visible=s!=='s2';
  jun.visible=s==='s2'&&lt>.8;jun.position.set(0,-14.5,4);
  const la=Math.PI;gS.position.set(Math.cos(la)*560,0,-600);sunB.visible=sunBG.visible=s==='s2'||s==='cta';
  if(s==='h'){p=V3(Math.sin(t*.3)*1.5,-4,-516+k*4);q=V3(0,1.5,-600)}
  else if(s==='s2'){p=V3(-8+k*2,-4,-470+k*4);q=V3(-8,0,-600)}
  else{p=V3(0,-4,-512+k*3);q=V3(-1,1,-600)}}
 else if(set==='U'){scene.background=new THREE.Color(0x02030a);hemi.intensity=.1;U.tick(t);ut.rotation.z=98*D2R;ut.rotation.x=.25;
  p=V3(-500+Math.sin(t*.3)*2,-3,-522+k*5);q=V3(-500,0,-600)}
 else{const a=night?-20*D2R:MID*D2R;const az=Math.PI+Math.sin(t*.25)*.15;// cielo del norte (detrás de la cámara-izquierda)
  const az2=-.12+Math.sin(t*.25)*.05;const dir=V3(Math.sin(az2)*Math.cos(a),Math.sin(a),-Math.cos(az2)*Math.cos(a)).normalize();
  S.position.copy(dir.clone().multiplyScalar(40));S.target.position.set(0,0,4);S.target.updateMatrixWorld();
  skyDisc.position.copy(dir.clone().multiplyScalar(170));skyG.position.copy(skyDisc.position);
  scene.background=night?new THREE.Color(0x060a1c):new THREE.Color(0x8ad0ff);hemi.intensity=night?.28:.9;
  WINS.forEach((w,i)=>w.material.emissiveIntensity=night?((i*7)%5<3?1.4:0):0);lamps.forEach(g=>{g.userData.h.material.emissiveIntensity=night?2:0;g.userData.L.intensity=night?60:0});
  trees.forEach(g=>g.userData.lv.material.color.setHex(night?0xe8f0ff:0x4fa84a));
  if(night)SN.draw(t);
  CK.set(night?18+lt*.8:24+lt*.02);clk.visible=!night;clk.position.set(-8,17.6,-8);clk.set(['*00:00']);
  panel.visible=!night;polar.visible=night&&lt>.6;polar.position.set(0,9.5,2);
  hero.pose(t,m*.2,{look:night?.2:-.5,armsUp:night?0:.0,point:!night&&lt>1.5?.6:0,wave:0});hero.g.rotation.y=night?0:-.6;
  cam.fov=night?35:58;cam.updateProjectionMatrix();
  if(!night){p=V3(3-k*2,3.2,22-k*2);q=p.clone().add(V3(-.18,.45,-1))}
  else{p=V3(-3+k*3,7,36-k*2);q=V3(0,6,-2)}}
 if(set!=='Z'&&cam.fov!==35){cam.fov=35;cam.updateProjectionMatrix()}
 cam.position.copy(p);cam.lookAt(q);r.render(scene,cam)};
window.ready=true;
