# Propuesta comercial del Prospectador

Preparada para: Vertia Group / Global Vía Pública

Preparada por: MoAI

Fecha: 15 de octubre de 2026

Vigencia: 30 días corridos desde la fecha de emisión

Contacto: somos@mo-ai.cl

## Resumen ejecutivo

El Prospectador comercial es una aplicación web que acompaña al ejecutivo comercial en la parte del proceso que hoy consume tiempo sin aportar criterio: encontrar referentes dentro de las empresas objetivo, preparar un primer contacto pertinente, dar seguimiento ordenado y registrar cada gestión sin volver a cargar la misma información en varias herramientas. La reunión, la negociación y el cierre siguen siendo del ejecutivo; el sistema le devuelve tiempo y trazabilidad.

La solución se construye sobre una base ya existente de MoAI, lo que reduce el esfuerzo de desarrollo y permite cotizar este alcance en un nivel medio. Incluye carteras por ejecutivo con aislamiento de datos, gestión de empresas y contactos, importación de las planillas actuales, búsqueda y enriquecimiento con un proveedor tipo Lusha autorizado por Vertia, integración con Microsoft 365 para correo y calendario, campañas de correo con aprobación humana, seguimiento de respuestas, rebotes y exclusiones, agentes acotados sobre Claude API y un panel de métricas comerciales. La configuración regional base contempla Argentina, Chile, Perú, México y Uruguay desde el modelo de datos y los permisos.

La inversión propuesta es de USD 13.000 netos (UF 311,7235 netas), equivalente a UF 370,9510 con IVA incluido. El contrato se expresa y cobra en UF; los montos en USD son de referencia. El pago se estructura en un anticipo de 40% y seis cuotas mensuales que financian el desarrollo, no un servicio recurrente.

Este documento describe qué está incluido, con límites concretos; qué queda para etapas posteriores; y cómo se verifica el resultado. El valor no se mide por la cantidad de pantallas, sino por resultados verificables: un contacto enriquecido queda disponible sin volver a pagarlo, un envío programado respeta exclusiones y permisos antes de salir, y una respuesta detiene automáticamente la secuencia de seguimiento.

## El problema que abordamos

Hoy el trabajo de prospección vive repartido entre planillas, Outlook, un proveedor de datos y la memoria del ejecutivo. Esa dispersión tiene consecuencias medibles: contactos que se vuelven a pagar porque nadie recuerda que ya se consultaron, correos de seguimiento que salen después de que el prospecto ya respondió, personas que pidieron no ser contactadas y reaparecen en una campaña, y métricas que se arman a mano al cierre de mes.

El problema no es la falta de esfuerzo comercial, sino la ausencia de un lugar único donde la cartera, el historial y las reglas convivan con permisos claros. Cuando cada ejecutivo mantiene su propia versión de la verdad, la jefatura no tiene visibilidad consolidada y la organización no puede reutilizar información ya adquirida sin exponer la cartera de otro ejecutivo.

## Un día con la solución

Un ejecutivo entra con su identidad corporativa de Vertia y ve solo su cartera autorizada. Revisa una lista priorizada de contactos pendientes, con el motivo de la priorización a la vista. Busca referentes en una empresa objetivo a través del proveedor autorizado; antes de gastar créditos, el sistema le muestra candidatos y le permite elegir cuáles revelar. Si un contacto ya fue enriquecido y sigue vigente, no se vuelve a pagar.

Sobre esa base prepara una campaña. El sistema genera borradores adecuados al rubro y a la etapa, sin inventar antecedentes. El ejecutivo edita el texto y la firma, revisa la lista final de destinatarios y aprueba el envío. La tarea programada vuelve a comprobar, justo antes de enviar, que no haya exclusiones, respuestas previas ni límites excedidos. Cada envío queda registrado y vinculado a la conversación.

Durante el día llegan respuestas. El sistema las sincroniza desde los buzones autorizados, las asocia a la conversación correcta, notifica al ejecutivo y detiene el seguimiento automático de esa conversación. Un agente sugiere el estado comercial de la respuesta; el ejecutivo lo confirma o lo corrige. Las reuniones del calendario se vinculan a los contactos. Al cierre de mes, las métricas de gestión ya están construidas a partir de los registros, no de una planilla rehecha.

## Alcance incluido, con límites propuestos

El alcance siguiente se entrega como producto funcional. Donde corresponde se proponen límites concretos, que se incorporan como condiciones de la propuesta y no como aceptaciones ya existentes.

### Identidad, roles y cartera

Inicio de sesión con identidad corporativa de Vertia mediante Microsoft Entra ID. Separación de contactos, historial y gestión por ejecutivo, validada en el servidor. Roles de referencia: ejecutivo, jefatura, administrador funcional y soporte. El alcance exacto de jefatura y administración se acuerda en el levantamiento; no se asume acceso irrestricto a todas las carteras.

### Empresas, contactos e historial

Mantención de empresas y contactos con sus relaciones (agencia y anunciante diferenciados), historial cronológico de correos, respuestas, rebotes, reuniones y cambios de estado. Importación de las planillas actuales con vista previa, mapeo, validación y reporte de errores; repetir una importación no duplica registros válidos. Detección de duplicados por identificador de proveedor, email normalizado y empresa.

### Búsqueda y enriquecimiento

Integración con un proveedor de datos tipo Lusha, mediante su API oficial y con credenciales de Vertia. Límite propuesto: un proveedor en esta entrega. Conectar proveedores adicionales requiere alcance y credenciales aparte. El consumo de créditos queda registrado por usuario y operación, con cupos configurables. La reutilización de datos vigentes evita el gasto repetido.

### Campañas y correo corporativo

Creación de campañas con destinatarios revisables, borradores asistidos, secuencias de seguimiento y aprobación humana explícita para cada envío individual o en lote. Integración con Microsoft 365 (Graph) para enviar desde la identidad autorizada del ejecutivo y para leer calendario, sujeta a los permisos que habilite TI de Vertia. Cola de envíos con identificador único para evitar duplicados ante reintentos. Límites configurables por buzón, campaña y horario.

### Respuestas, exclusiones y seguimiento

Sincronización de respuestas y rebotes, vinculación a la conversación correcta, detención del seguimiento ante una respuesta, y registro de solicitudes de no contacto que excluyen a la persona de futuras campañas. Clasificación asistida del estado comercial, con confirmación del ejecutivo.

### Métricas comerciales

Panel de gestión mensual (actividad, correos, reuniones, respuestas, propuestas) acotado al alcance autorizado del usuario, con ganados, perdidos y pendientes, y definición explícita de período y denominador. No se incluye seguimiento de apertura por píxel, atribución de ventas ni garantía de entrega.

### Agentes sobre Claude API

Responsabilidades acotadas y trazables: priorización asistida, redacción de borradores, clasificación de respuestas y resumen comercial. Todas con control humano. El agente no negocia precios ni cierra ventas. Los permisos del usuario se aplican a toda recuperación de datos.

## Condiciones propuestas para delimitar la entrega

El piloto y la consolidación incluidos contemplan hasta cinco ejecutivos, un tenant corporativo Microsoft 365, un proveedor de prospectos, tres secuencias de campaña configurables y una interfaz simple de intercambio con POST. Si existe una API documentada y autorizada, la interfaz incluye un flujo unidireccional de envío o actualización de gestiones con validación y registro de errores; no incluye sincronización bidireccional de todos los datos. Si la API no está disponible, se implementa importación y exportación de archivos validados y cualquier conector posterior se cotiza por separado.

La carga inicial propuesta contempla hasta 5.000 empresas y 10.000 contactos desde un formato de planilla acordado, con deduplicación y reporte de errores. Son límites de la migración y del acompañamiento inicial, no una licencia por registro ni un límite permanente de almacenamiento. Si la muestra requiere limpieza manual o cruce con fuentes adicionales se informa el diferencial antes de ejecutarlo.

Fase MVP de referencia: semanas 1 a 6. Consolidación, aceptación y publicación: semanas 7 a 10. Se configura el modelo para los cinco países; el piloto productivo es Uruguay. El despliegue masivo y la validación local del resto de los países forman parte de la ampliación regional, sin reconstruir el núcleo.


## Fases

### Fase 1 — MVP con Agus en Uruguay

Puesta en marcha del núcleo en infraestructura de Vertia, con Agustín Silva como usuario referente: cartera aislada, importación de datos reales, enriquecimiento con un proveedor, campañas con aprobación, seguimiento y métricas base. El objetivo es operar el ciclo completo con datos reales de un ejecutivo.

### Fase 2 — Consolidación con el equipo

Extensión a un grupo comercial controlado, ajuste de roles de jefatura, refinamiento de métricas y estabilización operativa. Se incluye además el diseño y mapeo de la consolidación hacia POST y una interfaz simple de intercambio sobre una API documentada y autorizada. Si no existe una API validada, el alcance incluido es un intercambio de archivos validado (importación/exportación), y el conector específico se estima por separado.

Plazo de referencia: 8 a 10 semanas desde la entrega de accesos y datos, revisable según el alcance final.

## Objetivos regionales y separación de ampliaciones

La solución nace pensada para cinco países (Argentina, Chile, Perú, México y Uruguay) desde el modelo de datos, los permisos y la configuración regional base. El piloto opera en Uruguay y el despliegue a otros países se realiza por configuración. La validación de reglas locales corresponde a Vertia.

Quedan explícitamente fuera de esta propuesta, como roadmap separado: mensajería por WhatsApp y LinkedIn, conectores a proveedores de datos adicionales, automatizaciones de otras áreas y la conexión bidireccional completa con POST más allá del diseño, mapeo e interfaz simple descritos.

### Matriz de alcance

| Capacidad | Incluido | Futuro (ampliación) |
|---|---|---|
| Carteras por ejecutivo, empresas, contactos, historial | Sí | — |
| Importación de planillas con validación | Sí | — |
| Enriquecimiento con un proveedor autorizado | Sí | Proveedores adicionales |
| Microsoft 365 correo y calendario | Sí | — |
| Campañas con aprobación humana y seguimiento | Sí | — |
| Agentes acotados sobre Claude API | Sí | — |
| Configuración regional base 5 países | Sí | — |
| Consolidación POST: diseño, mapeo e interfaz simple | Sí | Conector bidireccional completo |
| WhatsApp / LinkedIn | — | Sí |

Lo que se muestre en la demostración sobre capacidades futuras está rotulado como demostración y no constituye producto final ni alcance contratado.

## Responsabilidades

### Vertia

Provee la infraestructura (AWS), PostgreSQL, las credenciales y cuentas de los servicios de terceros (proveedor de datos tipo Lusha, Microsoft 365, Claude API con Opus 5.5 como mínimo), los permisos de TI para Graph, los datos a importar, la validación de reglas regionales y la disponibilidad de los usuarios referentes. Los cargos de estos terceros los habilita y paga directamente Vertia y no forman parte de los honorarios de MoAI.

### MoAI

Diseña, desarrolla, prueba, documenta y publica de forma controlada la solución dentro del alcance acordado; capacita al usuario referente y entrega el soporte contratado por separado.

## Prueba de aceptación

La entrega se considera aceptada cuando, con datos reales de la cartera de referencia, se verifica el ciclo completo: importar sin duplicar, enriquecer un contacto y reutilizarlo sin volver a pagarlo, crear y aprobar una campaña, comprobar que un envío programado respeta exclusiones y permisos antes de salir, recibir una respuesta que detiene el seguimiento y verla reflejada en las métricas del período. Cada punto se demuestra sobre comportamiento verificable, no sobre la sola presencia de una pantalla.



## Soporte propuesto (contratado por separado)

Soporte mensual de 8 horas, de referencia USD 326,99 netos (UF 7,8408) al mes, convertido a UF en el presupuesto y cobrado desde la puesta en producción. Horario L a V de 09:00 a 18:00 hora de Chile, salvo festivos. Primera respuesta para incidencias críticas en 4 horas hábiles y para el resto en 1 día hábil; la resolución depende del diagnóstico. Las mejoras y funciones nuevas se gestionan por control de cambios y no se descuentan de las horas de soporte.

## Garantía

Se incluye una garantía de 60 días corridos desde la aceptación, por defectos atribuibles al desarrollo dentro del alcance entregado. La garantía no consume horas de soporte.

## Propiedad, licencias y cambios de alcance

El entregable desarrollado específicamente para Vertia queda a su disposición según los términos del contrato. Los componentes base y herramientas preexistentes de MoAI se licencian para su uso en esta solución. Las licencias y cuentas de terceros son contratadas y pagadas por Vertia a su nombre. Todo cambio de alcance se acuerda por escrito mediante control de cambios, con su efecto en plazo e inversión.

## Vigencia y contacto

Esta propuesta tiene una vigencia de 30 días corridos desde su emisión. Para dudas, ajustes o aceptación: somos@mo-ai.cl.


## Operación y ajustes durante el proyecto

Los servicios de terceros los contrata y paga Vertia durante desarrollo, pruebas, aceptación y producción. El detalle de AWS, PostgreSQL, Claude Opus 5.5, OCR, prospectos y firma se entrega como anexo de requerimientos a cargo del cliente. No se incluyen sus cargos dentro de los honorarios MoAI.

Se incorporan como anexos el protocolo de mantención y soporte y la matriz de roadmap. Toda publicación requiere pruebas, aceptación y una opción de recuperación. Los defectos del alcance aceptado se cubren por garantía; las mejoras se evalúan antes de ejecutarse. Una sustitución de esfuerzo equivalente puede acordarse por escrito antes de iniciar el trabajo. Si aumenta el esfuerzo, se comunica el diferencial de horas, precio y plazo para su aprobación previa.


## Cuadro financiero contractual

| Concepto | USD de referencia | UF de contratación |
|---|---:|---:|
| Honorarios netos | 13.000,00 | 311,7235 |
| IVA del 19 % | 2.470,00 | 59,2275 |
| Total con IVA | 15.470,00 | 370,9510 |

| Pago | Día propuesto | Neto UF | IVA UF referencial | Total UF |
|---|---:|---:|---:|---:|
| Anticipo al inicio | 0 | 124,6894 | 23,6910 | 148,3804 |
| Cuota mensual 1 | 30 | 31,1724 | 5,9228 | 37,0952 |
| Cuota mensual 2 | 60 | 31,1724 | 5,9228 | 37,0952 |
| Cuota mensual 3 | 90 | 31,1724 | 5,9228 | 37,0952 |
| Cuota mensual 4 | 120 | 31,1724 | 5,9228 | 37,0952 |
| Cuota mensual 5 | 150 | 31,1724 | 5,9228 | 37,0952 |
| Cuota mensual 6 | 180 | 31,1721 | 5,9225 | 37,0946 |

Las seis cuotas mensuales financian el desarrollo. El anticipo corresponde al 40 % y el saldo al 60 %. La última cuota concilia el redondeo de cuatro decimales. Los días 30 a 180 desde el inicio son una condición de calendario propuesta; las fechas se fijan en la orden de compra.

La UF queda fijada como unidad contractual al emitir esta propuesta. El USD se muestra únicamente como referencia de origen; no se aplica un segundo reajuste por dólar. La factura se emite en CLP según la UF del vencimiento acordado, calculando el IVA sobre la base en CLP. Los importes de IVA en UF son referenciales.

Referencias consultadas el 15 de octubre de 2026: UF CLP 41.162,73 y dólar observado CLP 987,03. [Banco Central de Chile](https://si3.bcentral.cl/indicadoressiete/secure/IndicadoresDiarios.aspx?Idioma=es-CL), [UF SII](https://www.sii.cl/valores_y_fechas/uf/uf2026.htm) e [IVA SII](https://www.sii.cl/preguntas_frecuentes/impuestos_mensuales/001_130_0572.htm). Vigencia comercial propuesta de 30 días.
