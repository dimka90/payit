from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..middlewares.auth import AuthMiddleware
from ..schemas.product import ProductCreate
from ..enums import Category
from datetime import datetime
from ..models.user import User
import logging

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/products",
    tags=["products"]
)

#todo, response model
@router.post("/", status_code=status.HTTP_201_CREATED)
def create(product: ProductCreate,
            current_user: User = Depends( AuthMiddleware), 
           db: Session = Depends(get_db)):
    if current_user.category != Category.farmer.value:
        raiseError("Only farmers can create products", status.HTTP_403_FORBIDDEN)

    print(current_user)

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