// Contrato compartido de movimiento, MOTION_GUIDE §§1–3.
export const EASE = {
  enter:'cubic-bezier(0.16, 1, 0.3, 1)', premium:'cubic-bezier(0.22, 1, 0.36, 1)',
  move:'cubic-bezier(0.76, 0, 0.24, 1)', exit:'cubic-bezier(0.7, 0, 0.84, 0)', pop:'cubic-bezier(0.34, 1.56, 0.64, 1)'
};
export const MS={feedback:150,move:400,hero:750,exit:240};
export const STAGGER={letter:30,word:90,item:60};
export const PARALLAX={front:1,mid:.5,back:.2};
export const STORY={enterStart:0,enterEnd:.18,visualStart:.22,visualEnd:.72,holdStart:.18,holdEnd:.84,push:.02,travel:44,mobilePin:.7};
const bezier=(x1,y1,x2,y2)=>x=>{
  let t=x;
  for(let i=0;i<8;i++){
    const cx=3*x1*t*(1-t)**2+3*x2*t*t*(1-t)+t**3-x;
    const dx=3*x1*(1-t)**2+6*(x2-x1)*t*(1-t)+3*(1-x2)*t*t;
    if(Math.abs(dx)<1e-6)break;
    t=Math.min(1,Math.max(0,t-cx/dx));
  }
  return 3*y1*t*(1-t)**2+3*y2*t*t*(1-t)+t**3;
};
export const ease={enter:bezier(.16,1,.3,1),premium:bezier(.22,1,.36,1),move:bezier(.76,0,.24,1),exit:bezier(.7,0,.84,0)};
export const seg=(p,a,b)=>Math.min(1,Math.max(0,(p-a)/(b-a)));
export const lerp=(a,b,k)=>a+(b-a)*k;
export function spring(t,zeta=.8,f=2){
  if(t<=0)return 0;
  const w=2*Math.PI*f;
  if(zeta>=1)return 1-Math.exp(-w*t)*(1+w*t);
  const wd=w*Math.sqrt(1-zeta*zeta);
  return 1-Math.exp(-zeta*w*t)*(Math.cos(wd*t)+zeta*w/wd*Math.sin(wd*t));
}
export const rng=seed=>()=>((seed=(seed*16807)%2147483647)-1)/2147483646;
