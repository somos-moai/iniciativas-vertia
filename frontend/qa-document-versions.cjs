// Prueba de interfaz del cambio de versión documental: PDF → PNG → PDF.
// Comprueba los valores DOM de los campos propuestos sin escribirlos, en cada cuadro de animación,
// antes y después de recargar; además borradores por versión, evidencia, rechazo de revisión
// obsoleta y confirmación en la versión vigente.
// Ejecutar SOLO contra staging aislado (crea un expediente sintético y escribe en su base):
//   VERTIA_QA_BASE=http://127.0.0.1:5180 node frontend/qa-document-versions.cjs
const fs=require('fs'),path=require('path'),os=require('os');
const {chromium}=require(path.join(os.tmpdir(),'vertia-browser-qa/node_modules/playwright'));
const base=process.env.VERTIA_QA_BASE||'http://127.0.0.1:5180',repo=path.resolve(__dirname,'..'),out=path.join(repo,'artifacts/qa/document-versions');
fs.mkdirSync(out,{recursive:true});
if(/somosmoai\.tech/.test(base)){console.error('Esta prueba escribe datos: use un staging aislado, no producción.');process.exit(2)}
const report={started_at:new Date().toISOString(),base,checks:[],page_errors:[]};
const EXPECTED={'Monto propuesto':'12500','Moneda':'USD','Fecha de inicio':'2026-10-01','Vencimiento':'2027-12-31'};
function check(name,ok,detail=''){report.checks.push({name,ok,detail});console.log((ok?'PASS ':'FAIL ')+name+(detail?' — '+detail:''));if(!ok)throw Error(name+': '+detail)}

async function api(ctx,body,profile='regional'){const r=await ctx.request.post(base+'/api/actions',{headers:{'X-Demo-User':profile},data:body});return {status:r.status(),json:await r.json()}}
async function openDocuments(page,reference){
 await page.goto(base+'/contratos',{waitUntil:'networkidle'});
 await page.locator('.side-nav').getByRole('button',{name:'Repositorio',exact:true}).click();
 await page.locator('tr',{hasText:reference}).first().click();
 await page.locator('.detail-tabs').getByRole('button',{name:'Documentos'}).click();
 await page.locator('.dw-workspace').waitFor();
}
async function waitReading(page){await page.locator('.wb-success').waitFor({timeout:100000});await page.locator('.dw-processing').waitFor({state:'detached'})}
const selector=page=>page.getByLabel('Seleccionar documento del expediente');
// Espera a que el estado refrescado incluya la versión: con la semilla grande el refresco tarda más que la lectura.
async function optionFor(page,ext){await page.waitForFunction(ext=>[...(document.querySelector('select[aria-label="Seleccionar documento del expediente"]')?.options||[])].some(o=>o.textContent.includes(ext)),ext,{timeout:30000});return page.evaluate(ext=>[...document.querySelector('select[aria-label="Seleccionar documento del expediente"]').options].filter(o=>o.textContent.includes(ext)).at(-1).value,ext)}
// Observa cada cuadro: tarjetas visibles con un input vacío o con el archivo de otra versión es un fallo.
async function watchFrames(page){await page.evaluate(()=>{window.__dwBad=[];const sel=()=>document.querySelector('select[aria-label="Seleccionar documento del expediente"]');const tick=()=>{const inputs=[...document.querySelectorAll('.dw-field-card input[aria-label^="Valor revisado"]')];const s=sel();const expected=s?.selectedOptions[0]?.textContent.split(' · ')[0];const shown=document.querySelector('.dw-preview header span')?.textContent;if(inputs.length&&inputs.some(i=>i.value===''))window.__dwBad.push('vacío');if(inputs.length&&expected&&shown!==expected)window.__dwBad.push('archivo '+shown+' ≠ '+expected);window.__dwRaf=requestAnimationFrame(tick)};tick()})}
async function stopFrames(page){return page.evaluate(()=>{cancelAnimationFrame(window.__dwRaf);return [...new Set(window.__dwBad)]})}
async function values(page){return page.evaluate(()=>Object.fromEntries([...document.querySelectorAll('.dw-field-card input[aria-label^="Valor revisado"]')].map(i=>[i.getAttribute('aria-label').replace('Valor revisado: ',''),i.value])))}
async function switchTo(page,value){await watchFrames(page);await selector(page).selectOption(value);await page.locator('.dw-field-card').first().waitFor();await page.waitForTimeout(1200);return stopFrames(page)}
function assertPdf(label,v,bad){
 check(label+': sin cuadros vacíos ni cruzados',bad.length===0,bad.join(', '));
 for(const [k,expected] of Object.entries(EXPECTED))check(`${label}: ${k}`,v[k]===expected,`valor DOM "${v[k]}"`);
 check(label+': contraparte',/Faro Retail SpA/.test(v['Contraparte']||''),`valor DOM "${v['Contraparte']}"`);
}

async function main(){
 const browser=await chromium.launch({channel:'msedge',headless:true});const __nc=browser.newContext.bind(browser);browser.newContext=async(o)=>{const c=await __nc(o);await c.addInitScript(()=>{for(const a of ['prospectador','contratos'])if(!localStorage.getItem('vertia-demo-profile-v3-'+a))localStorage.setItem('vertia-demo-profile-v3-'+a,'regional')});return c};
 try{
  const ctx=await browser.newContext({viewport:{width:1440,height:1000}}),page=await ctx.newPage();
  page.on('pageerror',e=>report.page_errors.push(e.message));
  const created=await api(ctx,{app:'contratos',action:'create_contract',payload:{title:'QA versiones documentales',country:'CL',company:'Sociedad ficticia QA',amount:0}});
  check('Expediente sintético creado',created.status===200,String(created.status));
  const cid=created.json.entity.id,reference=created.json.entity.reference;
  await page.addInitScript(()=>['prospectador','contratos'].forEach(a=>localStorage.setItem('vertia-demo-profile-v3-'+a,'regional')));
  await openDocuments(page,reference);
  await page.getByRole('button',{name:'Probar PDF de ejemplo'}).click();await waitReading(page);
  await page.getByRole('button',{name:'Probar imagen de ejemplo'}).click();await waitReading(page);
  const pdf=await optionFor(page,'.pdf'),png=await optionFor(page,'.png');
  check('Dos versiones reales cargadas',Boolean(pdf&&png&&pdf!==png));
  let bad=await switchTo(page,pdf);assertPdf('PNG → PDF',await values(page),bad);
  check('Versión anterior rotulada',await page.locator('.dw-extraction .wb-note',{hasText:'Versión anterior'}).count()===1);
  check('Versión anterior no se puede confirmar',await page.locator('.dw-extraction button[type=submit]').isDisabled());
  bad=await switchTo(page,png);check('PDF → PNG: sin cuadros vacíos ni cruzados',bad.length===0,bad.join(', '));
  bad=await switchTo(page,pdf);assertPdf('PDF → PNG → PDF',await values(page),bad);
  await page.screenshot({path:path.join(out,'pdf-version-anterior.png'),fullPage:false});
  await page.reload({waitUntil:'networkidle'});await openDocuments(page,reference);
  check('Tras recargar se abre la versión vigente',await selector(page).inputValue()===png);
  bad=await switchTo(page,pdf);assertPdf('Recarga → PDF',await values(page),bad);
  // Borradores aislados por versión
  await switchTo(page,png);await page.getByLabel('Valor revisado: Monto propuesto').fill('12600');
  await switchTo(page,pdf);check('Borrador de la imagen no altera el PDF',(await values(page))['Monto propuesto']==='12500');
  await page.locator('.dw-source').nth(2).click();await page.waitForTimeout(800);
  check('Evidencia lleva a la página de origen',(await page.locator('.dw-pager span').textContent()).startsWith('Página 1 de 3'));
  await switchTo(page,png);check('Borrador de la versión vigente se conserva',(await values(page))['Monto propuesto']==='12600');
  const obsolete=await api(ctx,{app:'contratos',action:'review_extraction',entity_id:cid,payload:{document_id:pdf,fields:{amount:12500}}});
  check('Backend rechaza revisión de versión anterior',obsolete.status===409,String(obsolete.status));
  await page.locator('.dw-field-card',{hasText:'Monto propuesto'}).locator('input[type=checkbox]').check();
  await page.getByRole('button',{name:'Confirmar campos revisados'}).click();await page.locator('.dw-reviewed').waitFor();
  const st=await (await ctx.request.get(base+'/api/state?app=contratos',{headers:{'X-Demo-User':'regional'}})).json();
  check('Confirmación en versión vigente persiste',st.contracts.find(c=>c.id===cid).amount===12600);
  await page.setViewportSize({width:390,height:844});await page.waitForTimeout(300);
  const d=await page.evaluate(()=>({width:document.documentElement.scrollWidth,viewport:innerWidth}));
  check('Móvil 390 sin scroll horizontal',d.width<=d.viewport+1,JSON.stringify(d));
  check('Sin errores JavaScript',report.page_errors.length===0,report.page_errors.join(' | '));
 }finally{
  report.finished_at=new Date().toISOString();report.passed=report.checks.filter(c=>c.ok).length;report.total=report.checks.length;
  fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(report,null,2));await browser.close();
 }
}
main().then(()=>console.log(`\n${report.passed}/${report.total} comprobaciones aprobadas`)).catch(e=>{console.error(e.message);process.exitCode=1});
