from pydantic import BaseModel, Field, validator, model_validator
from typing import List, Optional, Dict
from ..enums import ProductCategory,ProductStatus, ProuductUint

class Product(BaseModel):
    name: str = Field(min_length=3, max_length=30)
    description: Optional[str] = None
    status: ProductStatus
    category: ProductCategory
    price_per_unit: float = Field(gt=0, description="Price must be greater than 0")
    unit: ProuductUint
    location: str = Field(min_length=3, max_length=255)
    image_url: Optional[str] = None

@validator("price_per_unit")
def validate_price(cls, value):
    if value < 0:
        raise ValueError("Value must be greater than 0")
    return round(value, 2)

class ProductCreate(Product):
    pass

