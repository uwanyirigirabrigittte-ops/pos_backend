from sqlalchemy import(
     Column, 
     Integer, 
     String,
)
from sqlalchemy.orm import relationship

from ..database import Base

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, nullable=False)
    contact_name = Column(String, nullable=True)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=True)


    products = relationship("Product", back_populates="supplier")
