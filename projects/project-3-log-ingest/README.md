# Project 3 — Log Ingest

Purpose

- Show a small pipeline ingesting application logs into Loki and visualizing with Grafana.

Primary tech

- Promtail (log shipper), Loki, Grafana

Run / Demo (local)

1. Start the stack with Docker Compose from the project folder:

```powershell
cd path\to\pts-projects-repo\projects\project-3-log-ingest
docker compose up -d
```

2. Start the log generator (in a separate terminal):

```powershell
cd path\to\pts-projects-repo\projects\project-3-log-ingest
python generate_logs.py
```

3. Open Grafana at http://localhost:3000 (user: `admin`, password: `admin`) and add a Loki datasource pointing to `http://loki:3100`.

4. In Grafana Explore choose Loki and run a query such as:

```
{job="app"} |~ "heartbeat"
```

Files added

- `docker-compose.yml` — Loki + Promtail + Grafana
- `loki-config.yaml` — basic Loki local config
- `promtail.yml` — Promtail config to read `./logs/*.log`
- `generate_logs.py` — simple heartbeat log generator
- `logs/` — sample log folder

Notes

- This is a minimal local demo for interview purposes. For production use secure Grafana, enable auth, and configure retention/storage for Loki.
