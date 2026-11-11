#!/usr/bin/env python3
"""Regression tests reconciling the supplied dashboard PDF with raw data-derived metrics."""
import json
from pathlib import Path
S=json.loads((Path(__file__).resolve().parents[1]/'07_Evidence'/'validation_results.json').read_text())
checks={
 'row count':(S['row_count'],62516),
 'distinct complaint IDs':(S['distinct_ids'],62516),
 'duplicate ID rows':(S['duplicate_id_rows'],0),
 'complete duplicates':(S['duplicate_full_rows'],0),
 'blank sub issues':(S['blank_counts']['Sub-issue'],10858),
 'blank public responses':(S['blank_counts']['Company public response'],2175),
 'blank subproducts':(S['blank_counts']['Sub-product'],7),
 'valid timeliness denominator':(S['eligible_timeliness'],61022),
 'timely Yes':(S['timeliness_counts']['Yes'],58619),
 'timely No':(S['timeliness_counts']['No'],2403),
 'excluded timeliness':(S['excluded_timeliness'],1494),
 'in progress':(S['in_progress_count'],1494),
 'in-progress/timeliness pairing':(S['timeliness_inprogress_mismatched_rows'],0),
 'forwarding sum days':(S['forwarding_sum_days'],76575),
 'forwarding maximum':(S['forwarding_max_days'],275),
 'negative intervals':(S['negative_forwarding_count'],0),
 '2018 volume':(S['year_counts']['2018'],7872),
 '2022 volume':(S['year_counts']['2022'],12953),
 'checking/savings':(S['product_counts']['Checking or savings account'],24814),
 'credit card/prepaid':(S['product_counts']['Credit card or prepaid card'],16197),
 'managing account issue':(S['issue_counts']['Managing an account'],15109),
 'closed with explanation':(S['response_counts']['Closed with explanation'],41044),
}
for name,(actual,expected) in checks.items():
 assert actual==expected, f'FAIL {name}: {actual} != {expected}'
 print('PASS',name,actual)
assert round(S['timeliness_rate_pct'],2)==96.06
assert round(S['forwarding_mean_days'],2)==1.22
assert S['forwarding_median_days']==0
assert S['date_issue_count']==0
assert S['category_trim_or_clean_changed_rows']==0
print(f'PASS all {len(checks)+5} test assertions')
