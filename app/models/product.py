""" 
User
- id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
- name VARCHAR(30) NOT NULL,
- description VARCHAR(11) UNIQUE NOT NULL,
- email VARCHAR(100) UNIQUE NOT NULL,
- password VARCHAR(150) NOT NULL,
- gender ENUM('M', 'F') NOT NULL,
- category ENUM('buyer', 'farmer') NOT NULL,
- location VARCHAR(255) NOT NULL,
- created_at TIMESTAMP DEFAULT CURRENT TIMESTAMP NOT NULL,
- updated_at TIMESTAMP DEFAULT CURRENT TIMESTAMP ON UPDATE CURRENT TIMESTAMP
"""

from sqlalchemy import Integer, Column, String, DateTime, Enum, func, Text, ForeignKey
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship
from .base import Base
from ..enums import ProductCategory, ProductStatus, ProuductUint

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, nullable=False, index = True)
    name = Column(String(30), min_length=3, max_length=30, nullable=False)
    farmer_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable= False, index= True)
    description = Column(Text, nullable=False)
    category = Column(SQLEnum(ProductCategory), nullable= False)
    status = Column(SQLEnum(ProductStatus, default = ProductStatus.available, nullable = False))
    unit = Column(SQLEnum(ProuductUint), nullable= False)
    location = Column(String(255), nullable= False)
    image_url = Column(255, nullable= False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    farmer = relationship("USER" , back_populates="products")