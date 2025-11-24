from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas.user import UserCreateRequest
from ..database import get_db
from ..models.user import User
from ..schemas.user import User as UserResponse
from ..middlewares.auth import AuthMiddleware
from datetime import datetime
import logging
import bcrypt
import pymysql

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_current_user(current_user = Depends(AuthMiddleware)):
    return current_user

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create(user_request: UserCreateRequest, db: Session = Depends(get_db)):

    userExists = db.query(User).filter(
        (user_request.email == User.email) | (user_request.phone == User.phone)
    ).first()

    if userExists:
        raiseError("email or phone already exists")
    
    salts = bcrypt.gensalt(rounds=12)
    hashed_password = bcrypt.hashpw(user_request.password.encode('utf-8'), salts)
    
    new_user = User(
        **user_request.dict(exclude={"password", "confirm_password", "gender", "category"}),
        password=hashed_password.decode(),
        gender = user_request.gender.value,
        category = user_request.category.value
    )

    try:  
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    except pymysql.DataError as e:
        raiseError(e)
    except Exception as e:
        raiseError(e)

def raiseError(e):
    logger.error(f"failed to create record error: {e}")
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail = {
            "status": "error",
            "message": f"failed to create user: {e}",
            "timestamp": f"{datetime.utcnow()}"
        }
    )