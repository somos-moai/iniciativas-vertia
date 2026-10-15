# Codex — implementación e integración frontend

## Entrega

React 19 + Vite 6 + Lucide, CSS propio y marcas oficiales. Se implementó el frontend como respaldo de ejecución mientras el coordinador resuelve la conectividad de Gemini para su revisión real. Este archivo no atribuye implementación a Gemini.

- `frontend/src/main.jsx`: hub, dos aplicaciones y flujos conectados a FastAPI.
- `frontend/src/styles.css`: dos temas, dashboard, tablas, formularios, modales, drawer y adaptación móvil a 390 px.
- `frontend/package.json`, `package-lock.json`, `vite.config.js`, `index.html`.
- `frontend/build-local.cjs`: instala y compila en un caché temporal local y copia `dist/` al repositorio. La extracción concurrente de npm en la unidad compartida I: produjo errores EBADF; este mecanismo evita esa limitación.

## Recorridos

Prospectador: resumen con métricas; cartera de empresas y contactos; alta y edición; importación de contactos con deduplicación del backend; búsqueda y revelación de prospectos; créditos; campañas con contenido editable y generación simulada; aprobación humana; envío simulado; respuesta y cancelación de seguimiento; exclusión; reuniones; oportunidades con etapas; conciliación POST simulada; integraciones y roadmap.

Contratos: resumen; catálogo y búsqueda; filtros de estado; alta; documentos sintéticos y versiones; análisis simulado con evidencia y página; original y copia saneada a través de descarga autenticada por perfil; revisión, rechazo, aprobación, firma simulada y activación; obligaciones y evidencia; antecedentes; solicitudes de acceso y concesión temporal; auditoría; enmiendas y renovación identificadas como vista evolutiva; integraciones y roadmap.

Todas las acciones usan `POST /api/actions` y refrescan el estado desde PostgreSQL. No hay un fixture ni estado offline como sustituto. Los selectores de país filtran solo registros entregados por el servidor. Los perfiles son demostrativos y se identifican como «NO SSO». Los botones protegidos quedan deshabilitados según rol y transición; la autorización definitiva reside en FastAPI. Los errores del servidor se muestran al usuario.

Los borradores editados deben guardarse antes de aprobar o enviar; regenerar el borrador invalida su aprobación en el backend. El frontend no permite que una aprobación sobre contenido almacenado parezca aprobar cambios todavía sin guardar.

Los enlaces comerciales apuntan a `/propuestas/prospectador.html` y `/propuestas/contratos.html`. Los documentos contractuales se recuperan mediante `fetch` con `X-Demo-User`, se abren desde un blob y no exponen una URL pública sin control.

## Verificación

`node frontend/build-local.cjs`: build de producción correcto. Vite transformó 1.573 módulos; JS ~322 KB / 94 KB gzip, CSS ~58 KB / 13 KB gzip. Build final inicial: `index-C1aqcs3B.js`.

La revisión de navegador real y capturas desktop/móvil se realiza con el coordinador después de publicar en el VPS correcto. No se afirma todavía que esa revisión esté aprobada. El build no reemplaza pruebas de interfaz.

## Límites explícitos

Datos sintéticos; sin APIs externas, correo, firma legal ni IA real. PostgreSQL real; selector de perfil no equivale a autenticación productiva. La bitácora demo no se presenta como WORM. Monedas no se agregan como si fueran equivalentes. Infraestructura, APIs y licencias de producción corresponden a Vertia. Logística fuera de esta etapa.
