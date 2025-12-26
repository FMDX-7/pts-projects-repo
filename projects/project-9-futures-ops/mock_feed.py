import json
import random
import time

STATE_FILE = 'feed_state.json'
SYMS = ['ES', 'NQ']


def write_state():
    now = time.time()
    data = []
    for sym in SYMS:
        price = round(random.uniform(4000, 5000), 2) if sym == 'ES' else round(random.uniform(15000, 18000), 2)
        data.append({'symbol': sym, 'last': price, 'ts': now})
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump({'ts': now, 'quotes': data}, f)


def main():
    print('Mock futures feed running. Ctrl+C to stop.')
    try:
        while True:
            write_state()
            time.sleep(2)
    except KeyboardInterrupt:
        print('Stopped')


if __name__ == '__main__':
    main()
