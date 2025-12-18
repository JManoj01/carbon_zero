from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

# --- [KG5] Data Model ---

class Dorm(SQLModel, table=True):
    """Represents a dormitory for the leaderboard."""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    total_points: int = Field(default=0, index=True)
    
    users: List["User"] = Relationship(back_populates="dorm")

class User(SQLModel, table=True):
    """Represents a registered user."""
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    dorm_id: Optional[int] = Field(default=None, foreign_key="dorm.id")
    total_points: int = Field(default=0)
    current_streak: int = Field(default=0)
    last_action_date: Optional[datetime] = None

    dorm: Optional[Dorm] = Relationship(back_populates="users")
    actions: List["Action"] = Relationship(back_populates="user")

class ActionType(SQLModel, table=True):
    """Predefined sustainable actions."""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    description: str
    base_points: int
    carbon_impact_kg: float
    
    actions: List["Action"] = Relationship(back_populates="action_type")

class Action(SQLModel, table=True):
    """An instance of a user performing an action."""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    action_type_id: int = Field(foreign_key="actiontype.id")
    points_earned: int
    carbon_saved_kg: float
    logged_at: datetime = Field(default_factory=datetime.now)

    user: Optional[User] = Relationship(back_populates="actions")
    action_type: Optional[ActionType] = Relationship(back_populates="actions")
