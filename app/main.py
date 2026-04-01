from fastapi import FastAPI

from app.database import engine, Base

# Import Models
from app.models import user
from app.models import transaction

# Import Routes
from app.routes import user as user_routes
from app.routes import transaction as transaction_routes
from app.routes import dashboard as dashboard_routes


# Create Database Tables
Base.metadata.create_all(bind=engine)

# Create FastAPI App
app = FastAPI(
    title="Finance Data Processing API",
    description="Backend for Finance Dashboard with Role Based Access Control",
    version="1.0.0"
)


# Include Routers
app.include_router(user_routes.router)
app.include_router(transaction_routes.router)
app.include_router(dashboard_routes.router)


# Root Endpoint
@app.get("/")
def root():
    return {
        "message": "Finance Backend Running Successfully",
        "docs": "http://127.0.0.1:8000/docs"
    }