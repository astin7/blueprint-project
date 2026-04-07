from fastapi import FastAPI
from app.db.database import engine
from app.db.models import Base

Base.metadata.create_all(bind = engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API running"}