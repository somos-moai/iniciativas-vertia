// Read-only, local presentation audit. Never calls application mutation endpoints.
const fs=require('fs'),path=require('path'),os=require('os');
const {chromium}=require(path.join(os.tmpdir(),'vertia-browser-qa/node_modules/playwright'));
const out=path.resolve(__dirname,'../artifacts/qa/experience-v3/presentation');fs.mkdirSync(out,{recursive:true});
const base=process.env.VERTIA_PRESENTATION_BASE||'http://127.0.0.1:5180';
if(!/^http:\/\/(127\.0\.0\.1|localhost):/.test(base))throw Error('Local preview only');
const ids=['hero','problema','app1-intro','app1-wow','app2-intro','app2-wow','modelo','regional','alcance','cierre'];
const values=[0,.25,.5,.75,1];
const report={base,checks:[],errors:[],failedResources:[],snapshots:[]};
function auditContrast(id){
 const rgb=s=>(s.match(/[\d.]+/g)||[]).map(Number);
 const blend=(f,b)=>{const a=f[3]??1;return f.slice(0,3).map((c,i)=>c*a+b[i]*(1-a));};
 const lum=c=>c.map(x=>{x/=255;return x<=.04045?x/12.92:((x+.055)/1.055)**2.4;}).reduce((s,x,i)=>s+x*[.2126,.7152,.0722][i],0);
 const nodes=[...document.querySelectorAll(`#${id} *, .v3-header *`)];
 return nodes.filter(el=>el.getClientRects().length&&[...el.childNodes].some(c=>c.nodeType===3&&c.textContent.trim())&&el.getBoundingClientRect().top>=0&&el.getBoundingClientRect().bottom<=innerHeight).flatMap(el=>{
  const st=getComputedStyle(el);if(st.opacity==='0')return [];
  const chain=[];let n=el;while(n){chain.push(rgb(getComputedStyle(n).backgroundColor));n=n.parentElement;}
  let bg=[255,255,255];for(const c of chain.reverse())bg=blend(c,bg);
  const c=blend(rgb(st.color),bg),L=[lum(c),lum(bg)].sort((a,b)=>b-a),ratio=(L[0]+.05)/(L[1]+.05);
  return ratio<4.5?[{text:el.textContent.trim().slice(0,90),class:el.className,ratio:Number(ratio.toFixed(3)),color:st.color,bg}]:[];
 });
}
function check(name,pass,detail){report.checks.push({name,pass:!!pass,detail});if(!pass)console.log('FAIL',name,JSON.stringify(detail));}
async function state(page,id){return page.evaluate(id=>{const el=document.getElementById(id),title=el.querySelector('h1,h2'),r=title.getBoundingClientRect(),shot=el.querySelector('[data-shot]:not([hidden])');return {p:el.dataset.progress,transform:getComputedStyle(el.querySelector('[data-protagonist]')||el).transform,shot:[...el.querySelectorAll('[data-shot]')].findIndex(s=>!s.hidden),frameOverflow:shot?shot.scrollHeight-shot.clientHeight:0,overflow:document.documentElement.scrollWidth-innerWidth,title:[r.x,r.y,r.width,r.height],visible:[...el.querySelectorAll('[data-shot]')].filter(s=>!s.hidden).length};},id);}
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true});
 for(const [name,viewport] of Object.entries({desktop:{width:1440,height:900},mobile:{width:390,height:844}})){
  const page=await browser.newPage({viewport});page.on('pageerror',e=>report.errors.push(e.message));page.on('response',r=>{if(r.status()>=400)report.failedResources.push({url:r.url(),status:r.status()});});
  await page.goto(base,{waitUntil:'networkidle'});await page.waitForFunction(()=>Object.keys(window.__sections||{}).length===10&&typeof window.freezeAt==='function');await page.evaluate(()=>document.fonts.ready);
  check(`${name}: ten registered scenes`,await page.evaluate(()=>Object.keys(window.__sections||{}).length)===10);
  for(const id of ids){
   const forward=[];
   for(const p of values){await page.evaluate(([id,p])=>window.freezeAt(id,p),[id,p]);await page.evaluate(()=>new Promise(requestAnimationFrame));const s=await state(page,id);forward.push(s);check(`${name}: ${id} p${p} exact`,Number(s.p)===p,s);check(`${name}: ${id} p${p} no overflow`,s.overflow<=0,s.overflow);if(id.endsWith('wow'))check(`${name}: ${id} p${p} shot`,s.shot===Math.min(4,Math.floor(p*4)),s.shot);const file=`${name}_${id}_p${String(p).replace('.','')}.png`;await page.screenshot({path:path.join(out,file)});report.snapshots.push(file);}
   for(const p of [...values].reverse()){await page.evaluate(([id,p])=>window.freezeAt(id,p),[id,p]);await page.evaluate(()=>new Promise(requestAnimationFrame));const s=await state(page,id),old=forward[values.indexOf(p)];check(`${name}: ${id} reverse p${p}`,s.transform===old.transform&&s.shot===old.shot,{before:old,after:s});}
   if(name==='desktop'){const y=forward.slice(1,4).map(s=>s.title[1]);check(`${name}: ${id} fixed reading hold`,Math.max(...y)-Math.min(...y)<2,y);}
  }
  check(`${name}: all editorial images loaded`,await page.evaluate(()=>[...document.querySelectorAll('.v3-editorial img,.v3-intro-illustration img')].every(img=>img.complete&&img.naturalWidth===1599&&img.naturalHeight===900&&!img.hidden)));
  check(`${name}: official Global logo`,await page.evaluate(()=>[...document.querySelectorAll('img[alt="Global Vía Pública"]')].every(img=>img.getAttribute('src')==='/brand/global-oficial.webp'&&img.naturalWidth===721)));
  // Both interactive models and regional selectors must change visible content.
  await page.evaluate(()=>window.freezeAt('modelo',.5));await page.getByRole('tab',{name:'Contratos',exact:true}).click();check(`${name}: contract model`,await page.locator('.v3-model-root>strong').innerText()==='Contrato');await page.locator('.v3-model-branches button').first().click();check(`${name}: document model detail`,await page.locator('.v3-model-detail h3').innerText()==='Documento / versión');
  await page.evaluate(()=>window.freezeAt('regional',.5));await page.locator('.v3-country-tabs button[title="México"]').click();check(`${name}: region selection`,(await page.locator('.v3-country-info>strong').innerText()).includes('México'));
  for(const theme of ['dark','light']){
   await page.getByLabel('Tema de color',{exact:true}).selectOption(theme);
   for(const id of ids){
    for(const p of values){await page.evaluate(([id,p])=>window.freezeAt(id,p),[id,p]);await page.evaluate(()=>new Promise(requestAnimationFrame));const failures=await page.evaluate(auditContrast,id);check(`${name}: ${id} ${theme} p${p} contrast AA`,failures.length===0,failures);}
    await page.evaluate(([id])=>window.freezeAt(id,.5),[id]);await page.evaluate(()=>new Promise(requestAnimationFrame));
    if(theme==='dark'){await page.screenshot({path:path.join(out,`${name}_${id}_dark.png`)});report.snapshots.push(`${name}_${id}_dark.png`);}
   }
  }
  await page.goto(`${base}/?s=app1-wow&p=0.75`,{waitUntil:'networkidle'});await page.waitForFunction(()=>window.__sections?.['app1-wow']?.el.dataset.progress==='0.75000');check(`${name}: query QA hook`,(await state(page,'app1-wow')).p==='0.75000');
  await page.emulateMedia({reducedMotion:'reduce'});await page.goto(base,{waitUntil:'networkidle'});await page.waitForFunction(()=>Object.keys(window.__sections||{}).length===10);check(`${name}: reduced motion final states`,await page.evaluate(()=>[...document.querySelectorAll('.v3-chapter')].every(s=>s.dataset.progress==='1.00000')));check(`${name}: reduced motion no transforms`,await page.evaluate(()=>[...document.querySelectorAll('[data-protagonist]')].every(s=>getComputedStyle(s).transform==='none')));await page.screenshot({path:path.join(out,`${name}_reduced.png`)});
  await page.close();
 }
 check('zero page errors',report.errors.length===0,report.errors);check('zero missing resources',report.failedResources.length===0,report.failedResources);
 await browser.close();report.passed=report.checks.filter(c=>c.pass).length;report.failed=report.checks.filter(c=>!c.pass).length;fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(report,null,2));console.log(`${report.passed}/${report.checks.length} checks; ${report.snapshots.length} screenshots; ${report.failed} failed`);process.exitCode=report.failed?1:0;
})().catch(e=>{console.error(e);process.exit(1);});
