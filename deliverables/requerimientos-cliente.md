# Requerimientos que debe proporcionar Vertia

Versión 1 del 15 de octubre de 2026. Aplica por separado al Prospectador comercial y a Gestión Contractual. Estos recursos son habilitados, administrados comercialmente y pagados por Vertia. No forman parte de los USD 13.000 y USD 30.000 netos de desarrollo. La infraestructura del VPS demostrativo es independiente de la infraestructura AWS de producción.

## Base propuesta para dimensionar AWS y PostgreSQL

Proponemos una plataforma compartida con aislamiento entre aplicaciones y entre pruebas y producción. No se solicita una cuenta AWS ni una instancia física por cada país. Argentina, Chile, Perú, México y Uruguay se separan mediante permisos y configuración de la aplicación. Cualquier residencia de datos obligatoria por país debe validarse antes del diseño definitivo y puede modificar esta base.

| Recurso lógico solicitado | Cantidad base | Uso y condición |
|---|---:|---|
| Cuenta AWS de Vertia | 1 | Titularidad, facturación y responsable técnico designado por Vertia |
| Entornos | 2 | Pruebas integradas y producción; cuentas separadas si la política corporativa lo exige |
| Redes VPC | 2 | Una por entorno con subredes y reglas de seguridad; no exposición pública de PostgreSQL |
| Despliegues de aplicación | 4 | Prospectador y Contratos, cada uno en pruebas y producción |
| PostgreSQL administrado | 2 instancias lógicas | Una de pruebas y una de producción; cada una con dos bases y roles separados |
| Bases PostgreSQL de aplicación | 4 | prospectador_test, contratos_test, prospectador_prod y contratos_prod; nombres definitivos por TI |
| Almacenamientos S3 | 4 buckets | Documentos y exportaciones, separados por aplicación y entorno; cifrado, versionado y ciclo de vida |
| Secretos de conexión | 4 conjuntos mínimos | Uno por aplicación y entorno; incluir claves de proveedores sin almacenarlas en el repositorio |
| Identidades de ejecución | 4 roles mínimos | Permisos mínimos por despliegue; accesos humanos nominativos separados |
| Puntos de entrada HTTPS | 4 nombres | Dos aplicaciones por dos entornos; certificados y DNS bajo control de Vertia |
| Observabilidad | 4 grupos de registros | Registros, alarmas de error y consumo, auditoría sin contenido sensible innecesario |
| Respaldo PostgreSQL | 2 políticas | Una por entorno, con restauración probada; producción con recuperación a un punto en el tiempo |

Son cantidades de recursos lógicos, no una suma de máquinas que deban contratarse. El servicio de cómputo puede ser ECS Fargate u otra plataforma aprobada por TI. No se obliga a contratar simultáneamente EC2, ECS y Lambda. El balanceador, las zonas de disponibilidad, las salidas de red y WAF se concretan con TI según disponibilidad, conectividad y política corporativa. Una instancia administrada Multi AZ puede incluir varios nodos físicos sin cambiar el número de bases solicitado.

La base compartida reduce administración. La separación física entre aplicaciones se considera una alternativa si TI la exige: pasarían de dos a cuatro instancias PostgreSQL lógicas, manteniendo cuatro bases de aplicación. Esta alternativa debe cotizarla AWS a Vertia; no aumenta por sí sola los honorarios MoAI sin un cambio de implementación aprobado.

Dimensionamiento inicial para validar, no garantía de capacidad: PostgreSQL de pruebas equivalente a 2 vCPU y 4 GB; producción equivalente a 2 vCPU y 8 GB, almacenamiento inicial 100 GB y autoescalado de disco. Cada aplicación parte de 1 vCPU y 2 GB por tarea, ajustándose mediante pruebas de carga. El número de réplicas y la alta disponibilidad se acuerdan antes de producción. El volumen documental se almacena en S3, no como archivos binarios en PostgreSQL.

## Servicios y accesos del Prospectador

1. Un proveedor de prospectos, Lusha o equivalente, con plan que permita API, créditos contratados y condiciones de uso compatibles con los países objetivo. Vertia entrega la cuenta y confirma el presupuesto de consumo.
2. Microsoft 365 y Microsoft Graph con registro de aplicación y consentimiento del administrador. Piloto con hasta cinco buzones de ejecutivos y sus calendarios. Las políticas de correo, límites y remitentes son de Vertia.
3. Acceso a Claude API con Opus 5.5 como modelo mínimo acordado. Deben habilitarse proyectos o claves separados para pruebas y producción, límites de gasto y responsable de facturación.
4. API POST documentada, ambiente de pruebas, responsable funcional y credenciales con permisos acotados. Si no existe API utilizable, la etapa base usa intercambio de archivos validado y el conector adicional se evalúa por separado.
5. Catálogo de empresas, agencias, contactos y carteras; reglas de asignación, exclusión y seguimiento; muestras anonimizadas y responsables de aceptación.

## Servicios y accesos de Gestión Contractual

1. Un proveedor OCR con API, por ejemplo Amazon Textract, cuya cuenta y consumo sean de Vertia. Definir idiomas, calidad mínima del escaneo y categorías documentales antes de la prueba de precisión.
2. Claude API con Opus 5.5 como mínimo acordado; separar claves, registros y presupuestos entre pruebas y producción. Vertia aprueba la política de envío de documentos al proveedor de IA.
3. Un proveedor de firma electrónica con API documentada y entorno de pruebas. Vertia proporciona licencias, validación legal por país y políticas de firma. La integración no convierte a MoAI en certificador ni reemplaza una validación jurídica local.
4. Muestras documentales, hasta seis categorías contractuales iniciales y cinco plantillas base, reglas de revisión y aprobación, matriz de acceso por país y sociedad y criterios para generar copias saneadas.
5. Un responsable jurídico y un responsable operativo para el piloto. Los textos, poderes de representación, criterios legales y plazos por país son validados por Vertia.

## Costos de terceros y control de consumo

Vertia paga directamente AWS, PostgreSQL, correo, proveedores de prospectos, Claude, OCR, firma electrónica y cualquier herramienta externa. Incluye consumos de desarrollo, pruebas, aceptación y producción. MoAI incluye el trabajo de integrar los proveedores delimitados en cada propuesta; sus licencias y consumos se excluyen de los honorarios.

El consumo de IA se calcula con tokens de entrada y salida, documentos y reintentos; el OCR por páginas y servicios contratados; la prospectación por créditos y consultas; la firma por sobres o documentos conforme al plan del proveedor. No se fija un gasto mensual inventado sin conocer volúmenes. Antes del piloto se medirá una muestra, se presentará una proyección de consumo separada y Vertia aprobará los límites. Alertas propuestas al 50 %, 80 % y 100 % del presupuesto; al alcanzar el límite, las tareas de consumo quedan en pausa controlada para revisión del administrador.

## Preparación y aceptación de infraestructura

Antes de iniciar el plazo de implementación deben existir accesos nominativos, entornos disponibles, muestras acordadas y responsables designados. Antes de producción se verifican HTTPS, mínimo privilegio, restauración de un respaldo, separación de entornos, trazabilidad, alertas y revocación de credenciales. La infraestructura de demostración no acredita estos requisitos de producción.

Los objetivos propuestos de respaldo son retención de 30 días, punto de recuperación de hasta 24 horas y recuperación de hasta 8 horas, sujetos a diseño aprobado, capacidad del servicio y prueba de restauración. No constituyen un SLA contratado automáticamente. La disponibilidad y recuperación final se pactan con TI y sus costos los asume Vertia.
