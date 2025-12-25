import time
import requests
import incident_logger

HEALTH_URL = 'http://127.0.0.1:8080/health'
POLL_INTERVAL = 5


def check_once():
    try:
        r = requests.get(HEALTH_URL, timeout=2)
        if r.status_code != 200:
            incident_logger.log_incident({'type': 'health_check_failed', 'status_code': r.status_code})
            print('Health check failed:', r.status_code)
        else:
            print('Health OK')
    except Exception as e:
        incident_logger.log_incident({'type': 'health_check_error', 'error': str(e)})
        print('Health check error:', e)


def main():
    print('Starting monitor poller (press CTRL+C to stop)')
    try:
        while True:
            check_once()
            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        print('Stopping')


if __name__ == '__main__':
    main()
