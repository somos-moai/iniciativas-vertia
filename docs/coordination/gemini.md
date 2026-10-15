# Handoff a Gemini mediante Antigravity

**Estado: PENDIENTE de revisión real en Antigravity.** Fecha: 15-10-2026.

La interfaz actual fue implementada por Codex. Este documento prepara la colaboración solicitada; no acredita una revisión o autoría de Gemini. Cuando Gemini efectúe la revisión, debe sustituir el estado por fecha, modelo indicado por Antigravity, archivos revisados, hallazgos y pruebas realmente ejecutadas.

## Canal y contexto compartido

- Editor solicitado: **Antigravity** para Gemini. Claude participa mediante **Claude Code** y Codex coordina integración, pruebas y publicación.
- Repositorio: [somos-moai/iniciativas-vertia](https://github.com/somos-moai/iniciativas-vertia).
- Carpeta compartida: `I:/Unidades compartidas/Vertia/Proyectos Roadmap Vertia/iniciativas-vertia`.
- Contexto original: `I:/Unidades compartidas/Vertia/Proyectos Roadmap Vertia`.
- Ejecutable local detectado: `C:/Users/cueva/AppData/Local/Programs/Antigravity/Antigravity.exe`. No se inició una ventana ni una sesión del editor automáticamente.
- Descubrimiento local: comandos `antigravity`/`agy` no disponibles en PATH; no hay directorio CLI estándar. `resources/bin` contiene `language_server.exe` y `webm_encoder.exe`, sin interfaz headless de revisión identificada. El mecanismo preparado es abrir este repositorio en Antigravity y entregar el encargo al agente; no se simula una llamada automática inexistente.

Leer primero [AGENTS.md](../../AGENTS.md), [BRIEF.md](../BRIEF.md), [API_CONTRACT.md](../API_CONTRACT.md), [tarea frontend](../tasks/GEMINI_FRONTEND.md) y [contrato final backend](codex-backend.md). Inspeccionar después [frontend/src/main.jsx](../../frontend/src/main.jsx) y los activos de marca en `frontend/public/brand/`.

## Encargo para pegar en Antigravity

> Revisa como Gemini, de forma independiente y meticulosa, las dos demostraciones de este repositorio: Prospectador Global Vía Pública y Gestión Contractual Vertia. Lee AGENTS.md, docs/BRIEF.md, docs/API_CONTRACT.md y docs/coordination/codex-backend.md. La implementación actual de frontend pertenece a Codex. Evalúa experiencia de usuario, procesos, coherencia de integración, permisos, identidad visual, alcance MVP y roadmap regional. Identifica fallos concretos con evidencia y cambios propuestos. No atribuyas pruebas que no hayas ejecutado. Escribe tus resultados en docs/coordination/gemini.md; si necesitas cambios, limita tu intervención a frontend/ y este archivo, sin sobrescribir trabajo concurrente. Coordina primero mediante el registro compartido. No leas .env, credenciales ni documentos confidenciales; no envíes correos ni uses las APIs externas de las aplicaciones. Los adaptadores externos de estas maquetas son simulados. No ejecutes commits, push, despliegues, cambios de infraestructura o bases ajenas. Distingue claramente qué revisión hiciste, qué implementaste y qué permanece pendiente.

## Lista de revisión

### Prospectador

- Recorrido completo: empresa/contacto → búsqueda → revelado y créditos → campaña → borrador → edición → aprobación humana → envío simulado → respuesta/exclusión → reunión → oportunidad.
- Validar nombres exactos de acciones y payloads, refresco del estado y presentación de errores 400/401/403/404/409.
- Comprobar que enviar sin aprobar esté bloqueado, modificar el texto revoque aprobación y excluir/responder detenga seguimientos.
- Los candidatos no revelados no muestran correo; créditos y deduplicación deben corresponder al estado persistente.
- Carteras por ejecutivo y país; Legal no debe obtener datos comerciales no autorizados; consulta no puede modificar.
- Descarga CSV con `X-Demo-User`, persistencia al recargar y métricas derivadas de registros.

### Gestión contractual

- Recorrido: crear → adjuntar documento sintético → analizar → revisar → aprobar/rechazar → firma simulada → activar → obligación → evidencia → enmienda/renovación.
- Documentos reservados de otros países no exponen montos, partes, análisis ni antecedentes. Solicitud y concesión temporal permiten lectura según autorización.
- Copia saneada reconstruida sin campos originales: inspeccionar respuesta HTML, no solo apariencia visual. Firma demo no debe presentarse como firma legal.
- Validar revisión humana, fuente/versión del análisis, trazabilidad, alertas, obligaciones y antecedentes para licitaciones.
- Permisos y transiciones deben coincidir con backend; cualquier limitación de sociedad/tipo de flujo debe declararse y separarse de promesas productivas.

### Experiencia, marca y regionalización

- Pantallas 1440 px y 390 px; navegación, tablas, filtros, formularios, drawers, estados vacíos, loading, errores y accesibilidad básica.
- Logos oficiales, contraste y paletas de Global Vía Pública / Vertia; tipografía legible y registro formal.
- Datos sintéticos y proveedores simulados identificados de forma clara y discreta; ningún botón principal decorativo.
- Configuración base CL/UY/PE/AR/MX; filtro visual de país no altera autorización del perfil. Monedas y fechas comprensibles.
- Distinguir entrega incluida, evolución incluida y ampliación posterior. No prometer el CLM regional completo dentro del alcance comercial acotado.
- Coherencia con presupuestos: Prospectador USD 13.000 netos y Contratos USD 30.000 netos; contratación en UF, IVA separado; terceros a cargo de Vertia. No alterar cifras o condiciones sin coordinación.

## Entrega esperada

Registrar fecha, modelo visible en Antigravity, versión/commit revisado, pruebas ejecutadas y resultados. Para cada hallazgo: prioridad, archivo y línea, recorrido afectado, evidencia y corrección propuesta. Separar defectos demostrados, incertidumbres y mejoras opcionales. Si se corrige frontend, enumerar archivos y pruebas necesarias para que Codex integre y publique.

Los hallazgos y decisiones se comparten por `docs/coordination/` y el repositorio. No atribuir identidad Gemini a un subagente Codex.

## Registro de preparación por Codex

Antes de la aclaración del canal, se instaló Gemini CLI 0.64.0 de forma aislada en `/home/moai/iniciativas-vertia/agent-review` del VPS autorizado. Una invocación no produjo respuesta y terminó con código 41; **no hubo revisión real ni participación acreditable de Gemini**. Se suspendió esa vía al indicarse Antigravity. No se leyeron, transfirieron ni imprimieron tokens y no se modificó el servicio de las aplicaciones. La instalación no se utiliza como canal de colaboración.
