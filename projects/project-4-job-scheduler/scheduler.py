import json
import os
import threading
import subprocess
import time
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from tkinter import ttk

ROOT = os.path.dirname(__file__)
JOBS_FILE = os.path.join(ROOT, "jobs.json")
LOGS_DIR = os.path.join(ROOT, "logs")

os.makedirs(LOGS_DIR, exist_ok=True)


class Job:
    def __init__(self, name, command, interval, enabled=True):
        self.name = name
        self.command = command
        self.interval = int(interval)
        self.enabled = bool(enabled)
        self._stop_event = threading.Event()
        self._thread = None
        self.status = "stopped"

    def to_dict(self):
        return {
            "name": self.name,
            "command": self.command,
            "interval": self.interval,
            "enabled": self.enabled,
        }

    def _log_path(self):
        safe = "".join(c for c in self.name if c.isalnum() or c in ("-", "_", " ")).rstrip()
        return os.path.join(LOGS_DIR, f"{safe}.log")

    def _append_log(self, text):
        with open(self._log_path(), "a", encoding="utf-8") as f:
            f.write(text + "\n")

    def _run_once(self):
        ts = datetime.utcnow().isoformat() + "Z"
        header = f"{ts} - RUN - {self.name} - {self.command}"
        self._append_log(header)
        try:
            res = subprocess.run(
                self.command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300,
                cwd=ROOT,
            )
            out = res.stdout.strip()
            err = res.stderr.strip()
            if out:
                for line in out.splitlines():
                    self._append_log(f"{ts} - OUT - {line}")
            if err:
                for line in err.splitlines():
                    self._append_log(f"{ts} - ERR - {line}")
        except Exception as e:
            self._append_log(f"{ts} - EXC - {e}")

    def _run_loop(self):
        self.status = "running"
        while not self._stop_event.is_set():
            self._run_once()
            # wait with small sleep so we can be responsive to stop
            waited = 0
            while waited < self.interval and not self._stop_event.is_set():
                time.sleep(0.5)
                waited += 0.5
        self.status = "stopped"

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def stop(self):
        if self._thread and self._thread.is_alive():
            self._stop_event.set()
            self._thread.join(timeout=1)

    def run_now(self):
        t = threading.Thread(target=self._run_once, daemon=True)
        t.start()


class SchedulerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Job Scheduler")
        self.geometry("800x480")
        self.jobs = []
        self._load_jobs()
        self._build_ui()
        self._refresh_ui()

    def _load_jobs(self):
        if os.path.exists(JOBS_FILE):
            try:
                with open(JOBS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for j in data:
                    job = Job(j["name"], j["command"], j.get("interval", 60), j.get("enabled", True))
                    self.jobs.append(job)
            except Exception:
                messagebox.showwarning("Load jobs", "Failed to load jobs.json, starting empty.")

    def _save_jobs(self):
        data = [j.to_dict() for j in self.jobs]
        with open(JOBS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def _build_ui(self):
        frm = ttk.Frame(self)
        frm.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        cols = ("name", "command", "interval", "status")
        self.tree = ttk.Treeview(frm, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c.title())
            self.tree.column(c, anchor=tk.W, width=200)
        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        ctrl = ttk.Frame(frm)
        ctrl.pack(fill=tk.Y, side=tk.RIGHT, padx=6)

        ttk.Button(ctrl, text="Add Job", command=self._add_job).pack(fill=tk.X, pady=2)
        ttk.Button(ctrl, text="Edit Job", command=self._edit_job).pack(fill=tk.X, pady=2)
        ttk.Button(ctrl, text="Remove Job", command=self._remove_job).pack(fill=tk.X, pady=2)
        ttk.Separator(ctrl).pack(fill=tk.X, pady=4)
        ttk.Button(ctrl, text="Start", command=self._start_selected).pack(fill=tk.X, pady=2)
        ttk.Button(ctrl, text="Stop", command=self._stop_selected).pack(fill=tk.X, pady=2)
        ttk.Button(ctrl, text="Run Now", command=self._run_selected_once).pack(fill=tk.X, pady=2)
        ttk.Separator(ctrl).pack(fill=tk.X, pady=4)
        ttk.Button(ctrl, text="Open Log", command=self._open_log).pack(fill=tk.X, pady=2)
        ttk.Button(ctrl, text="Reload", command=self._refresh_ui).pack(fill=tk.X, pady=2)
        ttk.Button(ctrl, text="Save & Exit", command=self._on_exit).pack(fill=tk.X, pady=12)

    def _refresh_ui(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for j in self.jobs:
            self.tree.insert("", tk.END, values=(j.name, j.command, j.interval, j.status))

    def _add_job(self):
        dlg = JobDialog(self, None)
        self.wait_window(dlg)
        if dlg.result:
            name, cmd, interval = dlg.result
            job = Job(name, cmd, interval)
            self.jobs.append(job)
            self._save_jobs()
            self._refresh_ui()

    def _edit_job(self):
        sel = self.tree.selection()
        if not sel:
            return
        idx = self.tree.index(sel[0])
        job = self.jobs[idx]
        dlg = JobDialog(self, job)
        self.wait_window(dlg)
        if dlg.result:
            name, cmd, interval = dlg.result
            job.name = name
            job.command = cmd
            job.interval = int(interval)
            self._save_jobs()
            self._refresh_ui()

    def _remove_job(self):
        sel = self.tree.selection()
        if not sel:
            return
        idx = self.tree.index(sel[0])
        job = self.jobs.pop(idx)
        try:
            job.stop()
        except Exception:
            pass
        self._save_jobs()
        self._refresh_ui()

    def _start_selected(self):
        sel = self.tree.selection()
        if not sel:
            return
        idx = self.tree.index(sel[0])
        job = self.jobs[idx]
        job.start()
        self._refresh_ui()

    def _stop_selected(self):
        sel = self.tree.selection()
        if not sel:
            return
        idx = self.tree.index(sel[0])
        job = self.jobs[idx]
        job.stop()
        self._refresh_ui()

    def _run_selected_once(self):
        sel = self.tree.selection()
        if not sel:
            return
        idx = self.tree.index(sel[0])
        job = self.jobs[idx]
        job.run_now()

    def _open_log(self):
        sel = self.tree.selection()
        if not sel:
            return
        idx = self.tree.index(sel[0])
        job = self.jobs[idx]
        path = job._log_path()
        if os.path.exists(path):
            os.startfile(path)
        else:
            messagebox.showinfo("Log", "Log file does not exist yet.")

    def _on_exit(self):
        # stop all jobs
        for j in self.jobs:
            try:
                j.stop()
            except Exception:
                pass
        self._save_jobs()
        self.destroy()


class JobDialog(tk.Toplevel):
    def __init__(self, parent, job=None):
        super().__init__(parent)
        self.title("Job")
        self.result = None
        self.transient(parent)
        self.grab_set()

        ttk.Label(self, text="Name").grid(row=0, column=0, sticky=tk.W)
        self.name_e = ttk.Entry(self, width=60)
        self.name_e.grid(row=0, column=1, pady=4, padx=4)

        ttk.Label(self, text="Command").grid(row=1, column=0, sticky=tk.W)
        self.cmd_e = ttk.Entry(self, width=60)
        self.cmd_e.grid(row=1, column=1, pady=4, padx=4)

        ttk.Label(self, text="Interval (s)").grid(row=2, column=0, sticky=tk.W)
        self.int_e = ttk.Entry(self, width=20)
        self.int_e.grid(row=2, column=1, sticky=tk.W, pady=4, padx=4)

        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=8)
        ttk.Button(btn_frame, text="OK", command=self._ok).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text="Cancel", command=self._cancel).pack(side=tk.LEFT, padx=4)

        if job:
            self.name_e.insert(0, job.name)
            self.cmd_e.insert(0, job.command)
            self.int_e.insert(0, str(job.interval))

    def _ok(self):
        name = self.name_e.get().strip()
        cmd = self.cmd_e.get().strip()
        interval = self.int_e.get().strip() or "60"
        if not name or not cmd:
            messagebox.showerror("Invalid", "Name and command are required")
            return
        try:
            ival = int(interval)
            if ival <= 0:
                raise ValueError()
        except Exception:
            messagebox.showerror("Invalid", "Interval must be a positive integer (seconds)")
            return
        self.result = (name, cmd, ival)
        self.destroy()

    def _cancel(self):
        self.result = None
        self.destroy()


def main():
    app = SchedulerApp()
    app.protocol("WM_DELETE_WINDOW", app._on_exit)
    app.mainloop()


if __name__ == "__main__":
    main()
