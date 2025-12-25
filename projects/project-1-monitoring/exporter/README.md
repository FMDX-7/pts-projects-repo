# Simple Python Exporter (demo)

This tiny exporter exposes a single heartbeat metric at `http://localhost:8000/metrics`.

Run locally (in a virtualenv):

```powershell
# from the repo root (cross-platform):
cd projects/project-1-monitoring/exporter
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python exporter.py

# OR use an absolute path on your machine (replace with your path):
# cd "C:/path/to/pts-projects-repo/projects/project-1-monitoring/exporter"
# python -m venv .venv
# .\.venv\Scripts\Activate.ps1
# pip install -r requirements.txt
# python exporter.py
```

Prometheus scrape config in `../prometheus.yml` includes `python-exporter:8000` so the exporter will be picked up when running via Docker Compose (see top-level `docker-compose.yml`).
