from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.utils.dbengine import Base

class Manager(Base):
    __tablename__ = 'managers'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    location = Column(String, nullable=False)
    permissions = Column(String, nullable=False)
    user = relationship("User", back_populates="manager")