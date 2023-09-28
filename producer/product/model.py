from pydantic import BaseModel, conint


class Address(BaseModel):
    city: str
    country: str
    zip_code: conint(ge=100000, le=999999)  # 6 digits (Indian zip code)


class CreateProduct(BaseModel):
    name: str
    price: float
    quantity: int

    model_config = {"json_schema_extra": {"examples": [{"name": "Product 1", "price": 100.0, "quantity": 10}]}}


class Product(CreateProduct):
    id: str
    model_config = {
        "json_schema_extra": {
            "examples": [{"id": "60f1b2b9c9e9f9b3f0f3e4a1", "name": "Product 1", "price": 100.0, "quantity": 10}]
        }
    }


class OrderDetails(BaseModel):
    quantity: int
    user_address: Address
    model_config = {
        "json_schema_extra": {
            "examples": [{"quantity": 2,
                          "user_address": {"city": "Mumbai", "country": "India", "zip_code": 400001}}]
        }
    }
