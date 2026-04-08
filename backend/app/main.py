from fastapi import FastAPI
from app.db.database import engine
from app.db.models import Base
from app.api.routes import messages, feedback, stats

Base.metadata.create_all(bind = engine)

app = FastAPI()

app.include_router(messages.router)
app.include_router(feedback.router)
app.include_router(stats.router)


@app.get("/")
def root():
    return {"message": "API running"}