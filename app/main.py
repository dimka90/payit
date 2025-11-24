from fastapi import FastAPI
from .database import engine
from .models.user import User
from .models.product import Product
from .models.base import Base
from .routes.user import router as user_routes
from .routes.auth import router as auth_routes
from .routes.product import router as product_routes
import logging

logger = logging.getLogger(__name__)

# craete db tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title = "PayIt App",
    version = "0.0.1",
    description = "market place..."
    )

app.include_router(user_routes)
app.include_router(auth_routes)
app.include_router(product_routes)

@app.get("/")
def home():
    return {
        "status": "success",
        "message": "Hello world"
    }

