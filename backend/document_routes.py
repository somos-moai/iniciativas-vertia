"""Private real uploads with bounded local extraction. No paid APIs are used."""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path
from uuid import uuid4

from fastapi import Depends, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from .db import DocumentUpload

MAX_BYTES=15*1024*1024
MAX_PAGES=40
WORKER_SECONDS=90
_processing=threading.BoundedSemaphore(1)

def upload_root():
    value=os.environ.get("UPLOAD_DIR")
    if not value:
        raise HTTPException(503,"El almacenamiento privado de documentos todavía no está habilitado")
    root=Path(value).resolve()
    root.mkdir(mode=0o700,parents=True,exist_ok=True)
    os.chmod(root,0o700)
    return root

def folder_for(key):
    if not re.fullmatch(r"[a-f0-9]{32}",key): raise HTTPException(404,"Documento no disponible")
    root=upload_root(); path=(root/key).resolve()
    if not path.is_relative_to(root): raise HTTPException(403,"Ruta no permitida")
    return path

def cleanup(folder):
    # Only our verified UUID folder under UPLOAD_DIR, never a recursive delete.
    root=upload_root()
    if not folder.resolve().is_relative_to(root) or not re.fullmatch(r"[a-f0-9]{32}",folder.name):
        return
    for item in folder.iterdir():
        if item.is_file(): item.unlink(missing_ok=True)
    folder.rmdir()

def original_path(upload):
    ext={"application/pdf":".pdf","image/png":".png","image/jpeg":".jpg","image/webp":".webp"}[upload.content_type]
    return folder_for(upload.storage_key)/("original"+ext)

def require_native(s,user,contract):
    from . import main as api
    api.read(s,user,contract)
    if user["role"]!="regional" and user["country"]!=contract.data["country"]:
        raise HTTPException(403,"El acceso entre países permite únicamente la copia saneada, no el original ni su texto")

def public_document(upload):
    return {"id":upload.id,"filename":upload.filename,"content_type":upload.content_type,"mime":upload.content_type,"size_bytes":upload.size_bytes,"kind":upload.extraction.get("kind","contrato"),"version":upload.version,"created_at":upload.created_at.isoformat(),"page_count":upload.extraction.get("page_count",0),"status":upload.status,"synthetic":False,"real":True,"extraction_mode":"local_extraction","text_characters":upload.extraction.get("text_characters",0),"requires_review":upload.extraction.get("review_status")!="reviewed"}

def local_analysis(upload,contract):
    result=upload.extraction
    pages=[{k:p.get(k) for k in ["page","method","chars","confidence"]} for p in result.get("pages",[])]
    simulated_scan=any(p.get("method")=="escaneo_simulado" for p in result.get("pages",[]))
    return {"provider":"Texto PDF + escaneo simulado por nombre de archivo" if simulated_scan else "Lectura local del texto PDF","scan_simulated":simulated_scan,"mode":"local_extraction","simulated":False,"ai_connected":False,"ai_status":"Claude no conectado; lectura y reglas locales, sin interpretación jurídica por IA","document_id":upload.id,"summary":f"Se leyeron {len(pages)} páginas y {result.get('text_characters',0)} caracteres del archivo aportado. Se proponen {len(result.get('proposed_fields',[]))} campos mediante reglas locales; requieren revisión humana.","text_preview":"\n\n".join(p.get("text","") for p in result.get("pages",[]))[:4000],"pages":pages,"proposed_fields":result.get("proposed_fields",[]),"findings":[],"risk":"no_evaluado","risk_level":"no_evaluado","score":None,"warnings":result.get("warnings",[]),"source_version":upload.version,"analyzed_at":result.get("processed_at"),"requires_human_review":result.get("review_status")!="reviewed","review_status":result.get("review_status","pending"),"reviewed_fields":result.get("reviewed_fields",{}),"reviewed_by":result.get("reviewed_by"),"reviewed_at":result.get("reviewed_at")}

def review_extraction(s,user,contract,payload):
    from . import main as api
    if contract.data["status"] not in {"borrador","rechazado","en_renovacion"}:
        raise HTTPException(409,"La ficha solo puede actualizarse en borrador, rechazo o renovación")
    did=payload.get("document_id") or (contract.data.get("analysis") or {}).get("document_id")
    upload=s.get(DocumentUpload,did)
    if not upload or upload.contract_id!=contract.id: raise HTTPException(404,"Documento real no encontrado")
    require_native(s,user,contract)
    if upload.version!=contract.data["version"]: raise HTTPException(409,"La versión cambió; revise la extracción del documento más reciente")
    fields=payload.get("fields",{})
    if not isinstance(fields,dict) or not fields: raise HTTPException(400,"Seleccione al menos un campo para confirmar")
    permitted={"amount","currency","start_date","end_date","type","counterparty"}
    if set(fields)-permitted: raise HTTPException(400,"La revisión incluye campos no permitidos")
    accepted={}
    for field,value in fields.items():
        if field=="amount": accepted[field]=api.amount_field({"amount":value})
        elif field in {"start_date","end_date"}: accepted[field]=api.iso_date(value)
        elif field=="currency":
            if value not in {"USD","CLP","UF","EUR","PEN","MXN","UYU","ARS"}: raise HTTPException(400,"Moneda no admitida")
            accepted[field]=value
        else: accepted[field]=api.text_field({field:value},field,limit=200)
    upload.extraction={**upload.extraction,"review_status":"reviewed","reviewed_fields":accepted,"reviewed_by":user["id"],"reviewed_at":api.now(),"review_notes":str(payload.get("notes",""))[:2000]}
    s.add(upload)
    api.save(s,contract,**accepted,analysis=local_analysis(upload,contract),redacted_ready=False,redaction=None)
    docs=[]
    for doc in contract.data["documents"]:
        docs.append(public_document(upload) if doc.get("id")==upload.id else doc)
    api.save(s,contract,documents=docs)

def install_upload_routes(app):
    from . import main as api

    @app.get("/api/document-capabilities")
    def capabilities(user=Depends(api.viewer)):
        ready=bool(os.environ.get("UPLOAD_DIR"))
        # Demostración: las imágenes se identifican por nombre de archivo (escaneo simulado), sin OCR.
        languages=[]
        return {"real_uploads":ready,"max_bytes":MAX_BYTES,"max_pages":MAX_PAGES,"max_pixels":20_000_000,"timeout_seconds":WORKER_SECONDS,"concurrency":1,"supported_types":["application/pdf","image/png","image/jpeg","image/webp"],"ocr_available":False,"scan_mode":"simulado_por_nombre_de_archivo","ocr_languages":languages,"claude_connected":False,"mode":"local_extraction"}

    @app.post("/api/contracts/{cid}/uploads")
    @app.post("/api/contracts/{cid}/upload",include_in_schema=False)
    def upload(cid:str,file:UploadFile=File(...),kind:str=Form("contrato"),s:Session=Depends(api.session),user=Depends(api.viewer)):
        contract=api.get(s,"contratos","contracts",cid)
        api.write(s,user,contract); require_native(s,user,contract)
        if contract.data["status"] not in {"borrador","rechazado","en_renovacion"}: raise HTTPException(409,"Para cargar una nueva versión, el contrato debe estar en borrador, rechazado o en renovación")
        if not _processing.acquire(blocking=False): raise HTTPException(429,"Otro documento se está procesando. Intente nuevamente en unos segundos.",headers={"Retry-After":"5"})
        folder=None
        try:
            root=upload_root(); key=uuid4().hex; folder=folder_for(key); folder.mkdir(mode=0o700)
            name=re.sub(r"[\x00-\x1f\x7f/\\]","_",file.filename or "documento")[:200]
            head=file.file.read(16); file.file.seek(0)
            if not head: raise HTTPException(422,"El archivo está vacío")
            if head.startswith(b"%PDF-"): mime="application/pdf"; suffix=".pdf"; exts={".pdf"}
            elif head.startswith(b"\x89PNG\r\n\x1a\n"): mime="image/png"; suffix=".png"; exts={".png"}
            elif head.startswith(b"\xff\xd8\xff"): mime="image/jpeg"; suffix=".jpg"; exts={".jpg",".jpeg"}
            elif head.startswith(b"RIFF") and head[8:12]==b"WEBP": mime="image/webp"; suffix=".webp"; exts={".webp"}
            else: raise HTTPException(415,"Formato no válido: cargue PDF, PNG, JPEG o WebP con contenido real")
            if Path(name).suffix.lower() not in exts: raise HTTPException(415,"La extensión del archivo no coincide con su contenido")
            if file.content_type not in {mime,"application/octet-stream",None}: raise HTTPException(415,"El tipo MIME declarado no coincide con el archivo")
            path=folder/("original"+suffix); size=0; digest=hashlib.sha256()
            with open(path,"xb") as output:
                os.chmod(path,0o600)
                while chunk:=file.file.read(65536):
                    size+=len(chunk)
                    if size>MAX_BYTES: raise HTTPException(413,"El archivo excede el máximo de 15 MB")
                    digest.update(chunk); output.write(chunk)
            if not size: raise HTTPException(422,"El archivo está vacío")
            started=time.monotonic()
            # The parser needs local fonts/OCR, never DB passwords or provider keys.
            worker_env={key:value for key,value in os.environ.items() if key.upper() in {"PATH","LANG","LC_ALL","HOME","SYSTEMROOT","WINDIR","TEMP","TMP","APPDATA","LOCALAPPDATA","USERPROFILE","TESSDATA_PREFIX"}}
            worker_env.update({"OMP_THREAD_LIMIT":"1","PYTHONIOENCODING":"utf-8"})
            try:
                worker=subprocess.run([sys.executable,"-m","backend.document_worker",str(path),str(folder),mime,name],capture_output=True,text=True,encoding="utf-8",timeout=WORKER_SECONDS,cwd=Path(__file__).resolve().parents[1],env=worker_env)
            except subprocess.TimeoutExpired: raise HTTPException(422,"La lectura superó 90 segundos. Divida el documento o use una copia más legible.")
            try: result=json.loads(worker.stdout)
            except Exception: raise HTTPException(422,"El lector no pudo procesar el documento; pruebe una copia válida y más pequeña")
            if worker.returncode or result.get("status")=="failed": raise HTTPException(422,result.get("error","Documento ilegible o dañado"))
            version=contract.data.get("version",0)+1
            result.update({"processed_at":api.now(),"elapsed_seconds":round(time.monotonic()-started,2),"kind":kind[:64],"review_status":"pending"})
            from datetime import datetime,timezone
            record=DocumentUpload(id=f"upload-{key[:16]}",contract_id=cid,filename=name,content_type=mime,storage_key=key,sha256=digest.hexdigest(),size_bytes=size,version=version,status=result["status"],extraction=result,uploaded_by=user["id"],created_at=datetime.now(timezone.utc))
            s.add(record); s.flush()
            doc=public_document(record)
            api.save(s,contract,version=version,documents=contract.data.get("documents",[])+[doc],analysis=local_analysis(record,contract),redacted_ready=False,redaction=None,has_real_uploads=True)
            api.audit(s,"contratos",user,"upload_real_document",contract,f"Archivo real leído localmente: {result['page_count']} páginas; sin APIs externas")
            s.commit()
            return {"ok":True,"message":"Documento cargado y leído. Revise los campos propuestos antes de aplicarlos.","entity":contract.data,"document":doc,"processing":{"status":record.status,"elapsed_seconds":result["elapsed_seconds"],"page_count":result["page_count"],"text_characters":result["text_characters"],"warnings":result["warnings"],"ai_connected":False}}
        except Exception:
            s.rollback()
            if folder and folder.exists(): cleanup(folder)
            raise
        finally:
            file.file.close()
            _processing.release()

    def uploaded(s,user,cid,did):
        c=api.get(s,"contratos","contracts",cid); require_native(s,user,c)
        u=s.get(DocumentUpload,did)
        if not u or u.contract_id!=cid: raise HTTPException(404,"Archivo no encontrado")
        return c,u

    @app.get("/api/contracts/{cid}/uploads/{did}/text")
    def text(cid:str,did:str,s:Session=Depends(api.session),user=Depends(api.viewer)):
        c,u=uploaded(s,user,cid,did)
        pages=[{**{k:p.get(k) for k in ["page","text","method","confidence","chars"]},"preview_url":f"/api/contracts/{cid}/uploads/{did}/preview?page={p['page']}"} for p in u.extraction.get("pages",[])]
        return {"document":public_document(u),"pages":pages,"proposed_fields":u.extraction.get("proposed_fields",[]),"warnings":u.extraction.get("warnings",[]),"review_status":u.extraction.get("review_status","pending"),"mode":"local_extraction","ai_connected":False}

    @app.get("/api/contracts/{cid}/uploads/{did}/preview")
    def image(cid:str,did:str,page:int=1,s:Session=Depends(api.session),user=Depends(api.viewer)):
        c,u=uploaded(s,user,cid,did)
        if not 1<=page<=u.extraction.get("page_count",0): raise HTTPException(404,"Página no encontrada")
        path=folder_for(u.storage_key)/f"page-{page}.png"
        if not path.is_file(): raise HTTPException(404,"Vista previa no disponible")
        return FileResponse(path,media_type="image/png",headers={"Cache-Control":"no-store","X-Content-Type-Options":"nosniff","Content-Security-Policy":"default-src 'none'"})

    @app.get("/api/contracts/{cid}/uploads/{did}/original")
    def original(cid:str,did:str,s:Session=Depends(api.session),user=Depends(api.viewer)):
        c,u=uploaded(s,user,cid,did); path=original_path(u)
        if not path.is_file(): raise HTTPException(404,"Archivo no disponible")
        api.audit(s,"contratos",user,"download_real_original",c); s.commit()
        return FileResponse(path,media_type=u.content_type,filename=u.filename,content_disposition_type="attachment",headers={"Cache-Control":"no-store","X-Content-Type-Options":"nosniff","Content-Security-Policy":"sandbox; default-src 'none'"})
