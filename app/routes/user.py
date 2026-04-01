from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database import get_db
from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserLogin
)

from app.auth import create_access_token

router = APIRouter(tags=["Users"])

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


@router.post("/users", response_model=UserResponse)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    hashed_password = pwd_context.hash(
        user.password
    )

    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=400,
            detail="Invalid email"
        )

    if not pwd_context.verify(
        user.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid password"
        )

    token = create_access_token(
        {"user_id": db_user.id}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/users")
def get_users(
    db: Session = Depends(get_db)
):

    return db.query(User).all()