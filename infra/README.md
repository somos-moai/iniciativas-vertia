# Despliegue y operación de las demostraciones

Estas instrucciones corresponden exclusivamente a las dos aplicaciones con datos sintéticos. No describen la producción del cliente ni autorizan cambios en otros servicios del VPS.

La siguiente iteración incorpora carga y lectura real de PDF e imágenes. Antes de publicar esa versión se debe activar el acceso HTTP privado descrito abajo. Las cuentas y documentos precargados continúan siendo sintéticos.

## Entorno verificado

- VPS autorizado `217.196.62.58`, acceso SSH existente y host key verificada.
- Proyecto `/home/moai/iniciativas-vertia` y usuario de ejecución `moai`.
- Python 3.10 y PostgreSQL 16 del servidor, entorno `.venv` exclusivo.
- Base y rol exclusivos `vertia_demo`; credencial generada remotamente y guardada en `.env` con permiso `0600`.
- Backend más frontend compilado en un worker sobre `127.0.0.1:8788`.
- Dominio de demostración `iniciativasvertia.somosmoai.tech`.

## Preparación inicial

`prepare-demo-server.py` se ejecuta remotamente como root una sola vez. Conserva los recursos existentes si encuentra el entorno privado. Si hay conflicto de nombres sin entorno asociado, se detiene; no cambia contraseñas de recursos existentes.

Instalar `paramiko` en el runtime de despliegue local si no está disponible. La clave SSH permanece en su ubicación habitual y no se almacena en el proyecto. La conexión rechaza hosts desconocidos. No deshabilitar esa comprobación.

## Validación y publicación

1. Compilar el frontend localmente y comprobar que `frontend/dist/index.html` existe.
2. Revisar que todos los datos sean sintéticos y las integraciones externas estén identificadas como simuladas.
3. Ejecutar `python infra/deploy-demo.py`: transfiere backend, frontend compilado y entregables; instala dependencias y ejecuta las pruebas reales PostgreSQL en esquemas temporales exclusivos.
4. Para la versión con uploads, preparar primero el acceso privado y ejecutar `python infra/deploy-demo.py --publish --private`. El script comprueba nginx, activa la protección antes de iniciar esa versión y conserva el certificado existente. La opción `--tls` se utiliza solo cuando deba emitirse el certificado inicial del dominio verificado.
5. Validar la salud en `/api/health`, `/prospectador` y `/contratos`, iniciar sesión en perfiles de demostración y comprobar una modificación persistida por aplicación.
6. Registrar commit, fecha, versión, resultado de pruebas y enlaces en `docs/coordination/infra-discovery.md`.

El directorio `deliverables/` contiene los documentos finales; `PROPOSALS_DIR` apunta allí. La aplicación publica solamente extensiones HTML, PDF y DOCX. Nunca apuntar esta variable a la carpeta de trabajo completa ni incorporar credenciales a los entregables.

## Comprobaciones operativas

Desde el VPS, estos comandos no muestran credenciales:

```sh
systemctl is-active iniciativas-vertia
systemctl status iniciativas-vertia --no-pager
journalctl -u iniciativas-vertia -n 50 --no-pager
curl --fail --silent http://127.0.0.1:8788/api/health
nginx -t
certbot certificates
```

El servicio se reinicia ante fallas y tiene límites de memoria y CPU para reducir impacto sobre los demás proyectos. La demostración no promete SLA de producción. Los archivos privados y las variables del proceso no deben imprimirse al diagnosticar.

## Actualización y recuperación

Actualizar únicamente desde una revisión probada. Conservar el commit anterior y una copia de seguridad consistente de **la base exclusiva y `UPLOAD_DIR`** antes de cambios de esquema. Los originales se almacenan fuera de PostgreSQL; respaldar solo la base deja sus referencias incompletas. Coordinar una pausa de escritura para capturar ambos componentes y registrar fecha, versión y comprobación de integridad. Guardar los respaldos fuera de la raíz web, con permisos restrictivos y sin incluir `.env` en el repositorio.

Si una actualización falla, detener únicamente `iniciativas-vertia.service`, restaurar los archivos de la revisión anterior y, si cambió el esquema, restaurar solo `vertia_demo` junto con el directorio de uploads correspondiente al mismo respaldo aprobado. Verificar los hashes de originales contra los metadatos, reiniciar ese servicio y validar salud y rutas. No reiniciar PostgreSQL, Docker ni los servicios de otros clientes para recuperar esta demo.

La configuración nginx existente se preserva en despliegues posteriores para conservar TLS. Los cambios de proxy se revisan y se validan con `nginx -t` antes de recargar. Retirar una demostración requiere deshabilitar solamente su servicio y su sitio; eliminar base, rol o archivos exige una decisión explícita posterior.

## Límites de seguridad de esta entrega

La selección de perfiles es parte visible de la demostración; no constituye autenticación productiva ni SSO. Utilizar documentos de prueba controlados. Los envíos de correo, búsquedas comerciales, firma y análisis de IA externa se simulan. La carga, extracción y OCR reales solo se habilitan junto con el acceso privado. La infraestructura productiva deberá incorporar los controles y pruebas de aceptación definidos en los documentos de alcance, mantenimiento y requisitos de Vertia.

## Preparación para lectura documental real

`prepare-ocr-server.py` instala únicamente Tesseract y sus lenguajes español e inglés, más pypdf, pypdfium2, Pillow y python-multipart en el entorno exclusivo. No utiliza servicios ni claves de IA externas y no reinicia aplicaciones. El directorio `/home/moai/iniciativas-vertia/uploads` tiene modo `0700`, propietario `moai`; `UPLOAD_DIR` se guarda sin revelar el resto del entorno privado.

Los límites funcionales son 15 MB por archivo y 40 páginas PDF, un proceso de lectura a la vez y tiempo máximo de procesamiento de 90 segundos. nginx acepta 16 MB para cubrir el contenedor multipart y espera hasta 120 segundos. Los archivos no se publican como estáticos. El backend aplica permisos para consultar originales y resultados.

## Acceso privado para la versión con uploads

`prepare-private-access.py` genera remotamente una credencial aleatoria de 20 caracteres y un archivo htpasswd con propietario root, grupo www-data y modo `0640`. No imprime la clave ni activa nginx. El coordinador recibe la credencial en un archivo local fuera del repositorio; las pruebas la leen en memoria.

Publicar esa versión mediante `python infra/deploy-demo.py --publish --private`. Después de aprobar las pruebas, el script protege primero el sitio actual y recién entonces inicia el backend que acepta uploads. No sobrescribe otra configuración de autenticación existente. TLS permanece activo.

Validar que una solicitud anónima a la portada, ambas aplicaciones, API, assets y propuestas reciba `401`, y que las mismas rutas con credencial reciban su respuesta esperada. Verificar además carga de PDF de texto y OCR de una imagen de prueba, límites, permisos y ausencia de acceso estático al directorio privado.

Esta protección HTTP restringe el acceso a la demostración completa; la selección de perfiles sigue siendo una herramienta de demostración y no un SSO productivo. Utilizar documentos de prueba controlados. La lectura y OCR serán reales; correo, proveedores comerciales, firma e IA externa continúan simulados mientras no se autorice y valide su conexión.
