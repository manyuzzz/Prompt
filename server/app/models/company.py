from beanie import Document, Indexed
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime


class RecruitmentStage(BaseModel):
    stage: str
    description: Optional[str] = None
    duration: Optional[str] = None
    tips: List[str] = []


class AptitudeSection(BaseModel):
    name: str
    questions: Optional[str] = None
    time: Optional[str] = None
    topics: List[str] = []


class CompanyRole(BaseModel):
    title: str
    description: Optional[str] = None
    type: Optional[str] = None


class SalaryRange(BaseModel):
    min: Optional[str] = None
    max: Optional[str] = None
    currency: str = "INR"


class Company(Document):
    name: str
    slug: Indexed(str, unique=True)
    logo: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[str] = None
    headquarters: Optional[str] = None
    overview: Optional[str] = None
    roles: List[CompanyRole] = []
    eligibility: Dict = {}
    recruitment_process: List[RecruitmentStage] = []
    aptitude_pattern: Optional[Dict] = None
    coding_pattern: Optional[Dict] = None
    technical_topics: List[str] = []
    hr_topics: List[str] = []
    frequently_asked_topics: List[str] = []
    preparation_strategy: Optional[str] = None
    salary_range: Optional[SalaryRange] = None
    tier: str = "tier2"
    is_verified: bool = False
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "companies"
