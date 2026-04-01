from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate
from app.auth import get_current_user

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)


@router.post("/")
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    new_tx = Transaction(**transaction.dict())

    db.add(new_tx)
    db.commit()
    db.refresh(new_tx)

    return new_tx


@router.get("/")
def get_transactions(
    category: str = None,
    type: str = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    query = db.query(Transaction)

    if category:
        query = query.filter(
            Transaction.category == category
        )

    if type:
        query = query.filter(
            Transaction.type == type
        )

    return query.all()


@router.put("/{id}")
def update_transaction(
    id: int,
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    tx = db.query(Transaction).filter(
        Transaction.id == id
    ).first()

    if not tx:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    for key, value in transaction.dict().items():
        setattr(tx, key, value)

    db.commit()

    return tx


@router.delete("/{id}")
def delete_transaction(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    tx = db.query(Transaction).filter(
        Transaction.id == id
    ).first()

    if not tx:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    db.delete(tx)
    db.commit()

    return {"message": "Deleted"}