"""Request an actual bounded Claude Code review, without accessing API credentials."""
from pathlib import Path
import json, subprocess, shutil, tempfile
ROOT=Path(__file__).resolve().parents[1]
context='\n\n'.join((ROOT/p).read_text(encoding='utf-8-sig') for p in ['docs/coordination/ENCARGO_EXPERIENCIA_V2.md','docs/BRIEF.md','docs/commercial/roadmap-regional.md','docs/commercial/flujos-y-modelo-datos.md'])
prompt='''Eres Claude Code del equipo MoAI. El usuario dice que la maqueta es pobre y quiere una presentación previa de ambos proyectos en el mismo HTML, animaciones que expliquen procesos, modelos de datos supuestos y lectura real de PDF e imágenes. Transmite su confianza al equipo con trabajo verificable. Revisa el encargo y redacta una crítica de producto útil para implementar ahora. No edites archivos ni uses herramientas. Devuelve SOLO JSON válido con claves review_md y presentation_copy_md. En review_md enumera 8 criterios verificables y 5 supuestos de datos por proyecto, diferenciando modelo lógico propuesto de JSONB demo. presentation_copy_md: narrativa ejecutiva sobria de 600 palabras máximo, con apertura, dos proyectos, flujo de 5 etapas cada uno, roadmap 8-10/12-16 semanas y entrega regional; justifica valor sin ROI inventado ni metáforas vacías. IA externa y firma siguen desconectadas; extracción y OCR local serán reales. No confundas OCR con Claude. No cambies precio ni condiciones.\n\n'''+context
work=Path(tempfile.gettempdir())/'vertia-claude-experience';work.mkdir(exist_ok=True)
result=subprocess.run([shutil.which('claude'),'-p','--tools','','--model','opus','--output-format','json'],input=prompt,text=True,encoding='utf-8',errors='replace',capture_output=True,cwd=work,timeout=360)
if result.returncode:raise RuntimeError(result.stderr[:700])
envelope=json.loads(result.stdout);raw=envelope.get('result','').strip()
if raw.startswith('```'):raw=raw.split('\n',1)[1].rsplit('```',1)[0]
review=json.loads(raw)
out=ROOT/'docs/coordination/claude-experiencia-v2.md'
out.write_text('# Revisión de experiencia mediante Claude Code\n\nEjecución real con selector opus, 15 octubre 2026.\n\n'+review['review_md']+'\n\n## Narrativa sugerida\n\n'+review['presentation_copy_md'],encoding='utf-8')
print('Claude Code experience review complete; stop_reason='+str(envelope.get('stop_reason')))
