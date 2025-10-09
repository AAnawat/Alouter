from pymongo import MongoClient
from ...configs.mongoConfig import config


client = MongoClient(f"mongodb://${config.username}:${config.password}@${config.host}:${config.port}")

router_db = client["router"]