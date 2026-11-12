// MUNDO DE BLOQUES (motor v15, 04/11): piezas comunes para las escenas 3D. Personajes propios de la cuenta: capataz (casco amarillo) y abuela.
import * as THREE from 'three';
import {RoundedBoxGeometry} from '/node_modules/three/examples/jsm/geometries/RoundedBoxGeometry.js';
export {THREE};
export const W=1080,H=1920;
export const J=await (await fetch('/job.json')).json();
export const mk=s=>()=>{s=(s+0x6D2B79F5)|0;let t=Math.imul(s^s>>>15,1|s);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296};
export const ss=(a,b,x)=>{x=Math.min(1,Math.max(0,(x-a)/(b-a)));return x*x*(3-2*x)};
export const V3=(...a)=>new THREE.Vector3(...a);
export const clamp=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
export function stage({bg=0x7fc8ff,fog=null,fov=35,exposure=1.15,shadow=[0,0,0]}={}){
 const r=new THREE.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});r.setSize(W,H,false);r.setPixelRatio(1);
 r.toneMapping=THREE.ACESFilmicToneMapping;r.toneMappingExposure=exposure;r.shadowMap.enabled=true;r.shadowMap.type=THREE.PCFSoftShadowMap;document.body.prepend(r.domElement);
 const scene=new THREE.Scene();scene.background=new THREE.Color(bg);if(fog)scene.fog=new THREE.Fog(fog[0],fog[1],fog[2]);
 const cam=new THREE.PerspectiveCamera(fov,W/H,.1,500);return{r,scene,cam}}
// sol con sombra suave: la sombra de contacto es lo que más "pega" los personajes al suelo
export function sun(scene,{pos=[-14,26,14],color=0xfff0d8,power=2.6,span=26,target=[0,0,0]}={}){const d=new THREE.DirectionalLight(color,power);d.position.set(...pos);d.target.position.set(...target);scene.add(d.target);d.castShadow=true;d.shadow.mapSize.set(1024,1024);const c=d.shadow.camera;c.left=-span;c.right=span;c.top=span;c.bottom=-span;c.near=1;c.far=120;d.shadow.bias=-.0006;d.shadow.normalBias=.03;scene.add(d);return d}
export const box=(w,h,d,col,rad=.05,opt={})=>{const m=new THREE.Mesh(new RoundedBoxGeometry(w,h,d,2,rad),new THREE.MeshStandardMaterial({color:col,roughness:.72,...opt}));m.castShadow=true;m.receiveShadow=true;return m};
export const glowTex=(()=>{const c=document.createElement('canvas');c.width=c.height=128;const g=c.getContext('2d');const d=g.createRadialGradient(64,64,0,64,64,64);d.addColorStop(0,'rgba(255,255,255,1)');d.addColorStop(.25,'rgba(255,255,255,.45)');d.addColorStop(1,'rgba(255,255,255,0)');g.fillStyle=d;g.fillRect(0,0,128,128);return new THREE.CanvasTexture(c)})();
export const glow=(col,size,op=.8)=>{const s=new THREE.Sprite(new THREE.SpriteMaterial({map:glowTex,color:col,opacity:op,transparent:true,blending:THREE.AdditiveBlending,depthWrite:false}));s.scale.set(size,size,1);return s};
export function pixTex(w,h,draw,rep=[1,1]){const c=document.createElement('canvas');c.width=w;c.height=h;draw(c.getContext('2d'),w,h);const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;t.magFilter=THREE.NearestFilter;t.wrapS=t.wrapT=THREE.RepeatWrapping;t.repeat.set(...rep);return t}
// personaje genérico con piernas y brazos articulados
export function rig({skin,body,legC,shoe}){const g=new THREE.Group(),head=new THREE.Group();head.position.y=3.05;g.add(head);head.add(box(1.5,1.3,1.3,skin,.12));
 const eyes=[-.34,.34].map(x=>{const e=new THREE.Group();const w=box(.34,.4,.05,0xfdf8f0,.02);const p=box(.17,.25,.04,0x15101c,.02);p.position.z=.04;e.add(w,p);e.position.set(x,.14,.66);e.userData.p=p;head.add(e);return e});
 const nose=box(.2,.24,.14,0xc98c58,.05);nose.position.set(0,-.08,.69);head.add(nose);
 const mouth=box(.46,.1,.05,0x4a1a14,.02);mouth.position.set(0,-.38,.66);head.add(mouth);
 const torso=box(1.5,1.5,.95,body,.1);torso.position.y=1.65;g.add(torso);
 const arm=x=>{const a=new THREE.Group();a.position.set(x,2.3,0);const s=box(.44,1.3,.48,body,.08);s.position.y=-.58;const h=box(.46,.4,.5,skin,.08);h.position.y=-1.34;a.add(s,h);g.add(a);return a};
 const leg=x=>{const a=new THREE.Group();a.position.set(x,.95,0);const l=box(.6,.72,.72,legC,.06);l.position.y=-.4;const f=box(.66,.26,.92,shoe,.06);f.position.set(0,-.82,.1);a.add(l,f);g.add(a);return a};
 const o={g,head,eyes,mouth,armL:arm(-1.0),armR:arm(1.0),legL:leg(-.42),legR:leg(.42)};
 // pose: m=boca (0-1), wave, walk (fase o null), look (giro cabeza)
 o.pose=(t,m=0,{wave=0,walk=null,look=0,armsUp=0,point=0}={})=>{mouth.scale.y=1+m*2.4;mouth.position.y=-.38-m*.07;const bl=(t%3.1)>2.96;eyes.forEach(e=>{e.scale.y=bl?.1:1});head.rotation.y=look+Math.sin(t*.9)*.1;head.rotation.x=Math.sin(t*2.6)*.035-m*.05;
  const w=walk===null?0:Math.sin(walk)*.7;o.legL.rotation.x=w;o.legR.rotation.x=-w;
  o.armR.rotation.set(-w*.7,0,.14+Math.sin(t*1.7)*.05);o.armL.rotation.set(w*.7-m*.4,0,-.14-Math.sin(t*1.5)*.05);
  if(wave>0){o.armR.rotation.z=.14+wave*(2.45+.35*Math.sin(t*7))}
  if(armsUp>0){o.armR.rotation.z=.14+armsUp*2.7+Math.sin(t*5)*.12*armsUp;o.armL.rotation.z=-.14-armsUp*2.7-Math.sin(t*5)*.12*armsUp}
  if(point>0){o.armR.rotation.x=-point*1.6;o.armR.rotation.z=.14;o.armR.rotation.x+=Math.sin(t*6)*.12*point}};
 return o}
export function capataz(){const o=rig({skin:0xd9a06a,body:0x1f7a8c,legC:0x154f5c,shoe:0x20161c});const h=o.head;const brim=box(1.9,.14,1.65,0xffc42e,.04);brim.position.set(0,.72,.1);const dome=box(1.5,.5,1.3,0xffc42e,.14);dome.position.y=.98;const ridge=box(.3,.16,1.1,0xf2a800,.05);ridge.position.y=1.28;h.add(brim,dome,ridge);o.hat=[brim,dome,ridge];const hair=box(1.54,.22,.3,0x3a2416,.04);hair.position.set(0,.5,-.55);h.add(hair);[-.34,.34].forEach(x=>{const b=box(.42,.09,.05,0x3a2416,.02);b.position.set(x,.42,.67);h.add(b)});const shirt=box(1,.5,.05,0xf4efe6,.02);shirt.position.set(0,2.15,.47);o.g.add(shirt);const stripe=box(1.54,.14,.99,0xffe25a,.02);stripe.position.y=1.5;o.g.add(stripe);return o}
export function abuela(){const o=rig({skin:0xe3b48c,body:0xb0487f,legC:0x4a4258,shoe:0x2a2230});const h=o.head;const hair=box(1.56,.46,1.36,0xd8d8de,.12);hair.position.y=.56;h.add(hair);const bun=box(.7,.56,.6,0xcfcfd6,.14);bun.position.set(0,.98,-.2);h.add(bun);[-.34,.34].forEach(x=>{const r=new THREE.Mesh(new THREE.TorusGeometry(.26,.04,6,14),new THREE.MeshStandardMaterial({color:0x2a2a38}));r.position.set(x,.14,.71);h.add(r)});const shawl=box(1.56,.42,1.02,0xf2e2c8,.08);shawl.position.y=2.2;o.g.add(shawl);return o}
// cámara por planos: {seg:{p,q}} se encadenan con un fundido corto
export function camera(cam,order,shots,TL,fade=.7){return(t,extra)=>{let p=shots[order[0]].p.clone(),q=shots[order[0]].q.clone();for(const k of order.slice(1)){if(!TL[k])continue;const a=TL[k][0],e=ss(a,a+fade,t);p.lerp(shots[k].p,e);q.lerp(shots[k].q,e)}p.x+=Math.sin(t*.55)*.3;p.y+=Math.sin(t*.8)*.1;if(extra)extra(p,q);cam.position.copy(p);cam.lookAt(q)}}
export const segAt=(TL,t)=>{let s=Object.keys(TL)[0];for(const[k,[a]]of Object.entries(TL))if(t>=a)s=k;return s};
export const mouthAt=t=>J.mouth[Math.min(J.mouth.length-1,Math.floor(t*30))]||0;

// --- v17 (06/11): piezas nuevas reutilizables
// multitud barata: 2 mallas instanciadas (cuerpo+cabeza). set(i,x,y,z,s,ry) y luego done()
export function crowd(scene,n,{s=1,seed=7,pal=[0xe5343f,0x2a7de1,0xf2c230,0x34b56a,0xf2f2f2,0x8a5cd6,0xff7a2e,0x20c4c4,0xd94f9a,0x39424e],skins=[0xe3b48c,0xd9a06a,0xa8724a,0x7a4e2e,0xf0cba8]}={}){
 const R=mk(seed),bm=new THREE.MeshStandardMaterial({roughness:.8}),hm=new THREE.MeshStandardMaterial({roughness:.8});
 const body=new THREE.InstancedMesh(new THREE.BoxGeometry(1.1,1.9,.8),bm,n),head=new THREE.InstancedMesh(new THREE.BoxGeometry(.9,.85,.85),hm,n);body.frustumCulled=head.frustumCulled=false;body.castShadow=true;
 const C=new THREE.Color();for(let i=0;i<n;i++){C.setHex(pal[Math.floor(R()*pal.length)]);body.setColorAt(i,C);C.setHex(skins[Math.floor(R()*skins.length)]);head.setColorAt(i,C)}
 scene.add(body,head);const O=new THREE.Object3D();
 return{body,head,set(i,x,y,z,k=s,ry=0){O.position.set(x,y+.95*k,z);O.rotation.set(0,ry,0);O.scale.setScalar(k);O.updateMatrix();body.setMatrixAt(i,O.matrix);O.position.y=y+2.3*k;O.updateMatrix();head.setMatrixAt(i,O.matrix)},done(){body.instanceMatrix.needsUpdate=true;head.instanceMatrix.needsUpdate=true}}}
// partículas de cubos sin sombra: set(i,x,y,z,s) ; color por instancia opcional
export function puffs(scene,n,size,col,opt={}){const m=new THREE.InstancedMesh(new THREE.BoxGeometry(size,size,size),new THREE.MeshBasicMaterial({color:col,toneMapped:false,transparent:true,...opt}),n);m.frustumCulled=false;scene.add(m);const O=new THREE.Object3D();return{m,set(i,x,y,z,s=1,w=0){O.position.set(x,y,z);O.rotation.set(w,w*.7,0);O.scale.setScalar(s);O.updateMatrix();m.setMatrixAt(i,O.matrix)},done(){m.instanceMatrix.needsUpdate=true}}}
// nieve que cae determinista en una caja
export function snow(scene,n,[x0,x1,y1,z0,z1],{size=.22,seed=3,col=0xffffff,speed=2.2}={}){const R=mk(seed),P=[];for(let i=0;i<n;i++)P.push([x0+R()*(x1-x0),R()*y1,z0+R()*(z1-z0),.7+R()*.6,R()*9]);const g=new THREE.BufferGeometry(),a=new Float32Array(n*3);g.setAttribute('position',new THREE.BufferAttribute(a,3));const pts=new THREE.Points(g,new THREE.PointsMaterial({color:col,size,transparent:true,opacity:.9}));pts.frustumCulled=false;scene.add(pts);return{pts,draw(t){P.forEach((p,i)=>{a[i*3]=p[0]+Math.sin(t*.7+p[4])*.7;a[i*3+1]=y1-((p[1]+t*speed*p[3])%y1);a[i*3+2]=p[2]});g.attributes.position.needsUpdate=true}}}

// --- v18 (07/11): gráficos integrados en la escena y piezas nuevas reutilizables
// rótulo 3D (panel con texto dibujado en canvas): l=label3d(['25 cm'],{w:6,h:2}); l.set(['26 cm']) lo redibuja. sprite=true lo pone siempre de cara a cámara
export function label3d(lines,{w=6,h=2,bg='#10131f',fg='#ffffff',accent='#ffc23a',px=96,sprite=false,glowOn=true}={}){const c=document.createElement('canvas');c.width=1024;c.height=Math.round(1024*h/w);const g=c.getContext('2d');const tex=new THREE.CanvasTexture(c);tex.colorSpace=THREE.SRGBColorSpace;tex.anisotropy=8;
 const draw=L=>{g.clearRect(0,0,c.width,c.height);if(bg){g.fillStyle=bg;const r=40;g.beginPath();g.roundRect(6,6,c.width-12,c.height-12,r);g.fill();g.lineWidth=12;g.strokeStyle=accent;g.stroke()}g.textAlign='center';g.textBaseline='middle';const n=L.length;L.forEach((s,i)=>{const hi=s.startsWith('*');s=hi?s.slice(1):s;g.font=`900 ${px}px sans-serif`;let f=px;while(g.measureText(s).width>c.width-80&&f>20){f-=4;g.font=`900 ${f}px sans-serif`}if(!bg){g.lineJoin='round';g.lineWidth=Math.max(6,f*.09);g.strokeStyle='#10131f';g.strokeText(s,c.width/2,c.height*(i+.5)/n)}g.fillStyle=hi?accent:fg;g.fillText(s,c.width/2,c.height*(i+.5)/n)});tex.needsUpdate=true};draw(lines);
 let o;if(sprite){o=new THREE.Sprite(new THREE.SpriteMaterial({map:tex,transparent:true,toneMapped:false,depthTest:false}));o.scale.set(w,h,1);o.renderOrder=9}else{o=new THREE.Mesh(new THREE.PlaneGeometry(w,h),new THREE.MeshBasicMaterial({map:tex,transparent:true,toneMapped:false,side:THREE.DoubleSide}))}
 if(glowOn&&bg){}o.userData.set=draw;let last='';o.set=L=>{const k=L.join('|');if(k!==last){last=k;draw(L)}};return o}
// regla vertical de bloques con marcas cada 'step' (unidades de escena) y etiquetas
export function ruler(height,{step=.5,every=2,unit=10,label='cm',col=0xffd23a,ls=1}={}){const g=new THREE.Group();const b=box(.36*ls,height,.2*ls,col,.03*ls);b.position.y=height/2;g.add(b);for(let i=0;i*step<=height+1e-6;i++){const big=i%every===0;const m=box((big?.8:.5)*ls,.07*ls,.24*ls,0x10131f,.01*ls);m.position.set((big?.22:.1)*ls,i*step,.02);g.add(m);if(big){const l=label3d([`${i*unit} ${label}`],{w:2.2*ls,h:.6*ls,bg:null,fg:'#ffffff',px:200});l.position.set(1.7*ls,i*step,.05);g.add(l)}}return g}
// avión de bloques (caza de hélice): devuelve {g,prop}
export function plane({body=0x5b6b4a,wing=0x4b5a3c,accent=0xd8d0b8}={}){const g=new THREE.Group();const f=box(1.4,1.2,6.4,body,.3);g.add(f);const n=box(1.1,1,.6,0x2a2a30,.2);n.position.z=3.4;g.add(n);const w=box(9.5,.25,1.8,wing,.08);w.position.set(0,-.1,.6);g.add(w);const tw=box(3.6,.2,1,wing,.05);tw.position.set(0,.2,-2.9);g.add(tw);const fin=box(.2,1.4,1.1,wing,.05);fin.position.set(0,.9,-2.9);g.add(fin);const cab=box(.9,.6,1.4,0x9fd8ff,.2,{metalness:.3,roughness:.2});cab.position.set(0,.75,.6);g.add(cab);[-3.4,3.4].forEach(x=>{const r=box(.9,.06,.9,accent,.02);r.position.set(x,.08,.6);g.add(r);const r2=box(.45,.08,.45,0xc02028,.02);r2.position.set(x,.1,.6);g.add(r2)});const prop=new THREE.Group();prop.position.z=3.75;[0,1].forEach(k=>{const p=box(.18,2.4,.08,0x1a1a1a,.04);p.rotation.z=k*Math.PI/2;prop.add(p)});g.add(prop);return{g,prop}}
// cielo estrellado (esfera de puntos)
export function stars(scene,n=900,{r0=140,r1=180,seed=11,size=.7}={}){const R=mk(seed),p=new Float32Array(n*3);for(let i=0;i<n;i++){const a=R()*6.283,b=Math.acos(2*R()-1),d=r0+R()*(r1-r0);p[i*3]=d*Math.sin(b)*Math.cos(a);p[i*3+1]=d*Math.cos(b);p[i*3+2]=d*Math.sin(b)*Math.sin(a)}const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.BufferAttribute(p,3));const s=new THREE.Points(g,new THREE.PointsMaterial({color:0xffffff,size,sizeAttenuation:true}));scene.add(s);return s}
// globo terráqueo de cubos (Fibonacci): g.group, g.draw() ; landK umbral de tierra
export function voxGlobe(n=9000,rad=10,{cube=.5,seed=0}={}){const grp=new THREE.Group();const noise=(x,y,z)=>Math.sin(x*3.1+1.3+seed)*Math.cos(y*3.7-.7)+Math.sin(y*2.9+z*4.3)*.8+Math.cos(z*3.3-x*2.7+2)*.7+Math.sin(x*6.7+z*5.1)*.3;const im=new THREE.InstancedMesh(new THREE.BoxGeometry(cube,cube,cube),new THREE.MeshStandardMaterial({roughness:.6}),n);im.frustumCulled=false;grp.add(im);const O=new THREE.Object3D(),C=new THREE.Color();for(let i=0;i<n;i++){const y=1-2*(i+.5)/n,r=Math.sqrt(1-y*y),a=i*Math.PI*(3-Math.sqrt(5));const x=Math.cos(a)*r,z=Math.sin(a)*r;const land=noise(x,y,z)>.55;const h=rad+(land?.22:0);C.setHex(Math.abs(y)>.92?0xeef6ff:land?(i%3?0x58a84a:0x4f9842):(i%2?0x1467c8:0x0c4fae));C.multiplyScalar(.92+((i*7)%5)*.03);im.setColorAt(i,C);O.position.set(x*h,y*h,z*h);O.lookAt(0,0,0);O.updateMatrix();im.setMatrixAt(i,O.matrix)}const atm=glow(0x7fc8ff,rad*2.9,.35);grp.add(atm);return{group:grp,im}}

// --- v19 (08/11): plantilla de cubo que se pliega de verdad. net=[[col,row],...] (6 celdas), cols=['#hex'], base=celda fija. Bisagras anidadas (mismo árbol BFS que el assert de Python).
// fold(f) 0..1 pliega por profundidad (las de fuera esperan a las de dentro); faces[i].mesh para posiciones en mundo.
export function foldNet(net,cols,base,S=2.5,{th=.16,stagger=.55}={}){const key=c=>c[0]+','+c[1];const idx=new Map(net.map((c,i)=>[key(c),i]));const par=new Map([[base,null]]);const order=[base];const qu=[base];
 while(qu.length){const u=qu.shift();for(const d of [[1,0],[-1,0],[0,1],[0,-1]]){const v=idx.get(key([net[u][0]+d[0],net[u][1]+d[1]]));if(v!==undefined&&!par.has(v)){par.set(v,[u,d]);order.push(v);qu.push(v)}}}
 if(order.length!==6)throw new Error('plantilla no válida');
 const root=new THREE.Group();const faces=[];const mkFace=i=>{const g=new THREE.Group();const m=box(S*.96,th,S*.96,new THREE.Color(cols[i]).getHex(),.08);g.add(m);const e=box(S*.6,th*1.05,S*.6,new THREE.Color(cols[i]).multiplyScalar(1.12).getHex(),.06);e.position.y=.01;g.add(e);return{g,mesh:m,depth:0,hinge:null}};
 faces[base]=mkFace(base);root.add(faces[base].g);
 for(const v of order.slice(1)){const[u,d]=par.get(v);const F=mkFace(v);F.depth=faces[u].depth+1;const h=new THREE.Group();h.position.set(d[0]*S/2,0,d[1]*S/2);F.g.position.set(d[0]*S/2,0,d[1]*S/2);h.add(F.g);faces[u].g.add(h);F.hinge=h;F.axis=d[0]===1?['z',1]:d[0]===-1?['z',-1]:d[1]===1?['x',-1]:['x',1];faces[v]=F}
 const maxD=Math.max(...faces.map(f=>f.depth));
 return{root,faces,order,fold(f){faces.forEach(F=>{if(!F.hinge)return;const a=(F.depth-1)/maxD*stagger,b=a+(1-stagger*(maxD-1)/maxD);const k=ss(a,Math.min(1,b),f);F.hinge.rotation.set(0,0,0);F.hinge.rotation[F.axis[0]]=F.axis[1]*k*Math.PI/2})},center(){return root.position.clone().add(V3(0,S/2,0))}}}
// anillos (v19): textura de bandas concéntricas para RingGeometry (UV plano), sistema de anillos para un globo y arco de anillos en el cielo
export function bandTex(inner,{seed=5,pal=['#f2e2b8','#d9c294','#f6ecd0','#c8ae7c','#e8d8b0','#bfa77a']}={}){const c=document.createElement('canvas');c.width=c.height=1024;const g=c.getContext('2d');const q=mk(seed);let rr=inner*512;while(rr<512){const w=4+q()*26;g.beginPath();g.arc(512,512,Math.min(512,rr+w),0,6.2832);g.arc(512,512,rr,0,6.2832,true);g.fillStyle=pal[Math.floor(q()*pal.length)];g.globalAlpha=.35+q()*.6;g.fill();rr+=w+(q()<.15?6+q()*14:0)}const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;return t}
export function ringSystem({r0=13,r1=22,op=.85,seed=5}={}){const g=new THREE.Group();const m=new THREE.Mesh(new THREE.RingGeometry(r0,r1,160,1),new THREE.MeshBasicMaterial({map:bandTex(r0/r1,{seed}),transparent:true,opacity:op,side:THREE.DoubleSide,depthWrite:false}));m.rotation.x=-Math.PI/2;g.add(m);return{g,m}}
export function skyArch({r=520,w=90,center=[0,-330,-620],tilt=-.3,seed=5}={}){const g=new THREE.Group();g.position.set(...center);g.rotation.x=tilt;
 const mat=new THREE.MeshBasicMaterial({map:bandTex((r-w)/r,{seed}),transparent:true,opacity:.8,side:THREE.DoubleSide,fog:false,depthWrite:false,toneMapped:false});const m=new THREE.Mesh(new THREE.RingGeometry(r-w,r,256,1,0,Math.PI),mat);g.add(m);
 const sh=new THREE.Mesh(new THREE.RingGeometry(r-w-2,r+2,64,1,Math.PI/2-.11,.22),new THREE.MeshBasicMaterial({color:0x02030a,transparent:true,opacity:0,fog:false,depthWrite:false,side:THREE.DoubleSide}));sh.position.z=.5;sh.renderOrder=3;m.renderOrder=1;g.add(sh);
 return{g,draw(t,{night=0,gap=0}={}){mat.opacity=.85+.15*night;mat.color.setScalar(1+.25*night);sh.material.opacity=.85*gap}}}
// v23 (12/11): ARAÑA de bloques (personaje propio, diseño de la cuenta: cuerpo granate con rombo naranja, 8 ojos brillantes) y CAMA reutilizable.
// spider(s): o.g, o.walk(fase) anda con marcha alterna de 4+4 patas, o.freeze(k) encoge las patas (susto), o.wave(t) saluda con una pata delantera.
export function spider(s=1){const g=new THREE.Group();const body=new THREE.Group();g.add(body);body.position.y=.9;
 const ab=box(1.5,1.1,1.8,0x5a1e24,.4);ab.position.set(0,.25,-1.05);body.add(ab);const mark=box(.6,.08,.6,0xff8a2a,.05,{emissive:0xff6a10,emissiveIntensity:.35});mark.position.set(0,.82,-1.05);mark.rotation.y=Math.PI/4;body.add(mark);
 const ce=box(1.05,.75,1.05,0x3a1418,.3);ce.position.set(0,.1,.2);body.add(ce);
 const eyes=[];[[-.22,.32,.74,.13],[.22,.32,.74,.13],[-.42,.22,.68,.08],[.42,.22,.68,.08],[-.12,.5,.66,.07],[.12,.5,.66,.07],[-.3,.5,.6,.06],[.3,.5,.6,.06]].forEach(([x,y,z,r])=>{const e=new THREE.Mesh(new THREE.SphereGeometry(r,10,8),new THREE.MeshBasicMaterial({color:0xfff4e0,toneMapped:false}));e.position.set(x,y,z);body.add(e);eyes.push(e)});
 [-1,1].forEach(x=>{const f=box(.16,.32,.16,0x2a0e10,.04);f.position.set(x*.14,-.18,.72);body.add(f)});
 const legs=[];for(let side of[-1,1])for(let i=0;i<4;i++){const hip=new THREE.Group();hip.position.set(side*.45,.05,.55-i*.36);hip.rotation.y=side*(-.75+i*.5)+(side<0?Math.PI:0);body.add(hip);
  const up=new THREE.Group();up.rotation.z=.75;hip.add(up);const u=box(1.15,.16,.16,0x3a1418,.05);u.position.x=.55;up.add(u);
  const kn=new THREE.Group();kn.position.x=1.12;up.add(kn);kn.rotation.z=-1.9;const l=box(1.35,.13,.13,0x2a0e10,.05);l.position.x=.66;kn.add(l);
  legs.push({hip,up,kn,side,i,base:hip.rotation.y})}
 g.scale.setScalar(s);
 const o={g,body,eyes,legs,walk(ph){legs.forEach(L=>{const p=ph+((L.i+(L.side>0?1:0))%2)*Math.PI;L.hip.rotation.y=L.base+Math.sin(p)*.28;L.up.rotation.z=.75+Math.max(0,Math.cos(p))*.35;L.kn.rotation.z=-1.9});body.position.y=.9+Math.abs(Math.sin(ph*2))*.05},
  freeze(k){legs.forEach(L=>{L.up.rotation.z=.75+.55*k;L.kn.rotation.z=-1.9-.6*k});body.position.y=.9-.35*k},
  wave(t){const L=legs[0];L.up.rotation.z=1.6+Math.sin(t*7)*.35;L.kn.rotation.z=-1.1}};
 return o}
export function bed(col=0x3a6fd8){const g=new THREE.Group();const fr=box(4.4,.8,7,0x7a4e2e,.08);fr.position.y=.6;g.add(fr);const mat=box(4.1,.5,6.6,0xf2efe8,.15);mat.position.y=1.2;g.add(mat);
 const hb=box(4.6,3,.4,0x7a4e2e,.1);hb.position.set(0,1.6,-3.4);g.add(hb);const pil=box(2.6,.5,1.3,0xffffff,.22);pil.position.set(0,1.65,-2.4);g.add(pil);return g}
// persona TUMBADA boca arriba sobre una cama de bed() (cabeza en la almohada); devuelve la manta para animar la respiración
export function lieDown(o,B,col=0x3a6fd8){o.g.rotation.x=-Math.PI/2;o.g.position.set(0,1.92,1.25);B.add(o.g);const bl=box(4.3,.9,4.6,col,.25);bl.position.set(0,2.15,1.15);B.add(bl);const fold=box(4.32,.92,.6,0xf4f4f4,.22);fold.position.set(0,2.17,-1.05);B.add(fold);return{blanket:bl,fold}}
