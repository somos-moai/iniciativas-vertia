from .db import Record

COUNTRIES = [
    {"code":"CL","name":"Chile","currency":"CLP"},
    {"code":"UY","name":"Uruguay","currency":"UYU"},
    {"code":"PE","name":"Perú","currency":"PEN"},
    {"code":"AR","name":"Argentina","currency":"ARS"},
    {"code":"MX","name":"México","currency":"MXN"},
]
USERS = [
    {"id":"agustin-silva","name":"Agustín Silva","title":"Jefe Comercial","role":"manager","country":"UY","apps":["prospectador"]},
    {"id":"santiago-ordonez","name":"Santiago Ordoñez","title":"Jefe IA","role":"ia_lead","country":"UY","apps":["prospectador"]},
    {"id":"enrique-escobar","name":"Enrique Escobar","title":"Super admin","role":"superadmin","country":"UY","apps":["prospectador"]},
    {"id":"gonzalo-oviedo","name":"Gonzalo Oviedo","title":"Jefe de Innovación","role":"innovation_admin","country":"CL","apps":["contratos"]},
    {"id":"phillipe","name":"Phillipe","title":"Regional","role":"regional","country":"CL","apps":["contratos"]},
    {"id":"executive-pe","name":"Gabriela Arce","title":"Ejecutiva Comercial Perú","role":"executive","country":"PE","apps":["prospectador"]},
    {"id":"executive-ar","name":"Julián Medina","title":"Ejecutivo Comercial Argentina","role":"executive","country":"AR","apps":["prospectador"]},
    {"id":"executive-mx","name":"Adriana Montiel","title":"Ejecutiva Comercial México","role":"executive","country":"MX","apps":["prospectador"]},
    {"id":"regional","name":"Mariana Acosta","role":"regional","country":"CL"},
    {"id":"manager-cl","name":"Camila Valdés","role":"manager","country":"CL"},
    {"id":"executive-uy","name":"Diego Pereira","role":"executive","country":"UY"},
    {"id":"legal-pe","name":"Valentina Salazar","role":"legal","country":"PE"},
    {"id":"viewer-ar","name":"Martín Ferrer","role":"viewer","country":"AR"},
    {"id":"executive-cl","name":"Sofía Lagos","role":"executive","country":"CL"},
]
for profile in USERS:
    profile.setdefault("title", {"regional":"Dirección Regional","manager":"Jefatura Comercial","executive":"Ejecutivo Comercial","legal":"Asesora Legal","viewer":"Analista de Gestión"}.get(profile["role"],profile["role"]))
    profile.setdefault("apps", ["contratos"] if profile["role"]=="legal" else ["prospectador","contratos"])
OWNERS = {"CL":"executive-cl","UY":"executive-uy","PE":"legal-pe","AR":"viewer-ar","MX":"regional"}
STAMP = "2026-10-15T12:00:00+00:00"

def add(session, app, kind, id, **data):
    body = {"id":id,"created_at":STAMP, **data}
    session.add(Record(id=id,app=app,kind=kind,data=body))
    return body

def seed(session):
    sectors = ["Retail","Tecnología","Movilidad","Servicios financieros"]
    names = ["Horizonte","Prisma","Nexo","Origen"]
    contact_names = ["Elena Ríos","Tomás Vega","Lucía Montes","Bruno Sáez","Paula Lagos","Nicolás Paz","Clara Solís","Mateo Díaz"]
    for country in COUNTRIES:
        cc=country["code"]; owner=OWNERS[cc]
        for i in range(4):
            co=f"company-{cc}-{i}"
            add(session,"prospectador","companies",co,name=f"{names[i]} {cc}",domain=f"{names[i].lower()}-{cc.lower()}.example",sector=sectors[i],country=cc,owner_id=owner,status="activo",source="Datos sintéticos")
            for j in range(2):
                contact=f"contact-{cc}-{i}-{j}"
                status=["nuevo","contactado","respondió","reunión","propuesta","ganado","no_contactar","nuevo"][i*2+j]
                add(session,"prospectador","contacts",contact,name=contact_names[i*2+j],email=f"contacto{i}{j}@{names[i].lower()}-{cc.lower()}.example",title=["Directora de Marketing","Gerente Comercial"][j],phone="+00 000 000 000",company_id=co,company_name=f"{names[i]} {cc}",country=cc,owner_id=owner,status=status,excluded=status=="no_contactar",exclusion_reason="Preferencia del contacto (sintético)" if status=="no_contactar" else None,score=92-i*11-j*3,last_contact_at="2026-10-12T15:00:00+00:00",source="Importación demo")
            add(session,"prospectador","prospects",f"prospect-{cc}-{i}",name=f"{['Ana','Luis','Sara','Pedro'][i]} Ejemplo {cc}",email=f"prospecto{i}@empresa-{cc.lower()}.example",title="Responsable de Marca",company_name=f"Candidata {i+1} {cc}",sector=sectors[i],country=cc,owner_id=owner,status="pendiente",revealed=False,score=88-i*8,source="Lusha simulado",credit_cost=1)
        for i,status in enumerate(["borrador","aprobada","enviada"]):
            add(session,"prospectador","campaigns",f"campaign-{cc}-{i}",name=f"Circuito urbano {cc} · {['Diseño','Validación','Piloto'][i]}",country=cc,owner_id=owner,status=status,contact_ids=[f"contact-{cc}-0-0",f"contact-{cc}-1-0"],subject=f"Propuesta de visibilidad para {cc}",body="Demostración sintética: conversemos sobre espacios publicitarios y objetivos de marca.",approved_by="regional" if i else None,sent_count=2 if i==2 else 0,reply_count=1 if i==2 else 0,approval_note="Aprobación humana demo" if i else None)
        add(session,"prospectador","opportunities",f"opportunity-{cc}",name=f"Campaña regional {cc}",country=cc,owner_id=owner,company_id=f"company-{cc}-0",contact_id=f"contact-{cc}-0-0",amount=18000,currency="USD",status="propuesta",probability=60,expected_close="2026-11-30")
        add(session,"prospectador","activities",f"activity-{cc}",title="Reunión de descubrimiento",type="meeting",country=cc,owner_id=owner,contact_id=f"contact-{cc}-1-1",date="2026-10-20T15:00:00+00:00",status="programada",description="Reunión de descubrimiento del piloto")
        for i,status in enumerate(["borrador","en_revision","aprobado","pendiente_firma","activo"]):
            cid=f"contract-{cc}-{i}"
            add(session,"contratos","contracts",cid,title=f"{['Convenio comercial','Servicios de instalación','Arrendamiento soporte','Acuerdo de confidencialidad','Concesión publicitaria'][i]} · {cc}",name=f"Contrato {cc}-{100+i}",reference=f"VRT-{cc}-2026-{100+i}",country=cc,owner_id=owner,company=f"Vertia {cc}",counterparty=f"Contraparte {names[i%4]} {cc}",amount=25000+i*17500,currency="USD",type=["Comercial","Servicios","Arrendamiento","NDA","Concesión"][i],status=status,confidential=True,start_date="2026-10-01",end_date=f"2027-{(i%4)+1:02d}-28",version=1,documents=[{"id":f"doc-{cc}-{i}","filename":f"contrato_{cc.lower()}_{i}.pdf","kind":"contrato","version":1,"created_at":STAMP,"synthetic":True}],history=[{"status":status,"at":STAMP,"by":"regional","note":"Carga sintética inicial"}],analysis=None,redacted_ready=False,amendments=[],signature=None,template="Plantilla regional demo")
            for j in range(2):
                add(session,"contratos","obligations",f"obligation-{cc}-{i}-{j}",contract_id=cid,title=["Verificar póliza de responsabilidad","Revisar cumplimiento del hito"][j],country=cc,owner_id=owner,due_date=["2026-10-10","2026-11-15"][j],status="pendiente" if j==0 else "completada",evidence="Acta de revisión sintética" if j else None)
    add(session,"contratos","access_requests","access-demo",contract_id="contract-PE-4",country="PE",owner_id="executive-uy",requested_by="executive-uy",reason="Reutilizar antecedentes técnicos para licitación regional",status="pendiente",days=7)
    for app in ["prospectador","contratos"]:
        add(session,app,"audit",f"audit-seed-{app}",action="seed",title="Carga inicial de datos sintéticos",country="CL",owner_id="regional",actor="regional",detail="Demostración sin conexiones a proveedores externos")
