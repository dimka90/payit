from fastapi import APIRouter, status, Depends, HTTPException, File, UploadFile, Form
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
import os
import aiofiles
from typing import Optional
logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/products",
    tags=["products"]
)
UPLOAD_DIR = "/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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


# name: str = Field(min_length=3, max_length=30)
#     description: Optional[str] = None
#     status: ProductStatus
#     category: ProductCategory
#     price_per_unit: float = Field(gt=0, description="Price must be greater than 0")
#     unit: ProuductUint
#     location: str = Field(min_length=3, max_length=255)
#     image_url: Optional[str] = None

@router.post("/upload", status_code=status.HTTP_200_OK)
async def upload_product(name: str= Form(...),
                   description: Optional[str] = Form(...),
                   status: str = Form(...),
                   category: str = Form(...),
                   price_per_uint : float = Form(...),
                   uint: str = Form(...),
                   location: str = Form(...),
                   image_url: UploadFile = File(None)
                   ):
    print("File", image_url.filename.split(".")[-1])
    file_path = os.path.join(UPLOAD_DIR,image_url.filename)

    async with aiofiles.open(file_path, "wb") as outputfile:
        content = await image_url.read()
        await outputfile.write(content)


