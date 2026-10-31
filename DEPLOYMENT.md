# Deployment

Use Python 3.12. On Windows 11, install Python with the Python launcher, then from the repository directory:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe pipeline.py
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m streamlit run app/main.py
```

On Linux/macOS replace the interpreter with `.venv/bin/python`. The pipeline downloads once and reuses the untouched source. It produces a DuckDB database and aggregate reports. Network access is required for first acquisition and dependency installation. No credentials, subscription, GPU or paid API is needed.

Streamlit Community Cloud preparation: obtain data-hosting permission before placing customer-level data on a public service. Push the code only after owner approval, select Python 3.12 and app/main.py. Install requirements.txt, execute pipeline.py in a permitted private preparation stage or adapt the deployment startup command to run the pipeline before Streamlit. The app deliberately does not download data silently during ordinary page rendering. A plain code-only Community Cloud deployment without preparation will display an actionable missing-data message. Provision read/write disk for the ignored data directory. Do not put credentials in Git.

Designed for roughly 8GB RAM: small 64,000-row table, cached loads, precomputed segment tables, unique-support multinomial bootstrap. Exact peak memory and cold-start time must be profiled on the target host; no 8GB compatibility guarantee is inferred from architecture alone. Windows is the local verification environment. No public deployment has been performed.
