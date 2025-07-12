from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.config import SECRET_KEY, ALGORITHM
from cryptography.fernet import Fernet
import base64

if not SECRET_KEY:
    raise ValueError('SECRET Key is not set')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
fernet = Fernet(base64.urlsafe_b64encode(SECRET_KEY[:32].encode()))

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def encrypt_token(email: str) -> str:
    return fernet.encrypt(email.encode()).decode()

def decrypt_token(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()
