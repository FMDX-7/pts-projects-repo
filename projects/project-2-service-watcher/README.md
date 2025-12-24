# Project 2 — Service Watcher

Purpose

- Demonstrate on-host automation to detect and recover failed services (PowerShell for Windows, Bash/systemd for Linux).

Primary tech

- PowerShell, Bash, systemd, Windows Service management

Run / Demo

1. Run the watcher script on the host (PowerShell):

```powershell
cd "C:/Users/FM's Laptop/Downloads/pts-projects-repo/projects/project-2-service-watcher"
.\service_watcher.ps1
```

2. Simulate a service stop and verify watcher restarts it and logs the event.

What to include

- `service_watcher.ps1` with logging and restart logic
- `service_watcher.sh` equivalent for Linux
- Test script to simulate failures
- `watcher.log` sample and short video or GIF
