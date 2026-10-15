"""Render the native Word PDFs through the bundled Poppler for visual QA."""
from pathlib import Path
from decimal import Decimal
import json
from pypdf import PdfReader
from pdf2image import convert_from_path
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[1]
POPPLER=Path(r'C:\Users\cueva\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin')
fin=json.loads((ROOT/'docs/commercial/financials.json').read_text(encoding='utf-8-sig'))
for project in fin['projects']:
    for field in ['usd_net','usd_vat','usd_gross','uf_net','uf_vat','uf_gross']:
        total=sum(Decimal(str(p[field])) for p in project['payments'])
        assert total==Decimal(str(project[field])),(project['id'],field,total,project[field])
    ident=project['id']; pdf=ROOT/'deliverables'/f'{ident}.pdf'
    out=ROOT/'artifacts/qa'/ident;out.mkdir(parents=True,exist_ok=True)
    reader=PdfReader(pdf)
    print(ident,len(reader.pages),'pages; payment totals reconcile')
    for i,p in enumerate(reader.pages,1):
        text=p.extract_text() or ''
        print(i,len(text),text[:95].replace('\n',' / '), '... END:',text[-130:].replace('\n',' / '))
    pages=convert_from_path(pdf,dpi=120,poppler_path=POPPLER,fmt='png',output_folder=out,paths_only=False)
    for i,page in enumerate(pages,1):page.save(out/f'page-{i}.png')
    for start in range(0,len(pages),4):
        sheet=Image.new('RGB',(920,1250),'#dce3e8'); draw=ImageDraw.Draw(sheet)
        for j,page in enumerate(pages[start:start+4]):
            page.thumbnail((440,590));x=10+(j%2)*460;y=30+(j//2)*620
            sheet.paste(page,(x,y));draw.text((x,y-20),f'{ident} page {start+j+1}',fill='black')
        sheet.save(out/f'sheet-{start//4+1}.png')
print('Render fallback: packaged render_docx.py diagnosed missing soffice; native Microsoft Word ExportAsFixedFormat used. All PDF pages rasterized with bundled Poppler.')
