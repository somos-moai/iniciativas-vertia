// Read the explicitly provided demo credential file only in memory.
// Never print, copy, serialize or commit its contents.
const fs=require('fs'),path=require('path');
module.exports=function loadHTTPAuth(base){
 const filename=process.env.VERTIA_QA_CREDENTIAL_FILE||path.resolve(__dirname,'../../Acceso_Maquetas_Vertia.txt');
 if(!fs.existsSync(filename))return undefined;
 const input=fs.readFileSync(filename,'utf8');
 const find=names=>{for(const name of names){const match=input.match(new RegExp('^[ \\t*\\-]*(?:'+name+')[ \\t*]*[:=][ \\t]*(.+)$','im'));if(match)return match[1].trim().replace(/^[`"']|[`"']$/g,'')}return null};
 const username=find(['Usuario','Username','User']),password=find(['Clave','Contraseña','Password']);
 if(!username||!password)throw Error('El archivo autorizado de acceso no tiene las etiquetas Usuario y Clave esperadas.');
 return {username,password,origin:new URL(base).origin};
};
