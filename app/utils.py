from fastapi import UploadFile
import shutil
import os

OTP_STORE = {}  # in-memory store for demo {phone_or_email: otp}

def send_otp_mock(to: str) -> str:
    import random
    otp = str(random.randint(100000, 999999))
    OTP_STORE[to] = otp
    print(f"MOCK OTP for {to}: {otp}")
    return otp

async def save_upload_file(upload_file: UploadFile, destination: str) -> str:
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    with open(destination, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return destination
