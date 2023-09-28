def address_serializer(address) -> dict:
    return {"city": address["city"], "country": address["country"], "zip_code": address["zip_code"]}


def order_serializer(order) -> dict:
    return {
        "id": str(order["_id"]),
        "amount": order["amount"],
        "timestamp": order["timestamp"],
        "product_id": str(order["product_id"]),
        "user_address": address_serializer(order["user_address"]),
    }


def order_list_serializer(orders) -> list:
    return [order_serializer(order) for order in orders]
