from sqlalchemy.orm import Session
from . import models, schemas

# Users

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, email=user.email, phone=user.phone)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Brokers

def create_broker(db: Session, broker: schemas.BrokerCreate):
    db_broker = models.Broker(**broker.dict())
    db.add(db_broker)
    db.commit()
    db.refresh(db_broker)
    return db_broker

def get_broker_by_license(db: Session, license_number: str):
    return db.query(models.Broker).filter(models.Broker.license_number == license_number).first()

def get_brokers(db: Session, skip: int = 0, limit: int = 20, status: str = None):
    q = db.query(models.Broker)
    if status:
        q = q.filter(models.Broker.status == status)
    return q.offset(skip).limit(limit).all()

def get_broker(db: Session, broker_id: int):
    return db.query(models.Broker).filter(models.Broker.id == broker_id).first()

def update_broker_status(db: Session, broker_id: int, status: str):
    broker = get_broker(db, broker_id)
    if not broker:
        return None
    broker.status = status
    db.commit()
    db.refresh(broker)
    return broker
