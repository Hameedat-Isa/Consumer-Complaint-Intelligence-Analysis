# Dashboard evidence, coverage and improvement audit

**Reviewed:** `02_Dashboard/Submitted_PowerBI_Dashboard.pdf` (4 pages) and `02_Dashboard/Consumer_Complaint__Intelligence.pbip` (manifest only). Dashboard screenshots are in `07_Evidence/Dashboard_Screenshots/` and embedded in the narrative report.

| Page | Required visuals / coverage | Evidence |
|---|---|---|
| 1. Executive Complaint Overview | Total complaints; chronological monthly trend; product distribution; recorded timely rate; average forwarding | PDF page 1. Values reconcile: 62,516; 96.06%; 1.22 days. |
| 2. Product and Issue Analysis | Product volumes; top sub-products; top issues; product-versus-issue matrix | PDF page 2. Product and issue counts reconcile. Matrix initially scrolled toward long-tail issues in screenshot. |
| 3. Company Response Analysis | Recorded company response categories; valid Yes/No distribution; In progress and excluded counts; optional public response categories | PDF page 3. 1,494 in-progress and 1,494 exclusions are correctly separate measures. |
| 4. Complaint Timeline Analysis | Monthly and annual trend; forwarding distribution; average by product; longest intervals; YoY | PDF page 4. 5-day bin of 0–4 days = 58,891. Year comparison blanks at boundary years reflect incomplete periods. |

## Improvements identified without misrepresenting source work

1. **Native project missing dependencies:** The .pbip manifest points to `Consumer_Complaint__Intelligence.Report` but the corresponding report folder and semantic model were not uploaded. The PBIP is preserved, but cannot be opened as a complete editable Power BI project from this package. User must supply those directories or an editable .pbix if original native report editing is needed.
2. **Label forwarding sums correctly:** Source PDF page 4 shows `Sum of Forwarding Days = 76,575`. This is a total of calendar-day intervals, not a complaint count. Set row-level field to *Do not summarize*; avoid an unlabeled grand total.
3. **Improve matrix first view:** On page 2 the product–issue matrix is scrolled near low-frequency issues. Display highest-frequency issues first; add tooltips or a supporting table for long text labels.
4. **Clarify first histogram bin:** 58,891 is the number of records in the **0–4 days** bin, not the zero-day count (49,634). Label the axis in intervals.
5. **Keep explicit caveats:** Recorded timely classification is not satisfaction or resolution. Do not call the CFPB forwarding interval company resolution time.

## Offline companion

`02_Dashboard/Interactive_Complaint_Dashboard.html` is a standalone interactive four-page report with year and product slicers, responsive charts, a product–issue matrix, response metrics and long-interval case details. It is built directly from 62,516 validated complaint-level rows and requires no internet. It is **not** a native PBIX/PBIP substitute for editing in Power BI Desktop.

## Validation path

Rebuild via Python and run 27 assertions with `test_reconciliation.py`, then compare all four page totals against the uploaded screenshots. Original screenshots are evidence of the provided Power BI dashboard; they do not show newly built Power BI edits.
