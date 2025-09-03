from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from models.product import ProductCreate, ProductUpdate, ProductResponse
from services.product_service import ProductService
from exceptions.custom_exceptions import ProductNotFoundError, InvalidProductIdError, UserNotFoundError
from utils.auth import verify_token
import logging

logger = logging.getLogger("product_routes")

router = APIRouter()
product_service = ProductService()

@router.post("/products/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, current_user: str = Depends(verify_token)):
    try:
        logger.info(f"Creating product for user: {current_user}")
        created_product = product_service.create_product(product, current_user)
        logger.info("Product created successfully")
        return ProductResponse(**created_product.dict())
    except UserNotFoundError as e:
        logger.warning(str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")

@router.get("/products/", response_model=List[ProductResponse])
async def get_all_products():
    try:
        logger.info("Fetching all products")
        products = product_service.get_all_products()
        logger.info(f"Total products found: {len(products)}")
        return products
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")

@router.get("/products/user", response_model=List[ProductResponse])
async def get_user_products(current_user: str = Depends(verify_token)):
    try:
        logger.info(f"Fetching products for user: {current_user}")
        products = product_service.get_products_by_user(current_user)
        logger.info(f"Products found for user: {len(products)}")
        return products
    except UserNotFoundError as e:
        logger.warning(str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")

@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str):
    try:
        logger.info(f"Fetching product: {product_id}")
        product = product_service.get_product_by_id(product_id)
        logger.info(f"Product found: {product_id}")
        return product
    except InvalidProductIdError as e:
        logger.warning(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ProductNotFoundError as e:
        logger.warning(str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")

@router.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(product_id: str, product_update: ProductUpdate, current_user: str = Depends(verify_token)):
    try:
        logger.info(f"Updating product: {product_id}")
        updated_product = product_service.update_product(product_id, product_update, current_user)
        logger.info("Product updated successfully")
        return updated_product
    except InvalidProductIdError as e:
        logger.warning(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ProductNotFoundError as e:
        logger.warning(str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")

@router.delete("/products/{product_id}", status_code=status.HTTP_200_OK)
async def delete_product(product_id: str, current_user: str = Depends(verify_token)):
    try:
        logger.info(f"Deleting product: {product_id}")
        result = product_service.delete_product(product_id, current_user)
        logger.info(f"Product deleted successfully: {product_id}")
        return result
    except InvalidProductIdError as e:
        logger.warning(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ProductNotFoundError as e:
        logger.warning(str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")