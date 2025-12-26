# Project 9 — Futures Routing Ops Simulator (ES/NQ)

Purpose

- Simulate futures order routing/monitoring for ES and NQ with health checks, incidents, and a mini dashboard. Tailored to production support for futures/derivatives.

Includes

- `futures_service.py`: Flask API for futures orders (ES/NQ), health/metrics, incidents, and dashboard.
- `mock_feed.py`: mock futures price feed (ES/NQ) with heartbeat file.
- `monitor_poll.py`: polls health/feed and logs incidents on failures.
- `incident_logger.py`: JSONL incident log utilities.
- `run_simulator.py`: helper to start the service on port 8082.
- `static/dashboard.html`: dashboard (health, orders by symbol, incidents, feed heartbeat).
- `requirements.txt`: minimal deps.

Quick start

```powershell
cd projects/project-9-futures-ops
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

Start-Process -FilePath python -ArgumentList 'mock_feed.py' -WindowStyle Hidden
Start-Process -FilePath python -ArgumentList 'run_simulator.py' -WindowStyle Hidden
Start-Process -FilePath python -ArgumentList 'monitor_poll.py' -WindowStyle Hidden
Start-Process "http://127.0.0.1:8082/dashboard"
```

Sample order

```powershell
Invoke-RestMethod -Method Post -Body (ConvertTo-Json @{symbol='ES'; side='BUY'; qty=1; price=4800; tif='DAY'}) -ContentType 'application/json' http://127.0.0.1:8082/orders
```

Runbook
- See `runbook.md` for triage steps (feed stale, route down, risk breaches) and comms templates.
