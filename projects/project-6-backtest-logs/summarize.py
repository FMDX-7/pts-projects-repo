from backtest_parser import summarize
import json


def main():
    s = summarize('logs/sample_backtest.jsonl')
    print('Backtest summary (sample_backtest.jsonl):')
    print(json.dumps(s, indent=2))


if __name__ == '__main__':
    main()
