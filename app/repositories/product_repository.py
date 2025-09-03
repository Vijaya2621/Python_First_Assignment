from database.connection import get_database
from models.product import ProductModel, ProductCreate, ProductUpdate
from bson import ObjectId
from typing import List, Optional
import logging

logger = logging.getLogger("product_repository")

class ProductRepository:
    def __init__(self):
        self.db = get_database()
        self.collection = self.db.products

    def create_product(self, product: ProductCreate, user_email: str) -> ProductModel:
        product_dict = product.dict()
        product_dict["user_id"] = user_email
        result = self.collection.insert_one(product_dict)
        product_dict["_id"] = str(result.inserted_id)
        return ProductModel(**product_dict)

    def get_all_products(self) -> List[ProductModel]:
        products = list(self.collection.find())
        for product in products:
            product["_id"] = str(product["_id"])
        return [ProductModel(**product) for product in products]

    def get_products_by_user(self, user_email: str) -> List[ProductModel]:
        products = list(self.collection.find({"user_id": user_email}))
        for product in products:
            product["_id"] = str(product["_id"])
        return [ProductModel(**product) for product in products]

    def get_product_by_id(self, product_id: str) -> Optional[ProductModel]:
        if not ObjectId.is_valid(product_id):
            return None
        product = self.collection.find_one({"_id": ObjectId(product_id)})
        if product:
            product["_id"] = str(product["_id"])
            return ProductModel(**product)
        return None

    def update_product(self, product_id: str, product_update: ProductUpdate) -> Optional[ProductModel]:
        if not ObjectId.is_valid(product_id):
            return None
        
        update_data = {k: v for k, v in product_update.dict().items() if v is not None}
        if not update_data:
            return self.get_product_by_id(product_id)
        
        result = self.collection.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": update_data}
        )
        
        if result.matched_count:
            return self.get_product_by_id(product_id)
        return None

    def delete_product(self, product_id: str) -> bool:
        if not ObjectId.is_valid(product_id):
            return False
        result = self.collection.delete_one({"_id": ObjectId(product_id)})
        return result.deleted_count > 0

    def product_exists_by_id(self, product_id: str) -> bool:
        if not ObjectId.is_valid(product_id):
            return False
        return self.collection.count_documents({"_id": ObjectId(product_id)}) > 0