# Lectura real de documentos y perfilamiento verificable

Extensión del contrato API. Implementación local: PostgreSQL, archivos privados, pypdf y PDFium. Sin OCR: escaneo simulado: las imágenes y páginas sin texto se identifican por el nombre del archivo, sin OCR. **No se consume Claude ni otra API externa.** La interfaz debe distinguir el texto realmente leído de los datos sintéticos iniciales y del análisis jurídico por IA, que no está conectado.

## Carga y procesamiento

`POST /api/contracts/{contract_id}/uploads`, multipart: `file` obligatorio y `kind` opcional (`contrato` por defecto). Cabecera `X-Demo-User` del perfil. Alias `/upload` disponible, preferir plural. No enviar `Content-Type: application/json` para FormData; el navegador establece boundary.

- PDF, PNG, JPEG y WebP; magic bytes, extensión y MIME coherentes.
- Máximo 15 MiB, 40 páginas PDF y 20 millones de píxeles por imagen. Imágenes animadas, PDF cifrado y archivos dañados se rechazan.
- Extracción nativa de PDF si tiene texto. Páginas escaneadas e imágenes usan `method:"escaneo_simulado"`: los ejemplos publicados (`contrato_imagen_demostracion`, `contrato_servicios_demostracion`) devuelven su contenido conocido; otro archivo solo aporta el tipo inferido de su nombre, nunca montos, partes ni fechas. Se agrega un aviso en `warnings` y `analysis.scan_simulated:true`.
- Un proceso de lectura simultáneo; otro intento recibe 429 y `Retry-After: 5`. Límite global 90 segundos, subproceso con límites de recursos en Linux. No inventar barras de progreso de lectura: XHR puede medir transferencia; después indicar lectura en curso hasta recibir resultado.
- Respuesta completa o error; un fallo no guarda una versión documental inválida ni deja archivos parciales. Texto ilegible se informa como `completed_no_text` sin propuestas inventadas.
- Originales y previews en `UPLOAD_DIR` privado, directorio 700/archivos 600. Claves UUID internas; no devolver rutas ni claves de almacenamiento. Metadatos, páginas y extracción persisten en PostgreSQL, tabla `vertia_document_uploads`.

Respuesta:

```json
{
  "ok": true,
  "message": "Documento cargado y leído. Revise los campos propuestos antes de aplicarlos.",
  "entity": {"id":"...", "has_real_uploads":true, "analysis":{}},
  "document": {
    "id":"upload-...", "filename":"contrato.pdf", "content_type":"application/pdf",
    "mime":"application/pdf", "size_bytes":12345, "kind":"contrato", "version":2,
    "page_count":1, "status":"completed", "synthetic":false, "real":true,
    "extraction_mode":"local_extraction", "text_characters":500, "requires_review":true,
    "created_at":"ISO"
  },
  "processing": {"status":"completed", "elapsed_seconds":1.4, "page_count":1,
    "text_characters":500, "warnings":[], "ai_connected":false}
}
```

La carga requiere acceso nativo/regional y escritura, en borrador, rechazado o renovación. Cada carga aumenta versión y revoca análisis/copia saneada anteriores. Se guarda inmediatamente la nueva extracción local, marcada pendiente de revisión humana. Una carga real nunca se representa como documento sintético.

## Texto, vista previa y original

- `GET /api/contracts/{cid}/uploads/{document_id}/text`: `{document, pages:[{page,text,method,confidence,chars,preview_url}], proposed_fields, warnings, review_status, mode:'local_extraction', ai_connected:false}`.
- `GET /api/contracts/{cid}/uploads/{document_id}/preview?page=1`: PNG renderizado; no PDF/HTML del usuario ejecutable. Recuperar mediante fetch con cabecera y blob.
- `GET /api/contracts/{cid}/uploads/{document_id}/original`: bytes originales como adjunto, MIME correcto; descarga auditada.
- `GET /api/document-capabilities`: límites, `ocr_available:false`, `scan_mode:"simulado_por_nombre_de_archivo"` y `claude_connected:false`.

En la lista de integraciones, `Lectura de archivos` figura `conectado` (texto PDF real; imágenes con escaneo simulado); Claude, firma y proveedores pagados siguen simulados/desconectados. No presentar la lectura local real como un consumo de API IA.

Los tres endpoints requieren acceso **nativo al país o regional**. Una concesión entre países **no habilita original, previews, texto, evidencia original ni export de campos reservados**. En `state`, el contrato concedido tiene `sanitized_only:true`, `can_view_original:false`, `access_scope:'redacted_only'`, sin montos, partes, documentos originales, análisis ni historial confidencial. Solo puede abrir su extracto saneado una vez autorizado.

## Análisis local y revisión humana

`entity.analysis` contiene:

```json
{
  "provider":"Lectura local del texto PDF" | "Texto PDF + escaneo simulado por nombre de archivo", "scan_simulated":false, "mode":"local_extraction",
  "simulated":false, "ai_connected":false, "document_id":"upload-...",
  "summary":"Cantidad real de páginas, caracteres y propuestas",
  "text_preview":"Primeros 4000 caracteres realmente leídos",
  "pages":[{"page":1,"method":"pdf_text","chars":500,"confidence":null}],
  "proposed_fields":[{"field":"amount","label":"Monto propuesto","value":12500,
    "source_page":1,"evidence":"Monto total: USD 12,500.00","confidence":0.7,
    "confidence_kind":"heurística de regla; no probabilidad validada",
    "method":"regla local sobre texto leído","requires_review":true}],
  "findings":[], "risk":"no_evaluado", "risk_level":"no_evaluado", "score":null,
  "warnings":[], "source_version":2, "requires_human_review":true,
  "review_status":"pending"
}
```

Las reglas solo proponen tipo, contraparte, monto, moneda e inicio/vencimiento cuando existen patrones expresos con página y evidencia. No inventan cláusulas ni evaluación jurídica. Confianza de OCR es promedio de palabras Tesseract; confianza de propuesta es una heurística de regla declarada, **no precisión validada ni probabilidad de corrección**.

`POST /api/actions` con `action:'review_extraction'`, entity_id contrato y payload `{document_id,fields:{amount,currency,start_date,end_date,type,counterparty},notes}` aplica únicamente campos seleccionados por el usuario. Devuelve entidad con `analysis.reviewed_at/reviewed_by/reviewed_fields`, `review_status:'reviewed'`. No aplica datos automáticamente al contrato. Se rechaza revisión de una versión reemplazada. El análisis antiguo `analyze_contract` conserva/restituye extracción real; nunca la reemplaza por fixture. Para contratos iniciales sin carga real conserva el simulador explícito.

## Extractos saneados

En documento real, `redact_document` requiere `{safe_text:'extracto revisado autorizado para compartir',review_confirmed:true}` y perfil regional/jefatura/Legal. El HTML compartible se construye únicamente con ese extracto explícitamente aprobado y metadatos mínimos; todo texto se escapa. No contiene el original escondido ni se afirma anonimización automática. Nueva versión o revisión de campos revoca la copia previa. En documentos sintéticos iniciales se conserva el recorrido demo anterior.

El selector de perfiles es demostrativo, no autenticación. **Infra activa autenticación del sitio completo antes de publicar esta capacidad**, adicional a las autorizaciones de backend.

## Perfilamiento comercial sin datos inventados

`save_icp` guarda/versiona criterios y devuelve perfil; `state.icp` es perfil actual y `state.icp_profiles` historial visible. Payload: `{name?,target_sectors:[],countries:[],min_employees:null|number,max_employees:null|number,annual_budget_min:null|number,signals:[],exclusions:[],persona:string,offering?:string,ideal_customer?:string}`. Presupuesto del criterio en USD; sin conversión implícita.

`profile_company` sobre ID empresa guarda `{profile:{industry,offering,ideal_customer,employees,annual_budget,budget_currency,website_notes,persona,signals:[],exclusions:[]}}` y evalúa ICP. `evaluate_company` reevalúa; `enrich_company` no busca ni inventa datos: informa faltantes y ausencia de proveedor conectado.

Respuesta empresa añade `profile` y `fit:{score,score_type,decision,reasons,missing_fields,criteria_version,criteria_id,criteria_evaluated,criteria_configured,coverage,sources,evaluated_at,method,ai_connected:false,external_enrichment:false}`. El score, si hay criterios comprobables, es `100 × coincidencias / criterios evaluados`; no es probabilidad de venta. Si faltan datos, `decision:'informacion_insuficiente'` y se muestra cobertura. Sin criterios, `score:null`, `decision:'sin_criterios'`. No fabricar empleados, presupuesto, señales ni evidencia web. Los orígenes distinguen fixture, dato de cartera e ingreso manual.

`search_prospects` acepta `company_id` opcional: conserva cuenta y país en candidatos **ficticios explícitos**; `reveal_contact` reutiliza esa empresa. No es búsqueda real en Lusha. `create_campaign` admite `qualification_note` y `qualification_context.icp_id`; el servidor valida permisos y guarda snapshot de criterios, versión, empresas realmente seleccionadas, usuario y fecha. El recorrido mantiene aprobación humana y exclusiones.

## Validación

`backend/tests/test_real_documents.py` usa PDF válido con texto real, imagen PNG con escaneo simulado por nombre de archivo (ejemplo conocido y nombre desconocido sin datos inventados), metadatos/bytes originales, evidencia/campos, revisión humana, ACL de carga/lectura, rechazo de daño/tamaño/MIME, concesión entre países solo a extracto saneado, revocación al versionar e ICP transparente. Ejecutar junto a suite existente con PostgreSQL real autorizado.

**Resultado de la versión final: 15/15 pruebas aprobadas en 4,64 segundos**, staging aislado del VPS con PostgreSQL 16 y Tesseract real spa+eng. Incluye carga y lectura real del PDF y la imagen, además del recorrido empresa → candidatos → contacto vinculado → campaña con snapshot ICP. La validación visual de navegador se realiza por separado con el frontend contra una API temporal, antes de publicar.

Archivos sintéticos de prueba para ese recorrido visual: `backend/tests/fixtures/contrato_servicios_sintetico.pdf` (USD 12.500, vencimiento 2027-12-31) y `backend/tests/fixtures/foto_arrendamiento_sintetico.png` (USD 18.000, vencimiento 2028-06-30). Son archivos binarios válidos, no metadatos que simulan una carga.
