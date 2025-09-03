import os
from pymongo import MongoClient
from typing import Optional

class Database:
    client: Optional[MongoClient] = None
    database = None
    
    def connect(self):
        if self.database is None:
            mongo_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017/")
            db_name = os.getenv("DATABASE_NAME", "crud_app")
            self.client = MongoClient(mongo_url)
            self.database = self.client[db_name]
        return self.database

db = Database()

def get_database():
    return db.connect()

def connect_to_mongo():
    """Create database connection"""
    db.connect()

def close_mongo_connection():
    """Close database connection"""
    if db.client:
        db.client.close()
        db.client = None
        db.database = None