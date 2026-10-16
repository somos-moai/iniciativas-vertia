"""Transparent local ICP profiling. No external enrichment or invented firmographics."""
from datetime import datetime, timezone

def profile_action(s,user,a):
    from . import main as api
    if user["role"] in {"viewer","legal"}: api.fail("Este perfil no puede modificar el perfilamiento comercial",403)
    p=a.payload
    if a.action=="save_icp":
        countries=p.get("countries",[])
        sectors=p.get("target_sectors",[])
        for values in [countries,sectors,p.get("signals",[]),p.get("exclusions",[])]:
            if not isinstance(values,list) or len(values)>30 or not all(isinstance(v,str) and len(v)<=200 for v in values): api.fail("Los criterios deben contener listas de texto válidas")
        if set(countries)-{c["code"] for c in api.COUNTRIES}: api.fail("País objetivo inválido")
        data={"name":p.get("name","Perfil de cliente ideal"),"country":user["country"],"owner_id":user["id"],"target_sectors":sectors,"countries":countries,"signals":p.get("signals",[]),"exclusions":p.get("exclusions",[]),"persona":str(p.get("persona",""))[:500],"offering":str(p.get("offering",""))[:1000],"ideal_customer":str(p.get("ideal_customer",""))[:1000],"status":"activo","source":"criterios ingresados por usuario"}
        for key in ["min_employees","max_employees","annual_budget_min"]:
            value=p.get(key)
            if value is None or value=="": data[key]=None
            else:
                try: number=float(value)
                except (TypeError,ValueError): api.fail(f"Criterio {key} inválido")
                if not 0<=number<=1e12: api.fail(f"Criterio {key} fuera de rango")
                data[key]=number
        if data["min_employees"] is not None and data["max_employees"] is not None and data["min_employees"]>data["max_employees"]: api.fail("El mínimo de empleados excede el máximo")
        previous=[r for r in api.records(s,a.app,"icp_profiles") if r.data.get("owner_id")==user["id"]]
        version=max([r.data.get("version",0) for r in previous],default=0)+1
        for row in previous: api.save(s,row,status="historico")
        return api.new(s,a.app,"icp_profiles",**data,version=version)
    company=api.get(s,a.app,"companies",a.entity_id)
    api.write(s,user,company)
    data=company.data
    profile=dict(data.get("profile") or {})
    accepted={"industry","offering","ideal_customer","employees","annual_budget","budget_currency","website_notes","persona","signals","exclusions"}
    supplied=p.get("profile",p.get("fields",{}))
    if a.action=="profile_company" and not supplied:
        supplied={k:v for k,v in p.items() if k in accepted}
    if not isinstance(supplied,dict) or set(supplied)-accepted: api.fail("Campos de perfil no permitidos")
    for key,value in supplied.items():
        if key in {"employees","annual_budget"}:
            if value is None or value=="":
                profile[key]=None
                continue
            try: number=float(value)
            except (TypeError,ValueError): api.fail(f"Campo {key} debe ser numérico")
            if not 0<=number<=1e12: api.fail(f"Campo {key} fuera de rango")
            profile[key]=number
        elif key in {"signals","exclusions"}:
            if not isinstance(value,list) or len(value)>30 or not all(isinstance(v,str) and len(v)<=200 for v in value): api.fail(f"Campo {key} debe ser una lista de texto")
            profile[key]=value
        else:
            if not isinstance(value,str) or len(value)>2000: api.fail(f"Campo {key} inválido")
            profile[key]=value.strip()
    icps=[r.data for r in api.records(s,a.app,"icp_profiles") if r.data.get("status")=="activo" and api.allowed(s,user,r)]
    icp=next((c for c in icps if c["owner_id"]==user["id"]),icps[-1] if icps else {})
    criteria=p.get("criteria",icp)
    if not isinstance(criteria,dict): api.fail("Criterios inválidos")
    criteria=dict(criteria)
    for key in ["target_sectors","countries","signals","exclusions"]:
        values=criteria.get(key,[])
        if not isinstance(values,list) or len(values)>30 or not all(isinstance(v,str) for v in values): api.fail(f"Criterio {key} inválido")
    for key in ["min_employees","max_employees","annual_budget_min"]:
        if criteria.get(key) is not None:
            try: number=float(criteria[key])
            except (TypeError,ValueError): api.fail(f"Criterio {key} inválido")
            if not 0<=number<=1e12: api.fail(f"Criterio {key} fuera de rango")
            criteria[key]=number
    reasons=[]; missing=[]; matches=0; evaluated=0; configured=0; excluded=False
    sources=[{"field":"sector","source":"fixture sintético" if data.get("id","").startswith("company-") and len(data["id"])<20 else "ingreso manual","value":data.get("sector"),"evidence":f"Campo sector: {data.get('sector','sin dato')}"},{"field":"country","source":"registro de cartera","value":data["country"],"evidence":f"País declarado: {data['country']}"}]
    def evaluate(label,value,valid,required=True):
        nonlocal matches,evaluated,configured
        configured+=1
        if value is None or value=="" or value==[]:
            missing.append(label); reasons.append(f"{label}: falta evidencia; no se puntúa")
            return
        evaluated+=1
        if valid(value): matches+=1; reasons.append(f"{label}: coincide con el criterio declarado")
        else: reasons.append(f"{label}: no coincide con el criterio declarado")
    sectors=criteria.get("target_sectors",[])
    if sectors: evaluate("Sector",profile.get("industry") or data.get("sector"),lambda value:value.lower() in {v.lower() for v in sectors})
    countries=criteria.get("countries",[])
    if countries: evaluate("País",data["country"],lambda value:value in countries)
    minimum=criteria.get("min_employees"); maximum=criteria.get("max_employees")
    if minimum is not None or maximum is not None:
        evaluate("Número de empleados",profile.get("employees"),lambda value:(minimum is None or value>=minimum) and (maximum is None or value<=maximum))
    budget=criteria.get("annual_budget_min")
    if budget is not None:
        if profile.get("budget_currency")!="USD":
            configured+=1; missing.append("Presupuesto anual confirmado en USD"); reasons.append("Presupuesto: no se convierte ni infiere una moneda desconocida")
        else: evaluate("Presupuesto anual USD",profile.get("annual_budget"),lambda value:value>=budget)
    desired=criteria.get("signals",[])
    if desired: evaluate("Señales comerciales",profile.get("signals"),lambda value:bool({v.lower() for v in value}&{v.lower() for v in desired}))
    exclusions=criteria.get("exclusions",[])
    if exclusions and profile.get("exclusions"):
        hit={v.lower() for v in exclusions}&{v.lower() for v in profile["exclusions"]}
        excluded=bool(hit)
        if excluded: reasons.append("Exclusión declarada coincidente: "+", ".join(sorted(hit)))
    field_sources=dict(profile.get("field_sources") or {})
    for field in supplied:
        field_sources[field]={"recorded_by":user["id"],"recorded_at":api.now()}
    profile["field_sources"]=field_sources
    for field,origin in field_sources.items():
        sources.append({"field":field,"source":"ingreso manual confirmado por usuario","value":profile.get(field),"evidence":"Dato aportado o retirado en formulario; sin verificación externa",**origin})
    score=round(matches/evaluated*100) if evaluated else None
    decision="excluida" if excluded else "sin_criterios" if not configured else "informacion_insuficiente" if missing else "priorizar" if score is not None and score>=75 else "revisar" if score is not None and score>=50 else "baja_afinidad"
    fit={"score":score,"score_type":"porcentaje de criterios comprobables coincidentes; no probabilidad de venta","decision":decision,"reasons":reasons or ["Defina criterios ICP para evaluar esta empresa"],"missing_fields":missing,"criteria_version":criteria.get("version"),"criteria_id":criteria.get("id"),"criteria_evaluated":evaluated,"criteria_configured":configured,"coverage":round(evaluated/max(configured,1)*100),"sources":sources,"evaluated_at":api.now(),"method":"reglas locales transparentes","ai_connected":False,"external_enrichment":False}
    profile.update({"updated_by":user["id"],"updated_at":api.now(),"source":"datos declarados; sin enriquecimiento externo"})
    if a.action=="enrich_company": fit["notice"]="Sin API externa conectada: se evaluaron únicamente datos existentes. Complete los campos faltantes."
    api.save(s,company,profile=profile,fit=fit)
    return company
