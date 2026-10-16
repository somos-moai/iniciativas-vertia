# Frontend y pruebas de navegador

Aplicaciones React/Vite en `/prospectador` y `/contratos`; la portada explicativa vive en `PresentationHub.jsx`. La API aplica los permisos y persiste los cambios; el frontend no reemplaza esa autorización.

## Compilación en Windows con unidad compartida

Desde la raíz del repositorio:

```powershell
node frontend/build-local.cjs
```

El script instala y compila en un directorio temporal local y copia `dist/` a `frontend/`. Evita los errores de extracción concurrente de npm observados en Google Drive. En un filesystem local normal también funciona `npm install` y `npm run build` desde `frontend/`.

## Comprobación breve de la demostración publicada

Instalar Playwright una vez en su caché local:

```powershell
npm install --prefix "$env:TEMP\vertia-browser-qa" playwright
```

Se utiliza Microsoft Edge instalado; no se descarga otro navegador. Desde la raíz:

```powershell
node --use-system-ca frontend/qa-browser.cjs --smoke
```

El comando comprueba la protección frente a solicitudes anónimas, HTTPS con validación de certificado, la portada actual, los logos, el recorrido manual, la aplicación contractual, el PDF de ejemplo con lectura real y la portada móvil. Conserva o crea un expediente sintético de Faro Retail para hacer la prueba idempotente. No llama a APIs externas de pago.

La autenticación HTTP se carga únicamente en memoria desde el archivo de acceso autorizado ubicado junto a la carpeta del repositorio, `Acceso_Maquetas_Vertia.txt`. Si se necesita otra ubicación, definir `VERTIA_QA_CREDENTIAL_FILE`. La URL se puede ajustar con `VERTIA_QA_BASE`. Nunca escribir usuarios, claves o cabeceras de autorización en los scripts, reportes o repositorio. `--use-system-ca` permite usar las autoridades de confianza de Windows sin desactivar la verificación TLS.

Resultados y capturas: `artifacts/qa/private-smoke/` (ignorado por Git). Los errores se registran sin cabeceras ni credenciales.

## Recorridos completos actuales, sobre staging aislado

Preparar una API de staging con PostgreSQL y almacenamiento de archivos dedicados; el túnel autorizado debe escuchar en `127.0.0.1:8000`. Ejecutar Vite desde el caché local de compilación en el puerto 5180. Su proxy `/api` apunta a ese puerto 8000. No ejecutar estas pruebas contra una base corporativa.

```powershell
node frontend/qa-workspaces.cjs
node frontend/qa-workspaces-extra.cjs
node frontend/qa-summary.cjs
```

Los primeros dos comandos verifican ICP, fuentes y faltantes, cambios de perfil, selección de cuentas y responsables, campaña con criterios conservados, cargas PDF/imagen, escaneo simulado de imágenes por nombre de archivo, revisión humana, extracto autorizado, aislamiento del original entre países, conservación de formularios frente a errores 400 y vistas móviles. El tercer comando consolida el informe. Las pruebas usan documentos sintéticos y no consumen proveedores externos.

Resultados y capturas: `artifacts/qa/workspaces/`. Informe legible: `docs/coordination/qa-workspaces.md`. Se aprobaron 38 comprobaciones para la entrega actual.

`qa-captures.cjs` permite regenerar las comparaciones de original y evidencia de los expedientes de muestras existentes, sin crear registros. `qa-browser-v1.cjs` conserva la suite anterior revisada por Gemini, para referencia histórica de la versión con documentos sintéticos; sus selectores no representan el flujo de carga real actual. No se utiliza como comprobación de esta entrega.
