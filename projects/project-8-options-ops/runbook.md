# Runbook — Options Ops Simulator (Project 8)

Scenarios
- Feed stale (quote heartbeat too old)
- Route down / service unhealthy
- Risk limit breach (notional or capacity)

Quick checks (first 5 minutes)
- `GET /health` — should be `ok`; feed status should be `ok` with small age.
- `GET /quotes/status` — check `age_sec`; if >10s, feed is stale.
- `GET /metrics` — confirm orders_count; check limits.
- Synthetic order: POST a small single-leg order to confirm routing.

Remediation
- Feed stale: restart `mock_quote_feed.py`; verify `quotes_state.json` updates; re-check `/quotes/status`.
- Route/service issue: restart `run_simulator.py`; confirm `/health` returns ok.
- Risk breach: lower size or adjust limit in `OptionsRouter` (max_notional_per_order/max_open_orders); restart service if changed.

Communication templates
- To trading: "Options routing is degraded; investigating feed freshness. Synthetic orders paused. ETA 10m."
- To devs: "Feed stale alert since <ts>; `/quotes/status` age ~<age>s. Restarting feed; attached incidents.jsonl and service logs."

Artifacts
- Incidents: `incidents.jsonl`
- Feed heartbeat: `quotes_state.json`
- Service: `options_service.py`, `run_simulator.py`
- Monitor: `monitor_poll.py`
