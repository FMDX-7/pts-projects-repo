
# pts-projects-repo

A set of small, runnable demos and scaffolds for ops/monitoring/interview exercises. Each project is intentionally lightweight and self-contained so you can launch it locally and walk through the behavior.

Goals

- Provide runnable examples that are easy to explain in interviews or demos.
- Focus on common ops topics: monitoring stacks, log ingestion, service reliability tooling, simple schedulers, and trading/backtest helpers.

Projects (short summaries)

- `projects/project-1-monitoring`: Prometheus + Grafana + node/exporter examples. Use this to demo basic metrics collection and dashboards.
- `projects/project-2-service-watcher`: PowerShell/Bash watcher utilities that detect and restart a sample app. Useful for showing simple process supervision techniques.
- `projects/project-3-log-ingest`: Loki + Promtail + Grafana demo. Docker Compose brings up Loki, Promtail, and Grafana (Grafana mapped to a non-default port to avoid conflicts). Includes `generate_logs.py` for demo data.
- `projects/project-4-job-scheduler`: Tkinter GUI job scheduler. Add, edit, run jobs and view per-job logs in `projects/project-4-job-scheduler/logs/`.
- `projects/project-5-order-routing`: Minimal Flask in-memory order router and `sample_client.py` to post orders. Start the server and use the client to demonstrate request/response and in-memory state.
- `projects/project-6-backtest-logs`: Backtest log examples and analyzers. Includes a JSONL and CSV sample, `backtest_parser.py`, and a `analyze_pandas.py` script that produces simple PNG charts in `plots/`.

Quick start (general)

1. Open a shell and change into the project you want to run (example uses project-5):

```powershell
cd projects/project-5-order-routing
```

2. (Optional) Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # PowerShell on Windows
# or: source .venv/bin/activate  # macOS/Linux
```

3. Install dependencies if the project has a `requirements.txt`:

```powershell
pip install -r requirements.txt
```

4. Follow the project's own README for run commands. Examples:

- Project 3 (Docker Compose):

```powershell
cd projects/project-3-log-ingest
docker compose up -d
# then open Grafana (see project README for port)
```

- Project 5 (Flask simulator):

```powershell
cd projects/project-5-order-routing
python run_simulator.py    # starts the API on 127.0.0.1:5000
python sample_client.py    # posts sample orders
```

- Project 6 (backtest analysis):

```powershell
cd projects/project-6-backtest-logs
python analyze_pandas.py   # writes PNG charts to ./plots
```

Notes

- These demos are for local exploration and demonstrations — not production-ready.
- Avoid committing local-only or user-specific files. Each project may include a `jobs.json` or similar — add those to `.gitignore` if they contain local data.
- If you run into port conflicts (e.g., Grafana already on :3000), check the project's README for the mapped port and stop any conflicting service.

Contributing

- Add a new folder under `projects/` with a short README that explains what the demo shows and how to run it.
- Keep projects runnable with minimal setup (prefer a `requirements.txt` or a `docker-compose.yml` when external services are required).

Next steps and ideas

- Add a broker-backed order-routing demo (RabbitMQ/Redis Streams) for project-5.
- Add interactive Plotly dashboards or a small Jupyter notebook for deeper backtest analysis in project-6.
- Add automated Grafana provisioning for project-3 to pre-load datasources/dashboards.

License & safety

- No production credentials or secrets are included. Use caution if adapting configs for real environments.


