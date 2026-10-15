# Claude

@AGENTS.md
@docs/BRIEF.md
@docs/tasks/CLAUDE_PROPOSALS.md

## Alcance
- Escribes solo en docs/commercial/ y docs/coordination/claude.md.
- docs/commercial/financials.json es de Codex: solo lectura. Si falta un valor, no lo inventes; anótalo en docs/coordination/claude.md.
- No editar frontend/, backend/ ni infra/. Archivos fuera del repo (Presupuestador MoAI, propuestas y guion de Vertia): solo lectura.
- No sobrescribir archivos de docs/commercial/ creados por otro agente sin registrarlo en docs/coordination/claude.md.
- No ejecutar git; el coordinador hace commits.

## Reglas comerciales
- Cifras: fuente única BRIEF + financials.json (USD 987,03 / UF 41.162,73 al 15-10-2026). No usar 978,61.
- Separar siempre implementación, financiación (cuotas), soporte y proveedores externos (los paga Vertia).
- Leer también docs/context/. El roadmap usa las categorías incluido | ampliacion, iguales a la colección roadmap descrita en docs/coordination/codex-backend.md.

## Cierre
- Registrar en docs/coordination/claude.md: entregables, supuestos, inconsistencias detectadas y pendientes para Codex.
- No enviar ni publicar propuestas.
