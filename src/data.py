from pathlib import Path
import hashlib,json,urllib.request,io
import pandas as pd
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
URL='http://www.minethatdata.com/Kevin_Hillstrom_MineThatData_E-MailAnalytics_DataMiningChallenge_2008.03.20.csv'
GROUPS=['No E-Mail','Mens E-Mail','Womens E-Mail']
BASELINE=['recency','history','history_segment','mens','womens','zip_code','newbie','channel']
COLUMNS=BASELINE+['segment','visit','conversion','spend']
def validate(d):
    if set(d.columns)!=set(COLUMNS) or d.empty: raise ValueError('Expected 12 original columns and nonempty records')
    if d.isna().any().any(): raise ValueError('Missing observations require investigation')
    if set(d.segment)!=set(GROUPS): raise ValueError('Invalid or absent treatment')
    for c in ['visit','conversion','mens','womens','newbie']:
        if not d[c].isin([0,1]).all(): raise ValueError('Invalid binary '+c)
    for c in ['recency','history','spend']:
        if not pd.api.types.is_numeric_dtype(d[c]) or not np.isfinite(d[c]).all() or (d[c]<0).any(): raise ValueError('Invalid numeric '+c)
    if not d.recency.between(1,12).all() or (d.recency%1!=0).any(): raise ValueError('Invalid recency')
    for c,v in {'channel':['Phone','Web','Multichannel'],'zip_code':['Urban','Surburban','Rural'],'history_segment':['1) $0 - $100','2) $100 - $200','3) $200 - $350','4) $350 - $500','5) $500 - $750','6) $750 - $1,000','7) $1,000 +']}.items():
        if not d[c].isin(v).all(): raise ValueError('Invalid category '+c)
    if (d.conversion>d.visit).any() or ((d.spend>0)!=(d.conversion==1)).any(): raise ValueError('Inconsistent outcomes')
    return dict(rows=len(d),columns=len(d.columns),missing=d.isna().sum().to_dict(),duplicate_looking_rows=int(d.duplicated().sum()),dtypes=d.dtypes.astype(str).to_dict(),ranges=d.select_dtypes('number').agg(['min','max']).to_dict(),groups=d.segment.value_counts().to_dict())
def load(path=None):
    d=pd.read_csv(path or ROOT/'data/raw/hillstrom.csv');validate(d);return d
def acquire():
    p=ROOT/'data/raw/hillstrom.csv';p.parent.mkdir(parents=True,exist_ok=True)
    if not p.exists():
        with urllib.request.urlopen(URL,timeout=60) as r: raw=r.read()
        validate(pd.read_csv(io.BytesIO(raw)));p.write_bytes(raw)
    d=load(p)
    (ROOT/'data/provenance.json').write_text(json.dumps(dict(source=URL,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),rows=len(d),transformations='None; original bytes and duplicate-looking records retained',redistribution='No explicit dataset redistribution licence verified; customer-level files excluded from Git'),indent=2),encoding='utf-8')
    return d

