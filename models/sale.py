from sqlalchemy import(
     Column, 
     Integer, 
     Numeric, 
     DateTime, 
     ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    sale_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    sub_total = Column(Numeric(10, 2), nullable=False)
    tax_amount = Column(Numeric(10, 2), nullable=False)
    discount = Column(Numeric(10, 2), nullable=False)
    grand_total = Column(Numeric(10, 2), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)

   
    user = relationship("User", back_populates="sales")
    customer = relationship("Customer", back_populates="sales")
    
    
    items = relationship("SaleItem", back_populates="sale")
    payments = relationship("Payment", back_populates="sale")
    receipt = relationship("Receipt", back_populates="sale", uselist=False)
