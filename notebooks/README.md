# Analysis notebook entry point

The reproducible analysis lives in pipeline.py rather than execution-order-dependent notebook cells. To explore interactively, use `from src.data import load` and `from src.statistics import summary, compare` from the repository root. Rebuild reports with `python pipeline.py` before interpreting dashboard outputs.
