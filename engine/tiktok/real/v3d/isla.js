// ¿Y si saltamos todos en Mallorca? (1404). Serie ¿QUÉ PASARÍA SI…? Parte 3. Reutilizable: isla de cubos por polígono, plaza abarrotada, globo y pista de aeropuerto con cola infinita.
import {THREE,J,mk,ss,V3,clamp,stage,sun,box,glow,pixTex,capataz,segAt,mouthAt,crowd} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x6fbdf2,fog:[0x9fd3f5,90,330],exposure:1.1});const R=mk(1404);
scene.add(new THREE.HemisphereLight(0xdcefff,0x4a6a50,1.0));const S=sun(scene,{pos:[-30,70,40],span:60,power:2.4});const O=new THREE.Object3D(),CC=new THREE.Color();
// --- isla por polígono (lon,lat aproximados de la costa de Mallorca)
const COAST=[[2.32,39.60],[2.38,39.54],[2.52,39.46],[2.60,39.53],[2.70,39.55],[2.74,39.42],[2.86,39.36],[3.05,39.27],[3.18,39.33],[3.27,39.42],[3.37,39.53],[3.47,39.71],[3.31,39.75],[3.17,39.74],[3.11,39.80],[3.17,39.87],[3.21,39.96],[3.08,39.91],[3.02,39.86],[2.80,39.86],[2.68,39.80],[2.58,39.74],[2.42,39.64]];
const inP=(x,y)=>{let c=false;for(let i=0,j=COAST.length-1;i<COAST.length;j=i++){const[a,b]=COAST[i],[e,f]=COAST[j];if((b>y)!=(f>y)&&x<(e-a)*(y-b)/(f-b)+a)c=!c}return c};
const isl=new THREE.Group();scene.add(isl);const CELL=.72,cells=[];const lon0=2.9,lat0=39.62,LON=(.77/.0098)*CELL,LAT=(1/.0098)*CELL;
for(let i=-70;i<=70;i++)for(let k=-70;k<=70;k++){const x=i*CELL,z=k*CELL;const lo=lon0+x/LON,la=lat0-z/LAT;if(inP(lo,la)){const d=(()=>{let m=9;for(let a=0;a<COAST.length;a++){const[b,c]=COAST[a];m=Math.min(m,Math.hypot(b-lo,c-la))}return m})();
 const nw=clamp(((la-39.55)-(lo-2.45)*.55)/.32);const mnt=Math.pow(nw,2.2)*5.2*(.75+.25*Math.sin(x*.7)*Math.cos(z*.9));cells.push({x,z,h:.5+mnt+Math.sin(x*.5+z*.4)*.15,d,g:R()})}}
const NC=cells.length,tm=new THREE.InstancedMesh(new THREE.BoxGeometry(CELL,1,CELL),new THREE.MeshStandardMaterial({roughness:.9}),NC);tm.frustumCulled=false;tm.receiveShadow=true;tm.castShadow=true;isl.add(tm);
cells.forEach((c,i)=>{O.position.set(c.x,c.h/2-.4,c.z);O.scale.set(1,c.h+.4,1);O.updateMatrix();tm.setMatrixAt(i,O.matrix);CC.setHex(c.h>3.8?0x9a9a92:c.h>1.6?0x4f8a4a:c.d<.016?0xf2dfae:0x74b558);CC.multiplyScalar(.92+c.g*.14);tm.setColorAt(i,CC)});O.scale.set(1,1,1);
const tiny=crowd(scene,NC,{seed:11,s:.2});
function drawTiny(t,on,jump){for(let i=0;i<NC;i++){const c=cells[i];const k=ss(c.g*.9,c.g*.9+.1,on)*.36;const w=Math.max(0,Math.sin(clamp((t-jump-c.x*.012)*2.2)*Math.PI))*1.6;tiny.set(i,c.x,c.h-.4+(on>0?w:0)-(k<=0?9:0),c.z,Math.max(k,.001))}tiny.done()}
const seaI=(()=>{const m=new THREE.Mesh(new THREE.PlaneGeometry(1200,1200,1,1),new THREE.MeshStandardMaterial({color:0x1677c8,roughness:.25,metalness:.15}));m.rotation.x=-Math.PI/2;m.position.y=-.35;scene.add(m);return m})();
const SN=2200,sp=new THREE.InstancedMesh(new THREE.BoxGeometry(.9,.12,.9),new THREE.MeshBasicMaterial({color:0xd6f3ff,transparent:true,opacity:.5,toneMapped:false}),SN);sp.frustumCulled=false;isl.add(sp);const SP=[];for(let i=0;i<SN;i++){let x,z;do{x=(R()-.5)*180;z=(R()-.5)*160}while(cells.some(c=>Math.abs(c.x-x)<1&&Math.abs(c.z-z)<1)&&i%2);SP.push([x,z,R()*6])}
function drawSp(t){SP.forEach((p,i)=>{const s=Math.sin(t*1.4+p[2]);O.position.set(p[0],-.3,p[1]);O.scale.setScalar(s>.55?(s-.55)*2.4:.001);O.updateMatrix();sp.setMatrixAt(i,O.matrix)});O.scale.set(1,1,1);sp.instanceMatrix.needsUpdate=true}
// --- plaza abarrotada (a un lado del mundo: x=600)
const PX=600,pl=new THREE.Group();pl.position.set(PX,0,0);scene.add(pl);const floorT=pixTex(256,256,(g,w,h)=>{g.fillStyle='#b9b09c';g.fillRect(0,0,w,h);g.strokeStyle='#8c8472';g.lineWidth=6;for(let i=0;i<=8;i++){g.beginPath();g.moveTo(i*32,0);g.lineTo(i*32,h);g.stroke();g.beginPath();g.moveTo(0,i*32);g.lineTo(w,i*32);g.stroke()}},[12,12]);const fl=new THREE.Mesh(new THREE.PlaneGeometry(96,96),new THREE.MeshStandardMaterial({map:floorT,roughness:.95}));fl.rotation.x=-Math.PI/2;fl.receiveShadow=true;pl.add(fl);
const PN=1400,pc=crowd(scene,PN,{seed:21,s:1});const PP=[];const SQ=4.2;for(let i=0;i<PN;i++){const a=i*2.39996,rd=SQ+.5+Math.sqrt(i)*.74;PP.push([PX+Math.cos(a)*rd,Math.sin(a)*rd*.95,R()*6.28,R()])}
const hero=capataz();hero.g.position.set(PX-1.1,0,.2);scene.add(hero.g);const mate=crowd(scene,1,{seed:5,s:1});
const sq=new THREE.Mesh(new THREE.RingGeometry(SQ*.71,SQ*.71+.22,4),new THREE.MeshBasicMaterial({color:0xffe25a,toneMapped:false}));sq.rotation.set(-Math.PI/2,0,Math.PI/4);sq.position.set(PX,.08,0);scene.add(sq);
function drawPlaza(t,jump){for(let i=0;i<PN;i++){const p=PP[i];const w=Math.max(0,Math.sin(clamp((t-jump-p[3]*.08)/.62)*Math.PI))*2.8;pc.set(i,p[0],w+Math.abs(Math.sin(t*2+p[2]))*.05,p[1],1,Math.sin(t*.5+p[2])*.5)}pc.done();const w=Math.max(0,Math.sin(clamp((t-jump)/.62)*Math.PI))*2.8;hero.g.position.y=w;mate.set(0,PX+1.3,w,.1,1,-.3);mate.done()}
// --- globo
const G=new THREE.Group();G.position.set(-600,0,0);scene.add(G);const noise=(x,y,z)=>Math.sin(x*3.1+1.3)*Math.cos(y*3.7-.7)+Math.sin(y*2.9+z*4.3)*.8+Math.cos(z*3.3-x*2.7+2)*.7;const NG=8000,gi=new THREE.InstancedMesh(new THREE.BoxGeometry(.58,.58,.58),new THREE.MeshStandardMaterial({roughness:.65}),NG);gi.frustumCulled=false;G.add(gi);for(let i=0;i<NG;i++){const y=1-2*(i+.5)/NG,rd=Math.sqrt(1-y*y),a=i*Math.PI*(3-Math.sqrt(5));const x=Math.cos(a)*rd,z=Math.sin(a)*rd,l=noise(x,y,z)>.55;const g=10+(l?.2:0);O.position.set(x*g,y*g,z*g);O.lookAt(0,0,0);O.updateMatrix();gi.setMatrixAt(i,O.matrix);O.rotation.set(0,0,0);CC.setHex(Math.abs(y)>.86?0xf2f8ff:l?0x58a84a:(i%2?0x1467c8:0x0c4fae));gi.setColorAt(i,CC)}
const NS=1400,spos=new Float32Array(NS*3);for(let i=0;i<NS;i++){spos[i*3]=-600+(R()-.5)*260;spos[i*3+1]=(R()-.5)*300;spos[i*3+2]=-70-R()*40}const sg=new THREE.BufferGeometry();sg.setAttribute('position',new THREE.BufferAttribute(spos,3));const stars=new THREE.Points(sg,new THREE.PointsMaterial({color:0xe4eaff,size:.5,fog:false}));scene.add(stars);
const dot=glow(0xff4030,7,.95);dot.material.fog=false;dot.material.depthTest=false;dot.position.set(3.5,4.9,8.6);G.add(dot);
// --- pista: avión de cubos y cola infinita (x=1400)
const AX=1400,rw=new THREE.Group();rw.position.set(AX,0,0);scene.add(rw);const tar=new THREE.Mesh(new THREE.PlaneGeometry(400,400),new THREE.MeshStandardMaterial({color:0x4a4e58,roughness:.95}));tar.rotation.x=-Math.PI/2;tar.receiveShadow=true;rw.add(tar);for(let i=0;i<30;i++){const m=box(.6,.04,3,0xf0efe6,.01);m.position.set(16,.03,20-i*8);rw.add(m)}
function plane(){const g=new THREE.Group();const b=box(3.4,3.4,20,0xf4f4f6,.8);b.position.y=3.2;g.add(b);const n=box(3,2.6,3,0xf4f4f6,.9);n.position.set(0,3.1,-11);g.add(n);const w=box(26,.4,4.5,0xdfe3ea,.1);w.position.set(0,2.6,0);g.add(w);const tf=box(.5,4.6,3.2,0xe5343f,.1);tf.position.set(0,6.6,8.8);g.add(tf);const ts=box(9,.3,2.4,0xdfe3ea,.08);ts.position.set(0,4.6,9.4);g.add(ts);[-7,7].forEach(x=>{const e=box(1.7,1.7,3.2,0x5a6070,.2);e.position.set(x,1.5,-.6);g.add(e)});for(let i=0;i<9;i++)[-1,1].forEach(s=>{const v=box(.06,.6,.8,0x223044,.02);v.position.set(s*1.72,3.9,-7+i*1.8);g.add(v)});return g}
const pln=plane();pln.rotation.y=Math.PI;rw.add(pln);for(let i=0;i<14;i++){const h=box(46,10+Math.sin(i*1.7)*6+i%3*3,14,0x7d9ab0,.5);h.position.set(-180+i*30,3,215);rw.add(h)}
const QN=1800,COLS=6,qc=crowd(scene,QN,{seed:33,s:1});const qx=row=>AX-2+Math.sin(row*.05)*row*.12;
function drawQueue(t){const adv=(t*.7)%1;for(let i=0;i<QN;i++){const col=i%COLS,row=Math.floor(i/COLS)+3-adv;qc.set(i,qx(row)+(col-2.5)*1.45+Math.sin(i*7.3)*.2,Math.abs(Math.sin(t*4+i))*.05,row*1.65,1,Math.PI+Math.sin(i)*.3)}qc.done()}
const bag=box(1,1.3,.5,0xe5343f,.08);bag.position.set(AX-.6,.65,3.2);bag.visible=false;scene.add(bag);
// panel de llegadas
const pc2=document.createElement('canvas');pc2.width=512;pc2.height=256;const pg=pc2.getContext('2d');pg.fillStyle='#07101c';pg.fillRect(0,0,512,256);pg.fillStyle='#ffc23a';pg.font='900 46px monospace';pg.fillText('SALIDAS',20,56);pg.fillStyle='#fff';pg.font='700 34px monospace';['TU VUELO   EN 485 AÑOS','MADRID     EN 485 AÑOS','BOGOTÁ     EN 485 AÑOS','CDMX       EN 485 AÑOS'].forEach((s,i)=>pg.fillText(s,20,108+i*42));const pt=new THREE.CanvasTexture(pc2);pt.colorSpace=THREE.SRGBColorSpace;
const board=new THREE.Group();const brd=new THREE.Mesh(new THREE.BoxGeometry(11,5.5,.2),new THREE.MeshBasicMaterial({map:pt,toneMapped:false}));board.add(brd);const bfr=box(11.5,6,.1,0x20243c,.05);bfr.position.z=-.14;board.add(bfr);[-4,4].forEach(x=>{const l=box(.3,6,.3,0x30344a,.03);l.position.set(x,-5,-.1);board.add(l)});board.scale.setScalar(.72);board.rotation.y=Math.PI+.15;board.position.set(-6.5,6.2,30);rw.add(board);
hero.pose(0,0);
const SKY=new THREE.Color(0x6fbdf2),SPACE=new THREE.Color(0x02030c);
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],m=mouthAt(t);const js=TL.s2[0]+1.55;let p,q;
 scene.background=SKY;drawSp(t);
 if(s==='h'){const k=ss(0,d,lt);drawTiny(t,clamp(.25+lt/(d*.8)),999);p=V3(3,128-k*14,112-k*14);q=V3(3,-16,-2)}
 else if(s==='s1'){drawPlaza(t,999);hero.pose(t,m,{look:.2});p=V3(PX+2+Math.sin(t*.5)*.6,24-lt*.5,23-lt*.5);q=V3(PX,-1.2,-4.5)}
 else if(s==='s2'){if(t<js+1.25){drawPlaza(t,js);const up=ss(js-.7,js,t);hero.pose(t,m,{armsUp:up,look:0});const k=clamp(lt/2);p=V3(PX+.2,20-k*3,24-k*3);q=V3(PX,1.2,-2)}else{scene.background=SPACE;const k=t-js-1.25;G.rotation.y=Math.sin(t*.25)*.12;p=V3(-600+Math.sin(t*.4)*1.2,-6,50-k*.9);q=V3(-600,3.5,0)}}
 else if(s==='s3'){drawPlaza(t,999);hero.pose(t,m,{look:-.2+Math.sin(t*1.3)*.5});const k=ss(0,d,lt);p=V3(PX+.4,7+k*30,16+k*16);q=V3(PX,1.8+k*-7,0)}
 else{drawQueue(t);const tk=((t-TL.s4[0])%5.6)/5.6;const v=Math.pow(ss(.1,1,tk),2);pln.position.set(13,ss(.4,1,tk)*46,62+v*190);pln.rotation.x=-ss(.35,.5,tk)*.16;if(s==='s4'){const k=ss(0,d,lt);p=V3(AX+5.5,15-k*3,-16-k*3);q=V3(AX+1,3,50)}else{hero.pose(t,m,{look:0});hero.g.position.set(AX-2.2,0,1.6);hero.g.rotation.y=Math.PI-.12;bag.position.set(AX-.2,.65,2.2);p=V3(AX-2+Math.sin(t*.5)*.5,7,-34);q=V3(AX-2,2.5,3)}}
 pl.visible=fl.visible=pc.body.visible=pc.head.visible=mate.body.visible=mate.head.visible=sq.visible=['s1','s2','s3'].includes(s)&&!(s==='s2'&&t>=js+1.25);
 hero.g.visible=pl.visible||s==='cta';bag.visible=s==='cta';if(s==='s1'||s==='s3'||s==='s2'){hero.g.position.x=PX-1.1;hero.g.position.z=.2;hero.g.rotation.y=0}
 isl.visible=tiny.body.visible=tiny.head.visible=s==='h';seaI.visible=s==='h';
 G.visible=stars.visible=dot.visible=(s==='s2'&&t>=js+1.25);dot.material.opacity=.7+.3*Math.sin(t*6);
 rw.visible=qc.body.visible=qc.head.visible=(s==='s4'||s==='cta');
 scene.fog.near=s==='h'?260:70;scene.fog.far=s==='h'?700:(s==='s4'||s==='cta'?230:300);S.target.position.copy(q);S.position.set(q.x-30,70,q.z+40);S.target.updateMatrixWorld();
 cam.position.copy(p);cam.lookAt(q);r.render(scene,cam)};
window.ready=true;
