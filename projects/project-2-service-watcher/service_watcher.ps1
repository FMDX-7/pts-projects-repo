<#
.SYNOPSIS
  Simple service/process watcher for Windows (PowerShell).

.DESCRIPTION
  Monitors a Windows Service or arbitrary process and attempts to restart it when stopped.
  Writes events to a log file (`watcher.log` by default).

.EXAMPLES
  # Watch a Windows service by name and check every 15 seconds
  .\service_watcher.ps1 -Mode service -ServiceName "Spooler" -IntervalSeconds 15

  # Watch a process (by process name) and start it with a command if missing
  .\service_watcher.ps1 -Mode process -ProcessName "python" -StartCommand "C:\Python39\python.exe C:\path\to\sample_app.py" -IntervalSeconds 10
#>

param(
    [Parameter(Mandatory=$true)][ValidateSet("service","process")] [string]$Mode,
    [string]$ServiceName,
    [string]$ProcessName,
    [string]$StartCommand,
    [int]$IntervalSeconds = 10,
    [string]$LogFile = "./watcher.log"
)

function Write-Log {
    param([string]$Message)
    $timestamp = (Get-Date).ToString('s')
    $line = "$timestamp - $Message"
    $line | Out-File -FilePath $LogFile -Append -Encoding UTF8
    Write-Output $line
}

Write-Log "Starting watcher (Mode=$Mode, Interval=${IntervalSeconds}s)"

while ($true) {
    try {
        if ($Mode -eq 'service') {
            if (-not $ServiceName) { Write-Log "Error: -ServiceName is required for service mode"; break }
            $svc = Get-Service -Name $ServiceName -ErrorAction SilentlyContinue
            if (-not $svc) {
                Write-Log "Service '$ServiceName' not found"
            } else {
                if ($svc.Status -ne 'Running') {
                    Write-Log "Service '$ServiceName' status: $($svc.Status). Attempting Start-Service..."
                    try {
                        Start-Service -Name $ServiceName -ErrorAction Stop
                        Write-Log "Service '$ServiceName' started"
                    } catch {
                        Write-Log "Failed to start service '$ServiceName': $_"
                    }
                } else {
                    Write-Log "Service '$ServiceName' is running"
                }
            }
        } else {
            if (-not $ProcessName) { Write-Log "Error: -ProcessName is required for process mode"; break }
            $proc = Get-Process -Name $ProcessName -ErrorAction SilentlyContinue
            if (-not $proc) {
                # No process matched by executable name — try matching process command line (useful for scripts run by python)
                try {
                    $lowerName = $ProcessName.ToLower()
                    $procInfo = Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -and $_.CommandLine.ToLower().Contains($lowerName) } | Select-Object -First 1
                    if ($procInfo) {
                        $proc = Get-Process -Id $procInfo.ProcessId -ErrorAction SilentlyContinue
                    }
                } catch {
                    # ignore CIM errors and proceed
                }

                if (-not $proc) {
                    Write-Log "Process '$ProcessName' not running."
                    if ($StartCommand) {
                        Write-Log "Starting process with command: $StartCommand"
                        try {
                            # Parse StartCommand into executable and arguments so we can start the executable directly
                            $exe = $null; $args = $null
                            if ($StartCommand -match '^\s*"([^"]+)"\s*(.*)$') { $exe = $matches[1]; $args = $matches[2].Trim() }
                            elseif ($StartCommand -match '^\s*([^\s]+)\s*(.*)$') { $exe = $matches[1]; $args = $matches[2].Trim() }

                            if (-not $exe) { throw 'Unable to parse StartCommand' }

                            # Prefer starting the executable directly (avoid cmd.exe wrapper)
                            if ($args) {
                                $argList = $args -split ' ' | Where-Object { $_ -ne '' }
                                Start-Process -FilePath $exe -ArgumentList $argList -WorkingDirectory (Get-Location) -WindowStyle Hidden -ErrorAction Stop
                            } else {
                                Start-Process -FilePath $exe -WorkingDirectory (Get-Location) -WindowStyle Hidden -ErrorAction Stop
                            }

                            # Give process a small grace period and verify it started by re-checking command line
                            Start-Sleep -Seconds 2
                            $procInfo2 = Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -and $_.CommandLine.ToLower().Contains($lowerName) } | Select-Object -First 1
                            if ($procInfo2) {
                                Write-Log "Started process via command (PID $($procInfo2.ProcessId))"
                                $proc = Get-Process -Id $procInfo2.ProcessId -ErrorAction SilentlyContinue
                            } else {
                                Write-Log "Started process but could not verify via command line match"
                            }
                        } catch {
                            Write-Log "Failed to start process: $_"
                        }
                    } else {
                        Write-Log "No -StartCommand provided; cannot start process"
                    }
                }
            } else {
                Write-Log "Process '$ProcessName' running (PID $($proc.Id))"
            }
        }
    } catch {
        Write-Log "Watcher error: $_"
    }
    Start-Sleep -Seconds $IntervalSeconds
}
