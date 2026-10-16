import React,{useEffect,useState} from 'react';
import {Sun,Moon,Monitor} from 'lucide-react';
import './theme.css';

const KEY='vertia-theme';
const resolve=value=>value==='system'?(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'):value;
const saved=()=>{try{return ['light','dark','system'].includes(localStorage.getItem(KEY))?localStorage.getItem(KEY):'system'}catch{return 'system'}};
export function applyTheme(value=saved()){
  document.documentElement.dataset.theme=resolve(value);
  document.documentElement.style.colorScheme=resolve(value);
}
applyTheme();
export function ThemeToggle(){
  const [value,setValue]=useState(saved);
  useEffect(()=>{
    const media=matchMedia('(prefers-color-scheme: dark)');
    const update=()=>applyTheme(value);
    update();media.addEventListener('change',update);
    return()=>media.removeEventListener('change',update);
  },[value]);
  const Icon=value==='dark'?Moon:value==='light'?Sun:Monitor;
  return <label className="theme-control"><Icon size={16} aria-hidden="true"/><span className="sr-only">Tema de color</span><select aria-label="Tema de color" value={value} onChange={e=>{const next=e.target.value;setValue(next);localStorage.setItem(KEY,next);applyTheme(next)}}><option value="system">Sistema</option><option value="light">Claro</option><option value="dark">Oscuro</option></select></label>;
}
