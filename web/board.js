import {paintSurface,paintStone,shade} from './skins.js';
export function mountBoard(canvas,match,equipped,items,onPlay) {
  if(!canvas)return;
  const n=match.size,board=items.find(i=>i.id===equipped.board),stones=items.find(i=>i.id===equipped.stones);
  let hover=null,keyboardPoint=[Math.floor(n/2),Math.floor(n/2)];
  const allowed=()=>!match.finished&&!match.thinking&&match.next==='B';
  const occupied=point=>match.stones.some(([x,y])=>x===point[0]&&y===point[1]);
  canvas.width=1000;canvas.height=1000;
  const ctx=canvas.getContext('2d'),size=1000,pad=76,step=848/(n-1),dark=['midnight','railway_night','neon_grid','star_chart'].includes(board.id),line=dark?'#acb8b7':'#6d573e';
  function point(e){const rect=canvas.getBoundingClientRect();const x=Math.round(((e.clientX-rect.left)/rect.width*1000-pad)/step),y=n-1-Math.round(((e.clientY-rect.top)/rect.height*1000-pad)/step);return x>=0&&x<n&&y>=0&&y<n?[x,y]:null;}
  function play(p){if(p&&allowed()&&!occupied(p))onPlay(p);}
  canvas.addEventListener('pointermove',e=>{if(e.pointerType!=='touch'){hover=point(e);draw();}});
  canvas.addEventListener('pointerleave',()=>{hover=null;draw();});
  canvas.addEventListener('click',e=>play(point(e)));
  canvas.addEventListener('keydown',e=>{const directions={ArrowLeft:[-1,0],ArrowRight:[1,0],ArrowUp:[0,1],ArrowDown:[0,-1]};if(directions[e.key]){e.preventDefault();const [x,y]=directions[e.key];keyboardPoint=[Math.min(n-1,Math.max(0,keyboardPoint[0]+x)),Math.min(n-1,Math.max(0,keyboardPoint[1]+y))];hover=keyboardPoint;draw();}if(e.key==='Enter'||e.key===' '){e.preventDefault();play(keyboardPoint);}});
  const map=match.territory||match.sensei?.preview;
  const dead=new Set((map?.dead||[]).map(([x,y])=>`${x},${y}`));
  canvas.dataset.territory=map&&match.showTerritory?(map.estimated?'estimated':'final'):'hidden';
  function stone(x,y,color,opacity=1){paintStone(ctx,pad+x*step,pad+(n-1-y)*step,step*.455,color,stones,(dead.has(`${x},${y}`)&&match.showTerritory) ? .35 : opacity);}
  function territory(){
    if(!map||!match.showTerritory)return;
    for(const [x,y,c] of map.points){
      if(occupied([x,y])&&!dead.has(`${x},${y}`))continue;
      const px=pad+x*step,py=pad+(n-1-y)*step,r=step*.17;
      ctx.lineWidth=1.5;
      if(c==='N'){ctx.fillStyle='#738e86';ctx.beginPath();ctx.arc(px,py,step*.065,0,Math.PI*2);ctx.fill();}
      else{ctx.fillStyle=c==='B'?'#172421e6':'#fff9e7f0';ctx.strokeStyle=c==='B'?'#ecddad':'#44544a';ctx.fillRect(px-r,py-r,r*2,r*2);ctx.strokeRect(px-r,py-r,r*2,r*2);}
    }
    for(const [x,y] of map.dead||[]){const px=pad+x*step,py=pad+(n-1-y)*step,r=step*.25;ctx.strokeStyle='#d34334';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(px-r,py-r);ctx.lineTo(px+r,py+r);ctx.moveTo(px-r,py+r);ctx.lineTo(px+r,py-r);ctx.stroke();}
  }
  function draw(){paintSurface(ctx,board,size);ctx.strokeStyle=line;ctx.lineWidth=1.4;for(let i=0;i<n;i++){const pos=pad+step*i;ctx.beginPath();ctx.moveTo(pad,pos);ctx.lineTo(size-pad,pos);ctx.moveTo(pos,pad);ctx.lineTo(pos,size-pad);ctx.stroke();}ctx.lineWidth=2;ctx.strokeRect(pad,pad,848,848);const stars=n===9?[2,4,6]:n===13?[3,6,9]:[3,9,15];for(const x of stars)for(const y of stars){const center=(n-1)/2;if(n!==19&&((x===center)!==(y===center)))continue;ctx.beginPath();ctx.fillStyle=line;ctx.arc(pad+x*step,pad+y*step,n===19?4:4.5,0,Math.PI*2);ctx.fill();}ctx.fillStyle=line;ctx.font='19px "DM Sans", sans-serif';ctx.textAlign='center';ctx.textBaseline='middle';const letters='ABCDEFGHJKLMNOPQRST';for(let i=0;i<n;i++){ctx.fillText(letters[i],pad+i*step,39);ctx.fillText(letters[i],pad+i*step,963);ctx.fillText(String(n-i),38,pad+i*step);ctx.fillText(String(n-i),962,pad+i*step);}for(const [x,y,c]of match.stones)stone(x,y,c);territory();if(match.last){const[x,y,c]=match.last;ctx.strokeStyle=c==='B'?'#fff9d9b0':'#475640a0';ctx.lineWidth=2;ctx.beginPath();ctx.arc(pad+x*step,pad+(n-1-y)*step,step*.105,0,Math.PI*2);ctx.stroke();}if(match.hint?.point&&!match.finished){const[x,y]=match.hint.point;ctx.strokeStyle=dark?'#e5e9a4':'#fffbe1';ctx.lineWidth=4;ctx.shadowColor='#e7ec8c';ctx.shadowBlur=16;ctx.beginPath();ctx.arc(pad+x*step,pad+(n-1-y)*step,step*.36,0,Math.PI*2);ctx.stroke();ctx.shadowBlur=0;}if(hover&&allowed()&&!occupied(hover))stone(...hover,'B',.4);}
  draw();
}
function lighten(hex,factor){const nums=hex.replace('#','').match(/.{2}/g).map(v=>parseInt(v,16));return `rgb(${nums.map(v=>Math.round(factor>0?v+(255-v)*factor:v*(1+factor))).join(',')})`;}
