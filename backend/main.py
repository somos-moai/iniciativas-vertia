"""Functional, synthetic demonstration. All integrations are deliberately mocked."""
import csv
import hashlib
import html
import io
import json
import os
import re
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone, date
from typing import Any, Literal
from uuid import uuid4
from pathlib import Path

from fastapi import FastAPI, Depends, Header, HTTPException, Query
from fastapi.responses import HTMLResponse, Response, FileResponse
from pydantic import BaseModel, Field
from sqlalchemy import select, text
from sqlalchemy.orm import Session, sessionmaker

from .db import Record, make_engine, initialize
from .seed import USERS, COUNTRIES

KINDS = ["companies","contacts","campaigns","activities","opportunities","prospects","messages","contracts","access_requests","obligations","audit","notifications"]
APPS = {"prospectador","contratos"}

def now():
    return datetime.now(timezone.utc).isoformat()

def fail(message, code=400):
    raise HTTPException(code, message)

@asynccontextmanager
async def lifespan(app):
    app.state.engine = make_engine()
    initialize(app.state.engine)
    app.state.sessions = sessionmaker(app.state.engine, expire_on_commit=False)
    yield
    app.state.engine.dispose()

app = FastAPI(title="Vertia · Demostración sintética", version="1.0.0", lifespan=lifespan)

@app.middleware("http")
async def private_demo_responses(request,call_next):
    response=await call_next(request)
    if request.url.path.startswith("/api/"):
        response.headers["Cache-Control"]="no-store"
        response.headers["Vary"]="X-Demo-User"
        response.headers["X-Content-Type-Options"]="nosniff"
    return response

def session():
    with app.state.sessions() as s:
        yield s

def viewer(x_demo_user: str | None = Header(default=None)):
    user=next((u for u in USERS if u["id"] == (x_demo_user or "regional")), None)
    if not user:
        fail("Perfil de demostración desconocido",401)
    return user

def records(s, application, kind=None):
    q=select(Record).where(Record.app==application)
    if kind:
        q=q.where(Record.kind==kind)
    return list(s.scalars(q))

def save(s, record, **changes):
    record.data={**record.data, **changes, "updated_at":now()}
    s.add(record)
    return record.data

def new(s, application, kind, **data):
    rid=f"{kind.rstrip('s')}-{uuid4().hex[:12]}"
    body={"id":rid,"created_at":now(),**data}
    r=Record(id=rid,app=application,kind=kind,data=body)
    s.add(r)
    s.flush()
    return r

def get(s, application, kind, rid):
    if not isinstance(rid,str) or not rid or len(rid)>96:
        fail("Identificador de registro inválido")
    # FOR UPDATE serializes transitions, approval/send and credit deductions.
    r=s.scalar(select(Record).where(Record.id==rid,Record.app==application,Record.kind==kind).with_for_update())
    if not r:
        fail("Registro no encontrado",404)
    return r

def granted(s, user, cid):
    for r in records(s,"contratos","access_requests"):
        d=r.data
        if d.get("contract_id")==cid and d.get("requested_by")==user["id"] and d.get("status")=="aprobada":
            if d.get("expires_at","") > now():
                return True
    return False

def allowed(s, user, r):
    d=r.data
    if user["role"]=="regional":
        return True
    if r.app=="prospectador":
        if user["role"]=="legal":
            return False
        return d.get("country")==user["country"] and (user["role"] in {"manager","viewer"} or d.get("owner_id")==user["id"])
    if r.kind=="access_requests":
        return d.get("requested_by")==user["id"] or (d.get("country")==user["country"] and user["role"] in {"manager","legal"})
    if d.get("country")==user["country"]:
        return True
    cid=d.get("contract_id") if r.kind!="contracts" else r.id
    return bool(cid and granted(s,user,cid))

def read(s,user,r):
    if not allowed(s,user,r):
        fail("Su perfil no tiene acceso a este registro",403)
    return r

def write(s,user,r,roles=None):
    read(s,user,r)
    if user["role"]=="viewer":
        fail("El perfil de consulta no puede modificar registros",403)
    if user["role"]!="regional" and r.data.get("country")!=user["country"]:
        fail("La autorización entre países permite consulta, no edición",403)
    if roles and user["role"] not in roles:
        fail("Esta acción requiere un perfil autorizado de jefatura o Legal",403)

def text_field(p,key,default=None,limit=1000):
    v=p.get(key,default)
    if not isinstance(v,str) or not v.strip() or len(v)>limit:
        fail(f"Campo {key} requerido, hasta {limit} caracteres")
    return v.strip()

def country_field(user,p):
    cc=p.get("country",user["country"])
    if not isinstance(cc,str) or cc not in {c["code"] for c in COUNTRIES}:
        fail("País inválido")
    if user["role"]!="regional" and cc!=user["country"]:
        fail("No puede crear registros de otro país",403)
    if user["role"]=="viewer":
        fail("Perfil de consulta",403)
    return cc

def amount_field(p):
    try:
        amount=float(p.get("amount",0))
    except (ValueError,TypeError):
        fail("Monto inválido")
    if not 0<=amount<=1e12:
        fail("Monto fuera de rango")
    return amount

def iso_date(value):
    try:
        return date.fromisoformat(value).isoformat()
    except (TypeError,ValueError):
        fail("Fecha inválida: usar YYYY-MM-DD")

def audit(s,application,user,action,entity=None,detail=""):
    d=entity.data if isinstance(entity,Record) else entity or {}
    new(s,application,"audit",action=action,title=action.replace("_"," ").capitalize(),entity_id=d.get("id"),country=d.get("country",user["country"]),owner_id=user["id"],actor=user["id"],actor_name=user["name"],detail=detail or "Operación sintética persistida")

def notice(s,application,user,title,**data):
    new(s,application,"notifications",title=title,country=user["country"],owner_id=user["id"],status="nueva",**data)

def fingerprint(d):
    return hashlib.sha256(json.dumps({k:d.get(k) for k in ["subject","body","contact_ids"]},sort_keys=True).encode()).hexdigest()

def integrations(application):
    names=[("PostgreSQL","conectado","Persistencia real de demostración")]
    names += [(n,"simulado","Sin conexión ni consumos externos") for n in (["Lusha","Microsoft 365","Claude","POST"] if application=="prospectador" else ["OCR","Claude","Firma electrónica"])]
    return [{"id":n.lower().replace(" ","-"),"name":n,"status":st,"description":desc,"mode":"synthetic" if st=="simulado" else "postgresql"} for n,st,desc in names]

def state(s,user,application):
    if application not in APPS:
        fail("Aplicación inválida")
    out={k:[] for k in KINDS}
    for r in records(s,application):
        if allowed(s,user,r):
            d=dict(r.data)
            if r.kind=="contracts":
                d.update({"can_access":True,"can_edit":user["role"]!="viewer" and (user["role"]=="regional" or d["country"]==user["country"]),"restricted":False})
            if r.kind=="prospects" and not d.get("revealed"):
                d["email"]=None
                d["phone"]=None
            out[r.kind].append(d)
        elif r.kind=="contracts":
            # Regional catalog exposes only synthetic, non-sensitive locator metadata.
            d=r.data
            out["contracts"].append({"id":r.id,"title":f"Documento reservado · {d['country']}","name":f"Documento reservado · {d['country']}","reference":d["reference"],"country":d["country"],"status":"restringido","confidential":True,"can_access":False,"can_edit":False,"restricted":True,"documents":[],"history":[]})
    for kind in KINDS:
        out[kind].sort(key=lambda d:d.get("created_at",""),reverse=True)
    contacts=out["contacts"]; contracts=[c for c in out["contracts"] if not c.get("restricted")]
    obligations=out["obligations"]
    overdue=sum(o.get("status")!="completada" and o.get("due_date","9999")<date.today().isoformat() for o in obligations)
    messages=out["messages"]
    sent=sum(m.get("direction")=="outbound" for m in messages)+sum(c.get("sent_count",0) for c in out["campaigns"] if re.fullmatch(r"campaign-[A-Z]{2}-[0-2]",c["id"]))
    replies=sum(c.get("status")=="respondió" for c in contacts)
    pipeline=sum(o.get("amount",0) for o in out["opportunities"] if o.get("status") not in {"perdido","ganado"})
    out["metrics"]={"companies":len(out["companies"]),"contacts":len(contacts),"total_contacts":len(contacts),"prospects":len(out["prospects"]),"campaigns":len(out["campaigns"]),"active_campaigns":sum(c.get("status")=="enviada" for c in out["campaigns"]),"sent":sent,"replies":replies,"reply_rate":round(replies/max(sent,1)*100,1),"meetings":sum(a.get("type")=="meeting" for a in out["activities"]),"pipeline":pipeline,"pipeline_value":pipeline,"excluded":sum(c.get("excluded",False) for c in contacts),"contracts":len(contracts),"total_contracts":len(contracts),"active_contracts":sum(c.get("status")=="activo" for c in contracts),"pending_approval":sum(c.get("status") in {"en_revision","pendiente_aprobacion"} for c in contracts),"pending_signature":sum(c.get("status")=="pendiente_firma" for c in contracts),"expiring_soon":sum(0<=(date.fromisoformat(c["end_date"])-date.today()).days<=90 for c in contracts if c.get("end_date")),"overdue_obligations":overdue,"obligations":len(obligations),"contract_value":sum(c.get("amount",0) for c in contracts),"access_requests":sum(r.get("status")=="pendiente" for r in out["access_requests"])}
    used=sum(bool(p.get("revealed")) for p in out["prospects"])
    credit_limit=250*max(1,len({p.get("owner_id") for p in out["prospects"]}))
    out.update({"viewer":user,"users":USERS,"countries":COUNTRIES,"integrations":integrations(application),"credits":{"used":used,"limit":credit_limit,"remaining":max(credit_limit-used,0),"provider":"Lusha simulado","scope":"250 por cartera; agregado visible"},"generated_at":now(),"mode":"synthetic","roadmap":[{"id":"mvp","name":"MVP operativo","title":"MVP operativo","status":"incluido","description":"Piloto con perfiles, aprobaciones y trazabilidad"},{"id":"regional","name":"Consolidación regional","title":"Consolidación regional","status":"incluido","description":"Configuración base de cinco países, validación local por Vertia"},{"id":"evolution","name":"Evolución especializada","title":"Evolución especializada","status":"ampliacion","description":"WhatsApp/LinkedIn y conectores adicionales" if application=="prospectador" else "ERP avanzado, portal externo, add-in Word y analítica predictiva"}]})
    return out

class Action(BaseModel):
    app: Literal["prospectador","contratos"]
    action: str = Field(max_length=64)
    entity_id: str | None = Field(default=None,max_length=96)
    payload: dict[str,Any] = Field(default_factory=dict)

@app.get("/api/health")
def health(s:Session=Depends(session)):
    s.execute(text("SELECT 1"))
    return {"status":"ok","database":"postgresql","mode":"synthetic"}

@app.get("/api/state")
def get_state(app:Literal["prospectador","contratos"],s:Session=Depends(session),user=Depends(viewer)):
    return state(s,user,app)

def crm_action(s,user,a):
    p=a.payload; action=a.action; entity=None
    def target(kind):
        r=get(s,a.app,kind,a.entity_id or p.get(f"{kind.rstrip('s')}_id"))
        write(s,user,r)
        return r
    if action=="create_company":
        cc=country_field(user,p)
        if user["role"]=="legal": fail("Perfil Legal sin gestión comercial",403)
        domain=p.get("domain","empresa.example")
        if not isinstance(domain,str) or not domain.endswith(".example"): fail("La demostración solo admite dominios .example")
        entity=new(s,a.app,"companies",name=text_field(p,"name"),domain=domain,sector=p.get("sector","Otros"),country=cc,owner_id=user["id"],status="activo")
    elif action=="create_contact":
        co=get(s,a.app,"companies",p.get("company_id")); write(s,user,co)
        cc=country_field(user,p)
        if co.data["country"]!=cc: fail("El contacto y empresa deben compartir país")
        email=text_field(p,"email").lower()
        if not re.fullmatch(r"[^\s@]+@[^\s@]+\.example",email): fail("Usar un correo sintético terminado en .example")
        s.execute(text("SELECT pg_advisory_xact_lock(hashtext(:key))"),{"key":"contact-email:"+email})
        if any(r.data["email"].lower()==email for r in records(s,a.app,"contacts")): fail("El correo ya existe",409)
        entity=new(s,a.app,"contacts",name=text_field(p,"name"),email=email,title=p.get("title","Contacto"),company_id=co.id,company_name=co.data["name"],phone=p.get("phone",""),country=cc,owner_id=user["id"],status="nuevo",excluded=False,score=65,source="Ingreso manual")
    elif action in {"update_contact","update_company"}:
        entity=target("contacts" if action=="update_contact" else "companies")
        keys=["name","title","phone"] if action=="update_contact" else ["name","sector"]
        changes={k:text_field(p,k) for k in keys if k in p}
        if not changes: fail("No hay campos editables para actualizar")
        save(s,entity,**changes)
    elif action=="import_contacts":
        rows=p.get("rows",[])
        if not isinstance(rows,list) or not 1<=len(rows)<=100: fail("Importación demo: entre 1 y 100 filas")
        imported=0; skipped=0
        for row in rows:
            if not isinstance(row,dict): fail("Cada fila debe ser un objeto")
            email=text_field(row,"email").lower()
            if any(r.data.get("email")==email for r in records(s,a.app,"contacts")):
                skipped+=1; continue
            entity=crm_action(s,user,Action(app=a.app,action="create_contact",payload=row))
            imported+=1
        entity=new(s,a.app,"activities",title="Importación de contactos",type="import",country=user["country"],owner_id=user["id"],date=now(),status="completada",imported=imported,duplicates=skipped,description=f"{imported} contactos creados; {skipped} duplicados omitidos")
    elif action=="search_prospects":
        cc=country_field(user,p)
        if user["role"]=="legal": fail("Perfil Legal sin prospección",403)
        query=text_field(p,"query",limit=200)
        for i in range(3):
            token=uuid4().hex[:6]
            entity=new(s,a.app,"prospects",name=f"Contacto {i+1} · {query}",email=f"candidato-{token}@prospectos-{cc.lower()}.example",title="Responsable de Marketing",company_name=f"{query} · Empresa ficticia {i+1}",country=cc,owner_id=user["id"],sector=p.get("sector","Retail"),score=91-i*8,status="pendiente",revealed=False,source="Lusha simulado",credit_cost=1)
    elif action=="reveal_contact":
        entity=get(s,a.app,"prospects",a.entity_id or p.get("prospect_id")); write(s,user,entity)
        if entity.data.get("revealed"): fail("El prospecto ya fue revelado; no se descuentan créditos adicionales",409)
        # Lock owner-specific PostgreSQL key to avoid simultaneous overdraw.
        s.execute(text("SELECT pg_advisory_xact_lock(hashtext(:key))"),{"key":"credits:"+entity.data["owner_id"]})
        used=sum(r.data.get("revealed",False) for r in records(s,a.app,"prospects") if r.data.get("owner_id")==entity.data["owner_id"])
        if used>=250: fail("Créditos de demostración agotados",409)
        d=entity.data
        existing=next((r for r in records(s,a.app,"contacts") if r.data.get("email")==d["email"]),None)
        if existing:
            read(s,user,existing)
            save(s,entity,revealed=True,status="revelado",contact_id=existing.id)
        else:
            co=new(s,a.app,"companies",name=d["company_name"],country=d["country"],owner_id=d["owner_id"],sector=d.get("sector","Otros"),domain=d["email"].split("@")[1],status="activo")
            contact=new(s,a.app,"contacts",**{k:d[k] for k in ["name","email","title","country","owner_id","score"]},company_id=co.id,company_name=co.data["name"],status="nuevo",excluded=False,source="Lusha simulado")
            save(s,entity,revealed=True,status="revelado",contact_id=contact.id)
    elif action=="create_campaign":
        ids=p.get("contact_ids",[])
        if not isinstance(ids,list) or not ids or len(ids)>200 or not all(isinstance(rid,str) for rid in ids): fail("Seleccione entre 1 y 200 contactos")
        contacts=[get(s,a.app,"contacts",rid) for rid in set(ids)]
        for c in contacts:
            write(s,user,c)
            if c.data.get("excluded"): fail("La campaña contiene contactos excluidos",409)
        if len({c.data["country"] for c in contacts})!=1: fail("Cada campaña debe corresponder a un país")
        entity=new(s,a.app,"campaigns",name=text_field(p,"name"),country=contacts[0].data["country"],owner_id=user["id"],contact_ids=[c.id for c in contacts],subject=text_field(p,"subject","Propuesta de visibilidad",limit=300),body=text_field(p,"body","Borrador pendiente de revisión humana",limit=20000),status="borrador",approved_by=None,sent_count=0,reply_count=0)
    elif action in {"set_campaign_content","draft_campaign","approve_campaign","send_campaign"}:
        entity=target("campaigns"); d=entity.data
        if d["status"]=="enviada": fail("La campaña ya fue enviada",409)
        if action=="set_campaign_content":
            save(s,entity,subject=text_field(p,"subject",d.get("subject"),limit=300),body=text_field(p,"body",d.get("body"),limit=20000),status="borrador",approved_by=None,approval_hash=None)
        elif action=="draft_campaign":
            save(s,entity,body=f"Estimado equipo: hemos preparado una propuesta de visibilidad para {d['country']}. Revisemos objetivos, cobertura y próximos pasos. Texto generado por adaptador Claude simulado; requiere validación humana.",subject=f"Visibilidad y oportunidades · {d['name']}",status="borrador",approved_by=None,approval_hash=None,ai_generated=True)
        elif action=="approve_campaign":
            write(s,user,entity,{"manager","regional"})
            for rid in d["contact_ids"]:
                c=get(s,a.app,"contacts",rid); read(s,user,c)
                if c.data.get("excluded"): fail("Retire contactos excluidos antes de aprobar",409)
            save(s,entity,status="aprobada",approved_by=user["id"],approved_at=now(),approval_hash=fingerprint(d))
        else:
            if d["status"]!="aprobada" or not d.get("approved_by"): fail("El envío exige aprobación humana previa",409)
            if d.get("approval_hash") and d["approval_hash"]!=fingerprint(d): fail("El contenido cambió: requiere una nueva aprobación",409)
            sent=0; skipped=0
            for rid in d["contact_ids"]:
                c=get(s,a.app,"contacts",rid); read(s,user,c)
                if c.data.get("excluded") or c.data.get("status") in {"respondió","no_contactar"}:
                    skipped+=1; continue
                if not c.data["email"].endswith(".example"): fail("Destinatario no sintético bloqueado",409)
                new(s,a.app,"messages",contact_id=c.id,campaign_id=entity.id,country=d["country"],owner_id=c.data["owner_id"],subject=d["subject"],body=d["body"],direction="outbound",status="simulado",provider="Microsoft 365 simulado",followup_status="programado")
                save(s,c,status="contactado",last_contact_at=now()); sent+=1
            save(s,entity,status="enviada",sent_count=sent,skipped_count=skipped,sent_at=now(),simulated=True)
    elif action in {"receive_reply","exclude_contact","log_meeting"}:
        entity=target("contacts"); d=entity.data
        if action=="receive_reply":
            if d.get("excluded"): fail("Contacto excluido; no se reactiva automáticamente",409)
            save(s,entity,status="respondió")
            new(s,a.app,"messages",contact_id=entity.id,country=d["country"],owner_id=d["owner_id"],subject="Respuesta sintética",body=p.get("body","Nos interesa coordinar una reunión."),direction="inbound",status="recibido_simulado")
            notice(s,a.app,user,f"Respuesta de {d['name']}",contact_id=entity.id)
        elif action=="exclude_contact":
            save(s,entity,status="no_contactar",excluded=True,exclusion_reason=p.get("reason","Solicitud de no contacto"),excluded_at=now())
        else:
            if d.get("excluded"): fail("No puede programar acciones comerciales para un contacto excluido",409)
            event_date=p.get("date",now())
            try: datetime.fromisoformat(event_date.replace("Z","+00:00"))
            except (TypeError,ValueError): fail("Fecha de reunión inválida")
            new(s,a.app,"activities",type="meeting",title=p.get("title","Reunión comercial"),date=event_date,contact_id=entity.id,country=d["country"],owner_id=d["owner_id"],status="programada",provider="Calendario simulado")
            save(s,entity,status="reunión")
        if action in {"receive_reply","exclude_contact"}:
            for m in records(s,a.app,"messages"):
                if m.data.get("contact_id")==entity.id and m.data.get("direction")=="outbound":
                    save(s,m,followup_status="cancelado",cancellation_reason="respuesta" if action=="receive_reply" else "exclusión")
    elif action=="set_opportunity":
        co=get(s,a.app,"companies",p.get("company_id")); write(s,user,co)
        status=p.get("status","propuesta")
        if status not in {"nuevo","calificada","propuesta","negociacion","ganado","perdido"}: fail("Estado de oportunidad inválido")
        if p.get("contact_id"):
            c=get(s,a.app,"contacts",p["contact_id"]); read(s,user,c)
            if c.data.get("company_id")!=co.id: fail("El contacto no pertenece a la empresa")
        data=dict(name=text_field(p,"name"),company_id=co.id,contact_id=p.get("contact_id"),country=co.data["country"],owner_id=co.data["owner_id"],amount=amount_field(p),currency=p.get("currency","USD"),status=status)
        if a.entity_id:
            entity=target("opportunities"); save(s,entity,**data)
        else: entity=new(s,a.app,"opportunities",**data)
    elif action=="sync_post":
        if user["role"] not in {"regional","manager"}: fail("La conciliación requiere jefatura",403)
        entity=new(s,a.app,"activities",type="sync",title="Conciliación POST simulada",country=user["country"],owner_id=user["id"],status="completada",date=now(),description="3 registros validados; 0 enviados. Adaptador de archivos/API sin conexión real.",processed=3,errors=0)
    else: fail("Acción comercial no soportada")
    return entity

def contract_action(s,user,a):
    p=a.payload; action=a.action
    if action=="create_contract":
        cc=country_field(user,p)
        return new(s,a.app,"contracts",title=text_field(p,"title"),name=p["title"],reference=f"VRT-{cc}-{uuid4().hex[:6].upper()}",country=cc,owner_id=user["id"],company=text_field(p,"company",f"Vertia {cc} · Ficticia"),counterparty=p.get("counterparty","Contraparte ficticia"),amount=amount_field(p),currency=p.get("currency","USD"),type=p.get("type","Comercial"),confidential=bool(p.get("confidential",True)),status="borrador",start_date=date.today().isoformat(),end_date=iso_date(p.get("end_date",(date.today()+timedelta(days=365)).isoformat())),version=1,documents=[],history=[{"status":"borrador","at":now(),"by":user["id"]}],analysis=None,redacted_ready=False,amendments=[])
    if action=="grant_access":
        entity=get(s,a.app,"access_requests",a.entity_id)
        c=get(s,a.app,"contracts",entity.data["contract_id"])
        if not (user["role"]=="regional" or (user["country"]==c.data["country"] and (user["role"] in {"manager","legal"} or user["id"]==c.data["owner_id"]))): fail("Solo el responsable del país o regional puede autorizar acceso",403)
        if entity.data["status"]!="pendiente": fail("Solicitud ya resuelta",409)
        try: days=int(p.get("days",7))
        except (TypeError,ValueError): fail("Días inválidos")
        if not 1<=days<=30: fail("Acceso temporal entre 1 y 30 días")
        save(s,entity,status="aprobada",granted_by=user["id"],expires_at=(datetime.now(timezone.utc)+timedelta(days=days)).isoformat(),days=days)
        return entity
    if action=="complete_obligation":
        entity=get(s,a.app,"obligations",a.entity_id); write(s,user,entity)
        if entity.data["status"]=="completada": fail("Obligación ya completada",409)
        save(s,entity,status="completada",evidence=text_field(p,"evidence","Validación sintética registrada"),completed_by=user["id"],completed_at=now())
        return entity
    entity=get(s,a.app,"contracts",a.entity_id)
    if action=="request_access":
        if allowed(s,user,entity): fail("Ya cuenta con acceso a este contrato",409)
        if any(r.data.get("contract_id")==entity.id and r.data.get("requested_by")==user["id"] and r.data.get("status")=="pendiente" for r in records(s,a.app,"access_requests")): fail("Ya existe una solicitud pendiente",409)
        return new(s,a.app,"access_requests",contract_id=entity.id,title="Solicitud de acceso entre países",country=entity.data["country"],owner_id=user["id"],requested_by=user["id"],requester_name=user["name"],reason=text_field(p,"reason","Consulta de antecedente regional"),status="pendiente")
    write(s,user,entity)
    d=entity.data
    transition={"submit_review":({"borrador","rechazado"},"en_revision",None),"approve_contract":({"en_revision","pendiente_aprobacion"},"aprobado",{"regional","manager","legal"}),"reject_contract":({"en_revision","pendiente_aprobacion"},"rechazado",{"regional","manager","legal"}),"send_signature":({"aprobado"},"pendiente_firma",{"regional","manager","legal"}),"sign_contract":({"pendiente_firma"},"firmado",{"regional","manager","legal"}),"activate_contract":({"firmado"},"activo",{"regional","manager","legal"})}
    if action in transition:
        previous,following,roles=transition[action]
        if roles: write(s,user,entity,roles)
        if d["status"] not in previous: fail(f"Transición inválida desde {d['status']}",409)
        if action=="submit_review" and not d.get("documents"): fail("Adjunte un documento antes de enviar a revisión",409)
        changes={"status":following,"history":d.get("history",[])+[{"status":following,"at":now(),"by":user["id"],"note":p.get("reason","Transición del flujo demo")} ]}
        if action in {"send_signature","sign_contract"}: changes["signature"]={"provider":"Firma electrónica simulada","legal_signature":False,"status":"firmado_simulado" if action=="sign_contract" else "enviado_simulado","at":now(),"by":user["id"]}
        save(s,entity,**changes)
    elif action=="upload_document":
        filename=text_field(p,"filename",limit=200)
        if "/" in filename or "\\" in filename: fail("Nombre de archivo inválido")
        if d["status"] not in {"borrador","rechazado","en_renovacion"}: fail("Los documentos solo se modifican en borrador, rechazo o renovación",409)
        ver=d.get("version",0)+1
        save(s,entity,version=ver,documents=d.get("documents",[])+[{"id":f"doc-{uuid4().hex[:8]}","filename":filename,"kind":p.get("kind","contrato"),"version":ver,"created_at":now(),"synthetic":True}],analysis=None,redacted_ready=False)
    elif action=="analyze_contract":
        if not d.get("documents"): fail("Primero adjunte un documento sintético",409)
        save(s,entity,analysis={"provider":"Claude + OCR simulados","simulated":True,"summary":f"{d['type']} entre {d['company']} y {d.get('counterparty','Contraparte ficticia')}. Revisión humana requerida.","risk":"medio","risk_level":"medio","score":67,"extracted_fields":{"amount":d["amount"],"currency":d["currency"],"end_date":d["end_date"],"country":d["country"]},"findings":[{"title":"Renovación y aviso previo","severity":"media","evidence":"Cláusula sintética 4: aviso con 60 días de anticipación.","page":2,"recommendation":"Confirmar plazo con responsable local"},{"title":"Confidencialidad","severity":"alta","evidence":"Cláusula sintética 7: anexo con información reservada.","page":3,"recommendation":"Usar copia saneada para compartir entre países"}],"analyzed_at":now(),"source_version":d["version"],"requires_human_review":True})
    elif action=="redact_document":
        write(s,user,entity,{"regional","manager","legal"})
        if not d.get("documents"): fail("Primero adjunte un documento",409)
        # Safe rendition is constructed from an allowlist; original fields never embedded.
        save(s,entity,redacted_ready=True,redaction={"reviewed_by":user["id"],"reviewed_at":now(),"source_version":d["version"],"method":"copia reconstruida con lista permitida","removed_fields":["monto","contraparte","cuenta bancaria","identificador fiscal","condición comercial"]})
    elif action=="add_obligation":
        new(s,a.app,"obligations",contract_id=entity.id,title=text_field(p,"title"),due_date=iso_date(p.get("due_date")),country=d["country"],owner_id=d["owner_id"],owner=p.get("owner",user["name"]),status="pendiente")
    elif action=="add_amendment":
        if d["status"] not in {"activo","firmado","en_renovacion"}: fail("Las enmiendas requieren contrato firmado o activo",409)
        changes={"amendments":d.get("amendments",[])+[{"id":uuid4().hex[:10],"title":text_field(p,"title"),"description":p.get("description",""),"at":now(),"by":user["id"],"status":"registrada_demo"}]}
        if p.get("new_end_date"): changes["end_date"]=iso_date(p["new_end_date"])
        save(s,entity,**changes)
    elif action=="renew_contract":
        if d["status"] not in {"activo","vencido","en_renovacion"}: fail("Solo contratos activos o vencidos se pueden renovar",409)
        end=iso_date(p.get("end_date",(date.fromisoformat(d["end_date"])+timedelta(days=365)).isoformat()))
        if end<=d["end_date"]: fail("La renovación debe extender el vencimiento")
        save(s,entity,end_date=end,status="en_renovacion",history=d.get("history",[])+[{"status":"en_renovacion","at":now(),"by":user["id"],"note":"Renovación propuesta; requiere nueva revisión"}])
    else: fail("Acción contractual no soportada")
    return entity

@app.post("/api/actions")
def actions(a:Action,s:Session=Depends(session),user=Depends(viewer)):
    try:
        entity=crm_action(s,user,a) if a.app=="prospectador" else contract_action(s,user,a)
        audit(s,a.app,user,a.action,entity)
        s.commit()
        return {"ok":True,"message":"Operación registrada en la demostración.","entity":entity.data if entity else None}
    except Exception:
        s.rollback()
        raise

@app.get("/api/export")
def export(app:Literal["prospectador","contratos"],s:Session=Depends(session),user=Depends(viewer)):
    kind="contacts" if app=="prospectador" else "contracts"
    rows=[r.data for r in records(s,app,kind) if allowed(s,user,r)]
    fields=["id","name","email","company_name","country","status","owner_id"] if kind=="contacts" else ["id","reference","title","company","country","type","status","amount","currency","end_date"]
    buf=io.StringIO(); buf.write("\ufeff"); writer=csv.DictWriter(buf,fieldnames=fields,extrasaction="ignore"); writer.writeheader()
    # Spreadsheet formula injection is neutralized even for user-created fields.
    for row in rows:
        writer.writerow({k:("'"+v if isinstance(v,str) and v.startswith(("=","+","-","@","\t","\r")) else v) for k,v in row.items() if k in fields})
    return Response(buf.getvalue(),media_type="text/csv; charset=utf-8",headers={"Content-Disposition":f'attachment; filename="{app}-demo.csv"',"Cache-Control":"no-store"})

@app.get("/api/contracts/{cid}/document",response_class=HTMLResponse)
def document(cid:str,redacted:bool=True,s:Session=Depends(session),user=Depends(viewer)):
    r=get(s,"contratos","contracts",cid); read(s,user,r); d=r.data
    if redacted:
        if not d.get("redacted_ready"): fail("Genere y revise primero la copia saneada",409)
        parts=["COPIA SANEADA · DOCUMENTO SINTÉTICO",f"Referencia: {d['reference']}",f"País: {d['country']}",f"Tipo: {d['type']}","Objeto: colaboración comercial y antecedentes de experiencia.","Las condiciones comerciales e identificadores personales fueron retirados.","Uso demostrativo. Revisión humana registrada. No constituye un documento legal."]
    else:
        parts=["ORIGINAL SINTÉTICO · DEMOSTRACIÓN",d["title"],f"Referencia: {d['reference']}",f"Partes: {d['company']} y {d.get('counterparty','Contraparte ficticia')}",f"Monto confidencial: {d['amount']} {d['currency']}","Cuenta bancaria: DEMO-IBAN-99887766", "Identificador fiscal: DEMO-TAX-11223344","Condición comercial reservada: descuento privado del 17%",f"Vencimiento: {d['end_date']}","Cláusula 4: aviso previo con 60 días de anticipación.","Cláusula 7: confidencialidad de anexos y precios.","No corresponde a un documento real ni a una firma legal."]
    rendered='<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Documento sintético</title><body><main>'+''.join(f"<p>{html.escape(str(p))}</p>" for p in parts)+"</main></body></html>"
    audit(s,"contratos",user,"download_redacted" if redacted else "download_original",r)
    s.commit()
    return HTMLResponse(rendered,headers={"Cache-Control":"no-store","X-Content-Type-Options":"nosniff","Content-Security-Policy":"default-src 'none'; style-src 'none'; frame-ancestors 'self'","Content-Disposition":f'inline; filename="{cid}-{"saneado" if redacted else "original"}.html"'})

@app.get("/propuestas/{filename}",include_in_schema=False)
def proposal_file(filename:str):
    directory=os.environ.get("PROPOSALS_DIR")
    if not directory or Path(filename).suffix.lower() not in {".pdf",".docx",".html"}:
        fail("Documento no publicado",404)
    root=Path(directory).resolve()
    target=(root/filename).resolve()
    if not target.is_relative_to(root) or not target.is_file():
        fail("Documento no publicado",404)
    return FileResponse(target,headers={"Cache-Control":"no-cache","X-Content-Type-Options":"nosniff"})

@app.get("/{path:path}",include_in_schema=False)
def frontend_file(path:str):
    if path=="api" or path.startswith("api/"):
        fail("Endpoint API no encontrado",404)
    root=Path(os.environ.get("FRONTEND_DIST",Path(__file__).resolve().parents[1]/"frontend"/"dist")).resolve()
    target=(root/path).resolve()
    if not target.is_relative_to(root):
        fail("Ruta no permitida",404)
    if target.is_file():
        return FileResponse(target,media_type="image/webp" if target.suffix.lower()==".webp" else None,headers={"X-Content-Type-Options":"nosniff"})
    if path and not (path in {"prospectador","contratos"} or path.startswith(("prospectador/","contratos/"))):
        fail("Recurso no encontrado",404)
    index=root/"index.html"
    if not index.is_file():
        fail("Frontend pendiente de compilación",503)
    return FileResponse(index,headers={"Cache-Control":"no-cache","X-Content-Type-Options":"nosniff"})
