"""Dashboard aggregates with source ids and reproducible period filters."""
from collections import Counter, defaultdict
from calendar import monthrange
from datetime import date, timedelta
from .seed_v3 import FX

def timestamp(row):
    return str(row.get("sent_at") or row.get("date") or row.get("created_at") or "")[:10]

def usd(row):
    if row.get("amount_usd") is not None: return float(row["amount_usd"])
    amount=float(row.get("amount") or 0)
    return amount if row.get("currency")=="USD" else amount/FX.get(row.get("country"),1)

def delta(current,previous):
    return {"current":current,"previous":previous,"absolute":round(current-previous,2),"percent":round((current-previous)/previous*100,1) if previous else None}

def month_shift(d,months):
    value=d.year*12+d.month-1+months
    return date(value//12,value%12+1,1)

def summarize(out,start,end):
    def select(kind,test=lambda r:True):
        return [r for r in out.get(kind,[]) if start.isoformat()<=timestamp(r)<=end.isoformat() and test(r)]
    outbound=select("messages",lambda r:r.get("direction")=="outbound" and r.get("status") in {"simulado","enviado_simulado"})
    replies=select("messages",lambda r:r.get("direction")=="inbound" and r.get("classification","respuesta")=="respuesta")
    bounces=select("messages",lambda r:r.get("classification")=="rebote")
    meetings=select("activities",lambda r:r.get("type")=="meeting")
    opportunities=select("opportunities")
    return {"sent":len(outbound),"replies":len(replies),"bounces":len(bounces),"meetings":len(meetings),"opportunities":len(opportunities),"pipeline_usd":round(sum(usd(r) for r in opportunities if r.get("status") not in {"ganado","perdido"}),2),"won_usd":round(sum(usd(r) for r in opportunities if r.get("status")=="ganado"),2),"reply_rate":round(len(replies)/max(len(outbound),1)*100,1),"bounce_rate":round(len(bounces)/max(len(outbound),1)*100,1),"drilldown":{"sent":{"kind":"messages","ids":[r["id"] for r in outbound]},"replies":{"kind":"messages","ids":[r["id"] for r in replies]},"bounces":{"kind":"messages","ids":[r["id"] for r in bounces]},"meetings":{"kind":"activities","ids":[r["id"] for r in meetings]},"pipeline_usd":{"kind":"opportunities","ids":[r["id"] for r in opportunities if r.get("status") not in {"ganado","perdido"}]}},"start":start.isoformat(),"end":end.isoformat()}

def breakdown(rows,key):
    groups=defaultdict(list)
    for row in rows: groups[row.get(key) or "Sin clasificar"].append(row)
    return [{"id":value,"label":value,"count":len(items),"amount_usd":round(sum(usd(r) for r in items),2),"forecast_usd":round(sum(usd(r)*r.get("probability",0)/100 for r in items if r.get("status") not in {"ganado","perdido"}),2),"ids":[r["id"] for r in items]} for value,items in groups.items()]

def dashboard(out,application,period=None):
    anchor=date.fromisoformat(out.get("demo_as_of",date.today().isoformat()))
    try:
        selected=date.fromisoformat(period+"-01") if period and len(period)==7 else anchor.replace(day=1)
    except (ValueError,TypeError): selected=anchor.replace(day=1)
    end=min(month_shift(selected,1)-timedelta(days=1),anchor) if selected.year==anchor.year and selected.month==anchor.month else month_shift(selected,1)-timedelta(days=1)
    current=summarize(out,selected,end)
    prev_start=month_shift(selected,-1);previous=summarize(out,prev_start,date(prev_start.year,prev_start.month,min(end.day,monthrange(prev_start.year,prev_start.month)[1])))
    yoy_start=month_shift(selected,-12);yoy=summarize(out,yoy_start,date(yoy_start.year,yoy_start.month,min(end.day,monthrange(yoy_start.year,yoy_start.month)[1])))
    ytd=summarize(out,date(end.year,1,1),end)
    previous_ytd=summarize(out,date(end.year-1,1,1),date(end.year-1,end.month,min(end.day,monthrange(end.year-1,end.month)[1])))
    keys=["sent","replies","bounces","meetings","opportunities","pipeline_usd","won_usd"]
    comparisons={"mom":{k:delta(current[k],previous[k]) for k in keys},"yoy":{k:delta(current[k],yoy[k]) for k in keys},"ytd":{k:delta(ytd[k],previous_ytd[k]) for k in keys}}
    monthly=[]
    for offset in reversed(range(18)):
        start=month_shift(anchor,-offset);stop=min(month_shift(start,1)-timedelta(days=1),anchor)
        monthly.append({"month":start.strftime("%Y-%m"),**summarize(out,start,stop)})
    contacts=out.get("contacts",[]);opportunities=out.get("opportunities",[])
    stages=["nuevo","contactado","respondió","reunión","propuesta","ganado"]
    counts=Counter(c.get("status") for c in contacts)
    funnel=[]
    for i,status in enumerate(stages):
        ids=[r["id"] for r in contacts if r.get("status") in stages[i:]]
        funnel.append({"stage":status,"count":len(ids),"ids":ids,"conversion":round(len(ids)/max(funnel[-1]["count"],1)*100,1) if i else None,"definition":"Etapa alcanzada inferida del estado vigente; conversión acumulada respecto a la anterior"})
    campaigns=[]
    messages=out.get("messages",[]);activities=out.get("activities",[])
    for campaign in out.get("campaigns",[]):
        related=[m for m in messages if m.get("campaign_id")==campaign["id"]]
        sent=[m for m in related if m.get("direction")=="outbound" and m.get("status") in {"simulado","enviado_simulado"}]
        reply=[m for m in related if m.get("direction")=="inbound" and m.get("classification","respuesta")=="respuesta"]
        bounced=[m for m in related if m.get("classification")=="rebote"]
        meetings=[a for a in activities if a.get("campaign_id")==campaign["id"] and a.get("type")=="meeting"]
        campaigns.append({"id":campaign["id"],"name":campaign.get("name"),"sent":len(sent),"replies":len(reply),"bounces":len(bounced),"meetings":len(meetings),"reply_rate":round(len(reply)/max(len(sent),1)*100,1),"bounce_rate":round(len(bounced)/max(len(sent),1)*100,1),"message_ids":[r["id"] for r in related],"meeting_ids":[r["id"] for r in meetings]})
    contracts=[c for c in out.get("contracts",[]) if not c.get("restricted")]
    obligations=out.get("obligations",[])
    expiry={}
    for days in [30,60,90]:
        selected_contracts=[c for c in contracts if c.get("end_date") and anchor.isoformat()<=c["end_date"]<=(anchor+timedelta(days=days)).isoformat() and c.get("status") not in {"archivado","rechazado"}]
        expiry[str(days)]={"count":len(selected_contracts),"amount_usd":round(sum(usd(c) for c in selected_contracts),2),"ids":[c["id"] for c in selected_contracts]}
    cycle=defaultdict(list)
    cycle_ids=defaultdict(list)
    for contract in contracts:
        history=sorted(contract.get("history",[]),key=lambda r:r.get("at",""))
        for before,after in zip(history,history[1:]):
            try: days=(date.fromisoformat(after["at"][:10])-date.fromisoformat(before["at"][:10])).days
            except (ValueError,KeyError): continue
            if days>=0:
                cycle[before["status"]].append(days);cycle_ids[before["status"]].append(contract["id"])
    completed=[o for o in obligations if o.get("status")=="completada"]
    overdue=[o for o in obligations if o.get("status")!="completada" and o.get("due_date","9999")<anchor.isoformat()]
    risk=[c for c in contracts if c.get("end_date") and anchor.isoformat()<=c["end_date"]<=(anchor+timedelta(days=c.get("renewal_notice_days",60))).isoformat() and c.get("status") in {"activo","en_renovacion","firmado"}]
    clm={"value_usd":round(sum(usd(c) for c in contracts),2),"value_ids":[c["id"] for c in contracts],"by_status":breakdown(contracts,"status"),"by_country":breakdown(contracts,"country"),"by_type":breakdown(contracts,"type"),"expiring":expiry,"obligations":{"total":len(obligations),"completed":len(completed),"overdue":len(overdue),"compliance":round(len(completed)/max(len(obligations),1)*100,1),"completed_ids":[o["id"] for o in completed],"overdue_ids":[o["id"] for o in overdue]},"cycle_by_stage":[{"stage":stage,"average_days":round(sum(values)/len(values),1),"count":len(values),"ids":sorted(set(cycle_ids[stage]))} for stage,values in cycle.items()],"renewals_at_risk":{"count":len(risk),"ids":[c["id"] for c in risk]},"approval_bottlenecks":[{"id":c["id"],"title":c["title"],"status":c["status"],"days":max(0,(anchor-date.fromisoformat(c.get("history",[{}])[-1].get("at",c["created_at"])[:10])).days)} for c in contracts if c.get("status") in {"en_revision","pendiente_aprobacion"}]}
    # Legacy KPI names retained, values normalized instead of summing local currencies.
    if application=="prospectador":
        out["metrics"].update(pipeline=round(sum(usd(o) for o in opportunities if o.get("status") not in {"ganado","perdido"}),2),pipeline_value=round(sum(usd(o) for o in opportunities if o.get("status") not in {"ganado","perdido"}),2),forecast=round(sum(usd(o)*o.get("probability",0)/100 for o in opportunities if o.get("status") not in {"ganado","perdido"}),2),reporting_currency="USD")
    else: out["metrics"].update(contract_value=clm["value_usd"],reporting_currency="USD")
    return {"period":selected.strftime("%Y-%m"),"as_of":anchor.isoformat(),"current":current,"previous":previous,"yoy_previous":yoy,"ytd":ytd,"previous_ytd":previous_ytd,"comparisons":comparisons,"monthly":monthly,"funnel":funnel,"by_owner":breakdown(opportunities,"owner_id"),"by_country":breakdown(opportunities,"country"),"by_sector":breakdown(opportunities,"sector"),"campaign_performance":campaigns,"pipeline_usd":out["metrics"].get("pipeline",0),"forecast_usd":out["metrics"].get("forecast",0),"credits_results":{"credits_used":out.get("credits",{}).get("used",0),"contacts":len(contacts),"meetings":sum(a.get("type")=="meeting" for a in activities)},"clm":clm,"reporting_currency":"USD","fx_notice":"Equivalencias ilustrativas de demostración; monedas locales conservadas en cada registro","coverage":{"start":"2025-05-01","end":anchor.isoformat(),"previous_ytd_complete":False,"notice":"18 meses de historia; enero-abril del YTD anterior sin cobertura"}}
