#!/usr/bin/env python3
"""Create the Week 4 10-slide presentation aligned to the independent analytical report.
Requires python-pptx; all plots are computed by build_report_enhanced.py.
"""
from pptx import Presentation
from pptx.util import Inches,Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN,MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
FIG=ROOT/'07_Evidence'/'Analytical_Figures'
OUT=ROOT/'06_Presentation'/'Consumer_Complaint_Week4_Presentation.pptx'
prs=Presentation();prs.slide_width=Inches(13.33);prs.slide_height=Inches(7.50)
NAVY=RGBColor(17,45,80);BLUE=RGBColor(55,110,152);GOLD=RGBColor(200,157,60);INK=RGBColor(34,52,69);PALE=RGBColor(233,240,246);WHITE=RGBColor(255,255,255);MUTED=RGBColor(101,116,131)
def rect(sl,x,y,w,h,fill,rounded=False):
 sh=sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h));sh.fill.solid();sh.fill.fore_color.rgb=fill;sh.line.fill.background();return sh

def txt(sl,content,x,y,w,h,size=18,bold=False,color=INK,align=None):
 box=sl.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h));tf=box.text_frame;tf.word_wrap=True;tf.margin_left=Inches(.03);tf.margin_right=Inches(.03);tf.margin_top=Inches(.02);tf.margin_bottom=Inches(.02)
 for i,line in enumerate(content.split('\n')):
  p=tf.paragraphs[0] if i==0 else tf.add_paragraph();p.text=line;p.font.name='Aptos';p.font.size=Pt(size);p.font.bold=bold;p.font.color.rgb=color;p.space_after=Pt(5)
  if align is not None:p.alignment=align
 return box

def new(head,kicker=None):
 sl=prs.slides.add_slide(prs.slide_layouts[6]);rect(sl,0,0,13.33,.12,GOLD)
 if kicker:txt(sl,kicker.upper(),.62,.26,12,.24,10,True,GOLD)
 txt(sl,head,.62,.61,12,1.02,27,True,NAVY)
 rect(sl,.62,7.15,12.05,.012,PALE)
 txt(sl,'ANALYSTLAB AFRICA  •  EXPERIENCE LAB  •  WEEK 4   |   Complaint data are consumer reports, not verified misconduct',.64,7.23,11.85,.18,8,False,MUTED)
 txt(sl,str(len(prs.slides)),12.45,7.23,.25,.18,8,False,MUTED,PP_ALIGN.RIGHT)
 return sl

def pic(sl,filename,x,y,w,h):
 im=Image.open(FIG/filename);ratio=im.width/im.height;bw,bh=w,h
 if ratio>w/h:bh=w/ratio
 else:bw=h*ratio
 sl.shapes.add_picture(str(FIG/filename), Inches(x+(w-bw)/2), Inches(y+(h-bh)/2),width=Inches(bw),height=Inches(bh))

def callout(sl,num,label,x,y,w=3.2):
 rect(sl,x,y,w,1.18,PALE,True);txt(sl,num,x+.12,y+.16,w-.24,.44,24,True,NAVY);txt(sl,label,x+.12,y+.67,w-.24,.34,11,False,INK)

def note(sl,t,x=.76,y=6.55,w=11.75):txt(sl,t,x,y,w,.44,12,False,MUTED)

# 1 Cover
s=prs.slides.add_slide(prs.slide_layouts[6]);rect(s,0,0,13.33,7.5,NAVY);rect(s,.63,.7,.11,5.9,GOLD)
txt(s,'ANALYSTLAB AFRICA   |   WEEK 4   |   DATA ANALYTICS',1.04,.89,11,.28,12,True,GOLD)
txt(s,'Consumer Complaint Trends\n& Response Intelligence',1.04,1.56,11.5,2.05,37,True,WHITE)
txt(s,'Complaint volume grew. The response pattern is more complicated.',1.04,4.35,10.8,.72,22,False,WHITE)
txt(s,'62,516 Bank of America complaint records  •  CFPB extract  •  2017–2023',1.04,6.62,11,.28,13,False,WHITE)

# 2 source
s=new('What exactly is being measured?','Evidence standard')
callout(s,'62,516','unique complaint IDs',.75,1.7);callout(s,'12','source fields',4.03,1.7);callout(s,'0','duplicate IDs',7.31,1.7);callout(s,'1 May 2017','source begins (partial 2017)',10.59,1.7,2.0)
rect(s,.75,3.28,11.83,2.72,PALE,True)
txt(s,'Two different clocks',1.04,3.55,5.0,.5,23,True,NAVY)
txt(s,'Date submitted = CFPB receives the complaint\nDate received = CFPB forwards the complaint to the company',1.04,4.18,10.4,1.2,20,False,INK)
note(s,'These dates cannot measure company resolution time, and complaint labels are consumer-reported allegations.')

# 3 volume
s=new('Complaint volume increased 83.08% from 2019 to 2022','Trend')
pic(s,'enhanced_annual_volume.png',.55,1.58,8.8,4.78)
callout(s,'7,075','2019 full-year complaints',9.42,1.78,3.25);callout(s,'12,953','2022 full-year complaints',9.42,3.1,3.25);callout(s,'+5,878','Net increase',9.42,4.42,3.25)
note(s,'Do not compare 2017 or 2023 annual totals directly: both periods are incomplete.')

# 4 drivers
s=new('Four product groups account for 96.89% of net growth','Growth attribution')
pic(s,'enhanced_growth_drivers.png',.55,1.64,8.8,4.77)
rect(s,9.52,1.76,3.05,3.93,PALE,True)
txt(s,'2019 → 2022',9.7,2.02,2.65,.44,16,True,BLUE)
txt(s,'+2,106\nChecking / savings\n\n+1,656\nCredit / prepaid cards\n\n+1,231\nCredit reporting',9.7,2.59,2.65,2.73,15,False,NAVY)
note(s,'Growth counts are descriptive, not complaint incidence per active account.')

# 5 products
s=new('The issue mix changes with the financial product','Products and issues')
pic(s,'enhanced_products.png',.45,1.55,7.1,4.82)
rect(s,7.5,1.79,5.2,4.31,PALE,True)
txt(s,'Product → leading consumer-reported issue',7.7,2.0,4.8,.7,18,True,NAVY)
txt(s,'Checking/savings: Managing an account  |  15,109\nCredit/prepaid: Purchase on statement  |  4,415\nCredit reporting: Incorrect information  |  4,145\nMoney transfer: Fraud or scam  |  1,951',7.73,2.94,4.65,2.72,17,False,INK)
note(s,'Reported issues are not verified facts. Use product × issue cross-tabs for investigation.')

# 6 timing
s=new('A 96.06% overall timely rate masks a 2021 low','Response intelligence')
pic(s,'enhanced_timeliness_by_year.png',.65,1.63,8.68,4.65)
callout(s,'96.06%','All-time eligible rate',9.5,1.95,3.07);callout(s,'89.02%','2021 eligible rate',9.5,3.27,3.07);callout(s,'58.35%','June 2021 eligible rate',9.5,4.59,3.07)
note(s,'Timeliness = Yes / (Yes + No); the 1,494 blank records must not be recoded No.')

# 7 recent period
s=new('July 2023 was a volume peak, but many cases were still open','Recent-period caution')
pic(s,'enhanced_2023_inprogress.png',.56,1.67,8.73,4.74)
callout(s,'1,749','July 2023 records',9.46,1.95,3.12);callout(s,'863','July cases In progress',9.46,3.27,3.12);callout(s,'49.34%','Share In progress in July',9.46,4.59,3.12)
note(s,'August ends 28 Aug 2023; eligible-only rates may look artificially high while recent cases remain open.')

# 8 responses
s=new('Recorded response types are not proof of satisfactory resolution','Company responses')
pic(s,'enhanced_response_types.png',.5,1.64,9.2,4.65)
callout(s,'41,044','Closed with explanation',9.62,2.05,2.95);callout(s,'14,697','Monetary relief',9.62,3.39,2.95)
note(s,'60,311 chose not to provide a public-facing response; 2,175 public-response fields are blank.')

# 9 forwarding
s=new('CFPB forwarding was often same-day, with a long tail','Forwarding interval')
pic(s,'enhanced_forwarding_bands.png',.6,1.67,8.66,4.7)
callout(s,'79.39%','Zero calendar-day intervals',9.47,1.95,3.1);callout(s,'623','Above the 25-day P99 threshold',9.47,3.27,3.1);callout(s,'275 days','Maximum recorded interval',9.47,4.59,3.1)
note(s,'25 days is an analytical outlier threshold, not a legal deadline or company-resolution benchmark.')

# 10 recommendations
s=new('Four evidence-led recommendations','Decision and handover')
recs=[('01','Review high-volume product × issue combinations'),('02','Audit the June–October 2021 timeliness classifications'),('03','Show recent In progress cohorts beside eligible timeliness'),('04','Investigate CFPB forwarding intervals longer than 25 days')]
for i,(n,t) in enumerate(recs):
 y=1.68+i*1.05;rect(s,.85,y,11.6,.83,PALE,True);txt(s,n,1.08,y+.17,.54,.35,21,True,GOLD);txt(s,t,1.86,y+.19,10.0,.42,18,True,NAVY)
rect(s,.89,6.18,11.56,.47,NAVY,True);txt(s,'Deliverables: validated CSV • Power Query M • DAX • interactive HTML • 19-page report • README • QA evidence',1.08,6.29,11.1,.26,11,False,WHITE)
OUT.parent.mkdir(exist_ok=True,parents=True);prs.save(OUT);print('Created',len(prs.slides),'slides:',OUT)
