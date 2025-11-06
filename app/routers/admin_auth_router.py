from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta
from ..database import SessionLocal
from .. import models
import os

router = APIRouter(prefix="/admin-auth", tags=["admin-auth"])

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/login")
def admin_login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    """
    Simple mock admin login.
    Only users with is_admin=True can log in.
    Password is 'admin123' by default.
    """
    admin = db.query(models.User).filter(models.User.email == email, models.User.is_admin == True).first()
    if not admin:
        raise HTTPException(status_code=401, detail="Admin not found or not authorized")

    if password != "admin123":
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(admin.id), "role": "admin"})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/verify-token")
def verify_token(token: str):
    """Validate JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"valid": True, "data": payload}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
