from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    class Config:
        orm_mode = True

class BrokerCreate(BaseModel):
    name: str
    firm_name: str
    phone: str
    email: EmailStr
    address: str
    license_number: str
    regulator: Optional[str]
    specialization: Optional[str]

class BrokerOut(BaseModel):
    id: int
    name: str
    firm_name: str
    phone: str
    email: EmailStr
    address: str
    license_number: str
    regulator: Optional[str]
    specialization: Optional[str]
    status: str
    rating: int
    class Config:
        orm_mode = True
