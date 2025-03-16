from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.utils.dbengine import Base

class Admin(Base):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    department = Column(String, nullable=False)
    permissions = Column(String, nullable=False)
    user = relationship("User", back_populates="admin")
