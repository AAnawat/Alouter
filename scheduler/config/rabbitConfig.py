import os

config = {
    "username": os.environ.get("RABBITMQ_USER"),
    "password": os.environ.get("RABBITMQ_PASS"),
    "host": os.environ.get("RABBITMQ_HOST"),
}
