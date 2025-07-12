from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.utils.security import verify_password, create_access_token, encrypt_token, hash_password
from app.utils.email import send_verification_email
from app.utils.jwt import get_current_user
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db import get_db
from app.models import User, File as FileModel
from app.schemas import SignUpModel, LoginModel
import shutil
import uuid
import os

router = APIRouter()

@router.post("/signup")
async def signup(data: SignUpModel, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(and_(User.email == data.email, User.role == 'ops')))
    if result.scalar():
        raise HTTPException(status_code=400, detail="User exists")
    user = User(email=data.email, password_hash=hash_password(data.password), role="ops")
    db.add(user)
    await db.commit()
    token = encrypt_token(data.email)
    verify_url = f"http://localhost:8000/client/verify/{token}"
    await send_verification_email(data.email,verify_url)
    return {"msg": "Verify your email"}

@router.get("/verify/{token}")
async def verify_email(token: str, db: AsyncSession = Depends(get_db)):
    try:
        email = decrypt_token(token)
    except:
        raise HTTPException(status_code=400, detail="Invalid token")
    result = await db.execute(select(User).where(and_(User.email == email, User.role == 'ops')))
    user = result.scalar()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_verified = True
    await db.commit()
    return {"message": "Email verified please login"}


@router.post("/login")
async def login(data: LoginModel, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(and_(User.email == data.email, User.role == 'ops')))
    user = result.scalar()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=403, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id), "role": 'ops'})
    return {"access_token": token}

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "ops":
        raise HTTPException(status_code=403, detail="Access denied")
    
    if not file.filename:
        raise HTTPException(status_code=400, detail="File must have a filename")
    
    ext = file.filename.split(".")[-1]
    if ext not in {"pptx", "docx", "xlsx"}:
        raise HTTPException(status_code=400, detail="Invalid file type! File must be .pptx .docs .xlsx")

    content = await file.read()

    new_file = FileModel(
        id=uuid.uuid4(),
        filename=file.filename,
        content=content,
        uploaded_by=current_user["user_id"]
    )
    db.add(new_file)
    await db.commit()
    return {"msg": "File uploaded to DB"}