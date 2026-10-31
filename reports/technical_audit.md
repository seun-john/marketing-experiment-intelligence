# Technical audit

Verification date: 31 October 2026. Environment: Windows, Python 3.12, project-local virtual environment. No public repository, remote push or deployment was performed.

| Major feature | Status | Evidence / scope |
|---|---|---|
| Authentic source acquisition | PASS | Original publisher HTTP CSV; 64,000 rows, 12 columns; SHA-256 in data/provenance.json |
| Dataset validation and preservation | PASS | Schema/domain/outcome checks; 0 missing cells; 6,562 duplicate-looking rows retained |
| Fixed analysis plan | PASS | reports/analysis_plan.md; retrospective, not registered prospectively |
| Experiment integrity | PASS | Allocation/SRM, pairwise baseline SMDs, missingness and design limits recorded |
| SQL analysis | PASS | 12 executable queries; every output reconciled independently against Pandas |
| Primary conversion inference | PASS | Two fixed tests, Holm correction; Newcombe pointwise intervals; explicit denominators |
| Secondary visits/spending inference | PASS | Seven-test Holm family, Welch mean tests, seeded percentile bootstrap |
| Customer segment intelligence | PASS | All seven categorical attributes; sample sizes, pointwise intervals, sparse flags; 14 HC3 joint interactions and Holm adjustment |
| Hypothetical ROI calculator | PASS | Zero audience, invalid inputs and known economics fixture checked; margin applied once |
| Prospective experiment planner | PASS | Known sample-size reference, invalid probabilities, noninteger groups and infinite ratios checked |
| Streamlit workspace | PASS | All eight pages executed with Streamlit AppTest; selected metric/confidence/filter/input state changes checked |
| Desktop rendered application | PASS | Headless Chrome visited every page without Streamlit exceptions; actual screenshots in assets/ |
| Mobile overview | PASS | Actual 390px capture inspected; document width checked against viewport |
| All controls on all mobile devices | UNVERIFIED | No exhaustive device/browser or assistive-technology audit |
| Analytical report and downloads | PASS | Actual aggregate tables, 13 report sections, Markdown/HTML download controls executed; HTML rendered and font checked |
| Academic report typography | PASS | Browser-computed Times New Roman, 16px (=12pt), across report headings, body and tables; report_font_check.json |
| Reproducible analysis | PASS | Pipeline rerun on preserved original bytes; independent csv.DictReader counts match aggregate tables |
| Dependency pins / local launch | PASS | requirements.txt and requirements-lock.txt generated from tested environment; local HTTP/Streamlit run verified |
| Deployment documentation | PASS | DEPLOYMENT.md and start.ps1; code-only cloud launch needs explicit data preparation |
| Public cloud deployment | UNVERIFIED | No live deployment performed; owner's approval required before publication |
| Dataset redistribution licence | UNVERIFIED | No explicit original-data licence established; raw/processed records and database excluded from Git |
| Peak memory on an 8GB machine | UNVERIFIED | Low-memory empirical-support bootstrap implemented; target hardware not profiled |
| Optional uplift ML | NOT IMPLEMENTED | Core inference completed; no modelled individual effects claimed |

## Test evidence

Final pytest run: **36 passed**, 60.47 seconds. See pytest.txt and pytest.xml. Checks include data loading/validation, original treatment mapping, duplicate preservation, exact customer and outcome counts, absolute and relative lifts, zero-event intervals, published Newcombe interval reference, Fisher fallback, skewed spending, Holm corrections, SQL reconciliation, baseline SMD, segment denominators/empty filters, ROI economics, power reference/validation, Plotly unit transforms and full-page application execution.

The first run found a Pandas column-name/accessor collision on the segment page and incorrect hardcoded expected conversion counts in a test fixture. The page now accesses the sparse flag by column key; the corrected conversion expectations were verified against original records and a separate standard-library CSV aggregation. Final results contain no failing pytest checks. Browser checks cover all pages, but do not prove every possible input sequence or WCAG compliance.

## Independent numerical checks

Control: 21,306 assigned, 122 conversions, 2,262 visits, $13,908.33 spending. Men's email: 21,307 assigned, 267 conversions, 3,894 visits, $30,311.69 spending. Women's email: 21,387 assigned, 189 conversions, 3,238 visits, $23,038.11 spending. See independent_counts.json for a separate csv.DictReader computation.

Men's/control conversion effect: +0.6805 percentage points, pointwise 95% CI [0.5014, 0.8641], Holm p=3.0464e-13. Women's/control: +0.3111 points, CI [0.1502, 0.4745], Holm p=.0001571. Men's/women's exploratory difference: +0.3694 points, secondary-family Holm p=.0006155. Spending effects per assigned customer: men's/control $0.7698 (bootstrap CI $0.4793–$1.0524), women's/control $0.4244 ($0.1702–$0.6691). These are historical outcome effects, not measured profit.

SRM p=.90369 under an assumed equal marginal allocation. Maximum absolute pairwise baseline SMD=.0169. None of the 14 exploratory interaction tests has Holm-adjusted p<.05. These diagnostics neither prove the randomisation mechanism nor establish homogeneous effects.

## Remaining limits and actions

The publisher HTTPS certificate failed both Python and Windows verification. Acquisition used its original HTTP endpoint, with no TLS bypass. The stored checksum ensures byte reproducibility but is not independent authentication of an unencrypted download. Source documentation and actual schema agree. Obtain an independently authenticated copy if stronger provenance assurance is required.

The original data do not include assignment code, customer identifiers, delivery/opening logs, unsubscribe outcomes, actual costs or precise campaign dates. Complete recorded outcomes cannot rule out upstream attrition, contamination or interference. Historical effects need contemporary replication. Subgroup intervals are exploratory and unadjusted pointwise intervals; non-significance does not demonstrate equivalence. Scenario CI endpoints ignore uncertainty in cost/margin assumptions and are not profit prediction quantiles.

Before public release: resolve data-hosting/redistribution rights, obtain owner's publishing approval, execute the selected cloud preparation workflow, and profile memory on the target service. Optional future work is a separately validated uplift demonstration. No required local analytical feature remains knowingly broken.
