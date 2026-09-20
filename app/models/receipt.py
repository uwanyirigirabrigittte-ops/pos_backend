from sqlalchemy import(
     Column, 
     Integer, 
     String, 
     DateTime, 
     ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base

class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True)
    receipt_no = Column(String, nullable=False)
    sale_id = Column(Integer, ForeignKey("sales.id"), nullable=False)
    issue_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    
    sale = relationship("Sale", back_populates="receipt")
