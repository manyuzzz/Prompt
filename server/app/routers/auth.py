from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.models.user import User
from app.models.progress import Progress
from app.middleware.auth import create_access_token, get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    college: Optional[str] = None
    degree: Optional[str] = None
    branch: Optional[str] = None
    graduation_year: Optional[int] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UpdateProfileRequest(BaseModel):
    name: Optional[str] = None
    college: Optional[str] = None
    degree: Optional[str] = None
    branch: Optional[str] = None
    graduation_year: Optional[int] = None
    skills: Optional[list] = None
    target_role: Optional[str] = None
    target_companies: Optional[list] = None
    cgpa: Optional[float] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None


def user_response(user: User, token: Optional[str] = None) -> dict:
    data = {
        "id": str(user.id),
        "name": user.name,
        "email": user.email,
        "college": user.college,
        "degree": user.degree,
        "branch": user.branch,
        "graduation_year": user.graduation_year,
        "skills": user.skills,
        "target_role": user.target_role,
        "target_companies": user.target_companies,
        "cgpa": user.cgpa,
        "linkedin_url": user.linkedin_url,
        "github_url": user.github_url,
        "xp": user.xp,
        "level": user.level,
        "streak": user.streak,
        "badges": user.badges,
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }
    if token:
        data["token"] = token
    return data


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(body: RegisterRequest):
    existing = await User.find_one(User.email == body.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        name=body.name,
        email=body.email,
        password_hash=User.hash_password(body.password),
        college=body.college,
        degree=body.degree,
        branch=body.branch,
        graduation_year=body.graduation_year,
    )
    await user.insert()
    progress = Progress(user_id=user.id)
    await progress.insert()
    token = create_access_token(str(user.id))
    return {"success": True, "user": user_response(user, token)}


@router.post("/login")
async def login(body: LoginRequest):
    user = await User.find_one(User.email == body.email)
    if not user or not user.verify_password(body.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is inactive")
    token = create_access_token(str(user.id))
    return {"success": True, "user": user_response(user, token)}


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return {"success": True, "user": user_response(current_user)}


@router.post("/reset")
async def reset_progress(current_user: User = Depends(get_current_user)):
    from app.models.coding import Submission
    from app.models.progress import (
        CodingProgress, AptitudeProgress, InterviewProgress,
        ResumeProgress, RoadmapProgress,
    )
    from beanie.odm.operators.find.comparison import In
    import beanie

    # Reset user XP, level, streak, badges
    current_user.xp = 0
    current_user.level = 1
    current_user.streak = 0
    current_user.badges = []
    await current_user.save()

    # Reset progress document
    progress = await Progress.find_one(Progress.user_id == current_user.id)
    if progress:
        progress.coding = CodingProgress()
        progress.aptitude = AptitudeProgress()
        progress.interview = InterviewProgress()
        progress.resume = ResumeProgress()
        progress.roadmap = RoadmapProgress()
        progress.placement_readiness_score = 0
        progress.weekly_activity = []
        await progress.save()

    # Delete all submissions
    await Submission.find(Submission.user_id == current_user.id).delete()

    # Delete roadmaps
    try:
        from app.models.roadmap import Roadmap
        await Roadmap.find(Roadmap.user_id == current_user.id).delete()
    except Exception:
        pass

    # Delete interviews
    try:
        from app.models.interview import Interview
        await Interview.find(Interview.user_id == current_user.id).delete()
    except Exception:
        pass

    return {"success": True, "message": "Progress reset successfully"}


@router.put("/profile")
async def update_profile(body: UpdateProfileRequest, current_user: User = Depends(get_current_user)):
    update_data = {k: v for k, v in body.model_dump().items() if v is not None}
    for key, value in update_data.items():
        setattr(current_user, key, value)
    from datetime import datetime
    current_user.updated_at = datetime.utcnow()
    await current_user.save()
    return {"success": True, "user": user_response(current_user)}
