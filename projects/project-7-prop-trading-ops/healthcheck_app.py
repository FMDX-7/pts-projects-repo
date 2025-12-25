from flask import Flask, request, jsonify, send_from_directory
from router_extended import RouterExtended
import incident_logger

app = Flask(__name__)
router = RouterExtended()


@app.route('/health', methods=['GET'])
def health():
    # simple simulated health state; in a real system this would check dependencies
    return jsonify({"status": "ok"})


@app.route('/metrics', methods=['GET'])
def metrics():
    # minimal metric: number of orders
    return jsonify({"orders_count": len(router.list_all())})


@app.route('/orders', methods=['POST'])
def submit_order():
    order = request.get_json(force=True)
    res = router.submit(order)
    return jsonify(res), 201


@app.route('/orders', methods=['GET'])
def list_orders():
    return jsonify(router.list_all())


@app.route('/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    o = router.get(order_id)
    if not o:
        return jsonify({"error": "not found"}), 404
    return jsonify(o)


@app.route('/simulate-incident', methods=['POST'])
def simulate_incident():
    data = request.get_json(force=True)
    incident = incident_logger.log_incident(data)
    return jsonify(incident), 201


@app.route('/incidents', methods=['GET'])
def get_incidents():
    return jsonify(incident_logger.read_incidents())


@app.route('/dashboard', methods=['GET'])
def dashboard():
    # serve the static dashboard page
    return send_from_directory('static', 'dashboard.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=False)
