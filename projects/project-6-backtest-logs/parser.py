import json
from collections import defaultdict
from typing import Dict, Any


def parse_jsonl(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def summarize(path: str) -> Dict[str, Any]:
    total_pnl = 0.0
    trades = 0
    pnl_by_symbol = defaultdict(float)
    trades_by_symbol = defaultdict(int)

    for rec in parse_jsonl(path):
        pnl = float(rec.get('pnl', 0.0))
        sym = rec.get('symbol', 'UNKNOWN')
        total_pnl += pnl
        trades += 1
        pnl_by_symbol[sym] += pnl
        trades_by_symbol[sym] += 1

    avg_pnl = total_pnl / trades if trades else 0.0

    return {
        'total_trades': trades,
        'total_pnl': total_pnl,
        'avg_pnl_per_trade': avg_pnl,
        'pnl_by_symbol': dict(pnl_by_symbol),
        'trades_by_symbol': dict(trades_by_symbol),
    }


if __name__ == '__main__':
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else 'logs/sample_backtest.jsonl'
    s = summarize(path)
    print(json.dumps(s, indent=2))
