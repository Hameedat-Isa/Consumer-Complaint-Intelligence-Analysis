# Power BI Desktop rebuild and validation guide

**Purpose:** Deliver the required Power BI analytical logic for a native four-page report, using Power Query M and DAX. The uploaded `.pbip` is only a 311-byte project manifest; the `.Report` folder and semantic model files needed to open/edit its existing report were not supplied. This guide does not claim that a tested native `.pbix` was generated in the current environment. The functioning interactive HTML file is a separate, non-Power-BI companion.

## 1. Import and clean the source in Power Query

1. Open Power BI Desktop (Windows) and choose **Get data → Excel workbook**. Select `08_Source/Consumer_Complaints_original.xlsx` (or the original uploaded workbook), and the worksheet `Data`. Select **Transform Data**, not direct Load.
2. Alternatively, choose **Blank Query → Advanced Editor** and paste the entire `04_Analysis/PowerBI_M_Cleaning.pq` query. Change `SourcePath` at its top to the real absolute path where the original workbook is saved. Rename the loaded query **Complaints**. Load it.
3. Confirm there are 62,516 rows, 12 original fields plus Year, Month, Month Start, Quarter, Forwarding Days, Forwarding Band and Forwarding Band Sort. Set Forwarding Band to **Sort by column → Forwarding Band Sort**.
4. To audit data quality in Power BI, add a second **Blank Query** named **Data_Quality_Checks**, paste `04_Analysis/PowerBI_Data_Quality_Checks.pq`, and load it. All 11 expectations should report PASS for the unfiltered source. Never delete the 1,494 blank-timeliness rows.

## 2. Create reusable DAX measures

In the **Modeling** tab choose **New measure** and paste **one measure at a time** from `04_Analysis/KPI_Measures.dax`. Set `%` measures as percentages with 2 decimal places and forwarding measures with a **days** suffix. Before creating visuals, validate cards with all filters cleared:

| Check | Expected |
|---|---:|
| Total Complaints | 62,516 |
| Timely Yes / Timely No | 58,619 / 2,403 |
| Valid Timeliness Records | 61,022 |
| Recorded Timely Response % | 96.06% |
| Excluded Timeliness Records | 1,494 |
| In Progress | 1,494 |
| Average Forwarding Days | 1.22 |
| Median Forwarding Days | 0 |
| Same Day Forwarded | 49,634 |
| Forwarding More Than 25 Days | 623 |

## 3. Build the four pages specified in the brief

| Page | Visual | Fields / measure |
|---|---|---|
| **1 Executive Complaint Overview** | KPI cards | Total Complaints; Recorded Timely Response %; Average Forwarding Days; Valid Timeliness Records; Excluded Timeliness Records |
| | Line chart | Axis Month Start; Values Total Complaints (chronological date axis) |
| | Product distribution | Product + Total Complaints / Product Share % |
| | Year slicer | Year |
| **2 Product and Issue Analysis** | Bar charts | Product and Total Complaints; Sub-product and Total Complaints (Top 10); Issue and Total Complaints (Top 10) |
| | Matrix | Rows Issue; Columns Product; Values Total Complaints, sorted by most frequent issues |
| | Product slicer | Product |
| **3 Company Response Analysis** | Response bar chart | Company response to consumer; Total Complaints |
| | Timely donut | Timely response?; Total Complaints; visual filter **Yes or No only** |
| | KPI cards | In Progress; Excluded Timeliness Records; Valid Timeliness Records |
| | Public response table | Company public response; Total Complaints; retain visible blank category |
| **4 Complaint Timeline Analysis** | Line and annual bar charts | Month Start / Year; Total Complaints |
| | Interval distribution | Forwarding Band ordered by Forwarding Band Sort; Total Complaints |
| | Forwarding by product | Product; Average Forwarding Days |
| | Long interval detail table | Complaint ID; Date submitted; Date received; Product; Forwarding Days. Filter >25, sort descending, **Do not summarize** the row-level days field |
| | YoY summary table | Year; Total Complaints; Previous Full Year Complaints; Full Year YoY % (2019–2022 only) |

Add slicers for Year and Product where relevant. Display all-data references only with filters cleared. Include tooltip definitions: `Date submitted` = CFPB receipt; `Date received` = forwarded to company; forwarding duration is not company response/resolution time. Retain source missingness, do not turn null into No.

## 4. Reconciling and stress-testing the report

Use `07_Evidence/validation_results.json`, `07_Evidence/extended_insights.json` and the small aggregate CSVs to check page-level visuals. Check the March 2021 (1,098), July 2023 (1,749) and 2022 annual (12,953) trend points. For a product filter select Checking/savings: 24,814 rows with all years. Confirm total across product bars equals 62,516. Check `0 days` forwarding = 49,634 and `0–4 days` combined = 58,891, not interchangeable. Confirm the 2021 eligible timely rate ≈89.02%, July 2023 in-progress count 863, and the sum of forwarding-day intervals is 76,575 (this sum is **not** a complaint count).

A native PBIP/.pbix file can only be certified after Power BI Desktop opens and validates the complete report and model. If the original `.Report` and semantic-model folders are later supplied, replace the missing artifacts and inspect the original file rather than claiming this standalone manifest contains them.
