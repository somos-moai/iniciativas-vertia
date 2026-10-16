# QA — perfilamiento comercial y lectura documental real

Fecha de ejecución: 2026-10-16T01:44:51.094Z.

Entorno: Vite local 127.0.0.1:5180 con proxy a una API FastAPI de staging aislada por túnel SSH. PostgreSQL y uploads en esquema/directorio dedicados de pruebas; no se modificó la demostración pública en estas pruebas. Navegador Microsoft Edge headless, 1440×1000 y 390×844.

Resultado: **38/38 comprobaciones aprobadas**, sin errores JavaScript. Los rechazos 400 de validación fueron provocados intencionalmente para verificar que los formularios conserven su contenido.

## Recorridos comprobados

- Aprobado: Guided prospecting workspace loads
- Aprobado: No horizontal overflow: CRM ICP desktop — {"width":1440,"viewport":1440}
- Aprobado: ICP persisted with explicit criteria
- Aprobado: Company profile persisted
- Aprobado: Fit explains actual matching criteria
- Aprobado: Sources explicitly avoid external enrichment claims
- Aprobado: No horizontal overflow: CRM company desktop — {"width":1440,"viewport":1440}
- Aprobado: Cleared field becomes missing evidence
- Aprobado: Responsible discovery preserves selected company
- Aprobado: Campaign preserves qualification snapshot
- Aprobado: Qualified campaign remains pending human approval
- Aprobado: Approver sees selection rationale
- Aprobado: Real document workbench loads
- Aprobado: PDF read from actual file
- Aprobado: Extracted fields do not change contract before review
- Aprobado: Authenticated source-page preview is rendered
- Aprobado: No horizontal overflow: CLM document desktop — {"width":1440,"viewport":1440}
- Aprobado: PDF amount and date proposals use source evidence
- Aprobado: Human review persists edited fields
- Aprobado: Shared rendition contains only human-authorized extract
- Aprobado: Image upload invokes actual OCR
- Aprobado: New version invalidates previous shared extract
- Aprobado: No horizontal overflow: CRM ICP mobile — {"width":390,"viewport":390}
- Aprobado: No horizontal overflow: CRM profile mobile — {"width":390,"viewport":390}
- Aprobado: No horizontal overflow: CLM file review mobile — {"width":390,"viewport":390}
- Aprobado: No JavaScript page errors
- Aprobado: 400 validation preserves modal field values
- Aprobado: 400 validation preserves detailed company draft
- Aprobado: One-click PDF sample uses actual 3-page extraction
- Aprobado: Sample PDF proposes source amount and expiry
- Aprobado: PDF original preview uses authenticated blob
- Aprobado: One-click image sample uses actual raster OCR
- Aprobado: Foreign profile can request redacted access
- Aprobado: Regional approval grants only defined scope
- Aprobado: Foreign state exposes redacted-only flag
- Aprobado: Foreign grant cannot read original bytes
- Aprobado: UI opens authorized extract rather than original
- Aprobado: No JavaScript errors in samples/error handling

## Evidencia

Capturas y JSON completos en artifacts/qa/workspaces/. Para comparar original y extracción en un mismo viewport: clm-pdf-comparison-viewport.png y clm-real-image-comparison-viewport.png. Se inspeccionaron además las vistas de ICP y empresa y sus versiones móviles.

## Correcciones encontradas durante QA

- Componentes Field y drawer reconciliados de forma estable: una actualización del estado o un error 400 no remonta los formularios ni aborta una carga en curso.
- Los campos de auditoría de un perfil (field_sources, timestamps) se excluyen de la carga útil de edición; los campos numéricos retirados se envían como null y vuelven a ser evidencia faltante.
- Al cambiar de versión se cargan texto y páginas del documento seleccionado, sin reutilizar la extracción de otra versión.
- Los porcentajes heurísticos de propuestas documentales se presentan como «Propuesta de lectura», sin atribuirles una probabilidad jurídica validada.
- El acceso regional a archivos reales abre únicamente el extracto autorizado; no intenta mostrar páginas, texto ni bytes del original.

## Compilación y límites

Build de producción correcto: index-VONnwKLm.js e index-CTvZoLKH.css. Las dos muestras públicas (PDF de tres páginas y PNG de su primera página) pasan por el mismo upload y lector local que cualquier archivo seleccionado por el usuario. No se inyectan resultados de muestra en el frontend. No se consumen APIs externas.

La calificación comercial aplica reglas a los datos declarados y conserva fuentes y faltantes; no equivale a información externa verificada ni a una probabilidad de venta. La extracción PDF/OCR es real y local, con aceptación humana de los campos. Claude, proveedores de prospectos, correo y firma siguen siendo adaptadores simulados.

Sin publicación desde este agente. El coordinador revisa y realiza el despliegue privado.

## Defecto posterior confirmado y entrega pendiente

Después de estos 38 checks, la revisión visual detectó que al volver de una imagen a un PDF anterior pueden aparecer vacíos los inputs de campos propuestos, aunque la evidencia esté disponible. El agente frontend confirmó el caso antes de la interrupción solicitada por el usuario. No hay hotfix validado. Este resultado no cubre la correcta población de esos inputs al alternar versiones; ver HANDOFF_BUG_DOCUMENTOS.md y HANDOFF_CLAUDE.md antes de dar la entrega por cerrada.
