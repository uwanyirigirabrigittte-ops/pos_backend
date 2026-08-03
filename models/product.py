from sqlalchemy import(
     Column,
     Integer,
     String, 
     Numeric, 
     ForeignKey,
)
from sqlalchemy.orm import relationship

from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    barcode = Column(String, nullable=False)
    name = Column(String, nullable=False)
    cost_price = Column(Numeric(10, 2), nullable=False)
    retail_price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)

    
    category = relationship("Category", back_populates="products")
    supplier = relationship("Supplier", back_populates="products")
    sale_items = relationship("SaleItem", back_populates="product")
