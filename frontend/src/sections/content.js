export const FLOWS={
 prospectador:[
  {title:'Perfilar y priorizar',summary:'Empresa, rubro y señales → criterios y faltantes → cuenta priorizada. La afinidad es coincidencia con criterios, no probabilidad de venta.',actor:'Ejecutivo · criterios de Santiago Ordoñez'},
  {title:'Encontrar y revelar',summary:'Cuenta y cargo → revisar candidatos y costo → contacto vinculado y créditos trazables. Reutilizar contactos adquiridos.',actor:'Ejecutivo · proveedor autorizado'},
  {title:'Preparar y aprobar',summary:'Contexto y destinatarios → borrador editable → revisión humana. Cambiar contenido exige nueva aprobación.',actor:'Ejecutivo · jefatura para campañas masivas'},
  {title:'Enviar y escuchar',summary:'Mensaje aprobado → secuencia y límites → respuestas, rebotes o exclusión. Una respuesta detiene el seguimiento.',actor:'Ejecutivo · Microsoft 365 simulado en demo'},
  {title:'Reunir y avanzar',summary:'Conversación → reunión y propuesta → oportunidad, monto, etapa y próximo paso. El historial permite revisar el embudo.',actor:'Ejecutivo · Agustín Silva, jefatura'},
 ],
 contratos:[
  {title:'Solicitar e incorporar',summary:'Solicitud y PDF o imagen → expediente y versión. La lectura digital conserva texto por página; el escaneo de imágenes es simulado en esta demo.',actor:'Área solicitante · responsable del expediente'},
  {title:'Verificar con evidencia',summary:'Texto y campos sugeridos → contrastar página, monto, contraparte y vigencia → ficha confirmada por una persona.',actor:'Responsable documental · Claude API simulado'},
  {title:'Revisar y aprobar',summary:'Versión identificada → revisar, devolver o aprobar → decisión con fecha y motivo. Acceso entre países con autorización y copia saneada.',actor:'Legal · aprobadores definidos por Vertia'},
  {title:'Formalizar',summary:'Versión aprobada → proveedor de firma autorizado → estado y documento vigente. La firma del prototipo es simulada.',actor:'Apoderado · contraparte · proveedor por habilitar'},
  {title:'Cumplir y renovar',summary:'Contrato activo → responsables, obligaciones y alertas → evidencia y vencimiento. Automatización avanzada es ampliación.',actor:'Responsable del contrato · supervisión regional'},
 ]
};
export const MODELS={
 prospectador:[
  {name:'Empresa',fields:['País, sociedad y rubro','Perfil, criterios y fuentes','Cobertura, faltantes y afinidad','Responsable de cartera'],why:'Es la cuenta central. Una empresa agrupa varios contactos, actividades y oportunidades.'},
  {name:'Contacto',relation:'Empresa 1:N Contacto',fields:['Empresa y cargo','Correo y teléfono','Origen y revelación','Exclusión y cartera'],why:'Los datos de contacto se reutilizan según permisos y conservan su origen.'},
  {name:'Campaña',relation:'Contacto N:N Campaña',fields:['Contactos y secuencia','Contenido y versión','Revisión y aprobador','Envíos, respuestas y rebotes'],why:'La aprobación corresponde a un contenido y una lista; ambos deben poder reconstruirse.'},
  {name:'Actividad',relation:'Contacto 1:N Actividad',fields:['Mensaje, respuesta o reunión','Fecha y responsable','Resultado y motivo','Referencia al origen'],why:'El historial registra hechos y mantiene el siguiente paso de la relación.'},
  {name:'Oportunidad',relation:'Empresa 1:N Oportunidad',fields:['Cuenta y contacto','Monto y moneda','Etapa y responsable','Próxima gestión y resultado'],why:'La oportunidad vincula la conversación con una gestión comercial medible.'},
 ],
 contratos:[
  {name:'Contrato',fields:['País, sociedad y contraparte','Tipo, monto y moneda','Vigencia y responsable','Estado y versión vigente'],why:'Es el expediente central. Agrupa documentos, decisiones, obligaciones y autorizaciones.'},
  {name:'Documento / versión',relation:'Contrato 1:N Documento',fields:['Archivo y huella','Número de versión','Texto y evidencia por página','Revisión ligada al documento'],why:'El borrador y la lectura pertenecen a una versión identificada; no deben mezclarse entre documentos.'},
  {name:'Revisión',relation:'Documento 1:N Revisión',fields:['Versión revisada','Aprobador y fecha','Decisión y motivo','Correcciones y estado'],why:'Una aprobación conserva la referencia a lo que se revisó y a quién resolvió.'},
  {name:'Obligación',relation:'Contrato 1:N Obligación',fields:['Compromiso y responsable','Fecha de vencimiento','Estado y evidencia','Aviso y seguimiento'],why:'El registro básico y la alerta están incluidos; los flujos avanzados se cotizan aparte.'},
  {name:'Permiso temporal',relation:'Contrato 1:N Permiso',fields:['Solicitante y país','Motivo y aprobador','Alcance autorizado','Vencimiento del acceso'],why:'Compartir una copia revisada no concede acceso irrestricto al archivo original.'},
 ]
};
