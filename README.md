# pts-projects-repo

A lightweight scaffold for PTS-style projects and interview demos. This repository collects runnable demos, example configurations, and starter code focused on monitoring, service reliability, and ops automation.

Goals
- Provide small, self-contained projects you can run locally for demos or interview exercises.
- Show practical patterns: Prometheus/Grafana monitoring, log ingestion with Loki/Promtail, simple service watchers, and a GUI job scheduler.

Projects included
- `project-1-monitoring`: Prometheus + Grafana + exporters (Docker Compose examples and Prometheus scrape configs).
- `project-2-service-watcher`: PowerShell and Bash watcher scripts that detect and restart processes; includes a sample long-running app for testing.
- `project-3-log-ingest`: Loki + Promtail + Grafana demo with a small log generator and Compose files to run locally.
- `project-4-job-scheduler`: Tkinter GUI job scheduler demo (add/run scheduled jobs; per-job logs under `logs/`).

Quick start
1. Pick a project directory, e.g. `projects/project-3-log-ingest`.
2. Follow that project's `README.md` for run instructions (most projects use Docker Compose or a simple Python runner).

Notes
- This repo is intended for local demos and interview prep — not production use. Treat configs and credentials accordingly.
- Use `.gitignore` to avoid committing local-only files (for example user-specific `jobs.json` entries).

Contributions
- Add new demo projects under `projects/` and update this README with a short summary and run instructions.

