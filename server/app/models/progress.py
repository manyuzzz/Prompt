from beanie import Document, Indexed, PydanticObjectId
from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime


class CodingProgress(BaseModel):
    problems_solved: int = 0
    problems_attempted: int = 0
    easy_solved: int = 0
    medium_solved: int = 0
    hard_solved: int = 0
    topic_wise: Dict[str, int] = {}
    streak: int = 0
    longest_streak: int = 0
    last_solved_date: Optional[datetime] = None
    total_xp: int = 0


class CategoryProgress(BaseModel):
    attempted: int = 0
    correct: int = 0


class AptitudeProgress(BaseModel):
    total_attempted: int = 0
    total_correct: int = 0
    accuracy: float = 0.0
    quantitative: CategoryProgress = CategoryProgress()
    logical: CategoryProgress = CategoryProgress()
    verbal: CategoryProgress = CategoryProgress()
    total_xp: int = 0


class InterviewProgress(BaseModel):
    total_interviews: int = 0
    average_score: float = 0.0
    best_score: float = 0.0
    last_interview_date: Optional[datetime] = None
    total_xp: int = 0


class ResumeProgress(BaseModel):
    current_score: int = 0
    uploads_count: int = 0
    analysis_count: int = 0
    last_analyzed_date: Optional[datetime] = None


class RoadmapProgress(BaseModel):
    active_roadmap_id: Optional[PydanticObjectId] = None
    completion_percentage: float = 0.0
    tasks_completed: int = 0
    tasks_total: int = 0


class WeeklyActivity(BaseModel):
    week: str
    coding_problems: int = 0
    aptitude_questions: int = 0
    interview_sessions: int = 0
    hours_spent: float = 0.0


class Progress(Document):
    user_id: Indexed(PydanticObjectId, unique=True)
    coding: CodingProgress = CodingProgress()
    aptitude: AptitudeProgress = AptitudeProgress()
    interview: InterviewProgress = InterviewProgress()
    resume: ResumeProgress = ResumeProgress()
    roadmap: RoadmapProgress = RoadmapProgress()
    placement_readiness_score: int = 0
    weekly_activity: list = []
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "progress"

    def calculate_placement_readiness(self) -> int:
        coding_score = min(100, (self.coding.problems_solved / 150) * 100)
        aptitude_score = self.aptitude.accuracy
        interview_score = self.interview.average_score
        resume_score = self.resume.current_score
        roadmap_score = self.roadmap.completion_percentage
        streak_score = min(100, (self.coding.streak / 30) * 100)
        score = (
            coding_score * 0.20 +
            aptitude_score * 0.15 +
            interview_score * 0.20 +
            resume_score * 0.15 +
            roadmap_score * 0.15 +
            streak_score * 0.15
        )
        return round(score)
