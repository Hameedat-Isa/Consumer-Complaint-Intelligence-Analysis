#!/usr/bin/env python3
"""Create an offline, cross-filtering HTML companion for the Power BI PDF."""
import csv,json,html
from pathlib import Path
root=Path(__file__).resolve().parents[1]
source=root/'03_Data'/'Consumer_Complaints_Cleaned.csv'
columns=['Product','Sub-product','Issue','Sub-issue','Company response to consumer','Company public response']
values=[[] for _ in columns]; lookup=[{} for _ in columns]
records=[];longs=[]
with source.open(encoding='utf-8-sig',newline='') as f:
 for r in csv.DictReader(f):
  idx=[]
  for i,k in enumerate(columns):
   x=r[k] if r[k] else '(Not recorded)'
   if x not in lookup[i]: lookup[i][x]=len(values[i]);values[i].append(x)
   idx.append(lookup[i][x])
  days=int(r['Forwarding Days'])
  records.append([int(r['Year']), (int(r['Year'])-2017)*12+int(r['Month Start'][5:7])-1,*idx, {'Yes':1,'No':0}.get(r['Timely response?'],-1),days])
  if days>25:
   longs.append([r['Complaint ID'],r['Date submitted'],r['Date received'],idx[0],days,int(r['Year'])])
longs.sort(key=lambda r:(-r[4],r[0]))
assert len(records)==62516
D=json.dumps({'v':values,'r':records,'o':longs},ensure_ascii=False,separators=(',',':'))
CSS=r'''
:root{--navy:#0a2648;--blue:#143b66;--aqua:#2d7e90;--gold:#d3a340;--ink:#1c3144;--muted:#617388;--line:#d8e1e7;--bg:#f4f6f8;--card:#fff;--bad:#a23c2c}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,-apple-system,'Segoe UI',sans-serif}
.top{background:linear-gradient(112deg,#0b2544 0%,#194d72 100%);color:white;padding:22px clamp(18px,4vw,64px)}
.top .eyebrow{color:#b7d8dd;letter-spacing:1.8px;font-size:11px;font-weight:700;text-transform:uppercase}.top h1{font-size:clamp(23px,3.1vw,34px);margin:8px 0 3px;line-height:1.16;letter-spacing:-.7px}.top p{color:#d7e4ed;margin:4px 0 0;font-size:13px}
.nav{background:#fff;border-bottom:1px solid var(--line);display:flex;gap:3px;padding:10px clamp(18px,4vw,64px);flex-wrap:wrap;position:sticky;top:0;z-index:5}
.nav button{border:0;background:transparent;color:#344d62;padding:10px 14px;border-radius:8px;font-weight:700;cursor:pointer;font-size:13px}
.nav button.sel{color:#fff;background:var(--navy)}.nav button:hover:not(.sel){background:#eef3f6}
main{max-width:1470px;margin:auto;padding:22px 27px 65px}.filterbar{display:flex;align-items:end;gap:14px;flex-wrap:wrap;margin-bottom:20px}
.filterbar label{display:flex;flex-direction:column;color:var(--muted);font-size:12px;gap:4px;font-weight:700}
select,.reset{border:1px solid #bbcbd6;border-radius:8px;padding:10px 12px;background:white;color:var(--ink);font:inherit;font-size:13px;max-width:420px}
.reset{cursor:pointer;background:#eaf1f5;border-color:#eaf1f5}.tag{font-size:12px;color:var(--muted);padding:0 6px 8px}
section.page{display:none}.page.active{display:block}.lead{margin:0 0 14px;max-width:1040px;color:#40546a;font-size:14px}.section-title{font-size:22px;letter-spacing:-.25px;margin:0 0 5px}
.kpis{display:grid;grid-template-columns:repeat(5,minmax(145px,1fr));gap:13px;margin:16px 0 20px}
.kpi{border:1px solid var(--line);background:#fff;padding:15px 17px;border-radius:11px;box-shadow:0 2px 4px #112f4911;min-height:98px}.kpi b{display:block;font-size:clamp(22px,2vw,29px);line-height:1.3;color:var(--navy);font-variant-numeric:tabular-nums;margin:3px 0}.kpi span{color:var(--muted);font-size:12px}.kpi em{font-size:11px;color:var(--muted);font-style:normal}
.grid{display:grid;grid-template-columns:repeat(12,1fr);gap:16px;margin-bottom:16px}.panel{border:1px solid var(--line);border-radius:12px;background:white;padding:18px;box-shadow:0 2px 5px #122c4610;min-width:0}
.panel h3{font-size:16px;margin:0 0 3px;color:var(--navy)}.panel p.small{color:var(--muted);font-size:12px;margin:0 0 12px}.span8{grid-column:span 8}.span7{grid-column:span 7}.span6{grid-column:span 6}.span5{grid-column:span 5}.span4{grid-column:span 4}.span12{grid-column:span 12}
.bars{display:flex;flex-direction:column;gap:9px;margin-top:11px}.barrow{display:grid;grid-template-columns:minmax(150px,38%) 1fr 68px;gap:9px;align-items:center;font-size:12px}.barrow .lab{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.rail{height:13px;border-radius:3px;background:#eff3f6;overflow:hidden}.fill{height:100%;background:var(--navy);min-width:1px;border-radius:2px}.barrow .num{text-align:right;font-variant-numeric:tabular-nums;color:var(--muted)}
svg{display:block;width:100%;height:auto}.chart-text{font-size:11px;fill:#66798c}.chart-line{stroke:#dae2e8;stroke-width:1}.svg-axis{stroke:#c2cdd7;stroke-width:1}.chart-area{fill:#b5c9d6;opacity:.27}.line{stroke:var(--navy);stroke-width:3;fill:none;stroke-linejoin:round;stroke-linecap:round}.dot{fill:var(--gold);stroke:white;stroke-width:1}
.tablewrap{overflow:auto;max-height:425px}.t{width:100%;border-collapse:collapse;font-size:12px;white-space:nowrap}.t th{text-align:left;background:#eff3f6;padding:9px 10px;position:sticky;top:0;border-bottom:1px solid #c3d2dc;color:#163b57}.t td{padding:7px 10px;border-bottom:1px solid #e8edf1}.t tr:hover{background:#f6f9fa}.t th.right,.t td.right{text-align:right}.t tr.total{background:#eff4f7;font-weight:800}
.donutrow{display:flex;align-items:center;gap:26px;padding:10px 0}.donut{width:165px;height:165px;border-radius:50%;display:grid;place-items:center;flex-shrink:0;background:conic-gradient(var(--navy) 0 var(--pct),#c76745 var(--pct) 100%)}.donut-inner{width:116px;height:116px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;flex-direction:column}.donut-inner b{color:var(--navy);font-size:23px}.donut-inner small{color:var(--muted);font-size:10px}
.legend div{margin:8px 0;color:#3d5264;font-size:13px}.legend i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:9px}
.note{background:#eef3f6;border-left:3px solid var(--aqua);padding:12px 14px;color:#3e5a6e;font-size:12px;margin:17px 0 0}.foot{border-top:1px solid var(--line);margin-top:30px;padding:14px 0;color:#65788a;font-size:12px}
@media(max-width:1050px){.kpis{grid-template-columns:repeat(3,1fr)}.span8,.span7,.span6,.span5,.span4{grid-column:span 12}}@media(max-width:640px){main{padding:15px}.kpis{grid-template-columns:repeat(2,1fr)}.panel{padding:13px}.barrow{grid-template-columns:minmax(90px,38%) 1fr 52px}.nav button{padding:9px 10px;font-size:12px}}
@media print{.top{background:#0a2648!important;print-color-adjust:exact}.nav,.filterbar{display:none}.page{display:block!important;break-after:page}.panel{break-inside:avoid}.kpis{grid-template-columns:repeat(5,1fr)}}
'''
HTML=r'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Consumer Complaint Intelligence | Offline Interactive Dashboard</title><style>__CSS__</style></head><body>
<header class="top"><div class="eyebrow">AnalystLab Africa · Experience Lab · Week 4</div><h1>Consumer Complaint Trends &amp; Response Intelligence</h1><p>Bank of America complaints recorded in the supplied CFPB dataset | 1 May 2017 – 28 August 2023 | Self-contained interactive companion</p></header>
<nav class="nav" aria-label="Report pages"><button class="sel" data-tab="overview">01 &nbsp; Executive overview</button><button data-tab="products">02 &nbsp; Products &amp; issues</button><button data-tab="responses">03 &nbsp; Company responses</button><button data-tab="timeline">04 &nbsp; Complaint timeline</button></nav>
<main><div class="filterbar"><label for="year">Complaint submission year<select id="year"><option value="all">All years</option></select></label><label for="product">Financial product<select id="product"><option value="all">All financial products</option></select></label><button class="reset" id="reset">Clear filters</button><span class="tag" id="filterlabel">All available complaints</span></div>
<section id="overview" class="page active"><h2 class="section-title">Executive Complaint Overview</h2><p class="lead">Complaints became more numerous across the complete-calendar-year period through 2022, with account-related products contributing most of the recorded volume. The dataset measures complaint submissions, not proven violations.</p><div class="kpis" id="ov-kpis"></div><div class="grid"><div class="panel span8"><h3>Monthly complaint trend</h3><p class="small">Chronological monthly complaint counts; 2017 and 2023 are partial years</p><div id="ov-month"></div></div><div class="panel span4"><h3>Complaint distribution by product</h3><p class="small">Share of current filter selection</p><div id="ov-products"></div></div></div></section>
<section id="products" class="page"><h2 class="section-title">Product and Issue Analysis</h2><p class="lead">Complaint types differ sharply by product. Use the filters to isolate a product and inspect its most common issues, sub-products and related issue categories.</p><div class="grid"><div class="panel span6"><h3>Complaints by financial product</h3><p class="small">All available financial product classifications</p><div id="pr-products"></div></div><div class="panel span6"><h3>Top 10 sub-products</h3><p class="small">Blank sub-product values remain shown as not recorded</p><div id="pr-sub"></div></div><div class="panel span6"><h3>Top 10 reported issues</h3><p class="small">Consumer-reported issue categories</p><div id="pr-issues"></div></div><div class="panel span6"><h3>Product-versus-issue comparison</h3><p class="small">Highest-frequency issues; matrix scrolls horizontally if needed</p><div class="tablewrap" id="pr-matrix"></div></div></div></section>
<section id="responses" class="page"><h2 class="section-title">Company Response Analysis</h2><p class="lead">A recorded timely response indicator is distinct from satisfactory complaint resolution. Blanks are excluded from the Yes/No timeliness denominator and reported separately.</p><div class="kpis" id="re-kpis"></div><div class="grid"><div class="panel span5"><h3>Recorded response timeliness</h3><p class="small">Yes divided by Yes + No; excluded records are not treated as No</p><div id="re-donut"></div></div><div class="panel span7"><h3>Company response category distribution</h3><p class="small">Company response to consumer classification</p><div id="re-categories"></div></div><div class="panel span12"><h3>Public response summary</h3><p class="small">An optional public-facing field; blank does not mean the company failed to respond</p><div class="tablewrap" id="re-public"></div></div></div></section>
<section id="timeline" class="page"><h2 class="section-title">Complaint Timeline Analysis</h2><p class="lead">The interval is the calendar-day difference between the CFPB's receipt of the complaint and its forwarding to the company. It is not the company's resolution time.</p><div class="kpis" id="ti-kpis"></div><div class="grid"><div class="panel span7"><h3>Monthly complaint trend</h3><p class="small">Month Start, with date-aware sorting</p><div id="ti-month"></div></div><div class="panel span5"><h3>Annual complaint volume &amp; YoY change</h3><p class="small">YoY shown for complete-year comparisons in 2019–2022 only</p><div class="tablewrap" id="ti-year"></div></div><div class="panel span6"><h3>CFPB complaint-forwarding intervals</h3><p class="small">Calendar-day bins; bins are descriptive, not regulatory deadlines</p><div id="ti-dist"></div></div><div class="panel span6"><h3>Average forwarding interval by product</h3><p class="small">Mean calendar days; low-volume categories require caution</p><div id="ti-prod"></div></div><div class="panel span12"><h3>Unusually long forwarding intervals</h3><p class="small">Records above 25 days (greater than the global 99th percentile); 15 longest matching the filters</p><div class="tablewrap" id="ti-long"></div></div></div></section>
<div class="note">Interpretation: a complaint is a consumer report, not proof of misconduct. “Date submitted” is the CFPB receipt date; “Date received” is the CFPB-to-company forwarding date. A recorded Yes in the timely field is not a resolution-quality measure. Report coverage ends 28 August 2023. The report is a local, offline interactive companion; the supplied .pbip pointer alone is not a complete reopenable Power BI project.</div>
<footer class="foot">Source: supplied Consumer_Complaints.xlsx and ConsumerComplaints_DataDictionary.csv; all charts recompute from validated complaint-level data. Open this HTML file locally; no internet or external libraries required.</footer></main>
<script>
const DATA=__DATA__;
const [P,S,I,SI,R,U]=DATA.v; const D=DATA.r;const O=DATA.o;
const fmt=n=>Number(n||0).toLocaleString('en-US');const pct=n=>`${Number(n||0).toFixed(2)}%`;
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const count=(arr,idx)=>{const m=new Map();for(const x of arr){const k=x[idx];m.set(k,(m.get(k)||0)+1)}return [...m.entries()].sort((a,b)=>b[1]-a[1]);};
const lbl=(arr,k)=>arr[k]||'(Not recorded)';
const avg=a=>a.length?a.reduce((t,x)=>t+x[9],0)/a.length:0;
const median=a=>{if(!a.length)return 0;const vals=a.map(x=>x[9]).sort((a,b)=>a-b);return (vals[(vals.length-1)>>1]+vals[vals.length>>1])/2};
function kpis(items){return items.map(([name,value,foot])=>`<div class="kpi"><span>${esc(name)}</span><b>${esc(value)}</b><em>${esc(foot||'')}</em></div>`).join('')}
function bars(rows, labels, limit=12, suffix='', color='#0a2648'){const arr=rows.slice(0,limit),max=arr.length?arr[0][1]:1;return `<div class="bars">`+arr.map(([k,n])=>`<div class="barrow"><div class="lab" title="${esc(labels(k))}">${esc(labels(k))}</div><div class="rail"><div class="fill" style="width:${Math.max(0,100*n/max)}%;background:${color}"></div></div><div class="num">${Number.isInteger(n)?fmt(n):n.toFixed(2)}${suffix}</div></div>`).join('')+`</div>`}
function table(headers,rows){return `<table class="t"><thead><tr>`+headers.map(h=>`<th>${esc(h)}</th>`).join('')+`</tr></thead><tbody>`+rows.map(a=>`<tr>`+a.map(c=>`<td>${esc(c)}</td>`).join('')+`</tr>`).join('')+`</tbody></table>`}
function line(months){const w=840,h=320,l=44,r=12,t=17,b=38;const max=Math.max(1,...months.map(x=>x[1]))*1.15;const xx=i=>l+(w-l-r)*(i/Math.max(1,months.length-1));const yy=v=>t+(h-t-b)*(1-v/max);const points=months.map((x,i)=>`${xx(i).toFixed(1)},${yy(x[1]).toFixed(1)}`).join(' ');
 const xlabels=months.filter(x=>x[0].endsWith('-01')).map(x=>({d:x[0],i:months.findIndex(y=>y[0]==x[0])}));
 const ticks=[0,.25,.5,.75,1].map(a=>{let y=yy(max*a);return `<line class="chart-line" x1="${l}" y1="${y}" x2="${w-r}" y2="${y}"/><text class="chart-text" x="${l-5}" y="${y+4}" text-anchor="end">${fmt(Math.round(max*a))}</text>`}).join('');
 const labels=xlabels.map(({d,i})=>`<text class="chart-text" x="${xx(i)}" y="${h-14}" text-anchor="middle">${d.slice(0,4)}</text>`).join('');
 const area=`${l},${yy(0)} ${points} ${xx(months.length-1)},${yy(0)}`;
 return `<svg role="img" aria-label="Monthly complaint volume line chart" viewBox="0 0 ${w} ${h}" preserveAspectRatio="xMidYMid meet">${ticks}<polygon class="chart-area" points="${area}"/><polyline class="line" points="${points}"/>${labels}</svg>`}
const years=[2017,2018,2019,2020,2021,2022,2023];
let page='overview';let selYear='all';let selProd='all';
const yearEl=document.getElementById('year'),prodEl=document.getElementById('product');
for(const y of years){yearEl.insertAdjacentHTML('beforeend',`<option value="${y}">${y}</option>`)}
P.forEach((p,i)=>prodEl.insertAdjacentHTML('beforeend',`<option value="${i}">${esc(p)}</option>`));
function getRows(){return D.filter(x=>(selYear==='all'||x[0]===+selYear)&&(selProd==='all'||x[2]===+selProd))}
function months(a){const m=new Map();a.forEach(x=>m.set(x[1],(m.get(x[1])||0)+1));let keys=selYear==='all'?Array.from({length:76},(_,i)=>i+4):Array.from({length:12},(_,i)=>(+selYear-2017)*12+i);if(selYear==='2023')keys=keys.slice(0,8);if(selYear==='2017')keys=keys.slice(4);return keys.map(i=>[`${2017+Math.floor(i/12)}-${String((i%12)+1).padStart(2,'0')}`,m.get(i)||0])}
function render(){let a=getRows(),yes=a.filter(x=>x[8]===1).length,no=a.filter(x=>x[8]===0).length,excluded=a.length-yes-no,rate=yes+no?100*yes/(yes+no):0,progress=a.filter(x=>R[x[6]]==='In progress').length;
 document.getElementById('filterlabel').textContent=`${fmt(a.length)} complaints in current selection`;
 const m=months(a), b=count(a,2);document.getElementById('ov-kpis').innerHTML=kpis([['Total complaints',fmt(a.length),'Distinct complaint IDs'],['Recorded timely rate',pct(rate),`${fmt(yes+no)} valid Yes/No records`],['Timeliness exclusions',fmt(excluded),'Not classified as No'],['Average forwarding',avg(a).toFixed(2)+' days','CFPB forwarding interval'],['Median forwarding',median(a).toFixed(0)+' days','Calendar days']]);
 document.getElementById('ov-month').innerHTML=line(m);document.getElementById('ov-products').innerHTML=bars(b,k=>P[k],9);
 document.getElementById('pr-products').innerHTML=bars(b,k=>P[k],9);
 document.getElementById('pr-sub').innerHTML=bars(count(a,3),k=>S[k],10);
 document.getElementById('pr-issues').innerHTML=bars(count(a,4),k=>I[k],10);
 const issueKeys=count(a,4).slice(0,9).map(x=>x[0]),productKeys=count(a,2).slice(0,6).map(x=>x[0]);const cross=new Map();for(const x of a){const key=x[4]+'_'+x[2];cross.set(key,(cross.get(key)||0)+1)}
 document.getElementById('pr-matrix').innerHTML=table(['Issue',...productKeys.map(x=>P[x])],issueKeys.map(i=>[I[i],...productKeys.map(p=>fmt(cross.get(i+'_'+p)||0))]));
 document.getElementById('re-kpis').innerHTML=kpis([['Timely: Yes',fmt(yes),'Recorded Yes'],['Timely: No',fmt(no),'Recorded No'],['Valid records',fmt(yes+no),'Timeliness denominator'],['In progress',fmt(progress),'Current company response status'],['Excluded',fmt(excluded),'Blank indicator']]);
 document.getElementById('re-donut').innerHTML=`<div class="donutrow"><div class="donut" style="--pct:${rate}%"><div class="donut-inner"><b>${pct(rate)}</b><small>Recorded timely</small></div></div><div class="legend"><div><i style="background:#0a2648"></i>Yes: ${fmt(yes)}</div><div><i style="background:#c76745"></i>No: ${fmt(no)}</div><div>Excluded: ${fmt(excluded)}</div></div></div>`;
 document.getElementById('re-categories').innerHTML=bars(count(a,6),k=>R[k],9);
 document.getElementById('re-public').innerHTML=table(['Public response classification','Complaints'],count(a,7).map(([k,v])=>[U[k],fmt(v)]));
 const maxInterval=a.length?Math.max(...a.map(x=>x[9])):0;const longN=a.filter(x=>x[9]>25).length;
 document.getElementById('ti-kpis').innerHTML=kpis([['Complaints',fmt(a.length),'Selected period'],['Average forwarding',avg(a).toFixed(2)+' days','CFPB receipt → company'],['Median forwarding',median(a).toFixed(0)+' days','CFPB forwarding'],['Longest interval',fmt(maxInterval)+' days','Observed maximum'],['Over 25 days',fmt(longN),'Global P99 reference: 25 days']]);
 document.getElementById('ti-month').innerHTML=line(m);
 const annual=new Map();for(const x of D){if(selProd!=='all'&&x[2]!==+selProd)continue;annual.set(x[0],(annual.get(x[0])||0)+1)}
 document.getElementById('ti-year').innerHTML=table(['Year','Complaints','YoY %'],years.filter(y=>selYear==='all'||y===+selYear).map(y=>[y,fmt(annual.get(y)||0),y>=2019&&y<=2022&&annual.get(y-1)?pct(100*((annual.get(y)||0)/annual.get(y-1)-1)):'n/a*']));
 const cuts=[['0 days',x=>x===0],['1–4 days',x=>x>=1&&x<=4],['5–9 days',x=>x>=5&&x<=9],['10–24 days',x=>x>=10&&x<=24],['25+ days',x=>x>=25]];
 document.getElementById('ti-dist').innerHTML=bars(cuts.map(([name,test])=>[name,a.filter(x=>test(x[9])).length]).sort((a,b)=>b[1]-a[1]),k=>k,5);
 const pday=new Map();for(const x of a){if(!pday.has(x[2]))pday.set(x[2],[0,0]);const d=pday.get(x[2]);d[0]+=x[9];d[1]++}
 document.getElementById('ti-prod').innerHTML=bars([...pday.entries()].map(([k,[s,n]])=>[k,s/n]).sort((a,b)=>b[1]-a[1]),k=>P[k],9,' days','#2d7e90');
 document.getElementById('ti-long').innerHTML=table(['Complaint ID','CFPB received','Forwarded to company','Product','Days'],O.filter(x=>(selYear==='all'||x[5]===+selYear)&&(selProd==='all'||x[3]===+selProd)).slice(0,15).map(x=>[x[0],x[1],x[2],P[x[3]],x[4]]));
}
function activate(p){page=p;document.querySelectorAll('.nav button').forEach(x=>x.classList.toggle('sel',x.dataset.tab===p));document.querySelectorAll('section.page').forEach(x=>x.classList.toggle('active',x.id===p))}
document.querySelectorAll('.nav button').forEach(x=>x.addEventListener('click',()=>activate(x.dataset.tab)));
yearEl.addEventListener('change',()=>{selYear=yearEl.value;render()});prodEl.addEventListener('change',()=>{selProd=prodEl.value;render()});
document.getElementById('reset').addEventListener('click',()=>{selYear='all';selProd='all';yearEl.value='all';prodEl.value='all';render()});
render();
</script></body></html>'''
output=HTML.replace('__CSS__',CSS).replace('__DATA__',D)
p=root/'02_Dashboard'/'Interactive_Complaint_Dashboard.html';p.write_text(output,encoding='utf-8')
print('Created',p,'size',p.stat().st_size,'rows',len(records),'outlier rows',len(longs))
