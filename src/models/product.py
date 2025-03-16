from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.utils.dbengine import Base

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    warehouse_id = Column(Integer, ForeignKey('warehouses.id'))
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, nullable=False)
    category = Column(String, nullable=True)  # Category field
    subcategory = Column(String, nullable=True)  # Subcategory field
    length = Column(Float, nullable=True)  # Length field
    width = Column(Float, nullable=True)  # Width field
    height = Column(Float, nullable=True)  # Height field
    weight = Column(Float, nullable=True)  # Weight field
    order_products = relationship('OrderProduct', back_populates='product')
    items = relationship('Item', back_populates='product')  
    warehouse = relationship("Warehouse", back_populates="products")  # Add relationship to Warehouse