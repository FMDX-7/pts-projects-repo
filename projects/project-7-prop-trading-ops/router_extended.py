import time
import random
from typing import Dict, Any


class RouterExtended:
    """Order router that supports asset classes and simulates routing behavior."""
    def __init__(self):
        self.orders: Dict[str, Dict[str, Any]] = {}

    def submit(self, order: Dict[str, Any]) -> Dict[str, Any]:
        order_id = order.get("id") or str(int(time.time() * 1000))
        o = dict(order)
        o["id"] = order_id
        o["received_at"] = time.time()
        o["status"] = "accepted"
        asset = o.get("asset_class", "EQUITY").upper()
        # choose destination based on asset class
        if asset == "OPTIONS":
            dest = "OPTIONS_GATEWAY"
        elif asset == "FUTURES":
            dest = "FUTURES_GATEWAY"
        else:
            dest = "EQUITY_EXCHANGE"
        # simulate execution
        fill = {
            "status": "filled",
            "filled_qty": o.get("qty", 0),
            "avg_price": round(o.get("price", random.uniform(1, 200)), 2),
            "destination": dest,
        }
        o["execution"] = fill
        o["status"] = "filled"
        self.orders[order_id] = o
        return o

    def get(self, order_id: str):
        return self.orders.get(order_id)

    def list_all(self):
        return list(self.orders.values())
