from playwright.sync_api import sync_playwright
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
    browser=p.chromium.launch(channel='chrome',headless=True)
    page=browser.new_page(viewport={'width':1440,'height':1100},device_scale_factor=1)
    page.goto('http://127.0.0.1:8501');page.get_by_role('heading',name='Executive overview',exact=True).wait_for(timeout=60000)
    page.locator('[data-testid="stPlotlyChart"]').first.wait_for(timeout=60000)
    page.screenshot(path=str(root/'assets/dashboard_overview.png'),full_page=True)
    print(page.locator('body').inner_text()[:1800])
    results=[]
    labels=['Experiment design & quality','Campaign performance','Statistical testing lab','Customer segment intelligence','Marketing ROI simulator','Research & recommendations','Power & sample size']
    for label in labels:
        page.get_by_text(label,exact=True).first.click()
        page.get_by_role('heading',name=label,exact=True).wait_for(timeout=60000)
        page.wait_for_timeout(1500)
        errors=page.locator('[data-testid="stException"]').all_text_contents()
        results.append({'page':label,'errors':errors})
        if label in ['Marketing ROI simulator','Customer segment intelligence']:page.screenshot(path=str(root/'assets'/('dashboard_'+('roi' if label.startswith('Marketing') else 'segments')+'.png')),full_page=True)
    page.set_viewport_size({'width':390,'height':844})
    page.reload();page.locator('[data-testid="stDataFrame"]').first.wait_for(timeout=60000)
    page.get_by_role('button',name='Stop',exact=True).wait_for(state='hidden',timeout=60000)
    close=page.get_by_role('button',name='Close sidebar')
    if close.count(): close.click()
    page.wait_for_timeout(1000)
    page.screenshot(path=str(root/'assets/dashboard_mobile.png'),full_page=True)
    results.append({'mobile_document_width':page.evaluate('document.documentElement.scrollWidth'),'viewport':390})
    (root/'reports/browser_checks.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    browser.close()
