from sqlalchemy import Column, Integer, Float, DateTime, String
from src.utils.dbengine import Base

class Financial(Base):
    __tablename__ = "financials"

    id = Column(Integer, primary_key=True, index=True)
    transaction_date = Column(DateTime)
    amount = Column(Float)
    transaction_type = Column(String)  # e.g., "income", "expense"
    recipient = Column(String)
    sender = Column(String)