# Backend de demostración Vertia

FastAPI + SQLAlchemy 2 + psycopg 3. PostgreSQL real obligatorio. Sin archivos `.env`, sin fallback SQLite, sin llamadas salientes a proveedores. No se leen credenciales desde disco.

Desde la raíz del repositorio, instalar `python -m pip install -r backend/requirements.txt`. Entregar `DATABASE_URL` como variable de entorno del proceso, apuntando a una **base dedicada a esta demo**, por ejemplo `postgresql+psycopg://USUARIO:CLAVE@HOST:5432/vertia_demo` (marcadores, no credenciales reales). El usuario requiere creación de tablas en su esquema; no necesita superusuario.

Ejecutar `python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000`. El proxy publica `/api`; no exponer directamente el puerto del backend a Internet. La primera ejecución crea dos tablas `vertia_demo_records` y `vertia_demo_meta` y carga semilla determinística bajo bloqueo PostgreSQL. Los reinicios conservan todos los cambios. No existe endpoint público de reset.

`GET /api/health` comprueba PostgreSQL. OpenAPI en `/docs` permite revisar el contrato durante desarrollo. En demostraciones públicas aplicar restricción de acceso en el proxy: el selector `X-Demo-User` es **una simulación de identidad, no autenticación**. Toda autorización de lectura, exportación, documento y transición se evalúa en servidor para el perfil seleccionado; esto no reemplaza SSO/OIDC productivo.

## Integración

Ver `docs/API_CONTRACT.md` y `docs/coordination/codex-backend.md`. Frontend hace `fetch('/api/state?app=contratos', {headers: {'X-Demo-User': 'regional'}})` y refresca estado luego de cada acción exitosa. Todo proveedor tiene estado `simulado`, salvo PostgreSQL. Una firma demo no es una firma legal. La auditoría demo es persistente, pero no WORM ni evidencia de certificación.

## Pruebas reales

Configurar `TEST_DATABASE_URL` hacia PostgreSQL autorizado y ejecutar `python -m pytest backend/tests -q`. La suite crea un esquema aleatorio `vertia_test_<uuid>`, usa exclusivamente ese esquema y lo elimina al finalizar. El usuario de pruebas necesita `CREATE` en la base. No trunca tablas de otros esquemas ni usa datos corporativos. Sin PostgreSQL configurado, las pruebas se marcan omitidas; eso **no es validación de integración**. La suite cubre ACL país/cartera, perfiles inválidos y de lectura, aprobación humana, bloqueo de exclusiones, duplicados, créditos, ciclo contractual, análisis, saneamiento real del HTML, accesos temporales, exports y persistencia.

## Límites expresos

- Datos sintéticos de cinco países, correos `.example` exclusivamente.
- Los documentos son representaciones HTML y metadatos sintéticos; no se suben binarios reales ni se ejecuta OCR real.
- Motor de estados acotado, sin firma legal, envío real, APIs externas, scheduler ni SSO.
- Reglas contractuales no constituyen asesoría jurídica; las validaciones locales dependen de Vertia.
- Las credenciales, backups, HTTPS, restricción pública, retención y observabilidad de infraestructura pertenecen al despliegue del coordinador.
