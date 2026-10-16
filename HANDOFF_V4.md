# Handoff v4 — Rediseño para vender

16 de octubre de 2026. Escrito por Claude Code para la siguiente ventana de contexto de Claude. Lectura obligatoria antes de tocar código.

## 1. Veredicto del usuario (textual en lo esencial)

"La presentación está paupérrima, no calienta a nadie. Las imágenes no aportan nada, el scrollytelling no sirve de nada, no se siente una página viva con microinteracciones. El uso de la plataforma está complicado. El azul del modo oscuro no pega con el sidebar; el hover del sidebar y de la barra del módulo tienen un gris horrible. Creo que esto no lo voy a poder vender. Está demasiado plano, feo. El panel de seguimiento no se entiende, mucha letra. Le falta harto más talento."

Esto no es un problema de bugs: las pruebas pasan (ver §6). Es un problema de producto, de jerarquía visual y de oficio. La v3 explica mucho y muestra poco. La v4 debe hacer que un gerente de Vertia diga "lo quiero" en 3 minutos de demo.

## 2. Diagnóstico concreto de la v3

Presentación (`frontend/src/PresentationHub.jsx`, `presentation.css`, `sections/`, `teasers/`):
- 10 escenas de texto y mockups esquemáticos. No hay un momento "wow" ni el producto en uso; el scrollytelling solo desplaza bloques.
- Las imágenes GPT (ciudad costera con letreros, `frontend/public/media/*.webp`) son decorado genérico: no explican nada del producto ni de Vertia.
- Tipografía chica, mucho texto corrido, avisos de "simulado / demostración" repetidos.

Apps (`main.jsx`, `CommercialWorkspace.jsx`, `AnalyticsDashboard.jsx`, `ProspectingWorkbench.jsx`, `DocumentWorkspace.jsx`):
- Navegación de 11 secciones por app, organizada por módulo técnico y no por el trabajo del día. Cuesta saber dónde empezar.
- Pantallas que explican el proceso en párrafos en vez de dejar hacerlo. "Seguimiento" mezcla 4 pestañas, ritmo de envío, reglas y tablas: es ilegible.
- Avisos de simulación en cada pantalla: hacen que todo parezca maqueta. Basta un indicador global.
- Modo oscuro: superficies `#0e1924/#152534/#1c3042` (theme.css) que no conversan con el navy de marca del sidebar `#0a2240` (Global) / `#103b58` (Vertia).
- Hover y activo del sidebar `#ffffff0c/#ffffff0e` (styles.css) y pestañas de módulo grises: se ven sucios.
- Todo es plano: sin elevación, sin estados vivos, sin datos visuales protagonistas. Las microinteracciones son mínimas (`motion.css`).
- La base CSS es un parche sobre parche: `styles.css` (minificado, ~59 KB, tamaños remapeados), `legibility.css`, `theme.css`, `dark-overrides.css` (generado), `workbench.css`, `commercial.css`, `analytics.css`, `flows.css`. Rediseñar encima de esto es lento y frágil.

Lo que sí vale y se conserva (lógica, no estética):
- Backend: permisos por app, perfiles con nombre, Lusha simulado con créditos y topes, correo con ritmo del bot de Agustín, secuencias, bandeja, ICP y perfilamiento, analytics YoY/MoM/YTD, CLM con lectura real de PDF y escaneo simulado de imágenes por nombre, versiones documentales, accesos entre países, auditoría.
- Semilla v3 realista (480 empresas, 1.972 contactos, 235 oportunidades, 245 contratos, 18 meses con estacionalidad).
- Precios y condiciones: Prospectador USD 13.000 / 311,7235 UF; Contratos USD 30.000 / 719,3619 UF; IVA 19 % aparte; 40 % + 6 cuotas. Fuente única `docs/commercial/financials.json`.

## 3. Dirección propuesta para la v4 (a validar con el usuario antes de construir)

Principio: mostrar, no explicar. Cada pantalla responde una pregunta de una persona concreta y tiene una acción principal obvia.

Prospectador — el día de Agustín Silva:
- Inicio "Hoy": una cola de próximas acciones (responder a X, seguir a Y, revelar a Z, aprobar campaña) con un clic cada una; arriba 3–4 KPI con tendencia.
- Cuentas: tabla rica con afinidad visual; ficha 360 lateral (perfil, contactos, historia, oportunidades).
- Prospectar: buscador tipo Lusha con resultados en tarjetas, costo visible y revelar en lote.
- Bandeja: hilos estilo Outlook/Superhuman, compositor con borrador sugerido y estado claro; secuencias como línea de tiempo.
- Pipeline: kanban con arrastre, montos y forecast por columna.
- Métricas: un dashboard ejecutivo con selector de periodo.
- Máximo 5–6 entradas de navegación.

Contratos — el día de Phillipe y Gonzalo Oviedo:
- Inicio: vencimientos próximos, aprobaciones pendientes y obligaciones atrasadas como tarjetas accionables.
- Repositorio: tabla, filtros y vista kanban por estado.
- Ficha del contrato: documento a la izquierda y campos extraídos con evidencia a la derecha, con la línea de tiempo del ciclo; acciones según rol.
- Calendario de vencimientos y obligaciones.
- Configuración (Gonzalo): tipos, plantillas y flujos.

Sistema visual:
- Un solo sistema de tokens desde cero, con escala tipográfica (base 15–16 px), elevación, radios y tema por marca (Global rojo/navy; Vertia petróleo/lima).
- Modo oscuro derivado del navy de cada marca, para que el sidebar y el contenido sean la misma familia.
- Hover y activo con el color de marca en baja opacidad, nunca gris.
- Microinteracciones con propósito: hover de filas, arrastre con sombra, confirmaciones con pop, números que cambian al filtrar, skeletons, transiciones de panel (ver `docs/context/MOTION_GUIDE.md` §7).
- Un único indicador global "Entorno de demostración"; quitar los avisos repetidos de cada pantalla. Los adaptadores se rotulan como simulados solo donde se usan (Lusha, Microsoft 365, firma, Claude).

Presentación:
- Reemplazar el scrollytelling por una demo guiada corta: portada con promesa clara → "un día con la solución" para cada app, con la interfaz real animada (capturas o grabaciones del producto, no ilustraciones) → resultados y forma de trabajo → inversión → entrar a la demo.
- Idealmente, un video de 60–90 s por app con la UI real (lo puede producir Gemini; ver §4).
- Nada de imágenes decorativas genéricas. Cada visual debe mostrar el producto o un dato de Vertia.

## 4. Equipo y reparto (decisión del usuario: usar las mejores IAs, sin derrochar tokens)

Regla del usuario: **GPT no debe generar subagentes**; se come todos los tokens. Aplica a GPT 6.1 Sol y a cualquier agente: una sola sesión por encargo, con alcance de archivos y presupuesto acotados.

Asignar según fortalezas conocidas de cada familia y confirmar con el usuario las capacidades reales de estas versiones antes de depender de ellas:

| Rol | Agente | Encargo |
|---|---|---|
| Dirección de producto, UX, sistema de diseño en código, integración y QA final | Claude (esta continuidad) | Escribe el brief de diseño, define pantallas y flujos, implementa el frontend nuevo, revisa todo y mantiene pruebas |
| Exploración visual y movimiento | Gemini 4 Argon (Antigravity) | Moodboard y 2–3 direcciones visuales de alta fidelidad para "Hoy", Bandeja, Ficha de contrato y portada; crítica visual multimodal sobre capturas; video o product film de la UI real |
| Piezas acotadas de implementación y activos | GPT 6.1 Sol (Codex) | Tareas cerradas: endpoints o ajustes de backend que pida el diseño, componentes aislados con especificación cerrada, imágenes solo si muestran producto. Sin subagentes; un archivo o módulo por encargo |

Proceso para no repetir la v3:
1. Brief de diseño en una página (`docs/design/BRIEF_V4.md`): personas, 3 momentos que deben vender, pantallas y criterios. Aprobación del usuario.
2. Gemini produce direcciones visuales y el usuario elige una. Sin código antes de esto.
3. Claude construye el sistema de tokens y componentes nuevos en archivos nuevos (por ejemplo `frontend/src/ui/`), sin heredar `styles.css`, y migra pantalla por pantalla, empezando por "Hoy" del Prospectador.
4. Revisión visual con capturas a 1440 px después de cada pantalla. El usuario ve avances temprano.
5. GPT recibe solo encargos cerrados derivados del punto 3. Coordinación por `docs/coordination/` y nunca dos agentes sobre los mismos archivos.

Criterio de cierre: guion de demo de 3 minutos por app (`docs/design/DEMO_SCRIPT.md`) que el usuario pueda presentar sin explicar la interfaz.

## 5. Restricciones que siguen vigentes

- Solo escritorio (1440 px y superiores). Móvil no es criterio.
- Datos sintéticos verosímiles, sin "ficticia" en cada registro; correos con dominio `.example` (no se pueden enviar).
- Lusha, Microsoft 365, Claude API, POST y firma son simulados. No afirmar IA conectada ni firma legal. El PDF se lee de verdad; las imágenes usan escaneo simulado por nombre de archivo.
- Perfiles por defecto: Prospectador abre con Agustín Silva (Jefe Comercial, UY); Contratos con Gonzalo Oviedo (Jefe de Innovación, lectura regional y configuración; no edita contratos). Phillipe (solo nombre) es Regional; Santiago Ordoñez, Jefe IA; Enrique Escobar, Super admin.
- Logo oficial Global: `frontend/public/brand/global-oficial.png/.webp` (transparente). No generar logos con IA.
- No cambiar precios ni condiciones. No exponer credenciales. Acceso privado HTTP del sitio publicado intacto. No tocar servicios ni bases ajenas del VPS.
- Publicar, commit y push solo con aprobación explícita del usuario.

## 6. Estado técnico al cierre de esta ventana

Git: `main` sigue en `b884845` y es lo publicado en el VPS (versión `c87b74c`). Todo el trabajo v3 (Codex más las correcciones de Claude) está en la rama **`experiencia-v3`** (commit `f4262fc`), subida a GitHub y **no publicada**. Partir el rediseño v4 desde esa rama, en una rama nueva, por ejemplo `rediseno-v4`.

Correcciones de Claude sobre la v3 (sin commit):
- Contraste AA en ambos temas: `scripts/gen_dark_overrides.py` → `frontend/src/dark-overrides.css`; correcciones en `theme.css`.
- Semilla realista con estacionalidad, tendencia, correos nombre.apellido e historial de etapas (`backend/seed_v3.py`).
- Embudo coherente (`AnalyticsDashboard.jsx`).
- Regresión de `request_access` para perfiles de consulta (`backend/main.py`), con prueba nueva.
- Búsqueda de responsables para empresas nuevas (`backend/commercial.py`).
- Perfiles por defecto con la clave `vertia-demo-profile-v3-<app>`; las suites fijan su perfil.
- Esperas por condición en `qa-document-versions.cjs` y `qa-workspaces.cjs`.

Pruebas (staging local, base limpia, 16-10-2026): backend 34/34; `qa-workspaces` 26/26; `qa-workspaces-extra` 12/12; `qa-commercial-v3` 28/28; `qa-analytics-theme-v3` 51/51; `qa-document-versions` 31/31; `qa-presentation-v3` 550/550.

Staging local (Windows):
- PostgreSQL desechable: clúster en la carpeta temporal de la sesión anterior (`scratchpad/stage/pgdata`, puerto 5433, usuario `vertia`, sin clave, solo loopback). Si no existe, recrearlo con `initdb -U vertia -A trust` y `pg_ctl -o "-p 5433 -c listen_addresses=127.0.0.1"`. El servicio PostgreSQL del sistema (5432) no se usa.
- Python 3.13 con venv en `%TEMP%\vs` (pypdfium2 falla con 3.14 y con rutas largas).
- Servidor: `uvicorn backend.main:app --loop asyncio:SelectorEventLoop` con `FRONTEND_DIST` apuntando a un build local. En Windows, el bucle por defecto (Proactor) y el proxy de Vite cortan respuestas grandes de `/api/state` (ERR_CONNECTION_RESET); no ocurre en el VPS Linux.
- Compilar en una carpeta local, no en `I:` (npm falla con EBADF en la unidad compartida); `node frontend/build-local.cjs` lo hace.
- Las suites `qa-*.cjs` escriben datos: nunca apuntarlas a producción.

Publicación: `python infra/deploy-demo.py --publish --private` (ver `infra/README.md`). La semilla v3 es aditiva; antes de aplicarla en el VPS, respaldar la base `vertia_demo` y `UPLOAD_DIR`.

## 7. Primera tarea de la nueva ventana

1. Leer este archivo, `AGENTS.md`, `docs/BRIEF.md` y los requisitos originales (`../Iniciativa CRM Prospectador - Agus/`, `../Iniciativa Contratos - Gonzalo Phillipe/`).
2. Abrir la app en staging y recorrer cada pantalla con capturas, para formarse criterio propio (no basta con este diagnóstico).
3. Proponer al usuario, en una página, la dirección v4: momentos que venden, mapa de pantallas, sistema visual y reparto concreto para Gemini y GPT. Esperar su aprobación antes de construir.
