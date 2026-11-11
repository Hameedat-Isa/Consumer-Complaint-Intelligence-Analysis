# Consumer Complaint Trends and Response Intelligence Platform

**AnalystLab Africa — Experience Lab Internship Programme, Week 4, Data Analytics track**  
**Analysis version:** 2.0 | **Source:** Supplied Bank of America/CFPB complaint extract, 1 May 2017–28 August 2023.

## Start here

1. Read **`01_Report/Consumer_Complaint_Intelligence_Report.pdf`**, the 19-page illustrated, evidence-led final report (or the editable `.docx`). It contains a title page, narrative, full evidence, four screenshots taken from the user-provided Power BI PDF, 12 KPI definitions and evidence-to-action recommendations.
2. Open **`02_Dashboard/Interactive_Complaint_Dashboard.html`** in a modern browser. The four-page dashboard is self-contained, requires no internet, contains all 62,516 validated complaints and recalculates when **Year** or **Product** changes. This is a working interactive **HTML companion**, not a native Power BI document.
3. Review **`05_Documentation/INDEPENDENT_FINDINGS_AND_RECOMMENDATIONS.md`** for the twelve independently computed findings and four specific recommendations, and **`05_Documentation/POWER_BI_REBUILD_GUIDE.md`** for the native Power BI field, M and DAX specifications.

## What the data independently establish

- **62,516** unique complaints, zero duplicate IDs; **0** invalid/negative forwarding intervals.
- **2019–2022:** 7,075 → 12,953 records, up **83.08%**. Checking/savings, credit/prepaid, credit reporting and money transfer/services contributed **96.89%** of net growth.
- **Product concentration:** checking/savings 24,814 (39.69%); credit/prepaid cards 16,197 (25.91%). Top issue: Managing an account 15,109.
- **Recorded timeliness:** 58,619 Yes and 2,403 No; **96.06%** of **61,022** valid Yes/No entries. Another **1,494** In progress records have blank timeliness and are excluded, never recoded No.
- **2021 response-pattern exception:** annual eligible Yes rate **89.02%**; June 2021 **58.35%**.
- **2023 observation caveat:** 863 of 1,749 July complaints (49.34%) were In progress; 587 of 717 August complaints (81.87%) were In progress. Do not treat a high eligible-only rate in these recent cohorts as proof of universally timely response.
- **CFPB forwarding:** average **1.22** calendar days, median **0**, and **623** cases longer than the observed P99 threshold of 25 days. This is **not** company response or resolution time.

**Responsible use:** consumer-reported issues do not prove misconduct, response categories do not prove satisfaction and counts cannot be converted into complaint rates without a relevant customer/account population denominator. The extract ends 28 August 2023, so 2017 and 2023 are partial years.

## Deliverables, mapped to the brief

| Required item | Where to find it |
|---|---|
| Cleaned dataset or reproducible cleaning | `03_Data/Consumer_Complaints_Cleaned.csv`, `04_Analysis/prepare_and_validate.py` and original untouched `08_Source/Consumer_Complaints_original.xlsx` |
| Power BI analytical scripts | `04_Analysis/PowerBI_M_Cleaning.pq`, `PowerBI_Data_Quality_Checks.pq`, `KPI_Measures.dax`; optional SQL `analysis_queries.sql` and reproducible Python `extended_insights.py` |
| KPI definitions/calculations | `05_Documentation/KPI_DICTIONARY.md` and report Appendix A |
| Interactive dashboard | `02_Dashboard/Interactive_Complaint_Dashboard.html` (working HTML); original Power BI PDF and incomplete original `.pbip` pointer retained |
| Five or more business insights | Report chapters 2–11 and `INDEPENDENT_FINDINGS_AND_RECOMMENDATIONS.md` (12 findings) |
| Three or more actionable recommendations | Report chapter 13 and findings register (4 actions) |
| README and data-quality documentation | This file, `DATA_QUALITY_AND_TESTING.md`, validation JSONs, script tests and provenance notes |
| Dashboard screenshots / integration evidence | `07_Evidence/Dashboard_Screenshots`, report pages 14–15, `COLLABORATION_AND_INTEGRATION.md` |
| Individual presentation support | `06_Presentation/` slide deck and narration script; no individual recording has been fabricated |

## Reproduce the entire numerical analysis

Open a terminal in the submission folder. Python 3.9+ standard library is enough for the data pipeline; no third-party Python packages are needed to validate the original 62,516 records.

```bash
python 04_Analysis/prepare_and_validate.py --source 08_Source/Consumer_Complaints_original.xlsx --outdir .
python 04_Analysis/test_reconciliation.py
python 04_Analysis/extended_insights.py
python 04_Analysis/build_interactive_dashboard.py
node 04_Analysis/test_interactive_dashboard.js
```

`prepare_and_validate.py` reads the original Excel worksheet directly from the Office Open XML ZIP, preserves all rows, checks the candidate primary key and dates, and emits a cleaned ISO-date CSV and source audit JSON. `extended_insights.py` re-aggregates the cleaned complaint-level data, asserts major figures, and creates enhanced annual/month/product/response CSVs. The dashboard builder writes a self-contained local HTML. The Node.js test is optional; it verifies the all-years, year filter and product filter views. Reproduce the report visuals with `python 04_Analysis/build_report_enhanced.py` (requires matplotlib and python-docx); conversion of the resulting DOCX to PDF uses LibreOffice or the DOCX toolchain.

## Power BI instructions

See **`05_Documentation/POWER_BI_REBUILD_GUIDE.md`**. The M query works on the *original Excel*, and the DAX measures define the KPI numerator/denominator precisely. Paste each measure separately into a Power BI table named `Complaints`, and compare its KPI cards against `07_Evidence/validation_results.json`. The second Power Query test script creates a quality-check table.

**Power BI file limitation:** the uploaded `Consumer_Complaint__Intelligence.pbip` is a 311-byte manifest that points to a `.Report` folder not included in the uploads. The native report and semantic-model directories are missing, so this package cannot claim to deliver or certify a newly edited `.pbix/.pbip` project. The original four-page PDF is included as screenshot evidence, and the fully working interactive HTML is a separate companion.

## Folder inventory

- `01_Report`: final illustrated editable Word report and PDF.
- `02_Dashboard`: offline interactive HTML; supplied Power BI PDF and uploaded PBIP manifest.
- `03_Data`: complete cleaned CSV plus trend, issue, product, response, timeliness and exception aggregate CSVs.
- `04_Analysis`: source-preserving Python parser, DAX, Power Query M, optional SQL, dashboard builder and tests.
- `05_Documentation`: this README, independent findings, KPI definitions, QA/testing, Power BI rebuild guide, project schedule, source provenance, limitations, integration record and checklist.
- `06_Presentation`: individual presentation slide deck plus narration script; actual recording requires the submitter.
- `07_Evidence`: full validation JSON, detailed insights JSON, screenshots supplied from Dashboard.pdf and fresh analytical figures.
- `08_Source`: original workbook, data dictionary, brief and guide, unmodified.

## Assessment and handover limitations

Actual team collaboration, mentor feedback revisions, repository/social posting and an individually recorded 5–10 minute presentation are personal/external activities. The package supplies structured logs, drafts and speaker notes but cannot authenticate those events. A validated forecast and AI assistant are shared-track integration goals, not invented deliverables for this Data Analytics track.

The assignment brief and data dictionary are the source authority for field meanings. This submission uses only uploaded data, with no outside data or unsupported misconduct claims.
