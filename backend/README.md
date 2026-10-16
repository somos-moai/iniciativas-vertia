# Backend de demostración Vertia

FastAPI + SQLAlchemy 2 + psycopg 3. PostgreSQL real obligatorio. Sin lectura de archivos `.env`, sin fallback SQLite, sin llamadas salientes a proveedores. Procesamiento local de PDF mediante pypdf y PDFium; las imágenes usan un escaneo simulado por nombre de archivo (sin OCR). No se leen credenciales desde disco.

Desde la raíz del repositorio, instalar `python -m pip install -r backend/requirements.txt`. Entregar `DATABASE_URL` como variable de entorno del proceso, apuntando a una **base dedicada a esta demo**, por ejemplo `postgresql+psycopg://USUARIO:CLAVE@HOST:5432/vertia_demo` (marcadores, no credenciales reales). El usuario requiere creación de tablas en su esquema; no necesita superusuario.

Ejecutar `python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000`, con un único worker para mantener una lectura simultánea. El proxy publica `/api`; no exponer directamente el puerto del backend a Internet. La primera ejecución crea tablas `vertia_demo_records`, `vertia_demo_meta` y `vertia_document_uploads` y carga semilla determinística bajo bloqueo PostgreSQL. Los reinicios conservan todos los cambios. No existe endpoint público de reset.

Configurar `UPLOAD_DIR` hacia un directorio privado dedicado y writable por el servicio (700; archivos 600), nunca dentro de `frontend/dist` ni documentos publicables. Tesseract ya no es necesario. Límites: 15 MiB, 40 páginas, 20 megapíxeles y 90 segundos; proxy máximo16MiB y timeout120s. Activar autenticación del sitio completo antes de exponer cargas reales: el selector de perfiles sigue siendo demostrativo. Conservar respaldo conjunto PostgreSQL+UPLOAD_DIR; uno sin el otro no restaura originales.

`GET /api/health` comprueba PostgreSQL. OpenAPI en `/docs` permite revisar el contrato durante desarrollo. En demostraciones públicas aplicar restricción de acceso en el proxy: el selector `X-Demo-User` es **una simulación de identidad, no autenticación**. Toda autorización de lectura, exportación, documento y transición se evalúa en servidor para el perfil seleccionado; esto no reemplaza SSO/OIDC productivo.

## Integración

Ver `docs/API_CONTRACT.md`, `docs/API_UPLOADS.md` y `docs/coordination/codex-backend.md`. Frontend hace `fetch('/api/state?app=contratos', {headers: {'X-Demo-User': 'regional'}})` y refresca estado luego de cada acción exitosa. Los proveedores externos siguen desconectados/simulados; lectura y OCR local de archivos reales no son simulaciones. Una firma demo no es una firma legal. La auditoría demo es persistente, pero no WORM ni evidencia de certificación.

## Pruebas reales

Configurar `TEST_DATABASE_URL` hacia PostgreSQL autorizado y ejecutar `python -m pytest backend/tests -q`. La suite crea esquemas aleatorios `vertia_test_<uuid>`, usa exclusivamente esos esquemas y los elimina al finalizar. El usuario de pruebas necesita `CREATE` en la base. No trunca tablas de otros esquemas ni usa datos corporativos. Sin PostgreSQL configurado, las pruebas se marcan omitidas; eso **no es validación de integración**. Incluye 15 pruebas de ACL, aprobación, exclusión, créditos, flujos, texto PDF real, OCR PNG real, previews, bytes originales, campos con evidencia, revisión humana, controles de tamaño/formato, saneamiento y versiones, e ICP con datos faltantes. OCR se omite solo si falta Tesseract: ejecutar completo en VPS con spa+eng.

## Límites expresos

- Datos iniciales sintéticos de cinco países, correos `.example` exclusivamente; archivos aportados por el usuario se identifican como reales, no fixtures.
- Extracción local de PDF y escaneo simulado de imágenes, con propuestas por reglas y revisión humana. No hay interpretación jurídica por Claude; no se inventan hallazgos.
- Motor de estados acotado, sin firma legal, envío real, APIs externas, scheduler ni SSO. Acceso concedido entre países permite únicamente extracto saneado aprobado, nunca original o texto OCR.
- ICP se evalúa con datos ingresados y criterios transparentes; no se inventan empleados, presupuesto, señales ni evidencia web.
- Reglas contractuales no constituyen asesoría jurídica; las validaciones locales dependen de Vertia.
- Las credenciales, backups, HTTPS, restricción pública, retención y observabilidad de infraestructura pertenecen al despliegue del coordinador.
