// Mito de los 8 vasos de agua (1703). Reutilizable: vaso de bloques que se llena (glass), cocina de día, biblioteca con lupa que barre, comida que suelta agua a una jarra.
import {THREE,J,mk,ss,V3,clamp,stage,sun,box,glow,pixTex,capataz,abuela,camera,segAt,mouthAt,puffs,label3d} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0xbfe3ff,fog:[0xbfe3ff,50,160],exposure:1.12});const R=mk(1703);
const hemi=new THREE.HemisphereLight(0xffffff,0x8a7a6a,1.25);scene.add(hemi);const S=sun(scene,{pos:[-10,24,16],span:22,power:2.4});
// --- vaso que se llena: {g,set(f)}
export function glass(h=1.6,rad=.5,col=0x3fb4ff){const g=new THREE.Group();const gl=new THREE.Mesh(new THREE.CylinderGeometry(rad,rad*.86,h,20,1,true),new THREE.MeshStandardMaterial({color:0xe8f6ff,transparent:true,opacity:.32,roughness:.05,metalness:.1,side:THREE.DoubleSide,depthWrite:false}));gl.position.y=h/2;g.add(gl);
 const bot=new THREE.Mesh(new THREE.CylinderGeometry(rad*.86,rad*.86,.08,20),new THREE.MeshStandardMaterial({color:0xdff2ff,transparent:true,opacity:.5}));bot.position.y=.04;g.add(bot);
 const w=new THREE.Mesh(new THREE.CylinderGeometry(rad*.92,rad*.82,1,20),new THREE.MeshStandardMaterial({color:col,transparent:true,opacity:.82,roughness:.1,emissive:col,emissiveIntensity:.12}));w.position.y=.06;g.add(w);
 const top=new THREE.Mesh(new THREE.CircleGeometry(rad*.9,20),new THREE.MeshBasicMaterial({color:0xbfeaff,transparent:true,opacity:.9}));top.rotation.x=-Math.PI/2;g.add(top);
 const set=f=>{f=clamp(f);w.visible=top.visible=f>.01;w.scale.y=Math.max(.01,f*(h-.14));w.position.y=.06+w.scale.y/2;top.position.y=.07+w.scale.y};set(0);return{g,set}}
// --- COCINA DE DÍA
const K0=new THREE.Group();scene.add(K0);
const fl=new THREE.Mesh(new THREE.PlaneGeometry(80,80),new THREE.MeshStandardMaterial({map:pixTex(64,64,(g)=>{for(let y=0;y<8;y++)for(let x=0;x<8;x++){g.fillStyle=(x+y)%2?'#f2ecdf':'#3f7fb0';g.fillRect(x*8,y*8,8,8)}},[14,14]),roughness:.85}));fl.rotation.x=-Math.PI/2;fl.receiveShadow=true;K0.add(fl);
const wall=box(50,18,1,0xf6e2b6,.05);wall.position.set(0,9,-8);K0.add(wall);
const win=box(9,6,.2,0x9fd8ff,.04,{emissive:0x6fb8ff,emissiveIntensity:.5});win.position.set(-7,10,-7.4);K0.add(win);
const table=box(11,.4,4.4,0x9a6a3c,.06);table.position.set(0,2.6,0);K0.add(table);[[-5,-1.8],[5,-1.8],[-5,1.8],[5,1.8]].forEach(([x,z])=>{const l=box(.4,2.6,.4,0x6b4426,.04);l.position.set(x,1.3,z);K0.add(l)});
const GL=[];for(let i=0;i<8;i++){const q=glass(1.5,.42);q.g.position.set(-1.8+(i%4)*1.2,2.8,i<4?-.4:1.0);K0.add(q.g);GL.push(q)}
const eight=label3d(['*8 VASOS','AL DÍA'],{w:4.4,h:2.2,px:150,accent:'#3fb4ff'});eight.position.set(0,6.4,-7.3);K0.add(eight);
const ab=abuela();ab.g.position.set(-2.9,0,3.0);ab.g.rotation.y=.5;scene.add(ab.g);
const jug=new THREE.Group();{const b=glass(1.8,.6);jug.add(b.g);b.set(.7);const h=box(.15,.9,.5,0xe8f6ff,.05,{transparent:true,opacity:.6});h.position.set(.7,1,0);jug.add(h)}ab.armR.add(jug);jug.position.set(0,-1.9,.5);jug.rotation.x=-1.2;
const cap=capataz();cap.g.position.set(2.9,0,3.0);cap.g.rotation.y=-.5;scene.add(cap.g);
// --- BIBLIOTECA (s1): estanterías, lupa que barre, panel
const LB=new THREE.Group();LB.position.set(0,0,-200);scene.add(LB);
const lfl=new THREE.Mesh(new THREE.PlaneGeometry(80,80),new THREE.MeshStandardMaterial({color:0x6a4a34,roughness:.9}));lfl.rotation.x=-Math.PI/2;LB.add(lfl);
const BOOKC=[0xb23a3a,0x2e5fa8,0x3e8a4a,0xd8a03a,0x6a3e8a,0x2a2a33,0xe0d4b8];
for(let s=0;s<3;s++){const sh=new THREE.Group();sh.position.set(-7+s*7,0,-5-Math.abs(s-1)*1.2);sh.rotation.y=(1-s)*.25;LB.add(sh);const fr=box(6,11,1.4,0x5a3a22,.04);fr.position.y=5.5;fr.position.z=-.3;sh.add(fr);
 for(let row=0;row<5;row++){const pl=box(5.8,.2,1.2,0x7a5232,.02);pl.position.set(0,.8+row*2.1,.2);sh.add(pl);let x=-2.7;while(x<2.6){const w=.22+R()*.25,h=1.2+R()*.6;const b=box(w,h,.9,BOOKC[Math.floor(R()*7)],.03);b.position.set(x+w/2,.9+row*2.1+h/2,.25);sh.add(b);x+=w+.03}}}
const mag=new THREE.Group();{const ring=new THREE.Mesh(new THREE.TorusGeometry(1.1,.16,10,32),new THREE.MeshStandardMaterial({color:0x2a2a33,metalness:.6,roughness:.3}));mag.add(ring);const lens=new THREE.Mesh(new THREE.CircleGeometry(1.05,32),new THREE.MeshStandardMaterial({color:0xcff0ff,transparent:true,opacity:.35,roughness:0}));mag.add(lens);const hd=box(.3,1.8,.3,0x7a4a22,.08);hd.position.set(0,-1.9,0);mag.add(hd)}LB.add(mag);const magG=glow(0xfff2c0,3.2,.5);LB.add(magG);
const year=label3d(['*2002','HEINZ VALTIN · DARTMOUTH'],{w:6.4,h:2.2,px:110});year.position.set(.6,7.6,-3);LB.add(year);
const zero=label3d(['NINGÚN ESTUDIO','*LO DEMOSTRABA'],{w:5.6,h:2,px:110,accent:'#ff4d6d'});zero.position.set(.8,4.4,2.4);LB.add(zero);
const valt=capataz();valt.g.position.set(-2.8,0,3.6);valt.g.rotation.y=.35;LB.add(valt.g);
// --- PANEL DE LA FRASE (s2-s3)
const PN=new THREE.Group();PN.position.set(0,0,-400);scene.add(PN);
const pfl=new THREE.Mesh(new THREE.PlaneGeometry(80,80),new THREE.MeshStandardMaterial({color:0x2a3550,roughness:.9}));pfl.rotation.x=-Math.PI/2;PN.add(pfl);
const doc=box(9,10,.3,0xf4ecd8,.05);doc.position.set(0,5,-3);PN.add(doc);
const l1=label3d(['RECOMENDACIÓN','*1 ML POR CALORÍA'],{w:8,h:2.6,px:110,bg:null,fg:'#2a2440',accent:'#2e5fa8'});l1.position.set(0,8.2,-2.8);PN.add(l1);
for(let i=0;i<4;i++){const ln=box(7-(i==3)*2.4,.18,.05,0x9a96a8,.02);ln.position.set(-(i==3)*1.2,6.6-i*.55,-2.8);PN.add(ln)}
const l2=label3d(['…LA MAYOR PARTE','*YA VA EN LA COMIDA'],{w:8,h:2.6,px:110,bg:'#fff6c8',fg:'#2a2440',accent:'#e0a020'});l2.position.set(0,3.3,-2.6);PN.add(l2);
const cover=box(8.6,3,.2,0x2a2440,.04);cover.position.set(0,3.3,-2.5);PN.add(cover);
const pcap=capataz();pcap.g.position.set(3.2,0,2.2);pcap.g.rotation.y=-.4;PN.add(pcap.g);
// --- COMIDA QUE SUELTA AGUA (s3)
const FD=new THREE.Group();FD.position.set(0,0,-600);scene.add(FD);
const ft=box(12,.4,5,0x9a6a3c,.06);ft.position.set(0,2.6,0);FD.add(ft);const ffl=new THREE.Mesh(new THREE.PlaneGeometry(80,80),new THREE.MeshStandardMaterial({color:0xe9dcc4,roughness:.9}));ffl.rotation.x=-Math.PI/2;FD.add(ffl);
const fwall=box(50,18,1,0xbfe0d0,.05);fwall.position.set(0,9,-8);FD.add(fwall);
const melon=new THREE.Group();{const rind=box(2.8,.5,1.4,0x2f8a3a,.1);rind.position.y=.25;melon.add(rind);const flesh=box(2.6,1.3,1.2,0xff4d5a,.1);flesh.position.y=1.1;melon.add(flesh);for(let i=0;i<6;i++){const sd=box(.12,.2,.05,0x1a1a1a,.02);sd.position.set(-1+i*.4,1.2+(i%2)*.3,.62);melon.add(sd)}}melon.position.set(-3.4,2.8,.6);FD.add(melon);
const soup=new THREE.Group();{const b=box(2.2,1,2.2,0xf2f2f2,.35);b.position.y=.5;soup.add(b);const s=box(1.9,.1,1.9,0xe0a040,.05,{emissive:0x804010,emissiveIntensity:.2});s.position.y=1.02;soup.add(s)}soup.position.set(-.9,2.8,.6);FD.add(soup);
const cup=new THREE.Group();{const b=box(1.1,1.2,1.1,0xffffff,.25);b.position.y=.6;cup.add(b);const c=box(.9,.1,.9,0x5a3018,.05);c.position.y=1.2;cup.add(c);const h=box(.15,.6,.5,0xffffff,.05);h.position.set(.66,.65,0);cup.add(h)}cup.position.set(1.2,2.8,.6);FD.add(cup);
const big=glass(3.6,1.1);big.g.position.set(3.4,2.8,.2);FD.add(big.g);
const drops=puffs(FD,120,.22,0x3fb4ff);
const src=[melon.position,soup.position,cup.position].map(p=>V3(p.x,p.y+1.6,p.z));
const lblF=label3d(['*CAFÉ Y TÉ','TAMBIÉN CUENTAN'],{w:5,h:2,px:120,accent:'#3fb4ff'});lblF.position.set(-1.2,1.3,3.4);FD.add(lblF);
const fcap=capataz();fcap.g.position.set(-4.6,0,3.4);fcap.g.rotation.y=.5;FD.add(fcap.g);
// --- SED (s4): capataz bebe cuando sale la gota de sed
const SD=new THREE.Group();SD.position.set(0,0,-800);scene.add(SD);
const sfl=new THREE.Mesh(new THREE.PlaneGeometry(80,80),new THREE.MeshStandardMaterial({map:pixTex(64,64,(g)=>{const q=mk(3);g.fillStyle='#7cc25a';g.fillRect(0,0,64,64);for(let i=0;i<300;i++){g.fillStyle=['#6fb24e','#8fd068','#5a9e40'][Math.floor(q()*3)];g.fillRect(Math.floor(q()*16)*4,Math.floor(q()*16)*4,4,4)}},[20,20]),roughness:1}));sfl.rotation.x=-Math.PI/2;sfl.receiveShadow=true;SD.add(sfl);
const scap=capataz();scap.g.position.set(0,0,0);SD.add(scap.g);const sg=glass(1.2,.36);scap.armR.add(sg.g);sg.g.position.set(0,-1.9,.4);sg.g.rotation.x=0;
const thirst=label3d(['*SED'],{w:2.6,h:1.4,px:150,accent:'#3fb4ff',sprite:true});SD.add(thirst);
const hot=label3d(['CALOR O DEPORTE:','*BEBE MÁS'],{w:5.6,h:2,px:110,accent:'#ff7a1a'});hot.position.set(0,.95,2.6);SD.add(hot);
const sunB=glow(0xfff2a0,9,.9);sunB.position.set(-8,13,-12);SD.add(sunB);
for(let i=0;i<7;i++){const tr=new THREE.Group();const tk=box(.6,3,.6,0x7a5232,.05);tk.position.y=1.5;tr.add(tk);const cr=box(2.6,2.4,2.6,0x3e8a3a,.3);cr.position.y=3.8;tr.add(cr);tr.position.set(-12+i*4+(i%2),0,-9-(i%3)*2);SD.add(tr)}
// --- cámara
const t1=TL.s1[0],t2=TL.s2[0],t3=TL.s3[0],t4=TL.s4[0],tC=TL.cta[0];
const shots={h:{p:V3(0,6.4,21),q:V3(0,4.6,0)},s1:{p:V3(1.5,5.6,25),q:V3(0,6.4,-2)},s2:{p:V3(-.5,5.4,21),q:V3(0,6.4,-3)},s3:{p:V3(0,6.2,23),q:V3(0,5.2,0)},s4:{p:V3(2.6,3.4,14),q:V3(0,3.6,0)},cta:{p:V3(0,6.4,21),q:V3(0,4.6,0)}};
shots.s1.p.add(LB.position);shots.s1.q.add(LB.position);shots.s2.p.add(PN.position);shots.s2.q.add(PN.position);shots.s3.p.add(FD.position);shots.s3.q.add(FD.position);shots.s4.p.add(SD.position);shots.s4.q.add(SD.position);
// s3: primero el panel (frase que nadie copió) y luego la comida
const sPN={p:V3(-.5,6.4,19).add(PN.position),q:V3(0,7.6,-3).add(PN.position)};
cam.far=1500;cam.updateProjectionMatrix();
const go=camera(cam,['h','s1','s2','s3','s4','cta'],shots,TL,.01);
window.renderAt=t=>{const s=segAt(TL,t),m=mouthAt(t);const lt=t-TL[s][0],d=TL[s][1]-TL[s][0];
 const half=s==='s3'&&lt<d*.45;
 K0.visible=ab.g.visible=cap.g.visible=s==='h'||s==='cta';LB.visible=s==='s1';PN.visible=s==='s2'||half;FD.visible=s==='s3'&&!half;SD.visible=s==='s4';
 // vasos que se llenan en cadena (gancho) y quedan llenos en el CTA
 GL.forEach((q,i)=>q.set(s==='cta'?1:ss(.25+i*.32,.55+i*.32,t)));
 ab.pose(t,m*0,{look:.2,point:.5});ab.armR.rotation.x=-1.1+Math.sin(t*2)*.08;cap.pose(t,s==='h'?m:m,{look:-.2,wave:s==='cta'?1:0,armsUp:s==='h'?.15:0});
 eight.visible=s==='cta';eight.scale.setScalar(1+.04*Math.sin(t*3));
 if(LB.visible){const k=lt/d;mag.position.set(-6+12*ss(.05,.7,k)+Math.sin(t*4)*.4,7+Math.sin(t*2.6)*2.2,.6);magG.position.copy(mag.position);year.visible=lt>.3;zero.visible=lt>d*.62;zero.scale.setScalar(1+.6*Math.exp(-Math.max(0,lt-d*.62)*5));valt.pose(t,m,{look:Math.sin(t*1.4)*.5,point:.6})}
 if(PN.visible){const tt=s==='s2'?lt:d+lt;const opn=s==='s3'?ss(.2,1.1,lt):0;cover.position.x=opn*9.4;cover.rotation.z=-opn*.4;l2.scale.setScalar(1+.08*opn*Math.sin(t*5));pcap.pose(t,m,{look:-.4,point:s==='s3'?ss(.6,1.2,lt):.3});}
 if(FD.visible){const k=clamp((lt-d*.45)/(d*.55));big.set(.08+.88*ss(.05,.9,k));for(let i=0;i<120;i++){const a=((t*.9+i/120)%1),sI=i%3,p0=src[sI],p1=V3(3.4,6.6,.2);const x=p0.x+(p1.x-p0.x)*a,z=p0.z+(p1.z-p0.z)*a,y=p0.y+(p1.y-p0.y)*a+Math.sin(a*Math.PI)*3;drops.set(i,x,y,z,k>0?(.9+.3*Math.sin(i))*(1-Math.abs(a-.5)*.6):0,0)}drops.m.instanceMatrix.needsUpdate=true;lblF.visible=lt>d*.62;fcap.pose(t,m,{look:.3,point:.6})}
 if(SD.visible){const k=lt/d;thirst.position.set(2.1,4.1+.2*Math.sin(t*4),.6);thirst.visible=k<.45;thirst.scale.set(2.6*(1+.15*Math.sin(t*8)),1.4*(1+.15*Math.sin(t*8)),1);const dr=ss(.42,.6,k)*(1-ss(.85,.98,k));sg.set(1-ss(.45,.85,k)*.9);scap.pose(t,m,{look:.1});scap.armR.rotation.x=-2.2*dr;scap.armR.rotation.z=.2*dr;scap.head.rotation.x=-.35*dr;hot.visible=k>.62}
 go(t,(p,q)=>{if(s==='h'){p.z-=t*.35;p.y-=t*.05}if(half){p.copy(sPN.p);q.copy(sPN.q);p.z-=lt*.4}if(s==='s1')p.z-=lt*.5;if(s==='s4')p.x-=lt*.3});
 r.render(scene,cam);return true};
window.ready=true;
