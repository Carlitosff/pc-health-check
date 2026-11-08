// ¿Qué color queda enfrente del rojo? (1602). Plantilla de cubo que se pliega de verdad (bisagras anidadas, mismo árbol que el assert de Python).
// Reutilizable: foldNet() en bloques.js (v19). Mesa-taller de bloques, capataz que señala, eje luminoso rojo-verde en la revelación.
import {THREE,J,mk,ss,V3,clamp,stage,sun,box,glow,pixTex,capataz,segAt,mouthAt,puffs,label3d,foldNet} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x2a2f4a,fog:[0x2a2f4a,40,120],exposure:1.1});const R=mk(1602);
scene.add(new THREE.HemisphereLight(0xe8eeff,0x40384a,1.25));const S=sun(scene,{pos:[-10,30,16],span:22});
// suelo de taller: tablones
const wood=pixTex(128,128,(g,w,h)=>{const q=mk(4);for(let y=0;y<h;y+=16){g.fillStyle=['#8a5a32','#7d5030','#956238'][Math.floor(q()*3)];g.fillRect(0,y,w,16);g.fillStyle='rgba(0,0,0,.18)';g.fillRect(0,y+14,w,2);for(let i=0;i<6;i++){g.fillStyle='rgba(60,30,10,.25)';g.fillRect(q()*w,y+3+q()*9,10+q()*30,2)}}},[6,6]);
const gnd=new THREE.Mesh(new THREE.PlaneGeometry(120,120),new THREE.MeshStandardMaterial({map:wood,roughness:.9}));gnd.rotation.x=-Math.PI/2;gnd.receiveShadow=true;scene.add(gnd);
// cuadrícula de corte (tapete verde de taller) bajo la plantilla
const mat=pixTex(256,256,(g,w,h)=>{g.fillStyle='#1f6b52';g.fillRect(0,0,w,h);g.strokeStyle='rgba(255,255,255,.22)';g.lineWidth=2;for(let i=0;i<=w;i+=16){g.beginPath();g.moveTo(i,0);g.lineTo(i,h);g.stroke();g.beginPath();g.moveTo(0,i);g.lineTo(w,i);g.stroke()}},[2,2]);
const tap=new THREE.Mesh(new THREE.BoxGeometry(15,.16,19),new THREE.MeshStandardMaterial({map:mat,roughness:.85}));tap.position.y=.08;tap.receiveShadow=true;scene.add(tap);
// la plantilla: J.net=[[col,row],...], J.cols=['#hex',...], J.base=índice de la cara que no se mueve
const SZ=2.6;const N=foldNet(J.net,J.cols,J.base,SZ);
// la plantilla gira -90° en y para que su lado largo vaya en vertical en el móvil
const holder=new THREE.Group();holder.rotation.y=-Math.PI/2;scene.add(holder);
const spinG=new THREE.Group();holder.add(spinG);spinG.add(N.root);
const bc=J.net[J.base],c0=J.net.reduce((a,c)=>[a[0]+c[0]/6,a[1]+c[1]/6],[0,0]);
// centro de la plantilla en el origen; spinG en el centro del cubo plegado (gira y sube desde ahí)
const RP=V3((bc[0]-c0[0])*SZ,.24,(bc[1]-c0[1])*SZ);const CC=RP.clone().add(V3(0,SZ/2,0));spinG.position.copy(CC);N.root.position.copy(RP).sub(CC);
const RED=J.red,ANS=J.answer;
// rótulos integrados: '?' encima del rojo y respuesta
const QL=label3d(['*?'],{w:2.6,h:2.6,px:760,bg:'',accent:'#ff3a4a',sprite:true});scene.add(QL);
const AL=label3d(['*ENFRENTE','DEL ROJO'],{w:5.4,h:2.2,px:120,sprite:true});scene.add(AL);AL.visible=false;
// eje luminoso entre las dos caras opuestas
const axis=new THREE.Mesh(new THREE.CylinderGeometry(.09,.09,1,10),new THREE.MeshBasicMaterial({color:0xfff2a0,toneMapped:false,transparent:true}));scene.add(axis);axis.visible=false;
const gR=glow(0xff3a4a,4,.9),gA=glow(0x4ade80,4,.9);scene.add(gR,gA);
const hero=capataz();hero.g.position.set(4.4,0,4.6);hero.g.scale.setScalar(.95);scene.add(hero.g);
const dust=puffs(scene,60,.16,0xfff0c0,{opacity:.9,depthWrite:false});const dp=[];for(let i=0;i<60;i++)dp.push([R()*6.28,R(),R()]);
const wpos=i=>{const v=new THREE.Vector3();N.faces[i].mesh.getWorldPosition(v);return v};
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],m=mouthAt(t);let p,q;
 // plegado: s3 entero (escalonado por profundidad); fuera de s3, plano antes y cerrado después
 let f=0;if(s==='s3')f=ss(.4,d-.2,lt);else if(s==='s4'||s==='cta')f=1;N.fold(f);
 // tras plegar: el cubo se eleva y gira para enseñar el rojo y luego su cara opuesta
 const lift=s==='s4'?ss(0,1,lt)*3.2:s==='cta'?3.2:0;let spin=0;if(s==='s4')spin=ss(.7,d*.42,lt)*Math.PI+ss(d*.55,d*.85,lt)*Math.PI;else if(s==='cta')spin=2*Math.PI+lt*.35;
 spinG.position.set(CC.x,CC.y+lift,CC.z);spinG.rotation.set(0,spin,0);holder.updateMatrixWorld(true);const ctr=CC.clone().add(V3(0,lift,0));
 const pr=wpos(RED),pa=wpos(ANS);
 QL.position.copy(pr).add(V3(-2.9,1.2+.15*Math.sin(t*4),.2));QL.visible=s!=='s4'&&s!=='cta';QL.material.opacity=s==='s3'?1-ss(.2,.9,lt):1;
 const showAx=s==='s4'&&lt>d*.3||s==='cta';axis.visible=gR.visible=gA.visible=showAx;
 if(showAx){const mid=pr.clone().add(pa).multiplyScalar(.5);const L=pr.distanceTo(pa)+2.2;axis.position.copy(mid);axis.scale.set(1,L,1);axis.quaternion.setFromUnitVectors(V3(0,1,0),pa.clone().sub(pr).normalize());axis.material.opacity=.55+.35*Math.sin(t*6);
  const dir=pa.clone().sub(pr).normalize();gR.position.copy(pr).addScaledVector(dir,-1.15);gA.position.copy(pa).addScaledVector(dir,1.15);gR.scale.setScalar(3.4+.5*Math.sin(t*5));gA.scale.setScalar(3.4+.5*Math.cos(t*5))}
 AL.visible=false;if(AL.visible){const cw=holder.localToWorld(ctr.clone());AL.position.copy(cw).add(V3(0,-3.6,2.4))}
 // chispas al cerrarse cada bisagra
 if(s==='s3'){const kk=ss(d*.78,d*.98,lt);for(let i=0;i<60;i++){const[a,b,c]=dp[i];const rr=.5+kk*(2+b*3);const cw=holder.localToWorld(ctr.clone());dust.set(i,cw.x+Math.cos(a)*rr,cw.y+(c-.5)*SZ+kk*b*1.2,cw.z+Math.sin(a)*rr,kk>0&&kk<1?(1-kk)*(.7+b):0)}dust.done()}else{for(let i=0;i<60;i++)dust.set(i,0,-50,0,0);dust.done()}
 // capataz: señala el rojo en la pregunta, aplaude/saluda al final
 hero.pose(t,m,{point:s==='s1'||s==='s2'?1:0,wave:s==='cta'?1:0,armsUp:s==='s4'&&lt>d*.6?.6:0,look:-.5+Math.sin(t*.6)*.15});hero.g.rotation.y=-.75;
 // cámara: casi cenital y quieta en la pregunta (la imagen tiene que ser exacta); se mueve al plegar
 if(s==='h'){const e=ss(0,d,lt);p=V3(.5,31-e*1.2,7.6-e*.3);q=V3(.5,0,-4.3)}
 else if(s==='s1'||s==='s2'){const e=ss(0,d,lt);p=V3(.5,29.8-e*.6,7.3-e*.2);q=V3(.5,0,-4.3)}
 else if(s==='s3'){const e=ss(0,d,lt);const a=e*1.1;p=V3(Math.sin(a)*15,22-e*11,Math.cos(a)*15*.5+7*(1-e)+e*6);q=V3(0,e*1.5,-.4)}
 else if(s==='s4'){const e=ss(0,d,lt);p=V3(4+e*2,10+e*1.5,15-e*1);q=V3(0,3.6+e*.6,0)}
 else{const e=ss(0,d,lt);p=V3(6-e*2,9+e*1.5,17+e*1);q=V3(1.5,3.8,-1)}
 p.x+=Math.sin(t*.5)*(s==='s1'||s==='s2'||s==='h'?0:.25);
 S.target.position.set(0,0,0);S.target.updateMatrixWorld();
 cam.position.copy(p);cam.lookAt(q);r.render(scene,cam)};
window.ready=true;
