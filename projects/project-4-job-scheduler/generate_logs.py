import os
import time
import random
from datetime import datetime

BASE_DIR = os.path.dirname(__file__)
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOGFILE = os.path.join(LOG_DIR, "app.log")

levels = ["INFO", "WARN", "ERROR", "DEBUG"]

with open(LOGFILE, "a", encoding="utf-8") as f:
    for i in range(1000):
        ts = datetime.utcnow().isoformat() + "Z"
        level = random.choice(levels)
        msg = f"{ts} - {level} - heartbeat - iteration={i}\n"
        f.write(msg)
        f.flush()
        time.sleep(2)
import time
import random
from datetime import datetime

LOGFILE = 'logs/Generator.log'

levels = ['INFO','WARN','ERROR','DEBUG']

with open(LOGFILE, 'a', encoding='utf-8') as f:
    for i in range(1000):
        ts = datetime.utcnow().isoformat() + 'Z'
        level = random.choice(levels)
        msg = f"{ts} - {level} - heartbeat - iteration={i}\n"
        f.write(msg)
        f.flush()
        time.sleep(2)
