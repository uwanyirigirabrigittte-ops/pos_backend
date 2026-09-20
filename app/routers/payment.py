from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.payment import PaymentCreate, PaymentRead, PaymentUpdate
from ..services import payment_service

router = APIRouter(prefix="/payments", tags=["payments"])

@router.get("/", response_model=list[PaymentRead])
def list_payments(db: Session = Depends(get_db)):
    return payment_service.list_payments(db)

@router.get("/{payment_id}", response_model=PaymentRead)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    return payment_service.get_payment(db, payment_id)

@router.post("/", response_model=PaymentRead, status_code=status.HTTP_201_CREATED)
def create_payment(data: PaymentCreate, db: Session = Depends(get_db)):
    return payment_service.create_payment(db, data)

@router.put("/{payment_id}", response_model=PaymentRead)
def update_payment(payment_id: int, data: PaymentUpdate, db: Session = Depends(get_db)):
    return payment_service.update_payment(db, payment_id, data)

@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    payment_service.delete_payment(db, payment_id)
    return None
