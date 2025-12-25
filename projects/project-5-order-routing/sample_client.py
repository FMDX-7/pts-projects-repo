import time
import requests

BASE = "http://127.0.0.1:5000"


def send_sample(symbol="ABC", qty=100, side="BUY"):
    payload = {"symbol": symbol, "qty": qty, "side": side}
    r = requests.post(f"{BASE}/orders", json=payload)
    print("Status:", r.status_code)
    print(r.json())


if __name__ == "__main__":
    for i in range(3):
        send_sample(symbol=f"SYM{i}", qty=100 + i * 10)
        time.sleep(0.5)
