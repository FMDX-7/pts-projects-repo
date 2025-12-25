# Project 7 — Prop Trading Services (ops/monitoring demo)

Purpose

- Demonstrate operational tooling for a prop trading environment that supports options, equities, and futures.
- Focus areas: order delivery/routing, health checks, incident logging, and a simple triage workflow/runbook.

What this demo includes

- `healthcheck_app.py` — small Flask service that exposes an order API plus `GET /health` and `GET /metrics` endpoints to simulate service health and basic metrics.
- `router_extended.py` — an order router that understands `asset_class` (options/equities/futures) and simulates routing/execution.
- `incident_logger.py` — appends incident events to `incidents.jsonl` for later review.
- `monitor_poll.py` — simple poller that periodically calls `/health` and writes incidents when checks fail (simulates on-call detection).
- `run_simulator.py` — helper to start the Flask app without the reloader.
- `requirements.txt` — minimal deps.

- `static/dashboard.html` — mini dashboard that visualizes health, orders by symbol, and incident counts (open `/dashboard`).

Quick start


1. Run the service:

```powershell
cd projects/project-7-prop-trading-ops
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run_simulator.py   # service listens on http://127.0.0.1:8080
```

2. In another shell run the monitor poller (it will create incidents on simulated failures):

```powershell
python monitor_poll.py   # polls http://127.0.0.1:8080/health
```

3. Post a sample order (example JSON includes `asset_class`):

```powershell
Invoke-RestMethod -Method Post -Body (@{symbol='AAPL'; qty=10; asset_class='EQUITY'} | ConvertTo-Json) -ContentType 'application/json' http://127.0.0.1:8080/orders
```

Files to inspect

- `healthcheck_app.py` — service endpoints and integration points to `router_extended` and `incident_logger`.
- `router_extended.py` — lightweight routing logic and simulated fills.
- `monitor_poll.py` — simulates on-call monitoring and incident creation.
- `incidents.jsonl` — persistent incident file (JSON-lines).
- `run_simulator.py` — start the service helper.

Next steps (optional)

- Hook this into a real alerting channel (Slack/email) or add Prometheus metrics export.
- Add an interactive dashboard for live incidents and current orders.
