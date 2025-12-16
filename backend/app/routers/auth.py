from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .. import models, schemas
from ..database import get_db
from ..utils.auth_helper import (
    create_access_token,
    get_current_user,
    SESSION_COOKIE_NAME,
)
from ..config import get_access_token_expires

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/login", response_model=schemas.LoginResponse)
def login(
    payload: schemas.LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    # create JWT
    token_expires = get_access_token_expires()
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role},
        expires_delta=token_expires,
    )

    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=int(token_expires.total_seconds()),
        path="/",
    )

    return schemas.LoginResponse.from_orm(user)

@router.post("/logout")
def logout(response: Response):
    # clear cookie
    response.delete_cookie(key=SESSION_COOKIE_NAME, path="/")
    return {"detail": "Logged out"}

@router.get("/me", response_model=schemas.LoginResponse)
def read_me(current_user: models.User = Depends(get_current_user)):
    return schemas.LoginResponse.from_orm(current_user)
