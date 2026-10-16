const fs=require('fs'),path=require('path'),os=require('os');
const {chromium}=require(path.join(os.tmpdir(),'vertia-browser-qa/node_modules/playwright'));
const out=path.resolve(__dirname,'../artifacts/qa/experience-v3/presentation');fs.mkdirSync(out,{recursive:true});
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true});
 const page=await browser.newPage({viewport:{width:1440,height:900}});await page.goto('http://127.0.0.1:5180',{waitUntil:'networkidle'});
 const cdp=await page.context().newCDPSession(page);
 await cdp.send('Tracing.start',{categories:'devtools.timeline,disabled-by-default-devtools.timeline.frame',transferMode:'ReturnAsStream'});
 const sample=await page.evaluate(async()=>{
  const node=document.getElementById('app1-wow'),start=scrollY+node.getBoundingClientRect().top,length=node.offsetHeight-innerHeight;
  window.dispatchEvent(new WheelEvent('wheel'));
  const deltas=[];let previous;
  for(let i=0;i<240;i++){
   const time=await new Promise(requestAnimationFrame);if(previous!==undefined)deltas.push(time-previous);previous=time;
   const p=i<120?i/119:(239-i)/119;window.scrollTo({top:start+length*p,behavior:'instant'});
  }
  const sorted=[...deltas].sort((a,b)=>a-b);return {frames:deltas.length,medianFrameMs:sorted[Math.floor(sorted.length/2)],p95FrameMs:sorted[Math.floor(sorted.length*.95)],framesOver25ms:deltas.filter(v=>v>25).length,deltas};
 });
 const done=new Promise(resolve=>cdp.once('Tracing.tracingComplete',resolve));await cdp.send('Tracing.end');const {stream}=await done;let trace='';for(;;){const result=await cdp.send('IO.read',{handle:stream});trace+=result.data;if(result.eof)break;}await cdp.send('IO.close',{handle:stream});fs.writeFileSync(path.join(out,'chrome-performance-trace.json'),trace);fs.writeFileSync(path.join(out,'performance.json'),JSON.stringify({...sample,context:'Headless Microsoft Edge, local preview; this is a desktop runtime sample, not a midrange hardware certification.'},null,2));console.log(JSON.stringify({...sample,deltas:undefined}));await browser.close();
})().catch(e=>{console.error(e);process.exitCode=1;});
