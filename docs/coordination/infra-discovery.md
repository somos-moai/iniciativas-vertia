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

## Preparación de la iteración documental real

La infraestructura quedó preparada sin reiniciar el backend actual: Tesseract 4.1.1 con `spa`, `eng` y `osd`; pypdf 6.20.1, pypdfium2 5.14.0, Pillow 12.3.0 y python-multipart 0.0.32 en el entorno exclusivo. apt instaló 7 paquetes nuevos, 24,1 MB adicionales y cero actualizaciones. La memoria disponible antes de instalar era aproximadamente 2,5 GiB y el disco libre 25 GiB. Se usó `NEEDRESTART_MODE=l` para listar necesidades existentes sin reiniciar otros servicios.

Directorio de uploads privado preparado con modo `0700`, propietario `moai`, y variable `UPLOAD_DIR` remota; `.env` permanece en `0600`. nginx ajustado a 16 MB y 120 segundos. Credencial HTTP privada preparada remotamente y entregada únicamente mediante archivo local fuera del repositorio; no está en código, documentos públicos ni logs. Durante la preparación se mantuvo la autenticación inactiva; su activación final se registra abajo.

Validación previa al despliegue: código copiado a un staging aislado bajo `qa-staging`, sin reemplazar archivos de la aplicación pública ni reiniciar su servicio. **15 pruebas aprobadas en 5,17 segundos** sobre PostgreSQL 16 y Tesseract reales. Incluyen PDF, revisión humana, bytes originales, ACL, archivos vacíos/corruptos/fuera de límite, permisos entre países, invalidación de acceso con nueva versión, OCR de imagen e ICP con evidencia explícita. El cap final autorizado es de **40 páginas PDF**, 15 MB y 90 segundos de procesamiento, con concurrencia uno. La suite usa esquemas temporales propios y archivos de prueba en directorios temporales.

Última copia completa del backend congelado validada en staging: **15/15 pruebas aprobadas en 4,64 segundos**. Para QA de interfaz se habilitó temporalmente `iniciativas-vertia-uiqa.service` sobre `127.0.0.1:8790`, con esquema PostgreSQL y uploads temporales propios y límites de 640 MB/75% CPU. Acceso local por túnel SSH en `127.0.0.1:8000`; no existe proxy público a ese puerto. El frontend puede probar procesos reales sin publicar funcionalidades nuevas ni modificar el servicio actual. Detener el servicio y túnel de QA cuando termine la validación final.

## Publicación privada de la versión documental

Publicación final autorizada por el coordinador el 15 de octubre de 2026, hora de Chile. Se ejecutó la suite completa nuevamente: **15 pruebas aprobadas en 5,67 segundos**. HTTP Basic se activó y validó en nginx **antes** de reiniciar la versión que permite uploads. nginx conserva TLS; `/`, aplicaciones, API, propuestas, assets y muestras responden **401 sin credencial y 200 con credencial**, verificadas por HTTPS. La credencial se encuentra únicamente en el archivo local `Acceso_Maquetas_Vertia.txt`, fuera del repositorio, y en almacenamiento privado remoto; nunca se imprime en los resultados.

El arranque tardó unos tres segundos; la comprobación inicial fija de dos segundos se adelantó al listener. Se verificó que la aplicación inició correctamente y se sustituyó esa espera por reintentos limitados en el script de despliegue. Se completó nginx con 16 MB y 120 segundos. No se modificó ningún servicio ajeno.

QA por HTTPS contra el servicio real con sus restricciones systemd: carga de PDF de texto y PNG, extracción/OCR reales, original descargado con hash idéntico, preview PNG válida, rechazo 403 del original a un perfil de otro país, campos conservados sin sobrescritura automática y revisión humana persistida en PostgreSQL. Se crearon solamente dos contratos sintéticos de QA. Claude permanece desconectado; no se consumieron APIs de IA.

El servicio público quedó activo con aproximadamente 62 MB de memoria en reposo; memoria disponible del VPS 2,7 GiB y disco libre 25 GiB. Se comprobaron uploads `0700`, archivos `0600` y htpasswd `root:www-data 0640`. Tras QA se detuvieron exclusivamente `iniciativas-vertia-uiqa.service` y el túnel SSH propio de puerto local 8000; el puerto de staging 8790 dejó de escuchar. No se borraron uploads de la aplicación ni datos de usuarios.

Fuente de publicación: repositorio `somos-moai/iniciativas-vertia`, árbol de trabajo coordinado y congelado antes del despliegue; commit final a cargo del coordinador. Los hashes locales se compararon con las respuestas HTTPS autenticadas y coinciden:

| Archivo | SHA256 |
|---|---|
| `frontend/dist/assets/index-VONnwKLm.js` | `17de9634ab88aa58298be65cc7a22324dd537090231dc3d74d958c051efc8209` |
| `frontend/dist/assets/index-CTvZoLKH.css` | `f31183cbc61417410d380658ed46832c31f1ad70f5ecdbd71901ccc56929b3ac` |
| `deliverables/prospectador.pdf` | `c3a45e2e59b4c065b27b319312f25faee4616d4961ffc09a05b5a9519a05aa29` |
| `deliverables/contratos.pdf` | `a065814c49f24632e4cc78a0ffb19f67d4f99dfb88ad34d8e22a76925f033259` |
| `frontend/dist/samples/contrato_servicios_demostracion.pdf` | `873c34066a47422f9f0f6f22b79ec1bcf7b15973f6152230e923d4a33451f350` |
| `frontend/dist/samples/contrato_imagen_demostracion.png` | `afb096519d6d2167f63a8289ec6a1103174b96fe8b3b3844cf5ecdc9c61a46ee` |

## Publicación c87b74c — 16-10-2026 (Claude Code)

Aprobada por el usuario. `python infra/deploy-demo.py --publish --private` desde commit c87b74c (rama main). Pruebas en el VPS antes de publicar: 15/15 en 5,61 s. Acceso privado reactivado antes de reiniciar; `nginx -t` correcto (avisos OCSP de certificados de otros sitios, preexistentes); salud local `{"status":"ok","database":"postgresql","mode":"synthetic"}`. Sin cambios de esquema; no se tocaron servicios ni bases ajenas.

Comprobación sin credenciales: 401 anónimo en `/`, `/contratos`, `/prospectador`, `/api/health`, `/api/state`, `/propuestas/contratos.pdf` y `/samples/...`. Servicio `active`. `index.html` publica `index-BZpHhlYZ.js` / `index-CTvZoLKH.css`; hash del JS y de `backend/document_worker.py` idénticos a los locales. `/api/document-capabilities` en loopback: `ocr_available:false`, `scan_mode:simulado_por_nombre_de_archivo`.

Pendiente: verificación autenticada del usuario (PDF → PNG → PDF en el sitio privado). La prueba `frontend/qa-document-versions.cjs` escribe datos y no debe apuntarse a producción.
