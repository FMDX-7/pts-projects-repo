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

Troubleshooting: Grafana to Loki datasource

- Important: when Grafana is running inside the same Docker Compose network (the default in this demo), the datasource URL in Grafana must be the service hostname and port that Grafana can reach inside the Compose network: `http://loki:3100`.
	- If you set the URL to `http://localhost:3100` in Grafana's UI, Grafana will try to connect to *its own* container's localhost, not your host machine — that will fail in this Compose setup.
	- If you are running Grafana on your host (not in Docker), then use `http://localhost:3100`.

- Quick checks if "Unable to connect with Loki" appears:
	1. From your host, confirm Loki is listening on the published port:

```powershell
# host (PowerShell)
curl http://localhost:3100/ready
```

	2. From inside the Grafana container (to test container networking):

```powershell
# run on host
docker compose exec grafana pwsh -c "curl -svS http://loki:3100/ready"
```

	3. Check container logs for errors:

```powershell
docker compose logs --tail 200 loki
docker compose logs --tail 200 promtail
docker compose logs --tail 200 grafana
```

	4. If Promtail shows DNS failures (errors like "no such host" for `loki`) or Loki failed to start, restart the stack and re-check logs:

```powershell
docker compose down
docker compose up -d --build
```

- Auto-provisioning Grafana datasource (optional):
	- To avoid manual steps you can add a provisioning file under `grafana/provisioning/datasources/loki.yml` that points Grafana to `http://loki:3100` and the container will create the datasource automatically on startup. I can add this file for you if you want.
