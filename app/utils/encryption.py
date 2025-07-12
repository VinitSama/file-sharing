from cryptography.fernet import Fernet
from app.config import ENCRYPTION_KEY

if not ENCRYPTION_KEY:
    raise ValueError("ENCRYPTION_KEY not found")

fernet = Fernet(ENCRYPTION_KEY)

def encrypt_path(path: str) -> str:
    return fernet.encrypt(path.encode()).decode()

def decrypt_path(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()