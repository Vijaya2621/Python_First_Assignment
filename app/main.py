from fastapi import FastAPI
from database.connection import connect_to_mongo, close_mongo_connection
from routes.users import router as user_router

app = FastAPI(
    title="CRUD API",
    description="A simple CRUD API using FastAPI and MongoDB",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    """Connect to MongoDB on startup"""
    connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    """Close MongoDB connection on shutdown"""
    close_mongo_connection()

# Include routers
app.include_router(user_router, prefix="/api/v1", tags=["users"])

@app.get("/")
async def root():
    """This endpoint returns a welcome message"""
    return {"message": "Welcome to CRUD API"}