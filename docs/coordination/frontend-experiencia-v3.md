# Frontend comercial · experiencia v3

16-10-2026. Implementación del subagente Codex frontend, coordinada con el implementador principal y backend. No se publicó ni se usó producción para pruebas.

## Archivos y puntos de integración

- `frontend/src/CommercialWorkspace.jsx` importa su `commercial.css` y exporta `OpportunityBoard`, `EnrichmentWorkspace`, `MailWorkspace`, `CommercialSettings` y alias `AISettings`.
- `OpportunityBoard({S,action,busy,readOnly,openForm,country,query})`: usa `S.opportunities`, mantiene filtros propios, conserva IDs y persiste movimientos mediante `set_opportunity(entity_id,{status})`. Alternativas: selector por tarjeta y Alt + flechas; Enter abre ficha, con historial. Montos separados por moneda; forecast USD solo suma registros con equivalencia explícita. Se muestra cantidad sin conversión.
- `EnrichmentWorkspace({S,action,busy,readOnly})`: filtros de país/cargo/seniority/departamento/empresa/dominio/industria/tamaño; datos enmascarados; selección múltiple; `preview_reveal` sin gasto y confirmación `reveal_contacts`; saldo de `credits.wallet`, organización, carteras, consumo y corridas. Respeta resultados de `last_search.result_ids`. Escucha `vertia-api-error` para la cuenta regresiva 429 y bloqueo temporal. La API vuelve a validar saldo, deduplicación, ACL y topes.
- `MailWorkspace({S,action,busy,readOnly,openForm,openDetail,initialTab})`: pestañas `today`, `inbox`, `sequences`, `campaigns`. Primer correo persistido mediante `draft_email`, revisado/editar y envío `send_email`; borrador de campaña masiva sujeto a aprobación humana. Hilos desde `inbox[].messages`; lectura explícita y temporizador de 10 minutos, ritmo visible y exclusiones. Secuencias persistidas `save_sequence`, días entre 7 y 90, hasta seis pasos, aprobación del próximo seguimiento `simulate_sequence`, y cola de correo programado.
- `CommercialSettings`: configuración de tono, cargos, instrucciones, presupuesto y habilitación del adaptador Claude simulado; solo Jefe IA/administración pueden guardar. Superadmin puede guardar límites de organización y carteras por `configure_credits`.
- `ProspectingWorkbench.jsx`: visualización nueva por criterio comprobable, distinguiendo coincidencia/revisión/faltante, con `role=meter` y texto equivalente. Corrige presentación de empleados/presupuesto nulos como faltantes. Se mantienen selectores y recorrido previo de QA.
- `workbench.css`: estilos acotados de los criterios, sin modificar los estilos documentales existentes.

## Decisiones

Los tokens de los módulos comerciales se alinean con el tema central: `--panel`, `--surface`, `--text`, `--muted`, `--border`, `--accent`. El tablero usa probabilidades de etapa 10/25/60/80/100/0, acordadas con backend. No se suman monedas locales sin equivalencia USD explícita. Los adaptadores Lusha/Microsoft 365/Claude/POST conservan rótulos simulados. El momento de confirmación se concentra en el guardado/revelación; se respeta movimiento reducido.

Los diálogos tienen foco inicial, Escape, ciclo de Tab y devolución del foco. Las tablas densas y el tablero desplazan internamente en 390 px. Los errores de backend conservan los datos del formulario.

## Verificación realizada

- Parseo JSX mediante esbuild instalado en caché local: `CommercialWorkspace.jsx` y `ProspectingWorkbench.jsx`, correcto.
- `frontend/qa-commercial-v3.cjs`, guardada con restricción explícita a localhost: primera ejecución integrada completó 7 comprobaciones reales de tablero: ausencia de desborde a 1440, registros, arrastrar, selector alternativo, Alt+flechas, persistencia tras recarga y ficha con historial. Capturas: `artifacts/qa/experience-v3/commercial/opportunity-board-1440.png` y `opportunity-history-1440.png`.
- La prueba detectó que una tarjeta movida podía quedar fuera de las primeras doce al llegar a una columna extensa; se corrigió el orden por `updated_at` y última tarjeta movida, y se verificó nuevamente arrastre/selector/teclado/recarga.
- La continuación de la suite quedó detenida al ejecutar búsqueda de contactos: el indicador de guardado no terminó en 90 segundos. Otro navegador contra el snapshot estático 5181 permaneció cargando `/api/state` más de 20 segundos. El coordinador y agente backend fueron informados; se investigó transporte Uvicorn/Windows y pool antes de seguir. No se atribuyen resultados verdes de créditos/correo/móvil todavía.
- La suite incluye las pruebas pendientes de preview sin gasto, revelación deduplicada, saldos, 429 con espera, borrador editado y envío simulado persistido, secuencia aprobada a cola, bandeja, configuración Jefe IA y móvil 390. Debe volver a ejecutarse con el transporte de staging estabilizado.

## Restricciones conservadas

Sin cambios en `main.jsx`, `styles.css`, presentación, `motion.*`, `DocumentWorkspace.jsx` ni backend por parte de este subagente. No se realizaron commits, push, llamadas a APIs comerciales externas ni publicación.
