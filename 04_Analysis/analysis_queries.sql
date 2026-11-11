-- Optional SQLite queries; first import 03_Data/Consumer_Complaints_Cleaned.csv
-- as a table named Complaints with source column names preserved (e.g. via SQLite GUI/CLI).
-- CSV dates are ISO YYYY-MM-DD. 'Forwarding Days' is an integer.
-- Python + M + DAX also provide the required analytical scripts.

-- Total complaints (candidate primary key is unique in audited source)
SELECT COUNT(DISTINCT "Complaint ID") AS total_complaints FROM Complaints;

-- Annual complaint volume
SELECT "Year", COUNT(DISTINCT "Complaint ID") AS complaints
FROM Complaints GROUP BY "Year" ORDER BY CAST("Year" AS INTEGER);

-- Monthly complaint volume
SELECT "Month Start", COUNT(DISTINCT "Complaint ID") AS complaints
FROM Complaints GROUP BY "Month Start" ORDER BY "Month Start";

-- Financial product contribution
WITH product_counts AS (
 SELECT "Product", COUNT(DISTINCT "Complaint ID") AS complaints
 FROM Complaints GROUP BY "Product"
)
SELECT "Product", complaints,
 ROUND(100.0 * complaints / (SELECT SUM(complaints) FROM product_counts),2) AS share_pct
FROM product_counts ORDER BY complaints DESC;

-- Top reported issues and product-vs-issue pairs
SELECT "Issue", COUNT(*) AS complaints FROM Complaints
GROUP BY "Issue" ORDER BY complaints DESC LIMIT 10;
SELECT "Product", "Issue", COUNT(*) AS complaints FROM Complaints
GROUP BY "Product", "Issue" ORDER BY complaints DESC;

-- Response timeliness: blanks are excluded from the denominator
SELECT SUM(CASE WHEN "Timely response?"='Yes' THEN 1 ELSE 0 END) AS timely_yes,
 SUM(CASE WHEN "Timely response?"='No' THEN 1 ELSE 0 END) AS timely_no,
 SUM(CASE WHEN "Timely response?" NOT IN ('Yes','No') OR "Timely response?" IS NULL THEN 1 ELSE 0 END) AS excluded,
 ROUND(100.0 * SUM(CASE WHEN "Timely response?"='Yes' THEN 1 ELSE 0 END)
  / NULLIF(SUM(CASE WHEN "Timely response?" IN ('Yes','No') THEN 1 ELSE 0 END),0),2) AS timely_pct
FROM Complaints;

-- Recorded company response categories and in-progress complaints
SELECT "Company response to consumer", COUNT(*) AS complaints
FROM Complaints GROUP BY "Company response to consumer" ORDER BY complaints DESC;

-- CFPB forwarding interval, NOT company response/resolution time
SELECT ROUND(AVG(CAST("Forwarding Days" AS REAL)),2) AS average_days,
 MIN(CAST("Forwarding Days" AS INTEGER)) AS min_days,
 MAX(CAST("Forwarding Days" AS INTEGER)) AS max_days
FROM Complaints;

-- Longest forward intervals; 25 days is the source-wide nearest-rank P99, not a legal deadline
SELECT "Complaint ID", "Date submitted", "Date received", "Product", "Forwarding Days"
FROM Complaints WHERE CAST("Forwarding Days" AS INTEGER) > 25
ORDER BY CAST("Forwarding Days" AS INTEGER) DESC LIMIT 30;
