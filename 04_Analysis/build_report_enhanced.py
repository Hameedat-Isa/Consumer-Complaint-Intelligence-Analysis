#!/usr/bin/env python3
"""Generate the independently reanalysed narrative DOCX and supporting figures.
Uses source-derived validation_results.json and extended_insights.json; does not fabricate observations.
Run after prepare_and_validate.py and extended_insights.py. Python dependencies: python-docx, matplotlib.
Export DOCX to PDF using LibreOffice or the supplied DOCX rendering tools.
"""
import json, math
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_BREAK
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_LINE_SPACING
from docx.enum.table import WD_ROW_HEIGHT_RULE

BASE=Path(__file__).resolve().parents[1]
E=json.loads((BASE/'07_Evidence'/'extended_insights.json').read_text())
A=json.loads((BASE/'07_Evidence'/'validation_results.json').read_text())
FIG=BASE/'07_Evidence'/'Analytical_Figures';FIG.mkdir(parents=True,exist_ok=True)
SHOT=BASE/'07_Evidence'/'Dashboard_Screenshots'
OUT=BASE/'01_Report'/'Consumer_Complaint_Intelligence_Report.docx'
NAVY='#112D50';DARK='#233548'; GOLD='#C89D3C'; BLUE='#376E98';MUTED='#6A7784';PALE='#E8EFF5';RED='#B84A42';GREEN='#278174'

plt.rcParams.update({'figure.dpi':160,'font.size':10,'axes.titlesize':13,'axes.labelsize':9,'xtick.labelsize':8.5,'ytick.labelsize':8.5,'font.family':'DejaVu Sans','axes.spines.top':False,'axes.spines.right':False,'savefig.facecolor':'white'})
def finish(ax,filename,height=3.1):
 ax.grid(axis='y',alpha=.14);ax.set_axisbelow(True);ax.tick_params(length=0);plt.tight_layout(pad=1.4);plt.savefig(FIG/filename,bbox_inches='tight',dpi=170);plt.close()

# Figure 1. Annual volume from the source workbook; boundary years are partial.
years=list(range(2017,2024));nums=[A['year_counts'][str(y)] for y in years]
fig,ax=plt.subplots(figsize=(8.3,3.3));colors=[PALE]+[NAVY if y!=2022 else BLUE for y in range(2018,2023)]+[PALE]
bars=ax.bar([str(y) for y in years],nums,color=colors,width=.66,edgecolor='#BECBD5',linewidth=.4)
for b,n,y in zip(bars,nums,years):ax.text(b.get_x()+b.get_width()/2,n+180,f'{n:,}'+('*' if y in [2017,2023] else ''),ha='center',va='bottom',fontsize=9,color=DARK,fontweight='bold')
ax.set_ylim(0,15000);ax.set_ylabel('Complaint records');ax.set_title('Annual complaint volume  |  2017 and 2023 are partial years',loc='left',color=NAVY,fontweight='bold');finish(ax,'enhanced_annual_volume.png')

# Figure 2. Net drivers of change 2019->2022.
drivers=E['2019_2022_top_drivers'];names=['Checking & savings','Credit / prepaid cards','Credit reporting','Money transfer / services','Debt collection','Vehicle loans','Personal / payday loans','Student loans','Mortgage'];ds=[r['Change'] for r in drivers]
fig,ax=plt.subplots(figsize=(8.4,3.8));bars=ax.barh(names[::-1],ds[::-1],color=[BLUE if x>=0 else RED for x in ds[::-1]],height=.66)
for bar,v in zip(bars,ds[::-1]):ax.text(v+(40 if v>=0 else -40),bar.get_y()+bar.get_height()/2,f'{v:+,}',ha='left' if v>=0 else 'right',va='center',fontsize=8.7,fontweight='bold')
ax.axvline(0,color='#8293A3',linewidth=.8);ax.set_xlim(-370,2400);ax.set_xlabel('Change in complaints, 2019 to 2022');ax.set_title('Four product groups explain nearly all net growth',loc='left',color=NAVY,fontweight='bold');finish(ax,'enhanced_growth_drivers.png')

# Figure 3. product volume.
products=list(A['product_counts'].items())
short=['Checking / savings','Credit / prepaid card','Credit reporting','Mortgage','Money transfer','Debt collection','Vehicle loan / lease','Payday / personal loan','Student loan']
fig,ax=plt.subplots(figsize=(8.4,3.5));bars=ax.barh(short[::-1],[v for _,v in products][::-1],color=[BLUE if i<2 else NAVY for i in range(len(products))][::-1],height=.7)
for b,v in zip(bars,[v for _,v in products][::-1]):ax.text(v+250,b.get_y()+b.get_height()/2,f'{v:,}',fontsize=8,va='center',color=DARK)
ax.set_xlim(0,28500);ax.set_title('Two products contribute 65.60% of all complaint records',color=NAVY,fontweight='bold',loc='left');ax.set_xlabel('Complaint records');finish(ax,'enhanced_products.png')

# Figure 4. recorded timeliness rates per year.
tby=E['timeliness_by_year'];fig,ax=plt.subplots(figsize=(8.4,3.25));yy=[x['Year'] for x in tby];rates=[x['Timely_eligible_percent'] for x in tby]
ax.plot(yy,rates,color=NAVY,marker='o',linewidth=2,markersize=6);ax.scatter([2021],[rates[4]],s=90,color=RED,zorder=4)
for y,r in zip(yy,rates):ax.annotate(f'{r:.1f}%',(y,r),xytext=(0,9 if y!=2021 else -19),textcoords='offset points',ha='center',color=RED if y==2021 else DARK,fontsize=8,fontweight='bold')
ax.set_xticks(yy);ax.set_ylim(83,103);ax.set_ylabel('% Yes among valid Yes/No');ax.set_title('A high overall rate conceals a substantial dip in 2021',loc='left',color=NAVY,fontweight='bold');finish(ax,'enhanced_timeliness_by_year.png')

# Figure 5. 2021 monthly timeliness
m21=E['2021_months'];fig,ax=plt.subplots(figsize=(8.4,3.25));x=list(range(1,13));y=[d['Timely_eligible_percent'] for d in m21]
ax.plot(x,y,color=NAVY,marker='o',linewidth=2.1);ax.axvspan(5.5,10.5,color='#FCEFEA',alpha=.6);ax.annotate('June: 58.4%',(6,y[5]),xytext=(7.0,69),arrowprops={'arrowstyle':'->','color':RED},color=RED,fontsize=9,fontweight='bold')
ax.set_ylim(50,104);ax.set_xticks(x,['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']);ax.set_ylabel('Valid Yes/No timeliness %');ax.set_title('2021: the midyear decline is concentrated in June–October',color=NAVY,fontweight='bold',loc='left');finish(ax,'enhanced_2021_timeliness.png')

# Figure 6. 2023 in-progress month mix
m23=E['2023_months'];fig,ax=plt.subplots(figsize=(8.4,3.4));xx=range(1,9);closed=[d['Yes']+d['No'] for d in m23];inprog=[d['Excluded'] for d in m23]
ax.bar(xx,closed,color=NAVY,label='Valid Yes / No');ax.bar(xx,inprog,bottom=closed,color=GOLD,label='In progress / no timeliness')
for m,tot,exc in zip(xx,[d['Total'] for d in m23],inprog):
 if m in (7,8):ax.text(m,tot+28,f'{tot:,}\n{exc:,} in progress',fontsize=8,ha='center',fontweight='bold',color=DARK)
ax.set_xticks(list(xx),['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug*']);ax.set_ylim(0,2060);ax.set_ylabel('Complaint records');ax.legend(loc='upper left',frameon=False,ncol=2,fontsize=8);ax.set_title('July 2023 is high volume — and roughly half still in progress',color=NAVY,fontweight='bold',loc='left');finish(ax,'enhanced_2023_inprogress.png')

# Figure 7. overall recorded response categories
rs=A['response_counts'];lbl=['Closed with explanation','Monetary relief','Non-monetary relief','In progress','Closed (other)'];val=[rs['Closed with explanation'],rs['Closed with monetary relief'],rs['Closed with non-monetary relief'],rs['In progress'],rs['Closed']]
fig,ax=plt.subplots(figsize=(8.4,3.4));bars=ax.barh(lbl[::-1],val[::-1],color=[NAVY,BLUE,GOLD,'#8499AC',PALE][::-1],height=.65)
for b,v in zip(bars,val[::-1]):ax.text(v+280,b.get_y()+b.get_height()/2,f'{v:,}',va='center',fontsize=8.6)
ax.set_xlim(0,46200);ax.set_title('An explanation is the most common recorded company response',color=NAVY,fontweight='bold',loc='left');ax.set_xlabel('Complaints');finish(ax,'enhanced_response_types.png')

# Figure 8. Forwarding interval band chart
fb=E['forwarding'];labels=['0 days','1–4 days','5–9 days','10–24 days','25+ days'];nums=[fb['zero'],fb['one_to_four'],fb['five_to_nine'],fb['ten_to_twenty_four'],fb['twenty_five_plus']]
fig,ax=plt.subplots(figsize=(8.4,3.4));bars=ax.bar(labels,nums,color=[NAVY,BLUE,'#8295A7',GOLD,RED],width=.69)
for b,v in zip(bars,nums):ax.text(b.get_x()+b.get_width()/2,v+480,f'{v:,}',ha='center',fontsize=9,fontweight='bold',color=DARK)
ax.set_ylim(0,58000);ax.set_title('Forwarding often occurred on the same calendar date',color=NAVY,fontweight='bold',loc='left');ax.set_ylabel('Complaint records');finish(ax,'enhanced_forwarding_bands.png')

# Figure 9. forwarding average by product
fwp=A['forwarding_by_product'];shortmap=dict(zip([p for p,n in products],short));ordered=sorted(fwp.items(),key=lambda z:z[1]['mean_days']);fig,ax=plt.subplots(figsize=(8.4,3.35));vals=[i[1]['mean_days'] for i in ordered];bars=ax.barh([shortmap.get(k,k) for k,v in ordered],vals,color=[GOLD if v['count']<100 else BLUE for k,v in ordered])
for b,(k,v) in zip(bars,ordered):ax.text(v['mean_days']+.04,b.get_y()+b.get_height()/2,f'{v["mean_days"]:.2f}d (n={v["count"]:,})',va='center',fontsize=7.8)
ax.set_xlim(0,3.05);ax.set_xlabel('Average CFPB forwarding days');ax.set_title('Average forwarding differs across product categories',color=NAVY,fontweight='bold',loc='left');finish(ax,'enhanced_forwarding_by_product.png')

# Build DOCX with precise structure and render-safe typography.
doc=Document();section=doc.sections[0];section.page_height=Inches(11.69);section.page_width=Inches(8.27)
section.top_margin=Inches(.79);section.bottom_margin=Inches(.75);section.left_margin=Inches(.8);section.right_margin=Inches(.8);section.header_distance=Inches(.34);section.footer_distance=Inches(.36)
styles=doc.styles;normal=styles['Normal'];normal.font.name='Aptos';normal.font.size=Pt(10.0);normal.font.color.rgb=RGBColor(37,51,66)
normal.paragraph_format.space_after=Pt(5.5);normal.paragraph_format.line_spacing=1.14
for sty,size,color,before,after in [('Title',25,NAVY,3,9),('Heading 1',17,NAVY,9,9),('Heading 2',11.4,BLUE,9,5),('Heading 3',10,NAVY,8,4)]:
 s=styles[sty];s.font.name='Aptos Display';s.font.size=Pt(size);s.font.color.rgb=RGBColor.from_string(color[1:]);s.font.bold=True;s.paragraph_format.space_before=Pt(before);s.paragraph_format.space_after=Pt(after)
if 'Caption Plus' not in styles:
 c=styles.add_style('Caption Plus',WD_STYLE_TYPE.PARAGRAPH);c.font.name='Aptos';c.font.size=Pt(8);c.font.italic=True;c.font.color.rgb=RGBColor(103,118,132);c.paragraph_format.space_after=Pt(8)
head=section.header.paragraphs[0];head.text='ANALYSTLAB AFRICA   /   EXPERIENCE LAB   /   WEEK 4';head.style='Caption Plus';head.alignment=WD_ALIGN_PARAGRAPH.RIGHT
footer=section.footer.paragraphs[0];footer.alignment=WD_ALIGN_PARAGRAPH.RIGHT
footer.add_run('Bank of America consumer complaint extract  •  2017–2023   |   ')
field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE');footer._p.append(field)
for r in footer.runs:r.font.size=Pt(7.3);r.font.color.rgb=RGBColor(120,129,138)

def p(txt='',bold_lead=None,style=None):
 x=doc.add_paragraph(style=style)
 if bold_lead and txt.startswith(bold_lead):x.add_run(bold_lead).bold=True;x.add_run(txt[len(bold_lead):])
 else:x.add_run(txt)
 return x

def h(title,level=1):doc.add_heading(title,level)
def shade(cell,fill):tcPr=cell._tc.get_or_add_tcPr();sh=OxmlElement('w:shd');sh.set(qn('w:fill'),fill);tcPr.append(sh)
def tb(rows,headers=None,widths=None,sz=8.6):
 data=([headers] if headers else [])+rows;table=doc.add_table(rows=0,cols=len(data[0]));table.style='Table Grid';table.alignment=WD_TABLE_ALIGNMENT.CENTER;table.autofit=False
 for ri,row in enumerate(data):
  cells=table.add_row().cells
  for ci,x in enumerate(row):
   cells[ci].text=str(x);cells[ci].vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
   if widths:cells[ci].width=Inches(widths[ci])
   if ri==0 and headers:shade(cells[ci],'112D50')
   elif ri%2==0:shade(cells[ci],'EFF4F7')
   for pp in cells[ci].paragraphs:
    pp.paragraph_format.space_after=Pt(0);pp.paragraph_format.space_before=Pt(0);pp.paragraph_format.line_spacing=1.08
    for run in pp.runs:run.font.name='Aptos';run.font.size=Pt(sz);run.font.bold=bool(headers and ri==0);run.font.color.rgb=RGBColor(255,255,255) if headers and ri==0 else RGBColor(34,50,65)
  tr=table.rows[-1]
  if headers and ri==0:tr._tr.get_or_add_trPr().append(OxmlElement('w:tblHeader'))
 doc.add_paragraph().paragraph_format.space_after=Pt(0)
 return table

def chart(file,caption,width=6.55):
 doc.add_picture(str(FIG/file),width=Inches(width));c=doc.add_paragraph(caption,style='Caption Plus');return c

def screenshot(n,caption,width=6.4):doc.add_picture(str(SHOT/f'page-{n}.png'),width=Inches(width));p(caption,style='Caption Plus')
def bullet(txt):p(txt,style='List Bullet')
def page():doc.add_page_break()

def kicker(txt):
 q=doc.add_paragraph();q.paragraph_format.space_after=Pt(7);r=q.add_run(txt.upper());r.bold=True;r.font.color.rgb=RGBColor.from_string(GOLD[1:]);r.font.size=Pt(9)

# Cover
for _ in range(3):p('')
kicker('Data analytics track  /  final evidence-led submission')
doc.add_heading('Consumer Complaint\nTrends & Response\nIntelligence Platform',0)
q=p('What complaint growth, response records and CFPB forwarding data actually show');q.runs[0].font.size=Pt(14);q.runs[0].bold=True;q.runs[0].font.color.rgb=RGBColor(55,110,152)
p('Bank of America consumer complaint extract  |  1 May 2017 – 28 August 2023')
p('Prepared for AnalystLab Africa  |  Experience Lab Internship Programme  |  Week 4')
for _ in range(3):p('')
h('THE CENTRAL STORY',2)
p('Full-year complaint volume rose sharply through 2022, but the recorded response picture is not uniform. A pronounced timeliness dip in 2021 and many still-in-progress complaints in July–August 2023 change how the headline 96.06% should be interpreted. The most actionable product patterns are account management, card transactions, and credit-reporting issues.')
tb([['62,516','Distinct consumer complaint records'],['83.1%','Complaint-volume growth, full-year 2019 to 2022'],['96.06%','Recorded timely Yes among 61,022 eligible Yes/No records'],['1.22 days','Average CFPB receipt-to-forwarding interval']],headers=['VALUE','WHAT IT ACTUALLY MEASURES'],widths=[1.35,5.0],sz=9)
p('Version 2.0  •  Independently recomputed from the original uploaded Excel file; supplied Power BI screenshots are identified as such.')
page()

# executive
kicker('Executive decision brief')
h('The volume trend is clear. The service-response interpretation requires care.')
p('The extract documents a rise from 7,075 complaints in 2019 to 12,953 in 2022: 5,878 additional records, or 83.08%. Four product groups account for 96.89% of that net increase. This supports targeted monitoring, not a claim that complaint *rates* or verified misconduct rose, because no customer/account denominators or investigation outcomes are provided.')
p('The overall timely-response field reads 96.06% Yes, but this hides an 89.02% eligible rate for 2021 and a June 2021 low of 58.35%. At the other end of the history, 1,494 complaints marked In progress have blank timeliness values, 1,450 of them submitted in July–August 2023. Comparing recent months without acknowledging those open records would be misleading.')
h('Six figures to retain',2)
tb([['62,516','Unique complaints; 2017–2023 (partial boundary years)'],['24,814','Checking/savings complaints, 39.69% of total'],['15,109','Managing an account: leading issue, all in checking/savings'],['58,619 / 61,022','Timely Yes / valid Yes+No; 96.06%'],['1,494','Missing timeliness records, all marked In progress'],['49,634','0-day CFPB forwarding records (79.39% of total)']],headers=['VERIFIED COUNT','MEANING'],widths=[1.4,4.95])
h('Management implications',2)
for s in ['Prioritise issue-specific diagnostic reviews where complaint counts concentrate: account management, card purchase disputes, and credit-reporting accuracy.', 'Track recorded timeliness by *submission month and product* rather than relying on one all-period percentage.', 'Monitor in-progress records as a distinct status, and investigate the 623 forwarding intervals longer than 25 days without treating forwarding as company resolution time.']:bullet(s)
p('Evidence standard: each figure in this report is traceable to the accompanying cleaned CSV, independently re-run validation output, and explicit calculation scripts. The four dashboard screenshots came from the uploaded Dashboard.pdf.')
page()

# scope/quality
kicker('01 / source integrity and methods')
h('A trustworthy complaint record comes before a trustworthy chart')
p('Each row is one consumer complaint record, identified by Complaint ID. The 12-field source workbook is the controlling source, and the flat table has no pre-existing relationship model. The supplied CFPB data dictionary defines Date submitted as the date the CFPB received the complaint, and Date received as the date it forwarded the record to the company.')
tb([['Records and key','62,516 rows; 62,516 unique IDs; 0 duplicate IDs; 0 fully duplicated rows'],['Date validation','All date pairs valid; 0 negative forwarding intervals; 1 May 2017–28 Aug 2023'],['Sub-issue blank','10,858 (17.37%); kept missing because not all issues have sub-issues'],['Public response blank','2,175 (3.48%); optional category, kept missing'],['Sub-product blank','7 (0.01%); kept missing'],['Timeliness blank','1,494 (2.39%); all In progress, excluded from Yes/No denominator'],['Categorical cleaning','Trim/control-character checks: 0 source rows required changes'],['New columns','Year, Month, Month Start, Quarter, Forwarding Days']],headers=['DATA-QUALITY CHECK','VERIFIED RESULT'],widths=[1.66,4.7],sz=8.25)
h('What is calculated and what is not',2)
p('Forwarding Days = Date received − Date submitted in calendar days. This records CFPB administrative forwarding, not company response time or resolution. Timely Response % = Yes / (Yes + No), explicitly excluding blank entries. Complaint counts use distinct Complaint ID, equal to row count here because IDs are unique.')
p('No records were removed, blanks were not filled with invented categories, and the source Excel workbook is retained unchanged. Cleaning and all checks are independently reproducible using the included Python standard-library script or Power Query M steps.')
page()

# annual
kicker('02 / demand trend')
h('Complaint volume rose 83.08% from 2019 to 2022')
p('The 2019–2022 comparison uses complete calendar years. Annual complaints increased from 7,075 to 12,953, a net rise of 5,878 records. Year-over-year counts grew 26.39% in 2020, 24.68% in 2021 and 16.18% in 2022. This is sustained growth in recorded complaint volume, not a customer-normalised complaint rate.')
chart('enhanced_annual_volume.png','Figure 1. Complaint totals for all years in the supplied extract; * marks incomplete calendar years.')
tb([['2018','7,872','Full year; 2017 is partial'],['2019','7,075','−10.12% versus 2018'],['2020','8,942','+26.39% versus 2019'],['2021','11,149','+24.68% versus 2020'],['2022','12,953','+16.18% versus 2021']],headers=['YEAR','COUNT','INTERPRETATION'],widths=[1.1,1.25,4.0],sz=8.7)
p('The 2017 data start in May and 2023 stop on 28 August. Therefore annual 2017/2018 and 2022/2023 comparisons must not be presented as like-for-like year-over-year performance. July 2023 is the highest recorded month (1,749), but its status mix needs separate examination on page 9.')
page()

# drivers
kicker('03 / decomposition of growth')
h('Four product lines explain 96.89% of net complaint growth')
p('The 2019–2022 increase is not distributed evenly. Checking/savings (+2,106), credit/prepaid cards (+1,656), credit reporting (+1,231), and money transfer/services (+702) contributed 5,695 of 5,878 net additional complaints. Mortgage volume fell by 56 across the same endpoints.')
chart('enhanced_growth_drivers.png','Figure 2. Difference in yearly complaint counts (2022 minus 2019). Positive and negative components reconcile to +5,878.')
tb([['Checking/savings','+2,106','35.83%'],['Credit/prepaid cards','+1,656','28.17%'],['Credit reporting','+1,231','20.94%'],['Money transfer/services','+702','11.94%'],['All other products (net)','+183','3.11%'],['Total net growth','+5,878','100.00%']],headers=['PRODUCT DRIVER','CHANGE','SHARE OF NET GROWTH'],widths=[3.3,1.25,1.8],sz=8.5)
p('Decision use: investigate these four product families first, but choose specific issues within them rather than interpreting count growth as a proven increase in wrongdoing or a rise in complaint incidence per active account.')
page()

# product/issue
kicker('04 / concentration and taxonomy')
h('Account complaints dominate the portfolio; problems differ by product')
p('Checking/savings (24,814) and credit/prepaid cards (16,197) account for 41,011 complaints, or 65.60% of the extract. The most common issue across all products is Managing an account (15,109). Every one of those records belongs to checking/savings, representing 60.89% of that product’s complaints.')
chart('enhanced_products.png','Figure 3. Product complaints across all recorded dates. Counts are not adjusted for number of customers or accounts.')
h('A product-specific issue hierarchy is more useful than one overall top-ten ranking',2)
tb([['Checking/savings','Managing an account','15,109','60.89%'],['Credit/prepaid card','Problem with a purchase shown on your statement','4,415','27.26%'],['Credit reporting','Incorrect information on your report','4,145','53.76%'],['Mortgage','Trouble during payment process','2,827','42.83%'],['Money transfer/services','Fraud or scam','1,951','56.50%'],['Debt collection','Attempts to collect debt not owed','1,351','49.38%']],headers=['PRODUCT','LEADING REPORTED ISSUE','COUNT','WITHIN PRODUCT'],widths=[1.35,2.9,0.8,1.3],sz=7.7)
p('These are consumer-reported issue labels. For example, a “Fraud or scam” classification describes the consumer allegation, not a verified finding of fraud.')
page()

# subproduct
kicker('05 / drilling below product groups')
h('Within high-volume products, sub-products sharpen the investigation')
p('Product categories can hide materially different customer interactions. Checking accounts alone account for 20,768 records; general-purpose credit/charge cards for 13,404; and credit reporting for 7,340. These sub-product labels support better operational routing than treating each broad product as one uniform workflow.')
tb([[s,f'{v:,}',f'{100*v/A["row_count"]:.2f}%'] for s,v in list(A['subproduct_counts'].items())[:10]],headers=['TOP SUB-PRODUCT','COMPLAINTS','SHARE OF ALL'],widths=[4.0,1.25,1.1],sz=8.2)
h('Most useful drill-downs',2)
for t in ['Checking/savings → Managing an account: 15,109 reported cases; examine the detailed sub-issue mix only where sub-issues are present.', 'Credit/prepaid → Purchase shown on statement: 4,415 cases; review categorised dispute pathways before assuming a cause.', 'Credit reporting → Incorrect information on report: 4,145 cases; track data accuracy complaints and recorded response classifications.', 'Money transfer/services → Fraud or scam: 1,951 cases; validate facts before inferring confirmed fraud or loss.']:bullet(t)
p('The accompanying interactive dashboard lets readers select a product and inspect its issue and sub-product distribution. Missing sub-products (7) and sub-issues (10,858) remain visibly missing rather than being reclassified.')
page()

# timeliness annual
kicker('06 / recorded company timeliness')
h('The 96.06% headline hides substantial variation by year')
p('A total of 58,619 complaints are marked timely Yes, 2,403 No, and 1,494 blank. The correct denominator is 61,022 valid Yes/No records. The overall 96.06% is accurate, but it is not an even trend and should not be interpreted as a resolution or satisfaction rate.')
chart('enhanced_timeliness_by_year.png','Figure 4. Annual percentage of valid Yes/No records marked Yes; 2023 is partial and excludes its in-progress records.')
tb([[str(x['Year']),f"{x['Yes']:,}",f"{x['No']:,}",f"{x['Excluded']:,}",f"{x['Timely_eligible_percent']:.2f}%"] for x in tby],headers=['YEAR','YES','NO','EXCLUDED','ELIGIBLE RATE'],widths=[.85,1.18,1.05,1.3,1.95],sz=8.2)
p('The fall to 89.02% in 2021 is an empirical classification change worth investigating. The dataset does not reveal the company processes or timing behind it, so the report does not assert a cause. Product and month breakdowns are provided for follow-up.')
page()

# 2021 monthly
kicker('07 / timeliness deep dive')
h('The main timeliness exception occurred mid-2021')
p('In June 2021, 389 of 934 complaints were marked No, leaving 545 marked Yes: just 58.35% eligible timeliness. July–October remained below 85% in all four months. The full 2021 year recorded 1,224 No indicators, compared with 62 in 2020 and 567 in 2022.')
chart('enhanced_2021_timeliness.png','Figure 5. Monthly Yes / (Yes + No) in 2021. All 2021 records had a valid Yes or No indicator.')
tb([['June 2021','545 Yes / 389 No','58.35%'],['July 2021','808 Yes / 147 No','84.61%'],['August 2021','704 Yes / 209 No','77.11%'],['September 2021','667 Yes / 154 No','81.24%'],['October 2021','701 Yes / 164 No','81.04%']],headers=['MONTH','ELIGIBLE RECORDS','RECORDED TIMELY RATE'],widths=[1.45,2.7,2.2],sz=8.4)
p('A practical review should first confirm whether the measurement definition, source data capture or operational process changed during this period. The recorded categories alone do not prove poor handling, a legal breach or the reason for the shift.')
page()

# 2023 artifact
kicker('08 / late-period snapshot caveat')
h('The July 2023 complaint spike includes an unusually large in-progress cohort')
p('July 2023 has 1,749 records, 705 more than July 2022 (1,044). However, 863 July complaints (49.34%) were still marked In progress and have no timeliness status. In August 2023, 587 of 717 (81.87%) were in progress, and that month is only observed through 28 August.')
chart('enhanced_2023_inprogress.png','Figure 6. Status composition by submission month in 2023. *August contains records only through 28 August.')
tb([['Jan–Jun 2023','44','2.95% of all 1,494 in-progress records'],['Jul 2023','863','57.76% of all in-progress records'],['Aug 2023','587','39.29% of all in-progress records'],['Jul–Aug combined','1,450','97.05% of all in-progress records']],headers=['SUBMISSION COHORT','IN PROGRESS','SHARE OF IN-PROGRESS TOTAL'],widths=[2.1,1.4,2.85],sz=8.2)
p('Interpretive guardrail: July and August 2023 have 100% Yes among the records with a valid Yes/No indicator, largely because open records are excluded. That is not evidence that every complaint filed in those months received a timely response. Status maturation and the dataset capture cutoff must be considered before judging recent-period timeliness.')
page()

# response
kicker('09 / company response classification')
h('“Closed with explanation” is the most common recorded disposition')
p('Most complaints have an explanation recorded (41,044; 65.65%). Others show monetary relief (14,697; 23.51%) or non-monetary relief (5,273; 8.43%). Another 1,494 were In progress, and 8 are simply recorded Closed. These categories describe the company’s database response classification, not consumer satisfaction or verified resolution quality.')
chart('enhanced_response_types.png','Figure 7. Company response to consumer distribution, as recorded in the source data.')
h('Public-facing response is optional',2)
tb([['Company chose not to provide a public response','60,311','96.47%'],['No public response category recorded (blank)','2,175','3.48%'],['Other explicit public response categories (combined)','30','0.05%']],headers=['PUBLIC RESPONSE CLASSIFICATION','RECORDS','SHARE'],widths=[4.22,1.05,1.1],sz=8.5)
p('The 60,311 explicit “chooses not to provide a public response” records should not be conflated with the 2,175 missing categories. Neither category is evidence that no consumer response was given.')
page()

# forward
kicker('10 / CFPB complaint forwarding')
h('Most complaints were forwarded promptly, but a long tail merits review')
p('The mean CFPB receipt-to-forwarding interval is 1.2249 calendar days, while the median is 0. A total of 49,634 cases (79.39%) have zero-day forwarding; 58,891 (94.20%) fall in the 0–4 day range. However, 623 records are above the dataset’s 99th-percentile nearest-rank threshold of 25 days, reaching a maximum of 275 days.')
chart('enhanced_forwarding_bands.png','Figure 8. Mutually exclusive forwarding interval bands. 0–4 days comprises the first two bars, not just the zero-day bar.')
tb([['Median','0 days'],['Mean','1.22 days'],['99th percentile (nearest rank)','25 days'],['Records > 25 days','623 (1.00%)'],['Maximum','275 days']],headers=['STATISTIC','VALUE'],widths=[4.0,2.35],sz=8.6)
p('The 25-day threshold is an analytical outlier rule, not a regulatory deadline. This stage precedes company handling. The supplied dates do not permit measurement of company response duration or final resolution time.')
page()

# forward product
kicker('11 / differences across products')
h('Forwarding intervals vary by product, with small-group uncertainty')
p('The average forwarding interval ranges from 0.74 days for credit reporting to 2.13 days for student loans. But student loans have only 39 complaint records. Product comparisons should be treated as descriptive, not a diagnosis of company speed or a statistically comparable service standard.')
chart('enhanced_forwarding_by_product.png','Figure 9. Average CFPB forwarding interval by product. Each label includes its source denominator.')
h('Most informative checks for the longest delays',2)
for x in ['Inspect the 30 longest intervals in the accompanying exception table and verify their original received/forwarded dates.', 'Use product, submission month and submission channel filters to identify whether cases cluster in specific source workflows.', 'Maintain separate measures for CFPB forwarding and recorded company timeliness; they are different processes and cannot be substituted.']:bullet(x)
p('No negative intervals, invalid dates or source formatting corrections were needed; the long tail is therefore a valid observed data pattern, although record-level operational reasons are not available.')
page()

# Dashboard screenshots 1+2
kicker('12 / existing Power BI dashboard evidence')
h('The uploaded Power BI PDF covers the four requested analytical pages')
p('These images are reproduced from the user-supplied Power BI dashboard PDF. They are evidence of the existing report layout and are not presented as newly rebuilt Power BI Desktop screenshots. The standalone interactive HTML companion is an independently calculated, working four-view dashboard.')
h('Page 1: Executive Complaint Overview',2)
screenshot(1,'Figure 10. Submitted Dashboard.pdf, page 1: KPI cards, monthly trend, product share and year filter.',width=5.6)
h('Page 2: Product and Issue Analysis',2)
screenshot(2,'Figure 11. Submitted Dashboard.pdf, page 2: ranked products, sub-products, issues and product-versus-issue table.',width=5.6)
page()

# Dashboard screenshots 3+4
kicker('12 / existing Power BI dashboard evidence')
h('Response classification and forwarding dashboards')
h('Page 3: Company Response Analysis',2)
screenshot(3,'Figure 12. Submitted Dashboard.pdf, page 3: timeliness, response types, in-progress and public response.',width=5.6)
h('Page 4: Complaint Timeline Analysis',2)
screenshot(4,'Figure 13. Submitted Dashboard.pdf, page 4: monthly/annual volumes, forwarding intervals and YoY comparisons.',width=5.6)
p('Review note: the PDF’s 0–4-day histogram bin shows 58,891, not the 49,634 zero-day count. Its case table presents 76,575 as “Sum of Forwarding Days,” which should be labelled a summed interval and not a complaint count.')
page()

# recommendations
kicker('13 / evidence to action')
h('Four practical actions follow directly from the observed patterns')
tb([['1 · Focus product reviews','Select checking/savings, credit/prepaid, credit reporting and money transfer/service families. Drill into the leading issue in each product, not raw totals alone.','Product × issue monthly counts; share of top issues'],
['2 · Audit the mid-2021 timeliness dip','Review the Yes/No classification and relevant case-processing records for June–October 2021. Distinguish measurement changes from operations before identifying any cause.','Monthly eligible timeliness %; No counts by product'],
['3 · Keep recent in-progress cases separate','Show Yes, No and In progress together; never classify blanks as No. Revisit recent months only when statuses have matured.','Excluded count and share by submission month'],
['4 · Investigate forwarding outliers','Review 623 cases >25 days and top-30 case IDs. Check date and submission metadata; classify findings as CFPB routing, not company-resolution performance.','Forwarding P50/P99; count above 25 days']],headers=['RECOMMENDATION','FIRST OPERATIONAL STEP','MONITOR'],widths=[1.55,3.58,1.22],sz=8.15)
h('Suggested monitoring cadence',2)
p('At each dataset refresh: run key/duplicate/date/timeliness QA; update annual and monthly views; review product–issue rankings; calculate eligible timeliness plus exclusions; and inspect exceptionally long forwarding intervals. The included README and scripts make each step inspectable. A formal operational schedule depends on the team’s actual update process.')
p('Recommendations call for targeted investigation, not assertions that complaints prove wrongdoing or that recorded response categories establish a satisfactory outcome.')
page()

# Business questions coverage
kicker('14 / assignment coverage')
h('All ten business questions are addressed with explicit boundaries')
tb([['1. Volume trend','2019–2022: +83.08%; 2017/2023 are partial.'],['2. Top products','Checking/savings 24,814; credit/prepaid 16,197.'],['3. Top issues','Managing an account 15,109 overall.'],['4. Product differences','Product–issue counts and within-product shares provided.'],['5. Time to company','CFPB forwarding: mean 1.22d, median 0d; not company response.'],['6. Company response types','Closed with explanation 41,044 is most common.'],['7. Recorded timeliness','58,619 / 61,022 eligible = 96.06%; 1,494 excluded.'],['8. Changed over time','Product growth decomposition and annual/monthly status trends.'],['9. Forecast suitability','Historical monthly series exists; no tested forecast model claimed for this track.'],['10. Accessible dashboard','Existing four-page Power BI PDF and independent interactive HTML companion.']],headers=['BRIEF QUESTION','DATA-SUPPORTED ANSWER'],widths=[2.1,4.25],sz=8.5)
h('Forecasting and AI integration are shared-track objectives, not invented results',2)
p('The monthly series can support a forecasting prototype, but the extract ends mid-2023, boundary periods are incomplete, and complaint composition/status changed. No independent forecast accuracy evaluation is supplied; therefore a forecast is not presented as validated. The cleaned CSV and definitions are integration-ready for statistical, predictive and natural-language interfaces, but completed integration with other tracks cannot be claimed without participant evidence.')
page()

# KPIs
kicker('Appendix A / definitions and DAX reference')
h('The 12 required KPI groups, with calculation basis and interpretive rules')
kpis=[
 ('1 · Total complaints','DISTINCTCOUNT(Complaint ID)','Unique complaint records, not consumers'),
 ('2 · Annual complaint volume','Total complaints grouped by Year','2017 and 2023 partial'),
 ('3 · Monthly complaint volume','Total complaints grouped by Month Start','Chronological monthly series'),
 ('4 · By financial product','Total complaints grouped by Product','Counts are not risk-adjusted'),
 ('5 · By reported issue','Total complaints grouped by Issue','Issue is consumer-reported'),
 ('6 · By sub-product/sub-issue','Total complaints grouped by each','Preserve missing labels'),
 ('7 · Product contribution %','Product complaints ÷ total in filter context','Remove Product filter only for denominator'),
 ('8 · Company response distribution','Count by Company response to consumer','Do not assume satisfaction'),
 ('9 · Timely-response %','Yes ÷ (Yes + No)','Exclude blanks; show eligible count'),
 ('10 · In progress','Count response = In progress','1,494; not classified as No'),
 ('11 · Forwarding mean/median','AVERAGE/MEDIAN(received − submitted)','Calendar days, CFPB forwarding'),
 ('12 · Year-over-year %','(This year − prior year) ÷ prior year','Comparable full years 2019–2022')]
tb([[a,b,c] for a,b,c in kpis],headers=['KPI','CALCULATION','INTERPRETATION'],widths=[1.7,2.35,2.3],sz=7.85)
p('Power BI-ready implementations are saved in 04_Analysis/PowerBI_M_Cleaning.pq and 04_Analysis/KPI_Measures.dax, with a report-setup guide and QA test scripts. Annual, monthly, product and issue KPIs use the same DISTINCTCOUNT measure grouped by their relevant dimension.')
page()

# limitations/handover
kicker('Appendix B / handover, limitations and audit trail')
h('Handover is reproducible; certain activities remain external')
h('What is delivered',2)
for s in ['The original 12-column Excel workbook plus a cleaned 62,516-record CSV and reproducible cleaning script, with no row loss or invented values.', 'Power BI M and DAX files, named measures and page-reconstruction instructions; independent source-versus-dashboard assertions and additional annual/monthly/product breakdowns.', 'A four-view offline interactive HTML dashboard, four screenshots of the uploaded Power BI PDF, source-derived analytical charts and this editable DOCX/PDF report.', 'README, data-quality document, KPI dictionary, findings/recommendation register, revision log, source attribution and presentation materials.']:bullet(s)
h('Native Power BI project caveat',2)
p('The supplied Consumer_Complaint__Intelligence.pbip is a 311-byte manifest pointing to Consumer_Complaint__Intelligence.Report; the referenced report and semantic-model folders were not supplied. A native editable Power BI project therefore cannot be certified or reconstructed from that pointer alone. The included Power Query/DAX files let a reviewer rebuild and validate a native report in Power BI Desktop; the HTML companion is interactive but not a .pbix/.pbip file.')
h('What the source cannot establish',2)
for s in ['Complaint data represent allegations, not confirmed regulatory breaches, individual customer incidence or the total number of financial product accounts.', 'Recorded timely response ≠ satisfactory outcome; CFPB forwarding ≠ company response or resolution time.', 'An individual audio/video presentation, genuine team collaboration evidence and actual mentor feedback-based revisions must be supplied by the responsible participant; draft materials cannot authenticate those activities.']:bullet(s)
p('Provenance: uploaded assignment brief, Consumer_Complaints(1).xlsx, ConsumerComplaints_DataDictionary(1).csv, and Dashboard.pdf. Summary statistics were independently recomputed from the source and tested against the original dashboard figures. See source README, JSON validation log and test scripts.')

doc.core_properties.title='Consumer Complaint Trends and Response Intelligence Platform — Evidence-Led Deep Dive'
doc.core_properties.subject='Week 4 Data Analytics report, Bank of America consumer complaints 2017–2023'
doc.core_properties.author='AnalystLab Africa | Data Analytics Track'
OUT.parent.mkdir(exist_ok=True,parents=True);doc.save(OUT)
print('Created',OUT,'figures',len(list(FIG.glob('enhanced*.png'))))
