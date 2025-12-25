# Project 2 — Service Watcher

## Purpose

Demonstrate on-host automation to detect and recover failed services/processes. Shows monitoring, logging, and automatic restart capabilities for production support roles.

## Primary Tech

- PowerShell (Windows), Bash (Linux)
- Process monitoring, systemd integration
- Logging and alerting patterns

## What's Included

- `service_watcher.ps1` — PowerShell watcher with process/service monitoring and auto-restart
- `service_watcher.sh` — Bash equivalent for Linux
- `sample_app.py` — Demo Python app that prints heartbeat for testing
- `watcher.log` — Output log showing detection and restart events

---

## Quick Start (Windows)

### 1. See the heartbeat app running

Open PowerShell and navigate to this project:

```powershell
cd path\to\pts-projects-repo\projects\project-2-service-watcher
python sample_app.py
```

You'll see:
```
sample_app started
heartbeat
heartbeat
...
```

Press `Ctrl+C` to stop it.

### 2. Run the watcher (foreground mode)

In the same terminal, start the watcher to monitor and auto-restart `sample_app`:

```powershell
.\service_watcher.ps1 -Mode process -ProcessName sample_app -StartCommand "python sample_app.py" -IntervalSeconds 5
```

Output:
```
2025-12-24T22:39:36 - Starting watcher (Mode=process, Interval=5s)
2025-12-24T22:39:37 - Process 'sample_app' running (PID 12345)
2025-12-24T22:39:42 - Process 'sample_app' running (PID 12345)
...
```

The watcher checks every 5 seconds. If the process stops, it will restart it automatically.

### 3. Test auto-restart (demo recovery)

Open a second PowerShell terminal:

```powershell
# Find and kill the sample_app process
Get-Process python | Where-Object { $_.CommandLine -like '*sample_app.py*' } | Stop-Process -Force
```

Watch the watcher terminal — it will detect the process stopped and restart it:
```
2025-12-24T22:40:15 - Process 'sample_app' not running.
2025-12-24T22:40:15 - Starting process with command: python sample_app.py
2025-12-24T22:40:17 - Started process via command (PID 67890)
2025-12-24T22:40:20 - Process 'sample_app' running (PID 67890)
```

### 4. Run watcher in background

To run the watcher as a background process:

```powershell
Start-Process pwsh -ArgumentList '-NoProfile','-File','.\service_watcher.ps1','-Mode','process','-ProcessName','sample_app','-StartCommand','python sample_app.py','-IntervalSeconds','5' -WindowStyle Hidden
```

Check logs:
```powershell
Get-Content .\watcher.log -Tail 20 -Wait
```

---

## Quick Start (Linux)

```bash
cd path/to/pts-projects-repo/projects/project-2-service-watcher

# Start watcher (foreground)
./service_watcher.sh process sample_app 5 "python3 sample_app.py"

# Or in background
./service_watcher.sh process sample_app 5 "python3 sample_app.py" &

# View logs
tail -f watcher.log
```

---

## Advanced Usage

### Monitor a Windows Service

```powershell
.\service_watcher.ps1 -Mode service -ServiceName "Spooler" -IntervalSeconds 15
```

### Monitor a Linux System Service

```bash
./service_watcher.sh service nginx 15
```

---

## Parameters

**PowerShell (`service_watcher.ps1`)**:
- `-Mode`: `service` or `process`
- `-ServiceName`: Windows service name (required for service mode)
- `-ProcessName`: Process name to monitor (required for process mode)
- `-StartCommand`: Command to start the process if not running
- `-IntervalSeconds`: Polling interval (default: 10)
- `-LogFile`: Log file path (default: `./watcher.log`)

**Bash (`service_watcher.sh`)**:
- First arg: `service` or `process`
- Second arg: Service/process name
- Third arg: Interval in seconds
- Fourth arg: Start command (for process mode)

---

## Comprehension

- **Problem**: Services crash in production; manual restarts cause downtime
- **Solution**: Automated watcher detects failures and restarts services within seconds
- **Logging**: All events logged to `watcher.log` for auditing and troubleshooting
- **Cross-platform**: PowerShell for Windows, Bash for Linux
- **Production-ready**: Can be deployed as Windows Task Scheduler job or Linux systemd service
