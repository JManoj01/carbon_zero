# Mass Impact

A full-stack web application for tracking sustainable actions and carbon impact at UMass Amherst. Users can log environmental actions, earn points, and compete in dorm-based leaderboards.

## Features

- User registration and authentication
- Log sustainable actions (recycling, biking, energy conservation, etc.)
- Track points and carbon impact
- Dorm-based leaderboards
- Real-time UI updates using HTMX
- RESTful API endpoints

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

## Installation

1. Navigate to the project directory:
   ```bash
   cd mass_impact
   ```

2. Create a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   ```

3. Activate the virtual environment:
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Make sure your virtual environment is activated.

2. Run the application:
   ```bash
   python -m app.main
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn app.main:app --reload
   ```

3. Open your browser and navigate to:
   ```
   http://127.0.0.1:8000
   ```

## Testing the Application

1. **Register a new user:**
   - Go to the home page
   - Fill in email, password, and select a dorm
   - Click register

2. **Log in:**
   - Use your registered credentials
   - You'll be redirected to the dashboard

3. **Log actions:**
   - On the dashboard, select an action type
   - Click "Log Action" to record it
   - Points and carbon impact are automatically calculated

4. **View leaderboard:**
   - The dashboard displays dorm rankings
   - Leaderboard updates automatically as actions are logged

5. **Manage actions:**
   - Edit action points by clicking the edit button
   - Delete actions using the delete button

## Project Structure

```
mass_impact/
├── app/
│   ├── main.py           # Application entry point and routes
│   ├── database.py       # Database configuration
│   ├── models.py         # SQLModel data models
│   ├── schemas.py        # Pydantic validation schemas
│   ├── auth.py           # Authentication utilities
│   └── routers/
│       ├── auth.py       # Authentication endpoints
│       ├── actions.py    # CRUD API endpoints
│       └── fragments.py  # HTMX UI endpoints
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   └── fragments/
│       ├── action_row.html
│       └── leaderboard.html
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Database

The application uses SQLite by default (stored in `mass_impact.db`). The database is automatically created on first run. All data persists between application restarts.

To use PostgreSQL instead, update `app/database.py`:
```python
DATABASE_URL = "postgresql://user:password@localhost:5432/mass_impact_db"
```

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Log in
- `GET /auth/logout` - Log out

### Actions API (JSON)
- `GET /api/actions/` - Get all actions for current user
- `PUT /api/actions/{action_id}` - Update an action
- `DELETE /api/actions/{action_id}` - Delete an action

### UI Endpoints (HTMX)
- `POST /fragments/actions/log` - Log a new action
- `GET /fragments/actions/{action_id}/edit` - Get edit form
- `PUT /fragments/actions/{action_id}` - Update action
- `DELETE /fragments/actions/{action_id}` - Delete action
- `GET /fragments/leaderboard` - Get leaderboard fragment

## Technologies Used

- **FastAPI** - Web framework
- **SQLModel** - Database ORM
- **Jinja2** - Template engine
- **HTMX** - Dynamic UI updates
- **Pydantic** - Data validation
- **Passlib** - Password hashing

## Notes

- The application seeds initial dorm and action type data on first access
- User authentication uses simple cookie-based sessions
- All passwords are hashed using bcrypt
- The database file (`mass_impact.db`) will be created in the project root on first run
