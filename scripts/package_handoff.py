"""Package commercial deliverables and check source for accidental credentials."""
from pathlib import Path
import json, re, shutil, subprocess, zipfile
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'deliverables'
for name in ['requerimientos-cliente.md','protocolo-soporte.md','roadmap-regional.md','scope-roadmap.json','supuestos.md']:
    shutil.copy2(ROOT/'docs/commercial'/name,OUT/name)
readme='''# Entrega comercial MoAI para Vertia

15 de octubre de 2026.

Prospectador y Gestión Contractual se presentan como propuestas independientes.
Cada una cuenta con HTML de lectura, Word editable y PDF revisado visualmente.

Maquetas: https://iniciativasvertia.somosmoai.tech
Repositorio: https://github.com/somos-moai/iniciativas-vertia

Los valores de referencia son USD 13.000 y USD 30.000 netos, respectivamente.
Las propuestas fijan UF de contratación, IVA del 19 % separado y un calendario
de 40 % inicial más seis cuotas de saldo. PAGOS_UF_v1.json contiene los importes
conciliados y sus fuentes; no es un archivo de importación a un sistema CLP.

Anexos: requerimientos a cargo de Vertia, protocolo de soporte y roadmap regional.
Los límites operativos y las condiciones de soporte son propuestas a formalizar.
Los costos de AWS, PostgreSQL, IA, OCR, prospectos y herramientas externas durante
desarrollo, pruebas y producción corresponden a Vertia.

Las maquetas son funcionales con datos sintéticos; integraciones y análisis son
simulados. El desarrollo productivo se delimita en cada propuesta.

Claude Code participó en los documentos. Codex implementó y verificó las maquetas.
La revisión de Gemini en Antigravity está preparada y permanece pendiente.
'''
(OUT/'LEER_PRIMERO.md').write_text(readme,encoding='utf-8')
names=['LEER_PRIMERO.md','PAGOS_UF_v1.json','requerimientos-cliente.md','protocolo-soporte.md','roadmap-regional.md','scope-roadmap.json','supuestos.md']
names += [f'{ident}.{ext}' for ident in ['prospectador','contratos'] for ext in ['html','docx','pdf']]
target=OUT/'Vertia_Propuestas_y_Anexos_2026-10-15.zip'
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as archive:
    for name in names:
        p=OUT/name;assert p.is_file() and p.stat().st_size>0,p
        archive.write(p,name)
print('Packaged',len(names),'files;',target.stat().st_size,'bytes')

paths=subprocess.run(['git','ls-files','--cached','--others','--exclude-standard','-z'],cwd=ROOT,capture_output=True,check=True).stdout.decode('utf-8').split('\0')
patterns=[re.compile(r'sk-ant-[A-Za-z0-9_-]{25,}'),re.compile(r'AIza[A-Za-z0-9_-]{30,}'),re.compile(r'ghp_[A-Za-z0-9]{25,}'),re.compile(r'github_pat_[A-Za-z0-9_]{30,}'),re.compile(r'-----BEGIN (?:OPENSSH|RSA|EC) PRIVATE KEY-----')]
bad=[]
for name in set(paths):
    p=ROOT/name
    if not name or not p.is_file() or p.suffix.lower() in {'.png','.webp','.jpg','.pdf','.docx','.ico'}:continue
    text=p.read_text(encoding='utf-8',errors='ignore')
    if any(pattern.search(text) for pattern in patterns):bad.append(name)
if bad:raise RuntimeError('Potential credentials in: '+', '.join(bad))
print('Source credential-pattern check passed.')
