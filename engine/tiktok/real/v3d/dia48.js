// ¿Y si el día durara 48 horas? (3604). Serie ¿QUÉ PASARÍA SI…? Parte 25. Fuentes y cálculo en serie_dia48.py.
// Reutilizable: PLAYA DEL ECUADOR (de giro.js) con ciclo día/noche lento, RELOJ DE 48 H en un poste (esfera con 48 marcas, una aguja que da una vuelta por día),
// TERMÓMETRO de bloques con columna que sube y baja, calima de calor y escarcha, báscula con lectura integrada, y TIERRA + LUNA en el espacio
// con un rótulo de horas por día (18 h → 24 h) y un 'freno' de marea dibujado.
import {THREE,J,mk,ss,V3,clamp,stage,sun,box,glow,pixTex,capataz,segAt,mouthAt,label3d,stars,voxGlobe,voxMoon,puffs,snow} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x8ad4ff,fog:[0xbfe6ff,70,260],exposure:1.08});const R=mk(3604);
const hemi=new THREE.HemisphereLight(0xdcefff,0xc8a878,1.3);scene.add(hemi);const S=sun(scene,{pos:[-16,34,18],span:30});
const DAY=new THREE.Color(0x7cc8ff),DUSK=new THREE.Color(0xff8a5a),NIGHT=new THREE.Color(0x0a1230),SPACE=new THREE.Color(0x02030a),HOT=new THREE.Color(0xffd6a0);
const st=new THREE.Group();scene.add(st);
const sand=pixTex(128,128,(g,w,h)=>{const q=mk(4);g.fillStyle='#e8d29a';g.fillRect(0,0,w,h);for(let i=0;i<900;i++){g.fillStyle=['#dcc489','#f2dfac','#cfb57a'][Math.floor(q()*3)];g.fillRect(Math.floor(q()*w/4)*4,Math.floor(q()*h/4)*4,4,4)}},[50,50]);
const gnd=new THREE.Mesh(new THREE.PlaneGeometry(400,400),new THREE.MeshStandardMaterial({map:sand,roughness:1}));gnd.rotation.x=-Math.PI/2;gnd.receiveShadow=true;st.add(gnd);
const sea=new THREE.Mesh(new THREE.PlaneGeometry(600,300),new THREE.MeshStandardMaterial({color:0x1a8ad0,roughness:.35,metalness:.1}));sea.rotation.x=-Math.PI/2;sea.position.set(0,.05,-165);st.add(sea);
const foam=[];for(let i=0;i<40;i++){const f=box(3+R()*4,.12,.6,0xffffff,.05);f.position.set(-60+i*3.1,.12,-15.5+R()*.6);st.add(f);foam.push(f)}
function palm(x,z,h,lean){const g=new THREE.Group();for(let i=0;i<h;i++){const s=box(.7,1,.7,i%2?0x8a6238:0x7a5430,.08);s.position.set(Math.sin(i/h*1.2)*lean,i+.5,0);g.add(s)}const top=V3(Math.sin(1.2)*lean,h,0);for(let k=0;k<7;k++){const a=k/7*6.283;const lf=new THREE.Group();lf.position.copy(top);lf.rotation.y=a;for(let j=0;j<4;j++){const b=box(1.1,.25,.9,j%2?0x3f9a3a:0x4fb04a,.05);b.position.set(.9+j*.95,-j*j*.12,0);lf.add(b)}g.add(lf)}g.position.set(x,0,z);st.add(g);return g}
const palms=[palm(-9,-4,9,1.4),palm(10,-7,11,-1.6),palm(-16,-10,8,1),palm(17,-2,7,-1.1)];
// RELOJ DE 48 H en un poste: 48 marcas (cada 6 h más largas) y una sola aguja que da una vuelta por día
const CLK=new THREE.Group();CLK.position.set(-2.9,0,-.4);st.add(CLK);const pole=box(.35,3.8,.35,0x5a3a1a,.04);pole.position.y=1.9;const cs=label3d(['*1 DÍA = 48 H'],{w:3.6,h:1.1,px:110});cs.position.set(0,2.4,.3);CLK.add(cs);CLK.add(pole);
const face=new THREE.Mesh(new THREE.CylinderGeometry(2.0,2.0,.25,48),new THREE.MeshStandardMaterial({color:0xf8f2e2,roughness:.6}));face.rotation.x=Math.PI/2;face.position.y=5.6;CLK.add(face);
const rim=new THREE.Mesh(new THREE.TorusGeometry(2.0,.14,8,48),new THREE.MeshStandardMaterial({color:0xffc23a,metalness:.5,roughness:.4}));rim.position.y=5.6;CLK.add(rim);
for(let i=0;i<48;i++){const a=i/48*6.2832;const m=box(.07,i%6?.16:.38,.05,i%12?0x20202a:0xe5343f,.01);m.position.set(Math.sin(a)*1.7,5.6+Math.cos(a)*1.7,.15);m.rotation.z=-a;CLK.add(m)}
const hand=new THREE.Group();hand.position.set(0,5.6,.2);CLK.add(hand);const hb=box(.14,1.55,.06,0x20202a,.02);hb.position.y=.7;hand.add(hb);const hub=box(.3,.3,.1,0xe5343f,.04);hand.add(hub);
// half-day: mitad de la esfera clara (día) y mitad oscura (noche)
const half=new THREE.Mesh(new THREE.CircleGeometry(1.5,48,Math.PI/2,Math.PI),new THREE.MeshBasicMaterial({color:0x22305a,transparent:true,opacity:.35}));half.position.set(0,5.6,.14);half.rotation.z=Math.PI;CLK.add(half);
// TERMÓMETRO de bloques
const TH=new THREE.Group();TH.position.set(3.4,0,.2);TH.scale.setScalar(.72);st.add(TH);const tb=box(1.1,6.4,.6,0xf4f6fa,.3);tb.position.y=3.6;TH.add(tb);const bulb=box(1.5,1.4,.8,0xe5343f,.5);bulb.position.y=.75;TH.add(bulb);
const col=box(.5,1,.62,0xe5343f,.1);TH.add(col);for(let i=0;i<10;i++){const tk=box(.3,.06,.64,0x30343e,.01);tk.position.set(.35,1.6+i*.55,0);TH.add(tk)}
const setTemp=x=>{const h=.4+x*5.2;col.scale.y=h;col.position.y=1.3+h/2};
// báscula
const scale=new THREE.Group();const base=box(3.2,.4,2.6,0xe8eaf0,.12);base.position.y=.2;scale.add(base);const top=box(2.8,.12,2.2,0x30343e,.05);top.position.y=.46;scale.add(top);scale.position.set(0,0,2);st.add(scale);
const disp=label3d(['80,0 kg'],{w:3.8,h:1.45,px:150,accent:'#4ade80'});disp.position.set(2.3,2.5,3.3);st.add(disp);const dpost=box(.25,1.6,.25,0x30343e,.03);dpost.position.set(2.3,.8,3.2);st.add(dpost);
const hero=capataz();hero.g.position.set(0,.52,2);scene.add(hero.g);
const HAZE=puffs(scene,60,.22,0xfff0c0,{opacity:.45,depthWrite:false});const hz=[...Array(60)].map(()=>[R()*20-10,R(),R()*6-2]);
const SW=puffs(scene,10,.16,0x8fd0ff,{opacity:.9});
const SN=snow(scene,500,[-14,14,14,-8,8],{size:.18,speed:1.0});
const sunDisc=new THREE.Mesh(new THREE.SphereGeometry(5,24,16),new THREE.MeshBasicMaterial({color:0xfff2b0,toneMapped:false,fog:false}));scene.add(sunDisc);const sunG=glow(0xffd070,40,.8);sunG.material.fog=false;scene.add(sunG);
const ST=stars(scene,1500,{r0:200,r1:240,size:1.2});ST.material.fog=false;ST.material.transparent=true;
// ---------- espacio (s4): Tierra y Luna
const GL=new THREE.Group();GL.position.set(600,0,0);scene.add(GL);const glb=voxGlobe(9000,10);GL.add(glb.group);
const MO=voxMoon(2200,3.2,{cube:.45,seed:3,emissive:.5});GL.add(MO.group);
const orbit=new THREE.Mesh(new THREE.TorusGeometry(26,.06,6,160),new THREE.MeshBasicMaterial({color:0x8fd0ff,transparent:true,opacity:.35,toneMapped:false}));orbit.rotation.x=Math.PI/2;GL.add(orbit);
const gS=new THREE.DirectionalLight(0xfff4e0,0);gS.position.set(560,30,60);gS.target=GL;scene.add(gS);
const t1=TL.s1[0],t2=TL.s2[0],t3=TL.s3[0],t4=TL.s4[0],tC=TL.cta[0];
// fase del día (0..1 = 48 h del reloj). El sol tarda 'un día de 48 h' en dar la vuelta: en el gancho se ve MUY lento; en s1 cruza día y noche.
const rate=t=>t<t1?.012:t<t2?.13:t<t3?.03:t<t4?.02:.02;
const phase=(()=>{const N=Math.ceil(J.total*30)+2,a=new Float32Array(N);let p=.30;for(let i=0;i<N;i++){a[i]=p;p+=rate(i/30)/30}return t=>a[Math.min(N-1,Math.floor(t*30))]})();
const RD=J.read||{s3:80.2};
window.renderAt=t=>{const s=segAt(TL,t),lt=t-TL[s][0],d=TL[s][1]-TL[s][0],m=mouthAt(t),k=ss(0,d,lt);
 const beach=s!=='s4';st.visible=beach;hero.g.visible=beach;GL.visible=!beach;sunDisc.visible=sunG.visible=beach;
 for(let i=0;i<60;i++)HAZE.set(i,0,-99,0,0);for(let i=0;i<10;i++)SW.set(i,0,-99,0,0);SN.pts.visible=false;
 let p,q;
 if(beach){let ph=phase(t);if(s==='s2')ph=.25+.2*ss(0,d*.5,lt)+.3*ss(d*.5,d*.8,lt);// s2: tarde de calor → noche fría
  const a=(ph-.25)*6.2832+Math.PI/2;const sy=Math.sin(a),sx=Math.cos(a);const SP=V3(sx*45,sy*42+16,-110);sunDisc.position.copy(SP);sunG.position.copy(SP);
  const day=ss(-.15,.35,sy),dusk=Math.exp(-(((sy-.05)/.18)**2));const c=NIGHT.clone().lerp(DAY,day).lerp(DUSK,dusk*.55);
  let heat=0,cold=0;if(s==='s2'){heat=ss(.2,d*.45,lt)*(1-ss(d*.5,d*.62,lt));cold=ss(d*.6,d*.9,lt)}
  c.lerp(HOT,heat*.35);scene.background=c;scene.fog.color.copy(c);scene.fog.near=70;scene.fog.far=260;
  S.position.set(sx*30,Math.max(4,sy*34),18);S.target.position.set(0,0,2);S.target.updateMatrixWorld();S.intensity=2.7*day+.15;hemi.intensity=.35+1.0*day;ST.material.opacity=1-day;ST.visible=day<.98;
  sea.material.color.setHex(0x1a8ad0).multiplyScalar(.35+.65*day);foam.forEach((f,i)=>{f.position.z=-15.5+Math.sin(t*1.4+i*.7)*.5});
  hand.rotation.z=-(ph%1)*6.2832;
  // termómetro: normal en h/s1, sube con la tarde larga y baja de noche (dibujo: sin cifras)
  setTemp(s==='s2'?(.45+.5*heat-.4*cold):.45);
  if(heat>.05)hz.forEach(([x,b,z],i)=>{const f=(t*.5+b)%1;HAZE.set(i,x,f*6,z+Math.sin(t+i)*.3,heat*(1-f)*1.4)});
  if(heat>.3)for(let i=0;i<10;i++){const f=(t*1.4+i/10)%1;SW.set(i,.6*Math.sin(i*2.1),3.6-f*1.6,2.6+.2*Math.cos(i),.9*(1-f))}
  if(cold>.05){SN.pts.visible=true;SN.pts.material.opacity=.9*cold;SN.draw(t)}
  let kg=80;if(s==='s3')kg=80+(RD.s3-80)*ss(1.0,d*.6,lt);else if(s==='cta')kg=RD.s3;
  disp.set([s==='s3'||s==='cta'?kg.toFixed(1).replace('.',',')+' kg':'80,0 kg']);disp.visible=(s==='s3');scale.visible=disp.visible;dpost.visible=disp.visible;
  hero.g.position.y=scale.visible?.52:0;
  palms.forEach((g,i)=>{g.rotation.z=Math.sin(t*(1.2+i*.1))*.02});
  hero.pose(t,m,{armsUp:s==='s2'?.35*heat:0,wave:s==='cta'?1:0,look:s==='h'?-.4+Math.sin(t*.6)*.2:s==='s1'?-.2:0,point:s==='h'?.7*ss(.6,1.4,lt):s==='s3'?.5*ss(.4,1,lt):0});
  hero.g.rotation.y=s==='h'?-.5:0;hero.g.rotation.z=cold*.04*Math.sin(t*30);
  if(s==='h'){p=V3(-1.0-k*.4,3.6,22-k*2);q=V3(-1.4,4.6,0)}
  else if(s==='s1'){p=V3(-1.5+k*2,3.0,26);q=V3(0,6.6,-2)}
  else if(s==='s2'){p=V3(1.4-k*.6,3.2,22);q=V3(1.4,4.0,0)}
  else if(s==='s3'){p=V3(1.1,3.4,24-k*2);q=V3(1.1,3.2,2)}
  else{p=V3(-1.2,2.6+k*.4,32);q=V3(-1.2,1.7,0)}}
 else{scene.background=SPACE;scene.fog.near=900;scene.fog.far=2000;S.intensity=0;hemi.intensity=.35;gS.intensity=3;ST.visible=true;ST.material.opacity=1;
  const spin=lt*(2.6-1.6*ss(1,d*.8,lt));glb.group.rotation.x=.18;glb.group.rotation.y=spin;
  const ma=lt*.35+1.2;const md=lerp(16,26,ss(.5,d*.8,lt));MO.group.position.set(Math.cos(ma)*md,1.5,Math.sin(ma)*md);MO.group.rotation.y=-ma;orbit.scale.setScalar(md/26);
  p=V3(600+Math.sin(t*.2)*1.2,6+k*3,72-k*8);q=V3(600,-2,0)}
 HAZE.done();SW.done();
 cam.position.copy(p);cam.lookAt(q);r.render(scene,cam)};
function lerp(a,b,x){return a+(b-a)*x}
window.ready=true;
