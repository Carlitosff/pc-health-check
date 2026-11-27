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
// v27: MOSQUITO de bloques (personaje propio, rayado blanco y negro): alas que baten, patas largas con bandas, trompa. o.buzz(t) bate alas;
// swarmPos(i,t,c,rx,ry,rz) da una trayectoria de zumbido determinista alrededor de c (para enjambres).
export function mosquito(s=1){const g=new THREE.Group();const D=0x2a2622,Wt=0xf2f2ee;
 const th=box(.5,.46,.56,D,.14);g.add(th);[-.12,.12].forEach(x=>{const m=box(.05,.3,.05,Wt,.01);m.position.set(x,.2,.12);g.add(m)});
 const ab=new THREE.Group();ab.position.set(0,.02,-.25);ab.rotation.x=-.18;g.add(ab);const a=box(.34,.3,1.25,D,.12);a.position.z=-.62;ab.add(a);
 for(let i=0;i<4;i++){const b=box(.36,.32,.07,Wt,.02);b.position.z=-.3-i*.26;ab.add(b)}
 const hd=box(.34,.32,.3,D,.1);hd.position.set(0,-.02,.42);g.add(hd);[-1,1].forEach(x=>{const e=box(.13,.18,.16,0x8a1418,.04,{emissive:0x4a0808,emissiveIntensity:.5});e.position.set(x*.13,0,.48);g.add(e)});
 const pr=box(.05,.05,.85,0x1a1612,.01);pr.position.set(0,-.18,.88);pr.rotation.x=.45;g.add(pr);[-1,1].forEach(x=>{const an=box(.03,.03,.45,0x1a1612,.01);an.position.set(x*.1,.08,.7);an.rotation.set(-.5,x*.35,0);g.add(an)});
 const legs=[];for(const sd of[-1,1])for(let i=0;i<3;i++){const hip=new THREE.Group();hip.position.set(sd*.2,-.18,.15-i*.18);hip.rotation.set(0,sd*(.5-i*.5)+(sd<0?Math.PI:0),.75);g.add(hip);
  const u=box(.85,.05,.05,D,.01);u.position.x=.42;hip.add(u);const kn=new THREE.Group();kn.position.x=.84;kn.rotation.z=-1.6;hip.add(kn);const l=box(1.05,.045,.045,D,.01);l.position.x=.52;kn.add(l);
  for(let k=0;k<3;k++){const w=box(.07,.06,.06,Wt,.01);w.position.x=.22+k*.32;kn.add(w)}legs.push(hip)}
 const wm=new THREE.MeshStandardMaterial({color:0xcfe6ff,transparent:true,opacity:.42,roughness:.2,side:THREE.DoubleSide,depthWrite:false});
 const wings=[-1,1].map(sd=>{const p=new THREE.Group();p.position.set(sd*.18,.24,-.05);const w=new THREE.Mesh(new THREE.PlaneGeometry(1.25,.36),wm);w.rotation.x=-Math.PI/2;w.position.x=sd*.62;p.add(w);g.add(p);p.userData.sd=sd;return p});
 g.scale.setScalar(s);const o={g,wings,legs,buzz(t){wings.forEach(p=>{p.rotation.z=p.userData.sd*(.25+.55*Math.sin(t*95));p.rotation.y=-p.userData.sd*.35})}};return o}
export const swarmPos=(i,t,c,rx=1.5,ry=1,rz=1.2)=>{const a=1.3+i*.37,b=.9+i*.23,ph=i*2.1;return new THREE.Vector3(c.x+rx*Math.sin(t*a+ph)*Math.cos(t*.31*b+i),c.y+ry*Math.sin(t*b*1.4+ph*1.7),c.z+rz*Math.cos(t*a*.8+ph))};
// v28 (17/11): PLANETA DE CUBOS CORTADO: corteza de `layers` capas (Fibonacci), cuña abierta entre los ángulos cut=[a0,a1] (en y),
// cara interior de roca y colores propios para esferas internas. Devuelve {group, im}. Sirve para 'por dentro de la Tierra', capas, núcleos.
export function voxShell({n=5000,rad=10,layers=3,cube=.55,cut=[0,Math.PI/2],cols=null,land=true,seed=0}={}){const grp=new THREE.Group();const noise=(x,y,z)=>Math.sin(x*3.1+1.3+seed)*Math.cos(y*3.7-.7)+Math.sin(y*2.9+z*4.3)*.8+Math.cos(z*3.3-x*2.7+2)*.7;
 const P=[];for(let L=0;L<layers;L++){const rr=rad-L*cube*.95;const nn=Math.round(n*(rr/rad)**2);for(let i=0;i<nn;i++){const y=1-2*(i+.5)/nn,r=Math.sqrt(1-y*y),a=i*Math.PI*(3-Math.sqrt(5));const x=Math.cos(a)*r,z=Math.sin(a)*r;let ang=Math.atan2(z,x);if(ang<0)ang+=6.283;if(ang>=cut[0]&&ang<=cut[1])continue;P.push([x,y,z,rr,L,i])}}
 const im=new THREE.InstancedMesh(new THREE.BoxGeometry(cube,cube,cube),new THREE.MeshStandardMaterial({roughness:.7}),P.length);im.frustumCulled=false;grp.add(im);const O=new THREE.Object3D(),C=new THREE.Color();
 P.forEach(([x,y,z,rr,L,i],k)=>{if(L>0)C.setHex(L===1?0x8a5a36:0x6a4428);else if(cols)C.setHex(cols[i%cols.length]);else{const ld=land&&noise(x,y,z)>.55;C.setHex(Math.abs(y)>.92?0xeef6ff:ld?(i%3?0x58a84a:0x4f9842):(i%2?0x1467c8:0x0c4fae))}C.multiplyScalar(.9+((i*7)%5)*.03);im.setColorAt(k,C);O.position.set(x*rr,y*rr,z*rr);O.lookAt(0,0,0);O.updateMatrix();im.setMatrixAt(k,O.matrix)});
 // caras del corte: dos medios discos de roca que tapan el grosor de la corteza
 const capM=new THREE.MeshStandardMaterial({color:0x7a5034,roughness:1,side:THREE.DoubleSide});[cut[0],cut[1]].forEach(a=>{const g=new THREE.RingGeometry(rad-layers*cube*.95,rad+cube*.4,48,1,-Math.PI/2,Math.PI);const m=new THREE.Mesh(g,capM);m.rotation.y=-a;grp.add(m)});
 return{group:grp,im}}
// v29 (18/11): SAPO de bloques (personaje propio nº 5): cuerpo achatado con BULTOS (glándulas de la piel, no verrugas), dos GLÁNDULAS PAROTOIDES
// grandes detrás de los ojos (o.paro, se pueden iluminar), ojos dorados con pupila horizontal que parpadean, buche que respira y SALTO con arco.
// o.pose(t,{hop:0..1 fase del salto, breathe:1, glow:0..1 bultos, paro:0..1 parotoides}). Mide ~2,4 u de largo con s=1.
export function toad(s=1,{col=0x7a7a3a,belly=0xd8c890,wart=0x5e5a2a}={}){const g=new THREE.Group();const b=new THREE.Group();g.add(b);g.scale.setScalar(s);
 const mt=c=>new THREE.MeshStandardMaterial({color:c,roughness:.75});const body=new THREE.Mesh(new THREE.SphereGeometry(1,24,16),mt(col));body.scale.set(1.15,.62,1.25);body.position.y=.72;b.add(body);
 const bel=new THREE.Mesh(new THREE.SphereGeometry(1,20,12),mt(belly));bel.scale.set(1.0,.45,1.05);bel.position.set(0,.55,.12);b.add(bel);
 const head=new THREE.Mesh(new THREE.SphereGeometry(.8,20,14),mt(col));head.scale.set(1.1,.62,.9);head.position.set(0,.95,.95);b.add(head);
 const throat=new THREE.Mesh(new THREE.SphereGeometry(.5,16,10),mt(belly));throat.scale.set(1,.55,.8);throat.position.set(0,.55,1.25);b.add(throat);
 const R=mk(505);const warts=[];const wm=new THREE.MeshStandardMaterial({color:wart,roughness:.7,emissive:0x4de3ff,emissiveIntensity:0});
 for(let i=0;i<46;i++){const a=R()*6.28,u=.25+R()*.7;const x=Math.cos(a)*1.1*u,z=Math.sin(a)*1.2*u-.1;const y=.72+.62*Math.sqrt(Math.max(0,1-(x/1.15)**2-(z/1.25)**2))-.02;const w=new THREE.Mesh(new THREE.SphereGeometry(.07+R()*.07,8,6),wm);w.position.set(x,y,z);b.add(w);warts.push(w)}
 const pm=new THREE.MeshStandardMaterial({color:0x8a7a3a,roughness:.6,emissive:0xff6a2a,emissiveIntensity:0});const paro=[-1,1].map(d=>{const p=new THREE.Mesh(new THREE.SphereGeometry(.3,14,10),pm);p.scale.set(.75,.55,1.5);p.position.set(d*.48,1.28,.45);p.rotation.y=d*.35;b.add(p);return p});
 const eyes=[-1,1].map(d=>{const e=new THREE.Group();const ball=new THREE.Mesh(new THREE.SphereGeometry(.24,16,12),new THREE.MeshStandardMaterial({color:0xe0a820,emissive:0x5a3a00,roughness:.25}));const pu=box(.3,.07,.05,0x0a0a0a,.02);pu.position.z=.22;const lid=new THREE.Mesh(new THREE.SphereGeometry(.26,14,8,0,6.29,0,1.6),mt(col));lid.rotation.x=-.4;e.add(ball,pu,lid);e.position.set(d*.42,1.32,1.2);e.userData.lid=lid;b.add(e);return e});
 const legs=[];[[-1,1],[1,1],[-1,-1],[1,-1]].forEach(([dx,dz])=>{const l=new THREE.Group();const th=box(.42,.32,.8,col,.12);th.position.set(0,.1,0);const ft=box(.5,.1,.45,belly,.04);ft.position.set(dx*.12,-.12,.32*dz+(dz>0?.1:.25));l.add(th,ft);l.position.set(dx*.95,.3,dz*.7);b.add(l);legs.push(l)});
 const o={g,b,paro,warts,eyes,legs};
 o.pose=(t,{hop=null,breathe=1,glow=0,paro:pg=0}={})=>{throat.scale.y=.55+.12*breathe*Math.max(0,Math.sin(t*5));const bl=(t%3.7)>3.55;eyes.forEach(e=>{e.userData.lid.rotation.x=bl?.9:-.4});
  wm.emissiveIntensity=glow*(1.1+.5*Math.sin(t*6));pm.emissiveIntensity=pg*(1.3+.6*Math.sin(t*5));
  if(hop!==null){const u=hop%1;b.position.y=Math.sin(Math.PI*u)*1.4;b.rotation.x=-Math.sin(Math.PI*2*u)*.25;legs.forEach((l,i)=>{l.rotation.x=(i>1?1:.4)*Math.sin(Math.PI*u)*-.9})}else{b.position.y=0;b.rotation.x=0}};
 return o}

// --- v31 (20/11): MANO DE BLOQUES articulada con modo RAYOS X (reutilizable para cualquier vídeo de manos, dedos, huesos o articulaciones)
// h=hand(+1|-1,{skin}) → h.g (grupo; dedos hacia +y, dorso hacia +z). h.curl(k[,i]) dobla (0–1) todos los dedos o el i (0 índice … 3 meñique);
// h.xray(k) vuelve la piel azul translúcida y enseña los huesos; h.knuckles = 4 objetos en los nudillos (getWorldPosition para chispas).
export function hand(side=1,{skin=0xd9a06a,bone=0xf4f6ff,blue=0x4aa8ff}={}){const g=new THREE.Group();const skins=[],bones=[];
 const sm=()=>{const m=new THREE.MeshStandardMaterial({color:skin,roughness:.65,transparent:true,opacity:1});skins.push(m);return m};
 const seg=(w,h,d,par,y)=>{const m=new THREE.Mesh(new RoundedBoxGeometry(w,h,d,2,Math.min(w,d)*.22),sm());m.castShadow=true;m.position.y=h/2;par.add(m);
  const b=new THREE.Mesh(new RoundedBoxGeometry(w*.42,h*.84,d*.42,2,.06),new THREE.MeshBasicMaterial({color:bone,toneMapped:false,transparent:true,opacity:0}));b.position.y=h/2;b.renderOrder=3;par.add(b);bones.push(b);return m};
 const palm=new THREE.Group();g.add(palm);seg(3.1,3.3,1.05,palm);palm.children[0].position.y=0;palm.children[1].position.y=0;
 const wrist=new THREE.Group();wrist.position.y=-1.65;g.add(wrist);const wr=seg(2.5,1.6,.95,wrist);wr.position.y=-.8;wrist.children[1].position.y=-.8;
 const fingers=[],knuckles=[],L=[[1.25,.85,.7],[1.45,.95,.75],[1.35,.9,.7],[1.0,.7,.6]];
 [-1.13,-.38,.38,1.13].forEach((x,i)=>{let par=palm;const js=[];L[i].forEach((len,k)=>{const j=new THREE.Group();j.position.set(k?0:x*side,k?L[i][k-1]:1.65,0);par.add(j);seg(.66-k*.05,len,.78-k*.05,j);js.push(j);par=j});
  const kn=new THREE.Mesh(new THREE.BoxGeometry(.5,.3,.2),sm());kn.position.set(x*side,1.62,.52);palm.add(kn);knuckles.push(kn);fingers.push(js)});
 const th=new THREE.Group();th.position.set(-1.55*side,-.5,.1);th.rotation.z=.4*side;palm.add(th);const t1=new THREE.Group();th.add(t1);seg(.74,1.05,.8,t1);const t2=new THREE.Group();t2.position.y=1.05;t1.add(t2);seg(.68,.8,.74,t2);
 const o={g,fingers,knuckles,thumb:[t1,t2],palm};
 o.curl=(k,i=null)=>{(i===null?[0,1,2,3]:[i]).forEach(n=>{const js=fingers[n];js[0].rotation.x=-1.45*k;js[1].rotation.x=-1.6*k;js[2].rotation.x=-1.2*k});};
 o.xray=k=>{const C=new THREE.Color(skin).lerp(new THREE.Color(blue),k);skins.forEach(m=>{m.color.copy(C);m.opacity=1-.72*k;m.emissive=new THREE.Color(blue);m.emissiveIntensity=.35*k;m.depthWrite=k<.5});bones.forEach(b=>b.material.opacity=k)};
 return o}
// v32 (21/11): CANASTA de baloncesto a escala (aro a 3,05 m; U = metros por unidad de escena), VASO de cristal transparente,
// VELA con llama que parpadea y luz puntual que tiembla (c.tick(t)), y RELOJ DE PARED analógico (k.set(horas)) para escenas de noche.
export function hoop(U=1.75/4.1){const g=new THREE.Group();const H=3.05/U;const pole=box(.35,H+.8,.35,0x4a4f5c,.05);pole.position.set(0,(H+.8)/2,-2.2);g.add(pole);
 const arm=box(.3,.3,1.8,0x4a4f5c,.04);arm.position.set(0,H+.6,-1.4);g.add(arm);const bd=box(4.2,2.6,.15,0xf6f6f6,.05);bd.position.set(0,H+1.1,-.5);g.add(bd);
 const sq=box(1.5,1.1,.17,0xe0343a,.02);sq.position.set(0,H+.85,-.49);g.add(sq);const sq2=box(1.2,.8,.18,0xf6f6f6,.02);sq2.position.set(0,H+.85,-.48);g.add(sq2);
 const rim=new THREE.Mesh(new THREE.TorusGeometry(.62,.07,8,24),new THREE.MeshStandardMaterial({color:0xff6a1a,roughness:.4}));rim.rotation.x=Math.PI/2;rim.position.set(0,H,.25);g.add(rim);
 for(let i=0;i<10;i++){const a=i/10*Math.PI*2;const n=box(.05,.9,.05,0xffffff,.01);n.position.set(Math.cos(a)*.52,H-.45,.25+Math.sin(a)*.52);n.rotation.z=Math.cos(a)*.15;g.add(n)}g.userData.H=H;return g}
export function glassCup(col=0x9ad8ff){const g=new THREE.Group();const m=new THREE.MeshStandardMaterial({color:col,transparent:true,opacity:.45,roughness:.05,metalness:.1});
 const c=new THREE.Mesh(new THREE.CylinderGeometry(.42,.34,1.1,16,1,true),m);c.position.y=.55;g.add(c);const b=new THREE.Mesh(new THREE.CylinderGeometry(.34,.34,.08,16),m);b.position.y=.04;g.add(b);
 const w=new THREE.Mesh(new THREE.CylinderGeometry(.38,.33,.6,16),new THREE.MeshStandardMaterial({color:0x4aa8ff,transparent:true,opacity:.6,roughness:.1}));w.position.y=.34;g.add(w);return g}
export function candle(scene,{h=1.2,col=0xf2e8d0}={}){const g=new THREE.Group();const plate=box(1.1,.12,1.1,0xb8902a,.04);plate.position.y=.06;g.add(plate);const wax=box(.42,h,.42,col,.05);wax.position.y=.12+h/2;g.add(wax);
 const fl=new THREE.Mesh(new THREE.ConeGeometry(.13,.42,8),new THREE.MeshBasicMaterial({color:0xffc04a,toneMapped:false}));fl.position.y=.12+h+.25;g.add(fl);const gl=glow(0xffa040,2.6,.85);gl.position.y=.12+h+.28;g.add(gl);
 const L=new THREE.PointLight(0xffa850,24,16,1.6);L.position.y=.12+h+.4;g.add(L);
 const o={g,light:L,tick(t,on=1){const f=.85+.1*Math.sin(t*23)+.06*Math.sin(t*41+1.3);fl.scale.set(1,f,1);fl.visible=gl.visible=on>0;L.intensity=24*f*on;gl.material.opacity=.85*f*on;fl.rotation.z=.08*Math.sin(t*7)}};return o}
export function wallClock(R=1.2){const g=new THREE.Group();const face=new THREE.Mesh(new THREE.CylinderGeometry(R,R,.2,32),new THREE.MeshStandardMaterial({color:0xf4efe2,roughness:.6}));face.rotation.x=Math.PI/2;g.add(face);
 const rim=new THREE.Mesh(new THREE.TorusGeometry(R,.1,8,32),new THREE.MeshStandardMaterial({color:0x6a4a30}));g.add(rim);for(let i=0;i<12;i++){const a=i/12*Math.PI*2;const m=box(.08,i%3?.14:.28,.05,0x20202a,.01);m.position.set(Math.sin(a)*R*.82,Math.cos(a)*R*.82,.12);m.rotation.z=-a;g.add(m)}
 const hh=new THREE.Group(),mm=new THREE.Group();const a=box(.12,R*.5,.05,0x20202a,.02);a.position.y=R*.25;hh.add(a);const b=box(.07,R*.78,.05,0x20202a,.02);b.position.y=R*.39;mm.add(b);hh.position.z=.15;mm.position.z=.18;g.add(hh,mm);
 return{g,set(hours){mm.rotation.z=-(hours%1)*Math.PI*2;hh.rotation.z=-(hours%12)/12*Math.PI*2}}}
// --- v33 (22/11): GIGANTE GASEOSO. Textura equirectangular con bandas de latitud que ondulan, remolinos y Gran Mancha Roja;
// tick(t) desliza las bandas a distinta velocidad (corrientes en chorro) sin re-dibujar el canvas. Reutilizable: Júpiter, Saturno (pal), planetas ficticios.
export function gasGiant(rad=10,{seed=4,spot=true,pal=['#e9dcc4','#c99a6b','#f3eadb','#b9774f','#e2c9a4','#a8683f','#efe2cb','#d3ae84'],seg=96}={}){
 const q=mk(seed),c=document.createElement('canvas');c.width=1024;c.height=512;const g=c.getContext('2d');
 let y=0;const bands=[];while(y<512){const h=10+q()*38;bands.push([y,h,pal[Math.floor(q()*pal.length)]]);y+=h}
 bands.forEach(([y0,h,col])=>{g.fillStyle=col;g.beginPath();g.moveTo(0,y0);for(let x=0;x<=1024;x+=16)g.lineTo(x,y0+Math.sin(x*.012+y0)*3+Math.sin(x*.041+y0*.3)*1.5);g.lineTo(1024,y0+h+2);for(let x=1024;x>=0;x-=16)g.lineTo(x,y0+h+2+Math.sin(x*.013+y0+h)*3);g.closePath();g.fill()});
 for(let i=0;i<260;i++){const x=q()*1024,yy=60+q()*392,r=2+q()*9;g.fillStyle=`rgba(${q()<.5?'255,250,240':'120,70,40'},${.12+q()*.22})`;g.beginPath();g.ellipse(x,yy,r*2.4,r,0,0,6.283);g.fill()}
 if(spot){const sx=700,sy=330;for(let k=0;k<5;k++){g.fillStyle=['#a8452c','#c0583a','#d4744f','#e39a74','#f0c4a0'][k];g.beginPath();g.ellipse(sx,sy,62-k*10,30-k*5,0,0,6.283);g.fill()}}
 const tex=new THREE.CanvasTexture(c);tex.colorSpace=THREE.SRGBColorSpace;tex.wrapS=THREE.RepeatWrapping;tex.anisotropy=8;
 const mesh=new THREE.Mesh(new THREE.SphereGeometry(rad,seg,seg/2),new THREE.MeshStandardMaterial({map:tex,roughness:.9}));
 const haze=new THREE.Mesh(new THREE.SphereGeometry(rad*1.03,48,24),new THREE.MeshBasicMaterial({color:0xffe2b8,transparent:true,opacity:.12,side:THREE.BackSide,depthWrite:false}));mesh.add(haze);
 return{mesh,tex,tick(t){tex.offset.x=(t*.012)%1;mesh.rotation.y=t*.05}}}
// --- v33 (22/11): taza de café con asa y vapor. mug({col}) → Group; m.userData.coffee (superficie) y steam(t, puffsObj, i0, x,y,z) para el humo.
export function mug(col=0xf2efe8){const g=new THREE.Group();const m=new THREE.MeshStandardMaterial({color:col,roughness:.35});
 const c=new THREE.Mesh(new THREE.CylinderGeometry(.5,.44,1.0,20,1,true),m);c.position.y=.5;g.add(c);const b=new THREE.Mesh(new THREE.CylinderGeometry(.44,.44,.08,20),m);b.position.y=.04;g.add(b);
 const inner=new THREE.Mesh(new THREE.CylinderGeometry(.47,.42,.96,20,1,true),new THREE.MeshStandardMaterial({color:col,roughness:.4,side:THREE.BackSide}));inner.position.y=.5;g.add(inner);
 const cof=new THREE.Mesh(new THREE.CylinderGeometry(.47,.47,.04,20),new THREE.MeshStandardMaterial({color:0x3b2214,roughness:.15}));cof.position.y=.86;g.add(cof);g.userData.coffee=cof;
 const h=new THREE.Mesh(new THREE.TorusGeometry(.26,.07,8,16,Math.PI),m);h.rotation.z=-Math.PI/2;h.position.set(.5,.5,0);g.add(h);return g}
export function steam(P,i0,n,x,y,z,t,s=1){for(let i=0;i<n;i++){const f=((t*.5+i/n)%1);P.set(i0+i,x+Math.sin(t*2+i*1.7)*.18*s*(1+f),y+f*1.6*s,z+Math.cos(t*1.6+i)*.12*s,(1-f)*.35*s)}}
// v34 (23/11): QUESO de bloques (cuña con agujeros; azul=true → queso azul con vetas), GATITO de bloques (personaje de sueño; casco y espada de cartón opcionales),
// COCODRILO de bloques (boca que se abre; zanahoria opcional) e ISLA DE SUEÑO movida aquí desde suenos.js para reutilizarla (dreamIsle).
export function cheese(s=1,{blue=false}={}){const g=new THREE.Group();const col=blue?0xeae6d6:0xffc83a;
 const sh=new THREE.Shape();sh.moveTo(0,0);sh.lineTo(3,0);sh.lineTo(0,1.7);sh.lineTo(0,0);
 const geo=new THREE.ExtrudeGeometry(sh,{depth:1.4,bevelEnabled:true,bevelSize:.06,bevelThickness:.06,bevelSegments:2});geo.translate(-1,0,-.7);
 const m=new THREE.Mesh(geo,new THREE.MeshStandardMaterial({color:col,roughness:.55}));m.rotation.x=-Math.PI/2;m.rotation.z=0;m.castShadow=true;
 const w=new THREE.Group();w.add(m);m.rotation.set(0,0,0);
 // agujeros (o vetas azules) en la cara frontal y lateral
 const hole=blue?0x3f6fa8:0xd89a1a;const Q=mk(blue?9:4);for(let i=0;i<(blue?9:6);i++){const x=-.8+Q()*2.2,y=.15+Q()*(1.5-(x+1)*.5);if(y<.1)continue;const h=new THREE.Mesh(blue?new THREE.BoxGeometry(.32+Q()*.3,.06,.04):new THREE.CircleGeometry(.12+Q()*.12,14),new THREE.MeshStandardMaterial({color:hole,roughness:.9}));if(blue)h.rotation.z=Q()*3;h.position.set(x,Math.min(y,1.55-(x+1)*.55),.77);w.add(h)}
 g.add(w);g.scale.setScalar(s);return g}
export function kitten(col=0xff9a3a,{helmet=true,sword=true}={}){const g=new THREE.Group();const b=box(1.4,.9,.8,col,.2);b.position.y=.75;g.add(b);
 const hd=new THREE.Group();hd.position.set(.85,1.35,0);g.add(hd);hd.add(box(.9,.8,.85,col,.2));[-.24,.24].forEach(z=>{const e=new THREE.Mesh(new THREE.ConeGeometry(.16,.34,4),new THREE.MeshStandardMaterial({color:col}));e.position.set(0,.5,z);hd.add(e);const ey=box(.06,.16,.12,0x15101c,.02);ey.position.set(.45,.08,z*.8);hd.add(ey)});
 const ns=box(.06,.1,.12,0xff6aa0,.02);ns.position.set(.46,-.08,0);hd.add(ns);
 if(helmet){const hm=box(.95,.28,.92,0xb8c0cc,.08,{metalness:.6,roughness:.3});hm.position.y=.42;hd.add(hm);const pl=box(.1,.34,.1,0xe5343f,.02);pl.position.set(0,.7,0);hd.add(pl)}
 const legs=[[-.45,-.25],[-.45,.25],[.45,-.25],[.45,.25]].map(([x,z])=>{const l=box(.24,.5,.24,col,.06);l.position.set(x,.25,z);g.add(l);return l});
 const tail=box(.16,.9,.16,col,.06);tail.position.set(-.75,1.3,0);tail.rotation.z=.5;g.add(tail);
 let sw=null;if(sword){sw=new THREE.Group();const bl=box(.1,1.3,.04,0xdfe6ee,.02,{metalness:.7,roughness:.25});bl.position.y=.75;const gd=box(.36,.08,.1,0xc8902a,.02);sw.add(bl,gd);sw.position.set(.6,.6,.45);g.add(sw)}
 g.tick=(t,ph=0)=>{const w=Math.sin(t*8+ph);legs.forEach((l,i)=>l.rotation.z=(i%2?1:-1)*w*.4);tail.rotation.z=.5+Math.sin(t*3+ph)*.3;if(sw)sw.rotation.z=-.4+Math.sin(t*4+ph)*.5;g.position.y=g.userData.y0+Math.abs(w)*.08};g.userData.y0=0;return g}
export function croc({col=0x3f8a3a,carrot=true}={}){const g=new THREE.Group();const b=box(3.4,.8,1.3,col,.25);b.position.y=.6;g.add(b);
 for(let i=0;i<5;i++){const sc=box(.3,.22,.5,0x2f6a2c,.05);sc.position.set(-1.2+i*.6,1.08,0);g.add(sc)}
 const tail=box(2.2,.5,.7,col,.2);tail.position.set(-2.6,.45,0);g.add(tail);
 const jawU=new THREE.Group();jawU.position.set(1.6,.85,0);g.add(jawU);const up=box(1.8,.32,.95,col,.12);up.position.x=.9;jawU.add(up);[-.25,.25].forEach(z=>{const e=box(.3,.3,.3,0xf2f2ee,.08);e.position.set(.1,.3,z);jawU.add(e);const p=box(.12,.16,.1,0x15101c,.02);p.position.set(.2,.32,z);jawU.add(p)});
 for(let i=0;i<5;i++){const tt=box(.1,.14,.08,0xffffff,.01);tt.position.set(.4+i*.32,-.2,.42);jawU.add(tt)}
 const jawL=box(1.8,.22,.9,0x5fae54,.1);jawL.position.set(2.5,.5,0);g.add(jawL);
 [[-1,-.55],[-1,.55],[1,-.55],[1,.55]].forEach(([x,z])=>{const l=box(.4,.4,.4,col,.08);l.position.set(x,.2,z);g.add(l)});
 let cr=null;if(carrot){cr=new THREE.Group();const c=new THREE.Mesh(new THREE.ConeGeometry(.18,1.1,8),new THREE.MeshStandardMaterial({color:0xff7a1e}));c.rotation.z=Math.PI/2;cr.add(c);const lf=box(.3,.3,.08,0x3cc46a,.04);lf.position.x=-.6;cr.add(lf);cr.position.set(3.1,.75,.0);g.add(cr)}
 g.tick=t=>{jawU.rotation.z=.15+.2*(.5+.5*Math.sin(t*4));tail.rotation.y=Math.sin(t*2)*.25};return g}
export function dreamIsle(isGray=false,seed=5){const gray=c=>{const C=new THREE.Color(c);const l=.2126*C.r+.7152*C.g+.0722*C.b;return new THREE.Color(l,l,l)};const g=new THREE.Group();const Q=mk(seed);const col=c=>isGray?gray(c).getHex():c;
 const top=box(7,1,5.2,col(0x58c25a),.2);g.add(top);const dirt=box(6,1.6,4.4,col(0x8a5a36),.2);dirt.position.y=-1.2;g.add(dirt);const tip=box(3.4,1.4,2.6,col(0x6e4528),.2);tip.position.y=-2.5;g.add(tip);
 [[-2.2,-1.2],[2.4,-1.4],[-2.6,1.4]].forEach(([x,z],i)=>{const tr=box(.5,1.6,.5,col(0x7a4e2e),.05);tr.position.set(x,1.3,z);g.add(tr);const lf=box(1.8,1.6,1.8,col([0x2fa84f,0x3cc46a,0x24944a][i]),.3);lf.position.set(x,2.7,z);g.add(lf)});
 const clouds=[];for(let i=0;i<5;i++){const c=box(1.6+Q(),.7,1.1,0xffffff,.3,{emissive:0xffffff,emissiveIntensity:.15});c.position.set((Q()-.5)*10,2+Q()*4,(Q()-.5)*3-1);g.add(c);clouds.push(c)}
 const L=new THREE.PointLight(0xfff0e0,40,22,1.2);L.position.set(0,7,5);g.add(L);g.userData.y=0;
 g.tick=t=>{g.position.y=g.userData.y+Math.sin(t*1.1+seed)*.25;g.rotation.y=Math.sin(t*.4+seed)*.25;clouds.forEach((c,i)=>{c.position.x=((c.position.x+5+.006*(i+1))%10)-5})};return g}
// v36 (25/11): LUNA DE CUBOS reutilizable (mares oscuros, cráteres y brillo propio). bump(dir, h) levanta un 'casquete' de cubos (montañas de la cara oculta).
export function voxMoon(n=5000,rad=6,{cube=.5,seed=1,emissive=.32,lit=true}={}){const grp=new THREE.Group();const q=mk(seed);const cr=[...Array(14)].map(()=>{const y=1-2*q(),a=q()*6.283,r=Math.sqrt(1-y*y);return[new THREE.Vector3(Math.cos(a)*r,y,Math.sin(a)*r),.12+q()*.22]});
 const mare=(v)=>Math.sin(v.x*2.3+seed)*Math.cos(v.y*2.1-1)+Math.sin(v.z*2.7+v.y*1.3)*.7>.55;
 const im=new THREE.InstancedMesh(new THREE.BoxGeometry(cube,cube,cube),new THREE.MeshStandardMaterial({roughness:1,emissive:0x8890a0,emissiveIntensity:lit?emissive:0}),n);im.frustumCulled=false;grp.add(im);
 const O=new THREE.Object3D(),C=new THREE.Color(),D=[];for(let i=0;i<n;i++){const y=1-2*(i+.5)/n,r=Math.sqrt(1-y*y),a=i*Math.PI*(3-Math.sqrt(5));const v=new THREE.Vector3(Math.cos(a)*r,y,Math.sin(a)*r);
  let g=mare(v)?.42:.72;for(const[c,s]of cr){const d=v.distanceTo(c);if(d<s)g*=d<s*.7?.72:1.18}g*=.94+((i*7)%5)*.03;C.setRGB(g,g,g*1.03);im.setColorAt(i,C);D.push(v);O.position.copy(v).multiplyScalar(rad);O.lookAt(0,0,0);O.updateMatrix();im.setMatrixAt(i,O.matrix)}
 return{group:grp,im,bump(dir,h,spread=.6){const O2=new THREE.Object3D();D.forEach((v,i)=>{const d=v.distanceTo(dir);const e=Math.max(0,1-d/spread);const hh=rad+h*e*e*(1+.25*Math.sin(i*1.7));O2.position.copy(v).multiplyScalar(hh);O2.lookAt(0,0,0);O2.updateMatrix();im.setMatrixAt(i,O2.matrix)});im.instanceMatrix.needsUpdate=true}}}

// --- v37 (26/11): COMIDA FAMILIAR y SUEÑO. turkey() pavo asado en bandeja (muslos con hueso, brillo), sofa(col), balance() báscula de platos
// con brazo (set(ang)), zzz(scene,n) Z que suben de una cabeza (at(i0,x,y,z,t)), feast() mesa larga con mantel, pan, patatas, tarta y copas.
export function turkey(s=1){const g=new THREE.Group();const plat=new THREE.Mesh(new THREE.CylinderGeometry(2.2,2.0,.18,32),new THREE.MeshStandardMaterial({color:0xf4f2ec,roughness:.3,metalness:.1}));plat.position.y=.09;g.add(plat);
 const skin={roughness:.38,emissive:0x3a1404,emissiveIntensity:.25};const b=box(2.6,1.45,1.9,0xb8642a,.55,skin);b.position.y=.95;g.add(b);const top=box(2.0,.5,1.5,0xc8743a,.25,skin);top.position.y=1.72;g.add(top);
 [-1,1].forEach(sd=>{const th=box(1.0,.85,.8,0xa8541e,.35,skin);th.position.set(1.05,.85,sd*.85);th.rotation.z=-.35;g.add(th);const bone=box(.55,.22,.22,0xf6efe0,.08);bone.position.set(1.75,1.15,sd*.85);bone.rotation.z=-.35;g.add(bone);const knob=box(.3,.34,.34,0xf6efe0,.12);knob.position.set(2.0,1.25,sd*.85);g.add(knob)});
 [[-.9,0x4a9a3a],[-.4,0xe8a02a],[.2,0x4a9a3a],[-1.6,0xd8342a]].forEach(([x,c],i)=>{const v=box(.32,.32,.32,c,.08);v.position.set(x,.32,(i%2?1:-1)*1.35);g.add(v)});g.scale.setScalar(s);return g}
export function sofa(col=0x6a4a8a){const g=new THREE.Group();const seat=box(6,1.1,2.6,col,.2);seat.position.y=.9;g.add(seat);const back=box(6,2.4,.8,col,.2);back.position.set(0,2.2,-1.0);g.add(back);[-3.1,3.1].forEach(x=>{const a=box(.7,1.9,2.6,col,.2);a.position.set(x,1.3,0);g.add(a)});const cus=box(1.4,1,.4,0xf2c230,.2);cus.position.set(-2,2.0,-.45);cus.rotation.z=.2;g.add(cus);[-2.7,2.7].forEach(x=>[-1,1].forEach(z=>{const l=box(.3,.35,.3,0x3a2416,.05);l.position.set(x,.18,z*1.1);g.add(l)}));return g}
export function balance(){const g=new THREE.Group();const base=box(3,.4,2,0x8a6a3a,.08,{metalness:.5,roughness:.35});base.position.y=.2;g.add(base);const post=box(.5,6,.5,0xd8b04a,.06,{metalness:.6,roughness:.3});post.position.y=3.2;g.add(post);
 const arm=new THREE.Group();arm.position.y=6.2;g.add(arm);const bar=box(11,.35,.35,0xd8b04a,.06,{metalness:.6,roughness:.3});arm.add(bar);const pans=[-5.2,5.2].map(x=>{const h=new THREE.Group();h.position.x=x;arm.add(h);const str=box(.08,2.6,.08,0x3a3a3a,.01);str.position.y=-1.3;h.add(str);const pan=new THREE.Mesh(new THREE.CylinderGeometry(1.9,1.5,.3,28),new THREE.MeshStandardMaterial({color:0xd8b04a,metalness:.6,roughness:.3}));pan.position.y=-2.7;h.add(pan);return h});
 const needle=box(.18,1.6,.18,0xff4a4a,.03);needle.position.y=.9;arm.add(needle);
 return{g,arm,pans,set(a){arm.rotation.z=a;pans.forEach(p=>p.rotation.z=-a)}}}
export function zzz(scene,n=3,{col='#9ad8ff',w=1.1}={}){const L=[];for(let i=0;i<n;i++){const z=label3d(['Z'],{w,h:w,bg:null,fg:col,px:300,sprite:true});scene.add(z);L.push(z)}
 return{L,at(x,y,z,t,on=1){L.forEach((o,i)=>{const f=((t*.45+i/n)%1);o.visible=on>0;o.position.set(x+f*1.6+Math.sin(t*2+i)*.2,y+f*2.6,z);const s=(.5+f*.9)*on;o.scale.set(w*s,w*s,1);o.material.opacity=(1-f)*on})}}}
export function feast(L=14){const g=new THREE.Group();const top=box(L,.3,4.6,0x7a4e2e,.05);top.position.y=3.0;g.add(top);const cloth=box(L+.2,.06,3.6,0xf4efe2,.02);cloth.position.y=3.18;g.add(cloth);const run=box(L+.2,.07,1.0,0xc0392b,.02);run.position.y=3.2;g.add(run);
 [[-L/2+.5,-1.9],[L/2-.5,-1.9],[-L/2+.5,1.9],[L/2-.5,1.9]].forEach(([x,z])=>{const l=box(.3,2.9,.3,0x5a3a22,.03);l.position.set(x,1.45,z);g.add(l)});
 const items=[];const add=(o,x,z)=>{o.position.set(x,3.24,z);g.add(o);items.push(o);return o};
 for(let i=0;i<5;i++){const b=box(.9,.5,.6,0xd8a050,.2);b.rotation.y=i*.7;add(b,-L/2+1.5+i*.4,-1.2+(i%2)*.3).position.y+=.25}
 const pot=new THREE.Group();const bowl=new THREE.Mesh(new THREE.CylinderGeometry(1.0,.7,.6,20),new THREE.MeshStandardMaterial({color:0x2a5aa8,roughness:.4}));bowl.position.y=.3;pot.add(bowl);for(let i=0;i<10;i++){const p=box(.4,.35,.4,0xf2d27a,.15);p.position.set(Math.cos(i)*.45,.65+(i%3)*.15,Math.sin(i*1.3)*.4);pot.add(p)}add(pot,-L/2+4.2,1.1);
 const cake=new THREE.Group();const c1=new THREE.Mesh(new THREE.CylinderGeometry(1.0,1.0,.8,24),new THREE.MeshStandardMaterial({color:0xe8a04a,roughness:.6}));c1.position.y=.4;cake.add(c1);const c2=new THREE.Mesh(new THREE.CylinderGeometry(1.02,1.02,.18,24),new THREE.MeshStandardMaterial({color:0xfff4e0,roughness:.4}));c2.position.y=.85;cake.add(c2);add(cake,L/2-2.2,-1.0);
 [-2.5,-1,2.2,3.6].forEach((x,i)=>{const gl=new THREE.Group();const st=box(.12,.7,.12,0xe8f4ff,.03,{transparent:true,opacity:.6});st.position.y=.35;gl.add(st);const cup=new THREE.Mesh(new THREE.CylinderGeometry(.32,.18,.6,14),new THREE.MeshStandardMaterial({color:0xe8f4ff,transparent:true,opacity:.45,roughness:.05}));cup.position.y=.95;gl.add(cup);const wn=new THREE.Mesh(new THREE.CylinderGeometry(.26,.18,.32,14),new THREE.MeshStandardMaterial({color:0x7a1028,roughness:.2}));wn.position.y=.85;gl.add(wn);add(gl,x,i%2?1.5:-1.5)});
 [-4,-1.8,.6,3,5].forEach((x,i)=>{const pl=new THREE.Mesh(new THREE.CylinderGeometry(.75,.65,.08,20),new THREE.MeshStandardMaterial({color:0xffffff,roughness:.3}));add(pl,x,i%2?-1.5:1.5)});
 return{g,items}}
// v38 (27/11): PERRO de bloques (personaje nº 4, propio). Mira a +x. pose(t,{guilt,wag,walk,sit}): guilt 0–1 = orejas gachas, cabeza baja,
// cola metida, cuerpo agachado y mirada hacia arriba (la 'cara de culpable'); wag = velocidad de la cola; walk = fase de paso o null; sit 0–1.
export function dog({col=0xc8894a,dark=0x6a4428,belly=0xf2dcb8,collar=0xe5343f}={}){const g=new THREE.Group();const B=new THREE.Group();g.add(B);
 const body=box(2.3,1.1,1.1,col,.25);body.position.y=1.35;B.add(body);const bl=box(1.6,.3,.9,belly,.1);bl.position.set(.1,.86,0);B.add(bl);
 const hd=new THREE.Group();hd.position.set(1.35,2.05,0);B.add(hd);hd.add(box(1.0,.95,.95,col,.22));
 const sn=box(.62,.5,.6,belly,.14);sn.position.set(.66,-.2,0);hd.add(sn);const ns=box(.22,.18,.26,0x1a1214,.06);ns.position.set(.98,-.05,0);hd.add(ns);
 const mo=box(.06,.06,.36,0x4a1a14,.02);mo.position.set(.96,-.36,0);hd.add(mo);
 const eyes=[-.24,.24].map(z=>{const e=new THREE.Group();const w=box(.06,.26,.24,0xfdf8f0,.02);const p=box(.05,.17,.14,0x15101c,.02);p.position.x=.03;e.add(w,p);e.position.set(.5,.14,z);e.userData.p=p;hd.add(e);return e});
 const brows=[-.24,.24].map(z=>{const b=box(.07,.07,.26,dark,.02);b.position.set(.52,.34,z);hd.add(b);return b});
 const ears=[-1,1].map(s=>{const e=new THREE.Group();e.position.set(-.05,.4,s*.5);const f=box(.42,.75,.16,dark,.06);f.position.y=-.3;e.add(f);hd.add(e);e.userData.s=s;return e});
 const cl=box(.2,.9,1.0,collar,.06);cl.position.set(1.0,1.75,0);B.add(cl);const tag=box(.05,.22,.2,0xffc23a,.03,{metalness:.7,roughness:.3});tag.position.set(1.12,1.38,0);B.add(tag);
 const legs=[[-.8,-.35],[-.8,.35],[.8,-.35],[.8,.35]].map(([x,z])=>{const l=new THREE.Group();l.position.set(x,.95,z);const m=box(.34,.95,.34,col,.08);m.position.y=-.45;const p=box(.4,.18,.42,belly,.06);p.position.set(.05,-.9,0);l.add(m,p);B.add(l);return l});
 const tail=new THREE.Group();tail.position.set(-1.15,1.7,0);const tm=box(.2,.9,.2,col,.08);tm.position.y=.42;const tt=box(.22,.22,.22,belly,.06);tt.position.y=.9;tail.add(tm,tt);B.add(tail);
 const o={g,B,head:hd,ears,eyes,tail,legs};
 o.pose=(t,{guilt=0,wag=0,walk=null,sit=0,look=0,m=0}={})=>{
  const w=walk===null?0:Math.sin(walk);legs.forEach((l,i)=>l.rotation.z=(i===0||i===3?1:-1)*w*.45);
  B.position.y=-guilt*.22-sit*.25+(walk===null?0:Math.abs(w)*.06);B.rotation.z=sit*.32;legs[0].rotation.z+=-sit*1.0;legs[1].rotation.z+=-sit*1.0;
  hd.rotation.z=-guilt*.38+Math.sin(t*1.6)*.03*(1-guilt)-sit*.32;hd.rotation.y=look+Math.sin(t*.8)*.08;hd.position.y=2.05-guilt*.18;
  ears.forEach(e=>{e.rotation.x=e.userData.s*(.12+Math.sin(t*3)*.05*(1-guilt));e.rotation.z=-guilt*.8});
  eyes.forEach(e=>{e.userData.p.position.y=guilt*.06;e.scale.y=(t%3.4)>3.28?.15:1});brows.forEach((b,i)=>{b.position.y=.34+guilt*.05;b.rotation.x=(i?1:-1)*guilt*.45});
  mo.scale.z=1-guilt*.4;mo.scale.y=1+m*3;
  tail.rotation.z=.55-guilt*2.0+Math.sin(t*(4+wag*16))*(.15+wag*.45)*(1-guilt*.8)};
 return o}
