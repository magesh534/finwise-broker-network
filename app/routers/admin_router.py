from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal as _SessionLocal_dep
from .. import crud

def get_db():
    db = _SessionLocal_dep()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get('/pending')
def pending_brokers(db: Session = Depends(get_db)):
    return crud.get_brokers(db, status='pending')

@router.post('/verify/{broker_id}')
def verify_broker(broker_id: int, approve: bool = True, db: Session = Depends(get_db)):
    status = 'verified' if approve else 'rejected'
    broker = crud.update_broker_status(db, broker_id, status)
    if not broker:
        raise HTTPException(status_code=404, detail='Broker not found')
    return {"msg": f"Broker {status}", "broker": broker}
