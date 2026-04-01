from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.auth import create_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(email: str, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid email"
        )

    token = create_token({
        "user_id": user.id,
        "role": user.role
    })

    return {
        "access_token": token
    }