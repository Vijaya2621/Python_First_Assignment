from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv
from database.connection import connect_to_mongo, close_mongo_connection
from routes.user_route import router as user_router
from routes.auth_routes import router as auth_router
from routes.product_route import router as product_router
import logging

# Load environment variables
load_dotenv()

logger = logging.getLogger("main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up CRUD API application")
    connect_to_mongo()
    logger.info("MongoDB connection established")
    yield
    # Shutdown
    logger.info("Shutting down CRUD API application")
    close_mongo_connection()
    logger.info("MongoDB connection closed")

app = FastAPI(
    title="CRUD API",
    description="A simple CRUD API using FastAPI and MongoDB",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers
app.include_router(auth_router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(user_router, prefix="/api/v1", tags=["users"])
app.include_router(product_router, prefix="/api/v1", tags=["products"])

@app.get("/")
async def root():
    """This endpoint returns a welcome message"""
    return {"message": "Welcome to CRUD API"}