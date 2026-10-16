"""Persistent, explicitly simulated Lusha and Microsoft 365 workflows."""
import hashlib
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from sqlalchemy import text
from fastapi import HTTPException
from .permissions import capabilities

WALLET_LIMIT=1250
ORG_LIMIT=7500
RUN_LIMIT=600
RATE_LIMITS={"minute":50,"hour":150,"day":1500}
MAIL_POLICY={"provider":"Microsoft 365 simulado","seconds_between":8,"pause_every":15,"pause_seconds":45,"window_start":"08:00","window_end":"20:00","cooldown_days":7,"poll_minutes":10,"timezone":"America/Montevideo","external_delivery":False}
TIMEZONES={"UY":"America/Montevideo","CL":"America/Santiago","PE":"America/Lima","AR":"America/Argentina/Buenos_Aires","MX":"America/Mexico_City"}
COMMERCIAL_ACTIONS={"search_prospects","reveal_contact","preview_reveal","reveal_contacts","draft_email","send_email","save_sequence","simulate_sequence","sync_inbox","poll_inbox","save_ai_settings","configure_credits","send_campaign"}

def utcnow(): return datetime.now(timezone.utc)
def parsed(value):
    if not value: return None
    try:
        dt=datetime.fromisoformat(str(value).replace("Z","+00:00"))
        return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt
    except (ValueError,TypeError): return None

def identity(data):
    return str(data.get("email","")).strip().casefold()

def lock(s,key):
    s.execute(text("SELECT pg_advisory_xact_lock(hashtext(:key))"),{"key":key})

def rate_check(s,user,operation,simulate=False):
    from . import main as api
    lock(s,"v3-lusha-rate-organization")
    current=utcnow()
    events=api.records(s,"prospectador","provider_queries")
    if simulate:
        raise HTTPException(429,{"message":"Lusha simulado: límite temporal. Reintente al concluir la espera.","retry_after":60,"retry_at":(current+timedelta(seconds=60)).isoformat(),"provider":"Lusha simulado"},headers={"Retry-After":"60"})
    for name,seconds in [("minute",60),("hour",3600),("day",86400)]:
        times=[parsed(r.data.get("created_at")) for r in events]
        recent=[dt for dt in times if dt and (current-dt).total_seconds()<seconds]
        if len(recent)>=RATE_LIMITS[name]:
            retry=max(1,int(seconds-(current-min(recent)).total_seconds())+1)
            raise HTTPException(429,{"message":f"Lusha simulado: tope de {RATE_LIMITS[name]} consultas por {name}","retry_after":retry,"retry_at":(current+timedelta(seconds=retry)).isoformat(),"provider":"Lusha simulado"},headers={"Retry-After":str(retry)})
    api.new(s,"prospectador","provider_queries",country=user["country"],owner_id=user["id"],operation=operation,provider="Lusha simulado",cost=0)

def credit_state(s,user,visible_prospects,source_rows=None):
    from . import main as api
    def source(kind): return [r for r in source_rows if r.kind==kind] if source_rows is not None else api.records(s,"prospectador",kind)
    rows=[r.data for r in source("credit_ledger")]
    # Legacy revealed records remain counted exactly once after migration.
    ledger_ids={pid for r in rows for pid in r.get("prospect_ids",[])}
    legacy=[r.data for r in source("prospects") if r.data.get("revealed") and r.id not in ledger_ids]
    wallets=[]
    owners={r.data.get("owner_id") for r in source("prospects")}|{user["id"]}
    settings=sorted([r.data for r in source("credit_settings")],key=lambda d:d.get("created_at",""))
    plan=settings[-1] if settings else {}
    for owner in sorted(owners):
        used=sum(r.get("cost",0) for r in rows if r.get("portfolio_id")==owner)+sum(1 for r in legacy if r.get("owner_id")==owner)
        limit=plan.get("wallet_limits",{}).get(owner,WALLET_LIMIT)
        u=next((u for u in api.USERS if u["id"]==owner),{})
        wallets.append({"owner_id":owner,"name":u.get("name",owner),"country":u.get("country"),"used":used,"limit":limit,"remaining":max(0,limit-used)})
    organization_used=sum(w["used"] for w in wallets); org_limit=plan.get("organization_limit",ORG_LIMIT)
    visible_owner_ids={p.get("owner_id") for p in visible_prospects}|{user["id"]}
    visible_wallets=[w for w in wallets if w["owner_id"] in visible_owner_ids]
    wallet=next(w for w in wallets if w["owner_id"]==user["id"])
    # Jefaturas see the team's subtotal, while an executive sees their own wallet.
    selected=visible_wallets if user["role"] in {"manager","regional","superadmin","ia_lead"} else [wallet]
    used=sum(w["used"] for w in selected); limit=sum(w["limit"] for w in selected)
    visible_history=[r for r in rows if r.get("portfolio_id") in visible_owner_ids or r.get("owner_id")==user["id"]]
    runs=defaultdict(lambda:{"used":0,"queries":0})
    for r in visible_history:
        rid=r.get("run_id","legacy"); runs[rid]["used"]+=r.get("cost",0); runs[rid]["queries"]+=1
    return {"used":used,"limit":limit,"remaining":max(0,limit-used),"wallet":wallet,"organization":{"used":organization_used,"limit":org_limit,"remaining":max(0,org_limit-organization_used)},"portfolios":visible_wallets,"history":sorted(visible_history,key=lambda x:x["created_at"],reverse=True),"runs":[{"id":rid,"run_id":rid,"limit":RUN_LIMIT,**v} for rid,v in runs.items()],"run_limit":RUN_LIMIT,"rate_limits":RATE_LIMITS,"provider":"Lusha simulado","scope":"Carteras visibles; saldo organizacional independiente","deduplication":"Identidad normalizada de contacto; sin cobro repetido"}

def ids_from(a):
    from . import main as api
    ids=a.payload.get("prospect_ids",a.payload.get("ids"))
    if ids is None: ids=[a.entity_id or a.payload.get("prospect_id")]
    if not isinstance(ids,list) or not 1<=len(ids)<=600 or not all(isinstance(v,str) and v for v in ids): api.fail("Seleccione entre 1 y 600 prospectos")
    return list(dict.fromkeys(ids))

def reveal_preview(s,user,a):
    from . import main as api
    ids=ids_from(a); targets=[api.get(s,a.app,"prospects",rid) for rid in ids]
    for r in targets: api.write(s,user,r)
    run_id=str(a.payload.get("run_id") or f"run-{user['id']}-{utcnow().date().isoformat()}")
    if not 1<=len(run_id)<=96: api.fail("Corrida inválida")
    ledger=[r.data for r in api.records(s,a.app,"credit_ledger")]
    known={identity(r.data) for r in api.records(s,a.app,"contacts")}
    known|={r.get("identity") for r in ledger}
    known|={identity(r.data) for r in api.records(s,a.app,"prospects") if r.data.get("revealed")}
    payable=[]; duplicates=[]; seen=set(known)
    for r in targets:
        key=identity(r.data)
        if key in seen: duplicates.append(r.id)
        else: payable.append(r); seen.add(key)
    cost=len(payable)
    run_used=sum(r.get("cost",0) for r in ledger if r.get("run_id")==run_id)
    snapshot=credit_state(s,user,[r.data for r in targets])
    costs=defaultdict(int)
    for r in payable: costs[r.data["owner_id"]]+=1
    wallets={w["owner_id"]:w for w in snapshot["portfolios"]}
    if cost+run_used>RUN_LIMIT: api.fail("Tope de 600 créditos por corrida; divida o reduzca la selección",409)
    if cost>snapshot["organization"]["remaining"]: api.fail("Saldo de la organización insuficiente",409)
    if any(value>wallets[owner]["remaining"] for owner,value in costs.items()): api.fail("Saldo de cartera insuficiente",409)
    return {"id":"reveal-preview","ids":ids,"prospect_ids":ids,"cost":cost,"duplicates":len(duplicates),"duplicate_ids":duplicates,"balance_after":snapshot["organization"]["remaining"]-cost,"run_id":run_id,"run_used":run_used,"run_limit":RUN_LIMIT,"provider":"Lusha simulado","requires_confirmation":True,"allowed":True,"remaining":sum(w["remaining"] for w in snapshot["portfolios"])},targets,payable

def reveal(s,user,a):
    from . import main as api
    lock(s,"v3-credits-organization")
    preview,targets,payable=reveal_preview(s,user,a)
    if a.action=="preview_reveal":
        return api.Record(id="reveal-preview",app=a.app,kind="preview",data=preview)
    if a.action=="reveal_contact" and targets[0].data.get("revealed"): api.fail("El prospecto ya fue revelado; no se descuentan créditos adicionales",409)
    rate_check(s,user,"reveal",a.payload.get("simulate_429",False))
    paid_ids={r.id for r in payable}
    for r in targets:
        d=r.data
        # Deduplication never returns another portfolio's contact id or fields.
        same=next((c for c in api.records(s,a.app,"contacts") if identity(c.data)==identity(d) and c.data.get("owner_id")==d["owner_id"]),None)
        if not same:
            if d.get("company_id"):
                co=api.get(s,a.app,"companies",d["company_id"]); api.write(s,user,co)
            else:
                co=api.new(s,a.app,"companies",name=d["company_name"],country=d["country"],owner_id=d["owner_id"],sector=d.get("sector","Otros"),domain=d["email"].split("@")[1],status="activo")
            same=api.new(s,a.app,"contacts",name=d["name"],email=d["email"],phone=d.get("phone",""),title=d["title"],score=d.get("score"),company_id=co.id,company_name=co.data["name"],country=d["country"],owner_id=d["owner_id"],status="nuevo",excluded=False,email_valid=True,source="Lusha simulado")
        cost=1 if r.id in paid_ids else 0
        if not d.get("revealed"):
            api.new(s,a.app,"credit_ledger",country=d["country"],owner_id=user["id"],portfolio_id=d["owner_id"],actor_name=user["name"],run_id=preview["run_id"],prospect_ids=[r.id],identity=identity(d),cost=cost,reason="Revelación" if cost else "Reutilización sin cargo",provider="Lusha simulado")
        api.save(s,r,revealed=True,status="revelado",contact_id=same.id,revealed_at=api.now(),credit_cost_paid=cost,run_id=preview["run_id"])
    if a.action=="reveal_contact": return targets[0]
    return api.Record(id="reveal-result",app=a.app,kind="result",data={**preview,"id":"reveal-result","revealed_count":len(targets),"requires_confirmation":False})

def useful(data):
    value=data.get("title","").casefold()
    return any(term in value for term in ["marketing","marca","general"])

def search(s,user,a):
    from . import main as api
    p=a.payload; cc=api.country_field(user,p)
    rate_check(s,user,"search",p.get("simulate_429",False))
    company=None
    if p.get("company_id"):
        company=api.get(s,a.app,"companies",p["company_id"]);api.write(s,user,company)
        if company.data["country"]!=cc: api.fail("La empresa y búsqueda deben compartir país")
    filters={k:str(p.get(k,"")).strip().casefold() for k in ["title","seniority","department","company","domain","sector","size"]}
    candidates=[r for r in api.records(s,a.app,"prospects") if api.allowed(s,user,r) and r.data.get("country")==cc and useful(r.data)]
    if company: candidates=[r for r in candidates if r.data.get("company_id")==company.id]
    aliases={"company":"company_name","domain":"domain"}
    for key,value in filters.items():
        if value: candidates=[r for r in candidates if value in str(r.data.get(aliases.get(key,key),"")).casefold()]
    # Una empresa nueva o manual también tiene responsables: se generan de forma determinística
    # (Lusha simulado). Empresa, dominio y sector describen a la propia empresa y no impiden generarlos;
    # los filtros de cargo, seniority y departamento se aplican después.
    if not candidates and company:
        from .seed_v3 import FIRST, LAST, phone, slug
        k=int(hashlib.sha256(company.id.encode()).hexdigest()[:8],16)
        generated=[]
        for j,(title,department) in enumerate([("Gerente de Marketing","Marketing"),("Gerente de Marca","Marketing"),("Gerente General","Dirección")]):
            token=hashlib.sha256(f"{company.id}:{j}".encode()).hexdigest()[:12]
            rid=f"prospect-search-{token}"
            first,last=FIRST[(k+j*5)%len(FIRST)],LAST[(k//7+j*3)%len(LAST)]
            existing=next((r for r in api.records(s,a.app,"prospects") if r.id==rid),None)
            generated.append(existing or api.new(s,a.app,"prospects",id=rid,name=f"{first} {last}",email=f"{slug(first)}.{slug(last)}@{company.data['domain']}",phone=phone(cc,k,j),title=title,seniority="gerencia",department=department,company_id=company.id,company_name=company.data["name"],domain=company.data["domain"],country=cc,owner_id=company.data["owner_id"],sector=company.data.get("sector","Otros"),score=None,status="pendiente",revealed=False,source="Lusha simulado",credit_cost=1))
        for key in ["title","seniority","department"]:
            if filters[key]: generated=[r for r in generated if filters[key] in str(r.data.get(key,"")).casefold()]
        candidates=generated
    query=str(p.get("query","")).strip().casefold()
    if query and not company:
        matched=[r for r in candidates if query in " ".join(str(r.data.get(k,"")) for k in ["name","title","company_name","sector"]).casefold()]
        candidates=matched
    candidates.sort(key=lambda r:(r.data.get("country")!="UY",r.data.get("company_name",""),r.id))
    try: limit=min(100,max(1,int(p.get("limit",50))))
    except (ValueError,TypeError): api.fail("Límite de búsqueda inválido")
    selected=candidates[:limit]
    search_row=api.new(s,a.app,"search_runs",country=cc,owner_id=user["id"],filters=p,result_ids=[r.id for r in selected],result_count=len(candidates),provider="Lusha simulado")
    for r in selected: api.save(s,r,last_search_id=search_row.id)
    if selected: return selected[-1]
    return search_row

def next_window(dt,country):
    local=dt.astimezone(ZoneInfo(TIMEZONES.get(country,"America/Montevideo")))
    if local.hour<8: local=local.replace(hour=8,minute=0,second=0,microsecond=0)
    elif local.hour>=20: local=(local+timedelta(days=1)).replace(hour=8,minute=0,second=0,microsecond=0)
    return local.astimezone(timezone.utc)

def scheduled_time(s,contact,earliest=None):
    from . import main as api
    current=utcnow(); earliest=max(current,earliest or current)
    last=parsed(contact.data.get("last_contact_at"))
    if last: earliest=max(earliest,last+timedelta(days=7))
    rows=[r.data for r in api.records(s,"prospectador","messages") if r.data.get("direction")=="outbound" and r.data.get("owner_id")==contact.data["owner_id"] and r.data.get("status")!="cancelado"]
    personal=[parsed(m.get("scheduled_at") or m.get("sent_at") or m.get("created_at")) for m in rows if m.get("contact_id")==contact.id]
    if personal: earliest=max(earliest,max(dt for dt in personal if dt)+timedelta(days=7))
    recent=[m for m in rows if parsed(m.get("scheduled_at") or m.get("sent_at")) and parsed(m.get("scheduled_at") or m.get("sent_at"))>=current-timedelta(hours=12)]
    if recent:
        last_slot=max(parsed(m.get("scheduled_at") or m.get("sent_at")) for m in recent)
        earliest=max(earliest,last_slot+timedelta(seconds=8+(45 if len(recent)%15==0 else 0)))
    return next_window(earliest,contact.data["country"])

def queue_email(s,user,contact,subject,body,campaign_id=None,earliest=None,sequence_id=None):
    from . import main as api
    d=contact.data
    if d.get("excluded") or d.get("status") in {"no_contactar","respondió"} or d.get("email_valid") is False: api.fail("Contacto excluido, respondió o tiene correo inválido",409)
    if not identity(d).endswith(".example"): api.fail("Destinatario no sintético bloqueado",409)
    lock(s,"mail-queue:"+d["owner_id"])
    scheduled=scheduled_time(s,contact,earliest)
    due=scheduled<=utcnow()+timedelta(seconds=1)
    row=api.new(s,"prospectador","messages",contact_id=contact.id,thread_id=f"thread-{contact.id}",campaign_id=campaign_id,sequence_id=sequence_id,country=d["country"],owner_id=d["owner_id"],subject=subject,body=body,direction="outbound",status="enviado_simulado" if due else "programado",provider="Microsoft 365 simulado",external_delivery=False,scheduled_at=scheduled.isoformat(),sent_at=api.now() if due else None,followup_status="programado",queue_reason="Horario, ritmo de envío y espera mínima de 7 días verificados",sector=d.get("sector"))
    if due: api.save(s,contact,status="contactado",last_contact_at=api.now())
    api.new(s,"prospectador","activities",contact_id=contact.id,type="email" if due else "email_queued",title="Correo enviado en simulador" if due else "Correo programado en simulador",date=api.now(),country=d["country"],owner_id=d["owner_id"],message_id=row.id,status="completada" if due else "programada",provider="Microsoft 365 simulado")
    return row

def draft_email(s,user,a):
    from . import main as api
    contact=api.get(s,a.app,"contacts",a.entity_id or a.payload.get("contact_id")); api.write(s,user,contact)
    d=contact.data; company=api.get(s,a.app,"companies",d["company_id"])
    configs=sorted(api.records(s,a.app,"ai_settings"),key=lambda r:r.data.get("version",0))
    config=configs[-1].data if configs else {}
    settings=config.get("settings",{})
    if settings.get("enabled") is False: api.fail("Los borradores asistidos están pausados en configuración",409)
    daily_budget=settings.get("daily_budget",100)
    generated_today=sum(r.data.get("created_at","")[:10]==utcnow().date().isoformat() for r in api.records(s,a.app,"email_drafts"))
    if generated_today>=daily_budget: api.fail("Presupuesto diario de borradores simulados agotado",409)
    sector=company.data.get("sector","su rubro")
    signal=(company.data.get("profile",{}).get("signals") or ["la próxima campaña"])[0]
    greeting=f"Hola {d['name'].split()[0]}, ¿cómo estás?" if d["country"]=="UY" else f"Hola {d['name'].split()[0]},"
    if "formal" in str(settings.get("tone","")).casefold(): greeting=f"Estimado/a {d['name']}:"
    request="¿Te viene bien conversar 20 minutos el martes o el jueves para revisar zonas y objetivos?" if d["country"]=="UY" else "¿Podemos coordinar 20 minutos esta semana para revisar cobertura y objetivos?"
    body=f"{greeting}\n\nVimos que {d['company_name']} está trabajando en {signal}. En {sector.lower()}, la presencia en vía pública puede acompañar ese momento con cobertura en los recorridos de su audiencia.\n\n{request}\n\n{user['name']}\nGlobal Vía Pública"
    if d.get("status")=="contactado": body=f"{greeting}\n\nRetomo el contacto sobre {signal} de {d['company_name']}. Podemos revisar una propuesta de cobertura ajustada a los objetivos de {sector.lower()}.\n\n{request}\n\n{user['name']}\nGlobal Vía Pública"
    return api.new(s,a.app,"email_drafts",contact_id=contact.id,country=d["country"],owner_id=d["owner_id"],subject=f"{d['company_name']} · cobertura para {signal}",body=body,status="borrador",provider="Claude simulado · reglas locales",requires_human_review=True,configuration_version=config.get("version"),generation_constraints=settings.get("instructions","Sin negociación de precios ni descuentos"),tone=settings.get("tone","Uruguayo" if d["country"]=="UY" else "Profesional"))

def save_sequence(s,user,a):
    from . import main as api
    p=a.payload; contact=api.get(s,a.app,"contacts",p.get("contact_id") or a.entity_id);api.write(s,user,contact)
    if contact.data.get("excluded") or contact.data.get("status")=="respondió": api.fail("No se puede programar una secuencia a este contacto",409)
    steps=p.get("steps",[{"delay_days":7,"subject":"Seguimiento de cobertura","body":"¿Coordinamos 20 minutos para revisar la propuesta?"},{"delay_days":14,"subject":"Retomo nuestra propuesta","body":"Quedo a disposición para revisar objetivos y zonas."}])
    if not isinstance(steps,list) or not 1<=len(steps)<=6: api.fail("Secuencia entre 1 y 6 pasos")
    clean=[]
    for step in steps:
        if not isinstance(step,dict): api.fail("Paso de secuencia inválido")
        try: days=int(step.get("delay_days",7))
        except (TypeError,ValueError): api.fail("Espera de seguimiento inválida")
        if not 7<=days<=90: api.fail("Cada seguimiento requiere entre 7 y 90 días de espera")
        clean.append({"delay_days":days,"subject":api.text_field(step,"subject","Seguimiento comercial",300),"body":api.text_field(step,"body","¿Coordinamos una reunión?",20000)})
    for old in api.records(s,a.app,"sequences"):
        if old.data.get("contact_id")==contact.id and old.data.get("status")=="activa": api.save(s,old,status="reemplazada")
    return api.new(s,a.app,"sequences",name=str(p.get("name","Seguimiento comercial"))[:200],contact_id=contact.id,country=contact.data["country"],owner_id=contact.data["owner_id"],steps=clean,status="activa",next_step=0,next_at=(utcnow()+timedelta(days=clean[0]["delay_days"])).isoformat(),provider="Microsoft 365 simulado",requires_human_approval=True)

def simulate_sequence(s,user,a):
    from . import main as api
    sequence=api.get(s,a.app,"sequences",a.entity_id or a.payload.get("sequence_id"));api.write(s,user,sequence)
    if sequence.data.get("status")!="activa": api.fail("La secuencia no está activa",409)
    contact=api.get(s,a.app,"contacts",sequence.data["contact_id"]);api.write(s,user,contact)
    n=sequence.data.get("next_step",0);steps=sequence.data["steps"]
    if n>=len(steps): api.fail("Secuencia completada",409)
    step=steps[n]; due=parsed(sequence.data.get("next_at")) or utcnow()+timedelta(days=step["delay_days"])
    message=queue_email(s,user,contact,step["subject"],step["body"],earliest=due,sequence_id=sequence.id)
    api.save(s,sequence,next_step=n+1,status="completada" if n+1==len(steps) else "activa",next_at=(parsed(message.data["scheduled_at"])+timedelta(days=steps[min(n+1,len(steps)-1)]["delay_days"])).isoformat(),last_message_id=message.id)
    return sequence

def cancel_pending(s,contact,reason):
    from . import main as api
    for row in api.records(s,"prospectador","messages"):
        if row.data.get("contact_id")==contact.id and row.data.get("direction")=="outbound":
            changes={"followup_status":"cancelado","cancellation_reason":reason}
            if row.data.get("status")=="programado": changes["status"]="cancelado"
            api.save(s,row,**changes)
    for row in api.records(s,"prospectador","sequences"):
        if row.data.get("contact_id")==contact.id and row.data.get("status")=="activa": api.save(s,row,status="cancelada",cancellation_reason=reason)

def sync_inbox(s,user,a):
    from . import main as api
    lock(s,"mail-sync:"+user["id"])
    runs=[r for r in api.records(s,a.app,"mail_sync") if r.data.get("owner_id")==user["id"]]
    last=max((parsed(r.data["created_at"]) for r in runs),default=None)
    if last and utcnow()<last+timedelta(minutes=10):
        return api.Record(id="inbox-wait",app=a.app,kind="result",data={"id":"inbox-wait","status":"espera","next_poll_at":(last+timedelta(minutes=10)).isoformat(),"message":"Lectura simulada cada 10 minutos","processed":0,"provider":"Microsoft 365 simulado"})
    # Process queued simulation locally; never opens a socket to Microsoft.
    sent=0
    queued=sorted(api.records(s,a.app,"messages"),key=lambda r:r.data.get("scheduled_at", ""))
    for message in queued:
        d=message.data
        if not api.allowed(s,user,message) or d.get("status")!="programado" or (parsed(d.get("scheduled_at")) or utcnow()+timedelta(days=1))>utcnow(): continue
        contact=api.get(s,a.app,"contacts",d["contact_id"])
        if contact.data.get("excluded") or contact.data.get("status") in {"respondió","no_contactar"}:
            cancel_pending(s,contact,"respuesta o exclusión");continue
        current=utcnow()
        allowed_at=next_window(current,contact.data["country"])
        previous_contact=parsed(contact.data.get("last_contact_at"))
        if previous_contact: allowed_at=max(allowed_at,previous_contact+timedelta(days=7))
        sent_messages=[m.data for m in api.records(s,a.app,"messages") if m.id!=message.id and m.data.get("owner_id")==d["owner_id"] and m.data.get("sent_at") and m.data.get("status")=="enviado_simulado"]
        recent=[parsed(m["sent_at"]) for m in sent_messages if parsed(m["sent_at"]) and parsed(m["sent_at"])>=current-timedelta(hours=12)]
        if recent: allowed_at=max(allowed_at,max(recent)+timedelta(seconds=8+(45 if len(recent)%15==0 else 0)))
        allowed_at=next_window(allowed_at,contact.data["country"])
        if allowed_at>current+timedelta(seconds=1):
            api.save(s,message,scheduled_at=allowed_at.isoformat(),queue_reason="Revalidación de horario, ritmo y espera entre contactos")
            continue
        api.save(s,message,status="enviado_simulado",sent_at=api.now());api.save(s,contact,last_contact_at=api.now(),status="contactado");sent+=1
    contacts=[r for r in api.records(s,a.app,"contacts") if api.allowed(s,user,r) and not r.data.get("excluded") and r.data.get("status")=="contactado"]
    if a.payload.get("contact_id"):
        chosen=api.get(s,a.app,"contacts",a.payload["contact_id"]);api.write(s,user,chosen);contacts=[chosen]
    kinds=["respuesta","rebote","respuesta_automatica","no_contactar"]
    processed=0
    for i,contact in enumerate(contacts[:4]):
        kind=a.payload.get("classification",kinds[i%4])
        if kind not in kinds: api.fail("Clasificación de bandeja inválida")
        texts={"respuesta":"Gracias, conversemos sobre la propuesta y coordinemos una reunión.","rebote":"Entrega no completada: dirección no disponible.","respuesta_automatica":"Estoy fuera de la oficina. Retomo la próxima semana.","no_contactar":"Por favor, no me contacten nuevamente."}
        api.new(s,a.app,"messages",contact_id=contact.id,thread_id=f"thread-{contact.id}",country=contact.data["country"],owner_id=contact.data["owner_id"],subject="Re: Propuesta de cobertura",body=texts[kind],direction="inbound",status="recibido_simulado",classification=kind,suggested_status="respondió" if kind=="respuesta" else "no_contactar" if kind in {"rebote","no_contactar"} else "contactado",provider="Microsoft 365 simulado",simulated=True)
        if kind=="respuesta": api.save(s,contact,status="respondió");cancel_pending(s,contact,"respuesta")
        elif kind in {"rebote","no_contactar"}: api.save(s,contact,status="no_contactar",excluded=True,email_valid=kind!="rebote",exclusion_reason=kind);cancel_pending(s,contact,kind)
        else:
            for sequence in api.records(s,a.app,"sequences"):
                if sequence.data.get("contact_id")==contact.id and sequence.data.get("status")=="activa": api.save(s,sequence,next_at=(utcnow()+timedelta(days=7)).isoformat(),pause_reason="respuesta automática")
        api.new(s,a.app,"activities",type="inbox",title=f"Bandeja: {kind.replace('_',' ')}",contact_id=contact.id,country=contact.data["country"],owner_id=contact.data["owner_id"],date=api.now(),status="completada",provider="Microsoft 365 simulado")
        api.notice(s,a.app,user,f"{contact.data['name']}: {kind.replace('_',' ')}",contact_id=contact.id);processed+=1
    return api.new(s,a.app,"mail_sync",country=user["country"],owner_id=user["id"],provider="Microsoft 365 simulado",processed=processed,sent_count=sent,next_poll_at=(utcnow()+timedelta(minutes=10)).isoformat(),status="completada")

def campaign_send(s,user,a):
    from . import main as api
    campaign=api.get(s,a.app,"campaigns",a.entity_id);api.write(s,user,campaign);d=campaign.data
    if d["status"]!="aprobada" or not d.get("approved_by"): api.fail("El envío exige aprobación humana previa",409)
    if d.get("approval_hash") and d["approval_hash"]!=api.fingerprint(d): api.fail("El contenido cambió: requiere una nueva aprobación",409)
    count=0;skipped=0
    for rid in d["contact_ids"]:
        c=api.get(s,a.app,"contacts",rid);api.read(s,user,c)
        if c.data.get("excluded") or c.data.get("status") in {"respondió","no_contactar"} or c.data.get("email_valid") is False: skipped+=1;continue
        queue_email(s,user,c,d["subject"],d["body"],campaign_id=campaign.id);count+=1
    api.save(s,campaign,status="enviada",sent_count=count,queued_count=count,skipped_count=skipped,sent_at=api.now(),simulated=True,delivery_note="Mensajes procesados por el simulador según su horario y ritmo")
    return campaign

def action(s,user,a):
    from . import main as api
    name=a.action;p=a.payload
    if name=="save_ai_settings":
        if not set(capabilities(user))&{"configure_ai","configure"}: api.fail("Solo Jefe IA o administración puede configurar agentes",403)
        allowed={"name","tone","target_roles","target_sectors","template","rules","enabled","daily_limit","prompt","offering","persona","instructions","daily_budget"}
        data={k:v for k,v in p.items() if k in allowed}
        if len(str(data))>16000: api.fail("Configuración demasiado extensa")
        if "enabled" in data and not isinstance(data["enabled"],bool): api.fail("Estado de agente inválido")
        if "daily_budget" in data:
            try: data["daily_budget"]=int(data["daily_budget"])
            except (ValueError,TypeError): api.fail("Presupuesto diario inválido")
            if not 0<=data["daily_budget"]<=5000: api.fail("Presupuesto diario entre 0 y 5000 borradores")
        for key in ["tone","persona","instructions","template","prompt","offering"]:
            if key in data and (not isinstance(data[key],str) or len(data[key])>5000): api.fail(f"Configuración {key} inválida")
        return api.new(s,a.app,"ai_settings",country=user["country"],owner_id=user["id"],settings=data,provider="Claude simulado",version=len(api.records(s,a.app,"ai_settings"))+1)
    if name=="configure_credits":
        if user["role"]!="superadmin": api.fail("Solo Super admin puede configurar créditos",403)
        try: limit=int(p.get("organization_limit",ORG_LIMIT));wallets={k:int(v) for k,v in p.get("wallet_limits",{}).items()}
        except (TypeError,ValueError,AttributeError): api.fail("Límites de créditos inválidos")
        if not 0<=limit<=1000000 or any(not 0<=v<=100000 for v in wallets.values()): api.fail("Límites fuera de rango")
        return api.new(s,a.app,"credit_settings",country=user["country"],owner_id=user["id"],organization_limit=limit,wallet_limits=wallets)
    if "manage_records" not in capabilities(user): api.fail("El perfil no puede operar acciones comerciales",403)
    if name=="search_prospects": return search(s,user,a)
    if name in {"preview_reveal","reveal_contact","reveal_contacts"}: return reveal(s,user,a)
    if name=="draft_email": return draft_email(s,user,a)
    if name=="send_campaign": return campaign_send(s,user,a)
    if name=="send_email":
        c=api.get(s,a.app,"contacts",a.entity_id or p.get("contact_id"));api.write(s,user,c)
        return queue_email(s,user,c,api.text_field(p,"subject",limit=300),api.text_field(p,"body",limit=20000))
    if name=="save_sequence": return save_sequence(s,user,a)
    if name=="simulate_sequence": return simulate_sequence(s,user,a)
    if name in {"sync_inbox","poll_inbox"}: return sync_inbox(s,user,a)
    api.fail("Acción comercial no soportada")

def extend_state(s,user,out,source_rows=None):
    credits=credit_state(s,user,out["prospects"],source_rows)
    # Contact identities are internal dedup keys, never exposed via ledger.
    credits["history"]=[{k:v for k,v in r.items() if k!="identity"} for r in credits["history"]]
    out["credits"]=credits
    out["credit_history"]=credits["history"]
    threads=defaultdict(list)
    for message in out["messages"]:
        threads[message.get("thread_id") or f"thread-{message.get('contact_id')}"] .append(message)
    out["inbox"]=[{"id":rid,"contact_id":messages[0].get("contact_id"),"subject":messages[-1].get("subject"),"messages":sorted(messages,key=lambda d:d.get("created_at","")),"last_at":max(m.get("created_at","") for m in messages),"classification":next((m.get("classification") for m in reversed(sorted(messages,key=lambda d:d.get("created_at",""))) if m.get("direction")=="inbound"),None)} for rid,messages in threads.items()]
    out["inbox"].sort(key=lambda t:t["last_at"],reverse=True)
    out["email_queue"]=[m for m in out["messages"] if m.get("direction")=="outbound" and m.get("status")=="programado"]
    out["mail_policy"]={**MAIL_POLICY,"timezone":TIMEZONES.get(user["country"],"America/Montevideo")}
    companies={c["id"]:c for c in out["companies"]}
    today=[]
    for c in out["contacts"]:
        if c.get("excluded") or c.get("email_valid") is False or c.get("status") in {"respondió","no_contactar","ganado","perdido"}: continue
        last=parsed(c.get("last_contact_at"));days=(utcnow()-last).days if last else 999
        if days<7: continue
        sector=companies.get(c.get("company_id"),{}).get("sector","Otros")
        priority=(30 if sector in {"Retail","Turismo","Gastronomía"} else 10)+(20 if c.get("status")=="nuevo" else 5)+min(days,90)
        today.append({**c,"sector":sector,"days_since_contact":None if not last else days,"priority":priority,"reason":f"{sector} · {c.get('status','nuevo')} · correo válido · {'primer contacto' if not last else str(days)+' días sin contacto'}"})
    out["write_today"]=sorted(today,key=lambda d:(d.get("country")!="UY",-d["priority"],d["name"]))
    searches=out.get("search_runs",[])
    out["last_search"]=next((r for r in searches if r.get("owner_id")==user["id"]),None)
    out["ai_settings_current"]=(out.get("ai_settings") or [{}])[0].get("settings",{})
