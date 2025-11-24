from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..middlewares.auth import AuthMiddleware
from ..schemas.product import ProductCreate
from ..models.product import Product
from ..enums import Category
from datetime import datetime
from ..models.user import User
import logging
import pymysql
logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/products",
    tags=["products"]
)

#todo, response model
@router.post("/", status_code=status.HTTP_201_CREATED)
def create(product_data: ProductCreate,
            current_user: User = Depends( AuthMiddleware), 
           db: Session = Depends(get_db)):
    if current_user.category != Category.farmer.value:
        raiseError("Only farmers can create products", status.HTTP_403_FORBIDDEN)

    new_product = Product(
        **product_data.model_dump(exclude={"category", "unit", "status", "price_per_unit"}),
        farmer_id  =  current_user.id,
        category=product_data.category.value,
        unit=product_data.unit.value,
        status=product_data.status.value
    )
    try:
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
    except pymysql.DatabaseError as e:
        raiseError(e, status.HTTP_500_INTERNAL_SERVER_ERROR)
    print(new_product)
    # print(product_data.__dict__)
    # print(current_user.__dict__)

def raiseError(e, status_code):
    logger.error(f"failed to create record error: {e}")
    raise HTTPException(
        status_code=status_code,
        detail = {
            "status": "error",
            "message": f"failed to create user: {e}",
            "timestamp": f"{datetime.utcnow()}"
        }
    )