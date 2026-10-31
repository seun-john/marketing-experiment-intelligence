"""Exercise actual Streamlit page code, including state changes, without a browser."""
from pathlib import Path
from streamlit.testing.v1 import AppTest
ROOT=Path(__file__).resolve().parents[1]
PAGES=['Executive overview','Experiment design & quality','Campaign performance','Statistical testing lab','Customer segment intelligence','Marketing ROI simulator','Research & recommendations','Power & sample size']
def test_all_pages():
    app=AppTest.from_file(str(ROOT/'app/main.py'),default_timeout=90).run()
    assert not app.exception
    for page in PAGES:
        app.sidebar.radio[0].set_value(page).run()
        assert not app.exception, page
        if page=='Campaign performance':
            for outcome in ['visit','spend']:
                app.selectbox[0].set_value(outcome).run();assert not app.exception
        if page=='Statistical testing lab':
            app.selectbox[0].set_value('spend').run();app.slider[0].set_value(.9).run();assert not app.exception
        if page=='Customer segment intelligence':
            app.multiselect[0].set_value([]).run();assert not app.exception
            assert any('No records' in x.value for x in app.info)
        if page=='Marketing ROI simulator':
            app.number_input[0].set_value(0).run();assert not app.exception
        if page=='Power & sample size':
            app.number_input[0].set_value(.9999).run();assert not app.exception
            assert len(app.error)>0
