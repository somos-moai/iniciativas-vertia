# Integración de la nueva experiencia Vertia

15 de octubre de 2026. Implementación basada en la instrucción de reforzar explicación, flujos, modelos supuestos y funcionamiento verificable. Se preservaron los avances de Claude Code y Gemini en Antigravity.

## Presentación antes de las aplicaciones

La portada incluye explicación de ambos proyectos, dos recorridos de cinco etapas con reproducción, pausa y controles manuales, entradas, decisiones, responsables y resultados. Las ilustraciones se identifican como recorridos explicativos. Después aparecen modelos conceptuales explorables, relaciones, supuestos por validar, configuración regional y roadmap con separación de incluido y ampliación. Los accesos a las aplicaciones se presentan al final del recorrido y en navegación.

Se probó en Edge con Playwright: cambios de etapa, controles anterior/siguiente, selección de entidades, cambio de país, viewport 390 sin desbordamiento, movimiento reducido y ausencia de errores de página. Se revisaron capturas de escritorio y móvil. Se corrigió un color de título heredado que reducía el contraste y se verificó la versión corregida.

## Procesos funcionales

El Prospectador guarda el perfil de cliente ideal y sus versiones. La ficha de empresa documenta fuentes, coincidencias y faltantes; el criterio se conserva en la campaña para su aprobación. El porcentaje es coincidencia de criterios evaluados, no probabilidad de venta ni inteligencia externa conectada.

Contratos incorpora archivos y lectura reales, previews y texto por página, propuestas editables y confirmación humana. Se eliminaron porcentajes de confianza de las reglas de extracción que podían confundirse con precisión validada. La revisión del original y la evidencia permanecen visibles. Una nueva versión revoca el extracto anterior; las concesiones entre países permiten únicamente el extracto confirmado.

Las pruebas de interfaz identificaron y corrigieron un desmontaje de formularios causado por componentes definidos dentro de App y un reenvío incorrecto de campos de auditoría al editar perfiles. Se comprobó que un error de validación conserve los campos escritos.

## Archivos de prueba

Se creó un PDF sintético real de tres páginas con marca Vertia y condiciones ficticias, y una imagen rasterizada de su primera página. Los botones de prueba cargan esos archivos por el mismo endpoint que un archivo del usuario. No inyectan texto ni resultados prefabricados. Se inspeccionaron las tres páginas del PDF y su texto; el frontend verificó extracción y OCR de ambos archivos.

## Colaboración

Claude Code aportó flujos, modelo y legibilidad en su sesión interactiva; además produjo una revisión nueva de narrativa y criterios verificables, registrada en claude-experiencia-v2.md. Gemini en Antigravity registró su revisión inicial y correcciones de pruebas en gemini.md. El nuevo encargo conjunto se conserva en ENCARGO_EXPERIENCIA_V2.md; no se atribuye una segunda revisión de Gemini sin su resultado.

Las claves de acceso se conservan fuera del repositorio. El sitio requiere autenticación antes de habilitar archivos reales. Claude API, correo, proveedor de prospectos, POST y firma permanecen desconectados o simulados; lectura PDF y OCR local son reales. Los precios y las condiciones de las propuestas productivas no se amplían automáticamente por esta mejora de demostración.
