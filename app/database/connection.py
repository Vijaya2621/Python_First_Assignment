import os
from pymongo import MongoClient
from typing import Optional

class Database:
    client: Optional[MongoClient] = None
    database = None                       

db = Database() 

def get_database():
    return db.database

def connect_to_mongo():
    """Create database connection"""
    mongo_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017/")
    db_name = os.getenv("DATABASE_NAME", "crud_app")
    
    db.client = MongoClient(mongo_url)
    db.database = db.client[db_name]

def close_mongo_connection():
    """Close database connection"""
    if db.client:
        db.client.close()