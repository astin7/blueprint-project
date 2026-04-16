from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.crud import create_feedback
from app.db.schemas import FeedbackCreate, FeedbackResponse


router = APIRouter()


@router.post("/feedback", response_model = FeedbackResponse)
def submit_feedback(payload: FeedbackCreate, db: Session = Depends(get_db)):
    create_feedback(
        db = db,
        message_id = payload.message_id,
        user_feedback = payload.user_feedback,
        notes = payload.notes
    )

    return {"message": "Feedback saved successfully"}