from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.crud import get_messages_with_detections, get_message_detail


router = APIRouter()


@router.get("/messages")
def list_messages(db: Session = Depends(get_db)):
    rows = get_messages_with_detections(db)
    results = []

    for message, detection in rows:
        results.append({
            "message_id": message.id,
            "raw_text": message.raw_text,
            "channel": message.channel,
            "is_scam": detection.is_scam,
            "confidence": detection.confidence,
            "scam_type": detection.scam_type,
            "created_at": message.created_at
        })

    return results


@router.get("/messages/{message_id}")
def get_message(message_id: int, db: Session = Depends(get_db)):
    message = get_message_detail(db, message_id)

    if not message:
        raise HTTPException(status_code = 404, detail = "Message not found")

    detection = message.detection
    reasons = [reason.reason for reason in detection.reasons] if detection else []

    return {
        "message_id": message.id,
        "raw_text": message.raw_text,
        "cleaned_text": message.cleaned_text,
        "channel": message.channel,
        "created_at": message.created_at,
        "detection": {
            "is_scam": detection.is_scam if detection else None,
            "confidence": detection.confidence if detection else None,
            "scam_type": detection.scam_type if detection else None,
            "recommended_action": detection.recommended_action if detection else None
        },
        "reasons": reasons
    }