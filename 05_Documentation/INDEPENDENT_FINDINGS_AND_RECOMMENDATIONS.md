# Independent findings and recommendations

**Study:** Consumer Complaint Trends and Response Intelligence Platform | **Scope:** Bank of America complaints, 1 May 2017–28 August 2023. All findings are independently calculated from the supplied 62,516-row Excel sheet, after retaining every source record. See `07_Evidence/extended_insights.json` and the CSVs in `03_Data` for inspectable counts.

## The story in one paragraph

Recorded complaint volumes grew across complete calendar years, but that increase was concentrated in four products rather than spread evenly across the portfolio. Most complaints carry a valid timely-response indicator marked Yes, yet the 96.06% all-period headline masks a sharp mid-2021 decline. July 2023 is the largest month by count, while almost half that month's complaints are still marked In progress; the open status means its apparent 100% timeliness among eligible cases cannot be interpreted as perfect performance. Finally, most records were forwarded by the CFPB on the date it received them, but a small, long right tail deserves separate operational verification. These records concern consumer reports, not proven misconduct or measured company resolution time.

## Evidence-backed findings

| # | Finding | Exact source evidence | Why this matters |
|---|---|---|---|
| 1 | Complaint volume grew **83.08%** from the full calendar year 2019 to 2022. | 7,075 (2019) → 12,953 (2022), +5,878. | Workload monitoring and analytical prioritisation. |
| 2 | **Four products accounted for 96.89% of net 2019–2022 growth.** | Checking/savings +2,106; credit/prepaid +1,656; credit reporting +1,231; money transfer +702; combined +5,695. | Investigate specific product drivers instead of generalising across the whole portfolio. |
| 3 | Checking/savings and credit/prepaid card complaints represent **65.60%** of all records. | 24,814 (39.69%) and 16,197 (25.91%), combined 41,011. | These are the highest-volume product families, but no active-customer denominator is provided. |
| 4 | **Managing an account** is the most frequently recorded issue. | 15,109 records, all in checking/savings (60.89% of that product). | Account-management issues are a practical first review target. |
| 5 | Different products have distinct leading reported issues. | Credit/prepaid: purchases on statement 4,415; credit reporting: incorrect information 4,145; mortgage: payment trouble 2,827; money transfer: fraud/scam 1,951. | Route issue reviews to relevant subject-matter teams; issue categories describe consumer reports, not validated facts. |
| 6 | The overall **recorded timely Yes rate is 96.06%** among eligible records. | 58,619 Yes ÷ 61,022 valid Yes/No; 2,403 No and 1,494 excluded. | Denominator integrity is essential; blanks are not No. |
| 7 | Recorded timeliness deteriorated conspicuously in **2021**, especially midyear. | 2021: 9,925 Yes / 1,224 No = 89.02%; June 2021: 545 Yes / 389 No = 58.35%. | Requires targeted validation and investigation before any operational explanation is claimed. |
| 8 | The **July 2023 peak** includes a substantial in-progress component. | July volume 1,749; 863 (49.34%) marked In progress. Aug: 587/717 (81.87%) In progress. | Recent eligible-only timeliness rates are subject to strong status-selection bias. |
| 9 | **Closed with explanation** is the most common company response category. | 41,044 of 62,516 records (65.65%); monetary 14,697; nonmonetary 5,273. | Database response classification does not establish consumer satisfaction. |
| 10 | Public response selection is not equivalent to company response. | 60,311 explicitly choose no public-facing response; 2,175 public-response fields blank; 30 other explicit categories. | Do not treat optional/blank public responses as proof of no company handling. |
| 11 | CFPB forwarding was commonly same-calendar-day but had a long tail. | 49,634 (79.39%) zero-day; mean 1.2249 days, median 0, 623 >25 days, max 275. | Isolate exceptional routing intervals without describing them as company resolution delays. |
| 12 | The dataset is incomplete at its boundary years and lacks normalising denominators. | Begins 1 May 2017; ends 28 August 2023; no accounts/customers or resolution dates. | Restrict like-for-like annual YoY to 2019–2022; avoid unsupported performance claims. |

## Actionable recommendations and evidence-to-action plan

1. **Prioritise four product-specific issue reviews.** Start with checking/savings account management, credit/prepaid card purchase disputes, credit-reporting inaccuracies and money-transfer fraud/scam *reports*. Produce a product-by-issue monitoring table for each refresh. Measure: monthly complaint counts and within-product issue shares. Reason: these four groups contribute 96.89% of net full-year 2019–2022 growth.
2. **Validate the recorded-timeliness shift in June–October 2021.** Examine the data dictionary, reporting pipeline or available case-level operational evidence for a definition/status change or case-processing change. Report Yes/No and eligible denominators separately by month and product. Measure: percentage Yes among valid cases plus absolute No counts. Do not assert causation from this extract.
3. **Track open recent cohorts separately.** Put In progress and excluded records beside the eligible timeliness percentage, and avoid interpreting July–August 2023 100% eligible response as universal timely completion. Measure: monthly open share and cohort maturation on later refreshes.
4. **Review CFPB forwarding interval exceptions.** Validate case date pairs and analyse records with >25 days in the supplied exception list, then inspect routing channels and products. Measure: count above 25 days, 99th percentile and case-level longest interval. The threshold is analytical, not legal.

## Evidence and caveats

The dataset records what consumers reported. It does not verify allegations, document satisfactory resolution, provide a regulatory SLA, describe complaint narratives or establish company response duration. Direct calculations and complete source/cleaned files accompany the report. A data-backed forecast is not claimed as validated for the Data Analytics track; the broader project may use this history for a separate evaluated predictive prototype.
