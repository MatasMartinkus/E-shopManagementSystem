from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float, String
from sqlalchemy.orm import relationship
from datetime import datetime
from src.utils.dbengine import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow)
    products = relationship('OrderProduct', back_populates='order')
    customer = relationship('Customer', back_populates='orders')

class OrderProduct(Base):
    __tablename__ = 'order_products'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    order = relationship('Order', back_populates='products')
    product = relationship('Product', back_populates='order_products')