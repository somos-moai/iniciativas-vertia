// Google Drive does not reliably support npm's concurrent tar extraction.
// Build in a dedicated local cache, then copy only the generated output back.
const fs=require('fs'),path=require('path'),os=require('os'),{spawnSync}=require('child_process');
const root=__dirname,cache=path.join(os.tmpdir(),'vertia-frontend-codex');
fs.mkdirSync(cache,{recursive:true});
for(const p of ['package.json','index.html','vite.config.js','src','public'])fs.cpSync(path.join(root,p),path.join(cache,p),{recursive:true});
console.log('Local build workspace:',cache);
let r=spawnSync('npm.cmd',['install','--no-audit','--no-fund'],{cwd:cache,shell:true,stdio:'inherit'});if(r.status)process.exit(r.status||1);
r=spawnSync('npm.cmd',['run','build'],{cwd:cache,shell:true,stdio:'inherit'});if(r.status)process.exit(r.status||1);
fs.cpSync(path.join(cache,'dist'),path.join(root,'dist'),{recursive:true});
fs.copyFileSync(path.join(cache,'package-lock.json'),path.join(root,'package-lock.json'));
console.log('Build copied into frontend/dist.');
