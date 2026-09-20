from sqlalchemy import(
     Column,
     Integer, 
     String,
)
from sqlalchemy.orm import relationship

from ..database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    loyalty_points = Column(Integer, nullable=False)

    
    sales = relationship("Sale", back_populates="customer")
