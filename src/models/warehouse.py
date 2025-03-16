from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from src.utils.dbengine import Base

class Warehouse(Base):
    __tablename__ = 'warehouses'

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    max_volume = Column(Float, nullable=True)
    max_weight = Column(Float, nullable=True)
    current_volume = Column(Float, default=0)
    current_weight = Column(Float, default=0)
    items = relationship('Item', back_populates='warehouse')
    products = relationship("Product", back_populates="warehouse")
    warehouse_administrators = relationship('WarehouseAdministrator', back_populates='warehouse')

class WarehouseAdministrator(Base):
    __tablename__ = 'warehouse_administrators'

    id = Column(Integer, primary_key=True, index=True)
    warehouse_id = Column(Integer, ForeignKey('warehouses.id'), nullable=False)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    dob = Column(Date, nullable=False)
    hourly_rate = Column(Float, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(Date, nullable=True)
    job_title = Column(String, nullable=False)
    warehouse = relationship('Warehouse', back_populates='warehouse_administrators')
    


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)  # Foreign key to Product
    quantity = Column(Integer, nullable=False)
    warehouse_id = Column(Integer, ForeignKey('warehouses.id'))
    warehouse = relationship('Warehouse', back_populates='items')
    product = relationship('Product')  # Relationship to Product