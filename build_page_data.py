from pathlib import Path
import csv,json
root=Path(__file__).resolve().parent
with (root/'reports/group_summary.csv').open(encoding='utf-8-sig') as f: groups=list(csv.DictReader(f))
with (root/'reports/treatment_effects.csv').open(encoding='utf-8-sig') as f: effects=list(csv.DictReader(f))
for row in groups+effects:
    for k,v in row.items():
        try:row[k]=float(v)
        except (ValueError,TypeError):pass
(root/'docs/results.json').write_text(json.dumps(dict(groups=groups,effects=effects),indent=2),encoding='utf-8')
(root/'docs/.nojekyll').touch()

import shutil
for name in ['analytical_report.html','treatment_effects.csv','group_summary.csv']:
    shutil.copy2(root/'reports'/name,root/'docs'/name)
for name in ['dashboard_overview.png','dashboard_segments.png','dashboard_roi.png']:
    shutil.copy2(root/'assets'/name,root/'docs/assets'/name)
