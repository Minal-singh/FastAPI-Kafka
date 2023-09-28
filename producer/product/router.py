from fastapi import APIRouter, HTTPException, status
from product.serializer import product_serializer, product_list_serializer
from product.model import Product, CreateProduct, OrderDetails
from database import Products
from bson.objectid import ObjectId
import json
from confluent_kafka import Producer


producer_conf = {"bootstrap.servers": "kafka:29092", "client.id": "fastapi-kafka-api"}

producer = Producer(producer_conf)

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_products(page: int = 1, limit: int = 10) -> list[Product]:
    skip = (page - 1) * limit
    products = product_list_serializer(Products.find().skip(skip).limit(limit))
    return products


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_product_by_id(id: str) -> Product:
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid id: {id}")
    product = Products.find_one({"_id": ObjectId(id)})
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id: '{id}' not found")
    product = product_serializer(product)
    return product


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(product: CreateProduct) -> Product:
    inserted_product = Products.insert_one(dict(product))
    inserted_product = Products.find_one({"_id": inserted_product.inserted_id})
    inserted_product = product_serializer(inserted_product)
    return inserted_product


@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_product(id: str, product: CreateProduct) -> Product:
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid id: {id}")
    updated_product = Products.update_one({"_id": ObjectId(id)}, {"$set": dict(product)})
    if updated_product.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id: '{id}' not found")
    updated_product = product_serializer(Products.find_one({"_id": ObjectId(id)}))
    return updated_product


@router.post("/buy/{id}", status_code=status.HTTP_200_OK)
def buy_product(id: str, orderDeatails: OrderDetails) -> dict:
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid id: {id}")
    product = Products.find_one({"_id": ObjectId(id)})
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id: '{id}' not found")
    if product["quantity"] < orderDeatails.quantity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="We don't have enough product(s) in stock")
    new_order_id = str(ObjectId())
    order_dict = dict(orderDeatails)
    order_dict["product_id"] = id
    order_dict["_id"] = new_order_id
    order_dict["user_address"] = dict(order_dict["user_address"])
    produce(order_dict)
    return {"message": "Order placed with id: " + new_order_id}


# Helper function
def produce(data: dict):
    try:
        data = json.dumps(data).encode("utf-8")
        print("Encoded data: ", data)
        producer.produce("orders", value=data)
        print({"status": "success", "msg": data})
    except Exception as e:
        print({"status": "error", "message": str(e)})
