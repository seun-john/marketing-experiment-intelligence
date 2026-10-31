"""Pointwise intention-to-treat inference; fixed random seeds."""
import numpy as np
import pandas as pd
from scipy import stats,optimize
from statsmodels.stats.proportion import confint_proportions_2indep,proportions_ztest,proportion_effectsize
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.power import NormalIndPower
from .data import GROUPS,BASELINE

def relative(effect,baseline): return float(effect/baseline) if baseline else np.nan

def compare(a,b,outcome='conversion',confidence=.95,bootstrap=2000,seed=20261031):
    if outcome not in ['conversion','visit','spend'] or not 0<confidence<1: raise ValueError('Invalid metric/confidence')
    a,b=np.asarray(a,dtype=float),np.asarray(b,dtype=float)
    if min(len(a),len(b))<2 or not np.isfinite(a).all() or not np.isfinite(b).all(): raise ValueError('Two complete observations per group required')
    effect=a.mean()-b.mean(); extra=dict(relative_low=np.nan,relative_high=np.nan)
    if outcome!='spend':
        if not np.isin(a,[0,1]).all() or not np.isin(b,[0,1]).all(): raise ValueError('Binary outcomes required')
        x,y=a.sum(),b.sum();tab=np.array([[x,len(a)-x],[y,len(b)-y]])
        expected=np.outer(tab.sum(1),tab.sum(0))/tab.sum()
        if (expected<5).any():
            test=stats.fisher_exact(tab);stat,p=test.statistic,test.pvalue;method='Fisher exact (odds ratio statistic); Newcombe interval'
        else: stat,p=proportions_ztest([x,y],[len(a),len(b)]);method='Pooled two-proportion z test; Newcombe interval'
        lo,hi=confint_proportions_2indep(x,len(a),y,len(b),method='newcomb',alpha=1-confidence)
        if x>0 and y>0:
            rl,rh=confint_proportions_2indep(x,len(a),y,len(b),compare='ratio',method='log',alpha=1-confidence)
            extra=dict(relative_low=rl-1,relative_high=rh-1)
    else:
        if min(a.min(),b.min())<0 or bootstrap<100: raise ValueError('Nonnegative spending; >=100 bootstrap draws')
        rng=np.random.default_rng(seed);means=[]
        for v in (a,b):
            values,counts=np.unique(v,return_counts=True)
            means.append(rng.multinomial(len(v),counts/len(v),size=bootstrap)@values/len(v))
        lo,hi=np.quantile(means[0]-means[1],[(1-confidence)/2,1-(1-confidence)/2])
        if a.var()+b.var()==0: stat,p=(0.,1.) if effect==0 else (np.sign(effect)*np.inf,0.)
        else: test=stats.ttest_ind(a,b,equal_var=False);stat,p=test.statistic,test.pvalue
        method=f'Welch mean test; empirical percentile bootstrap CI ({bootstrap} draws, seed {seed})'
    return dict(n_treatment=len(a),n_reference=len(b),treatment_mean=a.mean(),reference_mean=b.mean(),effect=effect,relative_lift=relative(effect,b.mean()),ci_low=float(lo),ci_high=float(hi),statistic=float(stat),p_value=float(p),method=method,**extra)

def effects(d):
    rows=[]
    for o in ['conversion','visit','spend']:
        for t,r in [(GROUPS[1],GROUPS[0]),(GROUPS[2],GROUPS[0]),(GROUPS[1],GROUPS[2])]:
            rows.append(compare(d.loc[d.segment==t,o],d.loc[d.segment==r,o],o)|dict(outcome=o,treatment=t,reference=r,family='Primary conversion (2)' if o=='conversion' and r==GROUPS[0] else 'Secondary/exploratory (7)'))
    out=pd.DataFrame(rows)
    for _,idx in out.groupby('family').groups.items(): out.loc[idx,'p_adjusted']=multipletests(out.loc[idx,'p_value'],method='holm')[1]
    return out

def summary(d):
    return d.groupby('segment').agg(customers=('conversion','size'),conversions=('conversion','sum'),conversion=('conversion','mean'),visits=('visit','sum'),visit=('visit','mean'),total_spend=('spend','sum'),spend=('spend','mean'),spend_sd=('spend','std')).reindex(GROUPS).reset_index()

def balance(d):
    f=pd.get_dummies(d[BASELINE],columns=['history_segment','channel','zip_code'],dtype=float);rows=[]
    for t,r in [(GROUPS[1],GROUPS[0]),(GROUPS[2],GROUPS[0]),(GROUPS[1],GROUPS[2])]:
        for c in f:
            a,b=f.loc[d.segment==t,c],f.loc[d.segment==r,c];sd=np.sqrt((a.var()+b.var())/2)
            rows.append(dict(feature=c,treatment=t,reference=r,smd=(a.mean()-b.mean())/sd if sd else 0.))
    return pd.DataFrame(rows)

def integrity(d):
    test=stats.chisquare(d.segment.value_counts().reindex(GROUPS))
    return dict(srm_statistic=float(test.statistic),srm_p=float(test.pvalue),expected_allocation='Assumed approximate 1:1:1',omnibus_p={o:float(stats.chi2_contingency(pd.crosstab(d.segment,d[o]),correction=False).pvalue) for o in ['conversion','visit']})

def segments(d,attribute,outcome='conversion'):
    if attribute not in BASELINE: raise ValueError('Pretreatment attributes only')
    if attribute=='history': d=d.assign(history=pd.cut(d.history,[-1,100,200,350,500,750,1000,np.inf]).astype(str))
    rows=[]
    for v,part in d.groupby(attribute,observed=True):
        for t in GROUPS[1:]:
            a,b=part.loc[part.segment==t,outcome],part.loc[part.segment==GROUPS[0],outcome]
            if min(len(a),len(b))>=2: rows.append(compare(a,b,outcome,bootstrap=1000)|dict(segment_value=str(v),treatment=t,sparse=min(len(a),len(b))<100 or (outcome!='spend' and min(a.sum(),b.sum())<10)))
    return pd.DataFrame(rows)

def interaction(d,attribute,outcome='conversion'):
    import statsmodels.formula.api as smf
    if attribute not in BASELINE or attribute=='history': raise ValueError('Use history_segment for categorical history interaction')
    m=smf.ols(f'{outcome} ~ C(segment)*C({attribute})',data=d).fit(cov_type='HC3')
    names=[n for n in m.params.index if ':' in n];contrast=np.zeros((len(names),len(m.params)))
    for i,n in enumerate(names): contrast[i,m.params.index.get_loc(n)]=1
    w=m.wald_test(contrast,scalar=True)
    return dict(statistic=float(w.statistic),p_value=float(w.pvalue),df=len(names),method='HC3 joint Wald test; additive scale; exploratory unadjusted')

def planning(baseline,mde,alpha=.05,power=.8,groups=3,ratio=1.):
    if not np.isfinite([baseline,mde,alpha,power,groups,ratio]).all() or int(groups)!=groups or not 0<baseline<1 or not 0<mde<1-baseline or not 0<alpha<1 or not 0<power<1 or not 2<=groups<=10 or ratio<=0: raise ValueError('Invalid planning inputs')
    n=int(np.ceil(NormalIndPower().solve_power(abs(proportion_effectsize(baseline+mde,baseline)),alpha=alpha/(groups-1),power=power,ratio=ratio)))
    nt=int(np.ceil(n*ratio));return dict(control_n=n,treatment_n=nt,total_n=n+(groups-1)*nt,per_comparison_alpha=alpha/(groups-1))

def detectable(baseline,n,alpha=.025,power=.8):
    return float(optimize.brentq(lambda x:NormalIndPower().power(abs(proportion_effectsize(baseline+x,baseline)),n,alpha,ratio=1)-power,1e-9,1-baseline-1e-9))
