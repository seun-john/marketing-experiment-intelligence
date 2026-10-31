import json
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from pathlib import Path
import pytest
from src.data import ROOT,load

def test_public_aggregates_match_original_records():
    data=json.loads((ROOT/'docs/results.json').read_text(encoding='utf-8'))
    original=load()
    assert len(data['groups'])==3 and len(data['effects'])==9
    assert sum(g['customers'] for g in data['groups'])==64000
    for group in data['groups']:
        part=original[original.segment==group['segment']]
        assert group['customers']==len(part)
        assert group['conversions']==int(part.conversion.sum())
        for metric in ['conversion','visit','spend']:assert group[metric]==pytest.approx(part[metric].mean())

def test_public_local_links_resolve():
    class Links(HTMLParser):
        paths=[]
        def handle_starttag(self,tag,attrs):
            for k,v in attrs:
                if k in ['href','src'] and v and not urlsplit(v).scheme and urlsplit(v).path:self.paths.append(unquote(urlsplit(v).path))
    parser=Links();parser.feed((ROOT/'docs/index.html').read_text(encoding='utf-8-sig'))
    assert parser.paths
    for link in parser.paths:assert (ROOT/'docs'/link).is_file(),link

def test_public_downloads_match_analysis():
    for name in ['analytical_report.html','treatment_effects.csv','group_summary.csv']:
        assert (ROOT/'docs'/name).read_bytes()==(ROOT/'reports'/name).read_bytes()
