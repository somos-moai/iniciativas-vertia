# Requerimientos del prospectador y CRM comercial de Vertia

Fecha: 15 de octubre de 2026  
Versión: 1.1  
Propósito: comparar estos requerimientos con una solución ya construida para identificar reutilización, ajustes, integraciones y trabajo faltante.

Inventario de comparación: **107 requisitos**, separados en **77 de base**, **22 propuestos** y **8 posteriores**, más **13 decisiones pendientes**. Cada requisito tiene un identificador, fuente, estado de alcance y columnas para registrar cobertura y evidencia. La clasificación de base identifica la necesidad documentada o solicitada; la aceptación comercial definitiva se cierra después del cruce.

## 1. Objetivo y alcance de la revisión

La solución debe ayudar al ejecutivo comercial a encontrar referentes en empresas, preparar el primer contacto, realizar seguimientos, detectar respuestas y registrar su gestión sin volver a cargar todo manualmente en distintas herramientas. El ejecutivo conserva la reunión, la propuesta comercial, la negociación y el cierre.

El objetivo de este documento es evaluar la cobertura del producto existente. La coincidencia de nombres de módulos, pantallas o tecnologías no demuestra cobertura: cada requisito debe contrastarse con comportamiento verificable, datos, permisos y una evidencia concreta. No se exige reconstruir una función que ya cumple el requisito.

El producto existente que se desea comparar todavía no fue inspeccionado. Por eso, todas las filas comienzan en SE, sin evaluar. No deben interpretarse como funciones faltantes.

### 1.1 Alcance de la primera entrega

- Piloto web en infraestructura provista por Vertia, inicialmente con Agustín Silva como usuario referente y después con un grupo comercial controlado.
- Base PostgreSQL compartida con aislamiento de información por ejecutivo y separación entre pruebas y producción.
- Empresas, contactos, prospección con Lusha o un proveedor autorizado equivalente, campañas de correo, seguimiento, historial y métricas.
- Integración corporativa con Microsoft 365 para correo y calendario; los permisos y el diseño de la integración deben validarse con TI.
- Análisis y asistencia mediante Claude API y agentes, con aprobación humana para acciones comerciales externas.
- Pruebas, documentación, publicación controlada, mantenimiento y soporte durante la operación.

### 1.2 Integración posterior y ampliaciones

La reunión comercial cierra con llevar la herramienta a la nube, probarla con Agus y luego extenderla al equipo. En ese cierre se posterga conectar directamente con POST. La conexión con POST sigue siendo un objetivo, pero no debe convertirse automáticamente en un bloqueo del piloto ni darse por contratada en ambos sentidos.

WhatsApp, mensajería por LinkedIn, despliegue regional completo y automatizaciones de otras áreas son ampliaciones por evaluar. La demostración de una plataforma con finanzas, tickets y otros módulos no convierte esos módulos en requisitos del prospectador.

## 2. Fuentes y precedencia

| Código | Fuente | Uso |
|---|---|---|
| S1 | [Bot Comercial GVP para IT](Bot_Comercial_GVP_para_IT.md), versión 9.4, build 2026-10-08-BB | Comportamiento documentado de la herramienta local, límites, archivos, integraciones y controles. |
| S2 | [Reunión de iniciativa Agustín Silva](<Iniciativa AGUSTIN SILVA.docx>), 15 de octubre de 2026 | Necesidades comerciales, convivencia con POST, piloto y separación por ejecutivo. |
| S3 | [Requerimientos de implementación AWS](<../Requerimientos de implementación AWS – Web apps MVP.md>) | Referencia de infraestructura, identidad corporativa y despliegue. El original aún describe dos aplicaciones y PostgreSQL. |
| S4 | [Propuesta Vertia 2027](../Propuesta_Vertia_2027_USD.docx) | Referencia de pruebas, entrega, garantía y soporte. Las condiciones comerciales siguen siendo propuestas. |
| S5 | Instrucciones del usuario en este chat, 15 de octubre de 2026 | PostgreSQL; AWS y base de datos aportados por Vertia; Claude Opus 5.5 como mínimo; agentes; todos los servicios externos pagados por Vertia; mantenimiento y soporte. |
| D | Diseño propuesto en este documento | Descomposición técnica para comparar soluciones. Requiere validación y no representa una funcionalidad observada en el código. |

Las instrucciones S5 prevalecen sobre los antecedentes. La decisión vigente es utilizar PostgreSQL, en coherencia con el documento AWS. Las restricciones de un programa local basado en Excel y Outlook COM describen el origen; no obligan a conservar esas tecnologías en la solución web.

El documento S1 declara aproximadamente 23.800 líneas de Python, dos módulos, 48 scripts de pruebas y 20 pantallas. Son afirmaciones del documento, no resultados de una auditoría del código. El código fuente y las pruebas no están en la carpeta revisada.

### 2.1 Interpretación de las tablas

Estado del alcance:

- Base: requisito documentado o solicitado para el producto objetivo. Se debe comprobar su cobertura.
- Propuesto: control, diseño o condición recomendados para producción; deben validarse al cerrar alcance.
- Posterior: objetivo o ampliación para una etapa posterior. No bloquea por sí solo el piloto.

Cobertura a completar:

| Código | Significado | Evidencia esperada |
|---|---|---|
| SE | Sin evaluar | Todavía no se revisó la implementación. |
| C | Cubierto | Caso ejecutado y ubicación del componente que lo resuelve. |
| P | Parcial | Qué resuelve, qué falta y prueba de la parte existente. |
| N | No cubierto | Revisión que confirma ausencia o incompatibilidad. |
| NA | No aplica | Justificación validada para el alcance de la etapa. |

En Evidencia y brecha registrar módulo o ruta de código, endpoint, captura o prueba, limitación detectada y ajuste necesario. Una casilla marcada o una pantalla aislada no bastan para dar por cubierta una función.

## 3. Flujo comercial esperado

1. El ejecutivo entra con su identidad corporativa y accede a su cartera autorizada.
2. Importa una base o busca empresas y referentes mediante un proveedor aprobado.
3. Revisa candidatos y autoriza revelar los datos que consumen créditos.
4. El sistema detecta duplicados, aplica exclusiones y asigna el contacto a una cartera.
5. Se priorizan contactos y se preparan borradores según rubro, contexto e historial.
6. El ejecutivo revisa destinatarios y contenido y aprueba el envío individual o el lote.
7. La tarea programada vuelve a comprobar permisos, exclusiones, respuesta previa y límites antes de enviar.
8. El envío y su resultado quedan registrados y vinculados con la conversación.
9. Se sincronizan respuestas, rebotes y reuniones; el sistema detiene seguimientos cuando corresponde.
10. Cuando el prospecto responde, el ejecutivo toma la conversación. La IA puede asistir, pero no negocia ni cierra.
11. Las reuniones, propuestas y resultados alimentan el historial y las métricas del período.
12. En la etapa acordada, se sincroniza con POST la información y los estados definidos por sus responsables.

## 4. Identidad, roles y cartera

Roles de referencia: ejecutivo comercial, jefatura autorizada, administrador funcional y soporte técnico. Los alcances exactos de jefatura y administración se deben acordar; no se asume acceso irrestricto a todos los correos o carteras.

| ID | Requisito verificable | Alcance | Fuente | Cobertura | Evidencia y brecha |
|---|---|---|---|---|---|
| ACC-01 | Iniciar sesión con identidad corporativa de Vertia mediante Microsoft Entra ID. Usuarios no autorizados no ingresan. | Base | S3 | SE | — |
| ACC-02 | Mantener usuarios, estado activo y rol. La baja impide nuevas acciones y requiere resolver tareas programadas pendientes. | Base | S2, S3, D | SE | — |
| ACC-03 | Separar contactos, historial y gestión por ejecutivo. Cambiar un identificador o consultar directamente una API no permite leer otra cartera. | Base | S2 | SE | — |
| ACC-04 | Definir acceso de jefatura a equipos y reportes mediante autorización explícita; mostrar solo el alcance habilitado. | Propuesto | D | SE | — |
| ACC-05 | Reasignar responsables con autorización y auditoría, sin duplicar contactos ni perder historial. | Propuesto | D | SE | — |
| ACC-06 | Aplicar permisos a lectura, edición, importación, exportación, envío y configuración. Las validaciones se realizan en el servidor. | Base | S2, S3, D | SE | — |

## 5. Empresas, contactos e historial comercial

| ID | Requisito verificable | Alcance | Fuente | Cobertura | Evidencia y brecha |
|---|---|---|---|---|---|
| DAT-01 | Mantener empresas con identificador interno estable, nombre, dominio, rubro, país y responsable; los campos definitivos se mapean con la base real. | Base | S1, S2, D | SE | — |
| DAT-02 | Mantener contactos relacionados con una empresa: nombre, cargo, email, teléfono y LinkedIn cuando existan, origen y ejecutivo responsable. | Base | S1, S2 | SE | — |
| DAT-03 | Registrar agencia y anunciante como relaciones diferenciadas cuando corresponda. No mezclar las empresas con las personas de contacto. | Base | S1, S2 | SE | — |
| DAT-04 | Conservar un historial cronológico de correos, respuestas, rebotes, reuniones, observaciones y cambios de estado, con fecha y origen. | Base | S1 | SE | — |
| DAT-05 | Importar los Excel originales con vista previa, mapeo, validación y reporte de errores. Repetir una importación no duplica registros válidos. | Base | S1, S5, D | SE | — |
| DAT-06 | Detectar duplicados por identificador de proveedor, email normalizado, empresa y otros criterios acordados; revisar coincidencias ambiguas antes de fusionar. | Base | S1, D | SE | — |
| DAT-07 | Manejar etapas comerciales, responsable, próxima acción y fecha. El catálogo de estados se valida con Agus y no se inventa a partir de nombres de pantallas. | Base | S1, S2, D | SE | — |
| DAT-08 | Filtrar y exportar la cartera autorizada. Toda exportación aplica los mismos permisos y registra quién la solicitó. | Propuesto | D | SE | — |

## 6. Búsqueda y enriquecimiento de prospectos

| ID | Requisito verificable | Alcance | Fuente | Cobertura | Evidencia y brecha |
|---|---|---|---|---|---|
| PRO-01 | Integrar Lusha mediante API oficial o un proveedor equivalente aprobado por Vertia, con credenciales de Vertia. | Base | S1, S5 | SE | — |
| PRO-02 | Buscar por empresa o dominio, país y cargo; priorizar inicialmente Uruguay y los perfiles de marketing, marca y gerencia general descritos por el negocio. | Base | S1 | SE | — |
| PRO-03 | Mostrar candidatos antes de revelar datos de pago y permitir que el ejecutivo seleccione cuáles consultar. | Base | S1 | SE | — |
| PRO-04 | Recuperar email, teléfono y LinkedIn cuando el proveedor los entregue. Datos ausentes quedan vacíos o como no disponibles. | Base | S1 | SE | — |
| PRO-05 | Reutilizar datos ya revelados y válidos para evitar consumo repetido innecesario. El tiempo de vigencia se acuerda. | Base | S1, D | SE | — |
| PRO-06 | Registrar créditos, proveedor, operación, usuario y fecha; aplicar cupos por ejecutivo o unidad según la política aprobada. | Base | S1, S3 | SE | — |
| PRO-07 | Configurar límites de consultas y créditos; ante un 429 o cuota agotada, pausar o reintentar de forma acotada sin duplicar operaciones. | Base | S1, D | SE | — |
| PRO-08 | Evitar revelar o incorporar nuevamente contactos excluidos, duplicados o sin autorización comercial, según reglas de deduplicación y cartera. | Base | S1, D | SE | — |
| PRO-09 | Encapsular el proveedor para permitir un reemplazo futuro. La primera entrega considera un proveedor; conectar varios requiere alcance y credenciales adicionales. | Propuesto | S5, D | SE | — |

### 6.1 Límites heredados que deben contrastarse

S1 documenta 50 consultas por minuto, 150 por hora, 1.500 por día y 600 créditos por corrida. Son parámetros de la herramienta local, no una afirmación sobre las cuotas vigentes de cualquier plan Lusha. La configuración productiva debe respetar el plan contratado, sus condiciones y los límites que apruebe Vertia; se aplica el límite más restrictivo.

Compartir una caché para no volver a pagar un contacto no debe revelar automáticamente la cartera de otro ejecutivo. Debe definirse cómo resolver propiedad, existencia de un contacto y reasignaciones sin exponer historiales ajenos.

## 7. Campañas, priorización y borradores

| ID | Requisito verificable | Alcance | Fuente | Cobertura | Evidencia y brecha |
|---|---|---|---|---|---|
| CAM-01 | Ordenar la base por rubro, estado, validez del correo y días desde el último contacto; permitir que el ejecutivo ajuste la selección. | Base | S1 | SE | — |
| CAM-02 | Crear campañas con responsable, destinatarios, objetivo, plantilla y estado. La lista final de destinatarios debe poder revisarse. | Base | S1, D | SE | — |
| CAM-03 | Generar borradores adecuados al rubro y etapa, con tono comercial local y pedido concreto, sin inventar antecedentes. | Base | S1, S5 | SE | — |
| CAM-04 | Permitir editar el contenido y la firma antes de aprobar. Cambiar destinatarios o contenido después de aprobar exige una nueva validación. | Base | S1, D | SE | — |
| CAM-05 | Configurar secuencias de seguimiento y esperas; mostrar cuál sería el próximo mensaje y cuándo corresponde. | Base | S1 | SE | — |
| CAM-06 | Exigir aprobación explícita del ejecutivo para el envío individual o en lote, manteniendo evidencia del contenido y destinatarios aprobados. | Base | S1 | SE | — |
| CAM-07 | Pausar o cancelar una campaña y detener pendientes. La interfaz distingue entre mensajes ya enviados, en ejecución y todavía cancelables. | Base | S1, D | SE | — |
| CAM-08 | Impedir que una secuencia negocie precios, ofrezca descuentos o cierre una venta por cuenta del ejecutivo. | Base | S1 | SE | — |

## 8. Correo corporativo y ejecución de envíos

| ID | Requisito verificable | Alcance | Fuente | Cobertura | Evidencia y brecha |
|---|---|---|---|---|---|
| MAIL-01 | Integrar correo corporativo sin depender de que Outlook de escritorio esté abierto. Microsoft Graph es el diseño de referencia, sujeto a permisos de TI. | Base | S1, S3, S5, D | SE | — |
| MAIL-02 | Enviar desde la identidad autorizada del ejecutivo, con su firma y registro en Enviados. Un buzón de notificaciones no sustituye automáticamente esa identidad. | Base | S1, S3 | SE | — |
| MAIL-03 | Distinguir envío aceptado por el proveedor, entrega cuando exista evidencia, error, rebote y estado desconocido. No presentar un mensaje aceptado como entregado. | Propuesto | D | SE | — |
| MAIL-04 | Mantener una cola de envíos con identificador único. Reintentos y reinicios no deben generar envíos duplicados por un fallo local. | Propuesto | D | SE | — |
| MAIL-05 | Configurar límites por buzón, campaña y organización, horario y zona horaria; validar los límites autorizados por TI y el proveedor. | Base | S1, D | SE | — |
| MAIL-06 | Aplicar el intervalo mínimo entre contactos a una misma persona y bloquear seguimientos incompatibles con una respuesta o exclusión reciente. | Base | S1 | SE | — |
| MAIL-07 | Permitir frenar tareas y suspender nuevos envíos ante errores repetidos, cuotas o alertas operativas. | Base | S1, S5, D | SE | — |
| MAIL-08 | Registrar mensaje, conversación, campaña, contacto, remitente, fecha y resultado, evitando copiar contenido sensible innecesario a logs operativos. | Base | S1, D | SE | — |
| MAIL-09 | Reintentar errores transitorios con espera acotada; separar errores permanentes y ofrecer revisión manual para resultados inciertos. | Propuesto | D | SE | — |
| MAIL-10 | Volver a comprobar exclusiones, permisos, respuesta previa y aprobación inmediatamente antes de ejecutar un envío programado. | Propuesto | S1, D | SE | — |

### 8.1 Parámetros de envío del programa original

La referencia S1 utiliza 8 segundos entre correos, una pausa de 45 segundos cada 15 mensajes, horario de 08:00 a 20:00 y al menos 7 días entre contactos a una misma persona. Deben poder configurarse y contrastarse con las políticas de Vertia. Estos valores no garantizan por sí solos ausencia de bloqueos o clasificación como spam.

## 9. Respuestas, exclusiones, seguimiento y calendario

| ID | Requisito verificable | Alcance | Fuente | Cobertura | Evidencia y brecha |
|---|---|---|---|---|---|
| FOL-01 | Sincronizar respuestas desde los buzones autorizados. La referencia actual revisa cada 10 minutos; la frecuencia final debe acordarse y ser medible. | Base | S1 | SE | — |
| FOL-02 | Vincular una respuesta con la conversación y el contacto correctos sin depender solo del asunto del correo. | Base | S1, D | SE | — |
| FOL-03 | Notificar al ejecutivo que hay una respuesta pendiente y detener el seguimiento automático de esa conversación. | Base | S1 | SE | — |
| FOL-04 | Sugerir el estado comercial de una respuesta y permitir confirmarlo o corregirlo. Respuestas automáticas y ambiguas requieren un tratamiento diferenciado. | Base | S1, S5, D | SE | — |
| FOL-05 | Registrar pedidos de no contacto y excluirlos de futuras campañas y colas. Definir si la exclusión rige por buzón, unidad o toda la organización. | Base | S1, D | SE | — |
| FOL-06 | Detectar rebotes, registrar su causa cuando esté disponible y evitar reintentos de direcciones permanentemente inválidas. | Base | S1, D | SE | — |
| FOL-07 | Leer reuniones del calendario autorizado y relacionarlas con contactos y gestión comercial; evitar duplicados por resincronización. | Base | S1 | SE | — |
| FOL-08 | Recuperar la sincronización desde el último punto confirmado después de cortes o expiración de permisos, con conciliación y alerta de atraso. | Propuesto | D | SE | — |

## 10. Propuestas y métricas comerciales

El prospectador registra y consulta resultados comerciales; la elaboración de circuitos, disponibilidad de soportes y cálculo de audiencias pertenecen a POST o a Logística, según el sistema maestro acordado.

| ID | Requisito verificable | Alcance | Fuente | Cobertura | Evidencia y brecha |
|---|---|---|---|---|---|
| MET-01 | Incorporar la información de la planilla de propuestas utilizada por Agus mediante importación o sincronización acordada, sin exigir una segunda carga manual del mismo dato. | Base | S1, S2 | SE | — |
| MET-02 | Relacionar propuesta, empresa, contacto y ejecutivo con estado, monto, moneda y fechas cuando la fuente los contenga. | Base | S1, S2, D | SE | — |
| MET-03 | Mostrar gestión mensual: actividad, correos, reuniones, respuestas y propuestas, separadas por el alcance autorizado del usuario. | Base | S1, S2 | SE | — |
| MET-04 | Mostrar ganados, perdidos y pendientes, importes y porcentaje de cierre, con definición explícita del denominador y del período. | Base | S2, D | SE | — |
| MET-05 | Comparar meses y años y mostrar un embudo consistente. Los totales y los detalles deben conciliar con los registros de origen. | Base | S1, S2 | SE | — |
| MET-06 | Gestionar monedas y fechas de forma explícita; no sumar montos de distintas monedas sin una regla de conversión acordada. | Propuesto | D | SE | — |

No se presupone seguimiento de apertura de correo, píxeles, atribución de ventas o una tasa de entrega garantizada. Si se requieren, se deben especificar y validar como funciones adicionales.

## 11. Claude API y agentes

Vertia debe facilitar una cuenta o proyecto con acceso API al modelo Claude Opus 5.5 como mínimo, según la instrucción recibida. La suscripción interactiva de un usuario no se considera prueba de que exista acceso API habilitado. Se deben validar identificador del modelo, disponibilidad, cuotas y condiciones de tratamiento de datos antes de producción.

Los agentes siguientes describen responsabilidades lógicas. Pueden implementarse en un mismo servicio con pasos controlados; no se exige contratar una plataforma de agentes externa ni crear un proceso independiente por cada función.

| Responsabilidad lógica | Entrada | Salida permitida | Control humano |
|---|---|---|---|
| Priorización asistida | Cartera autorizada y reglas comerciales | Lista ordenada con explicación y datos utilizados | El ejecutivo elige destinatarios. |
| Redacción | Rubro, etapa, contexto aprobado y plantilla | Borrador de primer contacto o seguimiento | El ejecutivo revisa y aprueba antes de enviar. |
| Clasificación de respuestas | Mensajes de conversaciones autorizadas | Estado sugerido, motivo y siguiente acción | Corrección y confirmación del ejecutivo según política. |
| Resumen comercial | Historial autorizado del contacto | Síntesis de gestiones y pendientes con referencias | El ejecutivo decide y actúa. |

| ID | Requisito verificable | Alcance | Fuente | Cobertura | Evidencia y brecha |
|---|---|---|---|---|---|
| AI-01 | Utilizar Claude API con Opus 5.5 como mínimo, con modelo y versión configurados; no degradar a otro modelo sin autorización. | Base | S5 | SE | — |
| AI-02 | Implementar responsabilidades de agentes acotadas y trazables para análisis y asistencia comercial; validar con Agus cuáles entran en el piloto. | Base | S5, D | SE | — |
| AI-03 | Generar borradores y sugerencias basados en datos existentes; distinguir información ausente de información confirmada. | Base | S1, S5 | SE | — |
| AI-04 | Conservar referencias al historial usado en clasificaciones y resúmenes, de modo que el ejecutivo pueda contrastar la sugerencia. | Propuesto | D | SE | — |
| AI-05 | Aplicar los permisos del usuario a toda recuperación de datos y herramienta invocada. Un agente no puede consultar otra cartera ni elevar permisos. | Base | S2, S5, D | SE | — |
| AI-06 | Impedir que texto recibido por correo cambie las instrucciones del agente o autorice consultas, exportaciones o envíos fuera de su función. | Propuesto | D | SE | — |
| AI-07 | Exigir aprobación humana antes de enviar correos o alterar decisiones comerciales relevantes; el agente no negocia descuentos ni cierra ventas. | Base | S1, S5 | SE | — |
| AI-08 | Limitar pasos, llamadas, tokens, duración, reintentos y presupuesto. Registrar consumo por operación, usuario, campaña y ambiente. | Propuesto | S5, D | SE | — |
| AI-09 | Versionar instrucciones y evaluar calidad con casos representativos. Si Claude falla o agota cuota, conservar la operación manual y los trabajos pendientes. | Propuesto | S5, D | SE | — |

### 11.1 Datos enviados a la IA

El uso de Claude para operar la aplicación es distinto de usar una IA para programarla. El documento AWS prohíbe usar datos reales sensibles en prompts de desarrollo. Esto debe mantenerse en desarrollo y pruebas.

En producción, cualquier análisis de correos o datos comerciales mediante Claude requiere aprobación de Vertia sobre datos permitidos, minimización, retención, acceso, ubicación de procesamiento y condiciones del proveedor. Esa autorización no debe presumirse a partir de que exista una API key. La aplicación debe poder limitar los campos enviados y omitir secretos y contenido no autorizado.

Referencia técnica para validar modelo y consumo al implementar: [documentación de precios y modelos de Claude](https://platform.claude.com/docs/en/about-claude/pricing). Este documento no fija una tarifa contractual de API.

## 12. POST y otras integraciones

POST conserva las funciones comerciales existentes que se acuerden como maestras. El prospectador no debe convertirse accidentalmente en un reemplazo de inventario, circuitos, audiencias o generación completa de propuestas.

| ID | Requisito verificable | Alcance | Fuente | Cobertura | Evidencia y brecha |
|---|---|---|---|---|---|
| INT-01 | Reservar identificadores internos y externos para enlazar empresas, contactos, propuestas y gestiones sin utilizar el nombre como única llave. | Propuesto | S2, D | SE | — |
| INT-02 | Conectar con POST cuando se habilite la etapa: documentar endpoints o archivos, permisos, cuotas, entidades y sentido de cada dato. | Posterior | S2 | SE | — |
| INT-03 | Registrar en POST las gestiones o contactos que se acuerden, sin cargar automáticamente todos los prospectos revelados si esa no es la política definida. | Posterior | S2, D | SE | — |
| INT-04 | Sincronizar cambios de POST hacia el prospectador solo si se aprueba ese sentido; definir sistema maestro, conflictos y conciliación por campo. | Posterior | S2, D | SE | — |
| INT-05 | Registrar errores de integración, reintentos y duplicados; permitir reanudar y conciliar sin volver a crear las mismas entidades. | Posterior | D | SE | — |
| INT-06 | Mantener el piloto operativo sin POST y documentar el mecanismo transitorio para propuestas y resultados comerciales. | Base | S1, cierre S2 | SE | — |

## 13. Arquitectura, PostgreSQL y ambientes

La arquitectura de referencia es una aplicación web con frontend, API, PostgreSQL y tareas en segundo plano, alojada en AWS de Vertia. React y FastAPI son las tecnologías de referencia del documento AWS; si el producto existente usa otro stack, se evalúa compatibilidad y mantenibilidad antes de imponer una reescritura.

| ID | Requisito verificable | Alcance | Fuente | Cobertura | Evidencia y brecha |
|---|---|---|---|---|---|
| TEC-01 | Ofrecer acceso web multiusuario sin depender de una PC específica ni de archivos Excel abiertos para persistir las operaciones. | Base | S2, S5 | SE | — |
| TEC-02 | Persistir en PostgreSQL provisto por Vertia, con migraciones versionadas, claves estables, integridad y transacciones para operaciones relacionadas. | Base | S5, D | SE | — |
| TEC-03 | Separar desarrollo/pruebas de producción: base, secretos, buzones o destinatarios de prueba y colas. Pruebas no envían accidentalmente campañas reales. | Base | S3, S5, D | SE | — |
| TEC-04 | Ejecutar envíos, búsqueda de prospectos, sincronización y agentes como trabajos en segundo plano con estado, reintentos y recuperación. | Base | S1, S3, S5, D | SE | — |
| TEC-05 | Documentar las API y los contratos de integración de los módulos que se reutilicen, con autenticación y errores definidos. | Propuesto | D | SE | — |
| TEC-06 | Incorporar control de concurrencia para ediciones, revelados y envíos, evitando pérdida de cambios o doble ejecución entre usuarios. | Propuesto | S2, D | SE | — |
| TEC-07 | Probar al menos 20 usuarios concurrentes como referencia inicial, con carga de tareas de fondo representativa; acordar tiempos de respuesta medibles. | Base | S3, D | SE | — |
| TEC-08 | Automatizar publicación a pruebas y producción, con aprobación, migración compatible, verificación de salud y reversión documentada. | Base | S3, S5 | SE | — |

### 13.1 Modelo de datos mínimo a contrastar

Este es un modelo conceptual propuesto para mapear contra las tablas existentes. No exige que cada fila sea una tabla independiente.

| Entidad | Datos o relaciones a comprobar |
|---|---|
| Usuario y alcance | Identidad corporativa, rol, equipo, país cuando corresponda, estado y buzón autorizado. |
| Empresa | Nombre, dominio, rubro, país, relaciones con agencias/anunciantes e identificadores externos. |
| Contacto | Empresa, nombre, cargo, canales, origen, responsable, estado y trazabilidad del enriquecimiento. |
| Exclusión de contacto | Canal, dirección normalizada, motivo, fecha, alcance y fuente. |
| Campaña y secuencia | Responsable, objetivo, destinatarios, pasos, esperas, horarios y estado. |
| Borrador y aprobación | Versión del contenido, destinatarios, aprobador y fecha. |
| Mensaje y conversación | Identificadores del proveedor, sentido, remitente, destinatario, fechas y resultado. |
| Actividad y seguimiento | Tipo, contacto, empresa, responsable, fecha, próxima acción y fuente. |
| Reunión | Identificador de calendario, participantes, fecha, estado y relación comercial. |
| Propuesta y resultado | Identificador, contacto/empresa, moneda, monto, estado y fechas; sistema de origen. |
| Consulta y revelado | Proveedor, consulta, resultado, créditos y relación con el contacto. |
| Trabajo asíncrono | Tipo, estado, intentos, identificador de idempotencia y error. |
| Ejecución de agente | Modelo, versión de instrucciones, referencias utilizadas, salida, revisión y consumo. |
| Integración externa | Sistema, entidad, identificador externo y estado de sincronización. |
| Auditoría y consumo | Actor, acción, objeto, fecha, resultado y medición por proveedor y ambiente. |

Los alcances por ejecutivo y país deben verificarse en backend y consultas. Los permisos y mecanismos de aislamiento de PostgreSQL deben validarse con pruebas entre usuarios y roles.

### 13.2 Infraestructura atribuible al CRM

Los siguientes son requisitos de capacidad inicial propuestos, no recursos ya contratados ni una garantía de rendimiento.

| Componente | Producción | Desarrollo/pruebas | Condición de comparación |
|---|---|---|---|
| Frontend | Un despliegue web del CRM | Un despliegue separado | Puede convivir con otros módulos sin mezclar permisos ni datos. |
| API | Dos tareas iniciales, referencia 0,5 vCPU y 1 GB por tarea; escalables | Una tarea inicial | Ajustar por pruebas y por la arquitectura existente. |
| Trabajos de fondo | Capacidad de worker para CRM | Capacidad separada de pruebas | Puede ser compartida con otras iniciativas si conserva aislamiento y control de concurrencia. |
| PostgreSQL | Una base lógica CRM en servicio productivo de Vertia | Una base lógica CRM en servicio de pruebas | No se exigen dos servidores nuevos exclusivos del CRM si ya existe capacidad equivalente. |
| Archivos | Espacio privado para importaciones y adjuntos autorizados | Espacio separado de pruebas | Política de retención y acceso definida. |
| Colas y errores | Colas para tareas y recuperación de fallos | Colas separadas | La cantidad final depende de cómo se separen envío, enriquecimiento y sincronización. |
| Identidad y secretos | Entra ID, permisos, claves y configuración productiva | Credenciales y datos de prueba | Vertia habilita; MoAI integra. |
| Operación | Logs, métricas, alertas, backups y procedimientos | Evidencia de pruebas y restauración | Puede reutilizar servicios corporativos existentes. |

No corresponde atribuir al CRM todos los recursos compartidos de las tres iniciativas ni duplicarlos al comparar costos o infraestructura.

## 14. Seguridad y manejo de información

| ID | Requisito verificable | Alcance | Fuente | Cobertura | Evidencia y brecha |
|---|---|---|---|---|---|
| SEC-01 | Guardar credenciales en el mecanismo de secretos autorizado por Vertia; no exponerlas en frontend, repositorio, exportaciones ni logs. | Base | S1, S3 | SE | — |
| SEC-02 | Cifrar comunicaciones y almacenamiento de acuerdo con las políticas de Vertia y restringir conectividad de PostgreSQL. | Base | S3, S5 | SE | — |
| SEC-03 | Registrar cambios de responsables, importaciones, exportaciones, aprobaciones, envíos y cambios de configuración con actor y fecha. | Base | S1, S3, D | SE | — |
| SEC-04 | Aplicar minimización y retención de contactos, mensajes, archivos y salidas de IA conforme a la política que apruebe Vertia. | Base | S3, S5, D | SE | — |
| SEC-05 | Validar tratamiento de datos de prospectos, uso de proveedores y mensajes comerciales con los responsables de Vertia; registrar reglas de exclusión aplicables. | Base | S1, S3 | SE | — |
| SEC-06 | Usar únicamente fuentes e integraciones autorizadas. No implementar scraping restringido, evasión de bloqueos o automatización de cuentas personales como atajo. | Base | S1 | SE | — |
| SEC-07 | Revisar permisos efectivos y revocaciones, incluyendo tokens, agentes y trabajos ya encolados. El soporte accede solo al alcance autorizado. | Propuesto | S3, D | SE | — |

## 15. Pruebas y aceptación

Las pruebas se realizan tanto sobre componentes reutilizados como sobre adaptaciones nuevas. El hecho de que una función exista en otra aplicación no demuestra que funcione con PostgreSQL, Entra ID, buzones y permisos de Vertia.

| ID | Requisito verificable | Alcance | Fuente | Cobertura | Evidencia y brecha |
|---|---|---|---|---|---|
| QA-01 | Probar el flujo de búsqueda, revelado, borrador, aprobación, envío, respuesta y derivación humana con trazabilidad completa. | Base | S1, S4, S5 | SE | — |
| QA-02 | Probar aislamiento entre ejecutivos y roles en pantallas, API, exportaciones, búsquedas y herramientas de agentes. | Base | S2, S5, D | SE | — |
| QA-03 | Probar reintentos, reinicios, resultados inciertos y ejecución concurrente para evitar correos, contactos y cobros duplicados evitables. | Propuesto | D | SE | — |
| QA-04 | Probar exclusión y respuesta recibidas después de aprobar una campaña y antes de enviar; no deben salir seguimientos incompatibles. | Base | S1, D | SE | — |
| QA-05 | Probar cuotas y fallas de Lusha, Claude y Microsoft 365, incluyendo 429, timeout y permisos revocados. | Base | S1, S5, D | SE | — |
| QA-06 | Evaluar agentes con casos comerciales revisados por Agus: datos ausentes, instrucciones maliciosas, clasificaciones ambiguas y ausencia de permiso. | Propuesto | S5, D | SE | — |
| QA-07 | Probar importación y conciliación de cartera, historial, propuestas y métricas sobre muestras representativas autorizadas. | Base | S1, S2, S4 | SE | — |
| QA-08 | Probar concurrencia, restauración y despliegue con reversión; conservar resultados y resolver fallas críticas antes de producción. | Base | S3, S4, S5 | SE | — |
| QA-09 | Ejecutar un piloto con Agus y después usuarios seleccionados; registrar observaciones, correcciones, capacitación y aceptación de salida. | Base | S2, S4 | SE | — |

### 15.1 Casos mínimos para el cruce funcional

| Caso | Situación | Resultado esperado |
|---|---|---|
| A | Dos ejecutivos buscan un contacto que ya fue revelado. | No se repite un consumo innecesario y no se expone la cartera ajena. |
| B | Un prospecto pide no recibir más correos cuando ya hay mensajes en cola. | Se registra la exclusión y se bloquean pendientes dentro del alcance definido. |
| C | El proveedor acepta un correo y el sistema pierde la conexión antes de registrar la respuesta. | Se concilia el resultado o se deriva a revisión; no se reenvía a ciegas. |
| D | El contacto responde antes de un seguimiento programado. | Se detiene la secuencia y se notifica al ejecutivo. |
| E | El mensaje entrante solicita al agente exportar otra cartera. | El agente no ejecuta la instrucción ni accede a datos fuera de alcance. |
| F | Se agota el presupuesto de IA. | Se detienen nuevas llamadas según política, se conserva el historial y queda disponible el trabajo manual. |
| G | Se vuelve a importar una planilla ya procesada. | Se identifican existentes y errores sin duplicar cartera ni actividades. |
| H | El usuario pierde acceso al buzón o deja la empresa. | Se detienen tareas que ya no puede autorizar y se activa la reasignación aprobada. |
| I | El dashboard muestra un porcentaje de cierre. | Se puede reproducir con el período, numerador, denominador y monedas definidos. |
| J | POST no está disponible o todavía no tiene integración. | El piloto continúa con el mecanismo transitorio acordado. |

## 16. Mantenimiento, soporte y continuidad

El mantenimiento cubre toda la operación: aplicación, base lógica, integraciones, tareas programadas, agentes, consumo y publicaciones. Vertia conserva la operación de sus servicios AWS y PostgreSQL; MoAI mantiene el software y coordina incidentes con TI y proveedores.

| ID | Requisito verificable | Alcance | Fuente | Cobertura | Evidencia y brecha |
|---|---|---|---|---|---|
| OPS-01 | Monitorear salud, errores, atraso de sincronización, colas, agentes y cuotas; enviar alertas al responsable operativo definido. | Base | S3, S5 | SE | — |
| OPS-02 | Mantener un procedimiento de incidentes con severidad, responsable, horario de cobertura, respuesta inicial y escalamiento; distinguir respuesta de resolución. | Base | S5, S4 | SE | — |
| OPS-03 | Revisar periódicamente dependencias, integraciones, versiones de modelos, permisos y cambios de API; validar cambios antes de publicarlos. | Base | S5, D | SE | — |
| OPS-04 | Separar corrección de defectos bajo garantía, soporte y nuevas funcionalidades. Conservar registro de solicitudes y horas cuando corresponda. | Propuesto | S4 | SE | — |
| OPS-05 | Mantener respaldos y un procedimiento de restauración con responsabilidades de Vertia y MoAI; acordar retención, pérdida máxima de datos y tiempo de recuperación. | Base | S3, S4, S5 | SE | — |
| OPS-06 | Publicar cambios mediante control de versiones, revisión, pruebas, aprobación y verificación posterior, con un responsable de reversión. | Base | S3, S5 | SE | — |
| OPS-07 | Medir consumo por proveedor y ambiente y avisar antes de agotar presupuestos; permitir pausar enriquecimiento, envíos o agentes de manera independiente. | Base | S3, S5, D | SE | — |
| OPS-08 | Entregar manual de usuario, instrucciones de despliegue, operación, recuperación, inventario de dependencias y responsables de cuentas. | Base | S4, S5 | SE | — |
| OPS-09 | Permitir exportación y transferencia de datos y documentación bajo permisos, para continuidad o cambio de mantenedor sin depender de una PC personal. | Propuesto | S4, D | SE | — |

### 16.1 Condiciones de soporte que siguen propuestas

En la conversación se planteó para el CRM una bolsa inicial de 8 horas mensuales. La propuesta general utiliza como referencia atención de lunes a viernes de 09:00 a 18:00 en Chile, excepto festivos; respuesta inicial crítica de hasta 4 horas hábiles y otros casos en un día hábil; garantía de defectos de 60 días desde aceptación, sin consumir soporte.

Estas son condiciones a formalizar, no un SLA ya contratado. Debe definirse la periodicidad de mantenimiento, responsables de alertas, escalamiento a Vertia, tratamiento de excesos de horas, emergencias fuera de horario y coordinación ante indisponibilidad de terceros. No se presupone una guardia humana 24/7.

## 17. Servicios y accesos a cargo de Vertia

Todos los costos de AWS, PostgreSQL, APIs, licencias y herramientas externas son contratados y pagados directamente por Vertia. La integración, configuración de la aplicación, pruebas y soporte de MoAI se tratan por separado. No se duplican compras de servicios corporativos ya disponibles.

| Aporte de Vertia | Información o habilitación necesaria | Uso |
|---|---|---|
| AWS | Ambientes, red, capacidad, almacenamiento, colas, permisos, secretos, monitoreo, dominios y certificados según diseño aprobado. | Alojar y operar la aplicación. |
| PostgreSQL | Endpoints privados de pruebas y producción, versión compatible, bases lógicas, usuarios, permisos y política de backups. | Persistencia y recuperación. |
| Entra ID | Registros de aplicación, tenant ID, client IDs, roles, consentimientos y redirecciones. | Identidad y autorización corporativas. |
| Microsoft 365 | Buzones de ejecutivos, calendario, remitentes y permisos Graph autorizados. | Correo y registro de reuniones. |
| Buzón de notificaciones | Identidad y permisos separados cuando se requiera. | Avisos internos; no sustituye el remitente comercial sin una decisión expresa. |
| Claude API | Proyecto/cuenta, acceso al modelo mínimo solicitado, API key, cuotas, presupuesto y autorización de tratamiento de datos. | Agentes y análisis en pruebas y producción. |
| Lusha o equivalente | Plan con API, key, créditos, límites, condiciones de reutilización y responsable de cuenta. | Búsqueda y enriquecimiento. |
| POST | Responsable técnico, documentación, pruebas, credenciales y permisos cuando se habilite la integración. | Sincronización de la etapa posterior. |
| Datos comerciales | Planillas e historial autorizados, muestras de propuestas, catálogo de estados y reglas de propiedad de cartera. | Mapeo, migración y validación. |
| Repositorio y despliegue | Ubicación acordada para código, pipeline y permisos de publicación. | Entrega y continuidad. |

Las pruebas con APIs reales también consumen créditos de Vertia. Se utilizan mocks o entornos de prueba para regresión cuando sea posible y se reservan créditos reales para pruebas de integración y aceptación. La programación interna de MoAI y los agentes que operan el producto deben identificarse por separado para no mezclar ni duplicar consumos.

No se requiere OCR para el flujo base del prospectador. El OCR corresponde a la iniciativa documental; si luego se pide analizar adjuntos escaneados dentro del CRM, deberá definirse ese alcance y su consumo.

## 18. Extensiones y exclusiones del piloto

| ID | Requisito verificable | Alcance | Fuente | Cobertura | Evidencia y brecha |
|---|---|---|---|---|---|
| EXT-01 | Evaluar WhatsApp mediante una integración oficial, con costos, requisitos de cuenta, permisos y paso al ejecutivo definidos antes de implementarlo. | Posterior | S2 | SE | — |
| EXT-02 | Evaluar viabilidad de mensajería LinkedIn por medios autorizados; no prometer acceso API o funciones a partir de una suscripción personal. | Posterior | S2, S1 | SE | — |
| EXT-03 | Extender a otros países con validación comercial local, reglas, idioma, zona horaria, permisos y soporte acordados. | Posterior | S2 | SE | — |
| EXT-04 | Incorporar otro proveedor de prospectos o canales adicionales solo después de comparar cobertura, duplicados, créditos y condiciones de integración. | Posterior | S5, D | SE | — |

Quedan fuera del flujo base la negociación autónoma, descuentos automáticos, cierre automático, compra de medios, disponibilidad de soportes, armado de circuitos, cálculo de audiencias, publicación en ad-server, ERP financiero, gestión contractual CLM y módulos generales de tickets o finanzas. Si alguno ya existe en el producto a comparar, se registra como capacidad adicional y no como requisito obligatorio de esta iniciativa.

## 19. Decisiones pendientes para cerrar el alcance

| ID | Decisión | Responsable de definición | Efecto |
|---|---|---|---|
| DEC-01 | Número de ejecutivos del piloto, jefaturas y reglas de acceso a cartera. | Vertia comercial y TI | Permisos, carga y aceptación. |
| DEC-02 | Resolver conflictos entre contacto compartido, propietario comercial y caché de datos revelados. | Vertia comercial | Deduplicación sin exponer carteras ajenas. |
| DEC-03 | Identidad de envío, buzones, permisos de calendario y mecanismo Graph. | TI Vertia y comercial | Integración Microsoft 365. |
| DEC-04 | Catálogo de estados y reglas del embudo, métricas y monedas. | Agus y responsables comerciales | Modelo y reportes. |
| DEC-05 | Proveedor de prospectos, volumen de búsquedas, créditos y datos a revelar. | Vertia | Integración, costo y límites. |
| DEC-06 | Responsabilidades exactas de los agentes, datos autorizados, modelo y umbrales de revisión. | Vertia y MoAI | Calidad, privacidad, consumo y pruebas. |
| DEC-07 | Alcance de no contactar y tratamiento de respuestas automáticas, ambiguas y rebotes. | Comercial y TI Vertia | Secuencias y exclusiones. |
| DEC-08 | Planillas de origen, volumen e historial a migrar, calidad y fuente maestra. | Vertia y MoAI | Migración y conciliación. |
| DEC-09 | Fecha y alcance de POST, dirección de sincronización y mecanismo disponible. | Vertia, proveedor POST y MoAI | Estimación de la etapa posterior. |
| DEC-10 | Arquitectura corporativa reutilizable y capacidad PostgreSQL/AWS disponible. | TI Vertia y MoAI | Recursos y esfuerzo de adaptación. |
| DEC-11 | Horarios y volumen de envío autorizados; pruebas sin afectar destinatarios reales. | TI Vertia y comercial | Operación y protección del correo. |
| DEC-12 | Soporte, garantía, backups, retención, recuperación y mantenimiento periódico. | Vertia y MoAI | Acuerdo de operación. |
| DEC-13 | Criterios de aceptación del piloto y umbrales de calidad y rendimiento. | Agus, TI Vertia y MoAI | Salida a producción. |

## 20. Cómo realizar el cruce con lo construido

1. Identificar el producto, versión, repositorio, arquitectura y módulos realmente disponibles.
2. Recorrer las tablas y registrar cobertura y evidencia por ID, empezando por identidad, datos, correo y prospección.
3. Ejecutar los casos del apartado 15.1 con dos usuarios y datos de prueba. Revisar los controles en backend además de la interfaz.
4. Separar reutilización directa, configuración, adaptación, integración nueva y desarrollo nuevo. Una diferencia de tecnología requiere análisis; no implica por sí sola reconstrucción.
5. Marcar las funciones posteriores sin mezclarlas con los bloqueos del piloto.
6. Registrar cada brecha con dependencia, responsable, esfuerzo estimado y prueba de aceptación.
7. Recalcular la estimación de desarrollo y soporte usando las brechas verificadas. La referencia preliminar de 320 horas no es una obligación de consumirlas ni una garantía de alcance indefinido.

### 20.1 Formato para registrar trabajo resultante

| Requisito relacionado | Cobertura | Componente existente | Ajuste necesario | Dependencia | Horas estimadas | Validación |
|---|---|---|---|---|---|---|
| Completar ID | SE | Pendiente de inspección | Pendiente | Pendiente | Por estimar | Caso y evidencia pendientes |

### 20.2 Evidencias necesarias para comenzar

- Acceso autorizado al código o a la documentación técnica y a una versión ejecutable del producto existente.
- Estructura de datos y versión de motor, API disponibles y mecanismos de autenticación.
- Ejemplos de campañas, seguimientos, respuestas, importaciones y dashboards con datos de prueba.
- Pruebas existentes, pipeline, documentación de despliegue y procedimientos de soporte.
- Lista de conectores y licencias que ya pertenecen a Vertia o que deben contratarse.

No registrar secretos, tokens ni credenciales dentro de este Markdown. Las evidencias deben apuntar a ubicaciones autorizadas y omitir datos personales innecesarios.
