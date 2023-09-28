def product_serializer(product) -> dict:
    return {"id": str(product["_id"]),
            "name": product["name"],
            "price": product["price"],
            "quantity": product["quantity"],
            }


def product_list_serializer(products) -> list:
    return [product_serializer(product) for product in products]
