import importlib.metadata as m
from pathlib import Path
packages=['numpy','pandas','scipy','statsmodels','duckdb','plotly','streamlit','pytest','tabulate']
Path('requirements.txt').write_text('\n'.join(f'{p}=={m.version(p)}' for p in packages)+'\n')
# Full tested environment lock is supplemental; no unrelated global dependencies included.
from importlib.metadata import distribution
seen=set()
def visit(name):
    from packaging.requirements import Requirement
    from packaging.utils import canonicalize_name
    name=canonicalize_name(name)
    if name in seen:return
    seen.add(name)
    for dep in distribution(name).requires or []:
        req=Requirement(dep)
        if req.marker is None or req.marker.evaluate():visit(req.name)
for p in packages:visit(p)
Path('requirements-lock.txt').write_text('\n'.join(f'{p}=={m.version(p)}' for p in sorted(seen))+'\n')
