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
