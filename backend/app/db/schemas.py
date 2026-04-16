from pydantic import BaseModel
from typing import Optional, List


class FeedbackCreate(BaseModel):
    message_id: int
    user_feedback: str
    notes: Optional[str] = None


class FeedbackResponse(BaseModel):
    message: str


class DetectionInfo(BaseModel):
    is_scam: bool
    confidence: float
    scam_type: Optional[str] = None
    recommended_action: Optional[str] = None


class MessageSummary(BaseModel):
    message_id: int
    raw_text: str
    channel: Optional[str] = None
    is_scam: bool
    confidence: float
    scam_type: Optional[str] = None


class MessageDetail(BaseModel):
    message_id: int
    raw_text: str
    cleaned_text: Optional[str] = None
    channel: Optional[str] = None
    detection: Optional[DetectionInfo] = None
    reasons: List[str]


class ScamTypeCount(BaseModel):
    scam_type: str
    count: int


class StatsResponse(BaseModel):
    total_messages: int
    total_scams_flagged: int
    scam_rate: float
    average_confidence: float
    most_common_scam_type: Optional[str] = None
    scam_type_counts: List[ScamTypeCount] = []