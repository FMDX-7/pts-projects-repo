# Project 5 — Order Routing Simulator (Flask in-memory)

Purpose

- Small, self-contained simulator demonstrating an order-routing REST API.

Components

- `simulator/router.py`: `InMemoryRouter` — stores orders in memory and simulates execution/fills.
- `simulator/app.py`: Flask HTTP API that exposes `POST /orders`, `GET /orders`, and `GET /orders/<id>` backed by the router.
- `run_simulator.py`: helper to start the Flask app without the development reloader.
- `sample_client.py`: example client that posts sample orders to the API.
- `requirements.txt`: Python dependencies.

How the pieces work together

- The client (`sample_client.py`) sends an HTTP POST to `POST /orders` with JSON order data.
- The Flask app (`simulator/app.py`) receives the request and calls `InMemoryRouter.submit()`.
- `InMemoryRouter.submit()` assigns an `id`, records `received_at`, marks the order `accepted`, and then immediately simulates an `execution` (a filled event) which is attached to the order object and stored in memory.
- The API returns the order JSON (including the `execution` block). `GET /orders` returns all stored orders from the router.

Quick start (generic)

1. Open a shell and change to the project folder:

```powershell
cd projects/project-5-order-routing
```

2. (Optional) Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # PowerShell
# or on macOS/Linux: source .venv/bin/activate
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Start the simulator (in one shell):

```powershell
python run_simulator.py
```

5. Run the sample client (in another shell):

```powershell
python sample_client.py
```

6. Inspect stored orders:

```powershell
Invoke-RestMethod http://127.0.0.1:5000/orders
# or use curl: curl http://127.0.0.1:5000/orders
```

What you should see

- The client prints responses with HTTP status `201` and a JSON order object that includes an `execution` block (`avg_price`, `filled_qty`, `destination`).
- `GET /orders` returns a JSON array of the in-memory orders.
- Orders are stored in memory only — they are lost when the server stops.

Files to inspect

- `simulator/app.py` — Flask routes and API glue.
- `simulator/router.py` — in-memory router and simulated fill logic.
- `run_simulator.py` — helper used to run the server without the reloader.
- `sample_client.py` — example client that posts orders.

Next steps (optional)

- Add persistent logging (append orders to a file) or a small SQLite backend if you want orders to survive restarts.
- Add a broker-backed demo (RabbitMQ/Redis Streams) and a `docker-compose.yml` to run the broker locally.


