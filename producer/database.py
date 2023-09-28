from pymongo.mongo_client import MongoClient
from dotenv import dotenv_values

config = dotenv_values(".env")

client = MongoClient(config["DATABASE_URI"])
print('Connected to MongoDB...')

db = client[config["DATABASE_NAME"]]
Products = db.products
Orders = db.orders
