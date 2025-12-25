import time
import random
from typing import Dict, Any


class InMemoryRouter:
    """Simple in-memory order router that accepts orders and simulates an execution."""
    def __init__(self):
        self.orders: Dict[str, Dict[str, Any]] = {}

    def submit(self, order: Dict[str, Any]) -> Dict[str, Any]:
        order_id = order.get("id") or str(int(time.time() * 1000))
        o = dict(order)
        o["id"] = order_id
        o["received_at"] = time.time()
        o["status"] = "accepted"
        # store initial state
        self.orders[order_id] = o

        # simulate a routing/filled event (synchronous, for demo)
        fill = {
            "status": "filled",
            "filled_qty": o.get("qty", 0),
            "avg_price": round(o.get("price", random.uniform(10, 100)), 2),
            "destination": "SIMEX",
        }
        o["execution"] = fill
        o["status"] = "filled"
        return o

    def get(self, order_id: str):
        return self.orders.get(order_id)

    def list_all(self):
        return list(self.orders.values())
