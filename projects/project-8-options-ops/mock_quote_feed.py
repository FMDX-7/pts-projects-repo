import json
import random
import time

STATE_FILE = 'quotes_state.json'
SYMS = ['AAPL', 'SPY']


def write_state():
    now = time.time()
    quotes = []
    for sym in SYMS:
        bid = round(random.uniform(50, 300), 2)
        ask = bid + round(random.uniform(0.1, 0.5), 2)
        quotes.append({'underlying': sym, 'bid': bid, 'ask': ask, 'ts': now})
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump({'ts': now, 'quotes': quotes}, f)


def main():
    print('Mock quote feed running. Press Ctrl+C to stop.')
    try:
        while True:
            write_state()
            time.sleep(2)
    except KeyboardInterrupt:
        print('Stopped')


if __name__ == '__main__':
    main()
