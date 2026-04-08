from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.models import Message, Detection, DetectionReason, Feedback


def create_message(
    db: Session,
    raw_text: str,
    cleaned_text: str | None = None,
    channel: str | None = None,
    sender_info: str | None = None,
    extracted_urls: str | None = None
):
    message = Message(
        raw_text = raw_text,
        cleaned_text = cleaned_text,
        channel = channel,
        sender_info = sender_info,
        extracted_urls = extracted_urls
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def create_detection(
    db: Session,
    message_id: int,
    is_scam: bool,
    confidence: float,
    scam_type: str | None = None,
    recommended_action: str | None = None,
    model_version: str | None = None,
    reasons: list[str] | None = None
):
    detection = Detection(
        message_id = message_id,
        is_scam = is_scam,
        confidence = confidence,
        scam_type = scam_type,
        recommended_action = recommended_action,
        model_version = model_version
    )
    db.add(detection)
    db.commit()
    db.refresh(detection)

    if reasons:
        for reason_text in reasons:
            reason = DetectionReason(
                detection_id = detection.id,
                reason = reason_text
            )
            db.add(reason)

        db.commit()

    return detection


def create_feedback(
    db: Session,
    message_id: int,
    user_feedback: str,
    notes: str | None = None
):
    feedback = Feedback(
        message_id = message_id,
        user_feedback = user_feedback,
        notes = notes
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback


def get_messages_with_detections(db: Session):
    return (
        db.query(Message, Detection)
        .join(Detection, Message.id == Detection.message_id)
        .order_by(Message.created_at.desc())
        .all()
    )


def get_message_detail(db: Session, message_id: int):
    return (
        db.query(Message)
        .filter(Message.id == message_id)
        .first()
    )


def get_stats(db: Session):
    total_messages = db.query(func.count(Message.id)).scalar() or 0

    total_scams_flagged = (
        db.query(func.count(Detection.id))
        .filter(Detection.is_scam == True)
        .scalar() or 0
    )

    average_confidence = db.query(func.avg(Detection.confidence)).scalar() or 0.0

    most_common = (
        db.query(Detection.scam_type, func.count(Detection.scam_type).label("count"))
        .filter(Detection.scam_type.isnot(None))
        .group_by(Detection.scam_type)
        .order_by(func.count(Detection.scam_type).desc())
        .first()
    )

    scam_type_counts_query = (
        db.query(Detection.scam_type, func.count(Detection.scam_type).label("count"))
        .filter(Detection.scam_type.isnot(None))
        .group_by(Detection.scam_type)
        .order_by(func.count(Detection.scam_type).desc())
        .all()
    )

    scam_type_counts = [
        {"scam_type": scam_type, "count": count}
        for scam_type, count in scam_type_counts_query
    ]

    scam_rate = (total_scams_flagged / total_messages) if total_messages > 0 else 0.0

    return {
        "total_messages": total_messages,
        "total_scams_flagged": total_scams_flagged,
        "scam_rate": round(scam_rate, 4),
        "average_confidence": round(float(average_confidence), 4),
        "most_common_scam_type": most_common[0] if most_common else None,
        "scam_type_counts": scam_type_counts
    }