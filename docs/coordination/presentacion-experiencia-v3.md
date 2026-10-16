# Presentación de experiencia v3 · Codex

Fecha: 16-10-2026 (Chile). Implementación local. No publicada; requiere aprobación del usuario.

## Entrega

Diez escenas: `hero`, `problema`, `app1-intro`, `app1-wow`, `app2-intro`, `app2-wow`, `modelo`, `regional`, `alcance` y `cierre`. Los briefs de `briefs/` se completaron antes de programar. Cada módulo independiente de `frontend/src/sections/<id>/index.js` expone `id`, `pin`, `mount(el)` y `render(p)` mediante una fábrica común. El estado visual depende de `p`, sin temporizadores ni aleatoriedad. La portada registra las diez secciones en `window.__sections` y permite `window.freezeAt(id,p)` y `?s=<id>&p=<0..1>`.

Los textos principales están inmóviles. Los protagonistas que contienen texto narrativo entran en p=0→0,18 y permanecen inmóviles hasta 1. Los mockups, la imagen editorial y el esquema del problema tienen un desplazamiento acotado; no hay desplazamiento del titular. Los teasers usan cinco intervalos iguales, con cortes en 0 / 0,2 / 0,4 / 0,6 / 0,8. El último resultado conserva un intervalo de lectura, no aparece solamente en el último píxel del pin. Cada etapa tiene 72vh de recorrido en escritorio. Los botones permiten visitar directamente cualquier etapa.

La portada incluye imágenes GPT optimizadas por el coordinador, con dimensiones nativas declaradas (1599×900) y rótulo de ilustración: proceso comercial en hero, proceso contractual en su introducción y coordinación regional. Los prompts y la revisión de esos activos están en `frontend/public/media/prompts.json`. No se generaron ni recrearon logos. Se consume `global-oficial.webp` y el activo oficial existente de Vertia.

Se reutilizó el esquema narrativo de los documentos originales de Vertia —problema, piloto, validación, expansión y responsables—, sin importar cifras ni alcance de Tesorería. La narrativa comercial vigente proviene de `docs/BRIEF.md`, `docs/commercial/scope-roadmap.json`, `financials.json` y los flujos/modelos existentes. No se atribuye a Claude o Gemini una revisión de esta implementación.

## Contenido y condiciones conservadas

- Ciclo comercial completo: perfil y fuentes, descubrimiento y revelado, costo y deduplicación, borrador y aprobación, envío/escucha, corte del seguimiento, reunión y oportunidad. Agustín Silva, Santiago Ordoñez y Enrique Escobar con sus cargos aprobados.
- Ciclo contractual: solicitud/carga, lectura y versión, extracción con evidencia/revisión humana, revisión/aprobación, firma y obligaciones. Gonzalo Oviedo y Phillipe, sin inventar apellido.
- Modelos lógicos interactivos de las dos aplicaciones, relaciones 1:N / N:N, campos y supuestos por validar. Diferencia explícita entre el modelo propuesto y la persistencia JSONB de la demostración.
- Argentina, Chile, Perú, México y Uruguay. Se distingue la configuración base incluida de la activación productiva completa y su validación local. Piloto comercial Uruguay; piloto CLM por confirmar.
- MVP y ampliaciones diferenciados según el alcance comercial vigente. Sin vender el programa CLM regional completo dentro del MVP.
- USD 13.000 / 311,7235 UF y USD 30.000 / 719,3619 UF netos; IVA 19 % separado y total bruto; 40 % inicial y seis cuotas. Condiciones de UF, garantía, soporte y terceros separadas.
- Lusha, Microsoft 365, Claude API, POST y firma rotulados como simulados. Ningún envío real ni firma con efecto legal. PDF digital con extracción real; imágenes/documentos sin texto con escaneo simulado por nombre. La portada no llama ni modifica datos de la API.

## Revisión local

Scripts reproducibles: `frontend/qa-presentation-v3.cjs` y `frontend/qa-presentation-performance-v3.cjs`. Ambos se restringen al preview local; la primera suite rechaza un origen remoto. Evidencia en `artifacts/qa/experience-v3/presentation/`, ignorada por Git.

Ronda 1: 344/346 comprobaciones. Se detectaron dos fallos reales de lectura: el contenido de los teasers cambiaba la altura del dispositivo, desplazando los titulares entre p=0,25 / 0,5 / 0,75. Se corrigieron alturas de marco constantes en escritorio y móvil. Ronda 2: 346/346.

Ronda de contraste: se detectó el título oscuro heredado de estilos globales sobre la sección Problema y tres textos claros heredados sobre tarjetas de papel en tema oscuro. Se fijó el color local de esos elementos. Auditoría de todos los p y ambos temas: 546/546 comprobaciones antes de integrar imágenes. El último recorrido añade comprobación de imágenes y logo oficial; su resultado definitivo se anota al final.

Capturas previstas y revisadas: diez escenas × cinco progresos × escritorio 1440×900 y móvil 390×844, más veinte capturas oscuras y dos de movimiento reducido. Los contactos visuales agrupan las diez escenas y sus cinco progresos. No hay overflow horizontal. Se comprueba el mismo transform/etapa al recorrer cada p en sentido inverso, el hook query, el modelo de Contratos, el selector de país y `prefers-reduced-motion`.

En móvil las escenas densas usan lectura natural en una columna; hero, problema y los dos teasers conservan pin ×0,7. En movimiento reducido se elimina el pin y el desplazamiento, mostrando estados finales y conservando controles y contenido en el DOM.

### Notas por escena

| Escena | Progresos revisados | Nota y corrección |
|---|---|---|
| hero | 0 / 0,25 / 0,5 / 0,75 / 1 | Titular y CTA estables; dossier separado. Se acortó el rótulo del dossier móvil para evitar recorte de una palabra. |
| problema | cinco p | Corrección de contraste del título heredado; fragmentos agrupados sin mover la explicación. |
| app1-intro | cinco p | Cinco pasos completos, responsables y perfilamiento; entrada única y lectura inmóvil desde 0,18. |
| app1-wow | cinco p | Marco constante elimina desplazamiento del titular; cinco estados deterministas; último resultado con hold 0,8→1. |
| app2-intro | cinco p | Evidencia y validación humana explícitas; diferencia PDF/escaneo simulado; editorial rotulado. |
| app2-wow | cinco p | Marco constante; confirmación con evidencia, autorización de acceso y firma simulada identificadas. |
| modelo | cinco p | Entidades y detalle interactivo; diagrama estable durante lectura; versión conceptual diferenciada. |
| regional | cinco p | País y moneda visibles; selección funciona; configuración y activación diferenciadas. |
| alcance | cinco p | Incluido y ampliaciones separados; mobile sin pin para no recortar el contenido. |
| cierre | cinco p | Inversión exacta, IVA y pagos; CTAs reales a las dos apps y propuestas; mobile sin pin. |

## Rendimiento y límites de la evidencia

Se guardó una traza Chrome DevTools en `chrome-performance-trace.json` y un muestreo de 239 frames en `performance.json`. Mediana de frame: 18 ms; p95: 18,5 ms, seis frames sobre 25 ms durante scroll bidireccional. El mismo entorno entrega mediana de 18 ms en una página completamente en blanco y en la portada en reposo (p95 18,5 / 18,1 ms). La cadencia medida está limitada por este entorno; no acredita 60 fps en un laptop medio.

En la traza de scroll: p95 Layout 1,044 ms, UpdateLayoutTree 2,691 ms y Paint 0,901 ms. Se anima transform; `will-change` solo se aplica en el rango activo. No se incorporaron bibliotecas de 3D, scroll ni video que no aporten a estos recorridos HTML. La certificación de 60 fps sobre hardware físico queda pendiente, explícitamente.

No se ejecutaron pruebas que escriban contra producción. No se alteraron backend, documentos cargados ni DocumentWorkspace. La compilación integrada y las regresiones de las aplicaciones corresponden al coordinador; no se afirman aquí resultados de pruebas que no ejecutó este agente.

## Resultado definitivo con assets y composición final

`node frontend/qa-presentation-v3.cjs`: **550/550 comprobaciones**, cero errores JS y cero recursos HTTP fallidos. Incluye las tres imágenes editoriales cargadas a su resolución nativa y el logo oficial. Se revisaron las 100 capturas de cinco progresos mediante hojas de contacto, las 20 capturas oscuras y los estados de movimiento reducido. El control interno de las diez pantallas de teaser no encuentra texto fuera del marco a 1440×900 o 390×844.

Extensión a 1920×1080 y 360×780: 100 estados inspeccionados, sin overflow horizontal ni overflow interno en los mockups. En 360px los teasers terminan a y=775,92 dentro de los 780px del viewport; se ajustaron padding y controles para mantener todo accesible. La composición wide conserva un padding de marco constante. Evidencia adicional: `extra-viewports.json` y seis capturas `extra_*.png`.

Durante la revisión visual se eliminó también la traslación vertical del dispositivo y de las hojas narrativas: podía invadir sus controles o las notas inferiores en p=0. El hero se desplaza lateralmente, el esquema del problema verticalmente y los demás sujetos usan un acercamiento de 2 %. Las hojas con texto concluyen su entrada en p=0,18. Los teasers se mantienen en tres niveles tipográficos para jerarquía y legibilidad. Cada cambio fue seguido por el último pase 550/550.

Archivos principales: `frontend/src/PresentationHub.jsx`, `presentation.css`, `sections/`, `teasers/`, diez `briefs/*.md`, `coord/status.md` y los dos scripts de QA. El coordinador integra y compila; no hay commit ni publicación realizados por este agente.
