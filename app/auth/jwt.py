from jose import jwt, JWTError
from datetime import timedelta, datetime
from typing import Optional
import os

SECRET_KEY = os.getenv('JWT_SECRET_KEY', '07c58ada9b9ce6bd36d679c77a81b5da9e7cf79593047c8b64bb79f0552f7f58')
ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRATION_MINUTES = os.getenv('JWT_EXPIRATION_TIME', 60)

def create_access_token(claims: dict, expires_delta: Optional[timedelta] = None) -> str:
    try:
        if expires_delta:
            expiration_time = datetime.utcnow() + expires_delta
        else:
            expiration_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINUTES)

        claims.update({'exp': expiration_time})

        return jwt.encode(claims, SECRET_KEY, algorithm=ALGORITHM)
    except JWTError as e:
        raise e


def verify_access_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as e:
        raise