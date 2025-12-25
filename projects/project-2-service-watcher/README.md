# Project 2 — Service Watcher

Purpose

- Demonstrate on-host automation to detect and recover failed services (PowerShell for Windows, Bash/systemd for Linux).

Primary tech

- PowerShell, Bash, systemd, Windows Service management

Run / Demo

1. Run the watcher script on the host (PowerShell):

```powershell
cd projects/project-2-service-watcher
.\service_watcher.ps1 -Mode process -ProcessName sample_app -StartCommand "python sample_app.py" -IntervalSeconds 5
```

2. Simulate a service stop and verify watcher restarts it and logs the event.

What to include

- `service_watcher.ps1` with logging and restart logic
- `service_watcher.sh` equivalent for Linux
- Test script to simulate failures
- `watcher.log` sample and short video or GIF

Quick test (process mode):

1. Open a PowerShell in the repo root and run the sample app in the background:

```powershell
cd projects/project-2-service-watcher
# start a sample app (in a separate terminal) for the watcher to monitor
python sample_app.py
```

2. In another PowerShell run the watcher (process mode):

```powershell
.\service_watcher.ps1 -Mode process -ProcessName sample_app -StartCommand "python sample_app.py" -IntervalSeconds 5
```

3. Kill the sample app (in the first terminal) and observe `watcher.log` — the watcher will attempt to restart it.

Linux test (process mode):

```bash
cd projects/project-2-service-watcher
python3 sample_app.py &
./service_watcher.sh process sample_app 5 "python3 sample_app.py"
```

Notes

- Use the `service` mode with real system services: `./service_watcher.sh service nginx 15` or `service_watcher.ps1 -Mode service -ServiceName Spooler`.
- The watcher logs to `watcher.log` in the same folder.
