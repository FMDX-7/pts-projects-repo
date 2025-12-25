Project 4 — GUI Job Scheduler
=============================

Quick Tkinter-based job scheduler for local demos. No external Python packages required.

Files
- `scheduler.py`: Tkinter GUI app. Run with `python scheduler.py`.
- `jobs.json`: persisted jobs (created automatically).
- `logs/`: job run logs.

How to run

1. From PowerShell in this folder run:

```powershell
python scheduler.py
```

2. Use the GUI to add jobs:
  - Add Job: provide `Name`, `Command` (shell command), and `Interval (s)`.
  - Start: starts the selected job (it will run immediately and then every N seconds).
  - Run Now: execute once immediately.
  - Open Log: opens the job log file in your default editor.

Notes
- Jobs and logs are stored under this folder (`jobs.json`, `logs/`).
- Commands are executed with the system shell (`shell=True`), so on Windows use typical PowerShell/CMD commands (e.g., `python script.py` or `dir`).
- This is a demo scheduler meant for local usage and interviews — not production-ready.

Outputs & logs

- Location: `projects/project-4-job-scheduler/logs/`
- Each job writes a log file named after the job (safe characters sanitized). Example lines from a job log:

```
2025-12-25T06:20:37.256929Z - RUN - Generator - python "generate_logs.py"
2025-12-25T06:20:57.669556Z - RUN - Generator - python cd...generate_logs.py"

```

- Interpretation:
  - `RUN` lines show the timestamp, job name, and the command executed.
  - `OUT` lines (if present) contain stdout from the command.
  - `ERR` lines contain stderr or exception traces.

Why you might see errors
- Wrong path or quoting — commands that point at a directory or use inconsistent quoting will fail (see the `can't find '__main__'` error above).
- Missing working directory — some scripts expect a `logs/` folder in their CWD; either run the script with the correct CWD or make the script create its own `logs/` folder.

How the GUI is created (implementation notes)

- Technology: the GUI is built with Tkinter (standard Python UI toolkit) — no external GUI packages required.
- Main files:
  - `scheduler.py` — the GUI application. Key classes:
    - `Job` — represents a scheduled job, runs commands in a background thread, appends to per-job log files.
    - `SchedulerApp` — Tkinter `Tk` subclass that builds the main window, holds the job list, and provides controls (Add/Edit/Start/Stop/Run Now/Open Log/Reload/Save & Exit).
    - `JobDialog` — simple modal dialog to create/edit job name, command and interval.
  - `jobs.json` — persisted job definitions loaded at startup.
  - `generate_logs.py` — included as a local demo generator script (writes to `logs/app.log` under project-4 when run locally).

- How commands are executed:
  - Commands are executed via `subprocess.run(..., shell=True, cwd=ROOT)` where `ROOT` is the scheduler folder. This ensures relative commands like `python generate_logs.py` resolve to files inside the project-4 folder.
  - Output and errors are captured and appended to the job log file.

Quick troubleshooting
- If a job fails with `can't open file` or `No such file or directory`:
  - Open the job with **Edit Job** and verify the `Command` string is a file (e.g. `python generate_logs.py`) not a directory.
  - Ensure the script exists in the project folder (we include `generate_logs.py` for the demo).
  - Click **Reload** in the GUI after changing `jobs.json` on disk (or restart the app).

Run the GUI

```powershell
cd ...
python scheduler.py
```

Add a demo `Generator` job in the GUI with:

- Name: `Generator`
- Command: `python generate_logs.py`
- Interval: `5`

Then click **Run Now** or **Start** and open `logs/app.log` to inspect generated entries.
