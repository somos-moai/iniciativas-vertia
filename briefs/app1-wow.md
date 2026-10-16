ID: app1-wow
OWNER: Codex / presentation_v3
GOAL: Ver cómo una cuenta se transforma en conversación, reunión y oportunidad bajo control humano.
PIN: 360vh de recorrido además del viewport; móvil ×STORY.mobilePin=0.7, salvo escenas densas con lectura natural; movimiento reducido sin pin.
LOOK: fondos de tokens compartidos, tinta #0a2240; Global #ce0e2d, Vertia #ccff00 sobre tinta. Tema oscuro con tokens. Títulos Manrope/DM Sans 650, cuerpo Inter/Arial 400, etiquetas 700; tracking -0.045em en títulos y 0.14em en etiquetas. Tres niveles37/21/10px; móvil29/19/9px; 360px26/19/9px.
LAYOUT: Cabecera fija y mockup debajo, una pantalla activa. Cinco controles manuales fuera del dispositivo.
HERO: Un único dispositivo con mockup HTML comercial. Escala0.98→1.00 en p=.22→.72; cortes de estado en0/.2/.4/.6/.8. No desplazar el marco hacia los controles. Tokens ease,seg,lerp y STORY compartidos; no temporizadores.
SECONDARY: etiquetas y controles fijos, sin movimiento competidor.
AMBIENT: push ligado al progreso de hasta 2 %; sin partículas, brillo ni loops autónomos. El primer fotograma es una composición completa.
TEXT HOLD: Cabecera0→1; cada pantalla conserva72 vh; la quinta se lee entre.8→1.
HANDOFF: match cut: ficha a pantalla. Sin fade de todas las capas.
BANNED extra: logos recreados, datos presentados como reales, ROI inventado, IA conectada o firma legal que son simuladas.
QA: cinco p=0/.25/.5/.75/1 en 1440×900 y 390×844, ambos temas para contraste. Reversibilidad, hook query y movimiento reducido. Extensión a 1920×1080 y 360×780. Marco constante; contraste de tarjetas papel independiente del tema; cinco etapas completas.
ESTADO: implementación y QA local completos; evidencia en artifacts/qa/experience-v3/presentation. Certificación de 60 fps en hardware físico pendiente. No publicar sin aprobación.
