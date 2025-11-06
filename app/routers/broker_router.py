from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, Form
from sqlalchemy.orm import Session
from typing import List, Optional, Union
from ..database import SessionLocal
from .. import crud, schemas, utils

# Dependency: get_db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(prefix="/brokers", tags=["brokers"])

@router.post('/', response_model=schemas.BrokerOut)
async def register_broker(
    name: str = Form(...),
    firm_name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    address: str = Form(...),
    license_number: str = Form(...),
    regulator: Optional[str] = Form(None),
    specialization: Optional[str] = Form(None),
    pan: Optional[Union[UploadFile, None, str]] = File(None),
    aadhaar: Optional[Union[UploadFile, None, str]] = File(None),
    db: Session = Depends(get_db)
):
    """
    Register a new broker with optional PAN/Aadhaar uploads.
    Handles empty file inputs gracefully from Swagger UI or frontend forms.
    """

    # Prevent duplicate license numbers
    if crud.get_broker_by_license(db, license_number):
        raise HTTPException(status_code=400, detail="License already registered")

    # Create broker entry
    broker_in = schemas.BrokerCreate(
        name=name,
        firm_name=firm_name,
        phone=phone,
        email=email,
        address=address,
        license_number=license_number,
        regulator=regulator,
        specialization=specialization
    )
    broker = crud.create_broker(db, broker_in)

    # Handle empty string issue from Swagger UI
    if isinstance(pan, str):
        pan = None
    if isinstance(aadhaar, str):
        aadhaar = None

    # Save uploaded files if provided
    base_path = f"uploads/brokers/{broker.id}/"
    if pan:
        path = await utils.save_upload_file(pan, base_path + "pan_" + pan.filename)
        broker.pan = path
    if aadhaar:
        path = await utils.save_upload_file(aadhaar, base_path + "aad_" + aadhaar.filename)
        broker.aadhaar = path

    db.commit()
    db.refresh(broker)
    return broker


@router.get('/', response_model=List[schemas.BrokerOut])
def list_brokers(skip: int = 0, limit: int = 20, status: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Retrieve a paginated list of brokers.
    Optionally filter by status: pending / verified / rejected
    """
    return crud.get_brokers(db, skip=skip, limit=limit, status=status)


@router.get('/{broker_id}', response_model=schemas.BrokerOut)
def get_broker(broker_id: int, db: Session = Depends(get_db)):
    """
    Get details of a single broker by ID.
    """
    b = crud.get_broker(db, broker_id)
    if not b:
        raise HTTPException(status_code=404, detail="Broker not found")
    return b

@router.get('/status/{license_number}')
def get_broker_status(license_number: str, db: Session = Depends(get_db)):
    broker = crud.get_broker_by_license(db, license_number)
    if not broker:
        raise HTTPException(status_code=404, detail="Broker not found")

    return {
        "license_number": broker.license_number,
        "name": broker.name,
        "firm_name": broker.firm_name,
        "status": broker.status,
    }
