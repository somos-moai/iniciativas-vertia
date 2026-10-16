// Flujo completo y modelo de datos simulado de cada solución.
// Fuente: acciones y validaciones reales de backend/main.py y contrato en docs/coordination/codex-backend.md.
import React, {useMemo, useState} from 'react';
import {ArrowRight, Database, Workflow, ShieldCheck, KeyRound, Link2, Users, History, PlugZap, Info} from 'lucide-react';
import './flows.css';

const list = (S, kind) => (Array.isArray(S?.[kind]) ? S[kind] : []);
const count = (items, fn) => items.filter(fn).length;
const fmt = n => new Intl.NumberFormat('es-CL').format(Number(n) || 0);

const FLOWS = {
  prospectador: {
    intro: 'Desde la cartera hasta la oportunidad: cada paso valida permisos en el servidor, guarda el cambio en PostgreSQL y deja registro de auditoría.',
    stages: [
      {title: 'Cartera y datos base', goal: 'Empresas y contactos ordenados por ejecutivo y país.', actors: ['Ejecutivo', 'Jefatura'], actions: ['create_company', 'create_contact', 'import_contacts', 'update_contact'], entities: ['companies', 'contacts', 'activities'], rule: 'Solo correos .example. Contacto y empresa del mismo país. La importación omite duplicados por correo y revierte completa si una fila es inválida.', section: 'cartera', live: S => `${fmt(list(S, 'companies').length)} empresas · ${fmt(list(S, 'contacts').length)} contactos`},
      {title: 'Descubrimiento de prospectos', goal: 'Buscar responsables en un mercado y sector objetivo.', actors: ['Ejecutivo', 'Jefatura'], actions: ['search_prospects'], entities: ['prospects'], adapter: 'Lusha simulado', rule: 'Cada búsqueda genera tres candidatos con correo oculto. El perfil Legal no prospecta.', section: 'descubrir', live: S => `${fmt(count(list(S, 'prospects'), p => !p.revealed))} candidatos sin revelar`},
      {title: 'Revelación con créditos', goal: 'Incorporar a la cartera solo los contactos elegidos.', actors: ['Ejecutivo'], actions: ['reveal_contact'], entities: ['prospects', 'contacts', 'companies'], adapter: 'Lusha simulado', rule: 'Un crédito por contacto y máximo 250 por cartera. Un contacto ya revelado no se cobra de nuevo.', section: 'descubrir', live: S => `${fmt(S?.credits?.used)} de ${fmt(S?.credits?.limit)} créditos usados`},
      {title: 'Campaña y borrador asistido', goal: 'Preparar el mensaje para un grupo de contactos.', actors: ['Ejecutivo'], actions: ['create_campaign', 'draft_campaign', 'set_campaign_content'], entities: ['campaigns'], adapter: 'Claude simulado', rule: 'Entre 1 y 200 contactos de un mismo país, sin excluidos. Editar el texto revoca cualquier aprobación previa.', section: 'campanas', live: S => `${fmt(count(list(S, 'campaigns'), c => c.status === 'borrador'))} campañas en borrador`},
      {title: 'Aprobación humana', goal: 'Una persona responsable valida destinatarios y contenido.', actors: ['Jefatura', 'Regional'], actions: ['approve_campaign'], entities: ['campaigns'], rule: 'Sin aprobación no hay envío. La aprobación guarda una huella del contenido: si el texto cambia, se exige aprobar otra vez.', section: 'campanas', live: S => `${fmt(count(list(S, 'campaigns'), c => c.status === 'aprobada'))} campañas aprobadas`},
      {title: 'Envío controlado', goal: 'Enviar solo a quien corresponde, una sola vez.', actors: ['Ejecutivo', 'Jefatura'], actions: ['send_campaign'], entities: ['messages', 'contacts', 'campaigns'], adapter: 'Microsoft 365 simulado', rule: 'Omite contactos excluidos o que ya respondieron y bloquea el doble envío. Ningún correo sale de la aplicación.', section: 'campanas', live: S => `${fmt(count(list(S, 'messages'), m => m.direction === 'outbound'))} mensajes salientes registrados`},
      {title: 'Respuesta, exclusión y seguimiento', goal: 'Detener la secuencia apenas el contacto responde o pide no ser contactado.', actors: ['Ejecutivo'], actions: ['receive_reply', 'exclude_contact'], entities: ['messages', 'notifications', 'contacts'], rule: 'Una respuesta o exclusión cancela los seguimientos pendientes de ese contacto. Un excluido no se reactiva automáticamente.', section: 'seguimiento', live: S => `${fmt(count(list(S, 'contacts'), c => c.status === 'respondió'))} respuestas · ${fmt(count(list(S, 'contacts'), c => c.excluded))} exclusiones`},
      {title: 'Reunión', goal: 'Convertir la respuesta en una reunión agendada.', actors: ['Ejecutivo'], actions: ['log_meeting'], entities: ['activities', 'contacts'], adapter: 'Calendario simulado', rule: 'No se agendan acciones comerciales con contactos excluidos.', section: 'seguimiento', live: S => `${fmt(count(list(S, 'activities'), a => a.type === 'meeting'))} reuniones`},
      {title: 'Oportunidad y resultado', goal: 'Seguir el negocio hasta ganarlo o cerrarlo.', actors: ['Ejecutivo', 'Jefatura'], actions: ['set_opportunity'], entities: ['opportunities'], rule: 'Etapas: nuevo, calificada, propuesta, negociación, ganado o perdido. El contacto debe pertenecer a la empresa.', section: 'resultados', live: S => `${fmt(count(list(S, 'opportunities'), o => !['ganado', 'perdido'].includes(o.status)))} oportunidades abiertas`},
      {title: 'Conciliación con POST', goal: 'Intercambiar gestiones con el sistema POST de Vertia.', actors: ['Jefatura', 'Regional'], actions: ['sync_post'], entities: ['activities'], adapter: 'POST simulado', rule: 'Valida registros y errores. En producción depende de una API documentada o, si no existe, de intercambio de archivos validado.', section: 'integraciones', live: S => `${fmt(count(list(S, 'activities'), a => a.type === 'sync'))} conciliaciones`},
    ],
    funnel: {
      title: 'Embudo comercial en su vista',
      rows: S => {
        const c = list(S, 'contacts');
        return [
          ['Contactos en cartera', c.length],
          ['Contactados', count(c, x => ['contactado', 'respondió', 'reunión'].includes(x.status))],
          ['Respondieron', count(c, x => ['respondió', 'reunión'].includes(x.status))],
          ['Con reunión', count(c, x => x.status === 'reunión')],
          ['Oportunidades abiertas', count(list(S, 'opportunities'), o => !['ganado', 'perdido'].includes(o.status))],
        ];
      },
    },
  },
  contratos: {
    intro: 'Desde la solicitud hasta las obligaciones: cada transición se valida en el servidor según perfil y estado, queda en el historial del contrato y en la auditoría.',
    stages: [
      {title: 'Alta del contrato', goal: 'Registrar el contrato con su país, partes y vigencia.', actors: ['Ejecutivo', 'Legal', 'Jefatura'], actions: ['create_contract'], entities: ['contracts'], rule: 'Se crea en borrador con referencia VRT-país, versión e historial. Es confidencial por defecto.', section: 'repositorio', live: S => `${fmt(count(list(S, 'contracts'), c => c.status === 'borrador'))} en borrador`},
      {title: 'Documento y versiones', goal: 'Adjuntar el documento y conservar cada versión.', actors: ['Propietario', 'Legal'], actions: ['upload_document'], entities: ['documents'], rule: 'Solo en borrador, rechazo o renovación. Cada carga sube la versión e invalida el análisis y la copia saneada anteriores.', section: 'repositorio', live: S => `${fmt(list(S, 'contracts').reduce((n, c) => n + (c.documents?.length || 0), 0))} documentos registrados`},
      {title: 'Lectura y verificación', goal: 'Leer el archivo y proponer campos con evidencia y página.', actors: ['Propietario', 'Legal'], actions: ['uploads', 'review_extraction', 'analyze_contract'], entities: ['analysis'], adapter: 'Texto PDF real; imágenes con escaneo simulado por nombre de archivo; Claude desconectado', rule: 'Los campos requieren confirmación humana. Los expedientes de ejemplo conservan análisis sintético identificado; la carga real nunca recibe hallazgos inventados.', section: 'repositorio', live: S => `${fmt(count(list(S, 'contracts'), c => c.analysis))} expedientes con lectura o análisis`},
      {title: 'Copia saneada', goal: 'Compartir entre países sin exponer datos sensibles.', actors: ['Legal', 'Jefatura', 'Regional'], actions: ['redact_document'], entities: ['redaction'], rule: 'La copia se reconstruye con una lista de campos permitidos: monto, contraparte, cuentas e identificadores fiscales no se incluyen.', section: 'repositorio', live: S => `${fmt(count(list(S, 'contracts'), c => c.redacted_ready))} copias saneadas`},
      {title: 'Envío a revisión', goal: 'Pasar el contrato a la cola de revisión.', actors: ['Propietario'], actions: ['submit_review'], entities: ['contracts', 'history'], rule: 'Exige al menos un documento. Un contrato rechazado puede corregirse y reenviarse.', section: 'trabajo', live: S => `${fmt(count(list(S, 'contracts'), c => ['en_revision', 'pendiente_aprobacion'].includes(c.status)))} en revisión`},
      {title: 'Aprobación o rechazo', goal: 'Decisión registrada con responsable y motivo.', actors: ['Jefatura', 'Legal', 'Regional'], actions: ['approve_contract', 'reject_contract'], entities: ['contracts', 'history'], rule: 'Solo jefatura, Legal o regional deciden. El rechazo exige motivo y devuelve el contrato para corrección.', section: 'trabajo', live: S => `${fmt(count(list(S, 'contracts'), c => c.status === 'aprobado'))} aprobados · ${fmt(count(list(S, 'contracts'), c => c.status === 'rechazado'))} rechazados`},
      {title: 'Firma', goal: 'Enviar a firma y registrar el resultado.', actors: ['Jefatura', 'Legal', 'Regional'], actions: ['send_signature', 'sign_contract'], entities: ['signature', 'history'], adapter: 'Firma electrónica simulada', rule: 'Aprobado, luego por firmar, luego firmado. En la demostración la firma no tiene efecto legal.', section: 'trabajo', live: S => `${fmt(count(list(S, 'contracts'), c => c.status === 'pendiente_firma'))} por firmar`},
      {title: 'Activación', goal: 'El contrato firmado pasa a vigente.', actors: ['Jefatura', 'Legal', 'Regional'], actions: ['activate_contract'], entities: ['contracts', 'history'], rule: 'Solo desde firmado. Desde aquí corren alertas y obligaciones.', section: 'repositorio', live: S => `${fmt(count(list(S, 'contracts'), c => c.status === 'activo'))} activos`},
      {title: 'Obligaciones y evidencia', goal: 'Cumplir compromisos con responsable, plazo y evidencia.', actors: ['Propietario', 'Legal'], actions: ['add_obligation', 'complete_obligation'], entities: ['obligations'], rule: 'Cada obligación tiene vencimiento y responsable. Completarla exige evidencia y registra quién y cuándo.', section: 'obligaciones', live: S => `${fmt(count(list(S, 'obligations'), o => o.status !== 'completada'))} pendientes · ${fmt(S?.metrics?.overdue_obligations)} atrasadas`},
      {title: 'Enmiendas y renovación', goal: 'Mantener el contrato al día durante su vigencia.', actors: ['Propietario', 'Legal'], actions: ['add_amendment', 'renew_contract'], entities: ['amendments', 'history'], rule: 'Enmiendas solo sobre contratos firmados o activos. La renovación extiende el vencimiento y vuelve a revisión.', section: 'repositorio', live: S => `${fmt(count(list(S, 'contracts'), c => c.status === 'en_renovacion'))} en renovación`},
    ],
    lateral: {title: 'Acceso entre países', text: 'Un perfil de otro país ve solo la referencia del contrato. Solicita acceso con motivo; el responsable del país o regional lo concede por 1 a 30 días, solo lectura.', actions: ['request_access', 'grant_access'], entities: ['access_requests'], section: 'accesos'},
    funnel: {
      title: 'Contratos por estado en su vista',
      rows: S => {
        const c = list(S, 'contracts').filter(x => !x.restricted);
        return [
          ['Borrador', count(c, x => x.status === 'borrador')],
          ['En revisión', count(c, x => ['en_revision', 'pendiente_aprobacion'].includes(x.status))],
          ['Aprobado', count(c, x => x.status === 'aprobado')],
          ['Por firmar', count(c, x => x.status === 'pendiente_firma')],
          ['Firmado', count(c, x => x.status === 'firmado')],
          ['Activo', count(c, x => x.status === 'activo')],
          ['En renovación', count(c, x => x.status === 'en_renovacion')],
          ['Rechazado', count(c, x => x.status === 'rechazado')],
        ];
      },
    },
  },
};

// Campos: [nombre, tipo, marca]. Marca: 'pk' clave, 'fk:<entidad>' referencia.
const COMMON = [['country', 'código país', 'fk:countries'], ['owner_id', 'perfil propietario', 'fk:users'], ['created_at', 'fecha ISO']];
const MODEL = {
  prospectador: {
    entities: [
      {id: 'users', name: 'Perfil de demostración', note: 'Seis perfiles sintéticos. No es SSO.', fields: [['id', 'texto', 'pk'], ['name', 'texto'], ['role', 'regional · manager · executive · legal · viewer'], ['country', 'código país', 'fk:countries']], live: S => list(S, 'users').length},
      {id: 'countries', name: 'País', note: 'Configuración base de cinco países.', fields: [['code', 'CL · UY · PE · AR · MX', 'pk'], ['name', 'texto'], ['currency', 'moneda']], live: S => list(S, 'countries').length},
      {id: 'companies', name: 'Empresa', fields: [['id', 'texto', 'pk'], ['name', 'texto'], ['domain', 'dominio .example'], ['sector', 'texto'], ['status', 'estado'], ...COMMON]},
      {id: 'contacts', name: 'Contacto', fields: [['id', 'texto', 'pk'], ['company_id', 'empresa', 'fk:companies'], ['name', 'texto'], ['email', 'único, .example'], ['title', 'cargo'], ['status', 'nuevo · contactado · respondió · reunión · no_contactar'], ['excluded', 'sí / no'], ['score', '0 a 100'], ['source', 'origen'], ...COMMON]},
      {id: 'prospects', name: 'Prospecto', note: 'Correo oculto hasta revelar.', fields: [['id', 'texto', 'pk'], ['contact_id', 'contacto al revelar', 'fk:contacts'], ['name', 'texto'], ['company_name', 'texto'], ['revealed', 'sí / no'], ['credit_cost', '1 crédito'], ['score', 'afinidad'], ...COMMON]},
      {id: 'campaigns', name: 'Campaña', fields: [['id', 'texto', 'pk'], ['contact_ids[]', 'destinatarios', 'fk:contacts'], ['approved_by', 'perfil que aprueba', 'fk:users'], ['subject', 'texto'], ['body', 'texto'], ['status', 'borrador · aprobada · enviada'], ['approval_hash', 'huella del contenido aprobado'], ['sent_count / skipped_count', 'números'], ...COMMON]},
      {id: 'messages', name: 'Mensaje', note: 'Solo se crea por acciones; nunca es un correo real.', fields: [['id', 'texto', 'pk'], ['contact_id', 'contacto', 'fk:contacts'], ['campaign_id', 'campaña', 'fk:campaigns'], ['direction', 'saliente · entrante'], ['followup_status', 'programado · cancelado'], ['provider', 'Microsoft 365 simulado'], ...COMMON]},
      {id: 'activities', name: 'Actividad', fields: [['id', 'texto', 'pk'], ['contact_id', 'contacto (opcional)', 'fk:contacts'], ['type', 'reunión · importación · conciliación'], ['date', 'fecha'], ['status', 'estado'], ...COMMON]},
      {id: 'opportunities', name: 'Oportunidad', fields: [['id', 'texto', 'pk'], ['company_id', 'empresa', 'fk:companies'], ['contact_id', 'contacto', 'fk:contacts'], ['amount', 'monto'], ['currency', 'moneda'], ['status', 'nuevo · calificada · propuesta · negociación · ganado · perdido'], ...COMMON]},
      {id: 'notifications', name: 'Notificación', fields: [['id', 'texto', 'pk'], ['contact_id', 'contacto', 'fk:contacts'], ['title', 'texto'], ['status', 'estado'], ...COMMON]},
      {id: 'audit', name: 'Auditoría', note: 'Bitácora de demostración; no es un registro inmutable (WORM).', fields: [['id', 'texto', 'pk'], ['actor', 'perfil que actúa', 'fk:users'], ['action', 'acción ejecutada'], ['entity_id', 'cualquier entidad'], ['detail', 'texto'], ...COMMON]},
    ],
    relations: [
      ['companies', '1 : N', 'contacts', 'Una empresa agrupa a sus contactos (company_id).'],
      ['prospects', '1 : 0..1', 'contacts', 'Al revelar, el prospecto se vincula al contacto creado o existente (contact_id).'],
      ['campaigns', 'N : N', 'contacts', 'Una campaña tiene de 1 a 200 destinatarios (contact_ids).'],
      ['campaigns', '1 : N', 'messages', 'El envío crea un mensaje por destinatario (campaign_id).'],
      ['contacts', '1 : N', 'messages', 'Mensajes salientes y respuestas del contacto (contact_id).'],
      ['contacts', '1 : N', 'activities', 'Reuniones agendadas con el contacto (contact_id).'],
      ['companies', '1 : N', 'opportunities', 'Oportunidades de negocio por empresa (company_id).'],
      ['users', '1 : N', 'companies', 'La cartera: cada registro pertenece a un perfil (owner_id).'],
      ['audit', 'N : 1', 'users', 'Cada acción registra quién la ejecutó (actor).'],
    ],
  },
  contratos: {
    entities: [
      {id: 'users', name: 'Perfil de demostración', note: 'Seis perfiles sintéticos. No es SSO.', fields: [['id', 'texto', 'pk'], ['name', 'texto'], ['role', 'regional · manager · executive · legal · viewer'], ['country', 'código país', 'fk:countries']], live: S => list(S, 'users').length},
      {id: 'countries', name: 'País', note: 'Configuración base de cinco países.', fields: [['code', 'CL · UY · PE · AR · MX', 'pk'], ['name', 'texto'], ['currency', 'moneda']], live: S => list(S, 'countries').length},
      {id: 'contracts', name: 'Contrato', note: 'Los contratos de otro país sin acceso solo muestran su referencia.', fields: [['id', 'texto', 'pk'], ['reference', 'VRT-país-código'], ['title', 'texto'], ['type', 'categoría'], ['company / counterparty', 'partes'], ['amount', 'monto'], ['currency', 'moneda'], ['confidential', 'sí / no'], ['status', 'borrador → en revisión → aprobado → por firmar → firmado → activo'], ['start_date / end_date', 'vigencia'], ['version', 'número'], ...COMMON], live: S => count(list(S, 'contracts'), c => !c.restricted)},
      {id: 'documents', name: 'Documento', embedded: true, note: 'Dentro del contrato.', fields: [['id', 'texto', 'pk'], ['contract', 'contrato contenedor', 'fk:contracts'], ['filename', 'nombre de archivo'], ['kind', 'tipo'], ['version', 'número'], ['synthetic', 'catálogo inicial: sí; archivo cargado: no']], live: S => list(S, 'contracts').reduce((n, c) => n + (c.documents?.length || 0), 0)},
      {id: 'history', name: 'Historial', embedded: true, note: 'Dentro del contrato.', fields: [['contract', 'contrato contenedor', 'fk:contracts'], ['status', 'estado alcanzado'], ['at', 'fecha'], ['by', 'perfil', 'fk:users'], ['note', 'motivo']], live: S => list(S, 'contracts').reduce((n, c) => n + (c.history?.length || 0), 0)},
      {id: 'uploads', name: 'Archivo y lectura real', note: 'Tabla vertia_document_uploads; binarios y previews en almacenamiento privado.', fields: [['id', 'identificador', 'pk'], ['contract_id', 'contrato', 'fk:contracts'], ['filename / content_type', 'archivo y formato'], ['page_count', 'páginas procesadas'], ['pages[]', 'texto, método de lectura y evidencia'], ['proposed_fields[]', 'valores pendientes de confirmación'], ['review_status', 'revisión humana']], live: S => list(S, 'contracts').reduce((n,c)=>n+(c.documents||[]).filter(d=>d.synthetic===false).length,0)},
      {id: 'analysis', name: 'Lectura y análisis', embedded: true, note: 'Texto PDF real y escaneo de imágenes simulado por nombre de archivo, con revisión humana; los análisis de ejemplo son sintéticos. Claude API no conectado.', fields: [['contract', 'contrato contenedor', 'fk:contracts'], ['summary', 'resultado de lectura'], ['mode', 'local_extraction o demostración'], ['risk_level / score', 'sin evaluar en lectura local'], ['proposed_fields[]', 'valor, evidencia, página y revisión'], ['source_version', 'versión del documento']], live: S => count(list(S, 'contracts'), c => c.analysis)},
      {id: 'redaction', name: 'Copia saneada', embedded: true, note: 'Reconstruida con lista de campos permitidos.', fields: [['contract', 'contrato contenedor', 'fk:contracts'], ['reviewed_by', 'perfil', 'fk:users'], ['source_version', 'versión'], ['removed_fields', 'campos excluidos']], live: S => count(list(S, 'contracts'), c => c.redacted_ready)},
      {id: 'signature', name: 'Firma', embedded: true, note: 'Simulada: legal_signature siempre falso.', fields: [['contract', 'contrato contenedor', 'fk:contracts'], ['provider', 'proveedor simulado'], ['status', 'enviado · firmado (simulado)'], ['legal_signature', 'no'], ['by', 'perfil', 'fk:users']], live: S => count(list(S, 'contracts'), c => c.signature)},
      {id: 'amendments', name: 'Enmienda', embedded: true, note: 'Dentro del contrato.', fields: [['id', 'texto', 'pk'], ['contract', 'contrato contenedor', 'fk:contracts'], ['title', 'texto'], ['description', 'texto'], ['by', 'perfil', 'fk:users']], live: S => list(S, 'contracts').reduce((n, c) => n + (c.amendments?.length || 0), 0)},
      {id: 'obligations', name: 'Obligación', fields: [['id', 'texto', 'pk'], ['contract_id', 'contrato', 'fk:contracts'], ['title', 'texto'], ['due_date', 'vencimiento'], ['owner', 'responsable'], ['status', 'pendiente · completada'], ['evidence', 'evidencia de cumplimiento'], ['completed_by', 'perfil', 'fk:users'], ...COMMON]},
      {id: 'access_requests', name: 'Solicitud de acceso', fields: [['id', 'texto', 'pk'], ['contract_id', 'contrato', 'fk:contracts'], ['requested_by', 'solicitante', 'fk:users'], ['granted_by', 'quien autoriza', 'fk:users'], ['reason', 'motivo'], ['status', 'pendiente · aprobada'], ['days / expires_at', '1 a 30 días, solo lectura'], ...COMMON]},
      {id: 'audit', name: 'Auditoría', note: 'Bitácora de demostración; no es un registro inmutable (WORM).', fields: [['id', 'texto', 'pk'], ['actor', 'perfil que actúa', 'fk:users'], ['action', 'acción ejecutada'], ['entity_id', 'cualquier entidad'], ['detail', 'texto'], ...COMMON]},
    ],
    relations: [
      ['contracts', '1 : N', 'documents', 'Cada carga agrega una versión del documento.'],
      ['contracts', '1 : N', 'uploads', 'Cada archivo real conserva su lectura por página y revisión.'],
      ['contracts', '1 : N', 'history', 'Cada transición de estado queda con fecha, perfil y motivo.'],
      ['contracts', '1 : 0..1', 'analysis', 'Último análisis, ligado a la versión del documento.'],
      ['contracts', '1 : 0..1', 'redaction', 'Copia saneada vigente para compartir entre países.'],
      ['contracts', '1 : 0..1', 'signature', 'Estado de la firma simulada.'],
      ['contracts', '1 : N', 'amendments', 'Enmiendas sobre contratos firmados o activos.'],
      ['contracts', '1 : N', 'obligations', 'Compromisos con responsable y plazo (contract_id).'],
      ['contracts', '1 : N', 'access_requests', 'Solicitudes de acceso desde otros países (contract_id).'],
      ['users', '1 : N', 'access_requests', 'Quién solicita y quién autoriza (requested_by, granted_by).'],
      ['audit', 'N : 1', 'users', 'Cada acción registra quién la ejecutó (actor).'],
    ],
  },
};

const ENTITY_NAME = app => Object.fromEntries(MODEL[app].entities.map(e => [e.id, e.name]));

function FlowView({app, S, go, onEntity}) {
  const flow = FLOWS[app];
  const names = ENTITY_NAME(app);
  const rows = flow.funnel.rows(S);
  const max = Math.max(1, ...rows.map(r => r[1]));
  return <>
    <div className="fx-layout">
      <ol className="fx-steps">
        {flow.stages.map((st, i) => <li className="fx-step" key={st.title}>
          <div className="fx-step-marker"><span>{String(i + 1).padStart(2, '0')}</span></div>
          <article className="fx-step-card">
            <header>
              <div>
                <h3>{st.title}</h3>
                <p>{st.goal}</p>
              </div>
              {st.adapter && <span className="fx-tag fx-tag-sim">{st.adapter}</span>}
            </header>
            <dl className="fx-grid">
              <div><dt><Users size={15}/> Quién</dt><dd>{st.actors.map(a => <span className="fx-chip" key={a}>{a}</span>)}</dd></div>
              <div><dt><Workflow size={15}/> Acción del sistema</dt><dd>{st.actions.map(a => <code key={a}>{a}</code>)}</dd></div>
              <div><dt><Database size={15}/> Registra</dt><dd>{st.entities.map(e => <button type="button" className="fx-chip fx-chip-link" key={e} onClick={() => onEntity(e)} title="Ver en el modelo de datos">{names[e] || e}</button>)}</dd></div>
            </dl>
            <p className="fx-rule"><ShieldCheck size={16}/> <span>{st.rule}</span></p>
            <footer>
              <span className="fx-live">{st.live(S)}</span>
              <button type="button" className="fx-go" onClick={() => go(st.section)}>Abrir en la demo <ArrowRight size={16}/></button>
            </footer>
          </article>
        </li>)}
      </ol>
      <aside className="fx-side">
        <section className="fx-box">
          <h3>{flow.funnel.title}</h3>
          <p>Calculado en vivo con los registros que su perfil puede ver.</p>
          <div className="fx-funnel">
            {rows.map(([name, value]) => <div key={name}>
              <div className="fx-funnel-label"><span>{name}</span><b>{fmt(value)}</b></div>
              <div className="fx-bar"><i style={{width: `${Math.max(value ? 4 : 0, value / max * 100)}%`}}/></div>
            </div>)}
          </div>
        </section>
        {flow.lateral && <section className="fx-box">
          <h3><KeyRound size={17}/> {flow.lateral.title}</h3>
          <p>{flow.lateral.text}</p>
          <div className="fx-inline">{flow.lateral.actions.map(a => <code key={a}>{a}</code>)}</div>
          <button type="button" className="fx-go" onClick={() => go(flow.lateral.section)}>Abrir accesos regionales <ArrowRight size={16}/></button>
        </section>}
        <section className="fx-box">
          <h3><History size={17}/> Transversal a todo el flujo</h3>
          <ul className="fx-list">
            <li>Cada acción valida el perfil y el país en el servidor, no solo en pantalla.</li>
            <li>Cada cambio se guarda en PostgreSQL y crea un registro de auditoría con actor, acción y entidad.</li>
            <li>Los servicios externos marcados como simulados no se conectan ni consumen créditos reales.</li>
          </ul>
          <button type="button" className="fx-go" onClick={() => go(app === 'contratos' ? 'auditoria' : 'integraciones')}>{app === 'contratos' ? 'Ver auditoría' : 'Ver integraciones'} <ArrowRight size={16}/></button>
        </section>
      </aside>
    </div>
  </>;
}

function ModelView({app, S, focus, setFocus}) {
  const model = MODEL[app];
  const names = ENTITY_NAME(app);
  const related = useMemo(() => {
    if (!focus) return new Set();
    const set = new Set([focus]);
    model.relations.forEach(([a, , b]) => { if (a === focus) set.add(b); if (b === focus) set.add(a); });
    model.entities.forEach(e => e.fields.forEach(f => { const ref = f[2]?.startsWith('fk:') && f[2].slice(3); if (e.id === focus && ref) set.add(ref); if (ref === focus) set.add(e.id); }));
    return set;
  }, [focus, app]);
  const liveCount = e => (e.live ? e.live(S) : list(S, e.id).length);
  return <>
    <div className="fx-callout">
      <Info size={20}/>
      <div>
        <b>Modelo de datos de la demostración.</b>
        <p>El catálogo inicial es sintético y se guarda en PostgreSQL real: <code>vertia_demo_records</code> contiene las entidades en JSONB. Las cargas reales tienen su tabla <code>vertia_document_uploads</code>, con páginas, extracción y revisión; los archivos y las vistas previas se almacenan en un área privada. Historial, firma y enmiendas se vinculan al expediente. El diagrama muestra el modelo lógico; las claves foráneas, índices y reglas productivas se definen en el levantamiento con Vertia.</p>
      </div>
    </div>
    <p className="fx-hint">Seleccione una entidad para resaltar sus relaciones.{focus && <button type="button" onClick={() => setFocus(null)}>Quitar selección</button>}</p>
    <div className="fx-entities">
      {model.entities.map(e => <article key={e.id} id={`fx-entity-${e.id}`} className={`fx-entity ${focus === e.id ? 'is-focus' : ''} ${focus && !related.has(e.id) ? 'is-dim' : ''} ${focus && related.has(e.id) && focus !== e.id ? 'is-related' : ''}`} onClick={() => setFocus(focus === e.id ? null : e.id)} tabIndex={0} onKeyDown={ev => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); setFocus(focus === e.id ? null : e.id); } }} aria-pressed={focus === e.id}>
        <header>
          <div>
            <h3>{e.name}</h3>
            <small>{e.embedded ? `contracts.${e.id}` : e.id}</small>
          </div>
          <span className="fx-count" title="Registros visibles para su perfil">{fmt(liveCount(e))}</span>
        </header>
        {e.note && <p className="fx-note">{e.note}</p>}
        <ul className="fx-fields">
          {e.fields.map(([f, t, mark]) => <li key={f}>
            <span className="fx-field-name">{mark === 'pk' && <em className="fx-key">PK</em>}{mark?.startsWith('fk:') && <em className="fx-key fx-fk" title={`Referencia a ${names[mark.slice(3)]}`}>FK</em>}{f}</span>
            <span className="fx-field-type">{mark?.startsWith('fk:') ? `→ ${names[mark.slice(3)]}` : t}</span>
          </li>)}
        </ul>
      </article>)}
    </div>
    <section className="fx-box fx-relations">
      <h3><Link2 size={17}/> Relaciones</h3>
      <div className="fx-table-wrap">
        <table>
          <thead><tr><th>Entidad</th><th>Cardinalidad</th><th>Entidad</th><th>Significado</th></tr></thead>
          <tbody>{model.relations.map(([a, card, b, text]) => <tr key={a + b + card} className={focus && (a === focus || b === focus) ? 'is-focus' : ''}>
            <td><button type="button" onClick={() => setFocus(a)}>{names[a]}</button></td>
            <td><span className="fx-card">{card}</span></td>
            <td><button type="button" onClick={() => setFocus(b)}>{names[b]}</button></td>
            <td>{text}</td>
          </tr>)}</tbody>
        </table>
      </div>
    </section>
  </>;
}

export function FlowModel({app, S, go}) {
  const [tab, setTab] = useState('flujo');
  const [focus, setFocus] = useState(null);
  const showEntity = id => {
    setFocus(id);
    setTab('modelo');
    setTimeout(() => document.getElementById(`fx-entity-${id}`)?.scrollIntoView({behavior: 'smooth', block: 'center'}), 60);
  };
  return <div className="fx">
    <div className="section-heading">
      <div>
        <span className="eyebrow">PROCESO DE PUNTA A PUNTA</span>
        <h1>Flujo completo y modelo de datos.</h1>
        <p>{FLOWS[app].intro}</p>
      </div>
    </div>
    <div className="fx-tabs" role="tablist">
      <button role="tab" aria-selected={tab === 'flujo'} className={tab === 'flujo' ? 'active' : ''} onClick={() => setTab('flujo')}><Workflow size={18}/> Flujo completo <span>{FLOWS[app].stages.length} etapas</span></button>
      <button role="tab" aria-selected={tab === 'modelo'} className={tab === 'modelo' ? 'active' : ''} onClick={() => setTab('modelo')}><Database size={18}/> Modelo de datos demostrado <span>{MODEL[app].entities.length} entidades</span></button>
    </div>
    {tab === 'flujo' ? <FlowView app={app} S={S} go={go} onEntity={showEntity}/> : <ModelView app={app} S={S} focus={focus} setFocus={setFocus}/>}
    <p className="fx-foot"><PlugZap size={16}/> Datos sintéticos. Los PDF cargados se leen de verdad; las imágenes usan un escaneo simulado por nombre de archivo. IA externa, firma, correo, calendario y proveedores de prospectos permanecen simulados.</p>
  </div>;
}
