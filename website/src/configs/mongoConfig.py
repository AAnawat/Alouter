import os

config = {
    "username": os.environ.get("MONGO_USERNAME"),
    "password": os.environ.get("MONGO_PASSWORD"),
    "host": os.environ.get("MONGO_HOST"),
    "port": os.environ.get("MONGO_PORT"),
}