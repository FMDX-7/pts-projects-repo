import json
import time
from typing import Dict, Any


INCIDENTS_FILE = 'incidents.jsonl'


def log_incident(payload: Dict[str, Any]) -> Dict[str, Any]:
    rec = dict(payload)
    rec['timestamp'] = time.time()
    with open(INCIDENTS_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(rec) + '\n')
    return rec


def read_incidents():
    out = []
    try:
        with open(INCIDENTS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    out.append(json.loads(line))
    except FileNotFoundError:
        return []
    return out
