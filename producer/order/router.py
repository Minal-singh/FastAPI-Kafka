from fastapi import APIRouter, HTTPException, status
from database import Orders
from order.serializer import order_serializer, order_list_serializer
from order.model import Order
from bson.objectid import ObjectId

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_orders(page: int = 1, limit: int = 10) -> list[Order]:
    skip = (page - 1) * limit
    orders = order_list_serializer(Orders.find().skip(skip).limit(limit))
    return orders


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_order_by_id(id: str) -> Order:
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid id: {id}")
    order = Orders.find_one({"_id": ObjectId(id)})
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id: '{id}' not found")
    order = order_serializer(order)
    return order
