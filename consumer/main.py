from confluent_kafka import Consumer
from pymongo.mongo_client import MongoClient
from dotenv import dotenv_values
from datetime import datetime as dt
import json
from bson import ObjectId

config = dotenv_values(".env")

client = MongoClient(config["DATABASE_URI"])
print("Connected to MongoDB...")

db = client[config["DATABASE_NAME"]]
Products = db.products
Orders = db.orders

conf = {"bootstrap.servers": "kafka:29092", "group.id": "fastapi-kafka-consumer"}

consumer = Consumer(conf)
consumer.subscribe(["orders"])


# Helper function to create order
def create_order(order: dict) -> None:
    product = Products.find_one({"_id": ObjectId(order["product_id"])})
    order["timestamp"] = dt.timestamp(dt.now())
    order["user_address"] = dict(order["user_address"])
    order["amount"] = product["price"] * order["quantity"]
    Products.update_one({"_id": ObjectId(order["product_id"])}, {"$inc": {"quantity": -order["quantity"]}})
    order["_id"] = ObjectId(order["_id"])
    Orders.insert_one(order)
    print({"status": "order-created", "order": order})


try:
    while True:
        msg = consumer.poll(1)
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue
        order = json.loads(msg.value().decode("utf-8"))
        create_order(order)
except Exception as e:
    print({"status": "consumer-error", "message": str(e)})
finally:
    consumer.close()
