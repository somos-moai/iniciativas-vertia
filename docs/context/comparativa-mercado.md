# Comparación de mercado para la gestión contractual de Vertia

Fecha de consulta: 15 de octubre de 2026  
Moneda: USD antes de impuestos  
Objetivo: comparar el MVP documental y el roadmap CLM planteados para Vertia con soluciones contratables, usando precios y condiciones publicados por sus proveedores.

## 1. Conclusión para la decisión

Hay competencia directa para el repositorio, búsqueda, alertas, colaboración, firma y análisis de contratos. Almacenar documentos y agregar un asistente de IA no es por sí solo una diferenciación suficiente para justificar un desarrollo a medida.

El desarrollo puede justificarse por control de infraestructura y datos, reglas específicas de acceso entre países, documentos para licitaciones, integración con el ecosistema Vertia y un uso de Claude bajo condiciones propias. Esas ventajas son objetivos de diseño que todavía deben implementarse y probarse; no son capacidades ya entregadas.

La recomendación es comparar en una prueba funcional breve cuatro candidatos: Zoho Contracts, ContractSafe, Concord y Webdox. Para un repositorio inicial, también debe evaluarse reutilizar SharePoint si las licencias corporativas lo permiten. DocuSign IAM es una alternativa adicional si la prioridad es firma y administración de acuerdos; su precio no representa el de DocuSign CLM.

## 2. Alcances que no deben mezclarse

| Alternativa | Alcance considerado | Estado |
|---|---|---|
| MVP documental MoAI | Repositorio, ficha, versiones, permisos por país, solicitudes de acceso, auditoría, OCR, búsqueda, Claude, protección de información y alertas básicas. | Propuesta de desarrollo de 320 horas; pendiente de descomposición y validación de reutilización. |
| Roadmap CLM MoAI | Lo anterior más plantillas, revisión, aprobación, firma, obligaciones, enmiendas, renovaciones, integraciones, portal y expansión regional. | Estimación de planificación de 960 horas totales, no precio cerrado validado del programa completo. |
| SaaS documental | Producto ya disponible para repositorio, búsqueda, alertas y colaboración; funciones según plan. | Suscripción y configuración. |
| SaaS CLM | Producto ya disponible para parte o todo el ciclo contractual; módulos y controles según edición. | Suscripción, implementación y posibles integraciones adicionales. |
| Configuración Microsoft | Repositorio y procesos sobre servicios existentes de Microsoft 365. | Trabajo de configuración y desarrollo; no es un CLM completo listo por pagar una licencia. |

La especificación original incluye exigencias superiores a un repositorio: aislamiento por país y sociedad, confidencialidad nominativa, aprobaciones, firma, auditoría inmutable, búsqueda que respete permisos, continuidad y gobierno regional. Su sección 25 contempla explícitamente decidir entre construir y contratar una plataforma. Fuente interna: [especificación CLM](CLM_Global_Especificacion_Tecnica.md), secciones 17 a 21 y 25.

## 3. Método y supuestos

- Se revisaron páginas oficiales de producto, precios, ayuda y condiciones. Los importes de blogs de terceros no se usaron como precios comerciales de los proveedores.
- Cuando una página genera precios dinámicamente, se revisó el contenido de su selector o archivo de precios oficial. Esto permitió verificar los tramos de ContractSafe y los importes USD de Zoho.
- Los escenarios aceptados para esta comparación son 10 y 20 usuarios gestores, con 500 y 2.500 contratos. Son escenarios hipotéticos, no cantidades confirmadas de Vertia.
- Un usuario gestor, un aprobador ocasional, un lector y un firmante externo pueden tener licencias distintas. No se asume que las 20 personas requieran 20 licencias completas.
- Tampoco son equivalentes contratos almacenados, documentos, páginas OCR, contratos nuevos por mes y sobres enviados a firma. Cada proveedor mide unidades diferentes.
- Los precios anualizados se calculan con la modalidad anual publicada. Un precio expresado por mes no implica contratación cancelable mes a mes.
- Las proyecciones a 36 meses mantienen precios y cantidades constantes, sin descuentos, inflación, reajustes, tipo de cambio, impuestos ni valor presente.
- No se enviaron solicitudes comerciales a proveedores. Donde se requiere cotización, el precio continúa pendiente.

## 4. ContractSafe y su precio por volumen

Importes mensuales equivalentes con prepago anual, verificados en el selector oficial:

| Contratos activos | Organize | Finalize | Maximize |
|---|---:|---:|---:|
| 100 a 500 | 585 | 825 | 960 |
| 1.001 a 2.500 | 845 | 1.150 | 1.325 |

Organize ofrece repositorio e IA; Finalize añade SSO, aprobación y firma; Maximize añade API y plantillas. Es el plan de referencia cuando se exige API. El precio publicitado de 450 corresponde a 100 contratos o menos.

Fuente: [precios y selector oficial](https://www.contractsafe.com/pricing); se inspeccionaron sus atributos HTML.

Su FAQ declara usuarios ilimitados y asistencia de implementación, migración y capacitación. Confirmar alcance y conteo de anexos. Fuente: [FAQ oficial](https://www.contractsafe.com/faq).

## 5. Precios por usuario y por equipo

| Producto y plan | Precio publicado con modalidad anual | Referencia para Vertia | Fuente |
|---|---|---|---|
| Zoho Contracts Standard | 25 por usuario/mes | Entrada; límites distintos de Professional. | [Precios](https://www.zoho.com/es-xl/contracts/pricing.html) |
| Zoho Contracts Professional | 40 por usuario/mes | Incluye obligaciones y registros de auditoría según comparación. | [Comparación](https://www.zoho.com/contracts/plan-comparison.html) |
| Zoho Contracts Premium | 50 por usuario/mes | Más capacidades; no equivale a confirmar Claude Opus como motor. | [Precios](https://www.zoho.com/es-xl/contracts/pricing.html) |
| Concord Essentials | 499/mes, incluye 5 usuarios; adicional 49 | Repositorio, OCR, IA y firma; comprobar controles necesarios. | [Precios](https://www.concord.app/pricing/) |
| Concord Business | 899/mes, incluye 5; adicional 69 | Aprobaciones, roles y equipos. | [Precios](https://www.concord.app/pricing/) |
| Concord Enterprise | 1.299/mes, incluye 5; adicional 89 | Publica API y administración de subsidiarias. | [Precios](https://www.concord.app/pricing/) |
| Docusign IAM Starter | 45 por usuario/mes | Funciones y cuotas inferiores a Professional. | [IAM en USD](https://ecom.docusign.com/en-US/plans-and-pricing/iam) |
| Docusign IAM Standard | 50 por usuario/mes; mínimo 3 | SSO sujeto a ventas; no es Docusign CLM. | [IAM en USD](https://ecom.docusign.com/en-US/plans-and-pricing/iam) |
| Docusign IAM Professional | 80 por usuario/mes; mínimo 3 | SSO y 10 workflows; revisión/aprobación avanzada requiere verificar edición. | [IAM en USD](https://ecom.docusign.com/en-US/plans-and-pricing/iam) |
| PandaDoc Business | 49 por usuario/mes | Enfoque en generación, aprobación y firma; API consume créditos. | [Precios](https://www.pandadoc.com/pricing/) |
| PandaDoc Enterprise | Cotización | SSO y espacios de equipo; precio Business no lo representa. | [Precios](https://www.pandadoc.com/pricing/) |

En Zoho se contrastaron los valores con el [archivo oficial de precios USD](https://www.zohowebstatic.com/sites/zweb/json/pricing/contracts-pricing-val.json). Valores mensuales sin modalidad anual: Standard 30, Professional 48 y Premium 60. Sus usuarios Lite anuales cuestan respectivamente 5, 10 y 15; se requiere al menos una licencia principal. La [ayuda de licencias](https://help.zoho.com/portal/en/kb/contracts/introduction/articles/subscription-and-licensing) diferencia gestores y colaboradores.

Concord publica lectores e invitados gratuitos. Se debe confirmar qué operaciones exigen una licencia pagada y cómo se licencia SSO. La [página de integraciones](https://www.concord.app/integrations/) declara compatibilidad con Azure AD, pero no sustituye la confirmación comercial del plan.

Docusign IAM distingue envíos web de automatizados y aplica cuotas. Las capacidades avanzadas de revisión no están todas en el precio Professional. No usar una licencia eSignature o IAM para presupuestar el producto CLM.

PandaDoc publica cargos/créditos adicionales para API y automatización; el conector Claude aparece en beta y no prueba que el plan incluya un agente autónomo con Opus 5.5 y cuotas suficientes. Confirmar ese alcance antes de comparar.

## 6. Competidores con cotización requerida

| Proveedor y producto | Qué publica | Cómo compite | Precio y pendientes |
|---|---|---|---|
| Webdox CLM | Essential: 15 administradores/operadores y 20 colaboradores; Professional: 30 y 60; Business: 50 y 150. Publica IA, firma, workflows y API. | Candidato directo para gestión contractual regional y operación en español. | Sin importe público verificable en la página. Pedir costo anual, implementación, capacidad IA y condiciones locales. [Fuente](https://www.webdoxclm.com/pricing). |
| Juro | Precio por volumen contractual y complejidad; usuarios, workflows y plantillas ilimitados según FAQ. Integraciones profundas pueden costar más. | CLM con generación, revisión y colaboración. | Cotización; no interpretar el valor inicial 0 del formulario como plan gratuito. [Fuente](https://juro.com/pricing). |
| Docusign CLM | Generación, negociación, workflow, repositorio e integraciones. | Competidor del roadmap completo. | Cotización independiente de IAM y eSignature; pedir implementación, conectores y soporte. [Fuente](https://www.docusign.com/products/clm). |
| Ironclad | CLM configurable, implementación propia, del proveedor o partners; algunas integraciones se cobran aparte. | Gestión contractual empresarial y legal. | Cotización. No se usó una estimación de terceros como precio oficial. [Fuente](https://ironcladapp.com/pricing). |
| Agiloft | Página de solicitud de precio; servicios de implementación y soporte separados en su oferta. | CLM configurable; declara controles por registro y campo. | Cotización; validar despliegue, motor, módulos y SLA. [Precios](https://www.agiloft.com/pricing), [seguridad](https://www.agiloft.com/terms-policies/security). |
| ContractWorks | Standard incluye 2.500 documentos, usuarios ilimitados y 5 licencias de firma; publica OCR. | Repositorio y administración documental. | La página consultada no muestra importe numérico y su HTML oculta precios. Solicitarlo; no asumir antiguos importes de comparadores. [Fuente](https://www.contractworks.com/contract-management-software-pricing). |
| Contractbook | Essential: 1 usuario y hasta 100 contratos firmados/año; Centralize: 5 y 350; Accelerate: 10 y 500. | Creación, colaboración y automatización contractual. | Los paquetes consultados no entregan un importe verificable; cotizar usuarios y volumen de firma. [Fuente](https://contractbook.com/pricing). |

No se les asigna un costo anual ficticio. Tampoco se infiere que la existencia de una API implique un conector POST o ERP ya construido.

## 7. Alternativa Microsoft para el MVP documental

[SharePoint Online Plan 1](https://www.microsoft.com/en-us/microsoft-365/sharepoint/compare-sharepoint-plans) publica 5 por usuario/mes con pago anual. Son 600/año para 10 usuarios o 1.200/año para 20, si se necesitara comprarlo por separado. Vertia podría tener derechos de uso mediante Microsoft 365; TI debe revisar el contrato vigente antes de comprar otra licencia.

[Power Automate Premium](https://www.microsoft.com/en-us/power-platform/products/power-automate/pricing) publica 15 por usuario/mes con pago anual; también existen licencias por proceso. No corresponde multiplicar automáticamente 15 por toda persona que vea documentos: el licenciamiento depende del diseño y los conectores.

SharePoint requiere configurar metadatos, permisos, solicitudes, versiones y flujos. OCR, clasificación, firma, agentes y tratamiento de información confidencial necesitan diseño y posibles licencias o consumos adicionales. No se presenta el precio de SharePoint como el costo total de un CLM.

Inferencia para Vertia: si la primera necesidad es organizar documentos y controlar accesos, revisar Microsoft antes de financiar un repositorio nuevo. Si AWS y PostgreSQL propios son obligatorios, esta alternativa no satisface ese requisito de arquitectura tal como está planteada.

## 8. Escenarios económicos por licencia

### 8.1 Productos por usuario

Importes calculados a partir de los precios oficiales anteriores. Todos los usuarios de estas filas se consideran gestores pagados, salvo la fila Lite. El volumen almacenado, capacidad IA y equivalencia funcional se validan aparte; no se afirma que cada plan satisfaga todos los controles de Vertia para 2.500 contratos.

| Plan | Usuarios | Equivalente mensual | Un año | 36 meses |
|---|---:|---:|---:|---:|
| Zoho Professional | 10 | 400 | 4.800 | 14.400 |
| Zoho Professional | 20 | 800 | 9.600 | 28.800 |
| Zoho Premium | 10 | 500 | 6.000 | 18.000 |
| Zoho Premium | 20 | 1.000 | 12.000 | 36.000 |
| Zoho Professional: 5 gestores y 15 Lite | 20 personas | 350 | 4.200 | 12.600 |
| Concord Business | 10 | 1.244 | 14.928 | 44.784 |
| Concord Business | 20 | 1.934 | 23.208 | 69.624 |
| Concord Enterprise | 10 | 1.744 | 20.928 | 62.784 |
| Concord Enterprise | 20 | 2.634 | 31.608 | 94.824 |
| Docusign IAM Professional | 10 | 800 | 9.600 | 28.800 |
| Docusign IAM Professional | 20 | 1.600 | 19.200 | 57.600 |
| PandaDoc Business | 10 | 490 | 5.880 | 17.640 |
| PandaDoc Business | 20 | 980 | 11.760 | 35.280 |

PandaDoc Business no se trata como equivalente a un plan con SSO. Las tarifas de estas tablas son de licencia; no son TCO completos ni incluyen necesariamente implementación, migración, integración, firma especial, soporte ampliado o consumos adicionales.

### 8.2 Productos por volumen

Estos cálculos usan el selector del apartado 4 y la política de usuarios de su FAQ.

| Plan | Contratos activos | Equivalente mensual | Un año | 36 meses |
|---|---:|---:|---:|---:|
| Maximize | 500 | 960 | 11.520 | 34.560 |
| Maximize | 2.500 | 1.325 | 15.900 | 47.700 |

La licencia de API no equivale a financiar el desarrollo del conector.

## 9. Comparación con el presupuesto de desarrollo MoAI

Valores internos de planificación ya presentados:

| Concepto | Valor |
|---|---:|
| MVP documental de 320 horas | 19.619,66 una vez |
| Roadmap CLM de 960 horas, incluido el MVP | 58.858,99 de desarrollo total |
| Soporte inicial de Contratos | 490,49/mes, 12 horas mensuales |
| Claude: escenario previo de consumo productivo | 528/mes |

El escenario Claude supone 5.000 llamadas al mes, 12.000 tokens de entrada y 2.000 de salida por llamada, con 20% de holgura. Es un supuesto de volumen, no una cotización de gasto obligatorio ni una medición real. Referencia para actualizar tarifas: [Claude API](https://platform.claude.com/docs/en/about-claude/pricing).

### 9.1 Costos comparables parcialmente calculables

| Escenario MoAI | Un año | 36 meses |
|---|---:|---:|
| MVP + soporte de 490,49/mes | 25.505,54 | 37.277,30 |
| MVP + soporte + Claude según escenario de 528/mes | 31.841,54 | 56.285,30 |
| Roadmap completo + mismo soporte inicial | 64.744,87 | 76.516,63 |
| Roadmap completo + mismo soporte + Claude del escenario | 71.080,87 | 95.524,63 |

Fórmula: desarrollo + meses × soporte; cuando corresponde se suma meses × consumo Claude. Se muestran ventanas con 12 o 36 meses completos de operación para comparar recurrencia; no constituyen un calendario de pagos ni significan que todo el roadmap se contrate o entregue el primer año. El soporte puede crecer al incorporar países e integraciones: mantener 12 horas es solo un supuesto de comparación.

Faltan AWS, PostgreSQL, OCR, firma, pruebas con APIs, migración extraordinaria, nuevas funciones y costos internos de Vertia. La reserva opcional del 15% tampoco está incluida. Los servicios externos son pagados por Vertia, pero siguen siendo parte de su costo total de propiedad.

### 9.2 Lectura económica

- El MVP más soporte cuesta aproximadamente 37.277 en tres años antes de infraestructura y APIs. Eso supera las licencias de Zoho Professional en ambos escenarios y queda cerca del costo de licencia de ContractSafe Maximize para 500 contratos.
- Al sumar el escenario previo de Claude, el MVP llega a aproximadamente 56.285 antes de AWS y OCR. El gasto de IA debe medirse: cambia materialmente la comparación.
- Los planes SaaS pueden incluir firma, flujos u otras funciones que aún no existen en nuestro MVP; a la vez, sus licencias pueden excluir la integración o confidencialidad específica requerida. La comparación no demuestra equivalencia funcional ni ahorro garantizado de ninguna ruta.
- No corresponde sumar automáticamente nuestra misma API Claude a todos los SaaS: algunos ya incluyen IA propia. Si Vertia exige específicamente Opus, hay que cotizar cómo se integra y qué licencia o consumo adicional requiere.

## 10. Diferencias que deben demostrarse antes de elegir

La existencia de un control genérico de permisos no prueba el flujo de compartimentación solicitado por Philippe. Estas verificaciones aplican por igual a proveedores y desarrollo propio.

| Requisito de Vertia | Evidencia mínima | Efecto si falta |
|---|---|---|
| Acceso por país, sociedad y rol | Usuario de México no puede leer ni inferir contratos restringidos de Perú en pantalla, API o exportación. | Configuración adicional, edición superior o desarrollo. |
| Solicitud de acceso entre países | Solicitud justificada, aprobación del dueño, alcance limitado, vencimiento y revocación. | Workflow específico. |
| Información confidencial | Entregar una copia realmente saneada; el texto oculto no se recupera al copiar, exportar o revisar capas y metadatos. | Proceso documental adicional; no basta ocultar un campo. |
| IA y búsqueda con permisos | Una pregunta no revela importes, nombres, fragmentos ni documentos fuera de alcance. | Control previo y posterior de recuperación y generación. |
| Acceso privilegiado | Definir quién puede ver contratos confidenciales, incluido soporte y administradores, y cómo se autoriza una excepción. | Brecha de seguridad o cambio de diseño. |
| Auditoría | Registrar lecturas sensibles, descargas, permisos y acciones; demostrar retención e inmutabilidad requerida. | Módulo o integración adicional. |
| Licitaciones y antecedentes | Cartas de experiencia, diseños y fichas técnicas como documentos independientes, con sus permisos y vínculos. | Una herramienta centrada solo en contratos puede requerir adaptación. |
| Cinco países | Sociedades, zonas horarias, calendarios, moneda, plantillas y aprobaciones sin mezclar accesos. | Configuración regional y validación local. |
| Firma | Proveedor aceptado, evidencias, cancelaciones, webhooks y requisitos locales validados por Legal. | Conector, licencias y consumo. |
| CRM, POST y ERP | API accesible en el plan y demostración del mapeo de identificadores, errores y conciliación. | Trabajo de integración a presupuestar. |
| Infraestructura y base propia | Confirmación expresa de si la oferta puede operar en AWS de Vertia y con PostgreSQL bajo su control. | La suscripción estándar puede no satisfacer la arquitectura exigida. |
| Claude Opus mínimo | Identificador de modelo, llamadas autorizadas, herramientas, cuotas, costo y política de datos verificables. | IA nativa o un conector genérico no demuestra cumplimiento. |
| Continuidad y salida | SLA, backup, restauración, residencia de datos, exportación completa y costo de terminar. | Riesgo operativo o dependencia comercial. |

No se presume que algún SaaS carezca de estas capacidades por no detallarlas en su página de precios. Tampoco se presume que el desarrollo propio ya las cumpla por figurar en el alcance.

## 11. Información para pedir en cotizaciones comparables

Usar el mismo cuestionario con todos los candidatos:

1. Precio para 10 y 20 usuarios completos y una mezcla de 5 gestores + 15 aprobadores/lectores.
2. Precio para 500 y 2.500 contratos activos; tratamiento de anexos, versiones, documentos de licitación, archivados y páginas OCR.
3. Compromiso mínimo, pago anual/mensual, moneda, impuestos, reajuste, renovación y posibilidad de reducir usuarios.
4. Implementación, migración, limpieza de datos, configuración por país, capacitación y validación incluidas o cotizadas por separado.
5. SSO Entra ID, altas y bajas, permisos por país, acceso excepcional y confidencialidad frente a administradores.
6. API, webhooks, límites, sandbox, conectores CRM/ERP/POST y costos de habilitación y operación.
7. Cuotas IA/OCR, páginas, idiomas, calidad en español, condiciones de datos y opción de usar Claude Opus con un proyecto de Vertia.
8. Firma incluida o externa, sobres y automatizaciones, verificación de identidad y cobros de proveedores locales.
9. SLA, horarios y canales de soporte, incidentes críticos, continuidad y costos de soporte premium.
10. Exportación de archivos, metadatos, relaciones e historial, asistencia de salida y eliminación certificada cuando corresponda.

Esta lista prepara una comparación formal; no implica que se hayan solicitado ofertas en nombre de Vertia.

## 12. Recomendación de evaluación

| Candidato | Por qué lo probaría | Qué debe resolver para ganar |
|---|---|---|
| Zoho Contracts Professional/Premium | Referencia de costo baja y funciones contractuales documentadas. | Permisos regionales, datos/IA, conectividad corporativa y proceso de confidencialidad. |
| ContractSafe Maximize | Precio por volumen, usuarios ilimitados y plan que publica API y SSO. | Uso de antecedentes no contractuales, compartimentación y costo con el volumen real. |
| Concord Enterprise | Referencia pública con API y subsidiarias, y colaboración contractual. | Licencias efectivamente necesarias, SSO, condiciones de implementación y permisos precisos. |
| Webdox | Oferta regional con roles de operador/colaborador, IA y API publicadas. | Cotización total y demostración de los controles de Vertia. |
| Microsoft sobre licencias existentes | Posible reutilización para un repositorio documental inicial. | Esfuerzo real de configuración, agentes, OCR, seguridad y mantenimiento. |

Mi recomendación es realizar una prueba con documentos autorizados representativos: un contrato vigente, uno escaneado, un anexo, una carta de experiencia y una ficha técnica, usando al menos dos países y tres perfiles. Pedir que cada candidato ejecute los casos de la sección 10, en vez de evaluar solo una presentación comercial.

Si una plataforma cubre las necesidades críticas a menor costo total, MoAI puede aportar levantamiento, configuración, integraciones y operación. Si las brechas de confidencialidad, infraestructura o flujo específico son decisivas, el desarrollo propio debe centrarse en esas diferencias y reutilizar lo que ya resuelve bien el mercado.
