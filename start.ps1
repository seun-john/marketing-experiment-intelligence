param([int]$Port=8501)
$ErrorActionPreference='Stop'
Push-Location $PSScriptRoot
try {
    & '.\.venv\Scripts\python.exe' pipeline.py
    if ($LASTEXITCODE -ne 0) { throw 'Data preparation failed' }
    & '.\.venv\Scripts\python.exe' -m streamlit run app/main.py --server.port $Port
} finally { Pop-Location }
