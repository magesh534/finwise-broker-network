from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import enum
from .database import Base
from datetime import datetime

class BrokerStatus(str, enum.Enum):
    pending = "pending"
    verified = "verified"
    rejected = "rejected"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)  # optional if using OTP
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Broker(Base):
    __tablename__ = "brokers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    firm_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    address = Column(String, nullable=False)
    license_number = Column(String, nullable=False, unique=True)
    regulator = Column(String, nullable=True)
    specialization = Column(String, nullable=True)
    status = Column(Enum(BrokerStatus), default=BrokerStatus.pending)
    rating = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    # link to documents
    pan = Column(String, nullable=True)
    aadhaar = Column(String, nullable=True)

class BrokerDocument(Base):
    __tablename__ = "broker_documents"
    id = Column(Integer, primary_key=True, index=True)
    broker_id = Column(Integer, ForeignKey("brokers.id"))
    filename = Column(String)
    document_type = Column(String)  # e.g., 'pan', 'aadhaar', 'license'
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    broker = relationship("Broker", backref="documents")
