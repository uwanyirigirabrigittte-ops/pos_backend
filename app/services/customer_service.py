from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..repositories.customer_repo import customer_repository
from ..schemas.customer import CustomerCreate, CustomerUpdate

def get_customer(db: Session, customer_id: int):
    customer = customer_repository.get(db, customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Registered customer profile not found"
        )
    return customer

def list_customers(db: Session):
    return customer_repository.get_all(db)

def create_customer(db: Session, data: CustomerCreate):
    payload = data.model_dump()
    if "loyalty_points" not in payload or payload["loyalty_points"] is None:
        payload["loyalty_points"] = 0
    return customer_repository.create(db, payload)

def update_customer(db: Session, customer_id: int, data: CustomerUpdate):
    customer = get_customer(db, customer_id)
    return customer_repository.update(db, customer, data.model_dump(exclude_unset=True))

def delete_customer(db: Session, customer_id: int):
    customer = get_customer(db, customer_id)
    customer_repository.delete(db, customer)
