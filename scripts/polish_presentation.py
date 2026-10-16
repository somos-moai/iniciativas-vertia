from pathlib import Path
import re, shutil, tempfile
p=Path(__file__).resolve().parents[1]/'frontend/src/presentation.css'
source=p.read_text(encoding='utf-8')
source=re.sub(r'font-size:(\d+(?:\.\d+)?)px',lambda m:'font-size:'+str(max(10,float(m[1]))).removesuffix('.0')+'px',source)
p.write_text(source,encoding='utf-8')
print('Presentation type minimum 10px for small labels; body remains 13-17px.')
preview=Path(tempfile.gettempdir())/'vertia-presentation-preview/src'
if preview.is_dir():
    for name in ['PresentationHub.jsx','presentation.css']:
        shutil.copy2(p.parent/name,preview/name)
