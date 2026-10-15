# Infraestructura de demostración

Verificación realizada el 15 de octubre de 2026. Fuente de conexión autorizada por el usuario: carpeta local `MOAI/Conexion VPS`. No se utilizará el servidor Geoinsumos indicado anteriormente.

## Servidor y aislamiento

- Host autorizado: `217.196.62.58`, nombre `srv1498889`.
- Acceso verificado mediante clave SSH existente con usuario `root`. No fue necesario usar ni revelar contraseñas.
- Ubuntu 22.04, Node 20.20.2, Python 3.10.12, PostgreSQL 16.13, Docker 29.1.3 y nginx disponibles.
- Existen numerosos sitios y servicios activos. Se preservan sus configuraciones, bases y procesos.
- Memoria: 7,8 GiB totales y aproximadamente 2,4 GiB disponibles al verificar; swap con uso significativo. Disco: aproximadamente 25 GiB disponibles. Usar un proceso de aplicación y servir el frontend compilado; evitar compilar dos stacks en el servidor o iniciar una instancia PostgreSQL adicional.
- Puerto candidato verificado libre: `127.0.0.1:8788`. Debe comprobarse nuevamente antes de publicar.
- Dominio de demostración: `iniciativasvertia.somosmoai.tech`; DNS verificado hacia el host autorizado. Certbot disponible.
- Sitio de presentación existente: `presentacionvertiagroup.somosmoai.tech`, raíz `/var/www/presentaciones`. No se modifica.

## Recursos creados exclusivamente para este proyecto

- Directorio `/home/moai/iniciativas-vertia`.
- Entorno Python `/home/moai/iniciativas-vertia/.venv`.
- Base PostgreSQL `vertia_demo`, propietario y rol exclusivo `vertia_demo`, sin privilegios de superusuario ni creación de otras bases o roles.
- `.env` remoto privado con modo `0600`, propietario `moai`, credencial aleatoria generada en el servidor y `DATABASE_URL`. Ninguna credencial se incorpora al repositorio.
- Los datos funcionales serán exclusivamente sintéticos. Los adaptadores externos se mantienen simulados.

## Publicación prevista

`infra/deploy-demo.py` transfiere backend y frontend compilado, instala dependencias en el entorno exclusivo y ejecuta pruebas PostgreSQL con esquemas temporales propios. La opción `--publish` habilita únicamente `iniciativas-vertia.service` y un sitio nginx nuevo; `--tls` solicita el certificado del dominio de demostración. No instalar el sitio hasta que pasen pruebas y exista frontend compilado.

El servicio ejecuta un único worker en loopback, como usuario `moai`, con límite de memoria de 640 MB y CPU del 75%. nginx dirige ambas aplicaciones al mismo backend. El archivo `infra/prepare-demo-server.py` prepara solamente recursos nuevos y conserva un entorno existente; nunca reemplaza claves de otros sistemas.

## Runtime de documentos verificado

Bundle oficial instalado: `C:/Users/cueva/.cache/codex-runtimes/codex-primary-runtime/runtime.json`, versión `26.1013.11914`.

- Node autorizado: `dependencies/node/bin/node.exe` dentro de ese bundle.
- Python autorizado: `dependencies/python/python.exe`.
- Poppler: `dependencies/native/poppler/Library/bin/pdftoppm.exe`.
- El manifiesto declara `libreOfficeVersion: null`. No existe `soffice.exe` en ese bundle ni en las rutas habituales de Program Files verificadas. No afirmar que el render DOCX está validado sin resolver esa dependencia.

## Operación

Validar salud local, ambas rutas de aplicación, persistencia PostgreSQL y TLS antes de entregar enlaces. Registrar resultados de pruebas y publicación en este archivo. El VPS corresponde a demostración; la producción del cliente utilizará infraestructura y servicios externos provistos por Vertia según sus requisitos.

## Validación ejecutada

Backend y dependencias transferidos al directorio exclusivo. Suite real sobre PostgreSQL 16 del VPS: **10 pruebas aprobadas**, última ejecución de publicación en **1,64 segundos**, con un aviso de deprecación de Starlette/httpx que no afecta el resultado. La suite crea y elimina únicamente esquemas temporales `vertia_test_*`; no usa SQLite ni abre datos de otras bases.

## Publicación completada

Fecha: 15 de octubre de 2026. Servicio exclusivo `iniciativas-vertia` iniciado; nginx validado y recargado correctamente. Certificado emitido y instalado por Certbot para `iniciativasvertia.somosmoai.tech`, vencimiento **13 de enero de 2027**, renovación automática programada. Las advertencias OCSP de nginx corresponden a certificados existentes de otros sitios y no impidieron la validación.

Comprobaciones HTTPS desde un cliente externo:

| Ruta | Resultado |
|---|---|
| `/api/health` | 200; `status: ok`, `database: postgresql`, `mode: synthetic` |
| `/prospectador` | 200; HTML SPA |
| `/contratos` | 200; HTML SPA |
| `/propuestas/prospectador.html` | 200; 49.232 bytes |
| `/propuestas/prospectador.pdf` | 200; 312.885 bytes; hash coincide con el entregable local final |
| `/propuestas/contratos.html` | 200; 49.960 bytes |
| `/propuestas/contratos.pdf` | 200; 301.980 bytes; hash coincide con el entregable local final |
| Ambas propuestas DOCX | 200; hashes coinciden con los entregables locales finales |
| `/assets/index-_hFDWIZc.js` y `/assets/index-DXqJ0axk.css` | 200; hashes coinciden con la compilación local final |
| `/brand/global.webp` y `/brand/vertia.webp` | 200; tipo MIME explícito `image/webp` |

Propuestas públicas servidas desde `/home/moai/iniciativas-vertia/deliverables`; ajuste no secreto aplicado también a la variable privada remota para evitar conflicto con systemd. Frontend y entregables pertenecen al usuario de ejecución `moai`. QA visual y recorridos de navegador continúan bajo el coordinador.

## Acceso a agentes y repositorio

Consulta de estado sin extraer credenciales: CLI Claude disponible en `/usr/bin/claude`; archivos de autenticación Claude y Gemini presentes bajo root. Gemini y gh no aparecen en PATH. El SSH de root a GitHub no autentica; el usuario `moai` autentica mediante una deploy key identificada como `somos-moai/Ecosistema-MoAI`, perteneciente a otro repositorio. Esa clave no acredita permisos de escritura sobre `somos-moai/iniciativas-vertia` y no se reconfigura ni reutiliza como credencial general.
