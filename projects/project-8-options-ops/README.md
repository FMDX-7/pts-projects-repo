# Project 8 — Options Routing Ops Simulator

Purpose

- Simulate an options order-routing service with monitoring, incidents, and a mini dashboard. Focus on application-support tasks for options market making.

Includes

- `options_service.py`: Flask API with endpoints for single/multi-leg options orders, health/metrics, incidents, and a dashboard.
- `mock_quote_feed.py`: mock NBBO-like feed writer; updates a quote heartbeat file.
- `monitor_poll.py`: polls health + quote status and logs incidents on failures.
- `incident_logger.py`: JSONL incident log utilities.
- `run_simulator.py`: helper to start the service on port 8081.
- `static/dashboard.html`: small dashboard (health, orders by symbol, incidents by type, feed heartbeat).
- `requirements.txt`: minimal deps.

Quick start

```powershell
cd projects/project-8-options-ops
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# start mock quote feed (background)
Start-Process -FilePath python -ArgumentList 'mock_quote_feed.py' -WindowStyle Hidden

# start service (background)
Start-Process -FilePath python -ArgumentList 'run_simulator.py' -WindowStyle Hidden

# start monitor poller (background)
Start-Process -FilePath python -ArgumentList 'monitor_poll.py' -WindowStyle Hidden

# open dashboard
Start-Process "http://127.0.0.1:8081/dashboard"
```

Sample order (single-leg)

```powershell
Invoke-RestMethod -Method Post -Body (ConvertTo-Json @{underlying='AAPL'; expiry='2025-01-17'; strike=200; option_type='C'; side='BUY'; qty=10; price=1.25; strategy_type='single'}) -ContentType 'application/json' http://127.0.0.1:8081/orders
```

Sample multi-leg order

```powershell
$legs = @(
  @{underlying='AAPL'; expiry='2025-01-17'; strike=200; option_type='C'; side='BUY'; qty=10; price=1.25},
  @{underlying='AAPL'; expiry='2025-01-17'; strike=210; option_type='C'; side='SELL'; qty=10; price=0.80}
)
Invoke-RestMethod -Method Post -Body (ConvertTo-Json @{strategy_type='vertical'; legs=$legs}) -ContentType 'application/json' http://127.0.0.1:8081/orders/multi
```

Runbook

- See `runbook.md` for triage (feed stale, route down, risk limit breach) and comms templates.
