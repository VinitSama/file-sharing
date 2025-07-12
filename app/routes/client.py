from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from io import BytesIO
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.db import get_db
from app.models import User, File as FileModel
from app.utils.email import send_verification_email
from app.utils.security import hash_password, create_access_token, encrypt_token, decrypt_token, verify_password
from app.utils.jwt import get_current_user
from app.utils.encryption import encrypt_path, decrypt_path
from app.schemas import SignUpModel, LoginModel, FileResponseModel
from typing import List
from uuid import UUID

router = APIRouter()

@router.post("/signup")
async def signup(data: SignUpModel, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(and_(User.email == data.email, User.role == 'client')))
    if result.scalar():
        raise HTTPException(status_code=400, detail="User exists")
    user = User(email=data.email, password_hash=hash_password(data.password), role="client")
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
    result = await db.execute(select(User).where(and_(User.email == email, User.role == 'client')))
    user = result.scalar()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_verified = True
    await db.commit()
    return {"message": "Email verified please login"}

@router.post("/login")
async def login(data: LoginModel, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(and_(User.email == data.email, User.role == 'client')))
    user = result.scalar()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=403, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id), "role": 'client'})
    return {"access_token": token}

@router.get("/files", response_model=List[FileResponseModel])
async def list_files(db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "client":
        raise HTTPException(status_code=403, detail="Access denied")
    result = await db.execute(select(FileModel).options(selectinload(FileModel.uploader)))
    files = result.scalars().all()
    return files

@router.get("/download/{option_id}")
async def download_file(
    request: Request,
    option_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "client":
        raise HTTPException(status_code=403, detail="Access denied")

    result = await db.execute(select(FileModel).where(FileModel.optionID == option_id))
    file = result.scalar()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    internal_path = f"{file.id}"
    encrypted_token = encrypt_path(internal_path)

    base_url = str(request.base_url).rstrip("/")
    return {"download_url": f"{base_url}/client/{encrypted_token}"}

@router.get("/{encrypted_token}")
async def handle_encrypted_download(
    encrypted_token: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        decrypted_id = decrypt_path(encrypted_token)
        file_id = UUID(decrypted_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    if current_user["role"] != "client":
        raise HTTPException(status_code=403, detail="Access denied")

    result = await db.execute(select(FileModel).where(FileModel.id == file_id))
    file = result.scalar()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    return StreamingResponse(
        BytesIO(file.content),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{file.filename}"'}
    )
