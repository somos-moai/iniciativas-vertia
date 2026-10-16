ID: regional
OWNER: Codex / presentation_v3
GOAL: Separar configuración base regional y activación productiva validada país por país.
PIN: 160vh de recorrido además del viewport; móvil ×STORY.mobilePin=0.7, salvo escenas densas con lectura natural; movimiento reducido sin pin.
LOOK: fondos de tokens compartidos, tinta #0a2240; Global #ce0e2d, Vertia #ccff00 sobre tinta. Tema oscuro con tokens. Títulos Manrope/DM Sans 650, cuerpo Inter/Arial 400, etiquetas 700; tracking -0.045em en títulos y 0.14em en etiquetas. h253/33px; cuerpo16/13px; contexto13/12px.
LAYOUT: Contexto y selector a la izquierda; editorial y ruta a la derecha. Móvil natural en una columna.
HERO: Editorial regional y ruta de cinco países. Push0.98→1.00 en p=.22→.72; país y moneda cambian por decisión del usuario. Tokens ease,seg,lerp y STORY compartidos; no temporizadores.
SECONDARY: etiquetas y controles fijos, sin movimiento competidor.
AMBIENT: push ligado al progreso de hasta 2 %; sin partículas, brillo ni loops autónomos. El primer fotograma es una composición completa.
TEXT HOLD: 0→1 para explicación y condiciones.
HANDOFF: corte. Sin fade de todas las capas.
BANNED extra: logos recreados, datos presentados como reales, ROI inventado, IA conectada o firma legal que son simuladas.
QA: cinco p=0/.25/.5/.75/1 en 1440×900 y 390×844, ambos temas para contraste. Reversibilidad, hook query y movimiento reducido. Extensión a 1920×1080 y 360×780. Argentina, Chile, Perú, México y Uruguay; piloto comercial UY, país piloto CLM por confirmar.
ESTADO: implementación y QA local completos; evidencia en artifacts/qa/experience-v3/presentation. Certificación de 60 fps en hardware físico pendiente. No publicar sin aprobación.
