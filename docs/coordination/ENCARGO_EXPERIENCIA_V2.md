# Encargo conjunto de experiencia y flujo real

15 de octubre de 2026. Instrucción directa del usuario para Codex, Claude Code y Gemini en Antigravity.

El usuario confía en el equipo y pide que esa confianza se refleje en una demostración convincente y funcional. La primera entrega no muestra suficiente profundidad. El estándar de esta revisión es que Vertia entienda qué compra, cómo funciona cada proceso, qué datos necesita y por qué el alcance propuesto tiene valor. El trabajo de cada agente se conserva y se integra; no competimos por autoría ni sustituimos evidencia por efectos visuales.

## Resultado esperado

Antes de entrar a las maquetas, el mismo sitio explica ambos proyectos, sus MVP, su roadmap regional y los supuestos de sus modelos de datos. Las animaciones enseñan el recorrido y las decisiones: entradas, responsables, controles y resultados. El visitante puede avanzar, detener y explorar cada etapa.

El Prospectador debe permitir definir y guardar el perfil de cliente ideal, documentar el perfil de una empresa, ver razones y faltantes y convertir ese trabajo en una campaña sometida a aprobación. Los proveedores de datos, correo e IA se identifican según su conexión real; no se inventan resultados externos.

Contratos debe recibir PDF e imágenes reales, extraer su texto o ejecutar OCR, mostrar páginas y evidencia, proponer campos editables y exigir revisión humana. El archivo y su lectura persisten, con permisos de servidor. El lector OCR local no se presenta como un análisis de Claude. El flujo de aprobación y firma continúa desde el expediente y conserva la distinción de firma simulada.

## Coordinación

- Codex coordinador: presentación inicial `frontend/src/PresentationHub.jsx` y `presentation.css`, narrativa, integración y revisión final.
- Codex frontend: espacios funcionales de perfilamiento y carga documental; integración en `main.jsx`, preservando `flows.jsx`, estilos y revisión de Claude/Gemini.
- Codex backend: carga, almacenamiento, extracción, OCR, propuestas con evidencia, ACL y pruebas; persistencia del perfilamiento acordada con frontend.
- Infraestructura: dependencias OCR y almacenamiento privado; despliegue aislado y protección del acceso cuando se habiliten archivos reales.
- Claude Code: sus flujos y modelos existentes se reutilizan; se solicita revisión de narrativa, supuestos y calidad de evidencia en `claude-experiencia-v2.md`.
- Gemini en Antigravity: revisar nueva presentación, animaciones, legibilidad y recorridos reales; registrar hallazgos en `gemini-experiencia-v2.md`. Este encargo está disponible en la carpeta y repositorio; no se registra como ejecutado hasta recibir su resultado.

## Criterios de cierre

No basta compilar. Probar en navegador escritorio y móvil, cargar un PDF de texto y una imagen sintética legible, contrastar el texto extraído con su contenido, editar y confirmar campos, revisar la fuente por página y completar un ciclo comercial y contractual. Validar los accesos, persistencia al recargar, animaciones pausables, movimiento reducido y documentación que coincida con lo publicado.

Precios, forma de pago, responsabilidad de terceros y separación MVP versus ampliaciones se conservan. Esta mejora de demostración no amplía automáticamente el contrato productivo.
