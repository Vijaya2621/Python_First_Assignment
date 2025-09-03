from fastapi import APIRouter, HTTPException, status
from models.auth_models import UserLogin, UserRegister, ResponseToken
from services.auth_service import AuthService
from exceptions.custom_exceptions import EmailAlreadyExistsError
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger("auth_routes")

router = APIRouter()
auth_service = AuthService()


# hash password and create user

@router.post("/register", response_model=ResponseToken)
async def register(user: UserRegister):
    """Register a new user"""
    try:
        logger.info(f"Register API called with email: {user.email}")
        token_response = auth_service.register_user(user)
        logger.info(f"User registered successfully: {user.email}")
        return token_response

    except EmailAlreadyExistsError as e:
        logger.warning(f"Registration failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.exception(f"Unexpected error during registration for {user.email}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error"
        )
        
@router.post("/login", response_model=ResponseToken)
async def login(user: UserLogin):
    """Login User"""
    try:
        logger.info(f"Login attempt for email: {user.email}")
        token_response = auth_service.login_user(user)
        logger.info(f"Login successful for email: {user.email}")
        return token_response
    
    except Exception as e:
        if "Invalid email or password" in str(e):
            logger.warning(f"Login failed for: {user.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        logger.exception(f"Unexpected error during login for {user.email}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error"
        )