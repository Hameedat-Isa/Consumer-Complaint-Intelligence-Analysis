#!/usr/bin/env python3
"""Reproducible standard-library audit and preparation for AnalystLab Week 4.

Run: python 04_Analysis/prepare_and_validate.py --source 08_Source/Consumer_Complaints_original.xlsx --outdir .
Requires Python >=3.9. No modifications to the original workbook. Excel dates are interpreted as
calendar days in the 1900 date system. Counts are of distinct Complaint ID values.
"""
import argparse, collections, csv, datetime as dt, json, re, statistics, zipfile, xml.etree.ElementTree as ET
from pathlib import Path

NS = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
HEADERS = ['Complaint ID', 'Submitted via', 'Date submitted', 'Date received', 'State', 'Product', 'Sub-product', 'Issue', 'Sub-issue', 'Company public response', 'Company response to consumer', 'Timely response?']
DERIVED = ['Year','Month','Month Start','Quarter','Forwarding Days']
MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December']

def iter_excel_rows(path):
    """Stream Data sheet values; supports shared strings and 1900-format Excel dates."""
    with zipfile.ZipFile(path) as z:
        strs = []
        if 'xl/sharedStrings.xml' in z.namelist():
            with z.open('xl/sharedStrings.xml') as f:
                for event, el in ET.iterparse(f,events=('end',)):
                    if el.tag == NS+'si':
                        strs.append(''.join(t.text or '' for t in el.iter(NS+'t')))
                        el.clear()
        with z.open('xl/worksheets/sheet1.xml') as f:
            for event, el in ET.iterparse(f, events=('end',)):
                if el.tag != NS+'row':
                    continue
                row = [''] * 12
                for c in el.findall(NS+'c'):
                    col = re.match(r'([A-Z]+)',c.attrib['r']).group(1)
                    idx = 0
                    for char in col: idx = idx * 26 + ord(char) - 64
                    idx -= 1
                    if idx >= 12: continue
                    v = c.find(NS+'v')
                    if c.attrib.get('t')=='inlineStr':
                        val=''.join(t.text or '' for t in c.iter(NS+'t'))
                    elif v is None: val = ''
                    elif c.attrib.get('t')=='s': val = strs[int(v.text)]
                    else: val = v.text or ''
                    row[idx] = val
                el.clear()
                yield row

def excel_date(x):
    if not x: return None
    try: return (dt.date(1899,12,30)+dt.timedelta(days=int(float(x))))
    except ValueError: return dt.date.fromisoformat(str(x)[:10])

def clean_text(s):
    # Trim printable/category whitespace, strip ASCII control characters; retain meaning/case.
    return ''.join(c for c in str(s or '').strip() if ord(c)>=32 and ord(c)!=127)

def calculate(source,outdir):
    outdir=Path(outdir); (outdir/'03_Data').mkdir(exist_ok=True,parents=True)
    (outdir/'07_Evidence').mkdir(exist_ok=True,parents=True)
    iterator=iter_excel_rows(source)
    header=next(iterator)
    if header != HEADERS: raise RuntimeError(f'Unexpected headers: {header}')
    miss=collections.Counter(); cvals={x:collections.Counter() for x in HEADERS}
    ids=set(); dupids=0; dupfull=0; fullrows=set(); dateerrors=[]; nonmatching=[]; altered=[]
    years=collections.Counter(); months=collections.Counter(); quarters=collections.Counter(); prod=collections.Counter();
    issues=collections.Counter(); subproduct=collections.Counter(); subissue=collections.Counter(); response=collections.Counter(); public=collections.Counter();
    timeliness=collections.Counter(); product_issue=collections.Counter(); prod_annual=collections.Counter(); issue_annual=collections.Counter();
    interval=collections.Counter(); prod_days=collections.defaultdict(list); outliers=[]; biggest=[]; channels=collections.Counter(); state=collections.Counter()
    mindate=maxdate=minforward=maxforward=None; count=0; sumdays=0
    fp=outdir/'03_Data'/'Consumer_Complaints_Cleaned.csv'
    with fp.open('w',newline='',encoding='utf-8-sig') as out:
        w=csv.writer(out);w.writerow(HEADERS+DERIVED)
        for raw in iterator:
            count+=1
            row=[clean_text(x) if i not in (2,3) else x for i,x in enumerate(raw)]
            if row!=raw: altered.append(count+1)
            ident=row[0]
            if ident in ids:dupids+=1
            ids.add(ident)
            tup=tuple(row)
            if tup in fullrows: dupfull+=1
            fullrows.add(tup)
            for j,x in enumerate(row):
                if not x:miss[HEADERS[j]]+=1
                cvals[HEADERS[j]][x]+=1
            try:
                d0=excel_date(row[2]); d1=excel_date(row[3]); days=(d1-d0).days
                if d0 is None or d1 is None: raise ValueError('Null date')
            except Exception as e:
                dateerrors.append({'row':count+1,'error':str(e)}); continue
            if days<0:nonmatching.append({'id':ident,'days':days})
            minforward=days if minforward is None else min(days,minforward)
            maxforward=days if maxforward is None else max(days,maxforward)
            mindate=d0 if mindate is None else min(d0,mindate)
            maxdate=d0 if maxdate is None else max(d0,maxdate)
            yr=d0.year; mon=d0.strftime('%Y-%m');prodname=row[5];issue=row[7];rsp=row[10]
            years[yr]+=1; months[mon]+=1; quarters[f'{yr}-Q{(d0.month-1)//3+1}']+=1
            prod[prodname]+=1; issues[issue]+=1; subproduct[row[6] or '(Not recorded)']+=1;subissue[row[8] or '(Not recorded)']+=1
            response[rsp]+=1; public[row[9] or '(No public response recorded)']+=1
            timeliness[row[11] or '(Not recorded)']+=1
            product_issue[(prodname,issue)]+=1; prod_annual[(yr,prodname)]+=1;issue_annual[(yr,issue)]+=1
            interval[days]+=1;sumdays+=days;prod_days[prodname].append(days)
            channels[row[1]]+=1;state[row[4] or '(Not recorded)']+=1
            if days>=25:
                outliers.append({'Complaint ID':ident,'Date submitted':d0.isoformat(),'Date received':d1.isoformat(),'Product':prodname,'Forwarding Days':days})
            w.writerow([row[0],row[1],d0.isoformat(),d1.isoformat(),*row[4:],yr,MONTHS[d0.month-1],d0.replace(day=1).isoformat(),f'Q{(d0.month-1)//3+1}',days])
    n_yes=timeliness['Yes'];n_no=timeliness['No'];eligible=n_yes+n_no
    all_intervals=[]
    for day,n in interval.items():all_intervals.extend([day]*n)
    all_intervals.sort()
    def percentile(p):
        # nearest-rank
        return all_intervals[max(0,__import__('math').ceil(p*len(all_intervals))-1)]
    if not dateerrors:
        assert count==len(ids)+dupids
        assert n_yes+n_no+timeliness['(Not recorded)']==count
        assert sum(years.values())==count
        assert sum(prod.values())==count
        assert sum(response.values())==count
        assert sum(interval.values())==count
    max10=sorted(outliers,key=lambda r:(-r['Forwarding Days'],r['Complaint ID']))[:30]
    summary={
        'source':'Consumer_Complaints_original.xlsx / Data sheet',
        'row_count':count,'original_columns':len(HEADERS),'distinct_ids':len(ids), 'duplicate_id_rows':dupids,'duplicate_full_rows':dupfull,
        'source_columns':HEADERS,'derived_columns':DERIVED,
        'blank_counts':dict(miss),'categorical_distinct_counts':{k:len(v) for k,v in cvals.items()},
        'category_trim_or_clean_changed_rows':len(altered),'category_changed_row_samples':altered[:20],
        'date_issues':dateerrors[:20], 'date_issue_count':len(dateerrors),
        'negative_forwarding_count':len(nonmatching),'negative_interval_examples':nonmatching[:10],
        'first_submitted_date':str(mindate),'last_submitted_date':str(maxdate),
        'year_counts':dict(sorted(years.items())),'month_counts':dict(sorted(months.items())),
        'quarter_counts':dict(sorted(quarters.items())),'product_counts':dict(prod.most_common()),
        'issue_counts':dict(issues.most_common()),'subproduct_counts':dict(subproduct.most_common()),'subissue_counts':dict(subissue.most_common()),
        'response_counts':dict(response.most_common()),'public_response_counts':dict(public.most_common()),
        'timeliness_counts':dict(timeliness.most_common()),'timeliness_rate_pct':round(100*n_yes/eligible,8), 'eligible_timeliness':eligible,
        'excluded_timeliness':count-eligible, 'in_progress_count':response['In progress'],
        'forwarding_sum_days':sumdays,'forwarding_mean_days':sumdays/count, 'forwarding_median_days':statistics.median(all_intervals),
        'forwarding_min_days':minforward,'forwarding_max_days':maxforward,'forwarding_percentile_95_nearest_rank':percentile(.95),
        'forwarding_percentile_99_nearest_rank':percentile(.99),
        'forwarding_distribution':dict(sorted(interval.items())),
        'forwarding_by_product':{p:{'count':len(vals),'mean_days':sum(vals)/len(vals),'median_days':statistics.median(vals),'max_days':max(vals)} for p,vals in prod_days.items()},
        'product_issue_pairs':[{'Product':p,'Issue':issue,'Complaints':n} for (p,issue),n in product_issue.most_common()],
        'product_year':[{'Year':yr,'Product':p,'Complaints':n} for (yr,p),n in sorted(prod_annual.items())],
        'issue_year':[{'Year':yr,'Issue':issue,'Complaints':n} for (yr,issue),n in sorted(issue_annual.items())],
        'top_longest_forwarding':max10,
        'channels':dict(channels.most_common()),'states':dict(state.most_common()),
        'unmatched_blanks_timeliness':count-eligible-response['In progress'],
        'blank_timeliness_on_inprogress_only': timeliness['(Not recorded)']==response['In progress'] and count-eligible==response['In progress'],
        'year_comparisons': [{'year':y,'count':years[y],'previous':years[y-1], 'yoy_percent':(years[y]/years[y-1]-1)*100} for y in (2019,2020,2021,2022)],
    }
    # Check that every missing timeliness is in progress in a second pass (not just same count).
    bad_blank=0
    with fp.open(encoding='utf-8-sig',newline='') as f:
        for r in csv.DictReader(f):
            if (not r['Timely response?']) != (r['Company response to consumer']=='In progress'):
                bad_blank+=1
    summary['timeliness_inprogress_mismatched_rows']=bad_blank
    summary['blank_timeliness_on_inprogress_only']=bad_blank==0
    with (outdir/'07_Evidence'/'validation_results.json').open('w',encoding='utf-8') as f:json.dump(summary,f,indent=2,ensure_ascii=False)
    def export(filename,headers,rows):
        with (outdir/'03_Data'/filename).open('w',newline='',encoding='utf-8-sig') as f:
            w=csv.writer(f);w.writerow(headers);w.writerows(rows)
    export('Monthly_Complaint_Volume.csv',['Month Start','Complaints'],[(k+'-01',v) for k,v in sorted(months.items())])
    export('Annual_Complaint_Volume.csv',['Year','Complaints','Year-over-year change % (complete years only)'],[(yr,n, round((n/years[yr-1]-1)*100,2) if yr in (2019,2020,2021,2022) else '') for yr,n in sorted(years.items())])
    export('Product_Complaint_Volume.csv',['Product','Complaints','Share %'],[(p,n,round(n/count*100,4)) for p,n in prod.most_common()])
    export('Issue_Complaint_Volume.csv',['Issue','Complaints'],issues.most_common())
    export('Product_Issue_CrossTab.csv',['Product','Issue','Complaints'],[(p,i,n) for (p,i),n in product_issue.most_common()])
    export('Response_Distribution.csv',['Response category','Complaints'],response.most_common())
    export('Forwarding_Interval_Distribution.csv',['Days','Complaints'],sorted(interval.items()))
    export('Top_30_Long_Forwarding_Intervals.csv',['Complaint ID','Date submitted','Date received','Product','Forwarding Days'],[[r[k] for k in ['Complaint ID','Date submitted','Date received','Product','Forwarding Days']] for r in max10])
    print('AUDIT',json.dumps({k:summary[k] for k in ['row_count','distinct_ids','duplicate_id_rows','duplicate_full_rows','blank_counts','first_submitted_date','last_submitted_date','date_issue_count','negative_forwarding_count','timeliness_counts','timeliness_rate_pct','forwarding_mean_days','forwarding_median_days','forwarding_max_days','forwarding_percentile_99_nearest_rank','timeliness_inprogress_mismatched_rows','category_trim_or_clean_changed_rows']},indent=2))
    print('YEARS',summary['year_counts'])
    print('PRODUCTS',summary['product_counts'])
    print('TOP ISSUES',list(summary['issue_counts'].items())[:12])
    print('RESPONSES',summary['response_counts'])
    print('LONG INTERVALS',summary['top_longest_forwarding'][:5])
    return summary

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',default='08_Source/Consumer_Complaints_original.xlsx');p.add_argument('--outdir',default='.'); a=p.parse_args()
    calculate(a.source,a.outdir)
