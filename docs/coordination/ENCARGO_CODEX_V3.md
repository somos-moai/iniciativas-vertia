# Encargo para Codex (GPT) — Experiencia v3: de maqueta a producto convincente

16 de octubre de 2026. Instrucción directa del usuario, consolidada por Claude Code. Destinatario: Codex como implementador principal, con sus subagentes. Gemini en Antigravity mantiene solo la revisión independiente, que sigue pendiente (ver `ENCARGO_EXPERIENCIA_V2.md`); Gemini no tenía asignada esta implementación.

## Lo que dijo el usuario

La app se ve pobre y la presentación no sorprende. El logo está mal; el tablero de oportunidades no funciona; los créditos no funcionan bien y no se ve como Lusha; el envío de correos debe parecerse al bot de Agustín. Hay que agregar los perfiles con nombre y cargo reales. El Prospectador necesita muchísimos más datos, más realistas y sin la palabra "ficticia" en cada registro. El perfilamiento debe mostrar cosas distintas por empresa. Los dashboards deben ser potentes, con comparaciones YoY, MoM y YTD, y tienen que impresionar. Hay que evaluar el modo oscuro. La presentación es muy simple: debe usar imágenes generadas para verse mucho más profesional.

Leer antes de empezar: `AGENTS.md`, `HANDOFF_CLAUDE.md`, `docs/context/MOTION_GUIDE.md` (secciones 4, 7 y 8 para las apps; la guía completa para la presentación), `../Iniciativa CRM Prospectador - Agus/Bot_Comercial_GVP_para_IT.md`, `../Iniciativa CRM Prospectador - Agus/Requerimientos_Prospectador_CRM_Vertia.md`, `../Iniciativa Contratos - Gonzalo Phillipe/CLM_Global_Especificacion_Tecnica.md`, `I:/Unidades compartidas/Vertia/docs/Guion_Presentacion.md` y `I:/Unidades compartidas/Vertia/propuestas/proyecto.md`.

## 1. Obligatorio: perfiles con nombre y cargo

Hoy `USERS` es una sola lista sintética compartida. Debe pasar a ser una lista de perfiles por aplicación, con ACL en el backend y los perfiles actuales de prueba de permisos conservados con nombres verosímiles.

Prospectador:

| Nombre | Cargo | Rol propuesto | Alcance propuesto |
|---|---|---|---|
| Agustín Silva | Jefe Comercial | manager | Uruguay (piloto); aprueba campañas, ve su equipo |
| Santiago Ordoñez | Jefe IA | ia_lead (nuevo) | Configura agentes, plantillas y reglas de IA; ve métricas; no aprueba envíos |
| Enrique Escobar | Super admin | superadmin (nuevo) | Todos los países, configuración, usuarios y créditos |

Gestión contractual (CLM):

| Nombre | Cargo | Rol propuesto |
|---|---|---|
| Gonzalo Oviedo | Jefe de Innovación | admin funcional: tipos, plantillas y flujos de aprobación; visión regional de lectura |
| Phillipe (solo nombre; el usuario no conoce el apellido, no inventarlo) | Regional | regional: todos los países |

Mantener el rótulo "Perfil de demostración · no SSO". Los roles nuevos necesitan permisos explícitos en el backend y pruebas de ACL. Roles y alcances confirmados por el usuario el 16-10-2026, incluidos Jefe IA y Jefe de Innovación tal como están arriba.

## 2. Logo

El usuario entregó el logo oficial de Global Vía Pública con fondo transparente: `frontend/public/brand/global-oficial.png` y `global-oficial.webp` (721×207, recortados al contenido, sin otra modificación). Reemplazar el `global.webp` anterior (400×114, que se veía pixelado) en la app, la presentación y las propuestas. Mostrarlo sin caja blanca cuando el fondo lo permita y respetar su área de resguardo. No redibujar ni generar logos con IA. Revisar con el mismo criterio el logo de Vertia.

## 3. Prospectador: que funcione como el trabajo real

### Tablero de oportunidades
Hoy no funciona. Debe permitir arrastrar y soltar entre etapas, persistiendo con `set_opportunity`; usar teclado y menú como alternativa accesible; mostrar total y monto por columna, probabilidad o forecast por etapa, filtros por ejecutivo, país y periodo, y abrir la ficha de la oportunidad con su historial. Toda acción se persiste y se audita.

### Créditos y Lusha (simulado, pero creíble)
Reproducir la experiencia de Lusha como adaptador simulado y rotulado:
- Búsqueda con filtros: país, cargo, seniority, departamento, empresa o dominio, industria y tamaño.
- Resultados con correo y teléfono enmascarados.
- Revelar uno o varios con vista previa del costo antes de confirmar.
- Saldo del plan, consumo por usuario y por corrida, e historial de consumo.
- Reglas del bot de Agustín: no pagar dos veces el mismo contacto; tope de 600 créditos por corrida; límites de 50 consultas por minuto, 150 por hora y 1.500 por día (con espera ante un 429 simulado); solo cargos útiles: gerentes de marketing, de marca y generales, con Uruguay primero.
- Hoy el saldo agregado (1.249 / 1.250) confunde: mostrar saldo por cartera y de la organización, con el contexto claro.

### Correo como el bot de Agustín (simulado, sin salida real)
- Lista de "a quién escribir hoy", ordenada por rubro, estado, correo válido y días sin contacto, con su motivo visible.
- Primer correo armado según rubro y estado, en tono local (uruguayo para el piloto) y con un pedido concreto. El ejecutivo lo edita y lo envía; la jefatura aprueba los envíos masivos.
- Secuencias de seguimiento con días de espera. Lectura simulada de la bandeja cada 10 minutos: respuestas, rebotes, respuestas automáticas y "no contactar", con sugerencia de estado.
- Vista tipo bandeja (hilos estilo Outlook) y registro en el historial del CRM.
- Ritmo visible: 8 s entre correos, pausa de 45 s cada 15, solo entre 08:00 y 20:00, y al menos 7 días entre dos contactos a la misma persona.
- Rotular como "Microsoft 365 simulado". Ningún mensaje sale de la aplicación.

### Perfilamiento con variedad real
Cada empresa debe verse distinta: señales según su rubro (aperturas, campañas, temporada, expansión), cobertura y faltantes diferentes, fuentes por campo, y un puntaje que varíe y se explique, con una visualización por criterio. No repetir la misma ficha con otro nombre. El puntaje sigue siendo coincidencia con criterios, no probabilidad de venta.

## 4. Datos: mucho más volumen y realismo

- Prospectador:
  - Más de 400 empresas y más de 1.500 contactos en los cinco países, con énfasis en Uruguay.
  - Entre 12 y 18 meses de historia: campañas, envíos, respuestas, rebotes, reuniones y oportunidades con montos en moneda local y USD.
  - Esa historia debe permitir comparaciones YoY, MoM y YTD.
- CLM:
  - Más de 200 contratos de tipos variados, con contrapartes, montos en moneda local, versiones y obligaciones.
  - Vencimientos a 30, 60 y 90 días, renovaciones e historial de aprobaciones con sus tiempos.
- Formato de los datos:
  - Nombres de empresas y personas verosímiles e inventados, nunca empresas reales ni nombres de otros clientes de MoAI.
  - Quitar el sufijo "Ficticia" de cada registro, como pidió el usuario. Mantener un solo aviso global y discreto de "Entorno de demostración".
- Correos con dominio reservado (`.example` u otro no enrutable): así no pueden enviarse nunca. Mostrarlos de forma discreta. Este punto conserva la regla de `AGENTS.md` sobre datos sintéticos; si el usuario prefiere otro formato, debe decidirlo explícitamente.
- La semilla debe ser determinística (con semilla fija), versionada y migrable sin borrar los documentos cargados por el usuario. Respaldar la base y `UPLOAD_DIR` antes de resembrar en el VPS.

## 5. Dashboards que impresionen

- Prospectador:
  - Comparaciones YoY, MoM y YTD con un selector de periodo.
  - Tendencias de 12 a 18 meses, embudo con conversión por etapa y desempeño por ejecutivo, país y rubro.
  - Rendimiento de campañas (respuesta, rebote, reuniones), pipeline y forecast, y créditos consumidos versus resultados.
- CLM:
  - Valor bajo gestión y contratos por estado, país y tipo.
  - Vencimientos a 30, 60 y 90 días, cumplimiento de obligaciones y tiempo de ciclo por etapa.
  - Cuellos de botella de aprobación y renovaciones en riesgo.
- Reglas comunes:
  - Las métricas se calculan desde los registros, no con valores fijos.
  - Cada cifra es trazable a un filtro de la lista correspondiente.
  - Los contadores animados solo en un dato principal (MOTION_GUIDE §4).

## 6. Diseño general, modo oscuro e imágenes

- Subir el nivel visual: jerarquía tipográfica, densidad útil, gráficos reales, estados vacíos con intención y un momento coreografiado por app (MOTION_GUIDE §7). Respetar la lista de prohibidos (§4).
- Modo oscuro: evaluarlo e implementarlo con tokens para las dos apps y la presentación, con selector persistente, `prefers-color-scheme` y contraste AA (≥ 4,5:1) en todos los estados.
- Imágenes generadas (GPT):
  - Para la presentación y las portadas: escenas del proceso comercial y contractual, renders de producto en marcos de dispositivo e ilustraciones de cada etapa.
  - Estilo consistente con las marcas, sin degradados morados, brillos ni estética genérica de IA.
  - No generar logos ni personas reconocibles, ni datos o capturas que aparenten ser reales. Rotular las imágenes como ilustrativas cuando corresponda.
  - Guardar los prompts usados y las imágenes en `frontend/public/media/`, optimizadas (WebP/AVIF, con tamaños declarados).

## 7. Presentación

Rehacer la portada como un scrollytelling según la MOTION_GUIDE completa: `render(p)` por sección, hook `?s=<id>&p=` para QA, un protagonista por escena y el texto fijo mientras se lee. Incluir un teaser "wow" por app (product film o mockup vivo) y la narrativa acordada en el guion de presentación de Vertia y en `propuestas/proyecto.md`. Debe contar:
- El problema.
- Cómo se trabaja con cada solución, con sus flujos completos y modelos de datos.
- El MVP versus las ampliaciones.
- El roadmap de cinco países.
- La inversión, sin cambiar cifras: USD 13.000 / 311,7235 UF y USD 30.000 / 719,3619 UF netos, IVA 19 % aparte, 40 % de anticipo y seis cuotas.

Llenar un brief por escena en `briefs/` antes de programarla.

## Restricciones que se mantienen

- No revertir el arreglo de versiones documentales (`DocumentWorkspace.jsx`: borradores por versión y lectura ligada al documento) ni el escaneo simulado por nombre de archivo. Mantener en verde `frontend/qa-document-versions.cjs` (31/31), `qa-workspaces.cjs`, `qa-workspaces-extra.cjs` y `backend/tests`.
- Adaptadores simulados rotulados: Lusha, Microsoft 365, Claude API, POST y firma. No afirmar IA conectada ni firma legal.
- Acceso privado HTTP intacto. No exponer credenciales. No tocar servicios ni bases ajenas del VPS. Probar en staging aislado; nunca correr suites que escriben contra producción.
- Precios, forma de pago y alcance comercial sin cambios.

## Cierre esperado

- Pruebas de interfaz nuevas en escritorio (1440) y móvil (390): tablero arrastrable y persistente, revelación con créditos y topes, secuencia y bandeja de correo, perfiles nuevos con su ACL, dashboards con periodos, modo oscuro con contraste, y presentación congelable por escena.
- Capturas de QA de cada recorrido.
- Registrar archivos, decisiones, pruebas reales y pendientes en `docs/coordination/codex-experiencia-v3.md`.
- Publicar solo con la aprobación del usuario.
- Claude Code queda disponible para revisar narrativa, datos y consistencia comercial. Gemini, para la revisión independiente de interfaz cuando el usuario la ejecute en Antigravity.

## Decisiones del usuario (16-10-2026)

1. Phillipe se muestra solo con su nombre; no hay apellido.
2. Logo oficial entregado (ver sección 2).
3. Roles de Santiago Ordoñez (Jefe IA) y Gonzalo Oviedo (Jefe de Innovación) aprobados como están propuestos.

## Decisión del usuario (16-10-2026): solo escritorio

La demostración y la presentación se evalúan solo en escritorio (1440 px y superiores). La versión móvil no es criterio de cierre: no invertir más trabajo en ella ni bloquear entregas por pruebas de 390 px; mantener sin romper lo que ya existe.
