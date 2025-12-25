
# Project 6 — Backtest Logs

Purpose

- Collect and present backtest logs and metrics from trading strategy runs (parsing, aggregation, visualization).

What this demo contains

- `logs/sample_backtest.jsonl` — sample backtest output (JSON-lines).
- `backtest_parser.py` — small parser that reads JSON-lines logs and summarizes trades and P&L.
- `analyze_pandas.py` — pandas-based CSV analyzer that produces simple visualizations (`plots/`).

Pandas visualization

1. Ensure dependencies installed:

```powershell
pip install -r requirements.txt
```

2. Run the analyzer to produce plots:

```powershell
python analyze_pandas.py
```

3. Result: two PNG files saved under `plots/`:
- `plots/cumulative_pnl.png` — cumulative PnL over time
- `plots/pnl_by_symbol.png` — total PnL per symbol

- `summarize.py` — CLI wrapper that prints a summary for the sample log.

Quick start

```powershell
cd projects/project-6-backtest-logs
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt   # optional: add pandas/matplotlib if you extend
python summarize.py
```

Notes

- The sample parser uses only the Python standard library and expects JSON-lines (one JSON object per line).
- Extend `parser.py` to support CSV or your backtest output format, or add Pandas-based analysis/plots.

