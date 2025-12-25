from prometheus_client import start_http_server, Gauge
import time

heartbeat = Gauge('pts_service_heartbeat', 'Heartbeat metric for demo')

if __name__ == '__main__':
    start_http_server(8000)
    while True:
        heartbeat.set(1)
        time.sleep(5)
