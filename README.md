# pts-projects-repo

A lightweight scaffold for the PTS interview projects. This repo collects the demos and walkthroughs used for interview prep and contains starter files for the monitoring and ops projects.

Included (scaffold):

- project-1-monitoring: Prometheus + Grafana compose and example config (see pts-projects/ for fuller scaffolding).
- project-2-service-watcher: PowerShell and Bash watcher scripts.
- other projects: placeholders for log-ingest, scheduler, order-routing, backtest-logs.

Getting started locally

1. Initialize a local git repository and create first commit:

```powershell
cd "C:/Users/FM's Laptop/Downloads/pts-projects-repo"
git init -b main
git add .
git commit -m "chore: scaffold pts-projects-repo"
```

2. (Optional) Create a GitHub repo and push:

```powershell
# create remote repo on GitHub via CLI (gh) then push
gh repo create <your-org-or-username>/pts-projects-repo --public --source=. --remote=origin --push
```

Next steps

- Review and copy over the detailed project folders from the workspace `pts-projects` if desired.
- Let me know if you want me to initialize git here, create a branch, or create a remote GitHub repo (I can generate `gh` commands but cannot push without credentials).