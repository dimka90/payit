from fastapi import APIRouter, status, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from ..database import get_db
from ..middlewares.auth import AuthMiddleware
from ..schemas.product import ProductCreate
from ..models.product import Product
from ..enums import Category,ProductCategory, ProductStatus, ProuductUint
from datetime import datetime
from uuid import uuid4
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
UPLOAD_DIR = "app/static/uploads"
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


@router.post("/upload", status_code=status.HTTP_200_OK)
async def upload_product(name: str= Form(...),
                   description: Optional[str] = Form(...),
                   status_val: str = Form(...),
                   category: str = Form(...),
                   price_per_uint : float = Form(...),
                   unit: str = Form(...),
                   location: str = Form(...),
                   image: UploadFile = File(None),
                   curent_user: User = Depends(AuthMiddleware),
                   db: Session = Depends(get_db)
                   ):
    print("File", image.filename.split(".")[-1].lower())

    try:
        category_enum = ProductCategory(category)
        status_enum= ProductStatus(status_val)
        unit_enum = ProuductUint(unit)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid value for category, status or unit {str(e)}"
        )
    
    # image processing
    if image is not None and image.filename:
        # todo validate file format
        file_ext = image.filename.split(".")[-1].lower()
        filname_unique = f"{uuid4()}.{file_ext}"

        file_path = os.path.join(UPLOAD_DIR, filname_unique)
        try:
            async with aiofiles.open(file_path, "wb") as outputfile:
                content = await image.read()
                await outputfile.write(content)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="AN error occured while saving the file"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="File is  not an image"
        )
     
    try: 
        image_url = f"/static/uploads/products/{filname_unique}"   
        new_product = Product(
            name = name,
            farmer_id = curent_user.id,
            description = description,
            category = category_enum.value,
            status = status_enum.value,
            unit = unit_enum.value,
            location = location,
            image_url = image_url
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        return {
            "Success": True,
            "detail": new_product,
            "message": "Product sucessfully saved" 
        }
    except ValueError as e:
        pass



