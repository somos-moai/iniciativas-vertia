import {ease,seg,lerp,STORY} from '../motion.js';

// Every write is derived from p. No elapsed time or accumulated state.
export function createScene(id,pin){
 let el;
 const render=p=>{
  if(!el)return;
  const q=Math.max(0,Math.min(1,Number.isFinite(Number(p))?Number(p):0));
  const readingSubject=id.endsWith('intro')||['modelo','alcance','cierre'].includes(id);
  const start=readingSubject?STORY.enterStart:STORY.visualStart,end=readingSubject?STORY.enterEnd:STORY.visualEnd;
  const k=ease.premium(seg(q,start,end));
  el.dataset.progress=q.toFixed(5);
  const travel=Math.round(lerp(STORY.travel,0,k));
  el.style.setProperty('--visual-x',`${id==='hero'?travel:0}px`);
  el.style.setProperty('--visual-shift',`${id==='problema'?travel:0}px`);
  el.style.setProperty('--visual-scale',String(lerp(1-STORY.push,1,k)));
  el.style.setProperty('--story-progress',String(q));
  el.querySelectorAll('[data-protagonist]').forEach(node=>{node.style.willChange=q>start&&q<end?'transform':'auto';});
  const shots=[...el.querySelectorAll('[data-shot]')];
  const step=Math.min(shots.length-1,Math.floor(q*shots.length));
  shots.forEach(node=>{const active=Number(node.dataset.shot)===step;node.hidden=!active;node.setAttribute('aria-hidden',String(!active));});
  el.querySelectorAll('[data-step]').forEach(node=>{const active=Number(node.dataset.step)===step;node.setAttribute('aria-pressed',String(active));});
  el.querySelectorAll('[data-current-step]').forEach(node=>{node.textContent=`0${step+1} / 05`;});
 };
 return {id,pin,render,mount(node){el=node;render(0);return()=>{el=undefined;};}};
}
