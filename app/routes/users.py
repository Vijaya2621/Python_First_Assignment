from fastapi import APIRouter, HTTPException, status
from typing import List
from bson import ObjectId
from models.user import UserModel, UserCreate, UserUpdate
from database.connection import get_database
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("assignment1")


router = APIRouter()

@router.post("/users/", response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """ API to create a new user """
    db = get_database()

    try:
        logger.info(f"Trying to create user with email: {user.email}")

        # Step 1: check if email already exists
        existing_user = db.users.find_one({"email": user.email})
        if existing_user:
            logger.warning("Email already registered")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        user_dict = user.dict()
        result = db.users.insert_one(user_dict)

        created_user = db.users.find_one({"_id": result.inserted_id})
        created_user["_id"] = str(created_user["_id"])

        logger.info("User created successfully")
        return UserModel(**created_user)

    except HTTPException as e:
        logger.error(f"HTTP error: {e.detail}")
        raise e 

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong."
        )


@router.get("/users/", response_model=List[UserModel])
async def get_all_users():
    """Get all users"""
    db = get_database()

    try:
        logger.info("Fetching all users from database")
        users = list(db.users.find())
        
        user_details = []
        for user in users:
            user["_id"] = str(user["_id"])
            user_details.append(UserModel(**user))  

        logger.info(f"Total users found: {len(users)}")
        return user_details 

    except HTTPException as e:
        logger.error(f"HTTP error: {e.detail}")
        raise e

    except Exception as e:
        logger.error(f"Unexpected error while fetching users: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while fetching users."
        )


@router.get("/users/{user_id}", response_model=UserModel)
async def get_user(user_id: str):
    """Get a specific user by ID"""
    db = get_database()

    try:
        logger.info(f"Fetching user with ID: {user_id}")

        if not ObjectId.is_valid(user_id):
            logger.warning("Invalid user ID format")
            raise HTTPException(
                status_code=400,
                detail="Invalid user ID format"
            )

        user = db.users.find_one({"_id": ObjectId(user_id)})

        if not user:
            logger.warning(f"User not found for ID: {user_id}")
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        user["_id"] = str(user["_id"])
        logger.info(f"User found: {user_id}")

        return UserModel(**user)

    except HTTPException as e:
        logger.error(f"HTTP error: {e.detail}")
        raise e

    except Exception as e:
        logger.error(f"Unexpected error while fetching user: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while fetching user."
        )


@router.put("/users/{user_id}", response_model=UserModel)
async def update_user(user_id: str, user_update: UserUpdate):
    """Update a user"""
    db = get_database()

    try:
        logger.info(f"Trying to update user: {user_id}")

        if not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=400, detail="Invalid user ID format")

        existing_user = db.users.find_one({"_id": ObjectId(user_id)})
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        update_data = {}
        for key, value in user_update.dict().items():
            if value is not None:
                update_data[key] = value

        if "email" in update_data:
            email_exists = db.users.find_one({
                "email": update_data["email"],
                "_id": {"$ne": ObjectId(user_id)}
            })
            if email_exists:
                raise HTTPException(status_code=400, detail="Email already registered")

        if update_data:
            db.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
            logger.info("User updated successfully")

        updated_user = db.users.find_one({"_id": ObjectId(user_id)})
        updated_user["_id"] = str(updated_user["_id"])
        return UserModel(**updated_user)

    except HTTPException as e:
        logger.error(f"HTTP error: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.delete("/users/{user_id}",status_code= status.HTTP_200_OK)
async def delete_user(user_id: str):
    """Delete a user"""
    db =get_database()
    try:
        logger.info(f"Trying to delete a user: {user_id}")
        if not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=400, detail ="Invalid user ID fromat")
        result = db.users.delete_one({"_id": ObjectId(user_id)})    
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        
        logger.info(f"User deleted successfully: {user_id}")
        return {"message": "User deleted successfully"}
    
    except HTTPException as e:
        logger.error(f"error while deleteing user: {e.detail}")
        raise e
    except HTTPException as e:
        logger.error(f"Unexpected error while deleting user: {str(e)}")
        raise HTTPException(status_code=500, detail="Something went wrong")