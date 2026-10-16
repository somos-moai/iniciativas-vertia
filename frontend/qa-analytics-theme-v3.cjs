// Staging-only audit. Configuration changes use a dedicated synthetic demo database.
const fs=require('fs'),path=require('path'),os=require('os');
const {chromium}=require(path.join(os.tmpdir(),'vertia-browser-qa/node_modules/playwright'));
const base=process.env.VERTIA_QA_BASE||'http://127.0.0.1:5181';
if(!/^http:\/\/(127\.0\.0\.1|localhost):/.test(base))throw Error('Use local isolated staging');
const out=path.resolve(__dirname,'../artifacts/qa/experience-v3/analytics-theme');fs.mkdirSync(out,{recursive:true});
const report={base,checks:[],errors:[],contrast:[],screenshots:[]};
function check(name,pass,detail){report.checks.push({name,pass:!!pass,detail});console.log(pass?'PASS':'FAIL',name,detail===undefined?'':JSON.stringify(detail));}
function auditContrast(){
 const rgb=s=>(s.match(/[\d.]+/g)||[]).map(Number);
 const blend=(f,b)=>{const a=f[3]??1;return f.slice(0,3).map((c,i)=>c*a+b[i]*(1-a));};
 const lum=c=>c.map(x=>{x/=255;return x<=.04045?x/12.92:((x+.055)/1.055)**2.4;}).reduce((s,x,i)=>s+x*[.2126,.7152,.0722][i],0);
 return [...document.querySelectorAll('.app *')].filter(el=>el.getClientRects().length&&[...el.childNodes].some(c=>c.nodeType===3&&c.textContent.trim())&&el.getBoundingClientRect().top>=0&&el.getBoundingClientRect().bottom<=innerHeight&&!el.closest('[disabled]')).flatMap(el=>{
  const st=getComputedStyle(el);if(st.opacity==='0')return[];
  const chain=[];let n=el;while(n){chain.push(rgb(getComputedStyle(n).backgroundColor));n=n.parentElement;}
  let bg=[255,255,255];for(const c of chain.reverse())bg=blend(c,bg);
  const c=blend(rgb(st.color),bg),L=[lum(c),lum(bg)].sort((a,b)=>b-a),ratio=(L[0]+.05)/(L[1]+.05);
  return ratio<4.5?[{text:el.textContent.trim().slice(0,75),class:typeof el.className==='string'?el.className:'',tag:el.tagName,ratio:Number(ratio.toFixed(3)),color:st.color,bg}]:[];
 });
}
async function screenshot(page,name){await page.screenshot({path:path.join(out,name),fullPage:true});report.screenshots.push(name);}
async function noOverflow(page,name){const d=await page.evaluate(()=>({width:document.documentElement.scrollWidth,viewport:innerWidth}));check(name,d.width<=d.viewport,d);}
async function nav(page,title){const menu=page.getByRole('button',{name:'Abrir menú',exact:true});if(await menu.isVisible())await menu.click();await page.locator('.side-nav').getByRole('button',{name:title,exact:true}).click();}
async function contrast(page,name){const failures=await page.evaluate(auditContrast);report.contrast.push({name,failures});check(name+' AA',failures.length===0,failures.slice(0,12));}
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true});const __nc=browser.newContext.bind(browser);browser.newContext=async(o)=>{const c=await __nc(o);await c.addInitScript(()=>{for(const a of ['prospectador','contratos'])if(!localStorage.getItem('vertia-demo-profile-v3-'+a))localStorage.setItem('vertia-demo-profile-v3-'+a,'regional')});return c};
 try{
  for(const [app,title] of [['prospectador','Decisiones con perspectiva.'],['contratos','Visibilidad para anticiparse.']]){
   const ctx=await browser.newContext({viewport:{width:1440,height:1000}}),page=await ctx.newPage();page.setDefaultTimeout(60000);page.on('pageerror',e=>report.errors.push(e.message));
   await page.goto(base+'/'+app,{waitUntil:'domcontentloaded'});await page.getByRole('heading',{name:title,exact:true}).waitFor();
   check(app+' dashboard loaded',await page.locator('.an-metric').count()===4);
   check(app+' explicit demo identity',(await page.locator('.profile-select>span').innerText()).includes('Perfil de demostración · no SSO'));
   const state=await page.evaluate(async app=>await(await fetch('/api/state?app='+app,{headers:{'X-Demo-User':'regional'}})).json(),app);
   check(app+' named profiles',app==='prospectador'?['Agustín Silva','Santiago Ordoñez','Enrique Escobar'].every(n=>state.users.some(u=>u.name===n)):['Gonzalo Oviedo','Phillipe'].every(n=>state.users.some(u=>u.name===n)));
   await page.getByLabel('Periodo del dashboard',{exact:true}).fill('2026-09');
   const recordDate=r=>(r.sent_at||r.received_at||r.date||r.created_at||r.at||r.start_date||'').slice(0,10);
   const rows=app==='prospectador'?state.messages.filter(r=>r.direction==='outbound'&&['simulado','enviado_simulado'].includes(r.status)):state.contracts.filter(r=>!r.restricted&&!r.sanitized_only);
   const expected=rows.filter(r=>recordDate(r)>='2026-09-01'&&recordDate(r)<'2026-10-01').length;
   check(app+' September KPI matches records',Number((await page.locator('.an-metric').nth(1).locator('strong').innerText()).replaceAll('.',''))===expected,{expected,actual:await page.locator('.an-metric').nth(1).locator('strong').innerText()});
   await page.getByRole('button',{name:'YTD',exact:true}).click();const ytd=rows.filter(r=>recordDate(r)>='2026-01-01'&&recordDate(r)<'2026-10-01').length;
   check(app+' YTD matches records',Number((await page.locator('.an-metric').nth(1).locator('strong').innerText()).replaceAll('.',''))===ytd,{expected:ytd});
   await page.locator('.an-metric').nth(1).click();check(app+' metric opens trace',await page.getByRole('dialog',{name:'Origen de la métrica'}).isVisible());check(app+' trace count matches metric',await page.locator('.an-trace-rows>button').count()===ytd);
   await screenshot(page,app+'-metric-origin.png');await page.getByRole('button',{name:'Cerrar origen de métrica',exact:true}).click();
   await page.getByRole('button',{name:'Mes',exact:true}).click();
   for(const theme of ['light','dark']){await page.getByLabel('Tema de color',{exact:true}).selectOption(theme);check(app+' theme '+theme,await page.evaluate(()=>document.documentElement.dataset.theme)===theme);await noOverflow(page,app+' desktop '+theme+' overflow');await contrast(page,app+' desktop '+theme+' dashboard');await screenshot(page,app+'-dashboard-'+theme+'.png');await page.evaluate(()=>scrollTo(0,650));await contrast(page,app+' desktop '+theme+' charts');await page.evaluate(()=>scrollTo(0,0));}
   await page.reload({waitUntil:'domcontentloaded'});await page.getByRole('heading',{name:title,exact:true}).waitFor();check(app+' theme persists after reload',await page.evaluate(()=>document.documentElement.dataset.theme)==='dark');
   const views=app==='prospectador'?['Descubrir prospectos','Contactos y créditos','Seguimiento','Propuestas y resultados','Agentes y reglas']:['Repositorio','Obligaciones','Tipos, plantillas y flujos'];
   for(const v of views){await nav(page,v);await contrast(page,app+' dark '+v);await screenshot(page,app+'-'+v.replaceAll(' ','-')+'-dark.png');}
   // Functional admin role has read-only regional access and can version configuration.
   if(app==='contratos'){
    const innovation=state.users.find(u=>u.name==='Gonzalo Oviedo');await page.getByLabel('Perfil de demostración',{exact:true}).selectOption(innovation.id);await page.getByText('Gonzalo Oviedo puede configurar tipos, plantillas y rutas.',{exact:false}).waitFor();
    const input=page.getByLabel('Nombre de configuración contractual',{exact:true});await input.fill('Configuración regional · QA v3');await page.getByRole('button',{name:'Guardar configuración',exact:true}).click();await page.getByText('Configuración guardada y versionada.',{exact:true}).waitFor();check('Innovation configuration persisted',true);
    await nav(page,'Repositorio');check('Innovation cannot create contracts',await page.getByRole('button',{name:'Nuevo contrato',exact:true}).isDisabled());await screenshot(page,'innovation-readonly.png');
   }
   await ctx.close();
   const mobile=await browser.newContext({viewport:{width:390,height:844},isMobile:true}),mp=await mobile.newPage();mp.setDefaultTimeout(60000);mp.on('pageerror',e=>report.errors.push(e.message));await mp.goto(base+'/'+app,{waitUntil:'domcontentloaded'});await mp.getByRole('heading',{name:title,exact:true}).waitFor();
   for(const theme of ['light','dark']){await mp.getByLabel('Tema de color',{exact:true}).selectOption(theme);await noOverflow(mp,app+' mobile '+theme+' overflow');await contrast(mp,app+' mobile '+theme+' dashboard');await screenshot(mp,app+'-mobile-'+theme+'.png');}
   await mobile.close();
  }
  check('No JavaScript errors',report.errors.length===0,report.errors);
 }finally{await browser.close();report.passed=report.checks.filter(c=>c.pass).length;report.failed=report.checks.filter(c=>!c.pass).length;fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(report,null,2));console.log(`${report.passed}/${report.checks.length} checks; ${report.failed} failed`);process.exitCode=report.failed?1:0;}
})().catch(e=>{console.error(e);process.exitCode=1});
