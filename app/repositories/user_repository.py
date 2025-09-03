from typing import List, Optional
from bson import ObjectId
from database.connection import get_database
from models.user import UserCreate, UserUpdate

class UserRepository:
    def __init__(self):
        self.db = get_database()
        self.collection = self.db.users

    def create_user(self, user_data: UserCreate) -> dict:
        user_dict = user_data.dict()
        result = self.collection.insert_one(user_dict)
        return self.collection.find_one({"_id": result.inserted_id})

    def get_user_by_email(self, email: str) -> Optional[dict]:
        return self.collection.find_one({"email": email})

    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        if not ObjectId.is_valid(user_id):
            return None
        return self.collection.find_one({"_id": ObjectId(user_id)})

    def get_all_users(self) -> List[dict]:
        return list(self.collection.find())

    def update_user(self, user_id: str, update_data: dict) -> Optional[dict]:
        if not ObjectId.is_valid(user_id):
            return None
        
        self.collection.update_one(
            {"_id": ObjectId(user_id)}, 
            {"$set": update_data}
        )
        return self.collection.find_one({"_id": ObjectId(user_id)})

    def delete_user(self, user_id: str) -> bool:
        if not ObjectId.is_valid(user_id):
            return False
        
        result = self.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0

    def email_exists_for_other_user(self, email: str, user_id: str) -> bool:
        return self.collection.find_one({
            "email": email,
            "_id": {"$ne": ObjectId(user_id)}
        }) is not None