from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from repositories.sale_item_repo import sale_item_repository
from schemas.sale_item import SaleItemCreate, SaleItemUpdate

def get_sale_item(db: Session, sale_item_id: int):
    item = sale_item_repository.get(db, sale_item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Cart line item entry not found"
        )
    return item

def list_sale_items(db: Session):
    return sale_item_repository.get_all(db)

def create_sale_item(db: Session, data: SaleItemCreate):
    # Automatically compute line-total based on user architecture layout rules: quantity * unit-price
    payload = data.model_dump()
    payload["line_total"] = payload["quantity"] * payload["unit_price"]
    return sale_item_repository.create(db, payload)

def update_sale_item(db: Session, sale_item_id: int, data: SaleItemUpdate):
    item = get_sale_item(db, sale_item_id)
    payload = data.model_dump(exclude_unset=True)
    
    # Recalculate line total if values change
    if "quantity" in payload or "unit_price" in payload:
        qty = payload.get("quantity", item.quantity)
        price = payload.get("unit_price", item.unit_price)
        payload["line_total"] = qty * price
        
    return sale_item_repository.update(db, item, payload)

def delete_sale_item(db: Session, sale_item_id: int):
    item = get_sale_item(db, sale_item_id)
    sale_item_repository.delete(db, item)
