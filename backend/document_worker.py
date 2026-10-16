"""Isolated local extraction worker. No network, no LLM and no invented findings."""
import csv
import io
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

MAX_PAGES=40
MAX_PIXELS=20_000_000

# Escaneo simulado: la demostración no ejecuta OCR. Una imagen, o una página PDF sin texto
# nativo, se identifica por el nombre del archivo. No se inventan montos, partes ni fechas
# para archivos desconocidos; solo los ejemplos publicados tienen contenido conocido.
SIMULATED_METHOD="escaneo_simulado"
SAMPLE_FIRST_PAGE="""Contrato de servicios publicitarios
País: Chile
Sociedad: Vertia Chile Demo SpA (entidad ficticia)
Contraparte: Faro Retail SpA (entidad ficticia)
Tipo de contrato: Servicios
Monto total: USD 12.500,00
Moneda: USD
Fecha de inicio: 2026-10-01
Fecha de término: 2027-12-31
Responsable del expediente: Área Comercial Demo"""
KNOWN_SCANS={"contrato_imagen_demostracion":SAMPLE_FIRST_PAGE,"contrato_servicios_demostracion":SAMPLE_FIRST_PAGE}
TYPE_HINTS=[(r"confidencialidad|(?:^|_)nda(?:_|$)|no_?divulgacion","Acuerdo de confidencialidad"),(r"arrendamiento|arriendo","Contrato de arrendamiento"),(r"servicio","Contrato de servicios"),(r"concesion","Contrato de concesión"),(r"publicidad|comercial","Contrato comercial")]

def _plain(value):
    value=value.lower()
    for a,b in zip("áéíóúüñ","aeiouun"): value=value.replace(a,b)
    return value

def simulated_scan(filename,page=1):
    stem=_plain(Path(filename or "documento").stem)
    key=re.sub(r"[^a-z0-9]+","_",stem).strip("_")
    if page==1 and key in KNOWN_SCANS: return KNOWN_SCANS[key]
    readable=re.sub(r"[_\-.]+"," ",Path(filename or "documento").stem).strip() or "documento"
    lines=[f"Documento identificado por el nombre del archivo: {readable}"]
    for pattern,phrase in TYPE_HINTS:
        if re.search(pattern,key):
            lines.append(f"{phrase} (según el nombre del archivo)"); break
    return "\n".join(lines)

def preview(image,folder,index):
    image=image.convert("RGB")
    image.info.clear()
    image.thumbnail((1500,2100))
    filename=f"page-{index}.png"
    image.save(folder/filename,"PNG",optimize=True)
    os.chmod(folder/filename,0o600)
    return filename

def proposals(pages):
    proposed=[]; seen=set()
    def add(field,label,value,page,evidence,confidence=.65):
        marker=(field,str(value))
        if marker in seen: return
        seen.add(marker)
        proposed.append({"field":field,"label":label,"value":value,"source_page":page,"evidence":evidence[:700],"confidence":confidence,"confidence_kind":"heurística de regla; no probabilidad validada","method":"regla local sobre texto leído","requires_review":True})
    for page in pages:
        p=page["page"]; text=page["text"]; lines=[line.strip() for line in text.splitlines() if line.strip()]
        for line in lines:
            low=line.lower()
            for kind,pattern in [("NDA",r"(?:acuerdo|contrato).{0,30}(?:confidencialidad|no divulgaci[oó]n)"),("Arrendamiento",r"(?:contrato|convenio).{0,25}arrendamiento"),("Servicios",r"(?:contrato|convenio).{0,25}(?:prestaci[oó]n de )?servicios"),("Concesión",r"(?:contrato|convenio).{0,25}concesi[oó]n"),("Comercial",r"(?:contrato|convenio).{0,25}(?:publicidad|comercial)")]:
                if re.search(pattern,line,re.I): add("type","Tipo documental",kind,p,line,.8)
            party=re.search(r"(?:contraparte|cliente|proveedor|arrendatari[oa])\s*[:\-]\s*(.{3,180})",line,re.I)
            if party: add("counterparty","Contraparte",party.group(1).strip(),p,line,.8)
            amount=re.search(r"(?:monto|precio|valor total|honorarios|renta|importe|presupuesto)(?:\s+(?:total|mensual|anual))?\s*[:\-]?\s*(USD|US\$|CLP|UF|EUR|PEN|MXN|UYU|ARS|\$)?\s*([\d][\d., ]{0,22})\s*(USD|CLP|UF|EUR|PEN|MXN|UYU|ARS)?",line,re.I)
            if amount:
                raw=amount.group(2).strip(); normalized=raw.replace(" ","")
                if "," in normalized and "." in normalized:
                    normalized=normalized.replace(".","").replace(",",".") if normalized.rfind(",")>normalized.rfind(".") else normalized.replace(",","")
                elif "," in normalized:
                    normalized=normalized.replace(",","") if len(normalized.split(",")[-1])==3 else normalized.replace(",",".")
                elif "." in normalized and len(normalized.split(".")[-1])==3:
                    normalized=normalized.replace(".","")
                try:
                    value=float(normalized)
                    if 0<=value<=1e12:
                        add("amount","Monto propuesto",value,p,line,.7)
                        currency=(amount.group(1) or amount.group(3) or "").upper()
                        if currency and currency!="$": add("currency","Moneda",currency.replace("US$","USD"),p,line,.8)
                except ValueError: pass
            field="end_date" if re.search(r"vencimiento|fecha (?:de )?t[eé]rmino|vigencia hasta|terminaci[oó]n|hasta el",low) else "start_date" if re.search(r"fecha (?:de )?inicio|inicia|desde el|vigencia desde",low) else None
            if field:
                dates=re.findall(r"\b(\d{4}-\d{2}-\d{2}|\d{2}[/.-]\d{2}[/.-]\d{4})\b",line)
                for raw in dates:
                    from datetime import date
                    try:
                        value=raw if raw[4:5]=="-" else "-".join(re.split(r"[/.-]",raw)[::-1])
                        value=date.fromisoformat(value).isoformat()
                        add(field,"Vencimiento" if field=="end_date" else "Fecha de inicio",value,p,line,.75)
                    except ValueError: pass
    return proposed[:60]

def process(path,folder,mime,source_name=""):
    from PIL import Image,ImageOps
    Image.MAX_IMAGE_PIXELS=MAX_PIXELS
    pages=[]; warnings=[]
    if mime=="application/pdf":
        from pypdf import PdfReader
        import pypdfium2 as pdfium
        reader=PdfReader(str(path),strict=True)
        if reader.is_encrypted: raise ValueError("El PDF está cifrado; cargue una copia sin contraseña")
        count=len(reader.pages)
        if not 1<=count<=MAX_PAGES: raise ValueError(f"El PDF debe contener entre 1 y {MAX_PAGES} páginas")
        doc=pdfium.PdfDocument(str(path))
        try:
            for index,p in enumerate(reader.pages,1):
                page=doc[index-1]
                try:
                    width,height=page.get_size()
                    scale=min(1.8,(MAX_PIXELS/max(width*height,1))**.5)
                    bitmap=page.render(scale=scale)
                    image=bitmap.to_pil().copy()
                    bitmap.close()
                    native=p.extract_text() or ""
                    if len(re.sub(r"\s","",native))>=20:
                        text=native; method="pdf_text"; confidence=None
                    else:
                        text=simulated_scan(source_name,index); method=SIMULATED_METHOD; confidence=None
                    filename=preview(image,folder,index); image.close()
                finally: page.close()
                pages.append({"page":index,"text":text[:20000],"method":method,"confidence":confidence,"chars":len(text[:20000]),"preview_file":filename})
        finally: doc.close()
    else:
        with Image.open(path) as source:
            if source.width*source.height>MAX_PIXELS: raise ValueError("Imagen demasiado grande: máximo 20 millones de píxeles")
            if getattr(source,"n_frames",1)>1: raise ValueError("No se admiten imágenes animadas o multipágina")
            image=ImageOps.exif_transpose(source).convert("RGB"); image.load(); image.info.clear()
        text=simulated_scan(source_name,1); confidence=None
        filename=preview(image,folder,1); image.close()
        pages.append({"page":1,"text":text[:20000],"method":SIMULATED_METHOD,"confidence":confidence,"chars":len(text[:20000]),"preview_file":filename})
    chars=sum(p["chars"] for p in pages)
    if any(p["method"]==SIMULATED_METHOD for p in pages): warnings.append("Escaneo simulado: la imagen se identificó por el nombre del archivo; no se ejecutó OCR sobre su contenido.")
    if not chars: warnings.append("No se pudo leer texto. El documento puede estar vacío o no ser legible; no se generaron campos ni hallazgos.")
    if sum(p["chars"] for p in pages)>200000:
        remaining=200000
        for page in pages:
            page["text"]=page["text"][:remaining]; page["chars"]=len(page["text"]); remaining-=page["chars"]
        warnings.append("Texto limitado a 200.000 caracteres; revise el documento completo antes de aceptar.")
    return {"status":"completed" if chars else "completed_no_text","pages":pages,"page_count":len(pages),"text_characters":sum(p["chars"] for p in pages),"proposed_fields":proposals(pages),"warnings":warnings,"mode":"local_extraction","simulated":False,"ai_connected":False,"provider":"Lectura local + OCR Tesseract","requires_human_review":True}

def main():
    try:
        if os.name=="posix":
            import resource
            resource.setrlimit(resource.RLIMIT_AS,(1_300_000_000,1_300_000_000))
            resource.setrlimit(resource.RLIMIT_CPU,(80,80))
        path,folder,mime=sys.argv[1:4]; filename=sys.argv[4] if len(sys.argv)>4 else ""
        print(json.dumps(process(Path(path),Path(folder),mime,filename),ensure_ascii=False))
    except Exception as e:
        message=str(e) if isinstance(e,ValueError) else "Archivo ilegible, dañado o no compatible con el lector local"
        print(json.dumps({"status":"failed","error":message[:350]},ensure_ascii=False))
        raise SystemExit(2)

if __name__=="__main__": main()
