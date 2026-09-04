from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class RoadmapResource(BaseModel):
    title: str
    url: Optional[str] = None
    type: str = "article"


class RoadmapTask(BaseModel):
    id: str = Field(default_factory=lambda: __import__('uuid').uuid4().hex)
    title: str
    description: Optional[str] = None
    type: str = "reading"
    estimated_time: Optional[str] = None
    resources: List[RoadmapResource] = []
    completed: bool = False
    completed_at: Optional[datetime] = None
    priority: str = "medium"
    xp_reward: int = 10


class RoadmapWeek(BaseModel):
    week_number: int
    title: str
    theme: Optional[str] = None
    goals: List[str] = []
    topics: List[str] = []
    tasks: List[RoadmapTask] = []
    completed: bool = False
    completion_percentage: float = 0.0


class RoadmapPhase(BaseModel):
    phase_number: int
    title: str
    description: Optional[str] = None
    weeks: List[RoadmapWeek] = []
    completed: bool = False


class StudentProfile(BaseModel):
    current_year: Optional[str] = None
    degree: Optional[str] = None
    branch: Optional[str] = None
    cgpa: Optional[float] = None
    current_skills: List[str] = []
    programming_language: Optional[str] = None
    dsa_level: str = "beginner"
    aptitude_level: str = "beginner"
    communication_level: str = "average"
    available_hours_per_day: int = 2
    has_projects: bool = False
    has_internship: bool = False
    has_previous_interviews: bool = False


class Roadmap(Document):
    user_id: PydanticObjectId
    title: str
    target_company: Optional[str] = None
    target_role: Optional[str] = None
    duration: int = 12
    student_profile: StudentProfile = StudentProfile()
    phases: List[RoadmapPhase] = []
    todays_tasks: List[RoadmapTask] = []
    completion_percentage: float = 0.0
    is_active: bool = True
    start_date: datetime = Field(default_factory=datetime.utcnow)
    estimated_end_date: Optional[datetime] = None
    generated_by: str = "ai"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "roadmaps"

    def calculate_completion(self) -> float:
        total = 0
        completed = 0
        for phase in self.phases:
            for week in phase.weeks:
                for task in week.tasks:
                    total += 1
                    if task.completed:
                        completed += 1
        return round((completed / total * 100) if total > 0 else 0, 1)
