from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class QuestionScores(BaseModel):
    relevance: float = 0
    technical: float = 0
    communication: float = 0
    clarity: float = 0
    confidence: float = 0
    completeness: float = 0


class QuestionResponse(BaseModel):
    id: str = Field(default_factory=lambda: __import__('uuid').uuid4().hex)
    question: str
    question_type: str = "general"
    user_answer: Optional[str] = None
    audio_path: Optional[str] = None
    scores: QuestionScores = QuestionScores()
    feedback: Optional[str] = None
    follow_up_question: Optional[str] = None
    duration: Optional[int] = None
    filler_word_count: int = 0
    word_count: int = 0


class OverallScores(BaseModel):
    overall: float = 0
    communication: float = 0
    technical_knowledge: float = 0
    confidence: float = 0
    problem_solving: float = 0
    clarity: float = 0
    answer_quality: float = 0


class InterviewFeedback(BaseModel):
    strengths: List[str] = []
    areas_to_improve: List[str] = []
    recommended_practice: List[str] = []
    summary: Optional[str] = None


class InterviewSettings(BaseModel):
    difficulty: str = "medium"
    number_of_questions: int = 10
    enable_speech: bool = True


class Interview(Document):
    user_id: PydanticObjectId
    type: str  # 'hr' | 'technical' | 'behavioral' | 'company-specific'
    target_company: Optional[str] = None
    target_role: Optional[str] = None
    status: str = "pending"  # pending | ongoing | completed | abandoned
    questions: List[QuestionResponse] = []
    overall_scores: OverallScores = OverallScores()
    feedback: InterviewFeedback = InterviewFeedback()
    duration: Optional[int] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    settings: InterviewSettings = InterviewSettings()
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "interviews"
