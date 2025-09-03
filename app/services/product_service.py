from repositories.product_repository import ProductRepository
from repositories.user_repository import UserRepository
from models.product import ProductModel, ProductCreate, ProductUpdate, ProductResponse
from exceptions.custom_exceptions import ProductNotFoundError, InvalidProductIdError, UserNotFoundError, InvalidUserIdError
from typing import List
import logging

logger = logging.getLogger("product_service")

class ProductService:
    def __init__(self):
        self.product_repository = ProductRepository()
        self.user_repository = UserRepository()

    def create_product(self, product: ProductCreate, user_email: str) -> ProductModel:
        if not self.user_repository.user_exists_by_email(user_email):
            raise UserNotFoundError(f"User with email {user_email} not found")
        
        return self.product_repository.create_product(product, user_email)

    def get_all_products(self) -> List[ProductResponse]:
        products = self.product_repository.get_all_products()
        return [ProductResponse(**product.dict()) for product in products]

    def get_products_by_user(self, user_email: str) -> List[ProductResponse]:
        if not self.user_repository.user_exists_by_email(user_email):
            raise UserNotFoundError(f"User with email {user_email} not found")
        
        products = self.product_repository.get_products_by_user(user_email)
        return [ProductResponse(**product.dict()) for product in products]

    def get_product_by_id(self, product_id: str) -> ProductResponse:
        if not product_id or len(product_id.strip()) == 0:
            raise InvalidProductIdError("Product ID cannot be empty")
        
        product = self.product_repository.get_product_by_id(product_id)
        if not product:
            raise ProductNotFoundError(f"Product with ID {product_id} not found")
        
        return ProductResponse(**product.dict())

    def update_product(self, product_id: str, product_update: ProductUpdate, user_email: str) -> ProductResponse:
        if not product_id or len(product_id.strip()) == 0:
            raise InvalidProductIdError("Product ID cannot be empty")
        
        existing_product = self.product_repository.get_product_by_id(product_id)
        if not existing_product:
            raise ProductNotFoundError(f"Product with ID {product_id} not found")
        
        if existing_product.user_id != user_email:
            raise ProductNotFoundError("Product not found or access denied")
        
        updated_product = self.product_repository.update_product(product_id, product_update)
        if not updated_product:
            raise ProductNotFoundError(f"Product with ID {product_id} not found")
        
        return ProductResponse(**updated_product.dict())

    def delete_product(self, product_id: str, user_email: str) -> dict:
        if not product_id or len(product_id.strip()) == 0:
            raise InvalidProductIdError("Product ID cannot be empty")
        
        existing_product = self.product_repository.get_product_by_id(product_id)
        if not existing_product:
            raise ProductNotFoundError(f"Product with ID {product_id} not found")
        
        if existing_product.user_id != user_email:
            raise ProductNotFoundError("Product not found or access denied")
        
        deleted = self.product_repository.delete_product(product_id)
        if not deleted:
            raise ProductNotFoundError(f"Product with ID {product_id} not found")
        
        return {"message": "Product deleted successfully"}