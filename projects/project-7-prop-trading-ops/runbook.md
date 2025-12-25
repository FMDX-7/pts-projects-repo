# Runbook — Triage & Escalation (Prop Trading Service)

Purpose

- Help on-call engineers quickly triage incidents that affect order routing or market-facing services.

When to use

- Use this runbook when health checks fail, orders are not being delivered, or downstream gateways show errors.

Initial triage (first 5 minutes)

1. Gather context
   - What alert fired? (`health_check_failed`, `health_check_error`, or other incident type)
   - When did it start? Check `incidents.jsonl` and timestamps.
   - Is trading live (market hours)? If yes, escalate faster.

2. Quick health checks
   - Check service/process status (server PID, memory, CPU): `Get-Process -Name python` or platform equivalent.
   - Query local health endpoint: `GET /health` — expect `{"status":"ok"}`.
   - Query metrics: `GET /metrics` for orders count or other custom metrics.

3. Verify order delivery
   - Try a synthetic order: POST a small order to `POST /orders` and confirm response contains an `execution` block.
   - If the API accepts but downstream shows failure, capture the returned payload and any error codes.

4. Check recent logs & incidents
   - Tail service logs and `incidents.jsonl` for errors and stack traces.
   - Look for repeated failures, timeouts, or dependency errors.

Remediation steps (common cases)

- Health endpoint returns error / times out:
  - Check service process and restart if hung.
  - If dependency (e.g., exchange gateway) is unreachable, mark as degraded and notify trading desk.

- Orders are failing to route:
  - Confirm router configuration and asset_class routing rules.
  - If a specific gateway is failing, re-route orders (if safe) or pause automated strategies.

- High error rate after deploy:
  - Roll back to previous release (if available) or disable the new feature.

Escalation matrix

- Tier 1 (you / on-call): Follow triage steps above, collect artifacts, and attempt a safe restart.
- Tier 2 (developer lead): If the root cause appears to be code or config, escalate to the developer responsible for the router/service.
- Tier 3 (SRE / Platform): For infrastructure issues (network, broker, storage), bring in SRE or platform team.

Communication templates

- Short incident notice (to trading desk):

```
We are experiencing degraded order routing for [ASSET_CLASS]. Investigating. Orders may be delayed. ETA 15m.
```

- Technical escalation message (to devs/SRE):

```
Incident: order-routing health checks failing since [timestamp]. Errors: [summary]. Key artifacts: incidents.jsonl, service logs, sample failing request/response.
```

Post-incident

- Capture timelines, root cause, and remediation in a short postmortem.
- Add checks or dashboards to catch similar regressions earlier.
