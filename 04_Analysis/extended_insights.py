#!/usr/bin/env python3
"""Independent, fully reproducible complaint-level analysis for AnalystLab Africa.
Requires only Python 3.9+ standard library. Input: 03_Data/Consumer_Complaints_Cleaned.csv
Output: five detailed aggregate CSV files and 07_Evidence/extended_insights.json.
This script never edits the uploaded workbook. Run from any working directory.
"""
import csv, json, collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'03_Data'/'Consumer_Complaints_Cleaned.csv'
OUT=ROOT/'03_Data'
AUDIT=ROOT/'07_Evidence'/'validation_results.json'
C=collections.Counter
annual=C(); month=C(); product_year=C(); product=C(); issue=C(); subissue=C(); product_issue=C(); response=C(); response_year=C(); response_product=C(); status_year=C(); status_month=C(); status_product=C(); forwarded=C(); product_days=collections.defaultdict(list); month_product=C()
for d in csv.DictReader(SRC.open(encoding='utf-8-sig',newline='')):
    y=int(d['Year']); m=int(d['Date submitted'][5:7]); p=d['Product']; i=d['Issue']; t=d['Timely response?'] or '(blank)'; response_name=d['Company response to consumer']; days=int(d['Forwarding Days'])
    annual[y]+=1; month[y,m]+=1; product_year[y,p]+=1;product[p]+=1;issue[i]+=1;subissue[d['Sub-issue'] or '(Not recorded)']+=1;product_issue[p,i]+=1;response[response_name]+=1;response_year[y,response_name]+=1;response_product[p,response_name]+=1;status_year[y,t]+=1;status_month[y,m,t]+=1;status_product[p,t]+=1;forwarded[days]+=1;product_days[p].append(days); month_product[y,m,p]+=1

def write_csv(name,cols,rows):
    with (OUT/name).open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f);w.writerow(cols);w.writerows(rows)

n=sum(annual.values());audit=json.loads(AUDIT.read_text())
assert n == audit['row_count'] == 62516
assert sum(status_year[y,'Yes'] for y in annual)==58619
assert sum(status_year[y,'No'] for y in annual)==2403
assert sum(status_year[y,'(blank)'] for y in annual)==1494
assert sum(forwarded.values())==n
assert sum(x for (y,m,t),x in status_month.items() if t=='(blank)' and y!=2023)==0
assert sum(status_month[y,m,'(blank)'] for y in annual for m in range(1,13))==1494
write_csv('Timeliness_by_Year.csv',['Year','Complaints','Yes','No','Excluded_Blank','Timely_Percent_Eligible'],[
    [y,annual[y],status_year[y,'Yes'],status_year[y,'No'],status_year[y,'(blank)'],f'{100*status_year[y,"Yes"]/(status_year[y,"Yes"]+status_year[y,"No"]):.4f}'] for y in sorted(annual)])
write_csv('Timeliness_by_Month.csv',['Year','Month','Complaints','Yes','No','Excluded_Blank','Timely_Percent_Eligible'],[
    [y,f'{m:02d}',month[y,m],status_month[y,m,'Yes'],status_month[y,m,'No'],status_month[y,m,'(blank)'],f'{100*status_month[y,m,"Yes"]/(status_month[y,m,"Yes"]+status_month[y,m,"No"]):.4f}' if status_month[y,m,'Yes']+status_month[y,m,'No'] else ''] for (y,m) in sorted(month)])
write_csv('Complaint_Growth_Drivers_2019_2022.csv',['Product','2019','2022','Change','Share_of_Net_Growth_Percent'],[
    [p,product_year[2019,p],product_year[2022,p],product_year[2022,p]-product_year[2019,p],f'{100*(product_year[2022,p]-product_year[2019,p])/(annual[2022]-annual[2019]):.4f}']
    for p,_ in sorted(product.items(),key=lambda kv:product_year[2022,kv[0]]-product_year[2019,kv[0]],reverse=True)])
write_csv('Product_Timeliness.csv',['Product','Complaints','Yes','No','Excluded_Blank','Timely_Percent_Eligible'],[
    [p,total,status_product[p,'Yes'],status_product[p,'No'],status_product[p,'(blank)'],f'{100*status_product[p,"Yes"]/(status_product[p,"Yes"]+status_product[p,"No"]):.4f}'] for p,total in product.most_common()])
write_csv('Subissue_Complaint_Volume.csv',['Sub-issue','Complaints'],[[k,v] for k,v in subissue.most_common()])
write_csv('Response_Year.csv',['Year','Response','Complaints'],[[y,r,response_year[y,r]] for y in sorted(annual) for r,_ in response.most_common()])
write_csv('Product_Issue_Top_30.csv',['Product','Issue','Complaints','Share_of_Product_Percent'],[[p,i,num,f'{100*num/product[p]:.4f}'] for (p,i),num in product_issue.most_common(30)])
net=annual[2022]-annual[2019]
results={
 'source_rows':n,
 'full_year_2019_to_2022':{'2019':annual[2019],'2022':annual[2022],'absolute_growth':net,'growth_percent':100*net/annual[2019]},
 '2019_2022_top_drivers':[{'Product':p,'2019':product_year[2019,p],'2022':product_year[2022,p],'Change':product_year[2022,p]-product_year[2019,p],'Share_of_net_growth_percent':100*(product_year[2022,p]-product_year[2019,p])/net} for p,_ in sorted(product.items(),key=lambda kv:product_year[2022,kv[0]]-product_year[2019,kv[0]],reverse=True)],
 'product_issue_top20':[{'Product':p,'Issue':i,'Count':num,'Share_of_product_percent':100*num/product[p]} for (p,i),num in product_issue.most_common(20)],
 'timeliness_by_year':[{'Year':y,'Total':annual[y],'Yes':status_year[y,'Yes'],'No':status_year[y,'No'],'Excluded':status_year[y,'(blank)'],'Timely_eligible_percent':100*status_year[y,'Yes']/(status_year[y,'Yes']+status_year[y,'No'])} for y in sorted(annual)],
 '2021_months':[{'Month':m,'Total':month[2021,m],'Yes':status_month[2021,m,'Yes'],'No':status_month[2021,m,'No'],'Timely_eligible_percent':100*status_month[2021,m,'Yes']/(status_month[2021,m,'Yes']+status_month[2021,m,'No'])} for m in range(1,13)],
 '2023_months':[{'Month':m,'Total':month[2023,m],'Yes':status_month[2023,m,'Yes'],'No':status_month[2023,m,'No'],'Excluded':status_month[2023,m,'(blank)'],'Excluded_share_percent':100*status_month[2023,m,'(blank)']/month[2023,m]} for m in range(1,9)],
 '2023_july':{'Total':month[2023,7],'In_progress':status_month[2023,7,'(blank)'],'2022_july_complaints':month[2022,7], 'pct_in_progress':100*status_month[2023,7,'(blank)']/month[2023,7]},
 '2023_august':{'Total':month[2023,8],'In_progress':status_month[2023,8,'(blank)'],'partial_month_through':'2023-08-28'},
 'forwarding':{'zero':forwarded[0], 'one_to_four':sum(n for d,n in forwarded.items() if 1<=d<=4), 'five_to_nine':sum(n for d,n in forwarded.items() if 5<=d<=9), 'ten_to_twenty_four':sum(n for d,n in forwarded.items() if 10<=d<=24),'twenty_five_plus':sum(n for d,n in forwarded.items() if d>=25),'above_25':sum(n for d,n in forwarded.items() if d>25)},
 'product_timeliness':[{'Product':p,'Total':tot,'Yes':status_product[p,'Yes'],'No':status_product[p,'No'],'Excluded':status_product[p,'(blank)'],'Rate_pct':100*status_product[p,'Yes']/(status_product[p,'Yes']+status_product[p,'No'])} for p,tot in product.most_common()],
 'complaint_response_distribution':dict(response),
}
assert results['2023_july']['In_progress']==863
assert results['2023_august']['In_progress']==587
assert abs(results['full_year_2019_to_2022']['growth_percent']-83.08127)<.01
(ROOT/'07_Evidence'/'extended_insights.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print('PASS additional reconciliation | growth',net,'| July 2023 in progress',results['2023_july']['In_progress'],'| records',n)
