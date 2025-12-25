#!/usr/bin/env bash
# Simple service/process watcher for Linux
# Usage examples:
#  ./service_watcher.sh service nginx 15
#  ./service_watcher.sh process myapp 10 "/usr/bin/python3 /opt/myapp/app.py"

MODE="$1"          # service | process
NAME="$2"
INTERVAL="${3:-10}"
STARTCMD="${4}"
LOGFILE="./watcher.log"

log() {
  echo "$(date -Is) - $1" | tee -a "$LOGFILE"
}

if [ -z "$MODE" ] || [ -z "$NAME" ]; then
  echo "Usage: $0 <service|process> <name> [interval_seconds] [start_command]"
  exit 1
fi

log "Starting watcher (mode=$MODE, name=$NAME, interval=${INTERVAL}s)"

while true; do
  if [ "$MODE" = "service" ]; then
    if systemctl is-active --quiet "$NAME"; then
      log "Service $NAME is active"
    else
      log "Service $NAME is not active — attempting restart"
      systemctl restart "$NAME" && log "Restarted $NAME" || log "Failed to restart $NAME"
    fi
  else
    # process mode
    if pgrep -f "$NAME" > /dev/null; then
      log "Process $NAME running"
    else
      log "Process $NAME not running"
      if [ -n "$STARTCMD" ]; then
        log "Starting: $STARTCMD"
        bash -c "$STARTCMD &" >/dev/null 2>&1
        sleep 1
        if pgrep -f "$NAME" > /dev/null; then
          log "Started $NAME"
        else
          log "Failed to start $NAME"
        fi
      else
        log "No start command provided for process mode"
      fi
    fi
  fi
  sleep "$INTERVAL"
done
