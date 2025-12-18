from fastapi import APIRouter, Depends, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from app.database import get_session
from app.models import User, Action, ActionType, Dorm
from app.auth import get_current_user

router = APIRouter(prefix="/fragments", tags=["fragments"])
templates = Jinja2Templates(directory="templates")

# --- [KG8] UI Endpoints & HTMX ---
# These endpoints return HTML snippets, not JSON.

@router.post("/actions/log")
async def log_action_ui(
    request: Request,
    action_type_id: int = Form(...),
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """CREATE (UI): Log an action and return the new HTML row."""
    action_type = session.get(ActionType, action_type_id)
    if not action_type:
        raise HTTPException(status_code=400, detail="Invalid Action Type")

    # Create Action
    new_action = Action(
        user_id=user.id,
        action_type_id=action_type.id,
        points_earned=action_type.base_points,
        carbon_saved_kg=action_type.carbon_impact_kg
    )
    
    # Update Stats
    user.total_points += new_action.points_earned
    if user.dorm:
        user.dorm.total_points += new_action.points_earned
        session.add(user.dorm)
    
    session.add(new_action)
    session.add(user)
    session.commit()
    session.refresh(new_action)
    
    # Return just the new row to prepend to the list
    return templates.TemplateResponse("fragments/action_row.html", {
        "request": request, 
        "action": new_action,
        "edit_mode": False
    })

@router.delete("/actions/{action_id}")
async def delete_action_ui(
    action_id: int,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """DELETE (UI): Delete action and return empty string to remove element."""
    # Logic duplicates the JSON API for safety, but returns HTMX-friendly empty response
    action = session.get(Action, action_id)
    if action and action.user_id == user.id:
        user.total_points -= action.points_earned
        if user.dorm:
            user.dorm.total_points -= action.points_earned
            session.add(user.dorm)
        session.delete(action)
        session.add(user)
        session.commit()
    
    return ""

@router.get("/actions/{action_id}/edit")
async def edit_action_form(
    request: Request,
    action_id: int,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """READ (UI): Return the row in 'edit mode' (inputs instead of text)."""
    action = session.get(Action, action_id)
    return templates.TemplateResponse("fragments/action_row.html", {
        "request": request, "action": action, "edit_mode": True
    })

@router.put("/actions/{action_id}")
async def update_action_ui(
    request: Request,
    action_id: int,
    points_earned: int = Form(...),
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """UPDATE (UI): Save changes and return the row in 'read mode'."""
    action = session.get(Action, action_id)
    if action:
        diff = points_earned - action.points_earned
        action.points_earned = points_earned
        user.total_points += diff
        if user.dorm:
            user.dorm.total_points += diff
            session.add(user.dorm)
        session.add(action)
        session.add(user)
        session.commit()
        session.refresh(action)

    return templates.TemplateResponse("fragments/action_row.html", {
        "request": request, "action": action, "edit_mode": False
    })

@router.get("/leaderboard")
async def get_leaderboard(
    request: Request,
    session: Session = Depends(get_session)
):
    dorms = session.exec(select(Dorm).order_by(Dorm.total_points.desc())).all()
    return templates.TemplateResponse("fragments/leaderboard.html", {
        "request": request, "dorms": dorms
    })
