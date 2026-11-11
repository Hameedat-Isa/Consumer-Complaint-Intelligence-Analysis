# Data-quality assessment and test evidence

**Analyzed source:** `08_Source/Consumer_Complaints_original.xlsx`, sheet `Data`. Original file unchanged. **Grain:** one `Complaint ID` per row. **Audit script:** `04_Analysis/prepare_and_validate.py`; output audit JSON: `07_Evidence/validation_results.json`.

## Inspection results

| Test | Observed | Assessment |
|---|---:|---|
| Rows | 62,516 | Expected source volume |
| Original columns | 12 | Matches source schema |
| Distinct IDs | 62,516 | Candidate primary key holds |
| Duplicate ID rows | 0 | Pass |
| Full row duplicates | 0 | Pass |
| Invalid/blank date pairs | 0 | Pass |
| Negative forwarding intervals | 0 | Pass |
| Submitted-date coverage | 2017-05-01 to 2023-08-28 | Two partial boundary years |
| Minimum / maximum forwarding days | 0 / 275 | Long right tail |
| Category values changed by trim/control-clean | 0 rows | No reclassification needed |

## Null and sparse fields (not silently imputed)

| Field | Blank records | Share | Treatment |
|---|---:|---:|---|
| Sub-issue | 10,858 | 17.37% | Preserve null: sub-issue not available for every issue |
| Company public response | 2,175 | 3.48% | Preserve null: public response is optional |
| Sub-product | 7 | 0.01% | Preserve null: sub-product not always assigned |
| Timely response? | 1,494 | 2.39% | Preserve null and exclude from Yes/No denominator |

All 1,494 missing timeliness indicators correspond to `In progress` response status; there are **zero mismatched rows**. Verified categories: 58,619 `Yes`, 2,403 `No`, and 1,494 blank. Thus 58,619 ÷ 61,022 = **96.06207597%**, displayed **96.06%**. It would be incorrect to treat 1,494 blanks as failures.

## Date interpretation and distribution

The data dictionary states `Date submitted` is the CFPB receipt date and `Date received` is the date the CFPB forwarded the complaint to the company. `Forwarding Days = Date received − Date submitted` (calendar days). It measures neither company response time nor resolution duration. Interval mean = **1.224886** days; median = **0**; total elapsed days = **76,575** (not number of complaints); nearest-rank P99 = **25 days**. Exactly **49,634** were forwarded in 0 days and **58,891** within 0–4 days. **623** exceeded 25 days; the maximum case is 275 days. P99 is an exploratory reference and not a legal or contractual SLA.

## Cleaning process

1. Validate the 12 original headers against the source dictionary.
2. Preserve all 62,516 complaint records and the original workbook, using Complaint ID as text.
3. Check exact ID and full-row uniqueness before any transformation.
4. Parse Excel-date serials using the source's 1900-format date convention; check anomalies and negative intervals.
5. Inspect missing fields and categoricals; strip whitespace/control codes where needed (0 rows affected); retain original category meanings and blanks.
6. Derive Year, Month, Month Start, Quarter, and integer Forwarding Days. Export dates to ISO 8601 in the CSV.
7. Reconcile all KPI totals with dashboard PDF. Write audit JSON and source-derived aggregate CSVs.

## Verification and known risks

`python 04_Analysis/test_reconciliation.py` runs 27 assertions covering headline KPIs and missingness. Checks are read-only with respect to the source. The annual year-over-year table deliberately leaves 2017, 2018 and 2023 without percentages, avoiding comparisons against partial-year baselines. No customer population denominator is supplied, so complaint counts cannot be turned into complaint rates by account/customer. No company resolution timestamp, complaint narrative, complaint substantiation, or verified outcome is supplied. Product-specific sparse classes such as Student loan (39 records) require small-sample caution.

## Power BI reconciliation issue to label clearly

In the source dashboard PDF, the forwarding case table uses `Sum of Forwarding Days` and a total of 76,575. This is the sum of intervals across all complaints, not a count or response-time KPI. Display each case's forwarding days as **Do not summarize** and avoid an unlabeled sum total.

## Extended independent audit: status coherence and temporal risk

After the original workbook was reprocessed and the existing 27 assertions passed, the cleaned complaint-level CSV was re-aggregated by `04_Analysis/extended_insights.py`. It asserts all 62,516 rows reconcile, validates the 58,619/2,403/1,494 Yes/No/blank split and confirms every blank timeliness value belongs to a 2023 submission (and to an In progress status via the original audit). The extra script writes `Timeliness_by_Year.csv`, `Timeliness_by_Month.csv`, `Product_Timeliness.csv`, `Complaint_Growth_Drivers_2019_2022.csv`, `Subissue_Complaint_Volume.csv`, `Response_Year.csv` and `Product_Issue_Top_30.csv`.

- **Mid-2021 classification shift:** June 2021 contains 545 timely Yes and 389 No records (58.35% Yes among 934 valid entries). The annual 2021 eligible rate is 89.02%. This is a genuine observed distribution shift, but the source does not identify why it happened. **Analytical risk: high if only the overall 96.06% is reported.** Mitigation: show recorded timeliness by month and product, with denominators.
- **July–August 2023 status-selection risk:** 863 of July's 1,749 complaints and 587 of August's 717 are In progress, corresponding to blank timeliness. They account for 1,450 of all 1,494 exclusions (97.05%). **Analytical risk: high for recent-cohort percentages.** Mitigation: show excluded counts and wait for a later independently captured snapshot before making performance comparisons; no refresh/current capture is supplied.
- **Long forwarding intervals:** 623 records exceed the dataset-wide 25-day nearest-rank P99, with a maximum of 275 days. **Analytical risk: medium** if falsely called company response time or compared to a fabricated legal standard. Mitigation: inspect source date records individually and keep CFPB forwarding separate from company timeliness.
- **Partial-year volume comparison:** 2017 and 2023 are incomplete. **Analytical risk: high** if compared to full years without accounting for exposure time. Mitigation: compare complete 2019–2022 full years, state the date coverage and flag August 2023 as partial.

## Independent reproducibility test sequence

```bash
python 04_Analysis/prepare_and_validate.py --source 08_Source/Consumer_Complaints_original.xlsx --outdir .
python 04_Analysis/test_reconciliation.py
python 04_Analysis/extended_insights.py
node 04_Analysis/test_interactive_dashboard.js
```

**Tests observed in this submission:** 27 source/dashboard reconciliation assertions passed; the extended-slice assertions passed; and the offline dashboard smoke tests passed for all data (62,516, 96.06%), year 2022 (12,953) and checking/savings product (24,814). The native Power BI M/DAX files were authored but have not been executed inside Power BI Desktop; the included Power Query `Data_Quality_Checks` query enables local retesting when Power BI is available.
