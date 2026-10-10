#!/usr/bin/env python3
"""Build the two current CV PDFs with ReportLab; reuse portfolio career content."""
from pathlib import Path
from html import escape
import runpy, shutil
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
ROOT=Path(__file__).resolve().parents[1]
content=runpy.run_path(str(ROOT/'scripts/build_site.py'))
fontdir=Path('/System/Library/Fonts/Supplemental')
for name,file in [('CV','Arial.ttf'),('CVBold','Arial Bold.ttf')]:pdfmetrics.registerFont(TTFont(name,str(fontdir/file)))
pdfmetrics.registerFontFamily('CV',normal='CV',bold='CVBold',italic='CV',boldItalic='CVBold')
ink=colors.HexColor('#212924'); green=colors.HexColor('#286b55'); muted=colors.HexColor('#58635b')
styles={
'name':ParagraphStyle('name',fontName='CVBold',fontSize=29,leading=34,textColor=ink,spaceAfter=7),
'role':ParagraphStyle('role',fontName='CVBold',fontSize=11,leading=15,textColor=green,spaceAfter=10),
'body':ParagraphStyle('body',fontName='CV',fontSize=9.4,leading=14,textColor=ink,spaceAfter=9),
'small':ParagraphStyle('small',fontName='CV',fontSize=8,leading=11,textColor=muted,spaceAfter=7),
'section':ParagraphStyle('section',fontName='CVBold',fontSize=12,leading=16,textColor=green,spaceBefore=12,spaceAfter=9),
'job':ParagraphStyle('job',fontName='CVBold',fontSize=10.2,leading=14,textColor=ink,spaceAfter=4),
'compact':ParagraphStyle('compact',fontName='CV',fontSize=8.6,leading=12.3,textColor=ink,spaceAfter=6)}
def p(text,style='body'):return Paragraph(text,styles[style])
def clean(s):return escape(s.replace('—','-').replace('–','-').replace('’',"'"))
def footer(c,doc):
 c.setStrokeColor(colors.HexColor('#d3d8cf'));c.line(42,37,553,37)
 c.setFont('CV',7);c.setFillColor(muted);c.drawString(42,25,'Francisco Caro Díaz | franciscocarodiaz.github.io');c.drawRightString(553,25,str(doc.page))
for lang in ['en','es']:
 d=content['DATA'][lang];es=lang=='es';items=[]
 items += [p('Francisco Caro Díaz','name'),p('Senior Android &amp; iOS Engineer | Mobile Tech Lead','role'),p('Sevilla, España' if es else 'Seville, Spain','small'),p('<link href="mailto:franciscocarodiaz@gmail.com">franciscocarodiaz@gmail.com</link> | <link href="https://www.linkedin.com/in/franciscocarodiaz/">LinkedIn</link> | <link href="https://github.com/franciscocarodiaz">GitHub</link> | <link href="https://franciscocarodiaz.github.io">Portfolio</link>','small')]
 summary=('Más de 13 años desarrollando y evolucionando productos móviles nativos. Combino desarrollo directo con liderazgo técnico, arquitectura, revisión de código, mentoring y responsabilidad sobre la calidad y las entregas. Trabajo en equipos pequeños y medianos junto a Producto, Diseño, Backend y QA.' if es else '13+ years building and evolving native mobile products. I combine hands-on development with technical leadership, architecture, code reviews, mentoring and ownership of quality and delivery. I work in small and mid-sized teams alongside Product, Design, Backend and QA.')
 items += [p(summary),p('Especialidades' if es else 'Core expertise','section'),p('Android: Kotlin, Jetpack Compose, Java, Coroutines, Room, Retrofit, Dagger/Hilt.<br/>iOS: Swift, SwiftUI.<br/>'+('Arquitectura e ingeniería' if es else 'Architecture &amp; engineering')+': Clean Architecture, MVVM, modularization, CI/CD, Fastlane, testing, Firebase, REST, GraphQL.'),p(('IA en mi trabajo diario: agentes de programación para explorar, implementar, refactorizar, probar y depurar código, con revisión técnica y responsabilidad sobre el resultado.' if es else 'AI in my daily workflow: coding agents for code exploration, implementation, refactoring, testing and debugging, with engineering review and ownership of the result.'))]
 items += [p('Experiencia reciente' if es else 'Recent experience','section')]
 for company,role,date,en,sp,stack in content['JOBS'][:3]:
  date=date.format(present=d['present'])
  if es:date=date.replace('Aug','Ago')
  items.append(KeepTogether([p(clean(company)+' | '+clean(role),'job'),p(clean(date),'small'),p(clean(sp if es else en)),p(clean(stack),'small')]))
 items += [PageBreak(),p('Trayectoria anterior' if es else 'Earlier experience','section')]
 for company,role,date,en,sp,stack in content['JOBS'][3:]:
  if es:date=date.replace('Jan','Ene').replace('Apr','Abr')
  items.append(KeepTogether([p(clean(company)+' | '+clean(role),'job'),p(clean(date)+'<br/>'+clean(sp if es else en),'compact')]))
 items += [p('Formación' if es else 'Education & training','section')]
 edu=[('Universidad de Sevilla','Ingeniería Informática | 2003-2011' if es else 'Computer Science | 2003-2011'),('Universidad de Sevilla','Máster: Desarrollo Web y Mobile | 2011-2012; Máster: E-learning | 2010-2012' if es else 'Master: Web & Mobile Development | 2011-2012; Master: E-learning | 2010-2012'),('Ironhack, Barcelona','Bootcamp de Desarrollo iOS | 2014 | Más de 400 horas' if es else 'iOS Development Bootcamp | 2014 | 400+ hours'),('Udacity / Stanford','Android / iOS con Swift | 2015' if es else 'Android / iOS with Swift | 2015'),('Scrum Manager','Scrum Expert | ID 19504')]
 for org,desc in edu:items.append(p('<b>'+clean(org)+'</b> - '+clean(desc),'compact'))
 items += [p('Idiomas' if es else 'Languages','section'),p('Inglés e italiano: competencia profesional. Francés: competencia profesional limitada.' if es else 'English and Italian: professional working proficiency. French: limited working proficiency.','compact'),p('Actualizado: octubre de 2026' if es else 'Updated: October 2026','small')]
 path=ROOT/f'files/cv/Francisco-Caro-Diaz-CV-{lang.upper()}.pdf'
 doc=SimpleDocTemplate(str(path),pagesize=(595.28,841.89),rightMargin=42,leftMargin=42,topMargin=39,bottomMargin=49,title=f'Francisco Caro Díaz - CV ({lang.upper()})',author='Francisco Caro Díaz')
 doc.build(items,onFirstPage=footer,onLaterPages=footer)
 legacy=['files/cv/CV-EN-FranciscoCaroDiaz-Jun2024.pdf','landing_es/files/cv/CV-EN-FranciscoCaroDiaz-Jun2024.pdf'] if not es else ['files/cv/CV-FranciscoCaroDiaz-Agosto2020.pdf','landing_es/files/cv/CV-FranciscoCaroDiaz-Junio2024.pdf']
 for name in legacy:shutil.copyfile(path,ROOT/name)
 print(path)
