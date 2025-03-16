from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from src.utils.dbengine import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_verified = Column(Boolean, default=False)
    role = Column(String, default="customer")  
    customer = relationship("Customer", back_populates="user", uselist=False) 
    admin = relationship("Admin", back_populates="user", uselist=False)
    manager = relationship("Manager", back_populates="user", uselist=False)