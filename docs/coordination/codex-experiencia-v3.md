# Experiencia v3 · registro de ejecución de Codex

16 de octubre de 2026. Encargo directo del usuario: `ENCARGO_CODEX_V3.md`. **Publicación pendiente de aprobación del usuario.** No se autorizan commits, push ni cambios del servicio publicado mediante este registro.

## Estado inicial y decisiones

- Se leyeron AGENTS, BRIEF, API_CONTRACT, HANDOFF_CLAUDE, MOTION_GUIDE y requisitos originales de ambas iniciativas. El guion y proyecto externos corresponden a Tesorería: se toma su estructura narrativa, sin trasladar ese alcance ni sus montos.
- Cambios previos preservados: `docs/coordination/claude.md`, MOTION_GUIDE, encargo v3 y logos oficiales recién aportados. Se conserva DocumentWorkspace y sus borradores por versión.
- Trabajo asignado a tres subagentes Codex según autorización del encargo: backend/datos/ACL; módulos comerciales del frontend; presentación y briefs. El agente principal integra shell, dashboards, tema, imágenes, propuestas y QA. No se atribuye esta ejecución a Claude o Gemini.
- Se aplican las habilidades build-cinematic-3d-scrollytelling e imagegen. Los adaptadores externos de las aplicaciones siguen simulados; imágenes de presentación por la herramienta incorporada, sin API de pago del proyecto.
- Se creó un clúster PostgreSQL 17 **local nuevo**, en loopback puerto 55489, con base `vertia_v3_staging` y almacenamiento temporal propio. Ninguna suite de escritura apunta a producción. No se leyó ni modificó una base ajena.

## En curso

- Migración aditiva versionada y datos deterministas, permisos explícitos por aplicación, créditos y correo del bot.
- Tablero accesible persistente, búsqueda y revelación con costo previo, bandeja y secuencias.
- Dashboards calculados desde registros y filtros trazables, tema persistente y logo oficial.
- Presentación con briefs previos, escenas congelables, mockups vivos e imágenes ilustrativas.

## Verificaciones

Se completará con comandos, resultados reales, capturas y limitaciones observadas. Las asignaciones anteriores no acreditan implementación ni pruebas aprobadas.

## Publicación

No realizada. Antes de resembrar el VPS se requieren respaldo consistente de PostgreSQL y UPLOAD_DIR y aprobación del usuario para publicar. Hasta entonces se trabaja exclusivamente en staging local.
