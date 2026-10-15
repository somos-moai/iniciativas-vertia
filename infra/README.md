# Despliegue y operación de las demostraciones

Estas instrucciones corresponden exclusivamente a las dos aplicaciones con datos sintéticos. No describen la producción del cliente ni autorizan cambios en otros servicios del VPS.

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
4. Si las pruebas pasan, ejecutar `python infra/deploy-demo.py --publish --tls`. El script crea únicamente el servicio y sitio propios, comprueba nginx antes de recargar y solicita el certificado del dominio ya verificado.
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

Actualizar únicamente desde una revisión probada. Conservar el commit anterior y una copia de seguridad de la base exclusiva antes de cambios de esquema. Los dumps contienen información sintética; aun así se almacenan fuera de la raíz web, con permisos restrictivos y sin incluir `.env` en el repositorio.

Si una actualización falla, detener únicamente `iniciativas-vertia.service`, restaurar los archivos de la revisión anterior y, si cambió el esquema, restaurar solo `vertia_demo` desde su respaldo aprobado. Reiniciar ese servicio y validar salud y rutas. No reiniciar PostgreSQL, Docker ni los servicios de otros clientes para recuperar esta demo.

La configuración nginx existente se preserva en despliegues posteriores para conservar TLS. Los cambios de proxy se revisan y se validan con `nginx -t` antes de recargar. Retirar una demostración requiere deshabilitar solamente su servicio y su sitio; eliminar base, rol o archivos exige una decisión explícita posterior.

## Límites de seguridad de esta entrega

La selección de perfiles es parte visible de la demostración; no constituye autenticación productiva ni SSO. No ingresar documentos, datos de contacto ni contratos reales. Los envíos de correo, búsquedas comerciales, OCR, firma y análisis de IA se simulan. La infraestructura productiva deberá incorporar los controles y pruebas de aceptación definidos en los documentos de alcance, mantenimiento y requisitos de Vertia.
