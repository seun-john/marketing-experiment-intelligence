# Marketing Experiment Intelligence
## 1. Executive Summary
Mens E-Mail: conversion difference 0.681 percentage points (95% CI 0.501 to 0.864); relative lift 118.8%; Holm p=3.0464e-13. Womens E-Mail: conversion difference 0.311 percentage points (95% CI 0.150 to 0.475); relative lift 54.3%; Holm p=0.00015711.
These assignment effects support evaluating campaign economics, rather than assuming either campaign is profitable. Contemporary rollout requires a new validation experiment.
## 2. Background and Business Problem
A retailer must decide whether promotional email produces incremental purchases and which merchandise campaign merits further testing. Observed purchasing alone includes customers who would have purchased without email; a randomised holdout provides the counterfactual comparison.
## 3. Research Questions and Hypotheses
Purchase conversion is the primary outcome. Two-sided campaign/control nulls specify zero risk difference, with family-wise alpha .05 and Holm correction. Direct campaign comparison, visits and spending are secondary. The retrospective analysis plan is recorded separately; no prospective preregistration is claimed.
## 4. Dataset and Experimental Design
Kevin Hillstrom's 20 March 2008 MineThatData challenge describes 64,000 customers purchasing within the prior year. Assignment was approximately one third per group, with two-week follow-up. The source CSV contains 64,000 records and 12 columns. Customer is the documented experimental unit; no customer identifier is supplied. All assignment records are retained. No invented dates, email opens or clicks are used.
## 5. Data Quality and Experiment Integrity
Missing cells: 0. Duplicate-looking full rows: 6562; retained because identical attributes cannot establish duplicate customers. Category, numeric, binary and outcome consistency checks passed. SRM chi-square=0.2025, p=0.90369, assuming equal marginal allocation probabilities. Maximum absolute baseline SMD=0.0169. These diagnostics do not prove correct randomisation. Delivery, opening, noncompliance, contamination, interference, pre-experiment exclusions and follow-up completeness beyond recorded fields cannot be audited. Complete recorded outcomes do not prove absence of earlier attrition.
## 6. Descriptive Analysis
Rates are proportions; spending is historical dollars per assigned customer, including zeros. Spend SD exposes dispersion.
| segment       |   customers |   conversions |   conversion |   visits |    visit |   total_spend |    spend |   spend_sd |
|:--------------|------------:|--------------:|-------------:|---------:|---------:|--------------:|---------:|-----------:|
| No E-Mail     |       21306 |           122 |   0.00572609 |     2262 | 0.106167 |       13908.3 | 0.652789 |    11.5882 |
| Mens E-Mail   |       21307 |           267 |   0.0125311  |     3894 | 0.182757 |       30311.7 | 1.42262  |    17.7542 |
| Womens E-Mail |       21387 |           189 |   0.00883714 |     3238 | 0.1514   |       23038.1 | 1.0772   |    15.1161 |
Zero-spend share: 99.10%; maximum spend: $499.00. Conditional purchasing-customer spending is not the primary spending estimand.
## 7. Campaign Effectiveness
Mens E-Mail: conversion difference 0.681 percentage points (95% CI 0.501 to 0.864); relative lift 118.8%; Holm p=3.0464e-13. Womens E-Mail: conversion difference 0.311 percentage points (95% CI 0.150 to 0.475); relative lift 54.3%; Holm p=0.00015711.
The direct men's versus women's contrast is exploratory. The men’s email conversion advantage is 0.369 percentage points (pointwise 95% CI 0.175–0.566); its secondary-family Holm-adjusted p-value is 0.000615. This comparison provides evidence favouring the men's campaign in this historical population, subject to exploratory status and the two-week horizon. Estimates apply to assignment in this experiment; they do not estimate the effect of reading an email.
## 8. Statistical Hypothesis Testing
| outcome    | treatment     | reference     |     effect |     ci_low |    ci_high |   relative_lift |      p_value |   p_adjusted |
|:-----------|:--------------|:--------------|-----------:|-----------:|-----------:|----------------:|-------------:|-------------:|
| conversion | Mens E-Mail   | No E-Mail     | 0.00680501 | 0.00501434 | 0.00864072 |        1.18842  | 1.52322e-13  | 3.04645e-13  |
| conversion | Womens E-Mail | No E-Mail     | 0.00311106 | 0.00150166 | 0.00474547 |        0.543313 | 0.000157105  | 0.000157105  |
| conversion | Mens E-Mail   | Womens E-Mail | 0.00369395 | 0.00174628 | 0.00566261 |        0.418003 | 0.000205154  | 0.000615461  |
| visit      | Mens E-Mail   | No E-Mail     | 0.0765896  | 0.0699533  | 0.0832267  |        0.721405 | 5.68517e-112 | 3.97962e-111 |
| visit      | Womens E-Mail | No E-Mail     | 0.0452331  | 0.0388941  | 0.0515743  |        0.426055 | 3.1824e-44   | 1.90944e-43  |
| visit      | Mens E-Mail   | Womens E-Mail | 0.0313565  | 0.0242841  | 0.0384277  |        0.207109 | 3.80217e-18  | 1.90108e-17  |
| spend      | Mens E-Mail   | No E-Mail     | 0.769827   | 0.479333   | 1.05244    |        1.17929  | 1.16381e-07  | 4.65526e-07  |
| spend      | Womens E-Mail | No E-Mail     | 0.424412   | 0.170165   | 0.669098   |        0.650152 | 0.0011294    | 0.00225879   |
| spend      | Mens E-Mail   | Womens E-Mail | 0.345415   | 0.0272073  | 0.657886   |        0.32066  | 0.0304687    | 0.0304687    |
Binary differences use Newcombe pointwise intervals and pooled proportion z tests with Fisher fallback for sparse tables. Spending uses Welch inference with seeded 2,000-draw percentile bootstrap intervals. Two primary p-values receive Holm adjustment; the other seven comparisons receive a separate Holm adjustment. Confidence intervals are not simultaneous and may disagree with adjusted significance decisions. P-values measure incompatibility with a specified null under assumptions, not the probability that a null is true. Lack of significance does not establish equivalence.
Overall binary-outcome Pearson p-values: {'conversion': 1.0020031529493264e-12, 'visit': 2.869178384267155e-110}. Approximate positive MDE at 80% power, equal arms of 21,306, control risk 0.5726%, two-sided alpha .025: 0.247 percentage points. This is a planning scenario, not observed-effect power.
## 9. Customer Segment Findings
Fourteen joint additive-scale treatment interaction tests across seven categorical attributes and conversion/spend use HC3 variance and Holm correction. 0 tests have adjusted p<.05. Full results and subgroup denominators/intervals are in interactions.csv and segment tables. Baseline subgroup conversion differences are descriptive associations; treatment effects within a pretreatment subgroup exploit random assignment. Differences in subgroup significance are not evidence of effect heterogeneity. Pointwise subgroup intervals and sparse events limit targeting claims. Confirm segment policies in a held-out experiment.
## 10. Business Implications
Conversion lift must be valued against email costs and contribution economics. Incremental revenue is not profit. The dashboard simulator uses user assumptions; none are observed costs. It multiplies assumed gross value by margin once, without adding spending-based value.
## 11. Recommendations
Retain a no-email holdout in a contemporary replication. Prioritise the men's merchandise campaign in a contemporary replication: it has the larger conversion and spending estimates and the exploratory direct comparison favours it. Confirm that its conservative contribution estimate exceeds implementation costs before scaling. Predefine conversion, decision thresholds, multiplicity control and operational guardrails. Avoid selecting the largest exploratory subgroup lift without independent validation. Collect delivery, opens, costs, unsubscribes and customer identifiers in future studies.
## 12. Limitations
Historical two-week results from prior-year purchasers need not generalise to current customers, channels or long-term customer value. Exact assignment code and intended allocation constraints are unavailable. No observed campaign costs, opens, delivery or calendar timestamps exist. Interference and attrition before the supplied table are unmeasured. Heavy-tailed spending and sparse purchases limit precision; bootstrap intervals have Monte Carlo error. Multiple primary comparisons share a control; Holm controls family-wise error without assuming independence. Exploratory findings require replication.
## 13. Conclusion
The randomised holdout supports intention-to-treat causal estimates subject to design assumptions. Business decisions require effect sizes, uncertainty and cost assumptions together; statistical significance alone cannot establish profitability or present-day performance.
## Sources
Kevin Hillstrom (2008), The MineThatData E-Mail Analytics And Data Mining Challenge. https://blog.minethatdata.com/2008/03/minethatdata-e-mail-analytics-and-data.html (checked 31 October 2026).
TensorFlow Datasets, hillstrom catalogue. https://www.tensorflow.org/datasets/catalog/hillstrom (checked 31 October 2026). Catalogue documentation licence is not assumed to licence the original customer CSV.
