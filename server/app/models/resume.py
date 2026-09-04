from beanie import Document, Link, PydanticObjectId
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.user import User


class PersonalInfo(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None


class Education(BaseModel):
    institution: Optional[str] = None
    degree: Optional[str] = None
    branch: Optional[str] = None
    cgpa: Optional[str] = None
    start_year: Optional[str] = None
    end_year: Optional[str] = None
    location: Optional[str] = None


class Experience(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    current: bool = False
    description: Optional[str] = None
    bullets: List[str] = []


class Project(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    technologies: List[str] = []
    link: Optional[str] = None
    github: Optional[str] = None
    bullets: List[str] = []


class Skills(BaseModel):
    technical: List[str] = []
    languages: List[str] = []
    tools: List[str] = []
    frameworks: List[str] = []
    databases: List[str] = []
    soft: List[str] = []


class Certification(BaseModel):
    name: Optional[str] = None
    issuer: Optional[str] = None
    date: Optional[str] = None
    link: Optional[str] = None


class CodingProfile(BaseModel):
    platform: Optional[str] = None
    username: Optional[str] = None
    url: Optional[str] = None


class Resume(Document):
    user_id: PydanticObjectId
    title: str = "My Resume"
    personal_info: PersonalInfo = PersonalInfo()
    education: List[Education] = []
    experience: List[Experience] = []
    projects: List[Project] = []
    skills: Skills = Skills()
    certifications: List[Certification] = []
    achievements: List[str] = []
    coding_profiles: List[CodingProfile] = []
    template: str = "ats-professional"
    uploaded_file: Optional[Dict[str, str]] = None
    is_uploaded: bool = False
    is_generated: bool = False
    raw_text: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "resumes"


class AnalysisSuggestion(BaseModel):
    category: str
    suggestion: str
    priority: str = "medium"


class JobMatch(BaseModel):
    job_description: Optional[str] = None
    match_percentage: int = 0
    matched_skills: List[str] = []
    missing_skills: List[str] = []
    relevant_keywords: List[str] = []
    role_suitability: Optional[str] = None
    missing_experience: List[str] = []


class ResumeScores(BaseModel):
    overall: int = 0
    ats: int = 0
    skills: int = 0
    projects: int = 0
    experience: int = 0
    education: int = 0
    keywords: int = 0
    formatting: int = 0


class ResumeAnalysis(Document):
    user_id: PydanticObjectId
    resume_id: Optional[PydanticObjectId] = None
    scores: ResumeScores = ResumeScores()
    extracted_info: Dict[str, Any] = {}
    strengths: List[str] = []
    weaknesses: List[str] = []
    suggestions: List[AnalysisSuggestion] = []
    missing_keywords: List[str] = []
    present_keywords: List[str] = []
    job_match: Optional[JobMatch] = None
    raw_analysis: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "resume_analyses"
