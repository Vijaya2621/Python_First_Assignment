from typing import List
from repositories.user_repository import UserRepository
from models.user import UserCreate, UserUpdate, UserModel, UserResponse
from exceptions.custom_exceptions import UserNotFoundError, EmailAlreadyExistsError, InvalidUserIdError
import logging

logger = logging.getLogger("user_service")

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def create_user(self, user_data: UserCreate) -> UserModel:
        if self.user_repository.get_user_by_email(user_data.email):
            raise EmailAlreadyExistsError("Email already registered")
        
        created_user = self.user_repository.create_user(user_data)
        created_user["_id"] = str(created_user["_id"])
        return UserModel(**created_user)

    def get_all_users(self) -> List[UserResponse]:
        users = self.user_repository.get_all_users()
        user_responses = []
        
        for user in users:
            user["_id"] = str(user["_id"])
            user_responses.append(UserResponse(
                id=user["_id"],
                name=user["name"],
                email=user["email"],
                age=user["age"]
            ))
        
        return user_responses

    def get_user_by_id(self, user_id: str) -> UserResponse:
        user = self.user_repository.get_user_by_id(user_id)
        
        if not user:
            if not user_id or len(user_id) != 24:
                raise InvalidUserIdError("Invalid user ID format")
            raise UserNotFoundError("User not found")
        
        user["_id"] = str(user["_id"])
        return UserResponse(
            id=user["_id"],
            name=user["name"],
            email=user["email"],
            age=user["age"]
        )

    def update_user(self, user_id: str, user_update: UserUpdate) -> UserResponse:
        existing_user = self.user_repository.get_user_by_id(user_id)
        if not existing_user:
            if not user_id or len(user_id) != 24:
                raise InvalidUserIdError("Invalid user ID format")
            raise UserNotFoundError("User not found")

        update_data = {}
        for key, value in user_update.dict().items():
            if value is not None:
                update_data[key] = value

        if "email" in update_data:
            if self.user_repository.email_exists_for_other_user(update_data["email"], user_id):
                raise EmailAlreadyExistsError("Email already registered")

        if update_data:
            updated_user = self.user_repository.update_user(user_id, update_data)
            updated_user["_id"] = str(updated_user["_id"])
            return UserResponse(
                id=updated_user["_id"],
                name=updated_user["name"],
                email=updated_user["email"],
                age=updated_user["age"]
            )
        
        existing_user["_id"] = str(existing_user["_id"])
        return UserResponse(
            id=existing_user["_id"],
            name=existing_user["name"],
            email=existing_user["email"],
            age=existing_user["age"]
        )

    def delete_user(self, user_id: str) -> dict:
        if not self.user_repository.get_user_by_id(user_id):
            if not user_id or len(user_id) != 24:
                raise InvalidUserIdError("Invalid user ID format")
            raise UserNotFoundError("User not found")
        
        success = self.user_repository.delete_user(user_id)
        if not success:
            raise UserNotFoundError("User not found")
        
        return {"message": "User deleted successfully"}