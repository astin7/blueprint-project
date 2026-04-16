from fastapi import FastAPI
from app.db.database import engine
from app.db.models import Base

# Import all route modules
from app.api.routes import messages, feedback, stats

# Create database tables
Base.metadata.create_all(bind = engine)

# Initialize app
app = FastAPI()

# Include all routers
app.include_router(messages.router)
app.include_router(feedback.router)
app.include_router(stats.router)


# Root endpoint
@app.get("/")
def root():
    return {"message": "API running"}