from pydantic import BaseModel, Field, EmailStr, validator, model_validator
from typing import List, Optional, Dict
from ..enums import Gender, Category
import re

class User(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    gender: str
    category: str
    location: str

class UserCreateRequest(BaseModel):
    name: str = Field(min_length=3, max_length=30)
    phone: str = Field(min_length=11, pattern=r"\d")
    email: EmailStr
    password: str = Field(min_length=6)
    confirm_password: str
    gender: Gender
    category: Category
    location: str = Field(min_length=3)

    @validator('phone')
    def phone_is_valid_numeric_value(cls, value):
        if value.isdigit() is not True:
            raise ValueError('phone number must be digits')
        return value
    
    @validator('password')
    def validate_password(cls, value):
        if not re.search(r"[A-Z]", value):
            raise ValueError('password must contain atleast one capital letter')
        if not re.search(r"[a-z]", value):
            raise ValueError('password must contain atleast one lowercase letter')
        if not re.search(r"\d", value):
            raise ValueError('password must contain atleast one numeric value')
        if not re.search(r"[^A-Za-z0-9]", value):
            raise ValueError('password must contain atleast one special character')
        return value
    
    @model_validator(mode='after')
    def validate_confirm_password(self):
        if self.password != self.confirm_password:
            raise ValueError('passwords must match')
        return self

