from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class Option(BaseModel):
    text: str
    is_correct: bool = False


class AptitudeQuestion(Document):
    question: str
    options: List[Option]
    correct_answer: int  # index of correct option
    explanation: Optional[str] = None
    category: str  # quantitative | logical | verbal
    subcategory: Optional[str] = None
    difficulty: str = "medium"
    companies: List[str] = []
    time_limit_seconds: int = 90
    xp_reward: int = 5
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "aptitude_questions"


class AptitudeAttempt(Document):
    user_id: PydanticObjectId
    question_id: PydanticObjectId
    selected_option: int
    is_correct: bool
    time_taken_seconds: int
    category: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "aptitude_attempts"
