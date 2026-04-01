from pydantic import BaseModel
from datetime import date

class TransactionCreate(BaseModel):
    amount: float
    type: str
    category: str
    date: date
    notes: str


class TransactionResponse(BaseModel):
    id: int
    amount: float
    type: str
    category: str
    date: date
    notes: str

    class Config:
        orm_mode = True