# Revisión de experiencia mediante Claude Code

Ejecución real con selector opus, 15 octubre 2026.

# Crítica de producto — Experiencia y flujo real Vertia

## Lectura del encargo
La primera maqueta se queda en lo visual y no demuestra profundidad. El estándar correcto no es "compila", sino que Vertia entienda qué compra, cómo funciona cada proceso, qué datos necesita y por qué el alcance tiene valor. Para transmitir confianza con trabajo verificable, la demostración debe exhibir el proceso completo con evidencia real donde corresponde (extracción y OCR local) y marcar con honestidad lo simulado (IA externa, firma, correo, calendario, proveedor de datos, POST). El riesgo mayor es presentar adaptadores demo como integraciones reales o el OCR local como un análisis de Claude; eso destruye la credibilidad que buscamos.

## 8 criterios verificables (comprobables en navegador)
1. **Presentación previa en el mismo HTML**: antes de las maquetas, un solo sitio explica ambos proyectos, sus MVP, roadmap regional y supuestos de datos; se puede avanzar, pausar y explorar cada etapa.
2. **Animaciones que explican el proceso**: cada etapa muestra entradas, responsables, controles y resultados; respetan movimiento reducido y son pausables en escritorio y móvil.
3. **Lectura real de PDF de texto**: al cargar un PDF, el texto extraído coincide con su contenido y se puede contrastar por página.
4. **OCR local real de imagen**: una imagen sintética legible produce texto contrastable, etiquetado explícitamente como OCR local — no como análisis de Claude ni de IA externa.
5. **Campos propuestos con evidencia y revisión humana**: los campos extraídos son editables, remiten a su página de origen y exigen confirmación humana antes de persistir.
6. **Persistencia y auditoría al recargar**: contrato, documento, versiones y análisis permanecen tras recargar; cada acción deja registro de actor, acción, entidad y país.
7. **ACL de servidor por país/cartera**: un perfil de otro país solo ve la referencia; request_access/grant_access concede solo lectura por 1 a 30 días y caduca.
8. **Honestidad de servicios**: IA externa, firma, correo, calendario, Lusha y POST figuran como simulados/desconectados; solo extracción y OCR local se presentan como reales, con archivo persistido bajo permisos de servidor.

## Supuestos de datos — Prospectador
Distinguir siempre **modelo lógico propuesto** (producción: tablas, FK, índices, RLS) del **JSONB demo** (`vertia_demo_records`, `kind`, `data` JSONB).
1. **Cartera por propietario**: demo guarda `owner_id`/`country` dentro del JSONB y filtra en aplicación; lógico propuesto: FK a ejecutivo + RLS por cartera e índices por país.
2. **Unicidad de correo de contacto**: demo valida el único en lógica sobre JSONB; lógico propuesto: constraint `UNIQUE(country,email)` indexado.
3. **Créditos de revelación (máx. 250/cartera, 1 por contacto)**: demo persiste `revealed`/`credit_cost` en el registro; lógico propuesto: tabla de consumos transaccional con saldo.
4. **Huella de aprobación de campaña**: demo guarda `approval_hash` en `data`; lógico propuesto: tabla de aprobaciones con versión de contenido inmutable y timestamp.
5. **Regionalidad base 5 países**: demo mantiene `country` por registro; lógico propuesto: catálogo país + permisos por país/ejecutivo con retención.

## Supuestos de datos — Contratos
1. **Contrato como agregado**: demo embebe documentos, historial, análisis, firma y enmiendas en el `data` JSONB del contrato; lógico propuesto: tablas separadas con FK `contract_id` e índices.
2. **Versionado de documentos**: demo incrementa `version` dentro del documento; lógico propuesto: tabla de versiones con hash del archivo y FK.
3. **Análisis con evidencia por página**: demo guarda `extracted_fields`/`findings` y `source_version` en JSONB; lógico propuesto: tabla de hallazgos con referencia a página/offset y versión analizada.
4. **Copia saneada**: demo lista `removed_fields` (monto, contraparte, cuentas, identificadores fiscales); lógico propuesto: política de clasificación + registro de redacción auditable.
5. **Acceso temporal entre países**: demo guarda la solicitud con `expires_at` en JSONB; lógico propuesto: tabla de permisos temporales con RLS por país/sociedad y caducidad por proceso programado.

El modelo relacional de producción —claves foráneas, índices, cifrado, retención y auditoría inmutable— se define en el levantamiento con Vertia; este anexo describe el modelo lógico demostrado, no el esquema productivo.

## Narrativa sugerida

## Iniciativas Vertia — recorrido de la demostración

Esta demostración reúne dos productos independientes en una misma plataforma para que Vertia vea, antes de entrar a cada maqueta, qué compra, cómo funciona cada proceso, qué datos necesita y dónde termina el alcance incluido. Las animaciones son pausables y explorables: muestran entradas, responsables, controles y resultados de cada etapa, no efectos decorativos. Los datos son sintéticos y persisten en PostgreSQL; cada acción valida perfil y país en el servidor.

### Prospectador comercial (USD 13.000 netos de referencia)

Ordena el trabajo comercial de principio a fin en cinco etapas:
1. **Cartera y datos base**: cada ejecutivo administra empresas y contactos propios, con importación validada y control de duplicados.
2. **Descubrimiento y revelación**: búsqueda de candidatos y revelación por crédito, respetando el consumo del proveedor de datos.
3. **Campaña y aprobación humana**: el borrador se somete a aprobación; editar el contenido revoca la aprobación y exige una nueva.
4. **Envío controlado y respuestas**: se omiten excluidos y quienes ya respondieron; se registra el seguimiento y nada sale fuera de la app.
5. **Oportunidad y conciliación**: la conversación se convierte en oportunidad y en actividad conciliable.

En esta demostración, el proveedor de datos, correo, calendario, IA externa y la conciliación POST están simulados y se identifican como tales. El valor está en el flujo gobernado: trazabilidad por ejecutivo, aprobación humana obligatoria y configuración regional base para los cinco países.

### Gestión Contractual (USD 30.000 netos de referencia)

Cubre el ciclo documental y un flujo contractual acotado, también en cinco etapas:
1. **Alta y documento**: contrato con referencia por país, versiones e historial.
2. **Extracción y lectura real**: se cargan PDF e imágenes reales; la extracción de texto y el OCR se ejecutan de forma local y real, con la fuente visible por página. El lector OCR no es un análisis de Claude.
3. **Revisión humana y copia saneada**: se proponen campos editables con evidencia y se construye una copia que excluye datos sensibles.
4. **Aprobación y firma**: aprobación por niveles y un proveedor de firma. En la demostración la firma permanece simulada y sin efecto legal.
5. **Activación, obligaciones y acceso entre países**: el expediente activo registra obligaciones con evidencia y concede acceso temporal de solo lectura bajo solicitud.

El archivo real y su lectura persisten con permisos de servidor. El valor está en la evidencia verificable: cada campo propuesto remite a su página de origen y ninguna decisión avanza sin revisión humana.

### Roadmap y entrega regional

Los plazos parten cuando están disponibles accesos, muestras y responsables. Prospectador: 8 a 10 semanas, con MVP en Uruguay y consolidación hasta cinco ejecutivos. Contratos: 12 a 16 semanas, con MVP documental primero, luego flujo y firma, y estabilización del piloto. La preparación regional base de los cinco países —Argentina, Chile, Perú, México y Uruguay— queda incluida en el modelo y los permisos; el despliegue masivo, la validación local de reglas y los conectores adicionales se ordenan como ampliaciones cotizables por país u ola.

Las iniciativas se contratan y aceptan por separado; esta mejora de la demostración no amplía el contrato productivo. Precios, forma de pago, garantía y la separación entre MVP y ampliaciones se conservan tal como fueron presentados.