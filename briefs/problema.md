ID: problema
OWNER: Codex / presentation_v3
GOAL: Reconocer la falta de continuidad entre información, decisión y siguiente paso.
PIN: 140vh de recorrido además del viewport; móvil ×STORY.mobilePin=0.7, salvo escenas densas con lectura natural; movimiento reducido sin pin.
LOOK: fondos de tokens compartidos, tinta #0a2240; Global #ce0e2d, Vertia #ccff00 sobre tinta. Tema oscuro con tokens. Títulos Manrope/DM Sans 650, cuerpo Inter/Arial 400, etiquetas 700; tracking -0.045em en títulos y 0.14em en etiquetas. h2 hasta53/34px; cuerpo16/13px; etiquetas10/9px.
LAYOUT: Texto fijo a la izquierda y esquema a la derecha; móvil esquema debajo.
HERO: Tres fragmentos agrupados de un mismo circuito. El grupo se aproxima verticalmente 44→0px en p=.22→.72; un solo transform. Tokens ease,seg,lerp y STORY compartidos; no temporizadores.
SECONDARY: etiquetas y controles fijos, sin movimiento competidor.
AMBIENT: push ligado al progreso de hasta 2 %; sin partículas, brillo ni loops autónomos. El primer fotograma es una composición completa.
TEXT HOLD: 0→1 para la explicación; el esquema acompaña como un solo objeto.
HANDOFF: match cut conceptual: fragmentos a expediente. Sin fade de todas las capas.
BANNED extra: logos recreados, datos presentados como reales, ROI inventado, IA conectada o firma legal que son simuladas.
QA: cinco p=0/.25/.5/.75/1 en 1440×900 y 390×844, ambos temas para contraste. Reversibilidad, hook query y movimiento reducido. Extensión a 1920×1080 y 360×780. Se corrigió el h2 heredado de estilos globales para contraste blanco sobre azul.
ESTADO: implementación y QA local completos; evidencia en artifacts/qa/experience-v3/presentation. Certificación de 60 fps en hardware físico pendiente. No publicar sin aprobación.
