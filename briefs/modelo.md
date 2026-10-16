ID: modelo
OWNER: Codex / presentation_v3
GOAL: Relacionar las entidades de cada solución y la responsabilidad de sus datos.
PIN: 160vh de recorrido además del viewport; móvil ×STORY.mobilePin=0.7, salvo escenas densas con lectura natural; movimiento reducido sin pin.
LOOK: fondos de tokens compartidos, tinta #0a2240; Global #ce0e2d, Vertia #ccff00 sobre tinta. Tema oscuro con tokens. Títulos Manrope/DM Sans 650, cuerpo Inter/Arial 400, etiquetas 700; tracking -0.045em en títulos y 0.14em en etiquetas. h253/33px; entidades16/14px; contexto13/12px.
LAYOUT: Diagrama a la izquierda y campos/contexto a la derecha; móvil columna sin pin.
HERO: Un esquema lógico interactivo. Escala0.98→1.00 en p=0→.18, luego reposo. La entidad se elige con controles accesibles. Tokens ease,seg,lerp y STORY compartidos; no temporizadores.
SECONDARY: etiquetas y controles fijos, sin movimiento competidor.
AMBIENT: push ligado al progreso de hasta 2 %; sin partículas, brillo ni loops autónomos. El primer fotograma es una composición completa.
TEXT HOLD: Título0→1; diagrama y campos.18→1.
HANDOFF: corte. Sin fade de todas las capas.
BANNED extra: logos recreados, datos presentados como reales, ROI inventado, IA conectada o firma legal que son simuladas.
QA: cinco p=0/.25/.5/.75/1 en 1440×900 y 390×844, ambos temas para contraste. Reversibilidad, hook query y movimiento reducido. Extensión a 1920×1080 y 360×780. Se verificó cambio a Contratos y selección de Documento/versión; modelo conceptual distinguido de JSONB.
ESTADO: implementación y QA local completos; evidencia en artifacts/qa/experience-v3/presentation. Certificación de 60 fps en hardware físico pendiente. No publicar sin aprobación.
