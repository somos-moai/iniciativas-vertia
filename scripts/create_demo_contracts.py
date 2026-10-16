"""Create synthetic but actual PDF/image files for the real upload journey."""
from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pdf2image import convert_from_path
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'frontend/public/samples';OUT.mkdir(parents=True,exist_ok=True)
pdfmetrics.registerFont(TTFont('DemoArial',r'C:\Windows\Fonts\arial.ttf'))
pdfmetrics.registerFont(TTFont('DemoArialBold',r'C:\Windows\Fonts\arialbd.ttf'))
ink=HexColor('#103B58')
styles={
 'title':ParagraphStyle('title',fontName='DemoArialBold',fontSize=23,leading=27,textColor=ink,spaceAfter=22),
 'heading':ParagraphStyle('heading',fontName='DemoArialBold',fontSize=13,leading=18,textColor=ink,spaceBefore=18,spaceAfter=9),
 'body':ParagraphStyle('body',fontName='DemoArial',fontSize=10.5,leading=17,spaceAfter=12),
 'data':ParagraphStyle('data',fontName='DemoArial',fontSize=10.5,leading=17,spaceAfter=7),
 'small':ParagraphStyle('small',fontName='DemoArial',fontSize=9,leading=14,textColor=HexColor('#667D8C'),spaceAfter=14),
}
def header(canvas,doc):
    canvas.saveState();canvas.setFillColor(ink);canvas.rect(0,717,612,75,fill=1,stroke=0)
    logo=ImageReader(ROOT/'frontend/public/brand/vertia.webp')
    canvas.drawImage(logo,45,735,width=150,height=32,mask='auto',preserveAspectRatio=True)
    canvas.setFillColor(HexColor('#D6E5EF'));canvas.setFont('DemoArial',8)
    canvas.drawRightString(567,752,'EXPEDIENTE VRT-CL-DEMO-001')
    canvas.drawRightString(567,737,'Documento sintético de demostración')
    canvas.setStrokeColor(HexColor('#D8E3EA'));canvas.line(45,51,567,51)
    canvas.setFillColor(HexColor('#677F90'));canvas.setFont('DemoArial',8)
    canvas.drawString(45,35,'Sin efecto jurídico. Entidades y condiciones ficticias. No firmar ni utilizar en operaciones reales.')
    canvas.drawRightString(567,20,f'{doc.page} / 3')
    canvas.restoreState()

story=[]
def p(text,style='body'):story.append(Paragraph(text,styles[style]))
def h(text):p(text,'heading')
p('Contrato de servicios publicitarios','title')
p('Ejemplo para probar carga, lectura, revisión y control contractual. Todos los antecedentes son ficticios.','small')
for text in ['País: Chile','Sociedad: Vertia Chile Demo SpA (entidad ficticia)','Contraparte: Faro Retail SpA (entidad ficticia)','Tipo de contrato: Servicios','Monto total: USD 12.500,00','Moneda: USD','Fecha de inicio: 2026-10-01','Fecha de término: 2027-12-31','Responsable del expediente: Área Comercial Demo']:
    p(text,'data')
h('1 Objeto del servicio')
p('Vertia Chile Demo SpA prestará a Faro Retail SpA servicios de planificación y exhibición publicitaria en soportes definidos en una orden de campaña. La orden identificará ubicaciones, período de exhibición, materiales y responsables operativos. Esta descripción solo sirve para demostrar la lectura de un contrato.')
h('2 Entrega y validación de materiales')
p('La contraparte entregará las piezas gráficas y las autorizaciones necesarias antes del inicio de cada campaña. El responsable operativo verificará las especificaciones técnicas y registrará la aceptación de los materiales. Las observaciones se incorporarán al expediente antes de autorizar su publicación.')
story.append(PageBreak())
p('Obligaciones y condiciones','title')
h('3 Reportes de exhibición')
p('Operaciones emitirá un reporte mensual de exhibición a más tardar el día 10 del mes siguiente. El reporte contendrá período, soportes, incidencias y evidencia disponible. El responsable del contrato registrará su recepción y cualquier observación de la contraparte.')
h('4 Condiciones económicas')
p('El monto indicado en la ficha corresponde al total de referencia del servicio ficticio. Toda modificación de alcance, precio o período requiere revisión y aprobación escrita. Las condiciones de facturación se verificarán antes de activar el expediente; la lectura automática no determina obligaciones tributarias.')
h('5 Confidencialidad y uso de antecedentes')
p('Los documentos comerciales y sus condiciones se compartirán únicamente con personas autorizadas. Una solicitud de acceso desde otro país debe indicar el propósito y el plazo. El responsable revisará un extracto autorizado antes de conceder acceso; la autorización no implica redistribuir el documento original.')
h('6 Incidencias y evidencia')
p('Una incidencia operativa deberá identificar fecha, campaña y soporte afectado. Su seguimiento registrará responsable, acción correctiva y evidencia de cierre. La aplicación de descuentos o ajustes requiere la aprobación del responsable comercial y no se ejecuta por una sugerencia de extracción.')
h('7 Revisión de datos')
p('La contraparte, el monto, la moneda y las fechas de este documento deben contrastarse con la página de origen antes de confirmar la ficha. Si existe discrepancia entre la extracción y el archivo, una persona deberá corregir el valor y registrar la razón de su decisión.')
story.append(PageBreak())
p('Vigencia y control de cambios','title')
h('8 Aviso previo de renovación')
p('El responsable del contrato revisará la continuidad del servicio con al menos 60 días de anticipación al término de la vigencia. La revisión deberá dejar una decisión registrada y señalar si corresponde una renovación, una enmienda o el cierre del expediente.')
h('9 Versiones y aprobaciones')
p('Cada carga documental debe conservar una versión identificable. Una nueva versión invalida las propuestas anteriores de lectura y los extractos preparados para compartir. El aprobador deberá comprobar que su decisión corresponde a la versión actual antes de remitir el documento al proveedor de firma.')
h('10 Formalización de la demostración')
p('Este archivo no acredita un acuerdo ni contiene firmas reales. El recorrido de firma del prototipo es simulado y no produce efectos jurídicos. La contratación productiva requiere el proveedor, los accesos y la validación legal que determine Vertia para cada país.')
h('Antecedentes de prueba')
p('Referencia: VRT-CL-DEMO-001. Correo de ejemplo: responsable@faro-retail.example. Documento generado para la demostración de MoAI y Vertia Group. Puede cargarse como PDF o como imagen para contrastar la extracción de texto con el OCR local.')
doc=SimpleDocTemplate(str(OUT/'contrato_servicios_demostracion.pdf'),pagesize=(612,792),topMargin=103,bottomMargin=70,leftMargin=45,rightMargin=45)
doc.build(story,onFirstPage=header,onLaterPages=header)
pdf=OUT/'contrato_servicios_demostracion.pdf';reader=PdfReader(pdf)
assert len(reader.pages)==3
assert '12.500,00' in reader.pages[0].extract_text()
poppler=Path(r'C:\Users\cueva\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin')
pages=convert_from_path(pdf,dpi=140,poppler_path=poppler)
pages[0].save(OUT/'contrato_imagen_demostracion.png')
qa=ROOT/'artifacts/qa/experience-v2';qa.mkdir(parents=True,exist_ok=True)
for i,page in enumerate(pages,1):page.save(qa/f'sample-contract-page-{i}.png')
print('Created actual three-page synthetic PDF and raster image for OCR; text asserted.')
