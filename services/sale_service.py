from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from repositories.sale_repo import sale_repository
from repositories.product_repo import product_repository
from repositories.customer_repo import customer_repository
from schemas.sale import SaleCreate, SaleUpdate

def get_sale(db: Session, sale_id: int):
    sale = sale_repository.get(db, sale_id)
    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Sales transaction header ledger not found"
        )
    return sale

def list_sales(db: Session):
    return sale_repository.get_all(db)

def create_sale(db: Session, data: SaleCreate):
    # 1. Deduct Stock Inventory for all checked-out cart items
    for item in data.items:
        db_product = product_repository.get(db, item.product_id)
        if not db_product or db_product.quantity < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient inventory or product missing for ID: {item.product_id}"
            )
        # Drop inventory count natively
        product_repository.update(db, db_product, {"quantity": db_product.quantity - item.quantity})
    
    # 2. Add Reward Loyalty Points if a valid customer account is linked
    if data.customer_id:
        db_customer = customer_repository.get(db, data.customer_id)
        if db_customer:
            # Award 1 point for every 10 units spent on grand total
            earned_points = int(data.grand_total // 10)
            customer_repository.update(
                db, 
                db_customer, 
                {"loyalty_points": db_customer.loyalty_points + earned_points}
            )
            
    return sale_repository.create(db, data.model_dump(exclude={"items"}))

def update_sale(db: Session, sale_id: int, data: SaleUpdate):
    sale = get_sale(db, sale_id)
    return sale_repository.update(db, sale, data.model_dump(exclude_unset=True))

def delete_sale(db: Session, sale_id: int):
    sale = get_sale(db, sale_id)
    sale_repository.delete(db, sale)
