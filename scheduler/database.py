from pymongo import MongoClient
from config.mongoConfig import config


client = MongoClient(
    f"mongodb://{config['username']}:{config['password']}@{config['host']}:{config['port']}"  # noqa: E501
)

router_db = client["router"]
