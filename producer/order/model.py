from pydantic import BaseModel, conint


class Address(BaseModel):
    city: str
    country: str
    zip_code: conint(ge=100000, le=999999)  # 6 digits (Indian zip code)


class Order(BaseModel):
    id: str
    timestamp: float
    amount: float
    product_id: str
    user_address: Address
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "60f1b2b9c9e9f9b3f0f3e4a1",
                    "timestamp": 1626451200.0,
                    "product_id": "60f1b2b9c9e9f9b3f0f3e4a1",
                    "amount": 200.0,
                    "user_address": {"city": "Mumbai", "country": "India", "zip_code": 400001},
                }
            ]
        }
    }
