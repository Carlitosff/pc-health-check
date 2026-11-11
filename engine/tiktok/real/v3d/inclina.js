// ¿Y si la Tierra se queda sin inclinación? (1904). Serie ¿QUÉ PASARÍA SI…? Parte 8.
// Reutilizable: globo con EJE visible que se endereza (tiltTo), línea día/noche (terminador) y rótulo de ángulo; PLAZA-RELOJ DE SOL: obelisco con su
// sombra real (luz direccional a la altura del sol), regla en el suelo para leer la sombra y panel 'MES · ÁNGULO'; polo con el sol rodando por el horizonte.
import {THREE,J,mk,ss,V3,clamp,stage,sun,box,glow,capataz,segAt,mouthAt,label3d,stars,voxGlobe,snow} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x02030a,fog:null,exposure:1.1});cam.far=2000;cam.updateProjectionMatrix();const R=mk(1904);
const hemi=new THREE.HemisphereLight(0xdcefff,0xb8a080,.5);scene.add(hemi);
const D2R=Math.PI/180;const ALT=J.alt||{jun:73.0,dic:26.2,eq:49.6};
// ---------- GLOBO (h, s1, s3, s4a)
const GL=new THREE.Group();GL.position.set(0,0,-600);scene.add(GL);const ST=stars(scene,1500,{r0:300,r1:360,size:1.4});ST.position.copy(GL.position);
const tilt=new THREE.Group();GL.add(tilt);const glb=voxGlobe(9000,10);tilt.add(glb.group);
const axis=new THREE.Mesh(new THREE.CylinderGeometry(.22,.22,30,12),new THREE.MeshBasicMaterial({color:0xffd23a,toneMapped:false}));tilt.add(axis);
[15,-15].forEach(y=>{const c=new THREE.Mesh(new THREE.SphereGeometry(.55,12,8),new THREE.MeshBasicMaterial({color:0xffd23a,toneMapped:false}));c.position.y=y;tilt.add(c)});
const eqR=new THREE.Mesh(new THREE.TorusGeometry(10.35,.12,8,120),new THREE.MeshBasicMaterial({color:0xff7a5a,toneMapped:false}));eqR.rotation.x=Math.PI/2;tilt.add(eqR);
const vert=new THREE.Mesh(new THREE.CylinderGeometry(.08,.08,32,8),new THREE.MeshBasicMaterial({color:0xffffff,transparent:true,opacity:.45,toneMapped:false}));GL.add(vert);
const ang=label3d(['*23,5°'],{w:8.5,h:3.2,px:170,sprite:true});GL.add(ang);
const gS=new THREE.DirectionalLight(0xfff4e0,3.2);gS.position.set(-560,0,-560);gS.target=GL;scene.add(gS);
// sol de referencia a la izquierda del globo
const sunB=new THREE.Mesh(new THREE.SphereGeometry(4,24,16),new THREE.MeshBasicMaterial({color:0xfff2b0,toneMapped:false}));sunB.position.set(-40,0,-600);scene.add(sunB);const sunBG=glow(0xffd070,26,.85);sunBG.position.copy(sunB.position);scene.add(sunBG);
const dn=label3d(['*12 h DÍA · 12 h NOCHE'],{w:14,h:2.2,px:120,sprite:true,accent:'#4ade80'});GL.add(dn);
// ---------- PLAZA-RELOJ DE SOL (s2, s3b, cta)
const PZ=new THREE.Group();scene.add(PZ);
const tiles=new THREE.Mesh(new THREE.PlaneGeometry(200,200),new THREE.MeshStandardMaterial({color:0xd9c8a8,roughness:.95}));tiles.rotation.x=-Math.PI/2;tiles.receiveShadow=true;PZ.add(tiles);
for(let i=-6;i<=6;i++){const l=box(.08,.02,40,0xc4b292,.01);l.position.set(i*3,.01,0);PZ.add(l);const m=box(40,.02,.08,0xc4b292,.01);m.position.set(0,.01,i*3);PZ.add(m)}
const ob=new THREE.Group();{const b=box(2.2,.6,2.2,0xb8b0a0,.06);b.position.y=.3;ob.add(b);const s=box(1.1,6,1.1,0xe8e0d0,.05);s.position.y=3.6;ob.add(s);const tp=new THREE.Mesh(new THREE.ConeGeometry(.78,1,4),new THREE.MeshStandardMaterial({color:0xffc23a,metalness:.4,roughness:.4}));tp.position.y=7.1;tp.rotation.y=Math.PI/4;tp.castShadow=true;ob.add(tp)}PZ.add(ob);
// regla de la sombra (hacia la cámara, +z): marcas cada 2 u
const rl=new THREE.Group();for(let i=0;i<=8;i++){const m=box(i%2?.7:1.3,.04,.14,0x10131f,.01);m.position.set(1.9,.03,i*2);rl.add(m)}const rb=box(.12,.03,16.2,0x10131f,.01);rb.position.set(1.9,.03,8);rl.add(rb);PZ.add(rl);
const H_OB=7.6;// altura hasta la punta
const tipM=glow(0xffd23a,1.6,.95);PZ.add(tipM);
const panel=label3d(['JUNIO','*73°'],{w:4.2,h:2.7,px:150});panel.position.set(-3.6,3.9,3);PZ.add(panel);const pp=box(.25,2.4,.25,0x30343e,.03);pp.position.set(-3.6,1.2,2.9);PZ.add(pp);
const B=[];for(let i=0;i<7;i++){const h=8+R()*10,w=5+R()*3;const b=box(w,h,5,[0xe0b088,0xd8c0a0,0xc89878,0xe8d8c0][i%4],.1);b.position.set(-21+i*7,h/2,-16-R()*4);PZ.add(b);for(let y=2;y<h-1;y+=2.2)for(let x=-w/2+1;x<w/2-.6;x+=1.6){const wn=box(.8,1.2,.1,0x3a4a6a,.02);wn.position.set(b.position.x+x,y,b.position.z+2.55);PZ.add(wn)}}
const trees=[];[[-9,6],[9,4],[-11,-6],[11,-7]].forEach(([x,z])=>{const g=new THREE.Group();const tr=box(.7,3,.7,0x6a4a2a,.05);tr.position.y=1.5;g.add(tr);const lv=box(3.4,2.8,3.4,0x4fa84a,.3);lv.position.y=4;g.add(lv);g.userData.lv=lv;g.position.set(x,0,z);PZ.add(g);trees.push(g)});
const hero=capataz();hero.g.position.set(3.4,0,6);PZ.add(hero.g);
const S=sun(scene,{pos:[0,30,-30],span:26,power:2.8});
const skyDisc=new THREE.Mesh(new THREE.SphereGeometry(3,20,14),new THREE.MeshBasicMaterial({color:0xfff2b0,toneMapped:false,fog:false}));scene.add(skyDisc);const skyG=glow(0xffd070,22,.8);scene.add(skyG);
// ---------- POLO (s4 2ª mitad): hielo y sol rodando pegado al horizonte
const PO=new THREE.Group();PO.position.set(800,0,0);scene.add(PO);
const ice=new THREE.Mesh(new THREE.PlaneGeometry(400,400),new THREE.MeshStandardMaterial({color:0xe8f2ff,roughness:.8}));ice.rotation.x=-Math.PI/2;ice.receiveShadow=true;PO.add(ice);
for(let i=0;i<30;i++){const s=1+R()*3;const b=box(s,s*.6,s,0xd8e8fa,.2);b.position.set((R()-.5)*60,s*.3,-8-R()*40);PO.add(b)}
const pole=box(.3,4,.3,0xd02a2a,.03);pole.position.set(3.2,2,-2);PO.add(pole);const flag=label3d(['POLO NORTE'],{w:3.4,h:1,px:110,accent:'#ff5a4a'});const hz=label3d(['*SOL EN EL HORIZONTE','TODO EL AÑO'],{w:7,h:2.2,px:110,sprite:true});hz.position.set(0,9.5,-6);PO.add(hz);flag.position.set(3.2,4.3,-2);PO.add(flag);
const hero2=capataz();hero2.g.position.set(-2.4,0,-1);PO.add(hero2.g);
const poS=new THREE.DirectionalLight(0xffc890,2.2);poS.castShadow=true;poS.shadow.mapSize.set(1024,1024);Object.assign(poS.shadow.camera,{left:-20,right:20,top:20,bottom:-20,far:200});poS.target=PO;scene.add(poS);
const poSun=new THREE.Mesh(new THREE.SphereGeometry(5,20,14),new THREE.MeshBasicMaterial({color:0xffd890,toneMapped:false,fog:false}));PO.add(poSun);const poG=glow(0xff9a50,40,.8);PO.add(poG);
const MON=['ENE','FEB','MAR','ABR','MAY','JUN','JUL','AGO','SEP','OCT','NOV','DIC'];
const t1=TL.s1[0],t2=TL.s2[0],t3=TL.s3[0],t4=TL.s4[0],tC=TL.cta[0];
// altura del sol en la plaza: s2 recorre el año real (junio → diciembre), s3 se queda en 49,6° todo el año
const altNow=(s,lt,d)=>{if(s==='s2'){const k=ss(.3,d*.45,lt)-ss(d*.5,d*.95,lt)*0;const a=ss(.3,d*.45,lt),b=ss(d*.55,d*.95,lt);return b>0?ALT.jun+(ALT.dic-ALT.jun)*b:ALT.eq+(ALT.jun-ALT.eq)*a}if(s==='cta'||s==='s3')return ALT.eq;return ALT.eq};
const month=(s,lt,d)=>{if(s==='s2'){const b=ss(d*.55,d*.95,lt);return b>.02?(b>.98?'DICIEMBRE':MON[(5+Math.round(b*6))%12]):'JUNIO'}if(s==='s3'||s==='cta')return MON[Math.floor((lt*2.2))%12];return 'MARZO'};
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],m=mouthAt(t);
 // qué set: h/s1 globo · s2 plaza · s3: globo (endereza) 0–40 % y plaza · s4: globo 0–50 % y polo · cta plaza
 const s3g=s==='s3'&&lt<d*.4,s4g=s==='s4'&&lt<d*.5;
 const set=(s==='h'||s==='s1'||s3g||s4g)?'G':(s==='s4')?'P':'Z';
 GL.visible=ST.visible=sunB.visible=sunBG.visible=set==='G';PZ.visible=skyDisc.visible=skyG.visible=set==='Z';PO.visible=set==='P';
 S.intensity=set==='Z'?2.8:0;gS.intensity=set==='G'?3.4:0;poS.intensity=set==='P'?2.4:0;
 let p,q;
 if(set==='G'){scene.background=new THREE.Color(0x02030a);hemi.intensity=.18;
  let tl=23.5;if(s==='s3')tl=23.5*(1-ss(d*.08,d*.32,lt));if(s==='s4')tl=0;
  tilt.rotation.z=-tl*D2R;glb.group.rotation.y=t*.35;
  ang.set([tl<.05?'*0°':`*${tl.toFixed(1).replace('.',',')}°`]);ang.position.set(6.5,13.5,4);
  dn.visible=s==='s4';dn.position.set(0,-14.5,4);
  // sol a la izquierda; en s1 el globo da la vuelta alrededor (estaciones): se cambia el lado iluminado
  let la=s==='s4'?Math.PI:Math.PI*.72;if(s==='s1')la=Math.PI+ss(.5,d-.3,lt)*Math.PI;
  const sg=1;gS.position.set(Math.cos(la)*560,s==='s4'||s==='s1'?0:120,-600+sg*Math.sin(la)*560);sunB.position.set(Math.cos(la)*40,0,-600+Math.sin(la)*40);sunBG.position.copy(sunB.position);
  sunB.visible=sunBG.visible=s==='s1';
  const k=ss(0,d,lt);
  if(s==='h'){p=V3(0,-4+k*1.5,-524-k*3);q=V3(0,4.5,-600)}
  else if(s==='s1'){p=V3(0,-6,-525);q=V3(0,1,-600)}
  else if(s==='s3'){p=V3(2-k*2,-4,-527+k*2);q=V3(0,4.5,-600)}
  else{p=V3(0,-4,-526-k*3);q=V3(0,4,-600)}}
 else if(set==='Z'){const a=altNow(s,lt,d)*D2R;const az=s==='cta'?0:Math.sin(t*.3)*.12;
  const dir=V3(Math.sin(az)*Math.cos(a),Math.sin(a),-Math.cos(az)*Math.cos(a));
  S.position.copy(dir.clone().multiplyScalar(40));S.target.position.set(0,0,4);S.target.updateMatrixWorld();
  skyDisc.position.copy(dir.clone().multiplyScalar(160));skyG.position.copy(skyDisc.position);
  const day=new THREE.Color(0x8ad0ff);scene.background=day;hemi.intensity=.9;
  const deg=Math.round(a/D2R);panel.set([month(s,lt,d),`*${deg}°`]);
  tipM.position.set(0,.06,H_OB/Math.tan(a)*Math.cos(az));tipM.visible=true;
  trees.forEach(g=>{g.userData.lv.material.color.setHex(s==='s2'&&lt>d*.6?0xc8892a:0x4fa84a)});
  hero.pose(t,m*.2,{wave:s==='cta'?1:0,look:-.3,point:s==='s2'&&lt>d*.5?.5:0});
  const k=ss(0,d,lt);
  if(s==='s2'){p=V3(10-k*3,16,30);q=V3(0,3,4)}
  else if(s==='s3'){p=V3(-8+k*4,14,31);q=V3(0,3,4)}
  else{p=V3(6-k*4,13+k,32);q=V3(0,3.5,3)}}
 else{scene.background=new THREE.Color(0x7a9ad8).lerp(new THREE.Color(0xffb080),.3);hemi.intensity=1.15;
  const az=-.22+.44*ss(d*.5,d,lt);const sp=V3(Math.sin(az)*120,4,-Math.cos(az)*120);poSun.position.copy(sp);poG.position.copy(sp);
  poS.position.copy(PO.position.clone().add(V3(Math.sin(az)*60,6,-Math.cos(az)*60)));poS.target.updateMatrixWorld();
  hero2.pose(t,m*.2,{look:Math.sin(az)*.6,armsUp:.15});
  const k=ss(0,d*.5,lt-d*.5);p=V3(800+1,6,25-k*3);q=V3(800,6,-20)}
 cam.position.copy(p);cam.lookAt(q);r.render(scene,cam)};
window.ready=true;
