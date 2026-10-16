ID: app1-intro
OWNER: Codex / presentation_v3
GOAL: Entender el ciclo comercial completo y quién responde en cada paso.
PIN: 160vh de recorrido además del viewport; móvil ×STORY.mobilePin=0.7, salvo escenas densas con lectura natural; movimiento reducido sin pin.
LOOK: fondos de tokens compartidos, tinta #0a2240; Global #ce0e2d, Vertia #ccff00 sobre tinta. Tema oscuro con tokens. Títulos Manrope/DM Sans 650, cuerpo Inter/Arial 400, etiquetas 700; tracking -0.045em en títulos y 0.14em en etiquetas. h243/34px; copia16/13px; lista12px y etiquetas10px.
LAYOUT: Columna de contexto y responsables junto a cinco pasos numerados. Móvil lectura natural sin pin.
HERO: La hoja de proceso comercial. Escala0.98→1.00 únicamente en p=0→.18; después inmóvil para lectura. Tokens ease,seg,lerp y STORY compartidos; no temporizadores.
SECONDARY: etiquetas y controles fijos, sin movimiento competidor.
AMBIENT: push ligado al progreso de hasta 2 %; sin partículas, brillo ni loops autónomos. El primer fotograma es una composición completa.
TEXT HOLD: Titular0→1; hoja de proceso.18→1, sin desplazamiento.
HANDOFF: corte. Sin fade de todas las capas.
BANNED extra: logos recreados, datos presentados como reales, ROI inventado, IA conectada o firma legal que son simuladas.
QA: cinco p=0/.25/.5/.75/1 en 1440×900 y 390×844, ambos temas para contraste. Reversibilidad, hook query y movimiento reducido. Extensión a 1920×1080 y 360×780. Cinco decisiones, entradas/resultados y cargos reales; afinidad no es probabilidad de venta.
ESTADO: implementación y QA local completos; evidencia en artifacts/qa/experience-v3/presentation. Certificación de 60 fps en hardware físico pendiente. No publicar sin aprobación.
