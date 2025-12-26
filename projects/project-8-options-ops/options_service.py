import json
import os
import time
from typing import Dict, Any, List

from flask import Flask, request, jsonify, send_from_directory

import incident_logger

app = Flask(__name__)


class OptionsRouter:
    def __init__(self):
        self.orders: Dict[str, Dict[str, Any]] = {}
        self.next_id = 1
        self.max_notional_per_order = 50_000
        self.max_open_orders = 200

    def _new_id(self) -> str:
        oid = str(self.next_id)
        self.next_id += 1
        return oid

    def _risk_check(self, order_notional: float):
        if order_notional > self.max_notional_per_order:
            incident_logger.log_incident({'type': 'risk_reject_notional', 'notional': order_notional})
            return False, 'notional_limit'
        if len(self.orders) >= self.max_open_orders:
            incident_logger.log_incident({'type': 'risk_reject_capacity', 'open_orders': len(self.orders)})
            return False, 'capacity_limit'
        return True, None

    def submit_single(self, order: Dict[str, Any]) -> Dict[str, Any]:
        price = float(order.get('price', 0))
        qty = float(order.get('qty', 0))
        notional = price * qty * 100  # options contract multiplier
        ok, reason = self._risk_check(notional)
        if not ok:
            return {'status': 'rejected', 'reason': reason}

        oid = self._new_id()
        o = dict(order)
        o['id'] = oid
        o['received_at'] = time.time()
        o['status'] = 'filled'
        o['execution'] = {
            'status': 'filled',
            'filled_qty': qty,
            'avg_price': round(price, 4),
            'destination': 'OPTIONS_GATEWAY',
        }
        self.orders[oid] = o
        return o

    def submit_multi(self, order: Dict[str, Any]) -> Dict[str, Any]:
        legs: List[Dict[str, Any]] = order.get('legs') or []
        # crude combined notional
        notional = 0.0
        for leg in legs:
            price = float(leg.get('price', 0))
            qty = float(leg.get('qty', 0))
            notional += price * abs(qty) * 100
        ok, reason = self._risk_check(notional)
        if not ok:
            return {'status': 'rejected', 'reason': reason}

        oid = self._new_id()
        o = dict(order)
        o['id'] = oid
        o['received_at'] = time.time()
        o['status'] = 'filled'
        o['legs'] = legs
        o['execution'] = {
            'status': 'filled',
            'filled_notional': round(notional, 2),
            'destination': 'OPTIONS_GATEWAY',
        }
        self.orders[oid] = o
        return o

    def list_all(self):
        return list(self.orders.values())


router = OptionsRouter()


def feed_status():
    path = 'quotes_state.json'
    if not os.path.exists(path):
        return {'status': 'stale', 'age_sec': None}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        ts = float(data.get('ts', 0))
        age = time.time() - ts
        return {'status': 'ok' if age < 10 else 'stale', 'age_sec': round(age, 2)}
    except Exception as e:
        return {'status': 'error', 'error': str(e)}


@app.route('/health', methods=['GET'])
def health():
    fs = feed_status()
    status = 'ok' if fs.get('status') == 'ok' else 'degraded'
    return jsonify({'status': status, 'feed': fs})


@app.route('/metrics', methods=['GET'])
def metrics():
    return jsonify({
        'orders_count': len(router.orders),
        'max_notional_per_order': router.max_notional_per_order,
        'max_open_orders': router.max_open_orders,
    })


@app.route('/quotes/status', methods=['GET'])
def quotes_status():
    return jsonify(feed_status())


@app.route('/orders', methods=['POST'])
def post_order():
    payload = request.get_json(force=True)
    res = router.submit_single(payload)
    if res.get('status') == 'rejected':
        return jsonify(res), 400
    return jsonify(res), 201


@app.route('/orders/multi', methods=['POST'])
def post_multi():
    payload = request.get_json(force=True)
    res = router.submit_multi(payload)
    if res.get('status') == 'rejected':
        return jsonify(res), 400
    return jsonify(res), 201


@app.route('/orders', methods=['GET'])
def list_orders():
    return jsonify(router.list_all())


@app.route('/incidents', methods=['GET'])
def get_incidents():
    return jsonify(incident_logger.read_incidents())


@app.route('/simulate-incident', methods=['POST'])
def simulate_incident():
    data = request.get_json(force=True)
    inc = incident_logger.log_incident(data)
    return jsonify(inc), 201


@app.route('/dashboard', methods=['GET'])
def dashboard():
    return send_from_directory('static', 'dashboard.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8081, debug=False)
