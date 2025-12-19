from fastapi import APIRouter, Depends, Form, HTTPException, Response, status, Request
from sqlmodel import Session, select
from app.database import get_session
from app.models import User, Dorm
from app.auth import get_password_hash, verify_password
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/auth", tags=["auth"])
templates = Jinja2Templates(directory="templates")

# --- [KG1] Endpoint Definitions (Auth) ---

@router.post("/register")
async def register(
    email: str = Form(...),
    password: str = Form(...),
    dorm_id: int = Form(...),
    session: Session = Depends(get_session)
):
    # Check if user exists
    existing_user = session.exec(select(User).where(User.email == email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        email=email,
        password_hash=get_password_hash(password),
        dorm_id=dorm_id
    )
    session.add(new_user)
    session.commit()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/login")
async def login(
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session)
):
    user = session.exec(select(User).where(User.email == email)).first()
    if not user or not verify_password(password, user.password_hash):
        # Graceful error handling [KG7]
        return HTMLResponse("<div class='error'>Invalid credentials</div>", status_code=401)
    
    # Simple cookie auth
    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="user_id", value=str(user.id), httponly=True)
    return response

@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("user_id")
    return response
