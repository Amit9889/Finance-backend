from sqlalchemy import Column, Integer, String, Float, Date
from app.database import Base

class Transaction(Base):

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    type = Column(String)
    category = Column(String)
    date = Column(Date)
    notes = Column(String)