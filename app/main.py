from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select
from app.database import create_db_and_tables, get_session
from app.routers import auth, actions, fragments
from app.models import ActionType, Dorm, Action
from app.auth import get_current_user
import uvicorn

app = FastAPI(title="Mass Impact")

# Include Routers [KG10]
app.include_router(auth.router)
app.include_router(actions.router)
app.include_router(fragments.router)

templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
async def home(request: Request, session: Session = Depends(get_session)):
    # Define all dorms
    all_dorms = [
        {"name": "Southwest", "total_points": 0},
        {"name": "Northeast", "total_points": 0},
        {"name": "Central", "total_points": 0},
        {"name": "Orchard Hill", "total_points": 0},
        {"name": "Sylvan", "total_points": 0},
        {"name": "Honors College", "total_points": 0},
        {"name": "North Apartments", "total_points": 0},
        {"name": "North 116 Apartments", "total_points": 0},
        {"name": "Puffton Apartments", "total_points": 0},
        {"name": "Fieldstone Apartments", "total_points": 0},
    ]
    
    # Define all action types
    all_action_types = [
        {"name": "Turn Off Lights", "description": "Saved electricity", "base_points": 10, "carbon_impact_kg": 1.0},
        {"name": "Recycle", "description": "Recycled items", "base_points": 10, "carbon_impact_kg": 0.5},
        {"name": "Bike to Class", "description": "Skipped the bus", "base_points": 50, "carbon_impact_kg": 2.0},
        {"name": "Use Reusable Bottle", "description": "Avoided single-use plastic", "base_points": 20, "carbon_impact_kg": 0.3},
        {"name": "Compost Food Waste", "description": "Reduced landfill waste", "base_points": 30, "carbon_impact_kg": 1.5},
        {"name": "Short Shower", "description": "Took a shower in under 5 minutes", "base_points": 40, "carbon_impact_kg": 2.5},
        {"name": "Use Public Transport", "description": "Used bus or train instead of car", "base_points": 60, "carbon_impact_kg": 3.0},
        {"name": "Plant a Tree", "description": "Planted a tree on campus", "base_points": 100, "carbon_impact_kg": 5.0},
        {"name": "Bought second-hand Items", "description": "Purchased used goods", "base_points": 25, "carbon_impact_kg": 1.2},
        {"name": "Walked to Class", "description": "Chose to walk instead of drive", "base_points": 15, "carbon_impact_kg": 0.8},
        {"name": "Used energy-efficient appliances", "description": "Opted for appliances that consume less power", "base_points": 35, "carbon_impact_kg": 1.7},
        {"name": "Participated in a campus clean-up", "description": "Helped clean the campus environment", "base_points": 45, "carbon_impact_kg": 2.2},
        {"name": "Donated Clothes", "description": "Donated clothes to charity instead of discarding", "base_points": 30, "carbon_impact_kg": 1.4},
        {"name": "Used LED Bulbs", "description": "Replaced incandescent bulbs with LED", "base_points": 20, "carbon_impact_kg": 1.1},
        {"name": "Meatless Meal", "description": "Chose a vegetarian or vegan meal", "base_points": 25, "carbon_impact_kg": 2.0},
        {"name": "Unplugged Electronics", "description": "Unplugged unused electronics to save energy", "base_points": 15, "carbon_impact_kg": 0.9},
        {"name": "Carpooled", "description": "Shared a ride instead of driving alone", "base_points": 40, "carbon_impact_kg": 2.8},
        {"name": "Used Digital Notes", "description": "Used digital notes instead of paper", "base_points": 10, "carbon_impact_kg": 0.2},
        {"name": "Fixed Instead of Replaced", "description": "Repaired an item instead of buying new", "base_points": 30, "carbon_impact_kg": 1.8},
        {"name": "Attended Sustainability Event", "description": "Participated in a sustainability workshop or event", "base_points": 35, "carbon_impact_kg": 0.5},
    ]
    
    # Get existing dorms and action types
    existing_dorms = {dorm.name for dorm in session.exec(select(Dorm)).all()}
    existing_action_types = {at.name for at in session.exec(select(ActionType)).all()}
    
    # Add missing dorms
    for dorm_data in all_dorms:
        if dorm_data["name"] not in existing_dorms:
            session.add(Dorm(**dorm_data))
    
    # Add missing action types
    for action_type_data in all_action_types:
        if action_type_data["name"] not in existing_action_types:
            session.add(ActionType(**action_type_data))
    
    if existing_dorms != {d["name"] for d in all_dorms} or existing_action_types != {at["name"] for at in all_action_types}:
        session.commit()
    
    dorms = session.exec(select(Dorm)).all()
    return templates.TemplateResponse("login.html", {"request": request, "dorms": dorms})

@app.get("/dashboard")
async def dashboard(
    request: Request, 
    user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    action_types = session.exec(select(ActionType)).all()
    recent_actions = session.exec(select(Action).where(Action.user_id == user.id).order_by(Action.logged_at.desc())).all()
    dorms = session.exec(select(Dorm).order_by(Dorm.total_points.desc())).all()
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
        "action_types": action_types,
        "actions": recent_actions,
        "dorms": dorms
    })

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
