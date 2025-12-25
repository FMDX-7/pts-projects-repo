import time
import random
from datetime import datetime

LOGFILE = 'logs/app.log'

levels = ['INFO','WARN','ERROR','DEBUG']

with open(LOGFILE, 'a', encoding='utf-8') as f:
    for i in range(1000):
        ts = datetime.utcnow().isoformat() + 'Z'
        level = random.choice(levels)
        msg = f"{ts} - {level} - heartbeat - iteration={i}\n"
        f.write(msg)
        f.flush()
        time.sleep(2)
