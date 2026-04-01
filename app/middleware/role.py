from fastapi import HTTPException, Depends
from app.auth import get_current_user


def role_required(required_role: str):

    def role_checker(current_user=Depends(get_current_user)):

        if current_user.role != required_role:
            raise HTTPException(
                status_code=403,
                detail="Not enough permissions"
            )

        return current_user

    return role_checker