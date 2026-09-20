from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime

from ..repositories.receipt_repo import receipt_repository
from ..schemas.receipt import ReceiptCreate, ReceiptUpdate

def get_receipt(db: Session, receipt_id: int):
    receipt = receipt_repository.get(db, receipt_id)
    if not receipt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Official printable store voucher receipt not found"
        )
    return receipt

def list_receipts(db: Session):
    return receipt_repository.get_all(db)

def create_receipt(db: Session, data: ReceiptCreate):
    payload = data.model_dump()
    # Add transaction print timestamp if missing
    if not payload.get("issue_date"):
        payload["issue_date"] = datetime.utcnow()
    return receipt_repository.create(db, payload)

def update_receipt(db: Session, receipt_id: int, data: ReceiptUpdate):
    receipt = get_receipt(db, receipt_id)
    return receipt_repository.update(db, receipt, data.model_dump(exclude_unset=True))

def delete_receipt(db: Session, receipt_id: int):
    receipt = get_receipt(db, receipt_id)
    receipt_repository.delete(db, receipt)
