from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..repositories.product_repo import product_repository
from ..schemas.product import ProductCreate, ProductUpdate

def get_product(db: Session, product_id: int):
    product = product_repository.get(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Boutique apparel item not found in stock catalog"
        )
    return product

def list_products(db: Session):
    return product_repository.get_all(db)

def create_product(db: Session, data: ProductCreate):
    return product_repository.create(db, data.model_dump())

def update_product(db: Session, product_id: int, data: ProductUpdate):
    product = get_product(db, product_id)
    return product_repository.update(db, product, data.model_dump(exclude_unset=True))

def delete_product(db: Session, product_id: int):
    product = get_product(db, product_id)
    product_repository.delete(db, product)
