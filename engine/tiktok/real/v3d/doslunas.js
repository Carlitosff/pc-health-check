// Serie P22 '¿Y si la Tierra tuviera dos lunas?' (3304). Fuentes en serie_doslunas.py.
// Reutilizable: PLAZA DE NOCHE con cielo estrellado y una o dos lunas (luz de luna regulable: moonLight), MINILUNA (roca de cubos) con estela
// alrededor de un globo, CHOQUE LENTO de una luna pequeña contra la grande que levanta montañas en la cara oculta (voxMoon.bump).
import {THREE,J,mk,ss,V3,clamp,stage,box,glow,capataz,segAt,mouthAt,puffs,stars,voxGlobe,voxMoon} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x07102a,exposure:1.2});cam.far=2000;cam.updateProjectionMatrix();const R=mk(3304);
const hemi=new THREE.HemisphereLight(0x6f86c8,0x1a1420,.55);scene.add(hemi);
// ---------- PLAZA (origen)
const PL=new THREE.Group();scene.add(PL);
{const fl=box(90,.4,90,0x4a4e5e,.02);fl.position.y=-.2;fl.receiveShadow=true;PL.add(fl);for(let i=0;i<18;i++){const l=box(90,.03,.12,0x3a3e4c,.01);l.position.set(0,.02,-45+i*5);PL.add(l);const l2=box(.12,.03,90,0x3a3e4c,.01);l2.position.set(-45+i*5,.02,0);PL.add(l2)}
 const q=mk(9);for(let i=0;i<10;i++){const side=i%2?1:-1,h=10+q()*18,w=7+q()*4;const b=box(w,h,8,[0x2e3550,0x3a3248,0x283a48][i%3],.05);b.position.set(side*(20+q()*6),h/2,-40+i*7);b.castShadow=b.receiveShadow=true;PL.add(b);
  for(let f=1;f<h/3-1;f++)for(let k=0;k<2;k++)if(q()<.55){const wdw=box(1.2,1.4,.2,0xffd27a,.01,{emissive:0xffb84a,emissiveIntensity:1.1});wdw.position.set(side*(20+q()*6)-side*(w/2+.05)*0,f*3,-40+i*7+4.05);wdw.position.x=b.position.x-w/4+k*w/2;PL.add(wdw)}}
 [-9,9].forEach(x=>{const p=box(.4,6,.4,0x22252e,.05);p.position.set(x,3,8);PL.add(p);const l=box(1.1,.6,1.1,0xfff0c0,.1,{emissive:0xffd890,emissiveIntensity:1.4});l.position.set(x,6.2,8);PL.add(l);const g=glow(0xffd890,5,.5);g.position.set(x,6.2,8);PL.add(g)});
 const fnt=box(7,1.2,7,0x8a8e9e,.1);fnt.position.set(0,.6,-6);PL.add(fnt);const wat=box(6,.2,6,0x2a5a9a,.02,{emissive:0x0a2a5a,emissiveIntensity:.6});wat.position.set(0,1.15,-6);PL.add(wat)}
const moonL=new THREE.DirectionalLight(0xc8d8ff,.8);moonL.position.set(-20,60,-60);moonL.castShadow=true;moonL.shadow.mapSize.set(1024,1024);{const c=moonL.shadow.camera;c.left=-40;c.right=40;c.top=40;c.bottom=-40;c.far=200}scene.add(moonL);
const CAP=capataz();CAP.g.position.set(4.5,0,10);CAP.g.rotation.y=Math.PI*.1;scene.add(CAP.g);
// cielo de la plaza: Luna grande y segunda luna (más pequeña)
const SKY=new THREE.Group();scene.add(SKY);
const M1=voxMoon(3500,9,{cube:.55,seed:1,emissive:.9});M1.group.position.set(-12,35,-120);SKY.add(M1.group);const h1=glow(0xdfe8ff,48,.35);h1.position.copy(M1.group.position);SKY.add(h1);
const M2=voxMoon(2200,5.2,{cube:.5,seed:4,emissive:.9});M2.group.position.set(15,22,-120);SKY.add(M2.group);const h2=glow(0xdfe8ff,28,.3);h2.position.copy(M2.group.position);SKY.add(h2);
const ST=stars(scene,1400,{r0:600,r1:800,size:1.6});
// ---------- ESPACIO (x=2000): Tierra y miniluna
const SP=new THREE.Group();SP.position.set(2000,0,0);scene.add(SP);
const EA=voxGlobe(9000,10,{cube:.55});SP.add(EA.group);const sunL=new THREE.DirectionalLight(0xfff2dc,2.4);sunL.position.set(2000-60,20,40);sunL.target.position.set(2000,0,0);scene.add(sunL,sunL.target);
const ROCK=new THREE.Group();SP.add(ROCK);{const q=mk(5);for(let i=0;i<9;i++){const c=box(.5+q()*.4,.5+q()*.4,.5+q()*.4,[0x8a7a6a,0x6e6258,0x9a8a78][i%3],.08);c.position.set((q()-.5)*.8,(q()-.5)*.8,(q()-.5)*.8);c.rotation.set(q()*3,q()*3,0);ROCK.add(c)}}
const rg=glow(0xffc23a,5,.9);ROCK.add(rg);
const TRAIL=puffs(scene,90,.22,0xffc23a,{opacity:.9});
// trayectoria de la miniluna (vista desde arriba: lazo alrededor de la Tierra y salida)
const path=u=>{const a=-2.2+u*4.6,rr=16+4*Math.sin(u*3.1);return V3(Math.cos(a)*rr,Math.sin(u*6.28)*3,Math.sin(a)*rr)};
// ---------- LUNA ANTIGUA (x=4000): choque lento de la compañera (1/3 del diámetro)
const AN=new THREE.Group();AN.position.set(4000,0,0);scene.add(AN);
const BM=voxMoon(7000,12,{cube:.55,seed:2,emissive:.25});AN.add(BM.group);const BC=voxMoon(1400,4,{cube:.5,seed:6,emissive:.25});AN.add(BC.group);
const sunA=new THREE.DirectionalLight(0xfff2dc,2.6);sunA.position.set(4000-40,30,50);sunA.target.position.set(4000,0,0);scene.add(sunA,sunA.target);
const SPL=puffs(scene,120,.6,0xbfc4cc,{opacity:.9});
console.assert(Math.abs(4/12-1/3)<1e-9);
const BDIR=V3(1,.15,0).normalize();
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],k=ss(0,d,lt),m=mouthAt(t);
 for(let i=0;i<90;i++)TRAIL.set(i,0,-999,0,0);for(let i=0;i<120;i++)SPL.set(i,0,-999,0,0);
 M1.group.rotation.y=t*.05;M2.group.rotation.y=-t*.08;EA.group.rotation.y=t*.12;M2.group.visible=true;h2.visible=true;
 CAP.pose(t,0,{look:.2});CAP.head.rotation.x=-.45;let p,q,light=.8;
 if(s==='h'||s==='cta'||(s==='s4'&&lt>d*.45)){// plaza de noche con dos lunas
  const dbl=s==='s4'?ss(d*.5,d*.8,lt):1;light=.9+1.1*dbl;CAP.pose(t,s==='cta'?m:0,{wave:s==='cta'?1:0,point:s==='h'?.8:0,look:.2});CAP.head.rotation.x=s==='cta'?-.1:-.45;
  if(s==='h'){p=V3(6-k*2,4+k*.6,31-k*2);q=V3(0,19,-60)}else if(s==='cta'){p=V3(5+k*2,4.5,31-k*2);q=V3(0,18,-60)}else{p=V3(0,4+k*1.5,33);q=V3(0,19,-60)}}
 else if(s==='s1'||s==='s2'){// miniluna alrededor de la Tierra y salida
  const u=s==='s1'?ss(0,d,lt)*.7:.7+ss(0,d*.8,lt)*.3;const P0=path(u);ROCK.position.copy(u<.98?P0:P0);ROCK.rotation.set(t*.7,t*.5,0);ROCK.scale.setScalar(2.2);
  if(s==='s2')ROCK.position.add(path(u).clone().normalize().multiplyScalar(ss(.3,d,lt)*30));
  for(let i=0;i<90;i++){const uu=u-i*.006;if(uu<0)break;const pp=path(uu);TRAIL.set(i,2000+pp.x,pp.y,pp.z,(1-i/90)*1.1)}
  const c=V3(2000,0,0);if(s==='s1'){p=V3(2000+6,62-k*8,64-k*6);q=V3(2000,-3,0)}else{p=V3(2000+16,52,78);q=V3(2000+ROCK.position.x*.35,-3,ROCK.position.z*.35)}}
 else if(s==='s3'||s==='s4'){// la compañera se acerca despacio y choca; en s4 se aplasta en la cara oculta
  const appr=s==='s3'?ss(.5,d,lt):1;const dist=12+4;const sy=BDIR.y*(dist+22*(1-appr)),sz=6*(1-appr);
  const sp=s==='s4'?ss(0,d*.4,lt):0;BC.group.position.set(BDIR.x*(dist+22*(1-appr))*(1-sp*.25),sy,sz);BC.group.scale.set(1-sp*.85,1+sp*.2,1+sp*.6);BC.group.visible=sp<.95;
  BM.bump(BDIR,s==='s4'?2.2*ss(.1,d*.4,lt):0,.55);
  if(s==='s4'){for(let i=0;i<120;i++){const a=i*.37,b=i*.71,rr=sp*(6+(i%7));const v=V3(BDIR.x*15+Math.cos(a)*.2*rr,Math.sin(b)*rr*.6,Math.cos(b)*rr*.6);SPL.set(i,4000+v.x+sp*2,v.y,v.z,(1-sp)*1.2)}}
  if(s==='s3'){p=V3(4000+10-k*2,16-k*4,128-k*16);q=V3(4000+9,4,0)}else{p=V3(4000+60,14,86);q=V3(4000+10,4,0)}}
 moonL.intensity=light;hemi.intensity=.35+light*.35;
 cam.position.copy(p);cam.lookAt(q);TRAIL.done();SPL.done();r.render(scene,cam)};
window.ready=true;
