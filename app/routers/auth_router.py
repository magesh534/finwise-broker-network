from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, auth, utils, models
from ..auth import get_db  # ✅ FIXED: get_db comes from auth.py, not database.py


# We will use a simple dependency below
def get_db():
    db = _SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post('/send-otp')
def send_otp(payload: dict, db: Session = Depends(get_db)):
    # payload: {"to": "email_or_phone"}
    to = payload.get('to')
    if not to:
        raise HTTPException(status_code=400, detail="`to` required")
    utils.send_otp_mock(to)
    return {"msg": "OTP sent (mock). Check server logs."}

@router.post('/verify-otp')
def verify_otp(payload: dict, db: Session = Depends(get_db)):
    to = payload.get('to')
    otp = payload.get('otp')
    if not to or not otp:
        raise HTTPException(status_code=400, detail="`to` and `otp` required")
    if utils.OTP_STORE.get(to) != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    # create or return user
    from ..crud import create_user
    existing = db.query(models.User).filter((models.User.email == to) | (models.User.phone == to)).first()
    if existing:
        user = existing
    else:
        # simple name fallback
        user = create_user(db, schemas.UserCreate(name=to.split("@")[0], email=to if "@" in to else f"{to}@phone.local", phone=to if "@" not in to else "000"))
    token = auth.create_access_token({"sub": str(user.id)})
    return {"access_token": token}
