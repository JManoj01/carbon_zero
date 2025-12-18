from sqlmodel import SQLModel, create_engine, Session
from typing import Generator

# --- [KG6] Persistent Data & Database Configuration ---
# For "out-of-the-box" run, we use SQLite. 
# DATABASE_URL = "postgresql://user:password@localhost/mass_impact_db"
DATABASE_URL = "sqlite:///./mass_impact.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """Dependency for getting DB session."""
    with Session(engine) as session:
        yield session
