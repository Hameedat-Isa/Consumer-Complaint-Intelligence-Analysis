# Week 4 Data Analytics submission checklist

## Verified technical artifacts included

- [x] Original, untouched 62,516-record Excel workbook and 12-field source dictionary.
- [x] Cleaned full complaint-level CSV preserving all rows and blanks; derived Year, Month, Month Start, Quarter, Forwarding Days.
- [x] Source-preserving reproducible Python cleaning/validation script; 27 checks passed against submitted PDF/dashboard reference figures.
- [x] Extended independent analysis (12 findings), monthly timeliness slices, growth attribution and status-cohort calculations.
- [x] Power BI Power Query M cleaning query, Power Query QA test table and DAX measure definitions.
- [x] KPI dictionary with the brief’s 12 required KPI groups and calculations.
- [x] Working, self-contained four-view HTML interactive dashboard; tested all-data/year/product filters.
- [x] Supplied four-page Power BI dashboard PDF and its four screenshots, identified as original user-provided evidence.
- [x] 19-page revised narrative report with title page, charts, findings, cautions and actionable recommendations (PDF and editable DOCX).
- [x] Four targeted evidence-based recommendations.
- [x] README, data-quality report, traceable audit JSON, provenance, Power BI rebuild instructions and project/integration documentation.
- [x] 10-slide presentation and individual narration script, about 7–8 minutes when read at a reasonable pace.
- [x] Log of substantive revisions after the user’s actual follow-up feedback.

## Still requires participant or original Power BI source assets

- [ ] **Native editable Power BI report:** the 311-byte uploaded `.pbip` points to a missing `.Report` directory and semantic model. The PDF and working HTML are included; the package does not certify a rebuilt `.pbix`.
- [ ] **Actual individual recorded presentation:** must be recorded by the participant; scripts and slides are supplied.
- [ ] **Evidence of genuine team collaboration and integration with other tracks:** documents describe integration-ready interfaces but cannot invent work performed by other people.
- [ ] **Verified mentor feedback-based changes:** no mentor feedback was supplied. Revisions based on the user’s follow-up are documented.
- [ ] **GitHub, LinkedIn and X posting:** drafts are available, but external publishing is not claimed.

### High-impact technical caveats

Do not recode blank `Timely response?` to No. Do not label CFPB forwarding time as company resolution time. Complaint allegations do not prove misconduct. 2017 and 2023 are partial calendar years; 2023 recent-month eligible timeliness is affected by still-in-progress records.
