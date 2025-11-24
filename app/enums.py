# ALl enums goes here
from enum import Enum

class Gender(Enum):
    male = 'M'
    female = 'F'

class Category(Enum):
    buyer = 'buyer'
    farmer = 'farmer'

class ProductCategory(Enum):
    grain = "grain"
    vegetables = "vegatables"
    livestock = "livestock"
    diary = "diary"
    other = "other"

class ProuductUint(Enum):
    kg = "kg"
    liter = "liter"
    bag = "bag"
    pices = "pieces"

class ProductStatus(Enum):
    available= "available"
    sold_out = "sold-out"
    discontinued = "discontiued"