"""Apply Codex consistency review to the Claude Code commercial drafts."""
from pathlib import Path
import json, re
ROOT=Path(__file__).resolve().parents[1]
folder=ROOT/'docs/commercial'
limits={
'prospectador':'''## Condiciones propuestas para delimitar la entrega

El piloto y la consolidación incluidos contemplan hasta cinco ejecutivos, un tenant corporativo Microsoft 365, un proveedor de prospectos, tres secuencias de campaña configurables y una interfaz simple de intercambio con POST. Si existe una API documentada y autorizada, la interfaz incluye un flujo unidireccional de envío o actualización de gestiones con validación y registro de errores; no incluye sincronización bidireccional de todos los datos. Si la API no está disponible, se implementa importación y exportación de archivos validados y cualquier conector posterior se cotiza por separado.

La carga inicial propuesta contempla hasta 5.000 empresas y 10.000 contactos desde un formato de planilla acordado, con deduplicación y reporte de errores. Son límites de la migración y del acompañamiento inicial, no una licencia por registro ni un límite permanente de almacenamiento. Si la muestra requiere limpieza manual o cruce con fuentes adicionales se informa el diferencial antes de ejecutarlo.

Fase MVP de referencia: semanas 1 a 6. Consolidación, aceptación y publicación: semanas 7 a 10. Se configura el modelo para los cinco países; el piloto productivo es Uruguay. El despliegue masivo y la validación local del resto de los países forman parte de la ampliación regional, sin reconstruir el núcleo.

''',
'contratos':'''## Condiciones propuestas para delimitar la entrega

Se propone un piloto de hasta diez usuarios internos en un país designado por Vertia, con la configuración base de Argentina, Chile, Perú, México y Uruguay. La entrega cubre hasta seis categorías contractuales, cinco plantillas base y tres niveles secuenciales de aprobación por flujo, con asignación de responsables, plazos y registro de decisiones. No incluye un motor de reglas ilimitado ni asesoría jurídica para redactar las plantillas.

Se incluye una carga inicial de hasta 500 fichas desde una planilla estructurada y hasta 50 expedientes documentales del piloto para validar clasificación y metadata. No es un límite de almacenamiento ni una licencia por contrato. La digitalización masiva, corrección manual de archivos deteriorados y migraciones desde fuentes adicionales requieren una estimación previa. Para OCR e IA se valida una muestra acordada de hasta 100 páginas representativas; se registra precisión y tratamiento de excepciones, sin prometer extracción perfecta ni aprobación jurídica automática.

Se incluye una integración con un proveedor de firma documentado, con envío, consulta o recepción de estado y asociación del documento firmado. Los firmantes externos usan el servicio del proveedor; el costo por firma es de Vertia. Las obligaciones básicas contemplan responsable, fecha, estado y alerta. Los anexos se versionan y vinculan al expediente; automatizar enmiendas, renovaciones, escalamiento o conciliación con ERP pertenece al roadmap posterior.

MVP documental de referencia: semanas 1 a 7. Flujo, firma y validación: semanas 8 a 14. Aceptación, publicación y estabilización: semanas 15 a 16. La activación productiva masiva en otros países, su validación legal y la formación de equipos locales se cotizan como ampliación; la configuración regional base ya queda incluida.

'''}
for ident in limits:
    path=folder/f'{ident}.md';source=path.read_text(encoding='utf-8-sig')
    # Replace the primary title with a plain, specific subject.
    title='Propuesta comercial del Prospectador' if ident=='prospectador' else 'Propuesta comercial de Gestión Contractual'
    source=re.sub(r'^# .*', '# '+title,source,count=1)
    source=re.sub(r'\n## Condiciones propuestas para delimitar la entrega\n.*?(?=\n## |\Z)','\n',source,flags=re.S)
    match=re.search(r'\n## Fases[^\n]*',source)
    pos=match.start() if match else len(source)
    source=source[:pos]+'\n'+limits[ident]+source[pos:]
    source=source.replace('MoAI no contrata, paga ni administra licencias de terceros a nombre de Vertia.','Vertia conserva la titularidad y facturación de las licencias de terceros; MoAI configura los accesos técnicos autorizados dentro de la integración acordada.')
    source += '\n\n## Operación y ajustes durante el proyecto\n\nLos servicios de terceros los contrata y paga Vertia durante desarrollo, pruebas, aceptación y producción. El detalle de AWS, PostgreSQL, Claude Opus 5.5, OCR, prospectos y firma se entrega como anexo de requerimientos a cargo del cliente. No se incluyen sus cargos dentro de los honorarios MoAI.\n\nSe incorporan como anexos el protocolo de mantención y soporte y la matriz de roadmap. Toda publicación requiere pruebas, aceptación y una opción de recuperación. Los defectos del alcance aceptado se cubren por garantía; las mejoras se evalúan antes de ejecutarse. Una sustitución de esfuerzo equivalente puede acordarse por escrito antes de iniciar el trabajo. Si aumenta el esfuerzo, se comunica el diferencial de horas, precio y plazo para su aprobación previa.\n'
    path.write_text(source,encoding='utf-8')

path=folder/'scope-roadmap.json'; roadmap=json.loads(path.read_text(encoding='utf-8-sig'))
for item in roadmap.get('items',[]):
    if item['id']=='prospectador-fase-2-consolidacion':
        item['weeks']='7-10'
        item['deliverables']=[x.replace('Diseño y mapeo de una interfaz simple hacia POST','Diseño, mapeo e implementación de una interfaz simple unidireccional hacia POST') for x in item['deliverables']]
        item['acceptance']=[x for x in item['acceptance'] if 'aunque la conexión' not in x]+['Interfaz simple validada contra API de prueba o intercambio de archivos si no existe API autorizada']
    if item['id']=='contratos-obligaciones-enmiendas-renovaciones':
        item['title']='Automatización avanzada de obligaciones, enmiendas y renovaciones'
        item['deliverables']=['Escalamiento automático y evidencia de obligaciones; el registro básico de responsable, fecha, estado y alerta está incluido en la base','Enmiendas y renovaciones con flujo automatizado propio, además del registro documental incluido']
roadmap['scope_limits_proposed']={
 'prospectador':{'executives':5,'prospect_providers':1,'m365_tenants':1,'campaign_sequences':3,'initial_companies':5000,'initial_contacts':10000,'post_interfaces':1},
 'contratos':{'pilot_users':10,'pilot_countries':1,'regional_country_configuration':5,'contract_categories':6,'templates':5,'approval_levels':3,'initial_metadata_records':500,'initial_document_files':50,'ocr_validation_pages':100,'signature_providers':1}}
path.write_text(json.dumps(roadmap,ensure_ascii=False,indent=2),encoding='utf-8')
print('Commercial scope normalized; limits remain explicitly proposed.')
