# Runbook — Futures Ops Simulator (Project 9)

Scenarios
- Feed stale (ES/NQ heartbeat old)
- Route/service degraded
- Risk notional breach

Quick checks
- `GET /health` — should be ok; feed status should be ok with small age.
- `GET /quotes/status` — verify `age_sec` < 10s.
- `GET /metrics` — see orders_count and notional limit.
- Synthetic order: POST small ES/NQ order to confirm routing.

Remediation
- Feed stale: restart `mock_feed.py`; confirm `feed_state.json` updates and `/quotes/status` shows ok.
- Route/service issue: restart `run_simulator.py`; verify `/health` is ok.
- Risk breach: lower size or adjust `max_notional_per_order` in `FuturesRouter` then restart.

Communication templates
- Trading: "Futures routing degraded (ES/NQ) due to feed freshness alert; synthetic orders paused. ETA 10m."
- Dev/SRE: "Feed stale since <ts>; `/quotes/status` age ~<age>s. Restarting feed; attaching incidents.jsonl and logs."

Artifacts
- Incidents: `incidents.jsonl`
- Feed heartbeat: `feed_state.json`
- Service: `futures_service.py`, `run_simulator.py`
- Monitor: `monitor_poll.py`
