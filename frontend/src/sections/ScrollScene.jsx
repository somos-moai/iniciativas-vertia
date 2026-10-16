import React,{useEffect,useRef} from 'react';
import {STORY,PARALLAX} from '../motion.js';

let frozen=null;
function installHook(){
 window.__sections=window.__sections||{};
 window.freezeAt=(id,p)=>{
  const scene=window.__sections[id];if(!scene)return false;
  const progress=Math.min(1,Math.max(0,Number(p)||0));
  frozen={id,p:progress};
  const top=window.scrollY+scene.el.getBoundingClientRect().top;
  const length=Math.max(0,scene.el.offsetHeight-innerHeight);
  window.scrollTo({top:top+progress*length,behavior:'instant'});
  scene.render(progress);
  return true;
 };
}
export function ScrollScene({scene,children,className=''}){
 const root=useRef(null);
 useEffect(()=>{
  const el=root.current;const unmount=scene.mount(el);
  installHook();window.__sections[scene.id]={el,render:scene.render};
  const reduced=matchMedia('(prefers-reduced-motion: reduce)');
  let frame=0,visible=true;
  const draw=()=>{
   frame=0;
   if(frozen?.id===scene.id){scene.render(frozen.p);return;}
   if(reduced.matches){scene.render(1);return;}
   if(!visible)return;
   const r=el.getBoundingClientRect(),length=Math.max(1,el.offsetHeight-innerHeight);
   scene.render(Math.max(0,Math.min(1,-r.top/length)));
  };
  const schedule=()=>{if(!frame)frame=requestAnimationFrame(draw);};
  const resume=()=>{frozen=null;schedule();};
  const observer=new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;if(visible)schedule();},{rootMargin:'100% 0px'});observer.observe(el);
  window.addEventListener('scroll',schedule,{passive:true});window.addEventListener('resize',schedule);
  window.addEventListener('wheel',resume,{passive:true});window.addEventListener('touchstart',resume,{passive:true});
  const key=e=>{if(['ArrowDown','ArrowUp','PageDown','PageUp','Home','End',' '].includes(e.key))resume();};window.addEventListener('keydown',key);
  reduced.addEventListener('change',schedule);
  const query=new URLSearchParams(location.search);
  document.fonts.ready.then(()=>{if(query.get('s')===scene.id)window.freezeAt(scene.id,query.get('p'));else schedule();});
  draw();
  return()=>{unmount();observer.disconnect();cancelAnimationFrame(frame);delete window.__sections[scene.id];window.removeEventListener('scroll',schedule);window.removeEventListener('resize',schedule);window.removeEventListener('wheel',resume);window.removeEventListener('touchstart',resume);window.removeEventListener('keydown',key);reduced.removeEventListener('change',schedule);};
 },[scene]);
 return <section ref={root} id={scene.id} className={`v3-chapter ${className}`} style={{'--pin':scene.pin,'--mobile-pin':STORY.mobilePin,'--mobile-travel':PARALLAX.mid}} aria-label={scene.id}><div className="v3-stage"><div className="v3-stage-inner">{children}</div><div className="v3-scene-progress" aria-hidden="true"><i/></div></div></section>;
}
