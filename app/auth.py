from passlib.context import CryptContext
from fastapi import Request, HTTPException, status, Depends
from sqlmodel import Session
from .database import get_session
from .models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# --- [KG4] Dependency Injection (Current User) ---
def get_current_user(request: Request, session: Session = Depends(get_session)) -> User:
    """Retrieves user based on session cookie."""
    user_id = request.cookies.get("user_id")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    user = session.get(User, int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
