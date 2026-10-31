from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from src.data import ROOT,load,validate,GROUPS,BASELINE
from src.statistics import summary,compare,segments,interaction,planning
from src.simulations import scenario
from src.visualisation import finish,forest,COLORS
st.set_page_config(page_title='Marketing Experiment Intelligence',page_icon=':material/analytics:',layout='wide')
st.markdown('''<style>.block-container{padding-top:4rem;max-width:1500px}h1{letter-spacing:-.035em}div[data-testid="stMetric"]{background:white;border:1px solid #D7DFEA;padding:20px;border-radius:10px}section[data-testid="stSidebar"]{border-right:1px solid #D7DFEA}.eyebrow{color:#1E40AF;letter-spacing:.13em;font-size:.75rem;font-weight:700}.stDownloadButton button{width:100%}</style>''',unsafe_allow_html=True)
PAGES=['Executive overview','Experiment design & quality','Campaign performance','Statistical testing lab','Customer segment intelligence','Marketing ROI simulator','Research & recommendations','Power & sample size']
st.sidebar.markdown('## Experiment Intelligence')
st.sidebar.caption('MARKETING ANALYTICS WORKSPACE')
page=st.sidebar.radio('Workspace',PAGES,label_visibility='collapsed')
st.sidebar.divider();st.sidebar.markdown('**Hillstrom · 2008**');st.sidebar.caption('Randomised assignment · 2-week follow-up\n\nHistorical evidence, not a current campaign.')
@st.cache_data
def inputs():
    return load(),pd.read_csv(ROOT/'reports/treatment_effects.csv'),pd.read_csv(ROOT/'reports/group_summary.csv')
try: d,e,s=inputs()
except FileNotFoundError:
    st.error('Source data or analysis artifacts are missing. Run: python pipeline.py');st.stop()
st.markdown('<div class="eyebrow">MARKETING EXPERIMENT INTELLIGENCE</div>',unsafe_allow_html=True)
st.title(page)
st.caption('A/B testing, campaign effectiveness and business decision analytics')
def chart(f): st.plotly_chart(f,width='stretch')
def metric_selector(key): return st.selectbox('Outcome',['conversion','visit','spend'],format_func=lambda x:{'conversion':'Purchase conversion','visit':'Website visits','spend':'Spending per assigned customer'}[x],key=key)
def group_chart(metric):
    t=s.copy();t['display']=t[metric]*(1 if metric=='spend' else 100)
    return finish(px.bar(t,x='segment',y='display',color='segment',color_discrete_sequence=COLORS,text_auto='.3f',hover_data=['customers']),f'{metric.title()} by assigned group','Dollars / customer' if metric=='spend' else 'Rate (%)')
def download(table,name): st.download_button('Download '+name,table.to_csv(index=False),name+'.csv','text/csv')
if page==PAGES[0]:
    st.info('Decision focus: establish incremental purchasing, then evaluate campaign economics with explicit cost assumptions.')
    cols=st.columns(5)
    for c,label,value in zip(cols,['Assigned customers','Experiment groups','Conversion rate','Visit rate','Spend / customer'],[f'{len(d):,}','3',f'{d.conversion.mean():.2%}',f'{d.visit.mean():.2%}',f'${d.spend.mean():.2f}']): c.metric(label,value)
    st.caption('Descriptive metrics · all assigned customers, including customers with zero outcomes.')
    a,b=st.columns([1,1]);
    with a: chart(group_chart('conversion'))
    with b: chart(forest(e[e.outcome=='conversion'],'conversion'))
    st.subheader('Primary evidence · fixed 5% family-wise significance level')
    for r in e[e.family=='Primary conversion (2)'].itertuples():
        st.write(f'**{r.treatment} vs control:** {r.effect*100:+.3f} percentage points; 95% CI [{r.ci_low*100:.3f}, {r.ci_high*100:.3f}]; relative lift {r.relative_lift:.1%}; Holm-adjusted p={r.p_adjusted:.4g}.')
    st.success('Recommendation: retain a randomised holdout in a contemporary replication and use conservative contribution assumptions before scaling. This historical experiment does not establish current profitability.')
    st.dataframe(s,width='stretch',hide_index=True)
elif page==PAGES[1]:
    st.write('Individual customers were randomly assigned to merchandise email or no email. Primary outcome: two-week purchase conversion. Visits and mean spending are secondary. Assignment effects do not measure the effect of opening an email.')
    chart(finish(px.bar(s,x='segment',y='customers',color='segment',color_discrete_sequence=COLORS,text='customers'),'Experimental allocation','Assigned customers'))
    info=json.loads((ROOT/'reports/integrity.json').read_text());q=validate(d)
    st.metric('Sample ratio mismatch p-value',f"{info['srm_p']:.4f}")
    st.caption('Chi-square goodness-of-fit against approximate 1:1:1. Intended exact constraints are unknown; a large p-value does not validate the assignment mechanism.')
    bal=pd.read_csv(ROOT/'reports/baseline_balance.csv');bal['comparison']=bal.treatment+' vs '+bal.reference
    chart(finish(px.scatter(bal,x='smd',y='feature',color='comparison'),'Pretreatment balance · standardised differences'))
    st.json(q);st.warning('No customer identifier, delivery logs, opening records or upstream attrition records are supplied. Duplicate-looking rows are retained. Complete recorded outcomes do not rule out unrecorded attrition or contamination.')
    with st.expander('Fixed statistical analysis plan'): st.markdown((ROOT/'reports/analysis_plan.md').read_text(encoding='utf-8-sig'))
elif page==PAGES[2]:
    metric=metric_selector('performance');chart(group_chart(metric));t=e[e.outcome==metric]
    chart(forest(t,metric));chart(forest(t,metric,True))
    if metric=='spend':
        st.caption('Relative spending lift is a point estimate; relative spending intervals are not estimated. Absolute mean-difference intervals use the empirical bootstrap.')
        dd=d[d.spend>0]
        chart(finish(px.histogram(dd,x='spend',color='segment',barmode='overlay',opacity=.5,nbins=50,color_discrete_sequence=COLORS),'Positive spending distribution · zero outcomes excluded from this chart only','Customers'))
        st.write(f'Zero spending: {(d.spend==0).mean():.2%} of assigned customers. Mean analysis includes all zeros.')
    st.dataframe(t,hide_index=True,width='stretch');download(t,'campaign_effects')
elif page==PAGES[3]:
    metric=metric_selector('lab');t=e[e.outcome==metric].reset_index(drop=True)
    choice=st.selectbox('Comparison',range(3),format_func=lambda i:t.iloc[i].treatment+' vs '+t.iloc[i].reference)
    conf=st.slider('Exploratory confidence level',.80,.99,.95,.01);view=st.radio('Interpretation',['Business','Technical'],horizontal=True)
    fixed=t.iloc[choice];r=compare(d.loc[d.segment==fixed.treatment,metric],d.loc[d.segment==fixed.reference,metric],metric,confidence=conf)
    st.write('**H0:** assigned-group outcome means are equal. **H1:** they differ (two-sided).')
    st.write(r['method']);cols=st.columns(3);cols[0].metric('Test statistic',f"{r['statistic']:.4f}");cols[1].metric('Unadjusted p',f"{r['p_value']:.5g}");cols[2].metric('Fixed-family Holm p',f'{fixed.p_adjusted:.5g}')
    unit='dollars / assigned customer' if metric=='spend' else 'percentage points';scale=1 if metric=='spend' else 100
    st.write(f"Effect: **{r['effect']*scale:+.4f} {unit}**; {conf:.0%} pointwise CI [{r['ci_low']*scale:.4f}, {r['ci_high']*scale:.4f}]. Denominators: {r['n_treatment']:,} and {r['n_reference']:,}.")
    st.info(f"Fixed reference decision at alpha .05: {'Reject zero-effect null' if fixed.p_adjusted<.05 else 'Insufficient evidence to reject zero-effect null'}. Family: {fixed.family}. Confidence slider does not alter this decision or multiplicity plan.")
    if view=='Business': st.write('Magnitude and interval width inform decisions alongside costs. A non-significant result does not establish no effect; a significant result does not establish profitability.')
    else: st.write('Independent customer outcomes, original random assignment and comparable follow-up are assumed. Interference is unmeasured. Intervals are pointwise, not multiplicity-adjusted; p-values are not probabilities that H0 is true.')
    st.dataframe(t,hide_index=True,width='stretch')
elif page==PAGES[4]:
    attr=st.selectbox('Pretreatment customer attribute',[x for x in BASELINE if x!='history']);metric=st.selectbox('Segment outcome',['conversion','spend'])
    full=pd.read_csv(ROOT/f'reports/segment_{attr}_{metric}.csv');values=st.multiselect('Segment values',sorted(full.segment_value.astype(str).unique()),default=sorted(full.segment_value.astype(str).unique()))
    t=full[full.segment_value.astype(str).isin(values)].copy()
    st.warning('Exploratory, pointwise intervals. Baseline differences are associations. Comparing subgroup p-values does not test treatment heterogeneity. Confirm targeting policies in a fresh experiment.')
    it=pd.read_csv(ROOT/'reports/interactions.csv');row=it[(it.attribute==attr)&(it.outcome==metric)].iloc[0]
    st.write(f'Joint HC3 interaction test: p={row.p_value:.5g}; Holm p={row.p_adjusted:.5g} across 14 exploratory interaction tests. Additive outcome scale.')
    if t.empty: st.info('Choose at least one segment value. No records selected.')
    else:
        t['reference']='No E-Mail · '+t.segment_value.astype(str);chart(forest(t,metric));st.dataframe(t,hide_index=True,width='stretch')
        if t['sparse'].any(): st.warning('Sparse groups: fewer than 100 assigned customers or fewer than 10 binary events in at least one arm. Interpret intervals cautiously.')
        filtered=d[d[attr].astype(str).isin(values)];st.dataframe(filtered.groupby([attr,'segment'],observed=True).agg(assigned=('conversion','size'),baseline_or_observed_conversion=('conversion','mean'),spend=('spend','mean')).reset_index(),hide_index=True)
        download(t,'segment_effects')
elif page==PAGES[5]:
    st.warning('Hypothetical economics. Effect estimates come from 2008; costs, audience, gross value and margin are assumptions. CI endpoint scenarios are not profit forecast quantiles.')
    campaign=st.selectbox('Campaign',GROUPS[1:]);a,b,c=st.columns(3)
    audience=a.number_input('Audience size',min_value=0,value=100000,step=1000);cost=b.number_input('Cost per email ($)',min_value=0.,value=.02,step=.01);fixedcost=c.number_input('Operational costs ($)',min_value=0.,value=500.)
    value=a.number_input('Gross value per incremental conversion ($)',min_value=0.,value=100.);margin=b.slider('Contribution margin',0.,1.,.4,.01)
    r=e[(e.outcome=='conversion')&(e.treatment==campaign)&(e.reference=='No E-Mail')].iloc[0]
    t=scenario(r.effect,r.ci_low,r.ci_high,audience,cost,margin,value,fixedcost)
    st.caption('Net contribution = incremental conversions × assumed gross value × margin − audience × email cost − operational costs. Spending lift is not added.')
    chart(finish(px.bar(t,x='scenario',y='net_contribution',color='scenario',color_discrete_sequence=COLORS,text_auto='.2f'),'Decision scenarios','Hypothetical net contribution ($)'));st.dataframe(t,hide_index=True,width='stretch');download(t,'hypothetical_scenarios')
elif page==PAGES[6]:
    report=(ROOT/'reports/analytical_report.md').read_text(encoding='utf-8');st.download_button('Download analytical report',report,'analytical_report.md','text/markdown');st.download_button('Download formatted HTML report',(ROOT/'reports/analytical_report.html').read_bytes(),'analytical_report.html','text/html');download(e,'treatment_effects');st.markdown(report)
elif page==PAGES[7]:
    st.info('Prospective planning tool. Independent-proportion normal approximation; Bonferroni correction over campaign/control comparisons. Does not calculate observed-effect post hoc power.')
    a,b=st.columns(2);baseline=a.number_input('Baseline conversion probability',.0001,.9999,.01,format='%.4f');mde=b.number_input('Minimum detectable absolute effect (probability)',.0001,.9999,.005,format='%.4f');alpha=a.number_input('Family-wise alpha',.001,.2,.05);power=b.slider('Desired power',.5,.99,.8,.01);groups=a.number_input('Number of experimental groups',2,10,3);ratio=b.number_input('Each treatment / control allocation ratio',.1,10.,1.)
    try:
        result=planning(baseline,mde,alpha,power,int(groups),ratio);st.json(result)
        from statsmodels.stats.power import NormalIndPower
        from statsmodels.stats.proportion import proportion_effectsize
        nn=np.linspace(100,result['control_n']*2,50);pp=NormalIndPower().power(abs(proportion_effectsize(baseline+mde,baseline)),nn,alpha/(groups-1),ratio=ratio)
        chart(finish(px.line(x=nn,y=pp,labels={'x':'Control sample size','y':'Power'}),'Illustrative power curve'))
        st.caption('All treatment groups share the specified ratio to control. Approximate sample sizes exclude delivery failure, attrition and design effects; rounding can slightly alter ratios.')
    except ValueError as error: st.error(str(error))

