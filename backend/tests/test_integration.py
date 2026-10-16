"""Actual PostgreSQL integration tests; no database mocks or SQLite fallback.

TEST_DATABASE_URL is mandatory to run. Tests create/drop only their own random schema.
"""
import os
from uuid import uuid4
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text

@pytest.fixture(scope="module")
def client():
    url=os.environ.get("TEST_DATABASE_URL")
    if not url:
        pytest.skip("TEST_DATABASE_URL no configurada: se requiere PostgreSQL real")
    if not url.startswith(("postgresql://","postgresql+psycopg://")):
        raise RuntimeError("Las pruebas requieren PostgreSQL real")
    url=url.replace("postgresql://","postgresql+psycopg://",1)
    schema="vertia_test_"+uuid4().hex
    admin=create_engine(url)
    with admin.begin() as c: c.execute(text(f'CREATE SCHEMA "{schema}"'))
    engine=create_engine(url,connect_args={"options":f"-csearch_path={schema}"})
    from backend import main
    original=main.make_engine
    main.make_engine=lambda:engine
    try:
        with TestClient(main.app) as c:
            yield c
    finally:
        main.make_engine=original
        engine.dispose()
        with admin.begin() as c: c.execute(text(f'DROP SCHEMA "{schema}" CASCADE'))
        admin.dispose()

def state(c,application,user="regional"):
    r=c.get("/api/state",params={"app":application},headers={"X-Demo-User":user})
    assert r.status_code==200,r.text
    return r.json()

def action(c,application,name,id=None,payload=None,user="regional",expected=200):
    r=c.post("/api/actions",headers={"X-Demo-User":user},json={"app":application,"action":name,"entity_id":id,"payload":payload or {}})
    assert r.status_code==expected,r.text
    return r.json()

def test_health_real_postgres_and_seed(client):
    assert client.get("/api/health").json()["database"]=="postgresql"
    s=state(client,"contratos")
    assert len(s["contracts"])==25
    assert len(s["countries"])==5
    assert all(i["status"]=="simulado" for i in s["integrations"] if i["name"] not in {"PostgreSQL","OCR local"})

def test_country_owner_acl_and_invalid_profile(client):
    s=state(client,"prospectador","executive-uy")
    assert len(s["contacts"])==8
    assert all(c["country"]=="UY" and c["owner_id"]=="executive-uy" for c in s["contacts"])
    assert client.get("/api/state?app=contratos",headers={"X-Demo-User":"admin"}).status_code==401
    action(client,"prospectador","exclude_contact","contact-CL-0-0",user="executive-uy",expected=403)
    action(client,"contratos","create_contract",payload={"title":"Prohibido","country":"CL"},user="executive-uy",expected=403)

def test_readonly_profile_and_catalog_redaction(client):
    s=state(client,"contratos","viewer-ar")
    foreign=next(c for c in s["contracts"] if c["country"]=="PE")
    assert foreign["restricted"] and "amount" not in foreign and "company" not in foreign
    assert client.get("/api/contracts/contract-PE-0/document?redacted=false",headers={"X-Demo-User":"viewer-ar"}).status_code==403
    action(client,"contratos","upload_document","contract-AR-0",{"filename":"x.pdf"},user="viewer-ar",expected=403)

def test_human_approval_exclusion_and_no_duplicate_send(client):
    campaign=action(client,"prospectador","create_campaign",payload={"name":"Prueba aprobación","contact_ids":["contact-UY-0-0"]},user="executive-uy")["entity"]
    cid=campaign["id"]
    action(client,"prospectador","draft_campaign",cid,user="executive-uy")
    action(client,"prospectador","send_campaign",cid,user="executive-uy",expected=409)
    action(client,"prospectador","approve_campaign",cid,user="executive-uy",expected=403)
    action(client,"prospectador","approve_campaign",cid)
    action(client,"prospectador","send_campaign",cid,user="executive-uy")
    action(client,"prospectador","send_campaign",cid,user="executive-uy",expected=409)
    action(client,"prospectador","receive_reply","contact-UY-0-0",user="executive-uy")
    msgs=state(client,"prospectador","executive-uy")["messages"]
    assert any(m.get("direction")=="outbound" and m["followup_status"]=="cancelado" for m in msgs)
    action(client,"prospectador","exclude_contact","contact-UY-0-0",user="executive-uy")
    action(client,"prospectador","create_campaign",payload={"name":"Bloqueo","contact_ids":["contact-UY-0-0"]},user="executive-uy",expected=409)

def test_reveal_credits_and_deduplication(client):
    before=state(client,"prospectador","executive-uy")
    action(client,"prospectador","reveal_contact","prospect-UY-0",user="executive-uy")
    action(client,"prospectador","reveal_contact","prospect-UY-0",user="executive-uy",expected=409)
    after=state(client,"prospectador","executive-uy")
    assert len(after["contacts"])==len(before["contacts"])+1
    assert after["credits"]["used"]==before["credits"]["used"]+1

def test_contract_complete_lifecycle_and_analysis(client):
    c=action(client,"contratos","create_contract",payload={"title":"Contrato prueba de ciclo","country":"CL","amount":123456,"company":"Sociedad prueba ficticia"})["entity"]
    cid=c["id"]
    action(client,"contratos","activate_contract",cid,expected=409)
    action(client,"contratos","submit_review",cid,expected=409)
    action(client,"contratos","upload_document",cid,{"filename":"documento.pdf"})
    r=action(client,"contratos","analyze_contract",cid)["entity"]
    assert r["analysis"]["simulated"] and r["analysis"]["findings"]
    for name in ["submit_review","approve_contract","send_signature","sign_contract","activate_contract"]:
        r=action(client,"contratos",name,cid)["entity"]
    assert r["status"]=="activo"
    assert not r["signature"]["legal_signature"]
    action(client,"contratos","add_obligation",cid,{"title":"Entregar acta","due_date":"2027-01-15"})
    action(client,"contratos","add_amendment",cid,{"title":"Ampliación de soporte"})
    r=action(client,"contratos","renew_contract",cid,{"end_date":"2029-12-31"})["entity"]
    assert r["status"]=="en_renovacion" and len(r["amendments"])==1

def test_sanitized_document_excludes_original_not_hidden(client):
    cid="contract-CL-2"
    action(client,"contratos","redact_document",cid)
    safe=client.get(f"/api/contracts/{cid}/document?redacted=true")
    original=client.get(f"/api/contracts/{cid}/document?redacted=false")
    assert safe.status_code==200 and original.status_code==200
    for secret in ["DEMO-IBAN-99887766","DEMO-TAX-11223344","descuento privado","60000"]:
        assert secret in original.text
        assert secret not in safe.text
    assert "COPIA SANEADA" in safe.text

def test_cross_country_request_grant_read_not_edit(client):
    req=action(client,"contratos","request_access","contract-MX-2",{"reason":"Antecedentes de licitación"},user="executive-uy")["entity"]
    action(client,"contratos","grant_access",req["id"],user="executive-uy",expected=403)
    action(client,"contratos","grant_access",req["id"],{"days":7})
    visible=next(c for c in state(client,"contratos","executive-uy")["contracts"] if c["id"]=="contract-MX-2")
    assert visible["can_access"] and not visible["can_edit"]
    action(client,"contratos","analyze_contract","contract-MX-2",user="executive-uy",expected=403)

def test_exports_are_acl_filtered_and_formula_safe(client):
    r=client.get("/api/export?app=prospectador",headers={"X-Demo-User":"executive-uy"})
    assert r.status_code==200 and "contact-UY" in r.text and "contact-CL" not in r.text
    co=action(client,"prospectador","create_company",payload={"name":"Empresa fórmula","domain":"formula.example","country":"CL"})["entity"]
    action(client,"prospectador","create_contact",payload={"name":"=HYPERLINK(test)","email":"formula@formula.example","company_id":co["id"],"country":"CL"})
    assert "'=HYPERLINK" in client.get("/api/export?app=prospectador").text

def test_no_real_email_allowed_and_changes_persist(client):
    action(client,"prospectador","create_contact",payload={"name":"Bloqueado","email":"someone@gmail.com","company_id":"company-UY-0","country":"UY"},user="executive-uy",expected=400)
    s1=state(client,"prospectador","executive-uy")
    s2=state(client,"prospectador","executive-uy")
    assert s1["contacts"]==s2["contacts"]
