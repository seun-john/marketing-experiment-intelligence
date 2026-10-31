from playwright.sync_api import sync_playwright
from pathlib import Path
import json
r=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
    b=p.chromium.launch(channel='chrome',headless=True)
    page=b.new_page(viewport={'width':1400,'height':1000})
    page.goto((r/'reports/analytical_report.html').as_uri())
    result=page.locator('body *').evaluate_all('(els)=>[...new Set(els.map(e=>getComputedStyle(e).fontFamily+" / "+getComputedStyle(e).fontSize))]')
    page.screenshot(path=str(r/'assets/analytical_report.png'))
    (r/'reports/report_font_check.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    assert all('Times New Roman' in x and '16px' in x for x in result),result
    b.close()
