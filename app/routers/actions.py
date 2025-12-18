from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from app.database import get_session
from app.models import Action, ActionType, User, Dorm
from app.schemas import ActionRead, ActionUpdate
from app.auth import get_current_user

router = APIRouter(prefix="/api/actions", tags=["actions"])

# --- [KG2] HTTP Methods (GET, POST, PUT, DELETE) & [KG7] JSON API ---
# This file handles the raw data logic for the UI to consume via HTMX/Fragments

@router.get("/", response_model=List[ActionRead])
def read_actions(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """READ: Get all actions for current user."""
    return [
        ActionRead(
            id=a.id, 
            action_name=a.action_type.name, 
            points_earned=a.points_earned,
            carbon_saved_kg=a.carbon_saved_kg,
            logged_at=a.logged_at
        ) for a in user.actions
    ]

@router.delete("/{action_id}", status_code=204)
def delete_action(
    action_id: int,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """DELETE: Remove an action."""
    action = session.get(Action, action_id)
    if not action or action.user_id != user.id:
        raise HTTPException(status_code=404, detail="Action not found")
    
    # Deduct points from user and dorm
    user.total_points -= action.points_earned
    if user.dorm:
        user.dorm.total_points -= action.points_earned
        session.add(user.dorm)
        
    session.delete(action)
    session.add(user)
    session.commit()
    return None

@router.put("/{action_id}", response_model=ActionRead)
def update_action(
    action_id: int,
    action_update: ActionUpdate,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """UPDATE: Modify an action (e.g. adjust points manually)."""
    action = session.get(Action, action_id)
    if not action or action.user_id != user.id:
        raise HTTPException(status_code=404, detail="Action not found")
    
    # Adjust difference
    diff = action_update.points_earned - action.points_earned
    
    action.points_earned = action_update.points_earned
    user.total_points += diff
    if user.dorm:
        user.dorm.total_points += diff
        session.add(user.dorm)
        
    session.add(action)
    session.add(user)
    session.commit()
    session.refresh(action)
    
    return ActionRead(
            id=action.id, 
            action_name=action.action_type.name, 
            points_earned=action.points_earned,
            carbon_saved_kg=action.carbon_saved_kg,
            logged_at=action.logged_at
    )
