from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.crud import get_stats
from app.db.schemas import StatsResponse


router = APIRouter()


@router.get("/stats", response_model = StatsResponse)
def stats(db: Session = Depends(get_db)):
    return get_stats(db)