# KPI dictionary and calculation specification

**Counting unit:** `DISTINCTCOUNT(Complaint ID)`. **Primary time axis:** CFPB receipt date `Date submitted`. **Filter convention:** year/product filters apply to current cohort unless a denominator specifies otherwise.

| Required KPI | Exact definition | Input fields | Validated reference |
|---|---|---|---|
| Total complaints | Distinct Complaint ID count | Complaint ID | 62,516 |
| Annual complaint volume | Distinct complaint IDs grouped by Year derived from Date submitted | Complaint ID, Date submitted / Year | 2019=7,075; 2022=12,953 |
| Monthly complaint volume | Distinct complaint IDs grouped by Month Start derived from Date submitted | Complaint ID, Date submitted / Month Start | July 2023=1,749 |
| Complaints by financial product | Distinct complaint IDs grouped by Product | Product, Complaint ID | Checking/savings=24,814 |
| Complaints by reported issue | Distinct complaint IDs grouped by Issue | Issue, Complaint ID | Managing an account=15,109 |
| Complaints by sub-product / sub-issue | Distinct complaint IDs by Sub-product or Sub-issue; show blanks as Not recorded | Sub-product, Sub-issue, Complaint ID | No records dropped |
| Product share percentage | Product count / total complaints with Product filter removed; retain other active filters | Product, Complaint ID | Checking/savings=39.69% |
| Company response category distribution | Distinct complaint ID count grouped by Company response to consumer; optionally present separate public response table | Company response to consumer, Company public response | Closed with explanation=41,044 |
| Timely response percentage | Count Yes / (Count Yes + Count No), times 100; exclude missing and report excluded count | Timely response? | 58,619/(58,619+2,403)=96.06%; excluded 1,494 |
| In-progress complaint count | Distinct complaint IDs where Company response to consumer = In progress | Company response to consumer | 1,494 |
| Average and median CFPB forwarding interval | Average and median of integer calendar days Date received − Date submitted, not resolution days | Date submitted, Date received, Forwarding Days | 1.22-day mean; zero-day median |
| Year-over-year changes | (Current full year − previous full year) / previous full year ×100, for 2019–2022 only | Year, Complaint ID | 2020 +26.39%; 2021 +24.68%; 2022 +16.18% |

**Missing timeliness protocol:** 1,494 blank timeliness values belong to In progress records. Exclude those from `Yes/(Yes+No)`; display excluded counts alongside the percentage.

**Forwarding definition:** Despite its label, `Date received` means the date the **company** received the complaint from the CFPB; the earlier `Date submitted` refers to when the **CFPB** received it. Difference is CFPB forwarding interval, not the company's response or resolution time.

**Incomplete periods:** 2017 has only May–December and 2023 January–August; no Year-over-year comparisons against partial years. DAX source: `04_Analysis/KPI_Measures.dax`.
