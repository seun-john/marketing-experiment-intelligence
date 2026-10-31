import numpy as np
import pandas as pd
import pytest
from scipy.stats import fisher_exact
from src.data import load,validate,GROUPS,ROOT
from src.statistics import compare,relative,summary,effects,balance,segments,planning
from src.simulations import scenario

@pytest.fixture(scope='session')
def data(): return load()

def test_authentic_data(data):
    assert data.shape==(64000,12)
    assert data.segment.value_counts().to_dict()=={'Womens E-Mail':21387,'Mens E-Mail':21307,'No E-Mail':21306}
    assert validate(data)['rows']==64000

@pytest.mark.parametrize('mutation',[lambda d:d.drop(columns='spend'),lambda d:d.assign(segment='unknown'),lambda d:d.assign(visit=2),lambda d:d.assign(history=-1),lambda d:d.assign(channel='unknown'),lambda d:d.assign(spend=np.nan),lambda d:d.assign(recency=13),lambda d:d.assign(history_segment='bad')])
def test_validation_rejects(data,mutation):
    with pytest.raises(ValueError): validate(mutation(data.copy()))

def test_original_retained(data):
    assert len(load())==len(data)
    doubled=pd.concat([data,data.iloc[[0]]],ignore_index=True)
    assert validate(doubled)['rows']==64001

def test_known_binary():
    a=[1,1,0,0];b=[1,0,0,0]
    r=compare(a,b)
    assert r['effect']==.25 and r['relative_lift']==1
    assert r['p_value']==pytest.approx(1.)
    assert r['ci_low']<.25<r['ci_high']
    assert r['n_treatment']==4

def test_published_newcombe_reference():
    # Fagerland et al. example used in statsmodels reference tests: 7/34 vs 1/34.
    r=compare([1]*7+[0]*27,[1]+[0]*33)
    assert r['ci_low']==pytest.approx(.019,abs=.002)
    assert r['ci_high']==pytest.approx(.34,abs=.005)

def test_zero_events():
    r=compare([0]*10,[0]*10)
    assert r['effect']==0 and r['p_value']==1
    assert np.isnan(r['relative_lift']) and r['ci_low']<0<r['ci_high']

@pytest.mark.parametrize('a,b,kwargs',[([1],[0],{}),([1,np.nan],[0,1],{}),([0,2],[0,1],{}),([0,1],[0,1],{'confidence':1}),([0,1],[0,1],{'outcome':'open'})])
def test_invalid_comparisons(a,b,kwargs):
    with pytest.raises(ValueError): compare(a,b,**kwargs)

def test_spend_skew():
    r=compare([0]*99+[1000],[0]*100,'spend')
    assert r['effect']==10 and np.isnan(r['relative_lift'])
    assert r['ci_low']<=10<=r['ci_high']
    assert compare([0]*5,[0]*5,'spend')['p_value']==1

def test_summary_denominators(data):
    s=summary(data).set_index('segment')
    assert s.loc['Mens E-Mail','customers']==21307
    assert s.loc['Mens E-Mail','conversions']==267
    assert s.loc['No E-Mail','conversions']==122
    assert s.loc['Womens E-Mail','conversions']==189
    assert s.loc['Mens E-Mail','spend']==pytest.approx(data.loc[data.segment=='Mens E-Mail','spend'].sum()/21307)

def test_holm_independent_reference():
    from statsmodels.stats.multitest import multipletests
    assert multipletests([.01,.04],method='holm')[1]==pytest.approx([.02,.04])

def test_families():
    e=pd.read_csv(ROOT/'reports/treatment_effects.csv')
    assert sorted(e.groupby('family').size())==[2,7]
    assert (e.p_adjusted>=e.p_value-1e-14).all()

def test_balance(data):
    b=balance(data)
    assert np.isfinite(b.smd).all() and len(b)>20
    equal=pd.concat([data.iloc[:200].assign(segment=g) for g in GROUPS],ignore_index=True)
    assert balance(equal).smd.abs().max()==0

def test_segments(data):
    out=segments(data,'newbie')
    assert len(out)==4
    for r in out.itertuples():
        part=data[data.newbie==int(r.segment_value)]
        assert r.n_treatment==(part.segment==r.treatment).sum()
    assert segments(data.iloc[:0],'newbie').empty
    with pytest.raises(ValueError): segments(data,'conversion')

def test_scenario():
    t=scenario(.01,0,.02,1000,.1,.4,100,50)
    assert list(t.net_contribution)==[-150,250,650]
    assert t.iloc[1].incremental_conversions==10
    assert t.iloc[1].break_even_effect==pytest.approx(.00375)
    assert np.isnan(scenario(0,0,0,0,0,0,0).iloc[0].break_even_effect)
    with pytest.raises(ValueError): scenario(.01,0,.02,-1,.1,.4,100)

@pytest.mark.parametrize('args',[(0,.01),(1,.01),(.9,.2),(.01,-.01)])
def test_planning_invalid(args):
    with pytest.raises(ValueError): planning(*args)

def test_planning_known_reference():
    # Conventional two-arm 10% to 15%, 80% power, 5% two-sided: approximately 685/arm.
    p=planning(.10,.05,groups=2)
    assert 680<=p['control_n']<=690
    assert p['total_n']==2*p['control_n']

def test_sql_reconciliation(data):
    import duckdb
    con=duckdb.connect();con.register('customers',data)
    for p in sorted((ROOT/'src/sql').glob('*.sql')):
        sql=con.execute(p.read_text(encoding='utf-8-sig')).df()
        assert len(sql)>0
        if p.stem[:2] in ['01','02','03','04','05','06']:
            sql=sql.set_index('segment')
            for g in GROUPS:
                rows=data[data.segment==g]
                if 'customers' in sql: assert sql.loc[g,'customers']==len(rows)
                if 'proportion' in sql: assert sql.loc[g,'proportion']==pytest.approx(len(rows)/len(data))
                if 'visits' in sql: assert sql.loc[g,'rate']==pytest.approx(rows.visit.mean())
                if 'conversions' in sql: assert sql.loc[g,'rate']==pytest.approx(rows.conversion.mean())
                if 'total_spend' in sql: assert sql.loc[g,'total_spend']==pytest.approx(rows.spend.sum())
                if 'mean_spend' in sql: assert sql.loc[g,'mean_spend']==pytest.approx(rows.spend.mean())
        elif p.stem[:2] in ['07','08']:
            for r in sql.itertuples():
                for metric in ['conversion','visit','spend']:
                    a=data.loc[data.segment==r.segment,metric].mean();b=data.loc[data.segment=='No E-Mail',metric].mean()
                    expected=a-b if p.stem[:2]=='07' else (a-b)/b
                    assert getattr(r,metric+('_difference' if p.stem[:2]=='07' else '_lift'))==pytest.approx(expected)
        else:
            attr={'09':'history_segment','10':'channel','11':'recency','12':'newbie'}[p.stem[:2]]
            for _,r in sql.iterrows():
                part=data[(data[attr]==r[attr])&(data.segment==r.segment)]
                assert r.assigned==len(part)
                for metric in ['conversion','visit','spend']: assert r[metric]==pytest.approx(part[metric].mean())
    con.close()


def test_integrity_equal_allocation(data):
    from src.statistics import integrity
    equal=pd.concat([data.iloc[:200].assign(segment=g) for g in GROUPS],ignore_index=True)
    assert integrity(equal)['srm_p']==1
    assert integrity(equal)['srm_statistic']==0

def test_interactions_multiplicity_artifact():
    it=pd.read_csv(ROOT/'reports/interactions.csv')
    assert len(it)==14
    assert set(it.outcome)=={'conversion','spend'}
    assert (it.p_adjusted>=it.p_value-1e-14).all()

def test_dashboard_transform_units():
    from src.visualisation import forest
    row=pd.DataFrame([dict(effect=.01,ci_low=0,ci_high=.02,relative_lift=.5,relative_low=0.,relative_high=1.,treatment='A',reference='B',n_treatment=100,n_reference=100)])
    fig=forest(row,'conversion')
    assert fig.data[0].x[0]==1
    assert fig.data[0].error_x.array[0]==1
    fig=forest(row,'conversion',True)
    assert fig.data[0].x[0]==50

def test_planning_rejects_fractional_or_infinite():
    with pytest.raises(ValueError): planning(.1,.01,groups=2.5)
    with pytest.raises(ValueError): planning(.1,.01,ratio=np.inf)
