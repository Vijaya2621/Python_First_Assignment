from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from models.user import UserModel, UserCreate, UserUpdate, UserResponse
from services.user_service import UserService
from exceptions.custom_exceptions import UserNotFoundError, EmailAlreadyExistsError, InvalidUserIdError
from utils.auth import verify_token
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger("user_routes")


router = APIRouter()
user_service = UserService()

@router.post("/users/", response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """ API to create a new user """
    try:
        logger.info(f"Trying to create user with email: {user.email}")
        created_user = user_service.create_user(user)
        logger.info("User created successfully")
        return created_user

    except EmailAlreadyExistsError as e:
        logger.warning(str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong."
        )


@router.get("/users/", response_model=List[UserResponse])
async def get_all_users(current_user: str = Depends(verify_token)):
    """Get all users"""
    try:
        logger.info("Fetching all users from database")
        users = user_service.get_all_users()
        logger.info(f"Total users found: {len(users)}")
        return users

    except Exception as e:
        logger.error(f"Unexpected error while fetching users: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while fetching users."
        )


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, current_user: str = Depends(verify_token)):
    """Get a specific user by ID"""
    try:
        logger.info(f"Fetching user with ID: {user_id}")
        user = user_service.get_user_by_id(user_id)
        logger.info(f"User found: {user_id}")
        return user

    except InvalidUserIdError as e:
        logger.warning(str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except UserNotFoundError as e:
        logger.warning(str(e))
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error while fetching user: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while fetching user."
        )


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user_update: UserUpdate, current_user: str = Depends(verify_token)):
    """Update a user"""
    try:
        logger.info(f"Trying to update user: {user_id}")
        updated_user = user_service.update_user(user_id, user_update)
        logger.info("User updated successfully")
        return updated_user

    except InvalidUserIdError as e:
        logger.warning(str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except UserNotFoundError as e:
        logger.warning(str(e))
        raise HTTPException(status_code=404, detail=str(e))
    except EmailAlreadyExistsError as e:
        logger.warning(str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: str, current_user: str = Depends(verify_token)):
    """Delete a user"""
    try:
        logger.info(f"Trying to delete a user: {user_id}")
        result = user_service.delete_user(user_id)
        logger.info(f"User deleted successfully: {user_id}")
        return result
    
    except InvalidUserIdError as e:
        logger.warning(str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except UserNotFoundError as e:
        logger.warning(str(e))
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error while deleting user: {str(e)}")
        raise HTTPException(status_code=500, detail="Something went wrong")