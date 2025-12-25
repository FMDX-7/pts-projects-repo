from flask import Flask, request, jsonify
from simulator.router import InMemoryRouter

app = Flask(__name__)
router = InMemoryRouter()


@app.route("/orders", methods=["POST"])
def submit_order():
    order = request.get_json(force=True)
    res = router.submit(order)
    return jsonify(res), 201


@app.route("/orders", methods=["GET"])
def list_orders():
    return jsonify(router.list_all())


@app.route("/orders/<order_id>", methods=["GET"])
def get_order(order_id):
    order = router.get(order_id)
    if not order:
        return jsonify({"error": "not found"}), 404
    return jsonify(order)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
