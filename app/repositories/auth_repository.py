from typing import Optional
from database.connection import get_database
from models.auth_models import UserRegister

class AuthRepository:
    def __init__(self):
        self.db = get_database()
        self.collection = self.db.users

    def get_user_by_email(self, email: str) -> Optional[dict]:
        return self.collection.find_one({"email": email})

    def create_user(self, user_data: dict) -> str:
        result = self.collection.insert_one(user_data)
        return str(result.inserted_id)