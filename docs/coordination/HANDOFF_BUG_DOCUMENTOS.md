# Defecto abierto de selección de versiones documentales

Registro de Codex para la continuación solicitada a Claude Code y Gemini. No hay un arreglo validado ni se ha publicado un hotfix.

## Evidencia confirmada

En `artifacts/qa/workspaces/clm-pdf-comparison-viewport.png` el PDF de ejemplo está seleccionado y se muestran sus evidencias, pero los inputs de tipo, contraparte, monto y moneda aparecen vacíos. En `clm-real-image-comparison-viewport.png`, correspondiente a la imagen posterior, los valores sí están poblados. El agente frontend confirmó antes de la interrupción que el problema aparece al cambiar de PNG a un PDF anterior; no era únicamente una captura tomada antes de cargar la imagen.

La carga inicial, extracción, OCR y revisión humana pasaron pruebas. Las 38 comprobaciones anteriores no afirmaban ni verificaban los valores DOM de los inputs al regresar a una versión anterior. No usar ese resultado como prueba de corrección de este defecto.

## Cómo retomarlo

1. Entrar con la credencial privada y perfil regional a un expediente en borrador.
2. En Documentos, usar «Probar PDF de ejemplo», esperar lectura completa y comprobar sus seis propuestas.
3. Usar «Probar imagen de ejemplo» para crear una nueva versión, esperar el OCR y comprobar sus propuestas.
4. Volver al PDF con el selector de documentos/versiones.
5. Sin teclear, consultar valores DOM: monto esperado 12500, contraparte Faro Retail SpA ficticia, moneda USD y fechas 2026-10-01 / 2027-12-31. Contrastar la respuesta `/text` con el estado del formulario.

Investigar `selected`, `documentData`, `proposals`, `reviewFields`, efectos de inicialización y respuestas asíncronas obsoletas en `frontend/src/DocumentWorkspace.jsx`. Esa es una guía de investigación, no una causa demostrada. Si la versión no es la vigente, el formulario debe indicar su condición y el backend debe impedir aplicar sus campos sobre el expediente actual; no eliminar esa protección para hacer pasar una prueba.

El usuario pidió handoff durante la investigación. Los subagentes frontend/backend quedaron interrumpidos; no hay un diagnóstico adicional confirmado. Consultar `git status` antes de continuar y no suponer que existen cambios de un hotfix.

## Cierre requerido

Prueba de interfaz específica de PDF → PNG → PDF con valores DOM sin rellenarlos en el test; repetir tras recargar, comprobar evidencias y páginas correctas, preservar edición ante errores y mantener el rechazo de revisión obsoleta. Compilar y publicar solo después de verificar el caso, registrando hashes y resultado. El build actualmente publicado conserva este defecto: VONnwKLm.js / CTvZoLKH.css.

## Resolución — Claude Code, 16-10-2026

Causa, corrección y pruebas registradas en docs/coordination/claude.md ("Resultado — defecto de versiones documentales"). Prueba específica: frontend/qa-document-versions.cjs (31/31 en staging local aislado; falla contra el componente anterior). Pendiente: publicación aprobada por el usuario y verificación en el sitio privado.
