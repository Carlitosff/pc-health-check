// ¿Y si la Tierra gira cada vez más deprisa? (1804). Serie ¿QUÉ PASARÍA SI…? Parte 7.
// Reutilizable: playa del ecuador con palmeras de bloques, báscula con lectura integrada (label3d), sol que cruza el cielo a la velocidad del día
// (ciclo día/noche con color de cielo según la altura del sol) y globo con el ecuador marcado.
import {THREE,J,mk,ss,V3,clamp,stage,sun,box,glow,pixTex,capataz,segAt,mouthAt,label3d,stars,voxGlobe,puffs} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x8ad4ff,fog:[0xbfe6ff,70,260],exposure:1.08});const R=mk(1804);
const hemi=new THREE.HemisphereLight(0xdcefff,0xc8a878,1.3);scene.add(hemi);const S=sun(scene,{pos:[-16,34,18],span:30});
const DAY=new THREE.Color(0x7cc8ff),DUSK=new THREE.Color(0xff8a5a),NIGHT=new THREE.Color(0x0a1230),SPACE=new THREE.Color(0x02030a);
// ---------- playa del ecuador
const st=new THREE.Group();scene.add(st);
const sand=pixTex(128,128,(g,w,h)=>{const q=mk(4);g.fillStyle='#e8d29a';g.fillRect(0,0,w,h);for(let i=0;i<900;i++){g.fillStyle=['#dcc489','#f2dfac','#cfb57a'][Math.floor(q()*3)];g.fillRect(Math.floor(q()*w/4)*4,Math.floor(q()*h/4)*4,4,4)}},[50,50]);
const gnd=new THREE.Mesh(new THREE.PlaneGeometry(400,400),new THREE.MeshStandardMaterial({map:sand,roughness:1}));gnd.rotation.x=-Math.PI/2;gnd.receiveShadow=true;st.add(gnd);
const sea=new THREE.Mesh(new THREE.PlaneGeometry(600,300),new THREE.MeshStandardMaterial({color:0x1a8ad0,roughness:.35,metalness:.1}));sea.rotation.x=-Math.PI/2;sea.position.set(0,.05,-165);st.add(sea);
const foam=[];for(let i=0;i<40;i++){const f=box(3+R()*4,.12,.6,0xffffff,.05);f.position.set(-60+i*3.1,.12,-15.5+R()*.6);st.add(f);foam.push(f)}
function palm(x,z,h,lean){const g=new THREE.Group();for(let i=0;i<h;i++){const s=box(.7,1,.7,i%2?0x8a6238:0x7a5430,.08);s.position.set(Math.sin(i/h*1.2)*lean,i+.5,0);g.add(s)}const top=V3(Math.sin(1.2)*lean,h,0);for(let k=0;k<7;k++){const a=k/7*6.283;const lf=new THREE.Group();lf.position.copy(top);lf.rotation.y=a;for(let j=0;j<4;j++){const b=box(1.1,.25,.9,j%2?0x3f9a3a:0x4fb04a,.05);b.position.set(.9+j*.95,-j*j*.12,0);lf.add(b)}g.add(lf)}const co=box(.6,.6,.6,0x5a3a1a,.2);co.position.copy(top).add(V3(.3,-.6,.3));g.add(co);g.position.set(x,0,z);g.userData.lean=lean;st.add(g);return g}
const palms=[palm(-9,-4,9,1.4),palm(10,-7,11,-1.6),palm(-16,-10,8,1),palm(17,-2,7,-1.1),palm(4,-12,10,.9)];
// cartel del ecuador
const sign=label3d(['ECUADOR','*0° 0′'],{w:5,h:2.4,px:120});sign.position.set(-6.5,4.4,-1.2);st.add(sign);const post=box(.3,3.2,.3,0x5a3a1a,.04);post.position.set(-6.5,1.6,-1.3);st.add(post);
// báscula + lectura
const scale=new THREE.Group();const base=box(3.2,.4,2.6,0xe8eaf0,.12);base.position.y=.2;scale.add(base);const top=box(2.8,.12,2.2,0x30343e,.05);top.position.y=.46;scale.add(top);scale.position.set(0,0,2);st.add(scale);
const disp=label3d(['80,0 kg'],{w:3.8,h:1.45,px:150,accent:'#4ade80'});disp.position.set(3.1,3.3,2.6);st.add(disp);const dpost=box(.25,2.2,.25,0x30343e,.03);dpost.position.set(3.1,1.1,2.5);st.add(dpost);
const hero=capataz();hero.g.position.set(0,.52,2);scene.add(hero.g);
// cosas que flotan al final (cubos de playa, pelota, toalla)
const loose=[];[[0xff5a3a,-4,4],[0x3ad1ff,6.4,3],[0xffd23a,-5.5,1.2],[0x7ce06a,7.4,.5],[0xff3fb0,-6.5,5]].forEach(([c,x,z],i)=>{const m=i%2?new THREE.Mesh(new THREE.SphereGeometry(.5,16,12),new THREE.MeshStandardMaterial({color:c,roughness:.5})):box(.9,.9,.9,c,.12);m.castShadow=true;m.position.set(x,.5,z);m.userData={x,z,ph:R()*6};st.add(m);loose.push(m)});
const sand2=puffs(scene,120,.25,0xe8d29a,{opacity:.9,depthWrite:false});const sp=[];for(let i=0;i<120;i++)sp.push([R()*6.28,R(),R()]);
// sol (disco que se ve) y estrellas
const sunDisc=new THREE.Mesh(new THREE.SphereGeometry(5,24,16),new THREE.MeshBasicMaterial({color:0xfff2b0,toneMapped:false,fog:false}));scene.add(sunDisc);const sunG=glow(0xffd070,40,.8);sunG.material.fog=false;scene.add(sunG);
const ST=stars(scene,1500,{r0:200,r1:240,size:1.2});ST.material.fog=false;ST.material.transparent=true;
// ---------- globo (s1)
const GL=new THREE.Group();GL.position.set(600,0,0);scene.add(GL);const glb=voxGlobe(9000,10);GL.add(glb.group);
const eq=new THREE.Mesh(new THREE.TorusGeometry(10.4,.16,8,120),new THREE.MeshBasicMaterial({color:0xffd23a,toneMapped:false}));eq.rotation.x=Math.PI/2;glb.group.add(eq);
const gLab=label3d(['*1 DÍA = 24 h','1.670 km/h'],{w:9,h:3.6,px:120,sprite:true});GL.add(gLab);
const gS=new THREE.DirectionalLight(0xfff4e0,0);gS.position.set(560,30,60);gS.target=GL;scene.add(gS);
// velocidad del día por segmento (vueltas de sol por segundo de vídeo): dibujo, no a escala; lo que se lee en la báscula sí es el cálculo
const t1=TL.s1[0],t2=TL.s2[0],t3=TL.s3[0],t4=TL.s4[0],tC=TL.cta[0];
const rate=t=>t<t1?.05+.25*ss(.5,t1,t):t<t3?.04:t<t4?.33:t<tC?.9:.05;
const phase=(()=>{const N=Math.ceil(J.total*30)+2,a=new Float32Array(N);let p=.18;for(let i=0;i<N;i++){a[i]=p;p+=rate(i/30)/30}return t=>a[Math.min(N-1,Math.floor(t*30))]})();
// lectura de la báscula (cálculo en serie_giro.py, pasa por J.read): kg a mostrar en cada segmento
const RD=J.read||{s2:79.72,s3:75.6,s4:0};
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],m=mouthAt(t);
 const beach=s!=='s1';st.visible=beach;hero.g.visible=beach;GL.visible=s==='s1';sunDisc.visible=sunG.visible=beach;sand2.m.visible=s==='s4';
 let p,q;
 if(beach){// sol: gira en el plano este-oeste; altura -> color del cielo y luz
  const a=phase(t)*6.2832;const sy=Math.sin(a),sx=Math.cos(a);const SP=V3(sx*45,sy*42+16,-110);sunDisc.position.copy(SP);sunG.position.copy(SP);
  const day=ss(-.15,.35,sy),dusk=Math.exp(-(((sy-.05)/.18)**2));const col=NIGHT.clone().lerp(DAY,day).lerp(DUSK,dusk*.55);scene.background=col;scene.fog.color.copy(col);scene.fog.near=70;scene.fog.far=260;
  S.position.set(sx*30,Math.max(4,sy*34),18);S.target.position.set(0,0,2);S.target.updateMatrixWorld();S.intensity=2.7*day+.15;hemi.intensity=.35+1.0*day;ST.material.opacity=1-day;ST.visible=day<.98;
  sea.material.color.setHex(0x1a8ad0).multiplyScalar(.35+.65*day);
  foam.forEach((f,i)=>{f.position.z=-15.5+Math.sin(t*1.4+i*.7)*.5});
  // báscula
  let kg=80,fl=0;
  if(s==='s2')kg=80-(80-RD.s2)*ss(.6,2.2,lt);else if(s==='s3')kg=RD.s2-(RD.s2-RD.s3)*ss(.4,d*.7,lt);else if(s==='s4'){kg=RD.s3-(RD.s3-RD.s4)*ss(.2,d*.55,lt);fl=ss(d*.5,d*.9,lt)}else if(s==='cta'){kg=0;fl=1}
  const txt=kg<.05?'0,0 kg':kg.toFixed(kg>=79.5&&s==='s2'?2:1).replace('.',',')+' kg';
  disp.set(s==='h'?['¿ ? kg']:[txt]);
  const lift=fl*4.5;hero.g.position.y=.52+lift+(fl>0?Math.sin(t*1.3)*.25*fl:0);hero.g.rotation.z=fl*.25*Math.sin(t*.7);
  loose.forEach((o,i)=>{const u=o.userData;o.position.y=.5+fl*(2+i*.9)+Math.sin(t*1.2+u.ph)*.2*fl;o.rotation.set(fl*t*.5,fl*t*.3*(i%2?1:-1),0)});
  palms.forEach((g,i)=>{g.rotation.z=Math.sin(t*(1.2+i*.1))*.02*(1+3*(s==='s4'||s==='cta'?1:0))});
  if(s==='s4'&&fl>0){const k=fl;for(let i=0;i<120;i++){const[a2,b,c]=sp[i];const rr=1+k*(2+b*4);sand2.set(i,Math.cos(a2)*rr,.3+k*b*3,2+Math.sin(a2)*rr,(1-k*.6)*(.6+b))}sand2.done()}
  hero.pose(t,m,{armsUp:s==='s4'?.7*fl:s==='s3'?.25:0,wave:s==='cta'?1:0,look:s==='h'?-.5+Math.sin(t*.8)*.3:s==='s3'?-.4:0,point:s==='s2'?.6*ss(.4,1,lt):0});
  // cámara: personaje en la mitad de abajo, cielo arriba (el sol se ve cruzar)
  if(s==='h'){const k=ss(0,d,lt);p=V3(1.6,3.2,21.5-k*2);q=V3(1.6,5.4,1)}
  else if(s==='s2'){const k=ss(0,d,lt);p=V3(2.6-k*.6,3,19-k*2);q=V3(1.6,4.4,2)}
  else if(s==='s3'){const k=ss(0,d,lt);p=V3(-1+k*2,2.6,25-k*2);q=V3(1.4,7.2,-2)}
  else if(s==='s4'){const k=ss(0,d,lt);p=V3(1.6,2.6+k*2,23+k*3);q=V3(1.6,5+fl*3,1);if(lt<.6){p.x+=Math.sin(t*50)*.08}}
  else{const k=ss(0,d,lt);p=V3(1.6,3.5+k,24+k*2);q=V3(1.6,6+k*2,0)}}
 else{scene.background=SPACE;S.intensity=0;hemi.intensity=.35;gS.intensity=3;ST.visible=true;ST.material.opacity=1;
  glb.group.rotation.x=.18;glb.group.rotation.y=-1+ (t-t1)*(.35+1.4*ss(t1+1.5,TL.s1[1],t));
  gLab.position.set(0,-2,13);const k=ss(0,d,lt);p=V3(600,-4+k*2,46-k*6);q=V3(600,4.5,0)}
 cam.position.copy(p);cam.lookAt(q);r.render(scene,cam)};
window.ready=true;
