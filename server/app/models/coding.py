from beanie import Document, Indexed, PydanticObjectId
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class TestCase(BaseModel):
    input: str
    expected_output: str
    explanation: Optional[str] = None
    is_hidden: bool = False


class Example(BaseModel):
    input: str
    output: str
    explanation: Optional[str] = None


class Solution(BaseModel):
    language: str
    code: str
    explanation: Optional[str] = None


class CodingProblem(Document):
    title: str
    slug: Indexed(str, unique=True)
    description: str
    difficulty: str  # easy | medium | hard
    topics: List[str] = []
    companies: List[str] = []
    input_format: Optional[str] = None
    output_format: Optional[str] = None
    constraints: Optional[str] = None
    examples: List[Example] = []
    test_cases: List[TestCase] = []
    hints: List[str] = []
    solutions: List[Solution] = []
    acceptance_rate: float = 0.0
    submission_count: int = 0
    likes: int = 0
    is_active: bool = True
    order: int = 0
    xp_reward: int = 50
    time_limit_ms: int = 2000
    memory_limit_mb: int = 256
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "coding_problems"


class Submission(Document):
    user_id: PydanticObjectId
    problem_id: PydanticObjectId
    code: str
    language: str
    status: str = "pending"
    execution_time_ms: Optional[int] = None
    memory_used_mb: Optional[float] = None
    test_cases_passed: int = 0
    total_test_cases: int = 0
    error_message: Optional[str] = None
    output: Optional[str] = None
    is_accepted: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "submissions"
