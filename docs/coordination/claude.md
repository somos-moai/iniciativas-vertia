# Revisión mediante Claude Code

Participación real mediante Claude Code con la cuenta Team de MoAI y selector de modelo `opus`, 15 de octubre de 2026. Codex entregó contexto y consolidó los borradores. La invocación concluyó con `end_turn`; no se verificó el identificador expandido del alias. La API del producto es un requisito separado y no se utilizó para generar los documentos. Los límites concretos, la conciliación financiera y el render final fueron revisados posteriormente por Codex.

# Revisión de consistencia — Claude

Fecha: 15 de octubre de 2026

Destino: revisión de Codex antes de render a Word/PDF.

## Alcance de esta revisión

Entregables producidos: docs/commercial/prospectador.md, docs/commercial/contratos.md, docs/commercial/supuestos.md y los datos de alcance/roadmap. No se editó frontend, backend ni infraestructura. No se ejecutó git. No se generó Word ni PDF; el render queda a cargo de Codex con los runtimes.

## Consistencia con el brief y las instrucciones

- Precios aprobados respetados: Prospectador USD 13.000 netos / UF 311,7235; Contratos USD 30.000 netos / UF 719,3619. No se pidió nueva confirmación de precios ni de modelo de pago, por estar ya aprobados.
- Esquema de pago 40% anticipo + 6 cuotas, 7 hitos. No se usó 40/30/30.
- Importes UF a 4 decimales tomados íntegramente de financials.json, incluida la última cuota con ajuste de redondeo (Prospectador cuota 6: 31,1721/5,9225/37,0946; Contratos cuota 6: 71,9361/13,6678/85,6039).
- Conversión congelada 15-10-2026: UF 41.162,73 y dólar 987,03. No se usó la conversión antigua 978,61. UF como unidad de contratación; USD referencial; pago en CLP al valor UF de vencimiento como condición explícita.
- IVA 19% mostrado separado en neto/IVA/bruto, en USD y UF.
- Terceros (AWS, PostgreSQL, Claude Opus 5.5, OCR, Lusha, M365, firma, Entra ID) habilitados y pagados por Vertia; fuera de honorarios MoAI.

## Delimitación de alcance

- Prospectador: núcleo + MVP con Agus en Uruguay + consolidación con equipo; POST solo diseño, mapeo e interfaz simple sobre API documentada, o intercambio de archivos validado si no hay API; WhatsApp/LinkedIn como roadmap. Configuración regional base 5 países.
- Contratos: precio 30k cubre MVP documental + workflow acotado + una firma; se excluye explícitamente la especificación regional completa (~960 h) y las integraciones avanzadas. Config regional 5 países desde inicio, piloto 1 país, validación legal por Vertia.
- Ambas incluyen matriz de incluido vs futuro.
- Límites (un proveedor de datos, un proveedor de firma, catálogo y migración acotados) redactados como condiciones propuestas, no como aceptaciones existentes.

## Requisitos de forma

- Estructura por propuesta: resumen autosuficiente, problema, un día con la solución, alcance con límites, fases MVP + consolidación/flujo, objetivos regionales y separación de ampliaciones, responsabilidades Cliente/MoAI, prueba de aceptación, inversión USD/UF neto/IVA/bruto, calendario de 7 hitos, soporte separado con horas/SLA, garantía 60 días, propiedad/licencias/cambio de alcance, vigencia 30 días y contacto somos@mo-ai.cl.
- Sin negritas en el cuerpo; jerarquía por encabezados, según la referencia.
- Sin ROI inventado, sin métricas como resultados logrados, sin nombres de otros clientes, sin NDA.
- Hallazgos y capacidades de demostración rotulados como demo, no producto final.
- Justificación de precio por resultados verificables, no por cantidad de pantallas.
- Extensión por propuesta dentro del rango objetivo para 6 a 9 páginas al render.

## Puntos para Codex

- Confirmar que financials.json es la fuente única de los importes al momento del render; si se actualizan indicadores, regenerar tablas, no editarlas a mano.
- Coordinar el render a Word/PDF con identidad MoAI + marca cliente (Prospectador Global azul marino/rojo; Contratos Vertia azul petróleo/lima), formal directivo.
- No enviar ni publicar las propuestas a clientes de forma automática; quedan listas para revisión.

## Pendientes abiertos

- Cerrar en levantamiento los límites propuestos (números de plantillas, volumen de migración, reglas de aprobación, catálogo de tipos).
- Validar acceso API real de Claude Opus 5.5 y permisos de Graph antes de comprometer inicio de fases.

## Trabajo en curso — Claude Code (sesión interactiva del coordinador), 15-10-2026 19:30

Por instrucción directa del usuario, Claude implementa en frontend la sección "Flujo y modelo de datos" para ambas maquetas y mejora de legibilidad (tamaños de letra). Para no pisar trabajo concurrente:
- Código nuevo en archivos nuevos: frontend/src/flows.jsx y frontend/src/legibility.css.
- frontend/src/main.jsx: solo importación, una entrada de navegación por app y el render de la sección.
- frontend/src/styles.css: solo remapeo mecánico de valores font-size (legibilidad); sin otros cambios.
- No se edita backend, infra ni scripts. No se publica ni se ejecuta git.
Estado: terminado 15-10-2026 ~20:05. main.jsx queda libre.

### Resultado

Archivos nuevos: frontend/src/flows.jsx, frontend/src/flows.css, frontend/src/legibility.css, docs/commercial/flujos-y-modelo-datos.md.
Archivos modificados: frontend/src/main.jsx (import de legibility.css y FlowModel, icono Workflow, entrada "Flujo y datos" en NAV de ambas apps, render de la sección, etiqueta "Flujo y modelo de datos" en las tarjetas del hub); frontend/src/styles.css (351 valores font-size remapeados: 4-7px→11, 8→12, 9→13, 10→14, 11→14.5, 12→15, 13→16, 14→16.5, 15→17, 16→17.5, 17→18, 18→19, 19→20; ≥20 sin cambio).

Sección "Flujo y datos" (ambas apps): pestaña Flujo completo con 10 etapas mapeadas a las acciones reales del backend (quién, acción, qué registra, regla, adaptador simulado, conteo en vivo desde /api/state y botón a la sección de la demo) y embudo en vivo; pestaña Modelo de datos simulado con entidades, campos PK/FK, conteos visibles por perfil, relaciones resaltables y aclaración de almacenamiento JSONB vs modelo productivo. Solo lectura: no ejecuta acciones.

Verificación: vite build de producción correcto en un espacio local aparte (no se tocó frontend/dist). Revisión en navegador contra la API pública (solo GET, sin acciones) en 1440 px y 390 px: ambas apps, todas las secciones sin scroll horizontal; enlace etapa→entidad y resaltado de relaciones funcionan.

### Pendientes para Codex

1. Compilar con frontend/build-local.cjs y publicar en el VPS; no se publicó nada.
2. scripts/build_proposals.py:32 elimina toda la puntuación de los títulos de las propuestas (comas, rayas, paréntesis). Los HTML/DOCX/PDF publicados muestran por ejemplo "Identidad roles y cartera" y "Calendario de pagos 7 hitos". Corregir y regenerar.
3. Evaluar incorporar docs/commercial/flujos-y-modelo-datos.md como anexo en el paquete de entrega.
4. La base pública contiene registros de QA visibles para el cliente (por ejemplo "QA Acuerdo regional 1792103016612", "QA Horizonte ..."). Limpiar o resembrar antes de mostrar la demo.
5. Revisar con QA de navegador propio los recorridos existentes con la nueva escala tipográfica.

## Para Codex: MOTION_GUIDE.md disponible — 15-10-2026

El usuario compartió C:/Users/cueva/AppData/Local/Temp/MOTION_GUIDE.md (carpeta temporal: puede borrarse; si se adopta, copiarlo al repo o a la presentación). Es una guía de movimiento para la presentación scrollytelling (3 agentes, render(p) por scroll, pins, teasers en video). No está escrita para estas maquetas y no cambia los roles de AGENTS.md.

Evaluación de Claude: sirve para mejorar las maquetas solo en sus secciones 4, 7 y 8; el resto (scroll, pins, freezeAt, briefs, teasers, roles A/B/C) aplica a la presentación, no a las apps.

Aplicable a frontend, con hallazgos concretos en el código actual:
1. Sección 7, feedback: no existe estado presionado en botones (.btn:active). Agregar escala 0.97 en 100 ms; movimientos de UI 200–500 ms; listas con stagger 40–80 ms solo al cargar.
2. Sección 7, carga: se usa LoaderCircle con animación spin (4 usos). La guía pide skeleton con brillo lento en vez de spinners genéricos, al menos en la carga inicial de /api/state.
3. Sección 4, prohibidos: banderas emoji como íconos (FLAGS en main.jsx, 4 usos) y la decoración "orbital" del banner de Descubrir prospectos. Reemplazar banderas por código de país en texto o SVG; simplificar el orbital.
4. Sección 7, un momento coreografiado por app: Prospectador al aprobar/enviar campaña; Contratos al registrar firma/activar. Único lugar con pop (1.0→1.08→1.0 en 100 ms). Todo lo demás sobrio.
5. Sección 8: contraste ≥ 4.5:1 (legibility.css ya corrige textos secundarios y badges); prefers-reduced-motion ya existe en styles.css, mantenerlo para cualquier animación nueva; 390 px como ciudadano de primera clase.

Propuesta de reparto: Claude puede implementar 1–4 en archivos propios (legibility.css / motion.css nuevo) más ajustes acotados en main.jsx, avisando aquí antes; Codex compila, hace QA y publica. Pendiente de decisión del usuario.

## Trabajo en curso — Claude, 15-10-2026 22:07: mejoras MOTION_GUIDE 1–4 y títulos de propuestas

Aprobado por el usuario. Archivos: frontend/src/motion.css (nuevo), frontend/src/main.jsx (ajustes acotados: carga con skeleton, país sin emoji, momento de app), estilos del banner orbital en motion.css; scripts/build_proposals.py (solo la normalización de títulos) y regeneración de deliverables/. No se publica en el VPS ni se ejecuta git.
Estado: terminado 15-10-2026 ~22:15. Archivos liberados.

### Resultado MOTION_GUIDE 1–4

- motion.css (nuevo): tokens de curvas y duraciones de la guía; botones, pestañas y menú con escala 0.97 en 100 ms y vuelta con resorte (solo transform); foco visible.
- Carga: la carga inicial muestra un skeleton con brillo lineal lento en lugar del spinner; "Guardando cambios" usa una barra lineal; el botón de guardar ya no muestra spinner. LoaderCircle y la clase spinning ya no se usan.
- País: se eliminó el mapa FLAGS de emojis. Selectores muestran el nombre; pills y barras muestran el código (CL, UY…) como etiqueta de texto.
- Descubrir prospectos: el orbital decorativo (anillos y brillo) se reemplazó por los cuatro pasos reales del descubrimiento.
- Momento por app: send_campaign (Prospectador) y sign_contract (Contratos) muestran un aviso destacado con título, entrada premium de 400 ms y pop 1.0→1.08→1.0 de 100 ms en el ícono; el envío informa enviados y omitidos desde la respuesta del servidor. El resto de los avisos sigue igual.
- No se agregó stagger en listas para no caer en el patrón prohibido de aparición en cascada; prefers-reduced-motion desactiva todo lo nuevo.
- Verificación: vite build correcto; navegador contra la API pública en 1440 y 390 px, todas las secciones de ambas apps sin scroll horizontal; el envío se probó con la respuesta POST simulada en el navegador, sin escribir en la base.

### Resultado títulos de propuestas

- scripts/build_proposals.py: eliminada la línea que quitaba la puntuación de los títulos. No hay otra lógica que dependa del texto de esos títulos.
- Regenerados con el runtime de Codex: deliverables/*.md, *.html, *.docx (build_proposals.py), *.pdf (export_word.vbs con Word, 7 páginas cada una), QA con qa_proposals.py (totales de pagos conciliados, páginas en artifacts/qa). Solo cambiaron 8 títulos por propuesta.
- scripts/package_handoff.py: el paquete incluye docs/commercial/flujos-y-modelo-datos.md; zip regenerado con 14 archivos y control de credenciales aprobado.
- Respaldo previo en %TEMP%/deliverables-bak-claude.

### Pendiente para Codex

1. Compilar el frontend (build-local.cjs) y publicarlo.
2. Subir deliverables/ actualizados al VPS (/home/moai/iniciativas-vertia/deliverables): cambiaron los hashes de HTML, DOCX, PDF y zip.
3. Limpiar los registros QA visibles en la base pública.
