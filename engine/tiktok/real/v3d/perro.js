// Mito '¿tu perro pone cara de culpable porque sabe que lo ha hecho mal?' (3503). Fuentes en mito_perro.py (Horowitz, Behavioural Processes 2009).
// Reutilizable: PERRO de bloques (dog() en bloques.js, con 'cara de culpable' graduable), SALÓN de día con sofá, cojín destrozado y relleno,
// puerta que se abre, plato con GALLETA en forma de hueso, investigadora (abuela) que se lleva la galleta, dueña (capataz) que riñe o acaricia.
import {THREE,J,mk,ss,V3,clamp,stage,sun,box,glow,pixTex,capataz,abuela,segAt,mouthAt,puffs,sofa,dog,label3d} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0xf2e6d2,exposure:1.12});const R=mk(3503);
const hemi=new THREE.HemisphereLight(0xfff4e4,0x8a7060,1.0);scene.add(hemi);const S=sun(scene,{pos:[10,24,16],span:24,power:2.0});
const wood=pixTex(64,64,(g,w,h)=>{g.fillStyle='#b88452';g.fillRect(0,0,w,h);g.fillStyle='#a8743f';for(let y=0;y<h;y+=8)g.fillRect(0,y,w,2);g.fillStyle='#c8945e';for(let i=0;i<40;i++)g.fillRect((i*37)%w,(i*23)%h,6,1)},[14,14]);
const fl=new THREE.Mesh(new THREE.PlaneGeometry(120,120),new THREE.MeshStandardMaterial({map:wood,roughness:.75}));fl.rotation.x=-Math.PI/2;fl.receiveShadow=true;scene.add(fl);
const wp=pixTex(64,64,(g,w,h)=>{g.fillStyle='#7fb8b0';g.fillRect(0,0,w,h);g.fillStyle='#8cc4bc';for(let x=0;x<w;x+=16)g.fillRect(x,0,7,h)},[12,5]);
const wall=new THREE.Mesh(new THREE.PlaneGeometry(80,30),new THREE.MeshStandardMaterial({map:wp,roughness:.9}));wall.position.set(0,15,-9);wall.receiveShadow=true;scene.add(wall);
const skirt=box(80,.6,.3,0xf4efe6,.03);skirt.position.set(0,.3,-8.85);scene.add(skirt);
// ventana con sol
const win=new THREE.Mesh(new THREE.PlaneGeometry(6,5),new THREE.MeshBasicMaterial({color:0x9fd8ff,toneMapped:false}));win.position.set(-8,9,-8.95);scene.add(win);
[[-8,11.6,6.6,.35],[-8,6.4,6.6,.35],[-11.15,9,.35,5.6],[-4.85,9,.35,5.6],[-8,9,.25,5]].forEach(([x,y,w,h])=>{const f=box(w,h,.25,0xf4efe6,.03);f.position.set(x,y,-8.85);scene.add(f)});
// puerta (bisagra en x=9.5)
const doorF=box(4.6,8.4,.3,0xf4efe6,.03);doorF.position.set(11.8,4.2,-8.9);scene.add(doorF);const dark=box(4,8,.1,0x2a2230,.01);dark.position.set(11.8,4,-8.8);scene.add(dark);
const hinge=new THREE.Group();hinge.position.set(9.8,0,-8.6);scene.add(hinge);const door=box(4,8,.3,0x9a6a42,.04);door.position.set(2,4,0);hinge.add(door);const knob=box(.3,.3,.4,0xffc23a,.05,{metalness:.7,roughness:.3});knob.position.set(3.5,4,.25);hinge.add(knob);
// sofá, cojín destrozado y relleno
const SF=sofa(0x3a5ab8);SF.position.set(-6,0,-6);scene.add(SF);
const cush=box(2.2,.5,1.6,0xe5343f,.2);cush.position.set(1.2,.3,3.9);cush.rotation.y=.5;cush.rotation.z=.15;scene.add(cush);
const FLF=puffs(scene,70,.32,0xffffff,{opacity:.95});const flf=[...Array(70)].map(()=>[(R()-.5)*5,R()*.25,(R()-.5)*4,.6+R()*.8]);
// plato con galleta-hueso
const plate=new THREE.Mesh(new THREE.CylinderGeometry(1.2,1.0,.2,28),new THREE.MeshStandardMaterial({color:0xf2f6ff,roughness:.3}));plate.position.set(3.6,.1,1.6);plate.receiveShadow=true;scene.add(plate);
const bone=new THREE.Group();{const c=0xd89a52;const m=box(1.1,.24,.3,c,.1);bone.add(m);[-1,1].forEach(s=>[-1,1].forEach(z=>{const k=box(.32,.26,.3,c,.12);k.position.set(s*.6,0,z*.17);bone.add(k)}))}bone.position.set(3.6,.34,1.6);scene.add(bone);
const boneG=glow(0xffe08a,2.4,.0);bone.add(boneG);
// personajes
const DG=dog();DG.g.position.set(1.4,0,1.2);DG.g.rotation.y=-.6;scene.add(DG.g);
const OW=capataz();OW.g.position.set(5.6,0,-1.4);scene.add(OW.g);
const AB=abuela();AB.g.position.set(11.8,0,-12);scene.add(AB.g);
const HE=puffs(scene,8,.32,0xff5a7a,{opacity:.9});
const sweat=label3d(['?'],{w:1.6,h:1.6,bg:null,fg:'#ffffff',px:260,sprite:true});sweat.position.set(0,-99,0);scene.add(sweat);
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],k=ss(0,d,lt),m=mouthAt(t);let p,q;
 for(let i=0;i<8;i++)HE.set(i,0,-99,0,0);sweat.position.y=-99;
 // relleno del cojín solo en el gancho (la 'escena del crimen'), que se mueve un poco con el aire
 flf.forEach(([x,y,z,sc],i)=>FLF.set(i,s==='h'?1.6+x*.6:-99,y*.6+.1+Math.max(0,Math.sin(t*1.2+i))*.08,3.6+z*.4,sc*.45));FLF.done();cush.visible=s==='h';
 bone.visible=true;boneG.material.opacity=0;plate.visible=!(s==='h'||s==='s3'||s==='s4');hinge.rotation.y=0;AB.g.visible=false;OW.g.visible=true;
 let guilt=0,wag=.3,sit=0,look=0;
 if(s==='h'){guilt=1;wag=0;OW.g.visible=false;bone.visible=false;
  p=V3(8.6+Math.sin(t*.4)*.3-k*.6,3.6,7.8-k*.5);q=V3(2.6,2.1,2.2)}
 else if(s==='s1'){guilt=0;sit=1;wag=.2;look=.25;OW.g.position.set(5.8,0,-.6);OW.g.rotation.y=-1.1;OW.pose(t,m,{point:ss(.6,1.4,lt)*.9,look:-.3});boneG.material.opacity=.5+.3*Math.sin(t*5);
  p=V3(2.4+k*1.4,6.2,19-k*2);q=V3(3.2,2.3,.6)}
 else if(s==='s2'){sit=1;look=.45;wag=.1;
  // la dueña se va por la puerta (0–45 %), entra la investigadora y se lleva la galleta (45–100 %)
  const out=ss(.05,.42,lt/d),inn=ss(.45,.7,lt/d),take=ss(.7,.8,lt/d),gone=ss(.82,1,lt/d);
  const bump=x=>Math.sin(clamp(x)*Math.PI);hinge.rotation.y=-1.3*Math.max(bump(out),bump(inn),bump(gone));
  OW.g.position.set(lerp(5.8,11.8,out),0,lerp(-.6,-11,out*out));OW.g.rotation.y=Math.PI-.35*(1-out);OW.pose(t,0,{walk:out<1?t*7:null});OW.g.visible=out<.98;
  AB.g.visible=inn>0;AB.g.position.set(lerp(11.8,4.6,inn)+gone*7,0,lerp(-11,1.0,inn)-gone*12);AB.g.rotation.y=gone>0?Math.PI*.85:-.6+.2*inn;AB.pose(t,0,{walk:(inn<1||gone>0)?t*7:null,point:take*(1-gone)*.8});
  if(take>0){const hp=new THREE.Vector3();AB.armR.children[1].getWorldPosition(hp);bone.position.lerpVectors(V3(3.6,.34,1.6),hp,take)}else bone.position.set(3.6,.34,1.6);
  p=V3(4.5+Math.sin(t*.3),7.5,24-k*2);q=V3(5,2.6,-2)}
 else if(s==='s3'){bone.visible=false;OW.g.position.set(5.0,0,0);OW.g.rotation.y=-1.2;OW.pose(t,m,{armsUp:ss(.3,1,lt)*.55,look:-.4});OW.head.rotation.x=.25;
  guilt=ss(.6,2.0,lt);wag=0;sit=0;sweat.position.set(DG.g.position.x+1.2,3.1+Math.sin(t*3)*.1,DG.g.position.z+.8);
  p=V3(4.4+Math.sin(t*.4)*.5,4.8,19.5-k*2);q=V3(3.6,1.4,.2)}
 else if(s==='s4'){bone.visible=false;OW.g.position.set(4.6,0,.6);OW.g.rotation.y=-1.25;OW.pose(t,m,{look:-.3});OW.armR.rotation.x=-1.0;OW.head.rotation.x=.35;
  guilt=1-ss(.8,2.4,lt);wag=ss(1.4,3,lt);
  if(lt>2.2)for(let i=0;i<8;i++){const f=((t*.6+i/8)%1);HE.set(i,2.6+Math.sin(i*2+t)*.5,3.2+f*2.4,1.2+Math.cos(i*1.7)*.4,(1-f)*1.2)}
  p=V3(4.0,4.6,17.5-k*1.5);q=V3(3.4,1.4,.4)}
 else{bone.visible=true;OW.g.position.set(5.2,0,.2);OW.g.rotation.y=-.6;OW.pose(t,m,{wave:1,look:-.1});wag=1;guilt=0;
  p=V3(3.4+k*.5,5.2,18);q=V3(3.4,.6,0)}
 HE.done();
 DG.pose(t,{guilt,wag,sit,look,m:0});
 cam.position.copy(p);cam.lookAt(q);r.render(scene,cam)};
function lerp(a,b,x){return a+(b-a)*x}
window.ready=true;
