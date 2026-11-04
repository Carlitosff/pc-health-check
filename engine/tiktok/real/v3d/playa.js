// Mito del corte de digestión (1203): playa de bloques.
import {THREE,J,mk,ss,V3,clamp,stage,sun,box,glow,pixTex,capataz,abuela,camera,segAt,mouthAt} from './bloques.js';
const TL=J.tl;const{r,scene,cam}=stage({bg:0x74c6ff,fog:[0x9fdcff,50,150],exposure:1.05});const R=mk(1203);
scene.add(new THREE.HemisphereLight(0xcfeaff,0xe8cf9c,1.5));sun(scene,{pos:[-12,30,20]});
// cielo
const skyTex=pixTex(4,64,(g,w,h)=>{const d=g.createLinearGradient(0,0,0,h);d.addColorStop(0,'#2f8ee0');d.addColorStop(.7,'#9fe0ff');d.addColorStop(1,'#fff1c9');g.fillStyle=d;g.fillRect(0,0,w,h)});skyTex.magFilter=THREE.LinearFilter;scene.background=skyTex;
{const P=[6,17,-48];const h=glow(0xfff0b0,26,.65);h.position.set(...P);h.material.fog=false;scene.add(h);const h2=glow(0xffffff,9,1);h2.position.set(...P);h2.material.fog=false;scene.add(h2);const h3=glow(0xffffff,6,1);h3.position.set(...P);h3.material.fog=false;scene.add(h3)}
const clouds=[];for(let i=0;i<9;i++){const g=new THREE.Group();const n=3+Math.floor(R()*3);for(let k=0;k<n;k++){const b=new THREE.Mesh(new THREE.BoxGeometry(4+R()*5,1.4+R()*1.6,3+R()*2),new THREE.MeshStandardMaterial({color:0xffffff,roughness:1,emissive:0xffffff,emissiveIntensity:.25}));b.position.set(k*2.6-n,R()*.8,R()*1.5);g.add(b)}g.position.set((R()-.5)*120,22+R()*14,-70-R()*40);g.userData.v=.4+R()*.5;scene.add(g);clouds.push(g)}
// arena con píxeles
const sandT=pixTex(128,128,(g,w,h)=>{const q=mk(5);g.fillStyle='#ecd29a';g.fillRect(0,0,w,h);for(let i=0;i<900;i++){g.fillStyle=['#e2c488','#f3dfae','#d8b878'][Math.floor(q()*3)];g.fillRect(Math.floor(q()*w/4)*4,Math.floor(q()*h/4)*4,4,4)}},[18,12]);
const sand=new THREE.Mesh(new THREE.PlaneGeometry(220,70),new THREE.MeshStandardMaterial({map:sandT,roughness:1}));sand.rotation.x=-Math.PI/2;sand.position.set(0,-.02,23);sand.receiveShadow=true;scene.add(sand);
// mar de cubos (empieza en z=-8)
const SX=64,SZ=56,CS=1.5;const seaM=new THREE.MeshStandardMaterial({roughness:.3,metalness:.05});const sea=new THREE.InstancedMesh(new THREE.BoxGeometry(CS,CS,CS),seaM,SX*SZ);sea.receiveShadow=true;scene.add(sea);const O=new THREE.Object3D(),col=new THREE.Color(),WARMC=new THREE.Color(0x18b6d8),DEEP=new THREE.Color(0x0a5fb8),ICE=new THREE.Color(0x0a2e78),FOAM=new THREE.Color(0xe8fbff);
const waveY=(x,z,t)=>Math.sin(x*.32+t*1.5)*.22+Math.sin(z*.42-t*1.9)*.26+Math.sin((x+z)*.18+t*.9)*.18;
function drawSea(t,cold){let i=0;for(let a=0;a<SX;a++)for(let b=0;b<SZ;b++){const x=(a-SX/2)*CS,z=-8.5-b*CS,y=waveY(x,z,t);O.position.set(x,y-CS/2-.15,z);O.updateMatrix();sea.setMatrixAt(i,O.matrix);col.copy(WARMC).lerp(DEEP,clamp(b/22));col.lerp(ICE,cold*.85);const fo=b<1?.75:clamp((y-.42)*2.5);col.lerp(FOAM,fo*(1-cold*.4));col.multiplyScalar(.92+((a*7+b*13)%5)*.03);sea.setColorAt(i,col);i++}sea.instanceMatrix.needsUpdate=true;sea.instanceColor.needsUpdate=true}
// sombrilla, toalla, pelota
const parasol=new THREE.Group();{const p=box(.16,6.2,.16,0xf4f4f4,.03);p.position.y=3.1;parasol.add(p);const st=[0xff3b4a,0xfff3e0];for(let i=0;i<4;i++){const s=box(5.4-i*1.25,.28,5.4-i*1.25,st[i%2],.05);s.position.y=6.1+i*.28;parasol.add(s)}parasol.position.set(4.8,0,1.6);parasol.rotation.z=-.08;scene.add(parasol)}
const towel=box(2.6,.09,4.4,0xff7a2e,.03);towel.position.set(.3,.04,3.2);scene.add(towel);for(let i=0;i<3;i++){const s=box(2.62,.1,.34,0xfff3e0,.02);s.position.set(.3,.05,1.8+i*1.4);scene.add(s)}
const ball=new THREE.Group();[0xff3b4a,0xffffff,0x2d7fe8].forEach((c,i)=>{const b=box(.9,.9,.3,c,.1);b.position.z=(i-1)*.3;ball.add(b)});ball.position.set(-5.2,.5,5.2);scene.add(ball);
// reloj despertador gigante con cuenta atrás
const cvs=document.createElement('canvas');cvs.width=512;cvs.height=512;const cg=cvs.getContext('2d');const cT=new THREE.CanvasTexture(cvs);cT.colorSpace=THREE.SRGBColorSpace;
function face(txt){cg.fillStyle='#fffdf5';cg.fillRect(0,0,512,512);cg.fillStyle='#111';cg.textAlign='center';cg.textBaseline='middle';cg.font='900 150px sans-serif';cg.fillText(txt,256,256);cg.fillStyle='#e11d2a';cg.font='900 54px sans-serif';cg.fillText('ESPERA',256,392);cT.needsUpdate=true}face('2:00');
const clock=new THREE.Group();{const body=new THREE.Mesh(new THREE.CylinderGeometry(2.1,2.1,1.1,8),new THREE.MeshStandardMaterial({color:0xe11d2a,roughness:.4}));body.rotation.x=Math.PI/2;body.castShadow=true;clock.add(body);const f=new THREE.Mesh(new THREE.BoxGeometry(2.9,2.9,.1),new THREE.MeshStandardMaterial({map:cT,roughness:.5}));f.position.z=.56;clock.add(f);[-1.25,1.25].forEach(x=>{const b=box(1.1,.8,.8,0xffc42e,.2);b.position.set(x,2.15,0);b.rotation.z=x*.35;clock.add(b)});[-1.2,1.2].forEach(x=>{const l=box(.3,.7,.3,0x333344,.05);l.position.set(x,-2.2,0);clock.add(l)})}clock.position.set(2.5,2.5,1);scene.add(clock);
const bits=[];{const cols=[0xe11d2a,0xfffdf5,0xffc42e,0x333344];for(let i=0;i<70;i++){const b=new THREE.Mesh(new THREE.BoxGeometry(.5,.5,.5),new THREE.MeshStandardMaterial({color:cols[i%4]}));b.castShadow=true;b.visible=false;b.userData={v:V3((R()-.5)*14,6+R()*12,(R()-.3)*10),w:V3(R()*9,R()*9,R()*9)};scene.add(b);bits.push(b)}}
// corazón de vóxeles
const heart=new THREE.Group();{const m=new THREE.MeshStandardMaterial({color:0xe8233c,roughness:.35,emissive:0x400008});const G=new THREE.BoxGeometry(.28,.28,.28);const P=[];for(let x=-11;x<=11;x++)for(let y=-11;y<=11;y++)for(let z=-5;z<=5;z++){const a=x/8.2,b=(y+1)/8.2,c=z/5.2;const v=Math.pow(a*a+2.25*c*c+b*b-1,3)-a*a*b*b*b-.1*c*c*b*b*b;if(v<0)P.push([x,y,z])}const I=new THREE.InstancedMesh(G,m,P.length);const o=new THREE.Object3D();P.forEach((q,i)=>{o.position.set(q[0]*.3,q[1]*.3,q[2]*.3);o.updateMatrix();I.setMatrixAt(i,o.matrix)});heart.add(I);heart.visible=false;scene.add(heart)}
// salpicaduras
const drops=[];for(let i=0;i<46;i++){const b=new THREE.Mesh(new THREE.BoxGeometry(.32,.32,.32),new THREE.MeshStandardMaterial({color:0xdff6ff,roughness:.2}));b.visible=false;b.userData={v:V3((R()-.5)*9,7+R()*9,(R()-.5)*9)};scene.add(b);drops.push(b)}
// personajes
const hero=capataz();scene.add(hero.g);const ab=abuela();scene.add(ab.g);ab.g.position.set(-2.6,0,4.6);ab.g.rotation.y=.35;
const HP=V3(.15,.12,3.2);
const t1=TL.s1[0],t2=TL.s2[0],t3=TL.s3[0],t4=TL.s4[0],tC=TL.cta[0],boomT=TL.s1[1]-1.9,jumpA=t2+.25,jumpB=t2+1.55;
const order=['h','s1','s2','s3','s4','cta'];
const shots={h:{p:V3(.3,5.2,31),q:V3(.3,6.6,2)},s1:{p:V3(1.2,5,24),q:V3(1.4,6.4,1)},s2:{p:V3(6,5,12),q:V3(0,5,-14)},s3:{p:V3(.5,4.4,8.5),q:V3(0,6,-13)},s4:{p:V3(7,3.8,6),q:V3(0,5.2,-8)},cta:{p:V3(-1,6,28),q:V3(-.8,1.6,-4)}};
const go=camera(cam,order,shots,TL,.7);
window.renderAt=t=>{const s=segAt(TL,t);const m=mouthAt(t);
 const coldK=s==='s2'?ss(t2+1.4,t2+2.2,t):s==='s3'?1:s==='s4'?1-ss(t4,t4+1.5,t):0;scene.fog.color.set(0x9fdcff).lerp(new THREE.Color(0x2a64b8),coldK*.6);
 drawSea(t,coldK);clouds.forEach(g=>{g.position.x=((g.position.x+60+g.userData.v*(1/30))%120)-60});
 // reloj
 const boom=t>=boomT;clock.visible=!boom;if(!boom){clock.rotation.z=Math.sin(t*14)*.04*(1+ss(t1,boomT,t)*4);clock.position.y=2.5+Math.abs(Math.sin(t*7))*.1;const sc=t<boomT?120-t*2.3:0;const left=Math.max(0,sc);const mm=Math.floor(left/60),ss_=Math.floor(left%60);face(`${mm}:${String(ss_).padStart(2,'0')}`)}
 bits.forEach(b=>{const a=t-boomT;b.visible=a>0&&a<4;if(b.visible){const u=b.userData;b.position.set(2.5+u.v.x*a,Math.max(.3,2.5+u.v.y*a-11*a*a),1+u.v.z*a);b.rotation.set(u.w.x*a,u.w.y*a,u.w.z*a)}});
 parasol.visible=s==='h'||s==='s1'||s==='cta';towel.visible=parasol.visible;
 // capataz
 let wave=0,walkP=null,look=0,armsUp=0,hp=HP.clone(),ry=0;
 if(s==='h'){look=-.25;}
 else if(s==='s1'){look=.5;armsUp=ss(boomT,boomT+.3,t)}
 else if(s==='s2'){const k=clamp((t-jumpA)/(jumpB-jumpA));const runK=clamp(k/.55),airK=clamp((k-.55)/.45);ry=Math.PI;hp.z=HP.z+(-9-HP.z)*ss(0,1,runK)+(-14+9)*airK;hp.y=.12+Math.sin(airK*Math.PI)*3.2-(airK>=1?3.1:airK*3.1);if(k<.55)walkP=t*14;if(airK>=1){ry=0;hp.y=-2.2+Math.sin(t*2.3)*.15}}
 else if(s==='s3'){hp.set(0,-2.2+Math.sin(t*2.3)*.15,-14)}
 else if(s==='s4'){const k=clamp((t-t4-.3)/(tC-t4-.6));hp.z=-5-8*k;hp.x=-.2;hp.y=.12-Math.max(0,(-hp.z-8)*.42);ry=Math.PI*.62;walkP=t*2.6;armsUp=.25*Math.max(0,Math.sin(t*1.2))}
 else{hp.set(2,-1.5+Math.sin(t*2.3)*.1,-11);wave=1;ry=0}
 hero.g.position.copy(hp);hero.g.rotation.y=ry;hero.pose(t,s==='h'||s==='cta'?m:m*.3,{wave,walk:walkP,look,armsUp});
 // abuela
 ab.g.visible=s==='h'||s==='s1'||s==='cta';ab.g.position.set(s==='cta'?-3.4:-2.6,0,s==='cta'?-3:4.6);ab.g.rotation.y=s==='cta'?.2:.35;ab.pose(t,s==='h'?m*.5:0,{point:s==='h'?1:0,armsUp:s==='cta'?.9:0,look:0});
 // salpicadura al caer
 const a=t-jumpB;drops.forEach((d,i)=>{d.visible=a>0&&a<1.4&&s==='s2';if(d.visible){const u=d.userData;d.position.set(u.v.x*a*.6,-.1+u.v.y*a-9.8*a*a,-14+u.v.z*a*.6)}});
 const b4=(t-t4)%1.5;
 // corazón: se frena (intervalo de 0,55 s a 1,5 s)
 heart.visible=s==='s3';if(heart.visible){const u=clamp((t-t3)/(t4-t3));const per=.55+.95*u;const ph=(((t-t3)/per)%1);const beat=1+.16*Math.exp(-ph*8)*(1-u*.45);heart.scale.setScalar(beat*(.55+.1*(1-u)));heart.position.set(Math.sin(t*.7)*.2,3.9,-5);heart.rotation.y=Math.sin(t*.6)*.4}
 go(t,(p,q)=>{if(s==='s4'){const e=ss(t4,t4+.7,t);p.z+=(hp.z+17-p.z)*e;p.x+=(9-p.x)*e;p.y+=(4.4-p.y)*e;q.x+=(hp.x-q.x)*e;q.z+=(hp.z-q.z)*e;q.y+=(5-q.y)*e}if(s==='s2'&&t>jumpA){const e=ss(jumpA,jumpA+.7,t);q.z+=(hp.z+14)*e;const f=ss(jumpB,jumpB+1.2,t);p.z-=f*13;p.x-=f*3;q.y-=f*3}});
 r.render(scene,cam);return true};
window.ready=true;
