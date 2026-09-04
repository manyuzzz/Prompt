from beanie import Document, Indexed
from pydantic import EmailStr, Field
from typing import Optional, List
from datetime import datetime
import bcrypt


class Badge(Document):
    name: str
    description: str
    earned_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "badges"


class User(Document):
    name: str
    email: Indexed(EmailStr, unique=True)
    password_hash: str = Field(exclude=True)
    college: Optional[str] = None
    degree: Optional[str] = None
    branch: Optional[str] = None
    graduation_year: Optional[int] = None
    skills: List[str] = []
    target_role: Optional[str] = None
    target_companies: List[str] = []
    cgpa: Optional[float] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    avatar: Optional[str] = None
    xp: int = 0
    level: int = 1
    streak: int = 0
    last_active_date: Optional[datetime] = None
    badges: List[dict] = []
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"

    def verify_password(self, plain_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode(), self.password_hash.encode())

    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode()

    def calculate_level(self) -> int:
        thresholds = [500, 1500, 3000, 5000, 8000, 12000, 17000, 23000, 30000]
        for i, t in enumerate(thresholds):
            if self.xp < t:
                return i + 1
        return 10
