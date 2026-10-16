"""Fixed-seed, additive demo catalogue. Never deletes uploads or user records."""
from datetime import date, datetime, timedelta, timezone
from random import Random
import re
from sqlalchemy import select
from .db import Record
from .seed import COUNTRIES

VERSION = 3
ANCHOR = date(2026, 10, 16)
FX = {"UY": 41.2, "CL": 945, "AR": 1450, "PE": 3.75, "MX": 18.6}  # illustrative fixture rates, not market quotes
OWNER = {"UY": "executive-uy", "CL": "executive-cl", "AR": "executive-ar", "PE": "executive-pe", "MX": "executive-mx"}
SECTORS = ["Retail", "Tecnología", "Movilidad", "Servicios financieros", "Gastronomía", "Salud", "Educación", "Turismo"]
SIGNALS = {
    "Retail": ["apertura de locales", "campaña de fin de año", "nueva colección"],
    "Tecnología": ["lanzamiento de producto", "expansión regional", "nueva aplicación"],
    "Movilidad": ["nueva ruta", "renovación de flota", "expansión urbana"],
    "Servicios financieros": ["nuevo producto", "campaña de inclusión", "apertura de sucursal"],
    "Gastronomía": ["apertura de locales", "menú de temporada", "nuevo servicio de entrega"],
    "Salud": ["nueva sede", "campaña preventiva", "ampliación de cobertura"],
    "Educación": ["matrículas abiertas", "nuevo programa", "campaña de admisiones"],
    "Turismo": ["temporada de verano", "nuevo destino", "campaña de reservas"],
}
FIRST = ["Lucía", "Mateo", "Valentina", "Joaquín", "Camila", "Bruno", "Florencia", "Nicolás", "María", "Tomás", "Paula", "Emiliano", "Catalina", "Andrés", "Renata", "Felipe"]
LAST = ["Pereira", "Soler", "Arce", "Medina", "Lagos", "Montiel", "Cabrera", "Salazar", "Fuentes", "Aguirre", "Lemos", "Navarro", "Cortés", "Vidal", "Benítez", "Rivas"]
ROOTS = ["Albor", "Brisalia", "Cendal", "Darsena", "Elaria", "Fresnal", "Gredal", "Hilaria", "Islar", "Juncal", "Kairal", "Lindara", "Mistralia", "Nubelar", "Olvar", "Puentaria", "Quirena", "Riberal", "Sendar", "Tramalia", "Umbralía", "Vental", "Yaralia"]
SUFFIX = ["Urbana", "del Plata", "Andina", "del Sur", "Metropolitana", "del Valle", "del Pacífico", "Austral", "Central", "Continental", "de la Costa", "del Parque", "de la Sierra", "del Puerto", "de la Rivera", "del Sol", "del Monte", "del Centro", "del Este", "del Norte"]

def stamp(d):
    return datetime.combine(min(d,ANCHOR), datetime.min.time(), tzinfo=timezone.utc).isoformat()

def month_date(offset, day=10):
    value=2026*12+9-offset
    return date(value//12,value%12+1,day)

# Historia verosímil: tendencia del piloto, estacionalidad del hemisferio sur y variación por país.
SEASON = {1:0.62,2:0.7,3:1.12,4:1.18,5:1.1,6:0.95,7:0.84,8:0.98,9:1.12,10:1.22,11:1.15,12:0.82}

def month_weights(cc, growth):
    noise=Random(f"meses-{cc}")
    weights=[]
    for offset in range(18):
        month=month_date(offset).month
        trend=1-growth*offset/17  # offset 0 = mes actual
        weights.append(max(0.05,trend*SEASON[month]*noise.uniform(0.82,1.18)))
    weights[0]*=ANCHOR.day/30  # el mes en curso va a mitad de camino
    return weights

def pick_date(rng, weights, max_offset=17):
    offset=rng.choices(range(max_offset+1),weights[:max_offset+1])[0]
    day=rng.randint(1,ANCHOR.day-1) if offset==0 else rng.randint(1,28)
    return month_date(offset,day),offset

def slug(text):
    text=text.lower()
    for a,b in zip("áéíóúüñ","aeiouun"): text=text.replace(a,b)
    return re.sub(r"[^a-z0-9]+","",text)

def phone(cc, n, j):
    """Formato telefónico de cada país; números generados para la demostración."""
    r=Random(f"tel-{cc}-{n}-{j}")
    if cc=="UY": return f"+598 9{r.randint(1,9)} {r.randint(100,999)} {r.randint(100,999)}"
    if cc=="CL": return f"+56 9 {r.randint(1000,9999)} {r.randint(1000,9999)}"
    if cc=="AR": return f"+54 11 {r.randint(1000,9999)}-{r.randint(1000,9999)}"
    if cc=="PE": return f"+51 9{r.randint(10,99)} {r.randint(100,999)} {r.randint(100,999)}"
    return f"+52 55 {r.randint(1000,9999)} {r.randint(1000,9999)}"

PIPELINE = ["nuevo","calificada","propuesta","negociacion"]
NOTES = {"nuevo":"Oportunidad abierta","calificada":"Necesidad y presupuesto validados","propuesta":"Propuesta enviada","negociacion":"Condiciones en negociación","ganado":"Orden de compra recibida","perdido":"Cerrada sin acuerdo"}

def stage_history(rng, opened, owner, stage):
    """Recorre cada etapa intermedia con fechas crecientes; una pérdida ocurre desde una etapa real."""
    if stage=="ganado": path=PIPELINE+["ganado"]
    elif stage=="perdido": path=PIPELINE[:rng.randint(1,4)]+["perdido"]
    else: path=PIPELINE[:PIPELINE.index(stage)+1]
    at=opened; history=[]; previous=None
    for status in path:
        history.append({"at":stamp(at),"by":owner,"from":previous,"status":status,"note":NOTES[status]})
        previous=status; at=at+timedelta(days=rng.randint(4,18))
    return history

LEGAL = ["S.A.", "SpA", "S.R.L.", "Ltda.", "S.A. de C.V.", "S.A.C."]

def seed_v3(session):
    rng=Random(84261016)
    existing={r.id:r for r in session.scalars(select(Record))}
    def add(application,kind,rid,created=None,**data):
        if rid in existing: return existing[rid].data
        row=Record(id=rid,app=application,kind=kind,data={"id":rid,"created_at":stamp(created or ANCHOR),"seed_version":VERSION,"synthetic":True,**data})
        session.add(row); existing[rid]=row
        return row.data
    # Upgrade only unmistakable legacy fixture labels, preserving all private uploads/user data.
    for row in existing.values():
        if row.data.get("has_real_uploads") or not re.fullmatch(r"(?:company|contact|prospect|contract)-[A-Z]{2}-\d+(?:-\d+)?",row.id): continue
        data=dict(row.data)
        for key in ["name","company_name","company","counterparty"]:
            if isinstance(data.get(key),str):
                data[key]=data[key].replace(" · Ficticia","").replace(" · Sociedad ficticia","")
        generic=re.fullmatch(r"Contraparte (\w+) ([A-Z]{2})",data.get("counterparty") or "")
        if generic:
            word,code=generic.groups(); k=sum(map(ord,row.id))
            data["counterparty"]=f"{word} {SUFFIX[k%len(SUFFIX)]} {LEGAL[k%len(LEGAL)]}"
        row.data=data
    total=0
    for country in COUNTRIES:
        cc=country["code"]; owner=OWNER[cc]; count=180 if cc=="UY" else 70
        crm_weights=month_weights(cc,0.62 if cc=="UY" else 0.4)  # el piloto uruguayo crece más rápido
        clm_weights=month_weights("clm-"+cc,0.3)
        opp_weights=month_weights("opp-"+cc,0.3)
        add("prospectador","icp_profiles",f"v3-icp-{cc}",name=f"Visibilidad urbana · {cc}",country=cc,owner_id=owner,status="activo",version=1,target_sectors=["Retail","Gastronomía","Turismo","Servicios financieros"],countries=[cc],signals=["apertura de locales","expansión regional","temporada de verano"],exclusions=["sin actividad"],min_employees=40,max_employees=3000,annual_budget_min=15000,persona="Gerencias de Marketing, Marca y General",offering="Campañas de vía pública con cobertura urbana",source="Criterios ilustrativos del catálogo")
        for i in range(count):
            n=total; total+=1; sector=SECTORS[(i+len(cc)+ord(cc[0]))%len(SECTORS)]
            name=f"{ROOTS[n%len(ROOTS)]} {SUFFIX[n//len(ROOTS)]}"
            co=f"v3-company-{cc}-{i:03}"; domain=f"{slug(name)}.example"
            created,company_offset=pick_date(rng,crm_weights)
            opened=None
            if i%2==0:
                opened,_=pick_date(rng,opp_weights)
                created=min(created,opened)  # la cuenta existe antes que su oportunidad
            signals=rng.sample(SIGNALS[sector],1+i%2)
            employees=None if i%7==0 else rng.choice([24,65,120,280,650,1800,4200])
            budget=None if i%5==0 else rng.choice([8000,18000,45000,90000,160000])
            criteria=[{"label":"Sector","matched":sector in ["Retail","Gastronomía","Turismo","Servicios financieros"],"weight":25,"available":True},{"label":"País piloto","matched":cc=="UY","weight":20,"available":True},{"label":"Tamaño","matched":employees is not None and 40<=employees<=3000,"weight":20,"available":employees is not None},{"label":"Presupuesto USD","matched":budget is not None and budget>=15000,"weight":20,"available":budget is not None},{"label":"Señales","matched":bool(set(signals)&{"apertura de locales","expansión regional","temporada de verano"}),"weight":15,"available":True}]
            available=[c for c in criteria if c["available"]]; score=round(sum(c["matched"] for c in available)/len(available)*100)
            missing=[c["label"] for c in criteria if not c["available"]]
            profile={"industry":sector,"employees":employees,"annual_budget":budget,"budget_currency":"USD","signals":signals,"exclusions":[],"offering":f"{sector}: cobertura en {1+i%9} ciudades","ideal_customer":["Consumidores urbanos","Familias y residentes","Profesionales y viajeros"][i%3],"persona":["Gerente de Marketing","Gerente de Marca","Gerente General"][i%3],"website_notes":f"{signals[0].capitalize()} en {cc}. Evidencia ilustrativa del catálogo, sin consulta web.","field_sources":{k:{"source":"Catálogo sintético v3","recorded_at":stamp(created)} for k in ["industry","employees","annual_budget","signals"]}}
            fit={"score":score,"coverage":len(available)*20,"decision":"informacion_insuficiente" if missing else "priorizar" if score>=75 else "revisar","score_type":"coincidencia de criterios; no probabilidad de venta","criteria":criteria,"criteria_evaluated":len(available),"criteria_configured":5,"reasons":[f"{c['label']}: {'coincide' if c['matched'] else 'requiere validación' if not c['available'] else 'no coincide'}" for c in criteria],"missing_fields":missing,"sources":[{"field":k,"source":"Catálogo sintético v3","value":profile[k],"evidence":"Dato ilustrativo de demostración; sin investigación externa"} for k in ["industry","employees","annual_budget","signals"]],"method":"reglas locales transparentes","ai_connected":False,"external_enrichment":False,"evaluated_at":stamp(ANCHOR)}
            add("prospectador","companies",co,created,name=name,domain=domain,sector=sector,country=cc,owner_id=owner,status="activo",employees=employees,size="1-50" if not employees or employees<=50 else "51-200" if employees<=200 else "201-1000" if employees<=1000 else "1000+",profile=profile,fit=fit,source="Catálogo sintético v3")
            for j in range(4):
                contact=f"v3-contact-{cc}-{i:03}-{j}"; person=f"{FIRST[(n+j*3)%16]} {LAST[(n//16+j*5)%16]}"
                status=["nuevo","contactado","respondió","reunión","propuesta","ganado","perdido","no_contactar"][(i*4+j)%8]
                add("prospectador","contacts",contact,created,name=person,email=f"{['marketing','marca','direccion','comercial'][j]}@{domain}",title=["Gerente de Marketing","Gerente de Marca","Gerente General","Directora Comercial"][j],seniority="gerencia",department=["Marketing","Marketing","Dirección","Comercial"][j],phone=phone(cc,n,j),company_id=co,company_name=name,sector=sector,country=cc,owner_id=owner,status=status,excluded=status=="no_contactar",email_valid=i%19!=0,score=score,last_contact_at=stamp(ANCHOR-timedelta(days=8+(i+j)%60)) if status!="nuevo" else None,source="Catálogo sintético v3")
            for j in range(2):
                pid=f"v3-prospect-{cc}-{i:03}-{j}"
                already=j==0 and i%5==0
                person=f"{FIRST[(n+j+7)%16]} {LAST[(n//16+j+2)%16]}"
                email=f"{slug(person.split()[0])}.{slug(person.split()[1])}@{domain}"
                prospect=add("prospectador","prospects",pid,created,name=person,email=email,phone=phone(cc,n,10+j),title=["Gerente de Marketing","Gerente de Marca"][j],seniority="gerencia",department="Marketing",company_id=co,company_name=name,domain=domain,sector=sector,size="51-200" if i%2 else "201-1000",country=cc,owner_id=owner,status="revelado" if already else "pendiente",revealed=already,credit_cost=1,credit_cost_paid=1 if already else 0,source="Lusha simulado")
                if already:
                    contact_id=f"v3-revealed-{cc}-{i:03}"
                    prospect["contact_id"]=contact_id
                    add("prospectador","contacts",contact_id,created,name=prospect["name"],email=email,phone=prospect["phone"],title=prospect["title"],company_id=co,company_name=name,sector=sector,country=cc,owner_id=owner,status="nuevo",excluded=False,email_valid=True,source="Lusha simulado")
                    add("prospectador","credit_ledger",f"v3-credit-{cc}-{i:03}",created,country=cc,owner_id=owner,portfolio_id=owner,run_id=f"v3-run-{cc}-{created:%Y-%m}",prospect_ids=[pid],identity=email,cost=1,reason="Revelación de referente",provider="Lusha simulado")
            if i%2==0:
                stage=["nuevo","calificada","propuesta","negociacion","ganado","perdido"][(i//2)%6]; usd=round(rng.uniform(5000,95000),2)
                add("prospectador","opportunities",f"v3-opportunity-{cc}-{i:03}",opened,name=f"{name} · {signals[0]}",company_id=co,contact_id=f"v3-contact-{cc}-{i:03}-0",country=cc,owner_id=owner,sector=sector,status=stage,amount=round(usd*FX[cc],2),currency=country["currency"],amount_usd=usd,fx_source="Equivalencia ilustrativa de la semilla; no cotización",probability={"nuevo":10,"calificada":25,"propuesta":60,"negociacion":80,"ganado":100,"perdido":0}[stage],expected_close=(ANCHOR+timedelta(days=(i%90)-15)).isoformat(),history=stage_history(rng,opened,owner,stage))
        # Complete 18-month event history: every numerator derives from these rows.
        for month in range(18):
            d=month_date(month,min(10,ANCHOR.day-1) if month==0 else 10)
            # Las campañas salen el día 10: el mes en curso ya la envió completa, sin el ajuste de mes parcial.
            scale=(crm_weights[month]/(ANCHOR.day/30) if month==0 else crm_weights[month])/max(crm_weights[1:]+[crm_weights[0]/(ANCHOR.day/30)])
            participants=max(4,min(count,round((26 if cc=="UY" else 14)*scale*rng.uniform(0.85,1.15))))
            reply_rate=0.14+0.11*(17-month)/17+rng.uniform(-0.03,0.03)
            bounce_rate=0.07-0.03*(17-month)/17+rng.uniform(-0.01,0.01)
            meeting_rate=0.38+0.14*(17-month)/17
            campaign=f"v3-campaign-{cc}-{month:02}"
            add("prospectador","campaigns",campaign,d,name=f"{SECTORS[month%8]} · {d:%B %Y}",country=cc,owner_id=owner,status="enviada",contact_ids=[f"v3-contact-{cc}-{i:03}-0" for i in range(participants)],subject=f"Cobertura urbana · {d:%Y-%m}",body="Primer contacto comercial revisado por jefatura. Microsoft 365 simulado.",approved_by="agustin-silva" if cc=="UY" else "regional",sent_count=participants,reply_count=round(participants*reply_rate),sent_at=stamp(d),approved_at=stamp(d-timedelta(days=1)))
            for j in range(participants):
                cid=f"v3-contact-{cc}-{j:03}-0"
                add("prospectador","messages",f"v3-message-{cc}-{month:02}-{j}",d,contact_id=cid,thread_id=f"thread-{cid}",campaign_id=campaign,country=cc,owner_id=owner,subject=f"Cobertura urbana · {d:%Y-%m}",body="Conversemos sobre la próxima campaña de marca. ¿Coordinamos 20 minutos esta semana?",direction="outbound",status="enviado_simulado",provider="Microsoft 365 simulado",sent_at=stamp(d),followup_status="completado",sector=SECTORS[(j+2+ord(cc[0]))%8])
                replied=rng.random()<reply_rate; bounced=not replied and rng.random()<bounce_rate
                if replied:
                    add("prospectador","messages",f"v3-reply-{cc}-{month:02}-{j}",d+timedelta(days=1),contact_id=cid,thread_id=f"thread-{cid}",campaign_id=campaign,country=cc,owner_id=owner,subject="Re: Cobertura urbana",body="Gracias, coordinemos una reunión para revisar cobertura.",direction="inbound",status="recibido_simulado",classification="respuesta",suggested_status="respondió",provider="Microsoft 365 simulado")
                elif bounced:
                    add("prospectador","messages",f"v3-bounce-{cc}-{month:02}-{j}",d+timedelta(days=1),contact_id=cid,thread_id=f"thread-{cid}",campaign_id=campaign,country=cc,owner_id=owner,subject="Entrega no completada",body="Rebote simulado: casilla no disponible.",direction="inbound",status="recibido_simulado",classification="rebote",suggested_status="no_contactar",provider="Microsoft 365 simulado")
                if replied and rng.random()<meeting_rate:
                    add("prospectador","activities",f"v3-meeting-{cc}-{month:02}-{j}",d+timedelta(days=3),contact_id=cid,campaign_id=campaign,title="Revisión de cobertura y objetivos",type="meeting",country=cc,owner_id=owner,status="completada",date=stamp(d+timedelta(days=3)),sector=SECTORS[(j+2+ord(cc[0]))%8])
        for i in range(44):
            cid=f"v3-contract-{cc}-{i:03}"; created,_=pick_date(rng,clm_weights); usd=round(rng.uniform(12000,350000),2)
            status=["borrador","en_revision","pendiente_aprobacion","aprobado","pendiente_firma","firmado","activo","activo","en_renovacion","vencido","archivado"][i%11]
            end=ANCHOR+timedelta(days=[15,28,44,58,74,88,125,210,-12,365,480][i%11])
            typ=["Comercial","Servicios","Arrendamiento","NDA","Concesión","Licencia","Suministro"][i%7]
            history=[{"status":"borrador","at":stamp(created),"by":owner,"note":"Solicitud inicial"},{"status":"en_revision","at":stamp(created+timedelta(days=1+i%4)),"by":"legal-pe" if cc=="PE" else "regional","note":"Validación de antecedentes"}]
            if status not in {"borrador","en_revision","pendiente_aprobacion"}: history.append({"status":"aprobado","at":stamp(created+timedelta(days=4+i%12)),"by":"regional","note":"Revisión humana de condiciones"})
            history.append({"status":status,"at":stamp(created+timedelta(days=7+i%14)),"by":owner,"note":"Estado del expediente"})
            add("contratos","contracts",cid,created,title=f"{typ} · {ROOTS[i%23]} {SUFFIX[(i//23)+cc.__len__()]}",name=f"Expediente {cc}-{300+i}",reference=f"VRT-{cc}-2026-{300+i}",country=cc,owner_id=owner,company=f"Vertia {country['name']}",counterparty=f"{ROOTS[(i+9)%23]} {SUFFIX[(i//23)+5]}",amount=round(usd*FX[cc],2),amount_usd=usd,currency=country["currency"],fx_source="Equivalencia ilustrativa de la semilla",type=typ,status=status,confidential=True,start_date=created.isoformat(),end_date=end.isoformat(),renewal_notice_days=30+(i%3)*30,version=1+i%3,documents=[{"id":f"v3-doc-{cc}-{i:03}-{v}","filename":f"{typ.lower()}_{cc}_{300+i}_v{v}.pdf","kind":"contrato","version":v,"created_at":stamp(created+timedelta(days=v)),"synthetic":True} for v in range(1,2+i%3)],history=history,analysis=None,redacted_ready=False,amendments=[],signature=None,template=f"Plantilla {typ.lower()} regional")
            for j in range(3):
                complete=(i+j)%4!=0
                add("contratos","obligations",f"v3-obligation-{cc}-{i:03}-{j}",created,contract_id=cid,title=["Renovar póliza de responsabilidad","Validar reporte de exhibición","Confirmar permiso de emplazamiento"][j],country=cc,owner_id=owner,due_date=(ANCHOR+timedelta(days=(i*3+j*15)%120-25)).isoformat(),status="completada" if complete else "pendiente",evidence="Acta de revisión registrada" if complete else None,completed_at=stamp(ANCHOR-timedelta(days=i%20)) if complete else None)
    session.flush()
