// ¿Y si acercamos la Luna hasta que se rompe? (1704). Serie ¿QUÉ PASARÍA SI…? Parte 6.
// Reutilizable: luna de cubos con escala y estiramiento de marea (tideMoon), ruptura en anillo alrededor de un globo, mar con nivel (de luna.js).
import {THREE,J,mk,ss,V3,clamp,stage,sun,box,glow,capataz,camera,segAt,mouthAt,stars,voxGlobe,ringSystem,skyArch} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x06102c,fog:[0x06102c,60,400],exposure:1.1});const R=mk(1704);
const hemi=new THREE.HemisphereLight(0xbcd0ff,0x1a2a4a,1.0);scene.add(hemi);const S=sun(scene,{pos:[-12,30,20],span:30,color:0xdfe8ff,power:1.5});
const NIGHT=new THREE.Color(0x06102c),SPACE=new THREE.Color(0x02030c);const CC=new THREE.Color();const O=new THREE.Object3D();
// ---------------- MUELLE Y MAR (nivel variable)
const set=new THREE.Group();scene.add(set);const CS=1.5,SX=30,SZ=48,sea=new THREE.InstancedMesh(new THREE.BoxGeometry(CS,CS,CS),new THREE.MeshStandardMaterial({roughness:.32,metalness:.1}),SX*SZ);sea.frustumCulled=false;set.add(sea);
const far=new THREE.Mesh(new THREE.PlaneGeometry(900,500),new THREE.MeshStandardMaterial({color:0x0c4b9a,roughness:.5}));far.rotation.x=-Math.PI/2;far.position.set(0,-.4,-300);set.add(far);
const waveY=(x,z,t,a)=>(Math.sin(x*.32+t*1.5)*.2+Math.sin(z*.42-t*1.9)*.24+Math.sin((x+z)*.18+t*.9)*.16)*a;
const A=new THREE.Color(0x18b6d8),B=new THREE.Color(0x0a5fb8),F=new THREE.Color(0xe8fbff);
function drawSea(t,lvl,lum,wa){let i=0;for(let a=0;a<SX;a++)for(let b=0;b<SZ;b++){const x=(a-SX/2)*CS,z=42-b*CS,w=waveY(x,z,t,wa),y=w+lvl;O.position.set(x,y-CS/2-.1,z);O.updateMatrix();sea.setMatrixAt(i,O.matrix);CC.copy(A).lerp(B,clamp(Math.abs(z-6)/30));CC.lerp(F,clamp((w-.34*wa)*2.6/wa));CC.multiplyScalar(lum*(.92+((a*7+b*13)%5)*.03));sea.setColorAt(i,CC);i++}sea.instanceMatrix.needsUpdate=true;sea.instanceColor.needsUpdate=true;far.position.y=-.4+lvl;far.material.color.setHex(0x0c4b9a).multiplyScalar(lum)}
const PY=3.2;{for(let i=0;i<18;i++){const p=box(5.2,.3,.92,i%2?0x8a6238:0x7a5430,.03);p.position.set(0,PY-.15,14-i);set.add(p)}[-2.3,2.3].forEach(x=>{for(let z=14;z>-4;z-=4){const q=box(.5,9,.5,0x4a3220,.05);q.position.set(x,PY-4.6,z);set.add(q)}})}
// regla de marea con franjas, a escala del dibujo (no del mundo)
const rul=new THREE.Group();rul.position.set(3.0,0,3);set.add(rul);for(let i=-6;i<9;i++){const q=box(.95,.98,.95,i%2?0xfff3e0:0xe5343f,.03);q.position.y=i+.5;rul.add(q)}
const hero=capataz();set.add(hero.g);const lantern=glow(0xffc070,5,.7);lantern.position.set(.6,PY+2.2,1.0);set.add(lantern);
const ST=stars(scene,1600,{r0:300,r1:380,size:1.4});ST.material.fog=false;
// ---------------- LUNA DE CUBOS (cielo del muelle y espacio)
const noise=(x,y,z)=>Math.sin(x*3.1+1.3)*Math.cos(y*3.7-.7)+Math.sin(y*2.9+z*4.3)*.8+Math.cos(z*3.3-x*2.7+2)*.7+Math.sin(x*6.7+z*5.1)*.3;
function tideMoon(n,seed){const im=new THREE.InstancedMesh(new THREE.BoxGeometry(1,1,1),new THREE.MeshStandardMaterial({roughness:1,emissive:0x707888,emissiveIntensity:.35,fog:false}),n);im.frustumCulled=false;const q=mk(seed),D=[];
 for(let i=0;i<n;i++){const y=1-2*(i+.5)/n,rd=Math.sqrt(1-y*y),a=i*2.39996;const x=Math.cos(a)*rd,z=Math.sin(a)*rd;const c=noise(x*2,y*2,z*2)>.5?.56:.92;D.push({x,y,z,r:q(),w:q()*9,ring:13.5+q()*10,ph:q()*6.283,lag:q()});im.setColorAt(i,new THREE.Color(c,c,c*1.03))}
 return{im,D,draw(c,R0,stretch,brk,cube,earth){// stretch: elipsoide alargado hacia la Tierra (eje x local). brk 0..1: se suelta y se reparte en anillo alrededor de 'earth'
  for(let i=0;i<n;i++){const d=D[i];let px=c.x+d.x*R0*stretch,py=c.y+d.y*R0/Math.sqrt(stretch),pz=c.z+d.z*R0/Math.sqrt(stretch);let s=cube;
   if(brk>0&&earth){const k=ss(d.lag*.45,d.lag*.45+.55,brk);const ang=Math.atan2(pz-earth.z,px-earth.x)+brk*2.2*(1-d.r*.3)+0;const rr=d.ring;const tx=earth.x+Math.cos(ang+d.ph*k*.6)*rr,tz=earth.z+Math.sin(ang+d.ph*k*.6)*rr,ty=earth.y+(d.r-.5)*.5;px+=(tx-px)*k;py+=(ty-py)*k;pz+=(tz-pz)*k;s=cube*(1-.35*k)}
   O.position.set(px,py,pz);O.rotation.set(d.w*brk,d.w*brk*.7,0);O.scale.setScalar(s);O.updateMatrix();im.setMatrixAt(i,O.matrix)}O.rotation.set(0,0,0);O.scale.setScalar(1);im.instanceMatrix.needsUpdate=true}}}
const skyM=tideMoon(6000,7);scene.add(skyM.im);
// ---------------- ESPACIO: Tierra de cubos y la Luna que se acerca
const SP=new THREE.Group();SP.position.set(0,0,-2400);scene.add(SP);
const G=voxGlobe(9000,10);SP.add(G.group);G.group.rotation.z=-.41;
const spL=new THREE.DirectionalLight(0xfff4e0,0);spL.position.set(-60,30,40);spL.target=G.group;SP.add(spL);
const spM=tideMoon(4200,11);SP.add(spM.im);
const RS=ringSystem({r0:13,r1:23,op:.0,seed:6});RS.g.rotation.x=0;SP.add(RS.g);
stars(SP,1500,{r0:160,r1:230,size:1.1,seed:5});
// el anillo visto desde el muelle (CTA): lo que queda de la Luna
const ARC=skyArch({r:560,w:120,center:[40,-210,-520],tilt:-.38});scene.add(ARC.g);
const t1=TL.s1[0],t2=TL.s2[0],t3=TL.s3[0],t4=TL.s4[0],tC=TL.cta[0];
const EARTH=V3(0,0,0);cam.far=4000;cam.updateProjectionMatrix();
const shots={h:{p:V3(-1.2,3.2,27),q:V3(1,11,0)},s1:{p:V3(-2,3.4,24),q:V3(.5,12,-10)},s2:{p:V3(1.5,5,34),q:V3(0,13,-10)},
 s3:{p:V3(18,26,70),q:V3(16,0,0)},s4:{p:V3(-6,30,64),q:V3(6,0,0)},cta:{p:V3(2.2,5.4,20),q:V3(0,16,-30)}};
['s3','s4'].forEach(k=>{shots[k].p.add(SP.position);shots[k].q.add(SP.position)});
const go=camera(cam,['h','s1','s2','s3','s4','cta'],shots,TL,.5);
window.renderAt=t=>{const s=segAt(TL,t),m=mouthAt(t);const space=s==='s3'||s==='s4';const dock=!space;
 set.visible=dock;SP.visible=space;ARC.g.visible=s==='cta';skyM.im.visible=dock&&s!=='cta';
 // tamaño aparente de la luna del cielo: x1 (h) → x2 (s1, mitad de camino) → x10 (s2, una décima parte): dibujo, no a escala angular exacta
 const kS=s==='h'?1+ss(.6,TL.h[1],t)*.3:s==='s1'?1.15+.85*ss(t1+.4,t1+3,t):s==='s2'?2+3.6*ss(t2+.3,t2+3.2,t):5.6;
 const MC=V3(7.5-kS*.7,17+kS*2.6,-80);skyM.draw(MC,4.6*kS,1,0,.6*kS,null);skyM.im.material.emissiveIntensity=.35+.1*kS;
 let lvl=0,wa=1,lum=.6;
 if(dock){scene.background=NIGHT.clone();scene.fog.color.copy(NIGHT);scene.fog.far=400;hemi.intensity=.95+(s==='s2'?.25:0);S.intensity=1.5;spL.intensity=0;
  // mareas: amplitud del dibujo según la fuerza (×1, ×8, ×1.000), comprimida para que quepa
  const amp=s==='s1'?.3+1.0*ss(t1+1.5,t1+3.5,t):s==='s2'?1.3+3.2*ss(t2+.8,t2+3.5,t):s==='cta'?.25:.3;lvl=amp*Math.sin(t*(s==='s2'?2.2:1.4));wa=s==='s2'?1.6:1;lum=.55+.12*Math.min(kS,3);
  drawSea(t,lvl,lum,wa);rul.visible=s==='s1'||s==='s2';ST.visible=true;ARC.draw(t,{night:1,gap:0});
  hero.g.position.set(s==='cta'?0:-1.6,PY,2.4);hero.g.rotation.y=s==='cta'?0:.15;
  if(s==='h')hero.pose(t,m,{look:.4,armsUp:.3});else if(s==='s2')hero.pose(t,m,{look:.3,armsUp:.8*ss(t2+1,t2+2,t)});else if(s==='cta')hero.pose(t,m,{wave:1,look:.05});else hero.pose(t,m,{look:.4,point:.7});
  lantern.material.opacity=.7}
 else{scene.background=SPACE.clone();scene.fog.far=1e5;hemi.intensity=.25;S.intensity=0;spL.intensity=2.6;ST.visible=false;G.group.rotation.y=t*.25;
  // distancia en radios terrestres (Tierra = 10 u): 60 → 28,9 (Roche fluida, 18.400 km) en s3; → 14,9 (rígida, 9.500 km) y ruptura en s4
  let D,st=1,brk=0;if(s==='s3'){const e=ss(t3,TL.s3[1]-.3,t);D=48-19.1*e;st=1+.38*ss(t3+2.4,TL.s3[1],t)}else{const e=ss(t4,t4+2,t);D=28.9-14*e;st=1.38+.25*e;brk=ss(t4+1.8,TL.s4[1]-.4,t)}
  window._D=Math.max(D,s==='s4'?22:D);spM.draw(V3(D,0,0),2.7,st,brk,.34,EARTH);RS.m&&(RS.m.material.opacity=.0);RS.g.traverse(o=>{if(o.material){o.material.transparent=true;o.material.opacity=.85*ss(.75,1,brk)}})}
 if(space){const D=window._D||40;const q=V3(D*.5,0,0).add(SP.position);const dist=(D+16)/(.63*.62);const sw=s==='s3'?Math.sin(t*.3)*4:Math.sin(t*.3)*3;cam.position.copy(q).add(V3(sw,dist*.25,dist));cam.lookAt(q);cam.rotateZ(Math.PI/2);cam.translateY(.13*.63*dist);r.render(scene,cam);return true}
 go(t,(p,q)=>{if(s==='s2'){const a=.06*ss(t2+1.5,t2+3,t);p.x+=Math.sin(t*41)*a;p.y+=Math.cos(t*37)*a}if(s==='h')p.z-=t*.25});
 r.render(scene,cam);return true};
window.ready=true;
