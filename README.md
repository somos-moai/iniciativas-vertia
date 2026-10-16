# Iniciativas Vertia

Dos iniciativas independientes para Vertia Group, coordinadas por MoAI: Prospectador comercial para Global Vía Pública y Gestión Contractual para Vertia. Logística se deja para una etapa posterior.

Continuación solicitada por el usuario: [handoff para Claude Code y Gemini](HANDOFF_CLAUDE.md). Contiene el estado publicado y el defecto abierto al consultar los campos propuestos de una versión documental anterior; no dar la entrega por cerrada antes de corregirlo y verificarlo.

## Demostración y propuestas

- Centro de demostración: https://iniciativasvertia.somosmoai.tech/
- Prospectador: https://iniciativasvertia.somosmoai.tech/prospectador
- Contratos: https://iniciativasvertia.somosmoai.tech/contratos
- Propuestas separadas: `deliverables/prospectador.html`, `.docx`, `.pdf` y `deliverables/contratos.html`, `.docx`, `.pdf`.
- Requisitos de Vertia: [docs/commercial/requerimientos-cliente.md](docs/commercial/requerimientos-cliente.md).
- Operación y soporte: [docs/commercial/protocolo-soporte.md](docs/commercial/protocolo-soporte.md).
- Alcance y roadmap: [docs/commercial/scope-roadmap.json](docs/commercial/scope-roadmap.json).

La portada explica primero ambos proyectos, sus recorridos animados y explorables, los modelos de datos propuestos y el roadmap regional. Después ofrece acceso a las aplicaciones. Los perfiles seleccionables permiten revisar permisos; ese selector no es autenticación productiva.

El catálogo inicial usa datos ficticios persistentes en PostgreSQL. El perfilamiento comercial guarda criterios y evidencia con resultados explicables. La carga de PDF e imágenes, la extracción de texto de los PDF y la confirmación humana son reales; las imágenes usan un escaneo simulado que identifica el documento por el nombre del archivo. Claude API, correo, firmas, prospectos y POST permanecen simulados; no existen firmas legales ni mensajes enviados a terceros. La lectura local no realiza una evaluación jurídica con IA.

El sitio se protege antes de habilitar cargas reales. Las credenciales se entregan en un archivo privado fuera del repositorio. Nunca guardar claves ni documentos de los usuarios en Git. Ver `docs/API_UPLOADS.md` para límites, versiones, evidencia y permisos de lectura.

## Acuerdos comerciales

Prospectador: USD 13.000 netos de referencia; contratación propuesta en 311,7235 UF netas. Contratos: USD 30.000 netos de referencia; contratación propuesta en 719,3619 UF netas. IVA del 19 % adicional. Cada iniciativa tiene 40 % inicial y seis cuotas mensuales de saldo; la última cuota ajusta el redondeo. Las cuotas financian desarrollo. Soporte y servicios de terceros se separan de los honorarios de desarrollo.

Los importes, fuentes de conversión y las siete cuotas de cada iniciativa están en `docs/commercial/financials.json`; no editar las tablas de forma independiente. Los límites operativos son condiciones propuestas para formalizar, no acuerdos ya aceptados por Vertia. El programa regional completo se mantiene separado del MVP cotizado.

## Trabajo entre agentes

- Codex: backend, frontend, pruebas PostgreSQL, integración, documentos finales y despliegue.
- Claude Code: elaboración real de propuestas y revisión de alcance; registro en `docs/coordination/claude.md`.
- Gemini mediante Antigravity: revisión inicial registrada en `docs/coordination/gemini.md`; el encargo de la nueva experiencia está en `docs/coordination/ENCARGO_EXPERIENCIA_V2.md`. No atribuir pruebas nuevas hasta recibir evidencia.

Leer `AGENTS.md`, `docs/BRIEF.md` y `docs/API_CONTRACT.md` antes de modificar. Los agentes registran decisiones y hallazgos en `docs/coordination/`, trabajan con cambios delimitados y no guardan secretos. Los documentos de contexto están en `docs/context/`; el proyecto compartido conserva los originales.

Repositorio remoto autorizado: `git@github.com:somos-moai/iniciativas-vertia.git`. Se verificó autenticación SSH como `somos-moai` y publicación efectiva de la rama `main`. La credencial HTTPS de otra cuenta no se utiliza para este repositorio.

## Desarrollo y publicación

Backend: Python, FastAPI, SQLAlchemy y PostgreSQL. Frontend: React, Vite y CSS. Ver `backend/README.md`, `frontend/README.md` si existe y `infra/README.md` para variables y comandos. No hay SQLite como sustituto de PostgreSQL.

En unidades de Google Drive, `npm install` puede fallar con EBADF; `frontend/build-local.cjs` compila en una carpeta temporal local y copia el resultado a `frontend/dist`. El despliegue usa solamente los directorios y servicio propios de esta iniciativa. Las instrucciones productivas requieren cuentas AWS y PostgreSQL de Vertia y la sustitución de los adaptadores simulados por integraciones verificadas.

`scripts/build_proposals.py` usa el runtime documental de Codex y Pandoc con la referencia MoAI. En Windows sin LibreOffice se diagnosticó el renderer empaquetado y se exportó mediante Microsoft Word; todos los PDF se rasterizaron con Poppler para revisión visual. Las imágenes de QA no son entregables comerciales.
