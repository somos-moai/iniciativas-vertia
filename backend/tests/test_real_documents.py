"""Real bytes, actual PostgreSQL and actual local OCR, never a simulated reading."""
import io
import shutil
from pathlib import Path
import pytest
from backend.tests.test_integration import client,action,state

def real_pdf():
    from pypdf import PdfWriter
    from pypdf.generic import DictionaryObject,NameObject,DecodedStreamObject
    writer=PdfWriter()
    lines=["CONTRATO DE SERVICIOS PUBLICITARIOS", "Documento de prueba ficticio - no contiene datos reales", "Contraparte: Empresa Faro Ficticia SpA", "Monto total: USD 12,500.00", "Fecha de inicio: 2026-10-15", "Fecha de vencimiento: 2027-12-31", "Cuenta reservada: TEST-BANK-998811", "Las partes acuerdan un servicio de publicidad exterior."]
    page=writer.add_blank_page(width=595,height=842)
    font=DictionaryObject({NameObject('/Type'):NameObject('/Font'),NameObject('/Subtype'):NameObject('/Type1'),NameObject('/BaseFont'):NameObject('/Helvetica')})
    page[NameObject('/Resources')]=DictionaryObject({NameObject('/Font'):DictionaryObject({NameObject('/F1'):writer._add_object(font)})})
    stream=DecodedStreamObject()
    commands=['BT /F1 14 Tf 45 780 Td']
    for i,line in enumerate(lines):
        if i: commands.append('0 -27 Td')
        safe=line.replace('\\','\\\\').replace('(','\\(').replace(')','\\)')
        commands.append(f'({safe}) Tj')
    commands.append('ET'); stream.set_data('\n'.join(commands).encode('ascii'))
    page[NameObject('/Contents')]=writer._add_object(stream)
    buf=io.BytesIO(); writer.write(buf); return buf.getvalue()

def real_image():
    from PIL import Image,ImageDraw,ImageFont
    image=Image.new('RGB',(1600,1000),'white'); draw=ImageDraw.Draw(image)
    candidates=['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','C:/Windows/Fonts/arial.ttf']
    fontpath=next((p for p in candidates if Path(p).exists()),None)
    font=ImageFont.truetype(fontpath,38) if fontpath else ImageFont.load_default(size=38)
    lines=['CONTRATO DE ARRENDAMIENTO','Documento de prueba ficticio','Contraparte: Empresa Horizonte Ficticia','Monto total: USD 18000','Fecha de vencimiento: 2028-06-30','Uso exclusivo de pruebas de lectura OCR']
    for i,line in enumerate(lines): draw.text((65,90+i*105),line,fill='black',font=font)
    buf=io.BytesIO();image.save(buf,format='PNG');return buf.getvalue()

def create(client,country='CL'):
    return action(client,'contratos','create_contract',payload={'title':'Lectura real - documento de prueba','country':country,'company':'Sociedad ficticia QA','amount':0})['entity']['id']

def upload(client,cid,data,name='contrato.pdf',mime='application/pdf',user='regional'):
    return client.post(f'/api/contracts/{cid}/uploads',headers={'X-Demo-User':user},files={'file':(name,data,mime)},data={'kind':'contrato'})

def test_real_pdf_evidence_review_and_original_bytes(client,tmp_path,monkeypatch):
    monkeypatch.setenv('UPLOAD_DIR',str(tmp_path/'private'))
    cid=create(client); content=real_pdf(); r=upload(client,cid,content)
    assert r.status_code==200,r.text
    result=r.json(); doc=result['document']; analysis=result['entity']['analysis']
    assert doc['synthetic'] is False and doc['real'] is True
    assert analysis['simulated'] is False and analysis['ai_connected'] is False
    assert analysis['findings']==[] and analysis['score'] is None
    assert analysis['mode']=='local_extraction'
    proposals=analysis['proposed_fields']
    assert any(p['field']=='amount' and p['value']==12500 for p in proposals)
    assert any(p['field']=='end_date' and p['value']=='2027-12-31' for p in proposals)
    assert all(p['source_page']==1 and p['evidence'] for p in proposals)
    assert result['entity']['amount']==0 # no unreviewed overwrite
    text=client.get(f'/api/contracts/{cid}/uploads/{doc["id"]}/text').json()
    assert 'TEST-BANK-998811' in text['pages'][0]['text']
    assert text['pages'][0]['method']=='pdf_text'
    original=client.get(f'/api/contracts/{cid}/uploads/{doc["id"]}/original')
    assert original.content==content and original.headers['content-type']=='application/pdf'
    preview=client.get(f'/api/contracts/{cid}/uploads/{doc["id"]}/preview?page=1')
    assert preview.status_code==200 and preview.content.startswith(b'\x89PNG')
    reviewed=action(client,'contratos','review_extraction',cid,{'document_id':doc['id'],'fields':{'amount':12500,'currency':'USD','end_date':'2027-12-31'},'notes':'Verificado en página 1'})['entity']
    assert reviewed['amount']==12500 and reviewed['analysis']['reviewed_by']=='regional'
    rerun=action(client,'contratos','analyze_contract',cid)['entity']
    assert rerun['analysis']['simulated'] is False and rerun['analysis']['findings']==[]

def test_upload_acl_corrupt_empty_magic_and_size(client,tmp_path,monkeypatch):
    monkeypatch.setenv('UPLOAD_DIR',str(tmp_path/'private'))
    cid=create(client)
    assert upload(client,cid,real_pdf(),user='executive-uy').status_code==403
    assert upload(client,cid,b'').status_code==422
    assert upload(client,cid,b'%PDF-damaged-document').status_code==422
    assert upload(client,cid,real_pdf(),name='archivo.png').status_code==415
    huge=b'%PDF-'+b'x'*(15*1024*1024)
    assert upload(client,cid,huge).status_code==413
    assert not (next(c for c in state(client,'contratos')['contracts'] if c['id']==cid)['documents'])

def test_real_cross_country_sanitized_only_and_new_version_revokes(client,tmp_path,monkeypatch):
    monkeypatch.setenv('UPLOAD_DIR',str(tmp_path/'private'))
    cid=create(client,'MX'); first=upload(client,cid,real_pdf()).json(); did=first['document']['id']
    req=action(client,'contratos','request_access',cid,{'reason':'Revisión regional de antecedentes'},user='executive-uy')['entity']
    action(client,'contratos','grant_access',req['id'])
    headers={'X-Demo-User':'executive-uy'}
    for suffix in ['original','text','preview?page=1']:
        assert client.get(f'/api/contracts/{cid}/uploads/{did}/{suffix}',headers=headers).status_code==403
    assert client.get(f'/api/contracts/{cid}/document?redacted=false',headers=headers).status_code==403
    assert client.get(f'/api/contracts/{cid}/document?redacted=true',headers=headers).status_code==409
    limited=next(c for c in state(client,'contratos','executive-uy')['contracts'] if c['id']==cid)
    assert limited['access_scope']=='redacted_only' and limited['analysis'] is None
    assert 'amount' not in limited and not limited['documents']
    action(client,'contratos','redact_document',cid,expected=400)
    action(client,'contratos','redact_document',cid,{'safe_text':'Experiencia autorizada: ejecución de servicios publicitarios.','review_confirmed':True})
    safe=client.get(f'/api/contracts/{cid}/document?redacted=true',headers=headers)
    assert safe.status_code==200 and 'Experiencia autorizada' in safe.text and 'TEST-BANK' not in safe.text and '12,500' not in safe.text
    second=upload(client,cid,real_pdf()).json()
    assert second['document']['version']>first['document']['version']
    assert second['entity']['redacted_ready'] is False
    assert client.get(f'/api/contracts/{cid}/document?redacted=true',headers=headers).status_code==409

def test_real_image_ocr_no_fabricated_reading(client,tmp_path,monkeypatch):
    if not shutil.which('tesseract'): pytest.skip('Requiere Tesseract real spa+eng; ejecutar en VPS')
    monkeypatch.setenv('UPLOAD_DIR',str(tmp_path/'private'))
    cid=create(client); r=upload(client,cid,real_image(),name='foto-contrato.png',mime='image/png')
    assert r.status_code==200,r.text
    d=r.json()['document']; result=client.get(f'/api/contracts/{cid}/uploads/{d["id"]}/text').json()
    assert result['pages'][0]['method']=='ocr_tesseract'
    assert 'ARRENDAMIENTO' in result['pages'][0]['text'].upper()
    assert any(p['field']=='amount' and p['value']==18000 for p in result['proposed_fields'])
    assert any(p['field']=='end_date' and p['value']=='2028-06-30' for p in result['proposed_fields'])

def test_icp_transparent_matching_and_missing_evidence(client):
    action(client,'prospectador','save_icp',payload={'target_sectors':['Retail'],'countries':['UY'],'min_employees':100,'annual_budget_min':20000,'signals':['expansión'],'persona':'Directora de Marketing'},user='executive-uy')
    r=action(client,'prospectador','evaluate_company','company-UY-0',user='executive-uy')['entity']
    assert r['fit']['decision']=='informacion_insuficiente' and r['fit']['missing_fields']
    assert r['fit']['external_enrichment'] is False
    r=action(client,'prospectador','profile_company','company-UY-0',{'profile':{'employees':200,'annual_budget':35000,'budget_currency':'USD','signals':['expansión'],'offering':'Publicidad exterior'}},user='executive-uy')['entity']
    assert r['fit']['decision']=='priorizar' and r['fit']['score']==100 and r['fit']['coverage']==100
    assert r['fit']['ai_connected'] is False and any(s['source']=='ingreso manual confirmado por usuario' for s in r['fit']['sources'])
    removed=action(client,'prospectador','profile_company','company-UY-0',{'profile':{'employees':None}},user='executive-uy')['entity']
    assert removed['profile']['employees'] is None and 'Número de empleados' in removed['fit']['missing_fields']
    action(client,'prospectador','profile_company','company-CL-0',{'profile':{'employees':1}},user='executive-uy',expected=403)
    candidate=action(client,'prospectador','search_prospects',payload={'query':'Responsable de marketing','country':'UY','company_id':'company-UY-0'},user='executive-uy')['entity']
    revealed=action(client,'prospectador','reveal_contact',candidate['id'],user='executive-uy')['entity']
    contact=next(c for c in state(client,'prospectador','executive-uy')['contacts'] if c['id']==revealed['contact_id'])
    assert contact['company_id']=='company-UY-0'
    icp=state(client,'prospectador','executive-uy')['icp']
    campaign=action(client,'prospectador','create_campaign',payload={'name':'Selección con trazabilidad','contact_ids':[contact['id']],'qualification_note':'Cuenta elegida tras revisar criterios y faltantes','qualification_context':{'icp_id':icp['id']}},user='executive-uy')['entity']
    assert campaign['qualification_context']['criteria_snapshot']['version']==icp['version']
    assert campaign['qualification_context']['company_ids']==['company-UY-0']
    assert campaign['qualification_context']['selected_by']=='executive-uy'
