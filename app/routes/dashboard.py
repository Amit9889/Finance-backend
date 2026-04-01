from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.transaction import Transaction
from app.auth import get_current_user

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/summary")
def get_summary(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    income = db.query(
        func.sum(Transaction.amount)
    ).filter(
        Transaction.type == "income"
    ).scalar() or 0

    expense = db.query(
        func.sum(Transaction.amount)
    ).filter(
        Transaction.type == "expense"
    ).scalar() or 0

    return {
        "total_income": income,
        "total_expense": expense,
        "net_balance": income - expense
    }