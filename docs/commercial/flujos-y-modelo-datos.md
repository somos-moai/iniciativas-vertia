# Anexo de flujos y modelos de datos

15 de octubre de 2026. Aplica a las demostraciones de Prospectador comercial y Gestión contractual publicadas en iniciativasvertia.somosmoai.tech, sección "Flujo y datos" de cada aplicación.

El catálogo inicial de la maqueta es sintético. Los registros y transiciones persisten en PostgreSQL y cada acción valida perfil y país en el servidor. La carga de PDF e imágenes, extracción de texto y OCR local son reales. Claude API, firma, correo, calendario, proveedor de prospectos y POST permanecen simulados; no se conectan ni consumen servicios externos. La lectura local no se presenta como interpretación jurídica de Claude. La implementación productiva se define en cada propuesta.

## Prospectador comercial — flujo completo

| Etapa | Quién | Acción del sistema | Qué registra | Regla verificable | Servicio |
|---|---|---|---|---|---|
| 1. Cartera y datos base | Ejecutivo, jefatura | create_company, create_contact, import_contacts, update_contact | Empresa, contacto, actividad de importación | Solo correos .example; contacto y empresa del mismo país; duplicados por correo omitidos; importación revierte completa ante una fila inválida | — |
| 2. Descubrimiento | Ejecutivo, jefatura | search_prospects | Prospecto | Tres candidatos por búsqueda con correo oculto; Legal no prospecta | Lusha simulado |
| 3. Revelación | Ejecutivo | reveal_contact | Prospecto vinculado a contacto y empresa | Un crédito por contacto, máximo 250 por cartera; un contacto ya revelado no se cobra otra vez | Lusha simulado |
| 4. Campaña y borrador | Ejecutivo | create_campaign, draft_campaign, set_campaign_content | Campaña en borrador | 1 a 200 contactos de un país, sin excluidos; editar revoca la aprobación | Claude simulado |
| 5. Aprobación humana | Jefatura, regional | approve_campaign | Campaña aprobada con huella del contenido | Sin aprobación no hay envío; si el contenido cambia se exige nueva aprobación | — |
| 6. Envío controlado | Ejecutivo, jefatura | send_campaign | Mensajes salientes; contacto contactado | Omite excluidos y contactos que respondieron; bloquea doble envío; ningún correo sale | Microsoft 365 simulado |
| 7. Respuesta y exclusión | Ejecutivo | receive_reply, exclude_contact | Mensaje entrante, notificación, contacto | Respuesta o exclusión cancela seguimientos pendientes; un excluido no se reactiva solo | — |
| 8. Reunión | Ejecutivo | log_meeting | Actividad de reunión | No se agenda con contactos excluidos | Calendario simulado |
| 9. Oportunidad | Ejecutivo, jefatura | set_opportunity | Oportunidad | Etapas nuevo, calificada, propuesta, negociación, ganado, perdido; el contacto pertenece a la empresa | — |
| 10. Conciliación POST | Jefatura, regional | sync_post | Actividad de conciliación | Valida registros y errores; en producción depende de API documentada o intercambio de archivos | POST simulado |

## Gestión contractual — flujo completo

| Etapa | Quién | Acción del sistema | Qué registra | Regla verificable | Servicio |
|---|---|---|---|---|---|
| 1. Alta | Ejecutivo, Legal, jefatura | create_contract | Contrato en borrador, referencia VRT-país, versión, historial | Confidencial por defecto; país según perfil | — |
| 2. Documento y versiones | Propietario, Legal | upload_document | Documento con versión | Solo en borrador, rechazo o renovación; cada carga invalida análisis y copia saneada | — |
| 3. Lectura y verificación | Propietario, Legal | uploads, review_extraction | Texto por página, propuestas de campos y evidencia | No aplica campos sin confirmación; conserva la versión de origen | PDF y OCR local reales para archivos cargados; Claude desconectado |
| 4. Copia saneada | Legal, jefatura, regional | redact_document | Copia reconstruida con lista permitida | Excluye monto, contraparte, cuentas e identificadores fiscales | — |
| 5. Envío a revisión | Propietario | submit_review | Estado en revisión e historial | Exige al menos un documento | — |
| 6. Aprobación o rechazo | Jefatura, Legal, regional | approve_contract, reject_contract | Decisión, responsable y motivo | Solo perfiles autorizados; el rechazo devuelve el contrato para corrección | — |
| 7. Firma | Jefatura, Legal, regional | send_signature, sign_contract | Estado de firma | Aprobado, por firmar, firmado; sin efecto legal en la demostración | Firma electrónica simulada |
| 8. Activación | Jefatura, Legal, regional | activate_contract | Contrato activo | Solo desde firmado | — |
| 9. Obligaciones | Propietario, Legal | add_obligation, complete_obligation | Obligación con responsable, vencimiento y evidencia | Completar exige evidencia y registra quién y cuándo | — |
| 10. Enmiendas y renovación | Propietario, Legal | add_amendment, renew_contract | Enmienda; nuevo vencimiento e historial | Enmiendas sobre firmado o activo; la renovación extiende el plazo y vuelve a revisión | — |

Acceso entre países: un perfil de otro país ve solo la referencia del contrato. Solicita acceso con motivo (request_access) y el responsable del país o regional lo concede por 1 a 30 días, solo lectura (grant_access).

Transversal a ambas soluciones: cada acción crea un registro de auditoría con actor, acción, entidad y país. La bitácora de la demostración no es un registro inmutable.

## Modelo de datos de la demostración

Almacenamiento de la demostración: PostgreSQL real, tabla vertia_demo_records (id, app, kind, data JSONB, created_at) y tabla vertia_demo_meta para el control de la semilla. Las cargas reales utilizan además vertia_document_uploads para metadatos, texto por página, propuestas y revisión. Los archivos binarios y previews permanecen en un directorio privado, fuera del repositorio y de las rutas estáticas públicas. Cada entidad de negocio se relaciona con país y propietario para validar su alcance.

El modelo relacional de producción, con claves foráneas, índices, cifrado y política de retención y auditoría, se define en el levantamiento con Vertia. Este anexo describe el modelo lógico demostrado, no el esquema productivo.

### Entidades comunes

| Entidad | Campos principales | Nota |
|---|---|---|
| Perfil de demostración | id, name, role, country | Seis perfiles sintéticos; no es SSO |
| País | code, name, currency | CL, UY, PE, AR, MX |
| Notificación | title, status, contact_id | — |
| Auditoría | actor, action, entity_id, detail | Una entrada por acción |

### Prospectador comercial

| Entidad | Campos principales | Relaciones |
|---|---|---|
| Empresa | name, domain, sector, status | 1:N contactos; 1:N oportunidades |
| Contacto | company_id, name, email único, title, status, excluded, score, source | N:1 empresa; 1:N mensajes; 1:N actividades |
| Prospecto | contact_id, name, company_name, revealed, credit_cost, score | 1:0..1 contacto al revelar |
| Campaña | contact_ids, subject, body, status, approved_by, approval_hash, sent_count | N:N contactos; 1:N mensajes |
| Mensaje | contact_id, campaign_id, direction, followup_status, provider | N:1 contacto; N:1 campaña |
| Actividad | contact_id, type (reunión, importación, conciliación), date, status | N:1 contacto |
| Oportunidad | company_id, contact_id, amount, currency, status | N:1 empresa; N:1 contacto |

### Gestión contractual

| Entidad | Campos principales | Relaciones |
|---|---|---|
| Contrato | reference, title, type, company, counterparty, amount, currency, confidential, status, start_date, end_date, version | Contiene documentos, historial, análisis, copia saneada, firma y enmiendas |
| Documento | filename, kind, version, synthetic | Dentro del contrato, 1:N |
| Historial | status, at, by, note | Dentro del contrato, 1:N |
| Análisis asistido | summary, risk_level, score, extracted_fields, findings, source_version | Dentro del contrato, 1:0..1 |
| Copia saneada | reviewed_by, source_version, removed_fields | Dentro del contrato, 1:0..1 |
| Firma | provider, status, legal_signature siempre falso | Dentro del contrato, 1:0..1 |
| Enmienda | title, description, by | Dentro del contrato, 1:N |
| Obligación | contract_id, title, due_date, owner, status, evidence, completed_by | N:1 contrato |
| Solicitud de acceso | contract_id, requested_by, granted_by, reason, status, days, expires_at | N:1 contrato; N:1 perfil |

## Perfilamiento comercial verificable

El perfil de cliente ideal se configura por usuario y conserva versiones. Define sectores, mercados, tamaño, presupuesto orientativo, señales y exclusiones. Una empresa documenta los datos conocidos y su origen; la evaluación compara esos datos con los criterios y muestra razones, faltantes y cobertura. Su porcentaje es coincidencia de criterios evaluados, no una probabilidad de venta. No se inventa información web ni se simula una consulta externa como real.

La selección de cuenta acompaña al contacto y a la campaña. El aprobador puede consultar la versión del perfil de cliente ideal y el contexto de selección registrado al crearla. Editar el mensaje exige una nueva aprobación; responder o excluir detiene el seguimiento.

## Lectura de archivos y confirmación humana

Se admiten PDF, PNG, JPEG y WebP de hasta 15 MiB; los PDF se limitan a 40 páginas. La aplicación conserva el archivo, genera previews y muestra texto por página. Utiliza extracción nativa para PDF con texto; las imágenes y páginas escaneadas usan en la demostración un escaneo simulado que identifica el documento por el nombre del archivo. El OCR real corresponde a la implementación productiva. Si la calidad impide reconocer texto, se informa sin inventar campos.

Las propuestas de contraparte, tipo, monto, moneda y fechas incluyen evidencia cuando una regla encuentra un patrón explícito. La persona puede editar el valor y seleccionar qué campos confirma. La lectura no calcula riesgo jurídico ni reemplaza a Claude API. Una versión nueva revoca el análisis anterior y el extracto compartible.

Para compartir un archivo cargado entre países se redacta y confirma un extracto autorizado. La concesión temporal permite ese extracto, no el original, sus páginas ni los campos reservados. La demostración no promete anonimización automática del contrato completo.

## Supuestos del modelo lógico propuesto

En producción se propone separar empresa, contacto, destinatario de campaña, gestión, oportunidad, contrato, documento, versión, decisión, obligación y autorización. Las relaciones conceptuales se muestran antes de ingresar a las aplicaciones. Se validan identificadores, unicidad, responsables, retención y niveles de acceso con Vertia antes de fijar claves, índices y reglas definitivas.

Los países comparten un núcleo configurable. No se asume que sus reglas legales sean idénticas ni que una autorización comercial implique acceso a contratos de otro país. La preparación regional está incluida; las activaciones masivas y validaciones locales pertenecen a las etapas definidas en el roadmap.

Fuente técnica: backend/main.py, docs/API_UPLOADS.md y docs/coordination/codex-backend.md. Si el backend cambia acciones o campos, este anexo y frontend/src/flows.jsx deben actualizarse juntos.
