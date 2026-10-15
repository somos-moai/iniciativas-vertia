# Coordinación Codex — backend

## Estado y ejecución

Implementación en `backend/`. FastAPI + SQLAlchemy + psycopg; PostgreSQL real obligatorio, sin fallback. `DATABASE_URL` por entorno; ejecutar desde raíz `python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000`. La semilla corre una sola vez y persiste después de reiniciar. README detalla pruebas con `TEST_DATABASE_URL`; nunca se leen `.env` ni credenciales del disco. Ninguna API externa se llama.

## Contrato listo para Gemini

Conserva `docs/API_CONTRACT.md`: GET `/api/state?app=prospectador|contratos`, POST `/api/actions`, GET `/api/export?app=...`, GET `/api/contracts/{id}/document?redacted=true|false`. Header `X-Demo-User`; omitir selecciona `regional`. Un perfil desconocido retorna 401; restricciones 403; registro inexistente 404; transición/duplicado/conflicto 409; validación 400/422. Error `{detail: 'explicación'}`. POST retorna `{ok:true,message,entity}`: **refrescar GET** para métricas y listas. No se debe asumir que POST retorna `state`.

Perfiles seleccionables (IDs exactos):

| id | role | country | Capacidad |
|---|---|---|---|
| regional | regional | CL | Visión regional y todas las acciones |
| manager-cl | manager | CL | Jefatura Chile, aprobar campañas y contratos |
| executive-uy | executive | UY | Cartera Uruguay, borradores y seguimiento; requiere jefatura para aprobar |
| legal-pe | legal | PE | Documentos Perú, aprobación y firma simulada; sin cartera comercial |
| viewer-ar | viewer | AR | Consulta Argentina, puede solicitar acceso entre países |
| executive-cl | executive | CL | Cartera propia Chile; no aprueba campañas/contratos |

Cinco países: `CL/UY/PE/AR/MX`; `countries` incluye `code/name/currency`. El selector de país UI filtra lo ya autorizado por el servidor: no cambia el permiso del perfil. `users` siempre enumera estos seis perfiles explícitamente sintéticos; esto no es SSO productivo.

### Colecciones y campos

Siempre retorna arrays (aunque vacíos): `companies`, `contacts`, `campaigns`, `activities`, `opportunities`, `prospects`, `messages`, `contracts`, `access_requests`, `obligations`, `audit`, `notifications`, `roadmap`, `integrations`. Objetos comunes `id`, `created_at` ISO y normalmente `country/owner_id/status`. No hay textos binarios reales.

- companies: `name,domain,sector,country,owner_id,status`.
- contacts: `name,email,title,phone,company_id,company_name,country,owner_id,status,excluded,exclusion_reason,score,source,last_contact_at`.
- prospects: `name,email,title,company_name,sector,country,owner_id,status,revealed,score,source,credit_cost,contact_id?`. El servidor retorna `email:null` hasta `revealed`; se trata de dato ficticio, nunca dato comprado real.
- campaigns: `name,country,owner_id,status,contact_ids[],subject,body,approved_by,approved_at?,sent_count,reply_count,skipped_count?,sent_at?`. Estados `borrador/aprobada/enviada`; aprobación invalida borrador IA y envío nunca automático.
- messages: `contact_id,campaign_id?,country,owner_id,subject,body,direction:outbound|inbound,status,followup_status:programado|cancelado,cancellation_reason?`. Solo se crean por acciones; nunca correo real.
- activities: `title,type:meeting|sync,date,contact_id?,country,owner_id,status,description?`.
- opportunities: `name,company_id,contact_id,country,owner_id,amount,currency,status`.
- contracts: `title,name,reference,country,owner_id,company,counterparty,amount,currency,type,status,confidential,start_date,end_date,version,documents[],history[],analysis,redacted_ready,redaction?,amendments[],signature?,can_access,can_edit,restricted`.
- documents[]: `id,filename,kind,version,created_at,synthetic:true`. No URL externa; botón de documento llama endpoint con header y abre blob HTML o descarga.
- history[]: `status,at,by,note?`.
- analysis: null o `{provider,simulated:true,summary,risk,risk_level,score,extracted_fields:{amount,currency,end_date,country},findings:[{title,severity,evidence,page,recommendation}],analyzed_at,source_version,requires_human_review:true}`.
- signature: null o `{provider,status,legal_signature:false,at,by}`.
- access_requests: `contract_id,country,owner_id,requested_by,requester_name?,reason,status:pendiente|aprobada,granted_by?,expires_at?,days?`.
- obligations: `contract_id,title,country,owner_id,due_date,status:pendiente|completada,evidence?,completed_at?,completed_by?`.
- audit: `action,title,entity_id?,country,owner_id,actor,actor_name?,detail,created_at`. Auditoría demo mutable en base, no WORM.
- notifications: `title,country,owner_id,status,contact_id?`.

Contratos de otro país sin acceso aparecen solo como catálogo: `{id,title:'Documento reservado · PE',name,reference,country,status:'restringido',confidential:true,can_access:false,can_edit:false,restricted:true,documents:[],history:[]}`. **No contienen monto, partes, análisis ni antecedentes**. Usar solicitud de acceso. Acceso concedido es temporal y solo de lectura: no habilita edición en otro país.

### Métricas

`metrics` es objeto numérico, no array. Prospectador: `companies,contacts,total_contacts,prospects,campaigns,active_campaigns,sent,replies,reply_rate,meetings,pipeline,pipeline_value,excluded`. `reply_rate` es porcentaje 0–100. `pipeline` es suma USD demo, las oportunidades iniciales son USD. Contratos: `contracts,total_contracts,active_contracts,pending_approval,pending_signature,expiring_soon,overdue_obligations,obligations,contract_value,access_requests`. Contratos restringidos no entran a métricas de información sensible. `expiring_soon` son próximos 90 días; atrasos se comparan con fecha actual.

`credits:{used,limit,remaining,provider:'Lusha simulado',scope:'250 por cartera; agregado visible'}`; cada revelado deduplicado consume un crédito; guard transaccional por cartera. Perfil ejecutivo ve límite 250; regional ve agregado de cinco carteras iniciales (1250). `integrations:[{id,name,status,description,mode}]` con PostgreSQL `conectado` y proveedores `simulado`. `roadmap:[{id,name,title,status:incluido|ampliacion,description}]`. `mode:'synthetic'` y `generated_at` en raíz.

### IDs de semilla para recorridos

- `company-UY-0`, `contact-UY-0-0`, `prospect-UY-0`.
- `campaign-UY-0` borrador, `campaign-UY-1` aprobada, `campaign-UY-2` enviada.
- `contract-CL-0` borrador, `contract-CL-1` revisión, `contract-CL-2` aprobado, `contract-CL-3` pendiente firma, `contract-CL-4` activo. Misma serie para UY/PE/AR/MX.
- `obligation-CL-4-0` pendiente y `obligation-CL-4-1` completada.
- `access-demo`: ejecutivo Uruguay solicita `contract-PE-4`; regional o Legal Perú puede conceder.

### Guardas de flujo relevantes

- `create_campaign` exige 1–200 contactos accesibles, de un país y no excluidos. `approve_campaign` solo regional/jefatura. `draft_campaign` vuelve a borrador; `send_campaign` exige aprobación, bloquea doble envío y omite contactos excluidos/respondidos. Respuesta o exclusión cancela seguimientos pendientes.
- `create_contact` exige `.example`, empresa existente y mismo país. `search_prospects` genera tres candidatos por búsqueda. No llamadas Lusha reales.
- `submit_review` exige documento; flujo borrador → en_revision → aprobado → pendiente_firma → firmado → activo. Aprobación, rechazo y firma solo regional/jefatura/Legal. `upload_document` permitido en borrador/rechazo/renovación; invalida análisis y copia saneada.
- `redact_document` exige revisión de perfil regional/jefatura/Legal. HTML saneado se reconstruye con campos permitidos y omite originales completamente; endpoint original verifica acceso igualmente.
- `renew_contract` activo/vencido → en_renovacion y fecha posterior. `add_amendment` requiere firmado/activo/renovación. `grant_access` 1–30 días, responsable del país/regional/propietario autorizado.

### Extensiones opcionales disponibles

- `update_contact` entity_id contacto `{name?,title?,phone?}` y `update_company` entity_id empresa `{name?,sector?}` permiten edición de campos acotada con el mismo ACL.
- `import_contacts` `{rows:[{name,email,title?,company_id,country,phone?}]}` admite 1–100 filas y omite duplicados; toda la importación revierte si una fila no es válida. Retorna actividad con `imported/duplicates`.
- `set_campaign_content` entity_id campaña `{subject?,body?}` permite edición humana y siempre revoca aprobación; bloqueado después de enviar.

### Hosting estático

El mismo FastAPI sirve `frontend/dist` por defecto; variable `FRONTEND_DIST` opcional. `/`, `/prospectador`, `/contratos` y subrutas tienen fallback SPA; recursos estáticos reales se sirven con prevención de traversal. No captura errores `/api/*`. Opcional `PROPOSALS_DIR` publica únicamente archivos `.html/.pdf/.docx` de ese directorio por `/propuestas/{filename}`; no usar allí documentos internos ni fuentes confidenciales. No se publica el resto del repositorio.

## Pruebas

Suite en `backend/tests/test_integration.py`. Requiere PostgreSQL real autorizado, crea esquema aleatorio exclusivo para no tocar tablas existentes. Se verifica ACL, envío aprobado/exclusión, créditos y duplicados, ciclo contractual, saneamiento, acceso temporal de lectura, CSV y persistencia.

**Resultado 15-10-2026: 10 pruebas aprobadas en PostgreSQL 17 real, 122,74 s**, Python 3.14.2 y pytest 9.0.3. Se inicializó un clúster local temporal exclusivo, enlazado únicamente a loopback en un puerto diferente al servicio existente. No se utilizaron bases corporativas, contraseñas existentes ni SQLite. Comando: `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest backend/tests -vv --tb=short`, con `TEST_DATABASE_URL` del clúster de prueba por entorno. Compilación Python e importación de rutas también verificadas.

**Validación adicional VPS: 10 pruebas aprobadas en PostgreSQL 16, 1,97 s**, Python 3.10. Reportado por Codex Infra sobre base/rol exclusivos. Una advertencia de dependencia; sin fallos. Infra vuelve a copiar `db.py/main.py` finales antes de publicar.
