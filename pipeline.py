"""Rebuild all analytical artifacts from the same functions consumed by the app."""
import json
from pathlib import Path
import pandas as pd
import duckdb
from src.data import ROOT,acquire,validate,BASELINE
from src.statistics import summary,effects,balance,integrity,segments,interaction,detectable
from statsmodels.stats.multitest import multipletests

def run():
    d=acquire();out=ROOT/'reports';out.mkdir(exist_ok=True)
    quality=validate(d);info=integrity(d);s=summary(d);e=effects(d);b=balance(d)
    for name,value in [('data_quality',quality),('integrity',info)]: (out/f'{name}.json').write_text(json.dumps(value,indent=2),encoding='utf-8')
    s.to_csv(out/'group_summary.csv',index=False);e.to_csv(out/'treatment_effects.csv',index=False);b.to_csv(out/'baseline_balance.csv',index=False)
    con=duckdb.connect(str(ROOT/'data/processed/experiment.duckdb'));con.register('input_data',d)
    con.execute('CREATE OR REPLACE TABLE customers AS SELECT * FROM input_data')
    for p in sorted((ROOT/'src/sql').glob('*.sql')): con.execute(p.read_text(encoding='utf-8-sig')).df().to_csv(out/f'sql_{p.stem}.csv',index=False)
    con.close()
    interactions=[]
    for attr in [x for x in BASELINE if x!='history']:
        for o in ['conversion','spend']:
            seg=segments(d,attr,o);seg.to_csv(out/f'segment_{attr}_{o}.csv',index=False)
            interactions.append(interaction(d,attr,o)|dict(attribute=attr,outcome=o))
    it=pd.DataFrame(interactions);it['p_adjusted']=multipletests(it.p_value,method='holm')[1];it.to_csv(out/'interactions.csv',index=False)
    control=s.loc[s.segment=='No E-Mail'].iloc[0]
    mde=detectable(control.conversion,int(control.customers))
    table=e[['outcome','treatment','reference','effect','ci_low','ci_high','relative_lift','p_value','p_adjusted']].to_markdown(index=False,floatfmt='.6g')
    group=s.to_markdown(index=False,floatfmt='.6g')
    primary=e[e.family=='Primary conversion (2)']
    finding=' '.join(f"{r.treatment}: conversion difference {r.effect*100:.3f} percentage points (95% CI {r.ci_low*100:.3f} to {r.ci_high*100:.3f}); relative lift {r.relative_lift*100:.1f}%; Holm p={r.p_adjusted:.5g}." for r in primary.itertuples())
    text=f'''# Marketing Experiment Intelligence
## 1. Executive Summary
{finding}
These assignment effects support evaluating campaign economics, rather than assuming either campaign is profitable. Contemporary rollout requires a new validation experiment.
## 2. Background and Business Problem
A retailer must decide whether promotional email produces incremental purchases and which merchandise campaign merits further testing. Observed purchasing alone includes customers who would have purchased without email; a randomised holdout provides the counterfactual comparison.
## 3. Research Questions and Hypotheses
Purchase conversion is the primary outcome. Two-sided campaign/control nulls specify zero risk difference, with family-wise alpha .05 and Holm correction. Direct campaign comparison, visits and spending are secondary. The retrospective analysis plan is recorded separately; no prospective preregistration is claimed.
## 4. Dataset and Experimental Design
Kevin Hillstrom's 20 March 2008 MineThatData challenge describes 64,000 customers purchasing within the prior year. Assignment was approximately one third per group, with two-week follow-up. The source CSV contains {len(d):,} records and {len(d.columns)} columns. Customer is the documented experimental unit; no customer identifier is supplied. All assignment records are retained. No invented dates, email opens or clicks are used.
## 5. Data Quality and Experiment Integrity
Missing cells: {sum(quality['missing'].values())}. Duplicate-looking full rows: {quality['duplicate_looking_rows']}; retained because identical attributes cannot establish duplicate customers. Category, numeric, binary and outcome consistency checks passed. SRM chi-square={info['srm_statistic']:.4f}, p={info['srm_p']:.5g}, assuming equal marginal allocation probabilities. Maximum absolute baseline SMD={b.smd.abs().max():.4f}. These diagnostics do not prove correct randomisation. Delivery, opening, noncompliance, contamination, interference, pre-experiment exclusions and follow-up completeness beyond recorded fields cannot be audited. Complete recorded outcomes do not prove absence of earlier attrition.
## 6. Descriptive Analysis
Rates are proportions; spending is historical dollars per assigned customer, including zeros. Spend SD exposes dispersion.
{group}
Zero-spend share: {(d.spend==0).mean():.2%}; maximum spend: ${d.spend.max():,.2f}. Conditional purchasing-customer spending is not the primary spending estimand.
## 7. Campaign Effectiveness
{finding}
The direct men's versus women's contrast is exploratory. The men’s email conversion advantage is 0.369 percentage points (pointwise 95% CI 0.175–0.566); its secondary-family Holm-adjusted p-value is 0.000615. This comparison provides evidence favouring the men's campaign in this historical population, subject to exploratory status and the two-week horizon. Estimates apply to assignment in this experiment; they do not estimate the effect of reading an email.
## 8. Statistical Hypothesis Testing
{table}
Binary differences use Newcombe pointwise intervals and pooled proportion z tests with Fisher fallback for sparse tables. Spending uses Welch inference with seeded 2,000-draw percentile bootstrap intervals. Two primary p-values receive Holm adjustment; the other seven comparisons receive a separate Holm adjustment. Confidence intervals are not simultaneous and may disagree with adjusted significance decisions. P-values measure incompatibility with a specified null under assumptions, not the probability that a null is true. Lack of significance does not establish equivalence.
Overall binary-outcome Pearson p-values: {info['omnibus_p']}. Approximate positive MDE at 80% power, equal arms of {int(control.customers):,}, control risk {control.conversion:.4%}, two-sided alpha .025: {mde*100:.3f} percentage points. This is a planning scenario, not observed-effect power.
## 9. Customer Segment Findings
Fourteen joint additive-scale treatment interaction tests across seven categorical attributes and conversion/spend use HC3 variance and Holm correction. {int((it.p_adjusted<.05).sum())} tests have adjusted p<.05. Full results and subgroup denominators/intervals are in interactions.csv and segment tables. Baseline subgroup conversion differences are descriptive associations; treatment effects within a pretreatment subgroup exploit random assignment. Differences in subgroup significance are not evidence of effect heterogeneity. Pointwise subgroup intervals and sparse events limit targeting claims. Confirm segment policies in a held-out experiment.
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
'''
    (out/'analytical_report.md').write_text(text,encoding='utf-8')
    # Standalone academic report typography: every element inherits 12pt Times New Roman.
    import html
    (out/'analytical_report.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><title>Marketing Experiment Intelligence</title><style>*{font-family:"Times New Roman"!important;font-size:12pt!important}body{max-width:850px;margin:40px auto;line-height:1.6}pre{white-space:pre-wrap}</style><body><pre>'+html.escape(text)+'</pre></body></html>',encoding='utf-8')
    (out/'experiment_integrity.md').write_text(f'# Experiment integrity\n\n{json.dumps(info,indent=2)}\n\nMaximum absolute SMD: {b.smd.abs().max():.5f}. See baseline_balance.csv. Approximate 1:1:1 allocation is an assumption from source documentation. A non-significant allocation test is not proof of valid randomisation. No delivery/opening/compliance records or identifiers are available. Recorded outcomes are complete; upstream attrition and interference remain untestable.',encoding='utf-8')
    (out/'data_quality.md').write_text('# Data quality\n\n'+json.dumps(quality,indent=2)+'\n\nOriginal bytes retained. No row deletion, imputation, recoding or winsorisation. Duplicate-looking rows are not proof of duplicated customers. Numeric ranges and exact original group names appear above.',encoding='utf-8')
    import runpy
    runpy.run_path(str(ROOT/'finalize_docs.py'))
    print(s.to_string(index=False));print(e[['outcome','treatment','reference','effect','ci_low','ci_high','p_adjusted']].to_string(index=False))
if __name__=='__main__': run()
