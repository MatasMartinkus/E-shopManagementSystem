from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.utils.dbengine import Base

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))  
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=True)
    user = relationship("User", back_populates="customer") 
    reference_code = Column(String, unique=True, index=True)
    orders = relationship('Order', back_populates='customer')

    @property
    def email(self):
        return self.user.email