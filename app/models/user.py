""" 
User
- id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
- name VARCHAR(30) NOT NULL,
- phone VARCHAR(11) UNIQUE NOT NULL,
- email VARCHAR(100) UNIQUE NOT NULL,
- password VARCHAR(150) NOT NULL,
- gender ENUM('M', 'F') NOT NULL,
- category ENUM('buyer', 'farmer') NOT NULL,
- location VARCHAR(255) NOT NULL,
- created_at TIMESTAMP DEFAULT CURRENT TIMESTAMP NOT NULL,
- updated_at TIMESTAMP DEFAULT CURRENT TIMESTAMP ON UPDATE CURRENT TIMESTAMP
"""

from sqlalchemy import Integer, Column, String, DateTime, Enum, func
from .base import Base
from ..enums import Gender, Category
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(String(30), min_length=3, max_length=30, nullable=False)
    phone = Column(String(20), unique=True, min_length=11, nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(100), nullable=False) #assignment, set boundaries
    gender = Column(Enum(Gender.male.value, Gender.female.value), nullable=False) # create Enum
    category = Column(Enum(Category.buyer.value, Category.farmer.value), nullable=False) # create ENum
    location = Column(String(255), min_length=3, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
