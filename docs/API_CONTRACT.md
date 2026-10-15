# Contrato de integración demo v1

Frontend en / con rutas /prospectador y /contratos. API bajo /api. Nginx proxy /api a FastAPI. frontend usa fetch y cabecera X-Demo-User con el id de perfil seleccionado, guardado en localStorage; selector explícito de demostración. No es autenticación productiva. Backend aplica visibilidad y permisos a cada lectura/acción.

GET /api/health -> {status, database, mode:"synthetic"}.
GET /api/state?app=prospectador|contratos -> objeto de estado abajo. GET inicial sin cabecera usa usuario regional de demostración.
POST /api/actions -> {app, action, entity_id:null|string, payload:{...}}; respuesta {ok:true,message,entity?,state?}. Frontend debe refrescar GET /api/state tras cada acción. Errores JSON detail con status HTTP adecuado. Backend no exige que el frontend entienda estados internos.
GET /api/export?app=prospectador|contratos -> CSV UTF8 limitado a permisos.
GET /api/contracts/{id}/document?redacted=true -> representación HTML descargable del documento sintético saneado. Original solo si hay acceso autorizado. No meter texto original en la respuesta saneada.

Estado retornado siempre incluye:
{viewer:{id,name,role,country}, users:[{id,name,role,country}], countries:[{code,name,currency}], metrics:{...}, companies:[], contacts:[], campaigns:[], activities:[], opportunities:[], prospects:[], messages:[], contracts:[], access_requests:[], obligations:[], audit:[], notifications:[], roadmap:[], integrations:[], credits:{used,limit}, generated_at}.

Toda entidad tiene id. Fechas ISO. Campos comunes name/title/status/country/owner_id/created_at. Se pueden añadir campos; frontend debe tolerar arrays vacíos y valores ausentes. Backend documentará esquema final y ejemplos en docs/coordination/codex-backend.md.

Acciones prospectador y payloads:
- create_company {name,domain,sector,country}
- create_contact {name,email,title,company_id,country,phone?}
- search_prospects {query,sector?,country?}: genera candidatos sintéticos .example, sin API externa.
- reveal_contact {prospect_id}: valida créditos y deduplica, crea contacto asociado; id prospecto por entity_id también.
- create_campaign {name,contact_ids:[],subject?,body?}
- draft_campaign entity_id campaña: genera borrador Claude simulado basado en datos.
- approve_campaign entity_id campaña: deja aprobación del texto/destinatarios.
- send_campaign entity_id campaña: envío simulado registrado; exige aprobación y excluye no contactar.
- receive_reply entity_id contacto {body?}: respuesta sintética que detiene seguimientos y notifica.
- exclude_contact entity_id contacto {reason?}: bloquea todos los pendientes.
- log_meeting entity_id contacto {title,date?}
- set_opportunity {name,company_id,contact_id?,amount,currency,status}
- sync_post: genera conciliación demo sin conexión externa.

Acciones contratos:
- create_contract {title,country,company,amount,currency,type,confidential?,end_date?}
- upload_document entity_id contrato {filename,kind?}: adjunto demo sin binarios reales.
- submit_review / approve_contract / reject_contract / send_signature / sign_contract / activate_contract entity_id contrato. Transiciones controladas con roles y estados; permitir completar un flujo con perfil regional.
- request_access entity_id contrato {reason}: solicitud al dueño del país.
- grant_access entity_id solicitud {days?}: solo dueño/rol regional autorizado, con auditoría.
- analyze_contract entity_id contrato: OCR/extracción/resumen y evidencia sintéticos, persistidos.
- redact_document entity_id contrato: genera copia saneada real de texto sintético, sin filtrar originales.
- add_obligation entity_id contrato {title,due_date,owner?}
- complete_obligation entity_id obligación {evidence?}
- add_amendment entity_id contrato {title,description?,new_end_date?}
- renew_contract entity_id contrato {end_date?}

Integraciones muestran status:"simulado" para Lusha, Microsoft365, Claude, POST, OCR y firma. PostgreSQL status:"conectado" solo si real. Estados CRM sugeridos nuevo/contactado/respondió/reunión/propuesta/ganado/perdido/no_contactar. Contratos borrador/en_revision/pendiente_aprobacion/aprobado/pendiente_firma/firmado/activo/en_renovacion/vencido/archivado/rechazado. UI usa rótulos en español.

