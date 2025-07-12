from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.config import SECRET_KEY

if not SECRET_KEY:
    raise ValueError("Secret key is not found")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/client/login")
ALGORITHM = "HS256"

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub") or ""
        role: str = payload.get("role") or ""
        if not user_id or not role:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        print(user_id,role)
        return {"user_id": user_id, "role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
