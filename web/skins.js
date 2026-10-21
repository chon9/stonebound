// Deterministic painted materials, shared by the shop and the playable board.
const seed=i=>(Math.sin(i*127.13+78.23)*43758.5453)%1;
export function shade(hex,f){const v=hex.replace('#','').match(/.{2}/g).map(v=>parseInt(v,16));return `rgb(${v.map(v=>Math.round(f>0?v+(255-v)*f:v*(1+f))).join(',')})`;}
export function paintSurface(ctx,b,size){
  ctx.save();ctx.fillStyle=b.color;ctx.fillRect(0,0,size,size);ctx.scale(size/1000,size/1000);
  const p=b.pattern,a=b.accent||'#d8c7a4';ctx.lineWidth=2;ctx.strokeStyle=a;ctx.globalAlpha=.24;
  if(p==='wood'||p==='paper'||p==='metal'){
    for(let i=0;i<(p==='paper'?500:180);i++){const x=i*6+Math.sin(i*3)*4;ctx.strokeStyle=i%3?'#493e29':'#fff9dc';ctx.globalAlpha=p==='metal'?.11:.07;ctx.beginPath();if(p==='paper'){const y=Math.abs(seed(i))*1000;ctx.moveTo(x%1000,y);ctx.lineTo(x%1000+18,y+2);}else{ctx.moveTo(x,0);ctx.bezierCurveTo(x+20,300,x-10,600,x+15,1000);}ctx.stroke();}
  }else if(p==='ripple'||p==='rain'||p==='rail'){
    for(let i=0;i<24;i++){ctx.beginPath();if(p==='ripple'){ctx.ellipse(490,470,i*38+12,i*22+10,-.2,0,Math.PI*2);}else if(p==='rain'){ctx.moveTo(i*52-100,0);ctx.lineTo(i*52-340,1000);}else{ctx.moveTo(i*50,0);ctx.lineTo(i*50,1000);ctx.moveTo(0,i*50);ctx.lineTo(1000,i*50);}ctx.stroke();}
  }else if(p==='porcelain'||p==='lantern'||p==='garden'||p==='leaves'){
    for(let i=0;i<26;i++){const x=(i*173+45)%1000,y=(i*267+68)%1000;ctx.save();ctx.translate(x,y);ctx.rotate(i*.9);ctx.beginPath();if(p==='lantern'){ctx.roundRect(-13,-25,26,50,12);}else{ctx.ellipse(0,0,13,p==='garden'?15:32,.7,0,Math.PI*2);ctx.moveTo(0,-26);ctx.lineTo(0,26);}ctx.stroke();ctx.restore();}
    if(p==='porcelain'){ctx.lineWidth=5;ctx.strokeRect(28,28,944,944);ctx.lineWidth=2;ctx.strokeRect(39,39,922,922);}
  }else if(p==='circuit'||p==='stars'){
    for(let i=0;i<42;i++){const x=(i*179+48)%1000,y=(i*293+72)%1000;ctx.beginPath();ctx.arc(x,y,i%3+1,0,Math.PI*2);ctx.stroke();if(p==='circuit'){ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x+24,y);ctx.lineTo(x+24,y+32);ctx.stroke();}else if(i%4===0){ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo((x+173)%1000,(y+67)%1000);ctx.stroke();}}
  }else if(p==='ink'||p==='marble'||p==='kintsugi'){
    ctx.lineWidth=p==='kintsugi'?6:3;
    for(let i=0;i<8;i++){ctx.beginPath();ctx.moveTo(i*168-150,1000);for(let j=0;j<9;j++)ctx.lineTo(i*168-150+Math.sin(j*2+i)*65,1000-j*130);ctx.stroke();}
  }
  ctx.globalAlpha=1;const g=ctx.createLinearGradient(0,0,1000,1000);g.addColorStop(0,'#ffffff1c');g.addColorStop(.5,'#ffffff00');g.addColorStop(1,'#161a111b');ctx.fillStyle=g;ctx.fillRect(0,0,1000,1000);
  if(p==='kintsugi'){for(let i=0;i<8;i++){ctx.beginPath();ctx.arc(155+i*98,15,8,0,Math.PI*2);ctx.fillStyle=['#5c998f','#8da478','#bf8595','#d7b566','#586b91','#bf896a','#abc1b9','#719286'][i];ctx.fill();ctx.strokeStyle='#776448';ctx.lineWidth=2;ctx.stroke();}}
  ctx.restore();
}
export function paintStone(ctx,px,py,r,color,s,opacity=1){
  const hex=color==='B'?s.color:(s.white_color||'#f0efe3');
  ctx.save();ctx.globalAlpha=opacity;ctx.shadowColor='#171c2b60';ctx.shadowBlur=r*.2;ctx.shadowOffsetY=r*.12;ctx.shadowOffsetX=r*.06;
  const g=ctx.createRadialGradient(px-r*.34,py-r*.38,r*.05,px,py,r*1.05);g.addColorStop(0,shade(hex,s.pattern==='matte'?.15:.38));g.addColorStop(.5,hex);g.addColorStop(1,shade(hex,-.35));ctx.fillStyle=g;ctx.beginPath();ctx.arc(px,py,r,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;ctx.shadowOffsetX=ctx.shadowOffsetY=0;ctx.clip();
  ctx.translate(px,py);ctx.scale(r,r);ctx.strokeStyle=color==='B'?'#f9eacb':'#615e49';ctx.lineWidth=.025;ctx.globalAlpha=opacity*.3;
  if(['vein','wave','crack','metal'].includes(s.pattern)){
    for(let i=0;i<4;i++){ctx.beginPath();ctx.moveTo(-1,-.7+i*.4);if(s.pattern==='crack'){ctx.strokeStyle='#e4b559';ctx.lineWidth=.045;ctx.lineTo(-.2,-.5+i*.4);ctx.lineTo(.1,-.8+i*.4);ctx.lineTo(1,-.4+i*.4);}else ctx.bezierCurveTo(-.5,-.9+i*.4,.1,.2+i*.4,1,-.7+i*.4);ctx.stroke();}
  }else if(['speckle','galaxy','seal'].includes(s.pattern)){
    for(let i=0;i<21;i++){ctx.beginPath();ctx.arc(Math.abs(seed(i))*1.8-.9,Math.abs(seed(i+32))*1.8-.9,.02+i%3*.01,0,Math.PI*2);ctx.stroke();}
    if(s.pattern==='seal'){ctx.lineWidth=.05;ctx.strokeRect(-.35,-.35,.7,.7);ctx.beginPath();ctx.moveTo(-.2,0);ctx.lineTo(.2,0);ctx.moveTo(0,-.2);ctx.lineTo(0,.2);ctx.stroke();}
  }else if(s.pattern==='glow'){
    const glow=ctx.createRadialGradient(-.4,-.4,0,0,0,1);glow.addColorStop(0,'#ffffdf80');glow.addColorStop(1,'#ffffff00');ctx.fillStyle=glow;ctx.fillRect(-1,-1,2,2);
  }
  ctx.restore();
}
export function paintPreview(canvas,b,s){const ctx=canvas.getContext('2d'),size=canvas.width;paintSurface(ctx,b,size);ctx.save();ctx.scale(size/400,size/400);ctx.strokeStyle=shade(b.color,-.5);ctx.lineWidth=1;for(let i=0;i<9;i++){const p=40+i*40;ctx.beginPath();ctx.moveTo(40,p);ctx.lineTo(360,p);ctx.moveTo(p,40);ctx.lineTo(p,360);ctx.stroke();}for(const[x,y,c]of[[2,2,'B'],[3,2,'W'],[3,3,'B'],[4,3,'W'],[5,5,'B'],[5,4,'W'],[6,5,'B']])paintStone(ctx,40+x*40,40+y*40,18,c,s);ctx.restore();}
