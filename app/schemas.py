from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# --- [KG3] Endpoint Validation (Pydantic Models) ---

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    dorm_id: int

class UserRead(BaseModel):
    id: int
    email: str
    total_points: int
    dorm_name: str

class ActionCreate(BaseModel):
    action_type_id: int

class ActionUpdate(BaseModel):
    points_earned: int

class ActionRead(BaseModel):
    id: int
    action_name: str
    points_earned: int
    carbon_saved_kg: float
    logged_at: datetime
