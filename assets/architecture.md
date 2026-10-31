# Architecture

```mermaid
flowchart LR
  A[Original Hillstrom CSV] --> B[Immutable acquisition and validation]
  B --> C[DuckDB customer table]
  C --> D[12 documented SQL queries]
  B --> E[Shared statistical functions]
  E --> F[Pipeline reports and aggregate tables]
  F --> G[Streamlit workspace]
  E --> G
  G --> H[Hypothetical decision simulator]
  I[pytest fixtures and independent checks] --> D
  I --> E
```

Data layer: src/data.py. Statistics and integrity: src/statistics.py. Hypothetical economics: src/simulations.py. SQL: src/sql/. Chart transforms: src/visualisation.py. Reproducible orchestration: pipeline.py. Presentation: app/main.py. Reports and dashboard consume the same estimates; app lab confidence changes invoke the shared comparison function, with fixed family decisions retained from pipeline outputs.
