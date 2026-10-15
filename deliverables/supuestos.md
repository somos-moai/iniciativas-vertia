Supuestos comerciales comunes a Prospectador y Contratos

15 de octubre de 2026 · Preparado para Vertia Group

## Fuente de precios e indicadores

Los precios netos de referencia fijados para presentar estas propuestas son USD 13.000 para Prospectador y USD 30.000 para Contratos. Esto no constituye una aceptación comercial del cliente. Los indicadores de conversión provienen de `docs/commercial/financials.json`, entregado por Codex: dólar observado del Banco Central CLP 987,03 y UF del SII CLP 41.162,73, ambos consultados el 15 de octubre de 2026. No se utiliza la conversión anterior de CLP 978,61 por dólar. Si `financials.json` cambia antes de formalizar, ambas propuestas deben recalcularse con el nuevo archivo, no con los valores de este documento.

## Unidad de contratación y redondeo

La Unidad de Fomento (UF) es la unidad de contratación y de cobro; el dólar es referencia informativa para que Vertia dimensione el valor en una moneda conocida. No se aplica un reajuste doble: el monto se fija en UF al emitir la propuesta y no se vuelve a indexar por tipo de cambio.

Los montos en UF se expresan con cuatro decimales. La última cuota de cada calendario de pagos absorbe la diferencia de redondeo acumulada por las cuotas anteriores, de modo que la suma de las siete cuotas coincida exactamente con el neto, el IVA y el bruto totales del proyecto.

## Conversión a pesos al momento del pago

Cada cuota se contrata en UF. Su equivalente en CLP se calcula con el valor de la UF del día de vencimiento efectivo acordado con Vertia, no con la UF de emisión de esta propuesta (15 de octubre de 2026). El IVA de referencia en UF de estas propuestas es informativo; la factura correspondiente calcula el IVA sobre la base en CLP del día de emisión de cada documento tributario.

## Calendario de pagos

Ambas propuestas usan la misma estructura: un anticipo del 40% al inicio del proyecto y seis cuotas mensuales netas iguales que completan el 60% restante, formalizadas como condición propuesta. La primera cuota mensual vence a los 30 días corridos desde el inicio del proyecto; cada cuota siguiente vence 30 días después de la anterior. Las cuotas financian el desarrollo descrito en cada propuesta; no constituyen un servicio de soporte recurrente, el cual se cotiza por separado.

## Servicios y licencias de terceros

AWS, PostgreSQL, el acceso a Claude API con el modelo Opus 5.5 como mínimo, OCR, Lusha o su proveedor equivalente, Microsoft 365, el proveedor de firma electrónica y cualquier otro servicio externo necesario para desarrollar, probar, aceptar y operar ambas soluciones son contratados y pagados directamente por Vertia. Esos costos no están incluidos en los honorarios de desarrollo ni en la bolsa de soporte de MoAI descritos en `prospectador.md` y `contratos.md`.

## Soporte y garantía

El soporte mensual es un servicio independiente del desarrollo, a contratar desde que cada solución entra en producción; no se activa automáticamente al firmar esta propuesta. La garantía de 60 días cubre exclusivamente defectos del alcance entregado y no consume horas de la bolsa de soporte. Las horas de soporte no utilizadas en un mes no se acumulan salvo acuerdo expreso posterior.

## Vigencia y formalización

Ambas propuestas son válidas por 30 días desde su emisión, hasta el 14 de noviembre de 2026. El alcance contempla solicitar a Vertia los accesos a Claude Opus 5.5, OCR, Lusha o equivalente, Microsoft 365 y un proveedor de firma. La habilitación efectiva se verifica antes del inicio de la integración; este documento no acredita la contratación ni la aprobación de cuentas por parte del cliente. Los agentes de desarrollo utilizan Claude Code, Codex y Antigravity por separado de las APIs del producto.

## Lo que no se afirma en estas propuestas

No se incluyen cifras de retorno de inversión, ahorro de tiempo ni resultados ya logrados: ningún número de impacto comercial se presenta como medido o garantizado. No se mencionan clientes de MoAI sujetos a confidencialidad. Toda función demostrada en la plataforma de demostración de este proyecto se identifica como adaptador simulado o dato sintético y no se presenta como integración real ni como firma legalmente vinculante; las propuestas comerciales describen el sistema productivo a construir, independiente del código de demostración.

## Decisiones pendientes que afectan el precio final

Las siguientes decisiones, si cambian el alcance descrito en `prospectador.md` o `contratos.md`, requieren una revisión de precio por control de cambios antes de ejecutarse:

- Número final de ejecutivos y países en operación productiva más allá del piloto.
- Selección del proveedor de enriquecimiento de prospectos y del proveedor de firma electrónica.
- Catálogo definitivo de tipos de contrato, plantillas y volumen de migración de contratos vigentes.
- Matriz de niveles de aprobación por país y monto para el flujo contractual acotado.
- Fecha y condición de la integración con POST y con cualquier ERP o CRM existente.
