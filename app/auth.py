from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta
from .database import SessionLocal
from sqlalchemy.orm import Session
from . import models
import os

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

# Dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# very simple JWT util

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# utility to ensure admin exists

def ensure_admin(db: Session):
    admin = db.query(models.User).filter(models.User.is_admin == True).first()
    if not admin:
        admin_user = models.User(name="admin", email="admin@finwise.local", phone="0000000000", is_admin=True)
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        return admin_user
    return admin
