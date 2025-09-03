from repositories.auth_repository import AuthRepository
from models.auth_models import UserLogin, UserRegister, ResponseToken
from utils.auth import hash_password, verify_password, create_access_token
from exceptions.custom_exceptions import EmailAlreadyExistsError
import logging

logger = logging.getLogger("auth_service")

class AuthService:
    def __init__(self):
        self.auth_repository = AuthRepository()

    def register_user(self, user: UserRegister) -> ResponseToken:
        existing_user = self.auth_repository.get_user_by_email(user.email)
        if existing_user:
            raise EmailAlreadyExistsError("Email already registered")

        hashed_password = hash_password(user.password)
        user_data = {
            "name": user.name,
            "email": user.email,
            "age": user.age,
            "password": hashed_password
        }

        user_id = self.auth_repository.create_user(user_data)
        if not user_id:
            raise Exception("User registration failed")

        access_token = create_access_token(data={"sub": user.email})
        return ResponseToken(access_token=access_token, token_type="bearer")

    def login_user(self, user: UserLogin) -> ResponseToken:
        db_user = self.auth_repository.get_user_by_email(user.email)
        if not db_user:
            raise Exception("Invalid email or password")

        if not verify_password(user.password, db_user["password"]):
            raise Exception("Invalid email or password")

        access_token = create_access_token(data={"sub": user.email})
        return ResponseToken(access_token=access_token, token_type="bearer")