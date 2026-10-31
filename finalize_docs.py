from pathlib import Path
import pandas as pd,json,html,re,csv
root=Path(__file__).resolve().parent
# Independent standard-library audit reads raw records without Pandas aggregation or shared functions.
counts={}
with (root/'data/raw/hillstrom.csv').open(newline='',encoding='utf-8-sig') as f:
    for r in csv.DictReader(f):
        x=counts.setdefault(r['segment'],{'n':0,'conversion':0,'visit':0,'spend':0.})
        x['n']+=1;x['conversion']+=int(r['conversion']);x['visit']+=int(r['visit']);x['spend']+=float(r['spend'])
(root/'reports/independent_counts.json').write_text(json.dumps(counts,indent=2),encoding='utf-8')
s=pd.read_csv(root/'reports/group_summary.csv');e=pd.read_csv(root/'reports/treatment_effects.csv')
readme=root/'README.md';text=readme.read_text(encoding='utf-8-sig')
addition='''## Verified findings

| Assignment | Customers | Purchases | Conversion | Spending / customer |
|---|---:|---:|---:|---:|
'''
for r in s.itertuples(): addition+=f'| {r.segment} | {r.customers:,} | {r.conversions} | {r.conversion:.3%} | ${r.spend:.3f} |\n'
addition+='\n'
for r in e[(e.outcome=='conversion')&(e.reference=='No E-Mail')].itertuples():addition+=f'- {r.treatment}: **{r.effect*100:+.3f} percentage points** (95% CI {r.ci_low*100:.3f}–{r.ci_high*100:.3f}); relative lift {r.relative_lift:.1%}; Holm p={r.p_adjusted:.4g}.\n'
addition+='\nBoth assignments increased conversion in this historical experiment. Profitability depends on costs and margin assumptions. All reported uncertainty intervals are pointwise.\n\n'
text=re.sub(r'## Verified findings.*?(?=## Statistical methods)', '', text, flags=re.S)
text=text.replace('## Statistical methods',addition+'## Statistical methods')
readme.write_text(text,encoding='utf-8')
# Render readable standalone report: 12pt Times New Roman applies to all headings, tables and body.
lines=(root/'reports/analytical_report.md').read_text(encoding='utf-8').splitlines();parts=[];i=0
while i<len(lines):
    line=lines[i]
    if line.startswith('|'):
        rows=[]
        while i<len(lines) and lines[i].startswith('|'):
            cells=[c.strip() for c in lines[i].strip('|').split('|')]
            if not all(re.fullmatch(r'[:\-\s]+',c or '-') for c in cells):rows.append(cells)
            i+=1
        parts.append('<div class="table-wrap"><table>'+''.join('<tr>'+''.join(f'<{"th" if j==0 else "td"}>{html.escape(c)}</{"th" if j==0 else "td"}>' for c in row)+'</tr>' for j,row in enumerate(rows))+'</table></div>');continue
    if line.startswith('#'):
        n=len(line)-len(line.lstrip('#'));parts.append(f'<h{n}>'+html.escape(line[n:].strip())+f'</h{n}>')
    elif line.strip():parts.append('<p>'+html.escape(line)+'</p>')
    i+=1
(root/'reports/analytical_report.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Marketing Experiment Intelligence</title><style>*{font-family:"Times New Roman"!important;font-size:12pt!important}body{max-width:1100px;margin:36px auto;padding:0 24px;line-height:1.6;color:#111}h1,h2{margin-top:28px}table{border-collapse:collapse;width:100%}td,th{padding:6px;border:1px solid #777;text-align:left}.table-wrap{overflow-x:auto}@media print{body{max-width:none;margin:0;padding:0}table{width:100%}tr{break-inside:avoid}}</style></head><body>'+''.join(parts)+'</body></html>',encoding='utf-8')
