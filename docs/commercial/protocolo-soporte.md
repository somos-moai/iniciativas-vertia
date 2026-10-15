# Protocolo propuesto de operación mantención y soporte

Aplicable a ambas iniciativas con bolsas y registros independientes. Las condiciones siguientes forman parte de la propuesta y deben incorporarse al acuerdo de servicio antes de producción. Las seis cuotas posteriores al anticipo financian el desarrollo; no equivalen a seis meses de soporte.

## Antes de producción

MoAI registra decisiones, versiones y cambios en el repositorio; revisa los cambios antes de publicarlos y utiliza pruebas separadas de producción. Vertia valida datos, permisos, reglas y servicios externos. Cada entrega presenta su alcance, evidencia de pruebas, incidencias conocidas, responsable de aceptación y procedimiento para volver a la versión anterior.

El piloto debe completar un ciclo operativo por iniciativa. Prospectador: incorporación de contacto, asignación, campaña aprobada, seguimiento, respuesta o exclusión y actualización del resultado. Contratos: incorporación documental, extracción revisada, solicitud, aprobación, firma de prueba, activación y seguimiento de obligación. Los conectores productivos requieren una prueba real controlada y autorizada distinta de la demostración sintética.

## Servicio mensual desde la puesta en producción

| Iniciativa | Dedicación propuesta | UF netas al mes | USD netos de referencia |
|---|---:|---:|---:|
| Prospectador | 8 horas | 7,8408 | 326,99 |
| Gestión Contractual | 12 horas | 11,7613 | 490,49 |

IVA del 19 % adicional. Conversión de referencia del 15 de octubre de 2026 contenida en financials.json. Cada bolsa cubre revisión de registros y trabajos pendientes, correcciones menores, actualizaciones compatibles, revisión de consumo, acompañamiento funcional y reporte de servicio. El tiempo se registra por ticket. Las horas no se acumulan salvo acuerdo escrito; no se excede una bolsa con cobro adicional sin aprobación escrita.

La garantía de 60 días desde la aceptación de producción cubre defectos reproducibles respecto del alcance aceptado, sin consumir horas de soporte. Nuevos flujos, integraciones, países con reglas adicionales, rediseños o aumentos sustanciales de volumen se gestionan mediante cambio de alcance. Una interrupción de AWS o un proveedor se coordina dentro del soporte disponible, pero la resolución del proveedor depende de su propio contrato.

## Recepción y atención de incidencias

Vertia designa dos contactos autorizados y MoAI un responsable de servicio. Se utiliza un registro compartido de tickets, con correo somos@mo-ai.cl como canal de entrada hasta habilitar el sistema definitivo. Cada ticket contiene iniciativa, ambiente, hora, impacto, pasos de reproducción, evidencia sin secretos y responsable del seguimiento.

Horario propuesto: lunes a viernes de 09:00 a 18:00, hora de Chile continental, excluidos festivos. Para impacto crítico en producción sin alternativa operativa, primera respuesta en hasta cuatro horas hábiles; para otras incidencias, hasta un día hábil. La respuesta incluye clasificación, responsable y siguiente actualización. El plazo de solución depende del diagnóstico y las dependencias; no se ofrece cobertura permanente ni resolución garantizada en cuatro horas.

MoAI clasifica, reproduce y propone corrección o mitigación. Vertia valida la recuperación cuando se requiera acceso funcional. El cierre registra causa, cambio, pruebas y medidas de prevención. Un incidente crítico recibe actualizaciones en cada avance relevante y al cierre de cada jornada hábil mientras continúe abierto.

## Rutinas de mantención

Semanalmente se revisan errores, colas, alertas y consumos. Mensualmente se entrega un informe de tickets, horas, disponibilidad observada, gasto de terceros reportado por sus plataformas y mejoras recomendadas. El registro distingue consumos reales de estimaciones.

Trimestralmente se propone una restauración controlada y revisión de permisos. Estas actividades se planifican dentro de la bolsa o se presupuestan si la exceden. Vertia mantiene las licencias, medios de pago, políticas corporativas y acceso a sus cuentas; MoAI mantiene la aplicación dentro del alcance contratado.

## Publicaciones y cambios

Todo cambio pasa por definición, evaluación de impacto, presupuesto si corresponde, aprobación escrita, implementación, pruebas, aceptación y publicación. Una mejora puede sustituir otra de esfuerzo equivalente antes de iniciarla, si ambas partes registran el intercambio y no compromete seguridad ni aceptación. Si aumenta complejidad o requiere rehacer trabajo aceptado, se informa el diferencial de horas, precio y plazo antes de ejecutar.

Los cambios normales se publican en una ventana acordada con respaldo, lista de verificaciones y responsable. Un cambio urgente registra su justificación y se revisa posteriormente. Nunca se usan claves productivas en el código, en tickets ni en datos sintéticos. El cierre o transición de servicio entrega código pactado, manuales, inventario de dependencias y revoca los accesos de quienes dejan de operar.
