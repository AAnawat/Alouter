import requests
import threading
import time
from src.infrastructure.flask.app import app


def start_app():
    app.run(port=8080)


def test_getURL():
    server = threading.Thread(target=start_app)
    server.daemon = True
    server.start()

    time.sleep(5)

    responses = [
        requests.get("http://localhost:8080/"),
        requests.get("http://localhost:8080/health-check"),
    ]

    for response in responses:
        assert response.status_code == 200
