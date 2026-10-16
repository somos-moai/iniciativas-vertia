"""v3 acceptance against the same disposable local PostgreSQL fixture as regression QA."""
from datetime import datetime, timedelta, timezone
import json
import pytest
from sqlalchemy import select, func
from backend.tests.test_integration import client, action, state

def test_v3_catalogue_realistic_and_traceable(client):
    s=state(client,"prospectador")
    assert len(s["companies"])>400 and len(s["contacts"])>1500
    assert len({c["country"] for c in s["companies"]})==5
    assert all(c["email"].endswith(".example") for c in s["contacts"])
    assert not any("ficticia" in c["name"].lower() for c in s["companies"])
    assert len(s["dashboard"]["monthly"])==18
    assert {"mom","yoy","ytd"}<=s["dashboard"]["comparisons"].keys()
    assert s["dashboard"]["coverage"]["previous_ytd_complete"] is False
    assert s["credits"]["organization"]["used"]==len(s["credit_history"])>0
    assert not any("identity" in row for row in s["credit_history"])
    current=s["dashboard"]["current"]
    ids=current["drilldown"]["sent"]["ids"]
    assert current["sent"]==len(ids)
    assert set(ids)<={m["id"] for m in s["messages"]}
    clm=state(client,"contratos")
    assert len(clm["contracts"])>200
    for days in ["30","60","90"]:
        entry=clm["dashboard"]["clm"]["expiring"][days]
        assert entry["count"]==len(entry["ids"])>0

def test_profiles_separated_and_named_acl(client):
    prospect=state(client,"prospectador","agustin-silva")
    assert prospect["viewer"]["name"]=="Agustín Silva"
    assert all(c["country"]=="UY" for c in prospect["contacts"])
    assert "gonzalo-oviedo" not in {u["id"] for u in prospect["users"]}
    clm=state(client,"contratos","gonzalo-oviedo")
    assert len({c["country"] for c in clm["contracts"]})==5
    assert all(not c["can_edit"] for c in clm["contracts"])
    assert next(u for u in clm["users"] if u["id"]=="phillipe")["name"]=="Phillipe"
    for person,application in [("gonzalo-oviedo","prospectador"),("santiago-ordonez","contratos"),("agustin-silva","contratos")]:
        assert client.get(f"/api/state?app={application}",headers={"X-Demo-User":person}).status_code==403
    for name in ["approve_contract","submit_review","grant_access"]:
        action(client,"contratos",name,"contract-CL-1",user="gonzalo-oviedo",expected=403)
    action(client,"prospectador","approve_campaign","campaign-UY-0",user="santiago-ordonez",expected=403)
    action(client,"prospectador","create_company",payload={"name":"Blocked","country":"UY"},user="santiago-ordonez",expected=403)

def test_manager_approval_and_superadmin_country_scope(client):
    campaign=action(client,"prospectador","create_campaign",payload={"name":"Piloto Uruguay","contact_ids":["contact-UY-0-0"]},user="executive-uy")["entity"]
    action(client,"prospectador","approve_campaign",campaign["id"],user="agustin-silva")
    action(client,"prospectador","approve_campaign","campaign-CL-0",user="agustin-silva",expected=403)
    created=action(client,"prospectador","create_company",payload={"name":"Cendal del Mirador","domain":"mirador.example","country":"MX"},user="enrique-escobar")["entity"]
    assert created["country"]=="MX"

def test_opportunity_status_only_persists_history_and_forecast(client):
    before=next(o for o in state(client,"prospectador","executive-uy")["opportunities"] if o["id"]=="opportunity-UY")
    changed=action(client,"prospectador","set_opportunity","opportunity-UY",{"status":"negociacion"},user="executive-uy")["entity"]
    assert changed["amount"]==before["amount"] and changed["probability"]==80
    assert changed["history"][-1]["from"]=="propuesta"
    after=next(o for o in state(client,"prospectador","executive-uy")["opportunities"] if o["id"]=="opportunity-UY")
    assert after["status"]=="negociacion" and after["history"]==changed["history"]
    assert any(a["action"]=="set_opportunity" and a["entity_id"]==after["id"] for a in state(client,"prospectador","executive-uy")["audit"])

def test_bulk_reveal_preview_no_cost_and_no_duplicate_payment(client):
    ids=["v3-prospect-UY-001-0","v3-prospect-UY-001-1"]
    before=state(client,"prospectador","executive-uy")["credits"]["used"]
    preview=action(client,"prospectador","preview_reveal",payload={"prospect_ids":ids,"run_id":"qa-bulk"},user="executive-uy")["entity"]
    assert preview["cost"]==2 and preview["allowed"]
    assert state(client,"prospectador","executive-uy")["credits"]["used"]==before
    result=action(client,"prospectador","reveal_contacts",payload={"prospect_ids":ids,"run_id":"qa-bulk"},user="executive-uy")["entity"]
    assert result["cost"]==2 and result["revealed_count"]==2
    duplicate=action(client,"prospectador","reveal_contacts",payload={"prospect_ids":ids,"run_id":"qa-bulk"},user="executive-uy")["entity"]
    assert duplicate["cost"]==0 and duplicate["duplicates"]==2
    assert state(client,"prospectador","executive-uy")["credits"]["used"]==before+2

def test_search_filters_masking_and_429_retry(client):
    candidate=action(client,"prospectador","search_prospects",payload={"country":"UY","company_id":"company-UY-0","query":"Marketing"},user="executive-uy")["entity"]
    assert candidate["email"] is None and candidate["email_masked"]
    assert candidate["company_id"]=="company-UY-0"
    result=action(client,"prospectador","search_prospects",payload={"country":"UY","department":"Marketing","seniority":"gerencia","sector":"Retail"},user="executive-uy")["entity"]
    assert result.get("email") is None
    response=client.post("/api/actions",headers={"X-Demo-User":"executive-uy"},json={"app":"prospectador","action":"search_prospects","payload":{"country":"UY","simulate_429":True}})
    assert response.status_code==429 and int(response.headers["Retry-After"])>0
    assert response.json()["detail"]["retry_after"]>0

def test_credit_wallet_and_run_caps_enforced(client):
    from backend import main
    with main.app.state.sessions() as s:
        main.new(s,"prospectador","credit_ledger",country="UY",owner_id="executive-uy",portfolio_id="executive-uy",run_id="qa-full-run",prospect_ids=[],identity="qa-already@data.example",cost=600)
        s.commit()
    action(client,"prospectador","preview_reveal",payload={"prospect_ids":["v3-prospect-UY-002-0"],"run_id":"qa-full-run"},user="executive-uy",expected=409)
    action(client,"prospectador","configure_credits",payload={"organization_limit":7500,"wallet_limits":{"executive-uy":0}},user="enrique-escobar")
    action(client,"prospectador","reveal_contact","v3-prospect-UY-002-0",user="executive-uy",expected=409)
    action(client,"prospectador","configure_credits",payload={"organization_limit":7500,"wallet_limits":{"executive-uy":1250}},user="enrique-escobar")
    action(client,"prospectador","configure_credits",payload={},user="agustin-silva",expected=403)

def test_mail_draft_queue_cooldown_sequence_and_exclusion(client):
    user="executive-uy";cid="contact-UY-1-1"
    draft=action(client,"prospectador","draft_email",cid,user=user)["entity"]
    assert "¿Te viene bien" in draft["body"] and draft["requires_human_review"]
    sequence=action(client,"prospectador","save_sequence",payload={"contact_id":cid,"steps":[{"delay_days":7,"subject":"Seguimiento","body":"¿Conversamos?"}]},user=user)["entity"]
    action(client,"prospectador","simulate_sequence",sequence["id"],user=user)
    queued=action(client,"prospectador","send_email",cid,{"subject":"Propuesta editada","body":"¿Coordinamos el jueves?"},user=user)["entity"]
    assert queued["status"]=="programado" and queued["external_delivery"] is False
    local=datetime.fromisoformat(queued["scheduled_at"]).astimezone(__import__('zoneinfo').ZoneInfo("America/Montevideo"))
    assert 8<=local.hour<20
    action(client,"prospectador","exclude_contact",cid,user=user)
    s=state(client,"prospectador",user)
    assert next(m for m in s["messages"] if m["id"]==queued["id"])["status"]=="cancelado"
    action(client,"prospectador","send_email",cid,{"subject":"Blocked","body":"No sale"},user=user,expected=409)
    action(client,"prospectador","save_sequence",payload={"contact_id":"contact-UY-0-1","steps":[{"delay_days":1}]},user=user,expected=400)

def test_inbox_classifies_and_respects_ten_minute_poll(client):
    result=action(client,"prospectador","poll_inbox",payload={"contact_id":"contact-UY-0-1","classification":"no_contactar"},user="executive-uy")["entity"]
    assert result["processed"]==1
    again=action(client,"prospectador","poll_inbox",user="executive-uy")["entity"]
    assert again["status"]=="espera" and again["processed"]==0
    s=state(client,"prospectador","executive-uy")
    assert next(c for c in s["contacts"] if c["id"]=="contact-UY-0-1")["excluded"]
    assert any(m.get("classification")=="no_contactar" for m in s["messages"])
    assert any(t["messages"] for t in s["inbox"])

def test_clm_configuration_snapshot_and_ia_pause(client):
    cfg={"name":"Flujo del piloto","types":["Comercial","NDA"],"templates":[{"name":"Base comercial","type":"Comercial","body":"Cláusulas para revisión humana"}],"approval_flows":[{"name":"Revisión regional","steps":["Legal","Regional"]}],"reminder_days":[90,60,30]}
    settings=action(client,"contratos","save_clm_settings",payload=cfg,user="gonzalo-oviedo")["entity"]
    contract=action(client,"contratos","create_contract",payload={"title":"Convenio del piloto","company":"Vertia Uruguay","country":"UY","type":"Comercial"},user="phillipe")["entity"]
    assert contract["configuration_version"]==settings["version"]
    assert contract["template"]["name"]=="Base comercial" and contract["approval_flow"]["steps"]==["Legal","Regional"]
    action(client,"prospectador","save_ai_settings",payload={"tone":"Formal","daily_budget":50,"enabled":False},user="santiago-ordonez")
    action(client,"prospectador","draft_email","contact-UY-1-1",user="executive-uy",expected=409)
    action(client,"prospectador","save_ai_settings",payload={"tone":"Formal","daily_budget":50,"enabled":True},user="santiago-ordonez")
    draft=action(client,"prospectador","draft_email","contact-UY-1-1",user="executive-uy")["entity"]
    assert draft["body"].startswith("Estimado/a") and draft["configuration_version"]

def test_additive_seed_rerun_preserves_user_records_and_uploads(client):
    from backend import main
    from backend.seed_v3 import seed_v3
    from backend.db import Record,DocumentUpload
    with main.app.state.sessions() as s:
        main.new(s,"contratos","contracts",id="private-migration-case",country="CL",owner_id="regional",title="Expediente privado",has_real_uploads=True,documents=[{"id":"private-upload-case","version":1}])
        upload=DocumentUpload(id="private-upload-case",contract_id="private-migration-case",filename="privado.pdf",content_type="application/pdf",storage_key="d"*32,sha256="a"*64,size_bytes=120,version=1,status="procesado",extraction={"text_preview":"Contenido privado preservado"},uploaded_by="regional")
        s.add(upload);s.commit()
        before=s.scalar(select(func.count()).select_from(Record))
        expected=dict(s.get(Record,"private-migration-case").data)
        seed_v3(s);s.commit()
        assert s.scalar(select(func.count()).select_from(Record))==before
        assert s.get(Record,"private-migration-case").data==expected
        assert s.get(DocumentUpload,"private-upload-case").extraction=={"text_preview":"Contenido privado preservado"}

def test_cross_portfolio_dedup_does_not_disclose_foreign_contact(client):
    from backend import main
    from backend.db import Record
    with main.app.state.sessions() as s:
        foreign=s.get(Record,"contact-UY-1-0")
        candidate=main.new(s,"prospectador","prospects",name="Referente de Chile",email=foreign.data["email"],title="Gerente de Marketing",country="CL",owner_id="executive-cl",company_id="company-CL-0",company_name="Horizonte CL",revealed=False,status="pendiente")
        cid=candidate.id;s.commit()
    preview=action(client,"prospectador","preview_reveal",payload={"prospect_ids":[cid]},user="executive-cl")["entity"]
    assert preview["cost"]==0 and preview["duplicates"]==1
    own=action(client,"prospectador","reveal_contact",cid,user="executive-cl")["entity"]
    assert own["contact_id"]!="contact-UY-1-0"
    visible=state(client,"prospectador","executive-cl")
    contact=next(c for c in visible["contacts"] if c["id"]==own["contact_id"])
    assert contact["name"]=="Referente de Chile" and contact["owner_id"]=="executive-cl"
    assert not any(c["id"]=="contact-UY-1-0" for c in visible["contacts"])


def test_provider_minute_limit_is_real_and_atomic(client):
    from backend import main
    from backend.commercial import RATE_LIMITS
    # Fill only this disposable test schema's provider window, never a production DB.
    with main.app.state.sessions() as s:
        for i in range(RATE_LIMITS["minute"]):
            main.new(s,"prospectador","provider_queries",country="UY",owner_id="executive-uy",operation="search",provider="Lusha simulado")
        s.commit()
    response=client.post("/api/actions",headers={"X-Demo-User":"executive-uy"},json={"app":"prospectador","action":"search_prospects","payload":{"country":"UY"}})
    assert response.status_code==429 and response.json()["detail"]["retry_after"]>0

@pytest.mark.parametrize("window,count,age",[("hour",150,120),("day",1500,7200)])
def test_each_provider_rate_window(monkeypatch,window,count,age):
    from backend import main
    from backend import commercial
    from fastapi import HTTPException
    current=datetime.now(timezone.utc)
    events=[main.Record(id=f"rate-case-{i}",app="prospectador",kind="provider_queries",data={"created_at":(current-timedelta(seconds=age)).isoformat()}) for i in range(count)]
    monkeypatch.setattr(main,"records",lambda *args:events)
    monkeypatch.setattr(commercial,"lock",lambda *args:None)
    with pytest.raises(HTTPException) as error:
        commercial.rate_check(None,{"id":"executive-uy","country":"UY"},"search")
    assert error.value.status_code==429
    assert window in error.value.detail["message"]
    assert int(error.value.headers["Retry-After"])>0



def test_read_only_profiles_can_request_access_but_not_edit(client):
    # Regresión: el bloqueo de edición impedía solicitar acceso a perfiles de consulta.
    target=next(c for c in state(client,"contratos")["contracts"] if c["country"]=="PE")
    action(client,"contratos","request_access",target["id"],{"reason":"Consulta regional de antecedente"},user="viewer-ar")
    denied=client.post("/api/actions",headers={"X-Demo-User":"viewer-ar"},json={"app":"contratos","action":"create_contract","entity_id":None,"payload":{"title":"No permitido","country":"AR"}})
    assert denied.status_code==403 and "consulta" in denied.json()["detail"]
    innovation=client.post("/api/actions",headers={"X-Demo-User":"gonzalo-oviedo"},json={"app":"contratos","action":"create_contract","entity_id":None,"payload":{"title":"No permitido","country":"CL"}})
    assert innovation.status_code==403
