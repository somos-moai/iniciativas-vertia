# Handoff para Claude Code y Gemini en Antigravity

Fecha: 15 de octubre de 2026, hora de Chile. El usuario solicita que Claude continúe la coordinación con Gemini. Codex deja la implementación, pruebas, despliegue y pendientes documentados. No dar por cerrada la entrega: hay un defecto confirmado en la revisión de versiones documentales.

## Lo que pide el usuario

La primera maqueta resultó insuficiente. El sitio debe explicar primero los dos proyectos, sus MVP, roadmap regional, flujos y modelos de datos supuestos; después permitir entrar a aplicaciones convincentes. Las animaciones deben enseñar cómo funcionan los procesos. El Prospectador debe demostrar perfilamiento y el flujo comercial completo. Contratos debe aceptar PDF e imágenes, leer su contenido realmente y permitir verificarlo y continuar el proceso.

El equipo solicitado incluye explícitamente a Claude Code, Gemini mediante Antigravity y Codex, además de los subagentes de Codex. El usuario confía en ese equipo y pide trasladar esa confianza a una entrega verificable. No sustituir a Gemini o Claude por subagentes Codex con esos nombres, ni atribuir pruebas que no ejecutaron.

## Ubicación y estado publicado

- Carpeta: `I:\Unidades compartidas\Vertia\Proyectos Roadmap Vertia\iniciativas-vertia`.
- Contexto original: carpeta superior `Proyectos Roadmap Vertia`; contiene requerimientos originales, propuesta y antecedentes de las iniciativas.
- Repositorio: https://github.com/somos-moai/iniciativas-vertia, rama `main`.
- Sitio correcto: https://iniciativasvertia.somosmoai.tech.
- Último frontend publicado: `index-VONnwKLm.js` y `index-CTvZoLKH.css`.
- Sitio protegido con HTTP Basic Auth antes de habilitar archivos reales. La portada, apps, API, propuestas, muestras y assets requieren acceso.
- Credenciales: archivo `I:\Unidades compartidas\Vertia\Proyectos Roadmap Vertia\Acceso_Maquetas_Vertia.txt`, fuera del repositorio. Leerlo únicamente para acceder o probar, sin imprimir su contenido ni copiarlo a Git o al chat.
- VPS correcto: `217.196.62.58`, SSH como `root` mediante la clave existente `C:\Users\cueva\.ssh\id_ed25519`. Servicio de aplicación como `moai`.
- Proyecto remoto: `/home/moai/iniciativas-vertia`; servicio `iniciativas-vertia`; FastAPI en loopback `8788`; PostgreSQL exclusivo `vertia_demo`.
- `.env` y uploads privados permanecen en el VPS. No imprimirlos ni modificar servicios o bases de otros proyectos.
- El staging temporal `8790`, el túnel local `8000` y el preview de presentación `5179` fueron detenidos tras las pruebas. No asumir que siguen disponibles. Comprobar el estado de `5180` en el informe del agente frontend.
- Base anterior a esta entrega: commit `904c2cd`, ya publicado. El trabajo nuevo y este handoff se entregan en el commit de cierre; comprobar `git log -1` y `git status` al comenzar.

## Implementación que ya existe

### Presentación antes de las maquetas

`frontend/src/PresentationHub.jsx` y `presentation.css` reemplazan la portada inicial. Incluyen explicación de los dos proyectos, dos recorridos de cinco etapas reproducibles, pausables y explorables, responsables, entradas, decisiones y resultados; modelos conceptuales con relaciones y campos seleccionables; supuestos por validar; selección de países CL/UY/PE/AR/MX; roadmap, alcance y precios; acceso a las apps al final. Las ilustraciones están identificadas como recorridos explicativos, no operaciones reales.

Se corrigió contraste del título sobre fondo oscuro, se respetó movimiento reducido y se revisaron escritorio y móvil. `flows.jsx`, `flows.css`, `legibility.css` y `motion.css` incorporan trabajo de Claude y se conservaron. Los modelos propuestos se distinguen del almacenamiento real de la demostración.

### Prospectador y perfilamiento

`frontend/src/ProspectingWorkbench.jsx` y `backend/profiling.py` implementan criterios ICP guardados por usuario y versionados; perfil de empresa editable; razones de afinidad, fuentes, cobertura y faltantes; selección de cuentas; responsables vinculados a la empresa; creación de campaña con snapshot del ICP y motivo de selección para el aprobador. El score es porcentaje de coincidencias sobre criterios evaluados, no probabilidad de venta. No se inventan empleados, facturación ni evidencia web.

El flujo previo de campañas mantiene edición, aprobación humana, envío simulado, respuestas, exclusiones, reuniones y oportunidad. Se corrigieron dos defectos: campos de auditoría reenviados al editar perfiles y remontaje de formularios al cambiar estado de App. `Field` es estable; `Detail()` se usa como helper sin hooks; el Workbench se renderiza directamente.

### Contratos y archivos reales

`frontend/src/DocumentWorkspace.jsx`, `backend/document_routes.py` y `backend/document_worker.py` aceptan PDF, PNG, JPEG y WebP; guardan originales privados y metadatos en PostgreSQL; extraen texto de PDF y ejecutan OCR Tesseract español/inglés en imágenes o páginas escaneadas. Muestran preview por página, texto recuperado y propuestas con evidencia. La persona edita y confirma campos antes de aplicarlos.

Límites: 15 MiB, 40 páginas PDF, 20 millones de píxeles por imagen, un procesamiento simultáneo y 90 segundos globales. Los errores son explícitos. No hay textos ni hallazgos inventados para archivos reales. Claude API no está conectado; el lector local no realiza una evaluación jurídica por IA.

Los extractos para compartir archivos reales son redactados y confirmados por una persona. Una concesión de otro país permite solamente ese extracto: no original, páginas, texto, montos ni análisis reservados. Una nueva versión revoca la copia compartida anterior.

Existen botones «Probar PDF de ejemplo» y «Probar imagen de ejemplo». Ambos cargan archivos reales por el mismo endpoint que un archivo del usuario. Los activos están en `frontend/public/samples/`: PDF ficticio de tres páginas con marca Vertia y PNG rasterizado de su primera hoja. Monto: USD 12.500; contraparte Faro Retail SpA ficticia; inicio 2026-10-01; término 2027-12-31. No tienen efecto jurídico.

## Prioridad inmediata y defecto abierto

Codex detectó en la revisión visual que, al pasar de una versión PNG a un PDF anterior mediante el selector de documentos, los campos propuestos pueden aparecer vacíos aunque existan sus evidencias y valores en la respuesta de lectura. La carga inicial de PDF y PNG y la confirmación humana sí pasaron pruebas. El caso de cambiar de versión NO queda cubierto por ese resultado y sigue pendiente.

Reproducción confirmada: cargar el PDF de ejemplo; cargar después la imagen de ejemplo como nueva versión; volver a seleccionar el PDF en el historial; revisar los valores DOM de tipo, contraparte, monto y moneda sin escribir nada. La captura `artifacts/qa/workspaces/clm-pdf-comparison-viewport.png` muestra inputs vacíos; la captura equivalente de la imagen muestra valores. El agente frontend confirmó que no era solamente una imagen sin terminar de cargar.

Investigar sincronización de `selected`, `documentData`, `proposals`, `reviewFields`, efectos y cancelación de respuestas en `DocumentWorkspace.jsx`. Es una hipótesis de investigación, no una causa ya demostrada. Mantener aislados los borradores por documento y evitar que una respuesta atrasada borre valores del seleccionado. Revisar también cuál es el estado correcto de una versión anterior: se puede consultar su evidencia, pero el backend debe seguir rechazando aplicar una revisión obsoleta a la versión actual.

Antes de cerrar: aserción de interfaz de que el monto es `12500` y la contraparte tiene valor en el PDF seleccionado, sin rellenarlos durante el test; alternar PDF → PNG → PDF, recargar y repetir; verificar evidencia, página, edición, borradores y rechazo de revisión obsoleta. No basta comprobar `API.proposed_fields`. Revisar `docs/coordination/HANDOFF_BUG_DOCUMENTOS.md` si el agente alcanzó a dejar diagnóstico adicional. No publicar un arreglo parcial sin comprobar este recorrido.

## Pruebas y evidencia disponibles

- Backend: 15/15 pruebas en PostgreSQL 16 y OCR reales. Última publicación: 5,67 segundos. Incluyen carga, lectura, evidencia, revisión, versiones, permisos, archivos dañados y perfilamiento.
- Interfaz nueva: 38/38 comprobaciones en staging aislado, cero errores JS; PDF real, PNG OCR, confirmación humana, ICP, campañas, formularios que conservan datos ante error 400 y móvil 390 sin overflow. Ese resultado no significa que el defecto de cambio de versión esté resuelto.
- Presentación: pruebas locales de etapas, controles, entidades, países, móvil y movimiento reducido, sin errores de página.
- Producción privada: 401 anónimo y 200 autenticado en 14 rutas; hashes de frontend/documentos coinciden; PDF y PNG subidos por HTTPS, original íntegro, preview PNG, revisión persistida y original denegado a otro país. Servicios operativos; staging y túnel detenidos.
- Informes: `docs/coordination/qa-workspaces.md`, `infra-discovery.md`, `experiencia-v2-codex.md`, `claude-experiencia-v2.md` y `gemini.md`.
- Capturas/JSON internos: `artifacts/qa/experience-v2/`, `artifacts/qa/workspaces/` y `artifacts/qa/private-smoke/` si se completó. No están incluidos en Git.

## Continuación con Gemini y Claude

Claude Code asume la coordinación y el arreglo del defecto documental, manteniendo el alcance comercial. Gemini en Antigravity debe revisar de forma independiente la nueva portada, las animaciones, los modelos supuestos y los recorridos reales. Su revisión inicial está registrada en `gemini.md`; no hay que confundirla con la revisión de esta nueva versión.

El encargo compartido está en `docs/coordination/ENCARGO_EXPERIENCIA_V2.md` y `GEMINI.md`. Registrar hallazgos nuevos de Gemini en `gemini-experiencia-v2.md`. Ver `despacho-equipo-v2.md` si existe para el estado de una solicitud en GitHub; una solicitud publicada no acredita que Gemini ya la ejecutó. No existe aquí una herramienta de comunicación directa con su sesión de Antigravity; la coordinación acordada es carpeta y repositorio.

Claude participó realmente por Claude Code: propuestas, flujos, modelos, legibilidad y nueva revisión de narrativa. No hacen falta claves de producto para esa colaboración. No usar la suscripción de Claude Code como una API pública de la aplicación. Para conectar Claude API, prospectos, correo o firma se necesitan los accesos correspondientes de Vertia.

## Compilar probar y publicar

En Windows/Google Drive, no ejecutar `npm install` en `I:`: falla con EBADF. Usar `node frontend/build-local.cjs`; compila en `%TEMP%/vertia-frontend-codex` y copia `dist`. Ver `frontend/README.md` para las suites actuales y sus variables. Los ejecutables de Node/npm están disponibles localmente.

Para pruebas de interfaz de staging hay que levantar nuevamente una API aislada y su proxy; no apuntar inadvertidamente una suite que escribe a producción. `frontend/qa-presentation.cjs` usa un preview independiente en `127.0.0.1:5179`. `qa-private-smoke.cjs` utiliza credenciales en memoria y crea un caso sintético si hace falta. `qa-browser-v1.cjs` conserva la suite histórica de Gemini; no afirmar que sus 54 checks corresponden a la versión nueva. Los informes indican el entorno real de cada prueba.

Despliegue: `python infra/deploy-demo.py --publish --private`, con el Python que tenga `paramiko` instalado. Reutiliza el acceso SSH existente y conserva TLS y protección HTTP. Se corrigió el chequeo de salud para reintentar: el arranque tarda aproximadamente tres segundos y una espera fija de dos producía un falso fallo. Leer `infra/README.md` antes de publicar. Respaldar de forma consistente la base exclusiva Y el directorio privado de uploads antes de cambios de esquema. No borrar documentos del usuario ni reiniciar servicios ajenos.

El runtime documental está en `C:\Users\cueva\.cache\codex-runtimes\codex-primary-runtime`. Las propuestas se generaron con Pandoc y referencia MoAI; los Word se exportaron mediante Word instalado porque falta LibreOffice, y los PDF se rasterizaron con Poppler. No regenerar los presupuestos sin conservar sus cifras ni entregar documentos modificados sin revisión visual.

## Condiciones comerciales que se conservan

Prospectador USD 13.000 netos de referencia / 311,7235 UF netas. Contratos USD 30.000 / 719,3619 UF netas. IVA 19 % adicional. Cada iniciativa: 40 % inicial y seis cuotas del saldo, última cuota ajusta redondeo. Fuente única `docs/commercial/financials.json`. Contratación en UF, sin doble reajuste USD/UF.

MVP y roadmap separados: Prospectador 8–10 semanas; Contratos 12–16. Base regional para cinco países y piloto; ampliaciones regionales/avanzadas por separado. Logística postergada. AWS, PostgreSQL, Claude API Opus 5.5 mínimo, OCR, prospectos y todas las herramientas externas los habilita y paga Vertia, incluidos desarrollo, pruebas y producción. Soporte separado de las cuotas; garantía de defectos 60 días. Ver propuestas y anexos para límites propuestos.

## Orden de trabajo recomendado

1. Leer este handoff y el diagnóstico adicional; comprobar Git y diferencias locales antes de tocar archivos.
2. Corregir y demostrar el defecto de selección de versión, preservando ACL y revisión humana.
3. Recibir la revisión de Gemini de la nueva experiencia y coordinar cambios delimitados, sin trabajo concurrente sobre el mismo componente.
4. Compilar la versión definitiva; probar casos nuevos y regresiones relevantes en escritorio/móvil.
5. Publicar conservando acceso privado; comprobar HTTPS, carga real y persistencia, y registrar commit/hashes/resultados.
6. Entregar al usuario enlaces, ubicación de credenciales y una explicación breve de qué es real y qué servicios externos siguen simulados.
