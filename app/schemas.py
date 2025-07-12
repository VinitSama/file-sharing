from pydantic import BaseModel, EmailStr
from uuid import UUID

class SignUpModel(BaseModel):
    email: EmailStr
    password: str

class LoginModel(SignUpModel):
    pass

class UploaderModel(BaseModel):
    email: str

    class Config:
        orm_mode = True

class FileResponseModel(BaseModel):
    id: UUID
    filename: str
    uploader: UploaderModel
    optionID: int

    class Config:
        orm_mode = True