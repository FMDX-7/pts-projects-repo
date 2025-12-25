import time
import signal
import sys

running = True

def handler(sig, frame):
    global running
    print('sample_app shutting down')
    running = False

signal.signal(signal.SIGINT, handler)

print('sample_app started')
while running:
    print('heartbeat')
    sys.stdout.flush()
    time.sleep(5)
